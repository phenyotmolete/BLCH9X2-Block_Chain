#Block itself is imported from block.py (Assignment 2)

from __future__ import annotations

import time
from typing import Any, Optional

from block import Block, GENESIS_PREVIOUS_HASH, create_genesis_block


class Blockchain:
    """An ordered sequence of blocks, each committing to the previous
    block's hash, with explicit rules for appending and for verifying
    the whole sequence.
    """

    def __init__(self) -> None:
        self.chain: list[Block] = [create_genesis_block(timestamp=0)]

    def tip(self) -> Block:
        """The most recently appended block — the only legal parent for
        the next append.
        """
        return self.chain[-1]

    def append_block(self, block: Block) -> None:
        """Append `block` only if all three writer-protection gates pass:
            1. block.index == tip.index + 1          (ordering)
            2. block.previous_hash == tip.hash        (link)
            3. block.hash == block.compute_hash()     (self-commitment)
        Raises ValueError, and leaves the chain unchanged, if any gate fails.
        """
        tip = self.tip()
        if block.index != tip.index + 1:
            raise ValueError(f"bad index: expected {tip.index + 1}, got {block.index}")
        if block.previous_hash != tip.hash:
            raise ValueError("bad previous_hash: does not match chain tip")
        if block.hash != block.compute_hash():
            raise ValueError("stored hash does not match recomputation")
        self.chain.append(block)

    def verify_chain(self, difficulty: Optional[int] = None) -> bool:
        """Return True iff the full chain is internally consistent.

        Reader-protection pillars, checked for every block:
            1. Genesis is at index 0 with the correct previous_hash sentinel.
            2. Every block's stored hash matches a fresh recomputation
               (self-hash integrity).
            3. Every non-genesis block's previous_hash matches the prior
               block's actual (current) hash (link integrity).
            4. (Optional) if `difficulty` is given, every non-genesis
               block's hash must start with that many leading hex zeros.
        """
        if not self.chain:
            return False

        genesis = self.chain[0]
        if genesis.index != 0 or genesis.previous_hash != GENESIS_PREVIOUS_HASH:
            return False
        if genesis.hash != genesis.compute_hash():
            return False

        prefix = ("0" * difficulty) if difficulty is not None else None

        for i in range(1, len(self.chain)):
            cur, prev = self.chain[i], self.chain[i - 1]
            if cur.index != i:
                return False
            if cur.hash != cur.compute_hash():
                return False
            if cur.previous_hash != prev.hash:
                return False
            if prefix is not None and not cur.hash.startswith(prefix):
                return False

        return True

    def __len__(self) -> int:
        return len(self.chain)

    def __repr__(self) -> str:
        return f"Blockchain(blocks={len(self.chain)})"


def make_next_block(chain: Blockchain, transactions: list[Any], nonce: int = 0) -> Block:
    """Build the next block pointing at the current tip (no mining yet).
    The caller is responsible for mining it (if a difficulty rule will be
    enforced) before passing it to chain.append_block().
    """
    tip = chain.tip()
    return Block(
        index=tip.index + 1,
        timestamp=int(time.time()),
        transactions=transactions,
        previous_hash=tip.hash,
        nonce=nonce,
    )
