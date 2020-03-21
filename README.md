# Assignment 3: The Lazy Cryptographer
Group members: Zoë, Tom, Jonathan and Hanabi

For this assignment we will crack the code of two encrypted messages by using the fact that they are encrypted with the same one-time-pad (otp).

Input: Two cyphertexts, encrypted with the same otp

Output: The book where the two encrypted passages are from

Functions still needed:

isngram(a, b) - a function that takes a string and an integer and decides if a is an english ngram of length b returns boolean

isenglishword(str1) - a function that takes a string and return True if that string is an english word

findwordswithsequence(str1) - a function that would output a list with all (or as many as we can) words in the english language that have that sequence str1 in it.

addwordtodatindex(dif, word, i) - a function that takes a difference (dif) and adds the string (word) to it at a specified index (i) and returns a string of the symbols that were changed. (so like addwordtod, but with only 1 output instead of a list)

