from __future__ import annotations

import hashlib
import json
import time
from typing import Any

#1. Hashing, steps from Assignment 1

def sha256_string(s: str) -> str:
    """SHA-256 hex digest of a UTF-8 string."""
    return hashlib.sha256(s.encode("utf-8")).hexdigest()


def canonical_dumps(obj: Any) -> str:
    """Stable JSON string used for hashing (module default canonical form)."""
    return json.dumps(obj, sort_keys=True, separators=(",", ":"))

# 2. Genesis 

# Sentinel value, this is not the hash of a real prior block. 
# lecture's example: sixty-four ASCII zeros.
GENESIS_PREVIOUS_HASH = "0" * 64

# 3. Block class

class Block:
    """A single block in the simplified ledger.

    Material fields (enter the hash commitment):
        index, timestamp, transactions, previous_hash, nonce
    Stored-only field (never fed back into its own pre-image):
        hash
    """

    def __init__(
        self,
        index: int,
        timestamp: int,
        transactions: list[dict[str, Any]],
        previous_hash: str,
        nonce: int = 0,
    ) -> None:
        self.index = index
        self.timestamp = int(timestamp)          # never store a raw float
        self.transactions = transactions
        self.previous_hash = previous_hash
        self.nonce = int(nonce)
        self.hash = self.compute_hash()

    def payload_for_hash(self) -> dict[str, Any]:
        """Material fields used in the hash commitment (excludes `hash`)."""
        return {
            "index": self.index,
            "timestamp": self.timestamp,
            "transactions": self.transactions,
            "previous_hash": self.previous_hash,
            "nonce": self.nonce,
        }

    def compute_hash(self) -> str:
        """hash = SHA256(canonical_json(payload_for_hash()))."""
        raw = canonical_dumps(self.payload_for_hash())
        return sha256_string(raw)

    def to_dict(self) -> dict[str, Any]:
        """Serialise the block including the stored hash (for display/export)."""
        data = self.payload_for_hash()
        data["hash"] = self.hash
        return data

    def __repr__(self) -> str:  # convenience for debugging / demos
        return f"Block(index={self.index}, hash={self.hash[:12]}...)"

# 4. Genesis and linking helpers

def create_genesis_block(timestamp: int | None = None) -> Block:
    """index=0, empty transactions, previous_hash=GENESIS_PREVIOUS_HASH, nonce=0."""
    ts = int(time.time()) if timestamp is None else int(timestamp)
    return Block(
        index=0,
        timestamp=ts,
        transactions=[],
        previous_hash=GENESIS_PREVIOUS_HASH,
        nonce=0,
    )


def create_linked_block(
    previous: Block,
    transactions: list[dict[str, Any]],
    timestamp: int | None = None,
    nonce: int = 0,
) -> Block:
    """Create the next block, linked to `previous` via previous_hash = previous.hash."""
    ts = int(time.time()) if timestamp is None else int(timestamp)
    return Block(
        index=previous.index + 1,
        timestamp=ts,
        transactions=transactions,
        previous_hash=previous.hash,
        nonce=nonce,
    )

# 5. Integrity check

def is_hash_valid(block: Block) -> bool:
    """True if the stored hash matches a fresh recomputation."""
    return block.hash == block.compute_hash()

# 6.proof-of-work

def mine_block(block: Block, difficulty: int = 3) -> Block:
    """Increment nonce until block.hash has `difficulty` leading hex zeros."""
    prefix = "0" * difficulty
    while True:
        block.hash = block.compute_hash()
        if block.hash.startswith(prefix):
            return block
        block.nonce += 1

 
