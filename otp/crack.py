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

def addwordtod(d, word):
    """This function adds [word] to all possible places in [d(ifference)] and gives all those outputs
Input = difference of two cypher texts (with same otp)
Output = dict where keys are start of difference where word is added and values are the added outcome  """
    list1 = []
    for i in range(0,len(d)-(len(word)-1)):
        list1.append(add_modulo_alphabet(d[i:i+len(word)], word))
    return list1

def addngramtod(d, txt, T=1, n=3):
    """Doesn't work yet! Tries addition of common english ngrams to difference until T (threshold) of the outcomes is also a common english ngram. Threshhold is standard set to 1 and n-gram to 3"""
    with open(txt, 'r') as txt:
        for ngram in txt:
            i = 0
            "when there are T common english n-grams found we stop"
            "ngram[0:n] because the file also contains numbers after each ngram"
            out = addwordtod(d, ngram[0:n])
            while i < T:
                for ngram_out in out:
                    "We want to save the index of the output n-gram if it is a common english n-gram"
                    idx_ngram = []
                    if ngram_out in txt:
                        ngrams_out.append(out.index(ngram_out))
                        i += 1
                    else:
                        continue
        return ngram, idx_ngram
    "We also want to know which common english ngram gave at leat T commonenglish ngrams as output"

