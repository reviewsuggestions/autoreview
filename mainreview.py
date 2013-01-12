#! /usr/bin/env python
import string, processing, sys, re, errorlisting, operator
import logging

DEBUG = False
COLUMNS = 4

#Done: Ascii converstion(ongoing), wordcounting, character list, sentence counting, Be conjugations/ratios, Words/sentence, Passive sections, Explanations

# This is the main process section for the file

# This function removes bbcode markups from a string and returns the string 
# without the markups
def bbcoderemover(section):
  return re.sub('\[/?[A-Za-z]+\]',"", section)

# This function takes a section of text and dictionaries, wordlist and capslist, 
# and and integer specifying wordcount, splits the text into words, strips off 
# punctuation and extraneous characters, and counts the words, returning a tuple 
# containing updated wordlist, capslist and wordcount. 
# Added periodcount which will likely be removed
def wordcounter(section, wordlist, capslist, wordcount, periodcount):
  words = section.split()
  for word in words:
    if '.' in word:
      periodcount += 1
    word = word.strip('[]/\:;,-><()\"\'*.?!')
    #possibly (',.?!-;:\'\"')
    #remove 's possessive
    if word[-2:] == "'s":
      word = word[:-2]
    if word != '':
      if word[0].isupper():
        if word in capslist:
          capslist[word] += 1
        else:
          capslist[word] = 1
      #Words in wordlist are lowercase
      word = word.lower()
      if word in wordlist:
        wordlist[word] += 1
      else:
        wordlist[word]=1
      wordcount += 1
  return (wordlist, capslist, wordcount, periodcount)

# Generates a list of words that are almost always capitalised and the most commonly capitalised dictionary
def charlistgenerator(wordlist, capslist, wordcount):
  charcount = 0
  chardict = []
  charlist = set(['Fluttershy', 'Pinkie', 'Rainbow', 'Dash', 'Rarity', 'Twilight', 'Sparkle', 'Applebloom', 'Apple', 'Bloom', 'Bon', 'Braeburn', 'Celestia', 'Cheerilee', 'Colgate', 'Derpy', 'Discord', 'Gilda', 'Luna', 'Lyra', 'Octavia', 'Pipsqueak', 'Blueblood', 'Scootaloo', 'Snails', 'Snips', 'Soarin', 'Spike', 'Spitfire', 'Sweetie', 'Belle', 'Trixie', 'Twist', 'Vinyl', 'Zecora','I','Mr','Mrs','Ms','Dr','Mister','Miss','Doctor', 'Chrysalis', 'Cadance','Sombra', 'Canterlot', 'Manehattan', 'Ponyville', 'Appleloosa', 'Equestria'])
  for (k,v) in capslist:
    kfloat = float(wordlist[k.lower()])
    if kfloat/v<1.1 and charcount < 15 and k!="I" and k!="I'm" and k!="I've" and k!="I'd" and k!="I'll" and wordcount/v<1500:
      chardict.append((k,v))
      charcount+=1
    if v>=3 and kfloat/v<1.26 and k!="I" and k!="I'm" and k!="I've" and k!="I'd" and k!="I'll":
      charlist.add(k)
  return (chardict,charlist)

# This sanitises mouseover text of doublequotes so it doesn't break up the title string
def sanitise(string):
  newstring = ""
  for char in string:
    if char == '"':
      newstring += "''"
    else:
      newstring += char
  return newstring


# This function takes the completed Error object and generates the html listing of errors
def listtohtml(errorobject):
  #TODO: handle in debugmode
  string = '<br><a href=\"' + errorobject.link + '\" title=\"' + errorobject.mouseover +'\"><h3>' + errorobject.errormsg + '</a></h3><br>'
  temp = errorobject.listing
  for obj in temp:
    if obj != []:
      mouseover = obj[0]
      obj = obj[1:]
      for item in obj:
        string += '<a title=\"' + sanitise(mouseover) + '\">' + item +'</a><br>'
  return string

def counttohtml(errorobject):
  return '<br><a href=\"' + errorobject.link + '\" title=\"' + errorobject.mouseover +'\"><b>' + errorobject.errormsg + '</b></a>: ' + str(errorobject.count) + '<br>'

