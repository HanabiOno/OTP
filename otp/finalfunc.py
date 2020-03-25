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
    couldbeenglish,
    cleanup,
)

import nltk

with open("../cyphertext0.txt", "r") as cypher0:
    c0 = cypher0.read()
with open("../cyphertext1.txt", "r") as cypher1:
    c1 = cypher1.read()

difference0 = subtract_modulo_alphabet(c0, c1)
difference1 = subtract_modulo_alphabet(c1, c0)

plaintext1 = '-'*len(difference0)
plaintext2 = '-'*len(difference0)

finalstring1 = str_indexer('-'*len(difference0))
finalstring2 = str_indexer('-'*len(difference0))


def helper(b, difference):
    '''This function will return a new dict with the differences the other way around'''
    couldbeword2 = {} #safe all words that have english outcome and only use those with value 1, to be sure
    for key in b: #We'll now go through the english ngrams we found
        c = findwordswithsequence(b[key]) #would return english words with that ngram
        d = []
        for word in c:
            if len(word)>5:
                d.append(word)
        for word in d: #lets go through the words
            upper = b[key].upper()
            wherengraminword = word.find(upper) #where in the word is ngram
            wordstartindex = key - wherengraminword #at what index should word start
            if wordstartindex < 0:
                continue
            dif = addwordtodatindex(difference, word, wordstartindex)
            if couldbeenglish(dif) == True: #if the word gives a english outcome it is good
            # There are occurences where there are more then 1 couldbeenglish possibilities at the same wordstartindex
            # To make sure we have the right one, we only safe it when there is only 1 option
                print(dif, 'wordofsequence is:', word)
                if wordstartindex in couldbeword2:
                    del couldbeword2[wordstartindex]
                else:
                    couldbeword2[wordstartindex] = word
    return couldbeword2

def helper2(couldbeworddict, d=difference1):
    curdict={'empty':'dict'}
    while curdict != {}:
        for idx in couldbeword:
            startidx = idx #will be updated
            endidx = idx + len(couldbeword[idx]) - 1 #will be updated
            reversestring = addwordtodatindex(d, couldbeword[idx], idx) #will be updated
            splitted = nltk.word_tokenize(reversestring)
            print("splitted reversestring", splitted)
            start = splitted[0]
            end = splitted[-1]
            startindex_end = endidx - len(end) +1
            boundarywords = {}
            boundarywords[idx] = start
            boundarywords[startindex_end] = end
            curdict = helper(boundarywords, d)
            if d == difference1:
                d = difference0
            else:
                d = difference1
            print('This is the outcome',boundarywords,helper(boundarywords, d))

j = 0
while j < 5:
    with open('../english_trigrams.txt', 'r') as trigrams:
        trigrams = trigrams.readlines()
        couldbeword = {} #safe all words that have english outcome and only use those with value 1, to be sure
        for trigram in trigrams:
            "current trigram to add to difference0"
            cur_trigram = trigram[:3].lower()
            "a will be the current trigram added to the difference at all possible places"
            a = addwordtod(difference0, cur_trigram)
            b = {} #dic we will use for english ngrams
            i = 0
            while i < len(a): #i is the current ngram we are checking
                if isngram(a[i]): #Check if ngram is an english ngram
                    b[i] =  a[i] #filling the dic with the ngrams with their index as key
                i += 1
            print('------------------------------------------------------------------------------------')
            print('Commong english ngrams after addition',cur_trigram,'to difference0 (keys are index):')
            print(b)
            print("Following passes couldbeenglish after addition findwordswithsequence(commong eng ngram above) to difference1:")

            couldbeword2 = helper(b, difference1)
            for key in couldbeword2:
                couldbeword[key]=couldbeword2[key]

            if j%1 == 0:
                print("These wordstartindices only have one option:", couldbeword)
                finalstring1 = str_indexer('-'*len(difference0))
                #finalstring1 = cleanup(finalstring1, index)
                finalstring2 = str_indexer('-'*len(difference0))
                for index in couldbeword:
                    finalstring1 = replacer(couldbeword[index], index, finalstring1)
                    finalstring1 = cleanup(finalstring1, index)
                    finalstring2 = replacer(addwordtodatindex(difference1, couldbeword[index], index), index, finalstring2)
                    finalstring2 = cleanup(finalstring2, index)
                print("How finalstring1 looks now:", str_returner(finalstring1))
                print("How finalstring2 looks now:", str_returner(finalstring2))

            helper2(couldbeword)
            print('end of loop nr:', j+1)
            j += 1


btest = {318: 'the', 323: 'i'}
btest2 = {381: 'dfather'}
print(helper(btest, difference1))
print(helper(btest2, difference1))

print(addwordtodatindex(difference0, "dfather", 381))
print(couldbeenglish('intervi'))
