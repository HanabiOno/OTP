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

c0 = open("../cyphertext0.txt", "r")
c1 = open("../cyphertext1.txt", "r")
difference0 = subtract_modulo_alphabet(c0.read(), c1.read())
difference1 = subtract_modulo_alphabet(c1.read(), c0.read())
#def str_builder(): #builds a string the size of the otp
#    length = len(otp0)
#    output_str = ''
#    for i in range(length):
#        output_str += '-'
#    return output

def replacer(word, index, lst): #takes in a list replacing a certain part, from the given index, by an inputted word
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

def isngram(str, start = False, end = False):
    #Takes a string str and booleans that decide if the ngram should be at a special location, and decides if str is an ngram.
    str = str.upper()
    with open("../dictionary.txt", "r") as d:
        dictionary = d.readlines()
    for line in dictionary:
        if start == True and len(line[:-1]) >= len(str):
            if str == line[:len(str)]:
                return True
            else:
                continue
        elif end == True and len(line[:-1]) >= len(str):
            if str == line[-1 - len(str):-1]:
                return True
            else:
                continue
        else:
            if str in line:
                return True
    return False

def isenglishword(str):
    #Takes a string str and return True if that string is a word, False otherwise
    str = str.upper()
    with open("../dictionary.txt", "r") as d:
        dictionary = d.readlines()
    for line in dictionary:
        if str == line[0:-1]:
            return True
    return False


def findwordswithsequence(str):
    #Takes a string str and outputs a list with all words that contain str
    str = str.upper()
    words_with_str = []
    with open("../dictionary.txt", "r") as d:
        dictionary = d.readlines()
    for line in dictionary:
        if str in line:
            words_with_str.append(line[0:-1])
    #including the str itself
    if isenglishword(str) and (str not in words_with_str):
        words_with_str.append(str)
    return words_with_str

def addwordtodatindex(d, word, index):
    #Takes a difference d, and adds word to d at index, returns a string with the new changed symbols.
    word_length = len(word)
    return add_modulo_alphabet(d[index:(index + word_length)], word)

