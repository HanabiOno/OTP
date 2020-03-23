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

with open("../cyphertext0.txt", "r") as cypher0:
    c0 = cypher0.read()
with open("../cyphertext1.txt", "r") as cypher1:
    c1 = cypher1.read()

difference0 = subtract_modulo_alphabet(c0, c1)
difference1 = subtract_modulo_alphabet(c1, c0)

plaintext1 = '-'*len(difference0)
plaintext2 = '-'*len(difference0)

finalstring1 = str_indexer('-'*len(difference0))

# After fifty iterations/trigrams you get the following words
# keys are wordstartindex and values are the word
fitytrigrams = {94: ['UNSAFE'], 633: ['RATTY'], 658: ['VAINLY'], 943: ['RADIATE'], 949: ['DACTYL'], 260: ['YAK'], 374: ['BIZ'], 390: ['IDEA'], 407: ['STARTS'], 708: ['RE'], 790: ['YOGI'], 443: ['SHAFT'], 550: ['ILIAD'], 549: ['WILIER'], 100: ['AT'], 649: ['PA'], 106: ['WORDY'], 480: ['TORI'], 886: ['MANHUNTS'], 680: ['IT'], 141: ['IT'], 846: ['LYRA'], 53: ['SOS'], 125: ['EM'], 340: ['POACH'], 7: ['RHEA'], 758: ['IS'], 932: ['STUB'], 700: ['PA'], 488: ['BRITTLE'], 224: ['DO'], 299: ['BORAX']}
for index in fiftytrigrams:
    finalstring1 = replacer(fiftytrigrams[index], index, finalstring1)
print(str_returner(finalstring1))

finalstring1 = str_indexer('-'*len(difference0))

j = 0
while j < 50:
    with open('../english_trigrams.txt', 'r') as trigrams:
        trigrams = trigrams.readlines()
        couldbeword = {} #safe all words that have english outcome and only use those with value 1, to be sure
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
                    if couldbeenglish(d) == True: #if the word gives a english outcome it is good
                    # There are occurences where there are more then 1 couldbeenglish possibilities at the same wordstartindex
                    # To make sure we have the right one, we only safe it when there is only 1 option
                        if wordstartindex in couldbeword:
                            del couldbeword[wordstartindex]
                        else:
                            couldbeword[wordstartindex] = [word]
            if j%10 == 0:
                print(j)
                print(couldbeword)
            j += 1


for index in couldbeword:
    finalstring1 = replacer(couldbeword[index], index, finalstring1)
print(str_returner(finalstring1))
