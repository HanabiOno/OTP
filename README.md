# The Lazy Cryptographer
Contributors: Zoë, Tom, Jonathan and Hanabi

For our code you need the nltk package, this can be installed in the following way:
sudo apt-get install python3-pip
pip3 install nltk

For this projects we will crack the code of two encrypted messages by using the fact that they are encrypted with the same one-time-pad (otp).

For this code we used a number of helperfunctions, most of which are in the crack.py file, which is in the otp folder, with their respective descriptions.

The final overarching function that uses these helperfunctions is in finalfunc.py(also in the otp folder) which takes the two cyphertext and returns more filled in versions of both passages. To use finalfunc.py you have to run it in your command line. The program will loop over the first most common trigrams and give you possible words these trigrams produce on both passages, it will show you an option with two strings and ask you if you wnat to keep them. You can type y for yes and n for no, you should only type y for strings that seem plausible and like good english (a word ending in v is very unlikely for instance). This goes on until you think that the passages sufficiently filled in, there are still some gaps allowed, but you have to be able to guess what can go in between the gaps. Then these more filled in passages can be given as input to func_loop, which is in crack.py and allows you to guess the missing gaps until you have filled passages. You have to give guesses at for the empty indexes, look what the output is and either accept or decline that output by typing yes or no respectively.

These passages can be googled to find out from which book they are.

The textfiles with book 1-5 are used to make a dictionary of the most common English words. The dictionary.txt file is used to found out if a word is actually English. The english_trigram.txt and english_quadgram.txt file contain the most commoon ngrams and are used as input for the final function.

Unittests for our helperfunctions can be found in the file unittests.py, which is also in the otp folder.

Our sources can be found in the wiki.