# Function that writes other statistics to the appropriate output
def statstohtml(heading, value, link = '', explanation = ''):
  if link != '':
    return '<br><a href=' + link + 'title=\"' + sanitise(explanation) + '\"><b>'+heading+':</b></a> '+str(value)+'<br>'
  else:
    return '<br><b>'+heading+':</b> '+str(value)+'<br>'

# Function that writes ratio statistics to the appropriate output
def ratiotohtml(heading, value, lastword='', link = '', explanation = ''):
  if link != '':
    return '<br><a href=' + link + 'title=\"' + sanitise(explanation) + '\"><b>'+heading+':</b></a> 1 every'+str(value)+' '+lastword+'<br>'
  else:
    return '<br><b>'+heading+':</b> 1 every '+str(value)+' '+lastword+'<br>' 

#Titlecase function that capitalises the first letter of a word
def titlecase(s):
  return re.sub(r"[A-Za-z]+('[A-Za-z]+)?",lambda mo: mo.group(0)[0].upper() + mo.group(0)[1:].lower(),s)

# Function that outputs the wordlist in html
# Expects a sorted list of (word, int) pairs, a dictionary containing caps, set of characters, and an int for the number of columns
# Outputs a string of html
def wordlisthtml(sortedwordlist, capsdict, columns):
  string = '<h2>Wordcounts</h2><br>This section contains wordcounts. The first number is total and the second is the number of capitalised occurrences.<br><table><tr><td>'
  columncounter = 0
  for (k,v) in sortedwordlist:
    if titlecase(k) in capsdict:
      string += k + " " + str(v) +" - " + str(capsdict[titlecase(k)])
    else:
      string += k + " " + str(v) +" - 0"
    if (columncounter % columns) == (columns - 1):
      string += "</td></tr>\n<tr><td>"
    else:
      string += "</td><td>&nbsp;</td><td>"
    columncounter += 1
  string +="</td></tr></table>"
  return string  

