#!/usr/bin/env python3
# -*-coding:utf-8-*-

"""Spelling Corrector in Python 3; see http://norvig.com/spell-correct.html
Copyright (c) 2007-2016 Peter Norvig
MIT license: www.opensource.org/licenses/mit-license.php
"""

################ Spelling Corrector

import re
import sys
import os
from collections import Counter



class CorrectWord(object):
    def __init__(self,fpath='ML/big.txt',dirpath=''):
        self.__WORDS=None
        self.f=fpath
        self.d=dirpath
        self.word=''
        
    def load_init(self):
        Tem=[]
        if os.path.isfile(self.f):
            Tem.append(open(self.f).read())

        if os.path.isdir(self.d):
            for root,dirs,fs in os.walk(self.d):
                for f in fs:
                    if os.path.splitext(f)[1] == '.txt':
                        Tem.append(open(os.path.join(root,f)).read())

        if len(Tem)>0:
            text='\n'.join(Tem)
            words=re.findall(r'\w',text.lower())
            self.__WORDS = Counter(words)
                
    def P(self):
        "Probability of `word`."
        N=sum(self.__WORDS.values())
        return self.__WORDS[self.word]/N

    def edits1(self):
        "All edits that are one edit away from `word`."
        letters    = 'abcdefghijklmnopqrstuvwxyz'
        splits     = [(self.word[:i], self.word[i:])    for i in range(len(self.word) + 1)]
        deletes    = [L + R[1:]               for L, R in splits if R]
        transposes = [L + R[1] + R[0] + R[2:] for L, R in splits if len(R)>1]
        replaces   = [L + c + R[1:]           for L, R in splits if R for c in letters]
        inserts    = [L + c + R               for L, R in splits for c in letters]
        self.eds1=set(deletes + transposes + replaces + inserts)
        return set(deletes + transposes + replaces + inserts)

    def edits2(self): 
        "All edits that are two edits away from `word`."
        return (e2 for e1 in self.edits1() for e2 in self.edits1(e1))

    def known(self,words): 
        "The subset of `words` that appear in the dictionary of WORDS."
        return set(w for w in words if w in self.__WORDS)

    def candidates(self): 
        "Generate possible spelling corrections for word."
        return (self.known([self.word]) or self.known(self.edits1()) or self.known(self.edits2()) or [self.word])

    def correction(self,word): 
        "Most probable spelling correction for word."
        self.word=word
        if self.__WORDS is None:
            self.load_init()
        return max(self.candidates(), key=self.P)
        
#"""
def words(text):
    return re.findall(r'\w+', text.lower())

def laod(fpath):
    Tem=[]
    if os.path.isfile(fpath):
        Tem.append(open(fpath).read())

    if os.path.isdir(fpath):
        for root,dirs,fs in os.walk(fpath):
            for f in fs:
                if os.path.splitext(f)[1] == '.txt':
                    Tem.append(open(os.path.join(root,f)).read())

    text='\n'.join(Tem)
    words=re.findall(r'\w',text.lower())
    WORDS = Counter(words)
    return WORDS


#WORDS = Counter(words(open('ML/big.txt').read()))
WORDS = laod('ML/big.txt')

def P(word, N=sum(WORDS.values())): 
    "Probability of `word`."
    return WORDS[word] / N

def correction(word): 
    "Most probable spelling correction for word."
    return max(candidates(word), key=P)

def candidates(word): 
    "Generate possible spelling corrections for word."
    return (known([word]) or known(edits1(word)) or known(edits2(word)) or [word])

def known(words): 
    "The subset of `words` that appear in the dictionary of WORDS."
    return set(w for w in words if w in WORDS)

def edits1(word):
    "All edits that are one edit away from `word`."
    letters    = 'abcdefghijklmnopqrstuvwxyz'
    splits     = [(word[:i], word[i:])    for i in range(len(word) + 1)]
    deletes    = [L + R[1:]               for L, R in splits if R]
    transposes = [L + R[1] + R[0] + R[2:] for L, R in splits if len(R)>1]
    replaces   = [L + c + R[1:]           for L, R in splits if R for c in letters]
    inserts    = [L + c + R               for L, R in splits for c in letters]
    return set(deletes + transposes + replaces + inserts)

def edits2(word): 
    "All edits that are two edits away from `word`."
    return (e2 for e1 in edits1(word) for e2 in edits1(e1))
#"""
if __name__=="__main__":
    d=correction(sys.argv[1])
    print(d)
    #cr=CorrectWord()
    pass

