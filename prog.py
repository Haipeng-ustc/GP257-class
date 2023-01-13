#!/usr/bin/env python

def printMany(word:str,n:int):
  """ I print word n times"""
  for i in range(n):
    print(word)



if __name__ == "__main__":
  printMany("Hello world",10)