# This is the main process. It takes a string 
# TODO: Make re-entrant (possibly)
# optionslist is (CapsPeriod, PassiveVoice, DialogueComma, DialoguePeriod, DialogueFront, PunctSpace, DoubleSpace, RandCaps, PunctOutsideQuote, ParagraphCaps, EndingPunct) 3 is completely omit, 1 is listing fully, 2 is just counting
# Outputsuppress is (wordlist, adverbs, uncommonwords, characters), 0 omits, 1 allows
def mainprocess(string, optionslist=[1,2,1,1,1,1,1,1,2,1,1], outputsuppress=[1,1,1,1]):
  optionscorrespond = errorlisting.initialise()
  wordlistsuppress = outputsuppress[0]
  adverbsuppress = outputsuppress[1]
  uncommonsuppress = outputsuppress[2]
  charsuppress = outputsuppress[3]
  wordcount = 0
  periodcount = 0
  capslist = {}
  wordlist = {}
  # Convert to recognisable format (ASCII)
  temp = processing.asciiconvert(string)
  # Add char warnings for large numbers of unrecognised characters
  string = temp[0]
  chartuple = temp[1]
  # Remove bbcode markup
  string = bbcoderemover(string)
  # Generate basic tools and stats
  temp = wordcounter(string, wordlist, capslist, wordcount, periodcount)
  wordlist = temp[0]
  capslist = temp[1]
  wordcount = temp[2]
  periodcount = temp[3]
  # Output is data for future use
  output = []
  output.append(wordcount)
  output.append(periodcount)
  beconjugations = 0
  for item in ('was','were','is','are','be','been'):
    beconjugations += wordlist[item]
  # Note: Ensure this is performed exactly once if re-entrance
  # Perhaps by defining a progress class
  sortedcapslist = sorted(capslist.iteritems(), key=operator.itemgetter(1), reverse=True)
  # charlistgenerator expects a dict for wordlist and a sorted list for capslist 
  temp = charlistgenerator(wordlist, sortedcapslist, wordcount)
  charlist = set(temp[1])
  chardict = temp[0]
  wordlist = sorted(wordlist.iteritems(), key=operator.itemgetter(1), reverse=True)
  if wordlistsuppress == 1:
    wordhtml = wordlisthtml(wordlist, capslist, COLUMNS)

  # split large string into lines, may happen earlier once length checking occurs
  string = string.split('\n')
  length = len(optionslist)
  for line in string:
    # Run error-checking
    for i in range(length):
      if optionslist[i]==1:
        temp = errorlisting.regexcheckclass(optionscorrespond[i], line, charlist)
        if temp != []:
          optionscorrespond[i].addtolist(temp)
      if optionslist[i]==2:
        optionscorrespond[i].addcount(errorlisting.regexcountclass(optionscorrespond[i], line, charlist))
  #Random statistics
  wordspersentence = float(wordcount)/periodcount
  if beconjugations != 0:
    beratio = wordcount/beconjugations
    besentence = float(periodcount)/beconjugations
  vocabwords = len(wordlist)
  # Compute adverbs and uncommonwords
  # Adverbs may be deprecated by sentence processing
  commonwordscounter = 0
  commonwordlist = []
  adverbscount = 0
  if adverbsuppress+uncommonsuppress > 0: #At least one is 1
    for (k,v) in wordlist:
      if uncommonsuppress == 1 and not(k in errorlisting.commonwords) and commonwordscounter < 12 and not(titlecase(k) in charlist):
        commonwordlist.append((k,v))
        commonwordscounter += 1
      if adverbsuppress == 1 and len(k)>2 and k[-2:]=="ly":
        adverbscount += v
  

  # Writing the output to html
  htmloutput = '<html><table border="0"><tr><td width="10%"></td><td><body>'
  htmloutput = '<h1>Review:</h1><br>Thanks for using autoreview. Any suggestions would be appreciated. You can contact me via email at reviewsuggestions(at)gmail(dot)com.<br>Note: The program is not perfect, so please check before making any changes<br><br>'
  htmloutput += statstohtml("Wordcount",wordcount)
  htmloutput += statstohtml("Sentences", periodcount)
  htmloutput += statstohtml("Words Per Sentence", wordspersentence)  
  htmloutput += statstohtml("Be Conjugations (was/were/is/are/be/been)",beconjugations)
  if beconjugations !=0:
    htmloutput += ratiotohtml("Be conjugation frequency", beratio, "words")
    htmloutput += ratiotohtml("Sentences containing be", besentence, "sentences")
  if adverbsuppress == 1:
    htmloutput += statstohtml("Adverbs occurrences", adverbscount)
    if adverbscount != 0:
      adverbsratio = wordcount/adverbscount
      htmloutput += ratiotohtml("Adverb frequency", adverbsratio, "words")

  #Output uncommonwords
  if uncommonsuppress == 1:
    htmloutput += "<hr> <h3>Uncommon words</h3><br>These are the most commonly occurring words from your fic that do not occur in the top 250 most common words.<br>"
    for (k,v) in commonwordlist:
      htmloutput += k + " " + str(v)+"<br>"

  if charsuppress == 1:
    htmloutput += "<hr><h3>Character List</h3><br>These are the most common words that occurred nearly always capitalised. As such, these should be major characters, places or other proper nouns within your story.<br>"
    for (k,v) in chardict:
      htmloutput += k + " " + str(v)+"<br>"
    
  temp = ''
  for i in range(length):
    if optionslist[i]==1 and optionscorrespond[i].listing != []:
       temp += listtohtml(optionscorrespond[i])+'<hr>'
    if optionslist[i]==2:
       htmloutput += counttohtml(optionscorrespond[i])
  htmloutput += '<hr><h2>Error listing:</h2><br>Each section contains suspected occurrences of errors. You can hover over the section heading for a short decription or click the section heading to go to a page with a longer explanation.<br>Hovering over each listed occurrence allows you to see the paragraph where the suspected error came from.<br>'+temp
  if wordlistsuppress == 1:
    htmloutput += wordhtml
  htmloutput += '</td><td width="10%"></td></tr></table></body></html>'
  return (htmloutput, chartuple, output)
