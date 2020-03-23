from otp import (
    one_time_pad,
    otp_encrypt,
    subtract_modulo_alphabet,
    add_modulo_alphabet,
)
from crack import(
    isngram,
    isenglishword,
    findwordswithsequence,
    addwordtodatindex,
    replacer,
    str_indexer,
    addwordtod,
    str_returner,
    couldbeenglish
)
c0 = open("../cyphertext0.txt", "r")
c1 = open("../cyphertext1.txt", "r")

difference0 = subtract_modulo_alphabet(c0.read(), c1.read())
difference1 = subtract_modulo_alphabet(c1.read(), c0.read())

print("difference1 is:", c1.read(), c0.read(), subtract_modulo_alphabet(c1.read(), c0.read()))

plaintext1 = '-'*len(difference0)
plaintext2 = '-'*len(difference0)

finalstring1 = str_indexer('-'*len(difference0))
cont = 'yes'
while cont == 'yes':
    with open('../english_trigrams.txt', 'r') as trigrams:
        trigrams = trigrams.readlines()
        for trigram in trigrams:
            "current trigram to add to difference0"
            cur_trigram = trigram[:3]
            "a will be the current trigram added to the difference at all possible places"
            a = addwordtod(difference0, cur_trigram)
            b = {} #dic we will use for english ngrams
            i = 0
            print("trigram is", cur_trigram)
            while i < len(a): #i is the current ngram we are checking
                if isngram(a[i]): #Check if ngram is an english ngram
                    b[i] =  a[i] #filling the dic with the ngrams with their index as key
                i += 1
            print('the english ngrams from a', b)
            for key in b: #We'll now go through the english ngrams we found
                c = findwordswithsequence(b[key]) #would return english words with that ngram
                for word in c: #lets go through the words
                    upper = b[key].upper()
                    wherengraminword = word.find(upper) #where in the word is ngram
                    wordstartindex = key - wherengraminword #at what index should word start
                    d = addwordtodatindex(difference1, word, wordstartindex)
                    print(word, wordstartindex)
                    if couldbeenglish(d) == True: #if the whole word makes sense we move on
                        replacer(word, wordstartindex, finalstring1)
                        break
            print(str_returner(finalstring1))
            cont = input("Type yes if you want to continue to next trigram")
