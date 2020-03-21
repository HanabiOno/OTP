
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
e = subtract_modulo_alphabet(cyphertext1, cyphertext2)

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

c0 = open("cyphertext0.txt", "r")
c1 = open("cyphertext1.txt", "r")
difference0 = subtract_modulo_alphabet(c0.read(), c1.read())
difference1 = subtract_modulo_alphabet(c1.read(), c0.read())
#def str_builder(): #builds a string the size of the otp
#    length = len(otp0)
#    output_str = ''
#    for i in range(length):
#        output_str += '-'
#    return output 
        
def replacer(word, index, lst): #takes in a string and replaces a part of a give string from a certain position with the inputted word                                                                    
    counter = 0
    new_list = []
    for i in range(len(lst)):
        temp_list = ['','']
        if i >= index and i < index+len(word):
            temp_list[0]= i
            temp_list[1] = word[counter]
            new_list.append(temp_list)
            counter += 1
        else:
            new_list.append(lst[i])
            
    return new_list


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

def isngram(str):
    #Takes a string str and decides if str is an ngram.
    str = str.upper()
    if len(str) == 3:
        with open("english_trigrams.txt", "r") as f:
            data = f.readlines()
        for line in data:
            if str in line:
                return True
        return False
    if len(str) == 4:
        with open("english_quadgrams.txt", "r") as f:
            data = f.readlines()
        for line in data:
            if str in line:
                return True
        return False
    
def isenglishword(str):
    #Takes a string str and return True if that string is a word, False otherwise
    str = str.upper()
    with open("dictionary.txt", "r") as d:
        dictionary = d.readlines()
    for line in dictionary:
        if str in line:
            return True
    return False
    
def findwordswithsequence(str):
    #Takes a string str and outputs a list with all words that contain str
    str = str.upper()
    words_with_str = []
    with open("dictionary.txt", "r") as d:
        dictionary = d.readlines()
    for line in dictionary:
        if str in line:
            words_with_str.append(line[0:-1])
    return words_with_str

def addwordtodatindex(d, word, index):
    #Takes a difference d, and adds word to d at index, returns a string with the new changed symbols.
    word_length = len(word)
    return add_modulo_alphabet(d[index:(index + word_length)], word)
    

'''
def couldbeenglish(str1): # A function that takes a string and returns True if the string looks like english
    CAPITALS = ("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
    SPECIALS = ("!\"#$%'()*-/0123456789:;?@[]\n") #removed spacebar period and comma for acuracy. Not sure if newline will cause major issues.
    OSPECIALS = (" .,")
    LETTERS = ("abcdefghijklmnopqrstuvwxyz")
    i=0
    while i < len(str1) - 1:
        if str1[i] in CAPITALS and str1[i+1] in CAPITALS:
            return False
        elif str1[i] in SPECIALS and str1[i+1] in SPECIALS:
            return False
        elif str1[i] in CAPITALS and str1[i+1] in SPECIALS:
            return False
        elif str1[1] in LETTERS and str1[i+1] in CAPITALS:
            return False
        i += 1
    indexofspecials = [] #list of the indexes of special symbols
    i=0
    while i < len(str1):
        if str1[i] in SPECIALS or str1[i] in OSPECIALS:
            indexofspecials.append(i)
        i += 1
    if not indexofspecials: #if the list is empty
        return couldsubbeenglish(lower(str1))
    checkcount = 0 #to see if we actually did any real checks
    if 0 not in indexofspecials: #let's check the first symbols up to the first special
        tmpstring = str1[:indexofspecials[0]]
        if len(tmpstring) > 2:
            if couldsubbeenglish(lower(tmpstring)) == False:
                return False
            else:
                checkcount += 1
    if len(str1) - 1 not in indexofspecials: #let's check the symbols after the last special
        tmpstring = str1[indexofspecials[-1]:]
        if len(tmpstring) > 2:
            if couldsubbeenglish(lower(tmpstring)) == False:
                return False
            else:
                checkcount += 1
    i=0
    #Let's check if the symbols between the specials make english words
    while i + 1 < len(indexofspecials):
        if not isenglishword(str1[indexofspecials[i]+1:indexofspecials[i+1]-1]):
            return False
        else:
            checkcount += 1
        i += 1
    if checkcount > 0:
        return True
            
#helper function for couldbeenglish. Takes an input that is only letters and at least 3 long and returns a boolean if it could be english
def couldsubbeenglish(str1):
    if not isngram(str1[:2], 3):
        return False
    elif len(str1) == 3:
        return True
    else:
        if len(str1[3:]) > 2:
            return couldsubbeenglish(str1[3:])
        else:
            return couldsubbeenglish(str1[1:3])
'''

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
        for j in c: #lets go through the words
           #  addwordtodatindex(dif, word, index) a function that would only do addwordtod at a specific index
            wherengraminword = j.find(b[key]) #where in the word is the ngram
            wordstartindex = key - wherengraminword #at what index should word start
            d = addwordtodatindex(dif2, j, wordstartindex) #see explanation above
           # couldbeenglish(d) is a function that checks if a string could be english
            if couldbeenglish(d) == True: #if the whole word makes sense we move on
                finalstring1 = finalstring1[:wordstartindex -1] + j + finalstring1[wordstartindex + len(j):] #Change finalstring1 to contain the word we found
                break
    return finalstring1

#now we have a string where a bunch of the "-" have been replaced with words. Now we can use these words to find words in the other string (finalstring2). We could keep doing this interchangingly until we have rather full strings

def proofofconceptp2
'''

def str_indexer(strng):
    lst =[]
    index_position = 0
    for letter in strng:
        temp_lst = []
        temp_lst.append(index_position)
        temp_lst.append(letter)
        lst.append(temp_lst)
        index_position += 1
    return lst 
        

def input_module(c1_c2, c2_c1, string1, string2):
    choice = input("Choose string to start from: (1/2)")
    user_index = eval(input('Enter index you want to start from: '))
    user_word = input('Enter word: ')
    if choice == '1':
        output_2 = add_modulo_alphabet(e[user_index:user_index+len(user_word)], user_word)
        output_1 = add_modulo_alphabet(d[user_index:user_index+len(user_word)], output_2)
    if choice == '2':
        output_1 = add_modulo_alphabet(d[user_index:user_index+len(user_word)], user_word)
        output_2 = add_modulo_alphabet(e[user_index:user_index+len(user_word)], output_1)
    
    return(replacer(output_1,  user_index, string1), replacer(output_2,  user_index, string2))
    
    
def func_loop(string1, string2):
    new_str1 = str_indexer(string1)
    new_str2 = str_indexer(string2)
    user_input ='yes'
    while user_input == 'yes' or user_input == 'yes ':
        print(new_str1)
        print('------------------------------------------------------------------------------')
        print(new_str2)
        temp1, temp2 = input_module(d, e, new_str1, new_str2)
        print(temp1)
        print('------------------------------------------------------------------------------')
        print(temp2)
        second_input = input('Do you want to keep this string?:')
        if second_input == 'yes' or second_input == 'yes ':
            new_str1 = temp1
            new_str2 = temp2
        user_input = input("Type yes if you want to continue")




func_loop("hap-----------------", "----------------------")

