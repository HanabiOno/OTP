# A first hint at how one might go about cracking the codes.

from otp import (
    one_time_pad,
    otp_encrypt,
    subtract_modulo_alphabet,
    add_modulo_alphabet,
)

# Make two short plaintexts using only lowercase letters.

plaintext1 = "the cat sat on the mat"
plaintext2 = "happy birthday to you"

# Make a random one time pad as long as the longer plaintext
otp0 = one_time_pad(max(len(plaintext1), len(plaintext2)))

# Encrypt with the otp
cyphertext1, _ = otp_encrypt(plaintext1, otp0)
cyphertext2, _ = otp_encrypt(plaintext2, otp0)

# Take the difference between the cyphertexts
d = subtract_modulo_alphabet(cyphertext2, cyphertext1)

# Now suppose we guess that the word 'the' occurs in plaintext1.
guess1 = add_modulo_alphabet(d, "the-------------------")

# 'hapm59ffw2laj)xx$5vz3'

# Notice how the first three letters are 'hap'. That might be part of an
# English word.

# Now suppose we guess that the word 'the' occurs at another place in the
# string.
guess2 = add_modulo_alphabet(d, "---------the----------")

# 'lq)m59ffw.VHj)xx$5vz3'

# The three corresponding letters are now '.VH' a combination that is highly
# unlikely to occur in English text.

# Continuing to test in this way gives some clues as to what letters appear
# where in the plaintexts. Now write some code to automate the process!
