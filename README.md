# BLCH9X2 Block_Chain
Blockchain assignment 1 2026
SimpleBlockchain: Assignment 1: Cryptographic Hash Lab

BLCH9X2 — Blockchain (MFE), University of Johannesburg

Student: Phenyo Thato Molete Student number: 216038155 Due date: 5 August 2026

What this is

A small module implementing the cryptographic primitives covered in Lecture 01, which later assignments build on: SHA-256 hashing of strings and files, the avalanche effect, and a toy proof-of-work nonce search.

Requirements
Python 3.10+
Standard library only (hashlib, time), no installs needed.
bash
pip install -r requirements.txt   # currently empty — stdlib only
How to run
Developed and tested in Google Colab. To run locally instead:
bash
python3 cryptography.py

This prints, in order:

SHA-256 digests of several test strings (PhenyoMFE, phenyomfe, IamsuperHungry, IAMSUPERhungry): demonstrating that hashing is case-sensitive: a single letter-case change produces a completely different digest.
SHA-256 of an uploaded file (BLOCKCHAINASSIGNMENTDOC.rtf), computed before and after changing a single comma inside it: showing the avalanche effect on real file content.
An avalanche-effect demo on the string "PhenyoMFE": flips a single bit of the last character and reports how many of the 256 output bits differ (measured: 124/256, 48.44%).
A proof-of-work parameter study: finds a nonce so the hash starts with n leading hex zeros, for n = 3 and n = 4, reporting the nonce, digest, attempt count, and elapsed time for each.
Project layout
.
├── cryptography.py     # sha256_string, sha256_file, avalanche_demo,
│                        # bit_difference, proof_of_work
├── requirements.txt
└── README.md
Notes for the report
All hash values, attempt counts, and timings in the submitted report are taken directly from my own Colab run — not fabricated.
AI assistance: I used Claude (Anthropic) for guidance on Python syntax and structuring the four required functions, following the patterns demonstrated in the Lecture 01 class notebook. I wrote, ran, and tested all code myself in Google Colab, chose my own test inputs, and wrote the reflection in my own words based on my own measured results.
