
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
d = subtract_modulo_alphabet(cyphertext0, cyphertext12)

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

#c0 = open("cyphertext0.txt", "r")
#c1 = open("cyphertext1.txt", "r")
#difference0 = subtract_modulo_alphabet(c0.read(), c1.read())
#difference1 = subtract_modulo_alphabet(c1.read(), c0.read())
#def str_builder(): #builds a string the size of the otp
#    length = len(otp0)
#    output_str = ''
#    for i in range(length):
#        output_str += '-'
#    return output 
        
def replacer(word, index, strng): #takes in a string and replaces a part of a give string from a certain position with the inputted word
    lst = list(strng)
    counter = 0
    for i in range(len(strng)):
        if i >= index and i < index+len(word):
            if lst[i] == '-': 
                lst[i] = word[counter]
                counter += 1
    ''.join(lst)
    return lst

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
        txt = txt.readlines() 
        for index in range(len(txt)): 
            txt[index] = txt[index][0:n]
        for ngram in txt:
            i = 0
            "when there are T common english n-grams found we stop"
            "ngram[0:n] because the file also contains numbers after each ngram"
            out = addwordtod(d, ngram)
            while i < T:
                for ngram_out in out:
                    "We want to save the index of the output n-gram if it is a common english n-gram"
                    idx_ngram = []
                    if ngram_out in txt:
                        ngrams_out.append(out.index(ngram_out))
                        i += 1
                    
                break #think this should work.                         
        return ngram, idx_ngram
    "We also want to know which common english ngram gave at leat T commonenglish ngrams as output"

'''
#Concept of overarching function, dif1 and dif2 are the two modulo differences
def proofofconceptp1(dif1, dif2):
    a = addwordtod(dif1, "the") #all the results from 'the'
    b = {} #dic we will use for english ngrams
    finalstringlength = len(dif1)
    finalstring1 = "-" * finalstringlength #The finalstring of one of the cypher texts
    i = 0
    while i < len(a): #i is the current ngram we are checking
        if isngram(a[i], 3): #A function that would check if the input is an english ngram
            b[i] =  a[i] #filling the dic with the ngrams with their index as key
    for key in b: #We'll now go through the ngrams we found                
        c = findwordswithsequence(b[key]) #would return english words with that ngram
        j = 0
        for j in c: #lets go through the words
           #  addwordtodatindex(dif, word, index) a function that would only do addwordtod at a specific index
            wherengraminword = j.find(b[key]) #where in the word is the ngram
            wordstartindex = key - wherengraminword #at what index should word start
            d = addwordtodatindex(dif2, j, wordstartindex) #see explanation above
            remainingword = j
            makesresultsense = True
            while len(remainingword) > 2: #We check if the word would work 
                if not isngram(remainingword[:2], 3):
                    makesresultsense = False #if it doesn't, we'll go to the next
                    break
                else:
                    remainingword = remainingword[3:]
            if makesresultsense == True: #if the whole word makes sense we move on
                finalstring1 = finalstring1[:wordstartindex -1] + j + finalstring1[wordstartindex + len(j):] #Change finalstring1 to contain the word we found
                break
    return finalstring1

#now we have a string where a bunch of the "-" have been replaced with words. Now we can use these words to find words in the other string (finalstring2). We could keep doing this interchangingly until we have rather full strings

def proofofconceptp2
'''