def couldbeenglish(str1): # A function that takes a string and returns True if the string looks like english
    CAPITALS = ("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
    IGNORED = ("%$#*/@")#No functionality for these symbols
    NUMBERS = ("0123456789")
    OPENERS = ("([")
    CLOSERS = (")]")
    ENDSPECIALS = (".,!:;?")
    CONNECTORS = ("-")
    QUOTES = ("\"'")
    BREAKS = (" \n")
    LETTERS = ("abcdefghijklmnopqrstuvwxyz")
    i=0
    while i < len(str1):
        if str1[i] in IGNORED:
            return False
        i += 1
    i=0
    while i < len(str1) - 1:
        if str1[i] in CAPITALS and str1[i+1] not in LETTERS:
            return False
        elif str1[i+1] in CAPITALS:
            if str1[i] in OPENERS:
                i += 1
                continue
            elif str1[i] in QUOTES:
                i += 1
                continue
            elif str1[i] in BREAKS:
                i += 1
                continue
            else:
                return False
        elif str1[i] in NUMBERS:
            if str1[i+1] in OPENERS:
                return False
            elif str1[i+1] in CONNECTORS:
                return False
            elif str1[i+1] in LETTERS:
                return False
        elif str1[i+1] in NUMBERS:
            if str1[i] in CLOSERS:
                return False
            elif str1[i] in ENDSPECIALS:
                return False
            elif str1[i] in CONNECTORS:
                return False
            elif str1[i] in LETTERS:
                return False
        elif str1[i] in OPENERS:
            if str1[i+1] in OPENERS:
                return False
            elif str1[i+1] in CLOSERS:
                return False
            elif str1[i+1] in ENDSPECIALS:
                return False
            elif str1[i+1] in CONNECTORS:
                return False
            elif str1[i+1] in BREAKS:
                return False
        elif str1[i+1] in OPENERS and str1[i] not in BREAKS:
            return False
        elif str1[i] in CLOSERS:
            if str1[i+1] in CLOSERS:
                return False
            elif str1[i+1] in CONNECTORS:
                return False
            elif str1[i+1] in QUOTES:
                return False
            elif str1[i+1] in LETTERS:
                return False
        elif str1[i+1] in CLOSERS:
            if str1[1] in CONNECTORS:
                return False
            elif str1[1] in BREAKS:
                return False
        elif str1[i] in ENDSPECIALS:
            if str1[i+1] in ENDSPECIALS:
                return False
            elif str1[i+1] in CONNECTORS:
                return False
            elif str1[i+1] in LETTERS:
                return False
        elif str1[i+1] in ENDSPECIALS:
            if str1[i] in CONNECTORS:
                return False
            elif str1[i] in QUOTES:
                return False
            elif str1[i] in BREAKS:
                return False
        elif str1[i] in CONNECTORS and str1[i+1] not in LETTERS:
            return False
        elif str1[i+1] in CONNECTORS and str1[i] not in LETTERS:
            return False
        elif str1[i] in QUOTES and str1[i+1] in QUOTES:
            return False
        elif str1[i] in BREAKS and str1[i+1] in BREAKS:
            return False
        i += 1 
    i=0
    while i < len(str1) - 2:
        if str1[i+1] in NUMBERS and str1[i] in OPENERS and str1[i+2] in QUOTES:
            return False
        elif str1[i+1] in NUMBERS and str1[i] in QUOTES and str1[i+2] in CLOSERS:
            return False
        elif str1[i+1] in QUOTES:
            if str1[i] in OPENERS:
                if str1[i+2] in CLOSERS:
                    return False
                elif str1[i+2] in BREAKS:
                    return False
            elif str1[i] in ENDSPECIALS:
                if str1[i+2] in CAPITALS:
                    return False
                elif str1[i+2] in LETTERS:
                    return False
                elif str1[i+2] in NUMBERS:
                    return False
            elif str1[i] in NUMBERS or str1[i] in LETTERS:
                if str1[i+2] in CAPITALS:
                    return False
                elif str1[i+2] in NUMBERS:
                    return False
                elif str1[i+2] in LETTERS:
                    return False
        elif str1[i+1] in BREAKS and str1[i] in LETTERS and str1[i+2] in CAPITALS:
            return False
        elif str1[i+1] in LETTERS:
            if str1[i] in CAPITALS:
                if str1[i+2] in CLOSERS or str1[i+2] in ENDSPECIALS or str1[i+2] in QUOTES or str1[i+2] in BREAKS:
                    if isenglishword(str1[i:i+1]) == False:
                        return False
            elif str1[i] in OPENERS or str1[i] in QUOTES:
                if str1[i+2] in CLOSERS or str1[i+2] in ENDSPECIALS or str1[i+2] in QUOTES:
                    return False
                elif str1[i+2] in BREAKS:
                    if isenglishword(str1[i+1]) == False:
                        return False
            elif str1[i] in BREAKS:
                if str1[i+2] in CLOSERS or str1[i+2] in ENDSPECIALS or str1[i+2] in QUOTES or str1[i+2] in BREAKS:
                    if isenglishword(str1[i+1]) == False:
                        return False
        i += 1    
    indexofspecials = [] #list of the indexes of special symbols
    i=0
    while i < len(str1):
        if str1[i] in IGNORED or str1[i] in NUMBERS or str1[i] in OPENERS or str1[i] in CLOSERS or str1[i] in ENDSPECIALS or str1[i] in CONNECTORS or str1[i] in QUOTES or str1[i] in BREAKS:
            indexofspecials.append(i)
        i += 1
    if not indexofspecials: #if the list is empty
        if str1[0] in CAPITALS:
            return isngram(str1, start = True)
        return isngram(str1)
    checkcount = 0 #to see if we actually did any real checks
    if 0 not in indexofspecials: #let's check the first symbols up to the first special
        tmpstring = str1[:indexofspecials[0]]
        if len(tmpstring) > 2:
            if tmpstring[0] in CAPITALS:
                if isenglishword(tmpstring) == False:
                    return False
                else:
                    checkcount += 1
            else:
                if isngram(tmpstring, end = True) == False:
                    return False
                else:
                    checkcount += 1
        else:
            if tmpstring[0] in CAPITALS:
                if isenglishword(tmpstring) == False:
                    return False
            else:
                if isngram(tmpstring, end = True) == False:
                    return False
    if len(str1) - 1 not in indexofspecials: #let's check the symbols after the last special
        tmpstring = str1[indexofspecials[-1] + 1:]
        if len(tmpstring) > 2:
            if isngram(tmpstring, start = True) == False:
                return False
            else:
                checkcount += 1
        else:
            if isngram(tmpstring, start = True) == False:
                return False
    i=0
    #Let's check if the symbols between the specials make english words
    while i + 1 < len(indexofspecials):
        if indexofspecials[i] + 1 != indexofspecials[i + 1]:
            if not isenglishword(str1[indexofspecials[i]+1:indexofspecials[i+1]]):
                return False
            else:
                checkcount += 1
        i += 1
    if checkcount > 0:
        return True
    else:
        return False

'''
#Concept of overarching function, dif1 and dif2 are the two modulo differences
def proofofconceptp1(dif1, dif2):
    a = addwordtod(dif1, "the") #all the results from 'the'
    b = {} #dic we will use for english ngrams
    finalstringlength = max(len(dif1), len(dif2))
    finalstring1 = "-" * finalstringlength #The finalstring of one of the cypher texts
    i = 0
    while i < len(a): #i is the current ngram we are checking
        if isngram(a[i]): #Check if ngram is an english ngram
            b[i] =  a[i] #filling the dic with the ngrams with their index as key
        i += 1
    for key in b: #We'll now go through the english ngrams we found
        c = findwordswithsequence(b[key]) #would return english words with that ngram
        for word in c: #lets go through the words
            upper = b[key].upper()
            wherengraminword = word.find(upper) #where in the word is ngram
            wordstartindex = key - wherengraminword #at what index should word start
            d = addwordtodatindex(dif2, word, wordstartindex)
            if couldbeenglish(d) == True: #if the whole word makes sense we move on
                finalstring1 = finalstring1[:wordstartindex -1] + word + finalstring1[wordstartindex + len(word):] #Change finalstring1 to contain the word we found
                break
    return finalstring1

#now we have a string where a bunch of the "-" have been replaced with words. Now we can use these words to find words in the other string (finalstring2). We could keep doing this interchangingly until we have rather full strings

#def proofofconceptp2
'''

def str_indexer(strng): #takes in a string and returns a list with the letters and their index positions
    lst =[]
    index_position = 0
    for letter in strng:
        temp_lst = []
        temp_lst.append(index_position)
        temp_lst.append(letter)
        lst.append(temp_lst)
        index_position += 1
    return lst


def input_module(c1_c2, c2_c1, string1, string2):#allows for user testing of the string
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

def str_returner(lst): #takes in a str, indexed list from str_indexer, and returns a singles string
    new_list = []
    for i in range(len(lst)):
        new_list.append(lst[i][1])
    return ''.join(new_list)

def func_loop(string1, string2):# a function that allows for the continual guessing of the correct word.
    new_str1 = str_indexer(string1)
    new_str2 = str_indexer(string2)
    user_input ='yes'
    while user_input == 'yes' or user_input == 'yes ':
        print(new_str1)
        print('------------------------------------------------------------------------------')
        print(new_str2)
        temp1, temp2 = input_module(d, e, new_str1, new_str2)
        print(str_returner(temp1))
        print('------------------------------------------------------------------------------')
        print(str_returner(temp1))
        second_input = input('Do you want to keep this string?:')
        if second_input == 'yes' or second_input == 'yes ':
            new_str1 = temp1
            new_str2 = temp2
        user_input = input("Type yes if you want to continue")

def cleanup (strng, index):#if collisions occur in the list, it removes the undesired letters. 
    counter = 0
    if (index-counter) > 0: #makes sure word is not at the beginning of a sentence
        while strng[index-counter][1] != '-':
            strng[index-counter][1] = '-'
            if index-counter > 0:
                counter += 1
    counter_2 = index + 1
    if counter_2 < (len(strng)-1): #makes sure word is not at the end of a sentence
        while strng[counter_2][1] != '-':
            strng[counter_2][1] = '-'
            if index+counter_2 <= (len(strng)-1):
                counter_2 += 1
        
    return strng
    


#func_loop("hap-----------------", "----------------------")


def pop_dict_creator(book_list, popularity_dict):
    #Takes a list of books and makes a dictionary of the words in these books
    for books in book_list:
        with open(books, 'r') as book:
            lines = book.readlines()
            for sentence in lines:
                splitted = sentence.split()
                for word in splitted:
                    word = word.lower()
                    if word not in popularity_dict:
                        popularity_dict[word] = 1
                    else:
                        popularity_dict[word] += 1
    return popularity_dict
    
def str_returner_word(lst, index_start):#from a given index in our list, returns it as a string. 

    new_list = []
    counter = 0
    while lst[index_start+counter][1] != '-':
        new_list.append(lst[index_start+counter][1])
        counter += 1
    return ''.join(new_list)
            
def chooser(word1, word2, pop_dict):#given two words, decideds which word to keep. 
    temp1 = word1.lower()
    temp2 = word2.lower()
    if temp1 in pop_dict and temp2 in pop_dict:
        if pop_dict[temp1] > pop_dict[temp2]:
            return word1
        else:
            return word2
    elif temp1 in pop_dict:
        return word1
    elif temp2 in pop_dict:
        return word2
    else:
        if len(word1) > len(word2):
            return word1
        else:
            return word2
    
def finder(lst, index): #finds beginning index of a string
    counter = 1
    while lst[index-counter][1] != '-':
        counter += 1
    return (index-counter + 1)

def collision_finder(lst, word, index): #find collisions between words (if they have the same index)
    if lst[index][1] != '-':
        return ([True, index])
    for i in range(len(word)):
        if lst[index+i+1][1] != '-':
            return [True, index+i+1]
    return [False, 'None']



def lst_replacer (finalstring, couldbeword, index, pop_dict): #adds a new word to our string and resolves any collisions that would occur
    if collision_finder(finalstring, couldbeword, index)[0] == True:
        if collision_finder(finalstring, couldbeword, index)[1] > index:
            collisionword = str_returner_word(finalstring, collision_finder(finalstring, couldbeword, index)[1])
            word = chooser(couldbeword, collisionword, pop_dict)
            if word == couldbeword:
                finalstring = cleanup(finalstring, collision_finder(finalstring, couldbeword, index)[1])
                finalstring = replacer(word, index, finalstring)
        
        else:
            start_index = finder(finalstring, index)
            collisionword = str_returner_word(finalstring, start_index)
            word = chooser(couldbeword, collisionword, pop_dict)
            if word == couldbeword:
                finalstring = cleanup(finalstring, start_index)
                finalstring = replacer(word, index, finalstring)
                
                
        return finalstring
    
    else:
        finalstring = replacer(couldbeword, index, finalstring)
        return finalstring
    
    
