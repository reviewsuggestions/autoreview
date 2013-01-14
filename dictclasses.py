#! /usr/bin/env python

#This is the class definitions for each type of word.

class Word:
  def __init___(self):
    self.wordType = ''
    self.word = ''
  def Type(self):
    return wordType
  def Word(self):
    return word

class Article(Word):
  def __init__(self, string):
    self.word = string
    self.wordType = "Article"

# Function that pluralises a word
def pluralise(string):
  last = string[-1]
  newstr = string[:]
  if last in ['s','x','z','o']:
    newstr += 'es'
  else:
    newstr += 's'
  return newstr

# LUS is True/False, whether the noun is a common LUS noun, ie unicorn
# Pro is True/False, whether it is a pronoun
class Noun(Word):
  def __init__(self, string, LUS, Pro, Plural = ''):
    self.wordType = "Noun"
    self.word = string
    self.LUS = LUS
    self.Pronoun = Pro
    if Plural = '':
      self.Plural = pluralise(string)
    else:
      self.Plural = Plural

# LUS is True/False, whether the noun is a common LUS adjective, ie lavender
class Adjective(Word):
  def __init__(self, string, LUS):
    self.word = string
    self.wordType = "Adjective"
    self.LUS = LUS 

class Adverb(Word):
  def __init__(self, string):
    self.word = string
    self.wordType = "Adverb"

class Conjunction(Word):
  def __init__(self, string):
    self.word = string
    self.wordType = "Conjunction"

#This class may not be used
class Interjection(Word):
  def __init__(self, string):
    self.word = string
    self.wordType = "Interjection" 

# Trivial Conjugation
def trivConj(string, dummy):
  return string

#Conjugates from base to typical third person
def Pres3Conj(string, dummy):
  last = string[-1]
  newstr = string[:]
  if last in ['s','x','z','o']:
    newstr += 'es'
  else:
    newstr += 's'
  return newstr

#Conjugates from base to past tense
def PastConj(string, dummy):
  last = string[-1]
  newstr = string[:]
  if last == 'e':
    newstr += 'd'
  else:
    newstr += 'ed' 
  return newstr

def gerundConj(string, dummy):
  last = string[-1]
  slast = string[-2]
  newstr = string[:]
  if last == 'e':
    if slast =='i':
      newstr = newstr[-2]+'ing'
    else:
      newstr = newstr[:-1]+'ing'
  else:
    newstr += 'ing'
  return newstr

# Function for mapping to the same object as previous, so code doesn't make lots of unnecessary copies
def optionmatch(i, string, optionslist):
  return optionslist[i]

def matchTriv(string, optionslist):
  return optionmatch(0, string, optionslist)

def matchPast(string, optionslist):
  return optionmatch(3, string, optionslist)

# Default functions for each type of conjugation
conjList = [trivConj,matchTriv,Pres3Conj,PastConj,matchPast,matchPast,gerundConj]



class Verb(Word):
  def __init__(self, string, optionslist=[1,1,1,1,1,1,1],stringlist=['']):
    self.type = "Verb"
    self.word = string
    conj = []
    # May reduce if options aren't needed
    for i in range(len(optionslist)):
      if optionslist[i]==1:
        conj.append(conjList[i](string, conj))
      else:
        conj.append(stringlist[0])
        stringlist = stringlist[1:]  
    self.Pres1 = conj[0]
    self.Pres2 = conj[1]
    self.Pres3 = conj[2]
    #self.pluralPres: Same as 2Pres
    self.Past1 = conj[3]
    self.Past2 = conj[4]
    #self.3Past: Same as 1Past
    #self.pluralPast: Same as 2Past
    self.pastPer = conj[5]
    #TODO: Fix this self.presPer : Same as pastPer
    #self.futPer: Same as pastPer
    #self.cond: Same as base
    #self.perfectCond: Same as perfect
    #self.subj: Same as base
    #self.pastSubj: Same as 2Past
    self.gerund = conj[6]
    #self.pastPart: Same as pastPer
    #TODO: self.speaking

def conjTest(verb):
  string = "Base: " + verb.word + "\nPresent:\nI "+ verb.Pres1 +"\nYou "+
           verb.Pres2 +"\nHe/she/it "+ verb.Pres3 + "\nWe/they " + verb.Pres2 
           +"\nPast:\nI "+ verb.Past1 +"\nYou "+ verb.Past2 +"\nHe/she/it "+
           verb.Past1 +"\nWe/they "+ verb.Past2 +
           "\nPast Perfect: I/you/we/they have "+ verb.pastPer+
           "\nPresent Perfect: I/you/we/they had "+ verb.pastPer +
           "\nFuture Perfect: I/you/we/they will have "+ verb.pastPer
           +"\nConditional Perfect: I/you/we/they have "+ verb.pastPer
           +"\nConditional Present: I/you/we/they would "+ verb.word +
           "\nGerund: I am "+ verb.gerund +"\nPast Participle: I have "
           + verb.pastPer
  print string
  return string

