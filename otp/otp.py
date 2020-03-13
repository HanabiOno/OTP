#!/usr/bin/env python
# -*- mode: python; coding: utf-8; -*-

"""
One-time Pads
"""

__author__ = "Breanndán Ó Nualláin"
__author_email__ = "<o@uva.nl>"

from random import randrange
import subprocess
import operator
import re
from os import stat

# Acceptable characters. We will filter out all others.
ALPHABET = (
    "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    "abcdefghijklmnopqrstuvwxyz"
    " !\"#$%'()*,-./0123456789:;?@[]\n"
)
ALPHABET_SIZE = len(ALPHABET)


def purify_file(infile, outfile):
    """Copy one file to another, removing characters not in ALPHABET."""
    with open(outfile, "w") as out:
        out.write(purify_text(open(infile).read()))


def purify_text(text):
    """Copy text, removing characters not in ALPHABET."""
    return "".join(c for c in text if c in ALPHABET)


def random_text(bookfile, size=1000):
    """Return a block of text of length SIZE from a random place in the
bookfile. All carriage returns, linefeeds and multiple spaces are replaced by
a single space.
"""
    length = file_size(bookfile)
    with open(bookfile, "r") as book:
        book.seek(randrange(length - size))
        return re.sub(r"\r\n|\s+", " ", book.read(size))


def file_size(filename):
    return stat(filename).st_size


def random_text_file(bookfile, rand_file, size=1000):
    """Write a file containing a random block of text of the given size from the
given book file.

    """
    text = random_text(bookfile, size)
    with open(rand_file, "w") as r:
        r.write(text)


def one_time_pad(length, alphabet=ALPHABET):
    """A random one-time pad."""
    lalph = len(alphabet)
    return "".join([alphabet[randrange(lalph)] for _n in range(length)])


def otp_encrypt(text, otp=None):
    """Encrypt the text with a given or generated OTP."""
    if not otp:
        otp = one_time_pad(len(text))
    cyphertext = add_modulo_alphabet(text, otp)
    return cyphertext, otp


def otp_decrypt(cyphertext, otp):
    """Decrypt the cyphertext using the one-time pad."""
    return subtract_modulo_alphabet(cyphertext, otp)


def add_mod(x, y, m):
    return (x + y) % m


def sub_mod(x, y, m):
    return (x - y) % m


def add_modulo_alphabet(s1, s2, alphabet=ALPHABET):
    """Add two strings modulo the alphabet."""
    sum = [
        alphabet[add_mod(alphabet.find(c1), alphabet.find(c2), len(alphabet))]
        for c1, c2 in zip(s1, s2)
    ]
    return "".join(sum)


def subtract_modulo_alphabet(s1, s2, alphabet=ALPHABET):
    """Subtract two strings modulo the alphabet."""
    diff = [
        alphabet[sub_mod(alphabet.find(c1), alphabet.find(c2), len(alphabet))]
        for c1, c2 in zip(s1, s2)
    ]
    return "".join(diff)


def generate_otp_file(otp_file, size=1000):
    """Generate a file containing a one-time pad of the given size over the
alphabet.

    """
    otp = "".join([ALPHABET[randrange(ALPHABET_SIZE)] for _n in range(size)])
    with open(otp_file, "w") as o:
        o.write(otp)


def otp_encrypt_file(plain_file, cypher_file, otp_file):
    """Encrypts contents of plaintext file using a newly generated one-time pad.
Writes cyphertext and OTP to given files in blocks.

    """
    with open(plain_file, "r") as p:
        plaintext = p.read()
    cyphertext, otp = otp_encrypt(plaintext)
    with open(cypher_file, "w") as c:
        c.write(cyphertext)
    with open(otp_file, "w") as o:
        o.write(otp)


def otp_decrypt_file(cypher_file, otp_file, plain_file):
    """Decrypts the cypher_file using the OTP in otp_file and writes the
resulting plaintext to plain_file.

    """
    with open(cypher_file, "r") as c:
        cyphertext = c.read()
    with open(otp_file, "r") as o:
        otp = o.read()
    plaintext = subtract_modulo_alphabet(cyphertext, otp)
    with open(plain_file, "w") as p:
        p.write(plaintext)


def encrypt_with_otp_file(plain_file, otp_file, cypher_file):
    """Encrypts contents of plaintext file using a given one-time pad. Writes
cyphertext to given files.

    """
    with open(plain_file, "r") as p:
        plaintext = p.read()
    with open(otp_file, "r") as o:
        otp = o.read()
    cyphertext = add_modulo_alphabet(plaintext, otp)
    with open(cypher_file, "w") as c:
        c.write(cyphertext)


def generate_team_files(team, book_file, blocks=2):
    otp_file = "otp%d.txt" % team
    generate_otp_file(otp_file)
    block_start = 0
    for block in range(block_start, block_start + blocks):
        block_file = "team%d-block%d.txt" % (team, block)
        enc_file = "team%d-enc%d.txt" % (team, block)
        dec_file = "team%d-dec%d.txt" % (team, block)
        random_text_file(book_file, block_file)
        encrypt_with_otp_file(block_file, otp_file, enc_file)
        otp_decrypt_file(enc_file, otp_file, dec_file)


### eof.
