#! /usr/bin/env python
import sys, string, re, operator
import time
import logging
import dictreturn




def titlecase(s):
        return re.sub(r"[A-Za-z]+('[A-Za-z]+)?",
                      lambda mo: mo.group(0)[0].upper() +
                                 mo.group(0)[1:].lower(),
                      s)

def writetuple(filename, string, value):
	s = str(value)
	s = string + " " + s + "<br>"
	return filename + s

def regcounter(line, counter, regex):
	for string in regex:
		matchObj = string.findall(line)
		if len(matchObj)>0:
			counter += len(matchObj)
	return counter
			

#This clears the unicode character that is encoded by 128 secondchar
def clearword(word, secondchar, string):
	linetarget = True
	while(linetarget):
		for i in range(len(word)-1):
			if ord(word[i])==128 and ord(word[i+1])==secondchar:
				if i>0 and i+2<len(word):
					word = word[:i-1] + string + word[i+2:]
					break
				elif i==0:
					word = string + word[i+2:]
					break					
				else:
					word = word[:i-1] + string
					break
			if i==len(word)-2:
				linetarget = False
		if len(word)<2:
			linetarget = False
	return word

#Returns a tuple of sets (hashtables) of words from a given list of words separated by whitespace (newlines or spaces), where every word is included in the first set of the tuple and words prepended by ampersands are excluded in the second tuple. Used in this program to create dictionaries.   
def ampstring_to_set(list):
  speak = list.split()
  dictuple = [[],[]]
  for word in speak:
    val = True
    if word[0]=='&':
      val = False
    word = word.strip('&\n')
    dictuple[0].append(word)
    if val:
      dictuple[1].append(word)
  return dictuple

#Default cases for expregstringout
def emptycond(string):
  return True

def emptymod(string):
  return string

def choponemod(string):
  return string[:-1]

#Put other cases for expregstringout here


# Given a list of strings (regular expressions found by the program), a function that takes a string and returns a true false value, a modifier function that takes the string and 'fixes' it for output, and an output string (explanation), returns either an empty string or the regular expression followed by the output string. Used to handle output for the program
def expregstringout(string, exp, stringmod=emptymod, cond=emptycond):
  s = ""
  for strin in string:
    if cond(strin):
      s = s + stringmod(strin) + exp
  return s

def wordcounter(line, periodcount, wordcount, wordlist, capslist):
  words = line.split()
  for word in words:
    front = True
    back = True
    while (front or back) and word != "":
      if ord(word[0])>127:
        word = word[1:]
      else:
        front = False	
      if word!="" and ord(word[-1])>127:
        word = word[:-1]
      else:
        back = False
    word = word.strip('[]/\:;,-><()\"\'*')
    if word.rfind(".")!=-1 or word.rfind("?")!=-1 or word.rfind("!")!=-1:
       periodcount = periodcount+1
       word = word.strip('.?!')
    wordcount = wordcount + 1
    if word != "":
      if word[0].isupper():
        if capslist.has_key(word):
          capslist[word] = capslist[word]+1
        else:
          capslist[word] = 1
      word = word.lower()		
      if wordlist.has_key(word):
        wordlist[word] = wordlist[word] +1
      else:
        wordlist[word] = 1
  return [wordlist, capslist, periodcount, wordcount]

def stringprocess(string):
  wordcount = 0
  wordlist = {}
  capslist = {}
  periodcount = 0
  passivecounter = 0
  missedcaps = 0
  quotepunct = 0

#writing regular expressions
  missCapPeriod = re.compile(r"[A-Z]?[a-z]+\.[\'\"]?\s[\'\"]?[a-z]+")
  bbcode = r'\[/?[A-Za-z]+\]'
  passivevoice = (re.compile('\swas\s[A-Za-z]+ed\s'),re.compile(r'\swere\s[A-Za-z]+ed\s'),re.compile(r'\sis\s[A-Za-z]+ed\s'),re.compile(r'\sare\s[A-Za-z]+ed\s'),re.compile(r'\swas\s[A-Za-z]+en\s'),re.compile(r'\swere\s[A-Za-z]+en\s'),re.compile(r'\sis\s[A-Za-z]+en\s'),re.compile(r'\sare\s[A-Za-z]+en\s'),re.compile('\sget\s[A-Za-z]+ed\s'),re.compile('\sget\s[A-Za-z]+en\s'),re.compile('\sgot\s[A-Za-z]+ed\s'),re.compile('\sgot\s[A-Za-z]+en\s'),re.compile('\shad\sbeen\s[A-Za-z]+ed\sby\s'),re.compile('\shad\sbeen\s[A-Za-z]+en\sby\s'))
  dialoguecomma = re.compile('([A-Za-z\']+,\" ([A-Za-z\'-]+ )?(Mrs?\.? )?(Ms\.? )?(Dr\.? )?(the )?([A-Z]?[a-z\'-]+ ){,2}([A-Z]?[a-z]+)[ ,\.!\?;:-])')
  dialogueperiod = re.compile('([A-Za-z]+[\.!\?(...)-]" ([A-Z][A-Za-z\'-]*|(Mrs?\.?)|(Ms\.?)|(Dr\.?)) ([A-Z][a-z\']+ ){,2}([a-z-]+ ){,2}[a-z]+[ ,\.!\?;:-])')
#dialogueperiod2 = re.compile('([A-Za-z]+[.!\?(...)-]" [(Mrs?\.? )|(Ms\.? )|(Dr\.? )([A-Za-z\']+ ){,2}([a-z]+ ){,2}[a-z]+[ ,.!\?;:-])')
  dipercheck = re.compile('(((\.\.\.)|[!\?-])\")')
  chardict = set(['Fluttershy', 'Pinkie', 'Rainbow', 'Dash', 'Rarity', 'Twilight', 'Applebloom', 'Apple', 'Bloom', 'Bon', 'Braeburn', 'Celestia', 'Cheerilee', 'Colgate', 'Derpy', 'Discord', 'Gilda', 'Luna', 'Lyra', 'Octavia', 'Pipsqueak', 'Blueblood', 'Scootaloo', 'Snails', 'Snips', 'Soarin', 'Spike', 'Spitfire', 'Sweetie', 'Trixie', 'Twist', 'Vinyl', 'Zecora','I','Mr','Mrs','Ms','Dr','Mister','Miss','Doctor'])
  randcapscheck = re.compile('[A-Za-z\']+[;,]? [A-Z][A-Za-z\']*')
  punctspacecheck = re.compile('[A-Za-z\']+[\.;,!?]"?[A-Za-z][A-Za-z\']*')
  quotepunctoutside = re.compile('[A-Za-z\']+[,\.;!?-]?"[,\.;!?-] [A-Za-z][A-Za-z\']*')
  paracaps = re.compile('[\'\"]?[a-z\']+ ')
  endline = re.compile('[A-Za-z\']+[,\.\?!:]? [A-Za-z\']+[\",]?\w*$')
  frontdial = re.compile('(([A-Z][A-Za-z\']+ )?([A-Za-z\']+ )?[A-Za-z\']+, \"[A-Za-z\']+)')
  doublespace = re.compile('[A-Za-z][A-Za-z\']*[,\.\?!;:\"-]?  \"?[A-Za-z][A-Za-z\']*')
#
# Main function: 
#  fw = open('zdictspeak','r')
  dicts = dictreturn.dictionarylist()
  speak = [[],[]]
  resspeak = [[],[]]
  fw = dicts[0]  
  fw = ampstring_to_set(fw)
  speak[0] = fw[0]
  resspeak[0] = fw[1]
  fw = dicts[1]
  fw = ampstring_to_set(fw)
  speak[1] = fw[0]
  resspeak[1] = fw[1]
  #fw.close()
  #fw = open('zdict250','r')
  fw = dicts[2]
  common = fw.split()
  line = []
  for word in common:
    word = word.strip('0123456789 \n')
    line.append(word)
  common = set(line)
#  fw.close()
# End of dictionary section.
  perregexlist = []
  capsregexlist = []
#filename = sys.argv[1]
#f = open(filename, 'r')
#er = open(filename+'derrors','w')
  f = string.split('\n')
  er = ''
  for line in f:
	#handling " and ' in line
    word = ''
    for i in line:
      j = ord(i)
      if j<256:
        word = word + i
      elif j==8217 or j==8216:
        word = word + '\''
      elif j==8220 or j==8221:
        word = word + '\"'
      elif j==8212 or j==8211:
        word = word + '-'
      elif j==8230:
        word = word + '...'
    line = word
	# regular expressions section
    passivecounter = regcounter(line, passivecounter, passivevoice)
    #missedcaps = regcounter(line, missedcaps, missCapPeriod)
    line = re.sub(bbcode,"",line)
    matchObj = missCapPeriod.findall(line)
#    for lead in matchObj:
#      er = er + lead + ' | <a href="http://auto-reviewer.appspot.com/explanations#capserror">Capitalisation error<br></a>'
    er = er + expregstringout(matchObj, ' | <a href="http://auto-reviewer.appspot.com/explanations#capserror">Capitalisation error<br></a>')
    matchObj = punctspacecheck.findall(line)
#    for lead in matchObj:
#      er = er + lead + ' | <a href="http://auto-reviewer.appspot.com/explanations#punctspace">Space following punctuation<br></a>'
    er = er + expregstringout(matchObj, ' | <a href="http://auto-reviewer.appspot.com/explanations#punctspace">Space following punctuation<br></a>')
    matchObj = quotepunctoutside.findall(line)
#    for lead in matchObj:
#      er = er + lead + ' | Check this: <a href="http://auto-reviewer.appspot.com/explanations#punctinside">Punctuation is generally inside quotes.</a><br>'
    er = er + expregstringout(matchObj, ' | Check this: <a href="http://auto-reviewer.appspot.com/explanations#punctinside">Punctuation is generally inside quotes.</a><br>')
    quoteregex = re.compile('\"[^\"]+?\"')
    matchObj = quoteregex.findall(line)
    for lead in matchObj:
      end = lead[-2]
      if end != "." and end != "," and end != "!" and end != "?" and end != "-" and end != "'":
        quotepunct +=1
      beg = lead[1]
      if ord(beg)>96 and ord(beg)<123:
        quotepunct +=1
    matchObj = dialoguecomma.findall(line)
    for lead in matchObj:
      lead = lead[0]
      perregexlist.append([lead,0])

    matchObj = doublespace.findall(line)
#    for lead in matchObj:
#      lead = lead + ' | <a href="http://auto-reviewer.appspot.com/explanations#doublespace">You have an extra space here</a><br>'
#      er = er + lead
    er = er + expregstringout(matchObj, ' | <a href="http://auto-reviewer.appspot.com/explanations#doublespace">You have an extra space here</a><br>')
	#Period checking will be handled when characters are listed.
    matchObj = dialogueperiod.findall(line)
    for lead in matchObj:
      lead = lead[0]
      perregexlist.append([lead, 1])
    matchObj = randcapscheck.findall(line)
    for lead in matchObj:
      capsregexlist.append(lead)
    matchObj = paracaps.match(line)
    if matchObj != None:
      matchObj = matchObj.group()
      matchObj = matchObj + ' | Check this: <a href="http://auto-reviewer.appspot.com/explanations#parastart">Paragraph start should be capitalised.</a><br>'
      er = er + matchObj
    
    matchObj = endline.findall(line)
    for lead in matchObj:
      lead = lead[:-1]
      lead = lead + ' | Check this: <a href="http://auto-reviewer.appspot.com/explanations#paraend">Paragraph end should be punctuated.</a><br>'
      er = er + lead
    matchObj = frontdial.findall(line)
    for lead in matchObj:
      lead = lead[0]
      perregexlist.append([lead,2])
	#wordcount section
    #Put in function
    helper = wordcounter(line, periodcount, wordcount, wordlist, capslist)
    wordlist = helper[0]
    capslist = helper[1]
    periodcount = helper[2]
    wordcount = helper[3]
  #End of line by line for loop
  
  waswere = 0
  for word in ('was','is','were','are', 'be', 'been'):
    if wordlist.has_key(word):
      waswere = waswere + wordlist[word]
  #filen = sys.argv[1]+"data"
  #fw = open(filen, 'w')
  stats = '('
  fw = ''
  s = str(wordcount)
  stats = stats + s + ', ' 
  fw = writetuple(fw,"Wordcount:",wordcount)
  s = str(periodcount)
  stats = stats + s + ', '
  fw = writetuple(fw,"Sentences:",periodcount)
  s = str(waswere)
  stats = stats + s + ', '
  fw = writetuple(fw,"Be conjugations (was/were/is/are/be/been):",waswere)
  if waswere > 0:
    fw = writetuple(fw,"Be ratio: 1 every",wordcount/waswere)
    s = str(wordcount/waswere)
    stats = stats + s + ', '
    val = float(periodcount)
    val = val/waswere
    s = str(val)
    stats = stats + s + ', '
    fw = writetuple(fw,"Sentences containing be: 1 every", val)
  else:
    stats = stats + "n, n, "
  if periodcount > 0:
    s = str(wordcount/periodcount)
    fw = writetuple(fw,"Words per sentence:",wordcount/periodcount)
    stats = stats + s + ', '
  else:
    stats = stats + "n, "
  fw = writetuple(fw,"Passive sections:",passivecounter)
  s = str(passivecounter)
  stats = stats + s + ', '
  if passivecounter > 0:
    s = str(periodcount/passivecounter)
    stats = stats + s + ', '
    fw = writetuple(fw,"Passive sentences: 1 every",periodcount/passivecounter)
  else:
    stats = stats + "n, "
  #filen = sys.argv[1]+"words"
  #fv = open(filen, 'w')
  fv = ''
  sorted_wordlist = sorted(wordlist.iteritems(), key=operator.itemgetter(1), reverse=True)
  sorted_capslist = sorted(capslist.iteritems(), key=operator.itemgetter(1), reverse=True)

  adverb = 0
  vocabcount = 0
  mostused = 0
  fw = fw + "<br><br>These are the uncommon words that you use the most: <br>"
  for (k,v) in sorted_wordlist:
    vocabcount += 1
    s = str(v)
    if k[-2:]=="ly":
      adverb = adverb + int(v)
    s = k + " " + s
    if capslist.has_key(titlecase(k)):
      w = str(capslist[titlecase(k)])
      s = s + " " + w
    s = s + "<br>"
    vfloat = float(v)
    if k not in common and (not capslist.has_key(titlecase(k)) or vfloat/capslist[titlecase(k)]>1.1) and mostused<12:
      mostused += 1
      fw = fw + s		
    fv = fv + s
  s = str(vocabcount)
  stats = stats + s + ', '
  s = str(adverb)
  stats = stats + s + ', '
  fw = writetuple(fw,"<br>Distinct Words Used:",vocabcount)
  fw = writetuple(fw,"Adverbs:",adverb)
  if adverb != 0:
    fw = writetuple(fw,"AdverbRatio: 1 per",wordcount/adverb)
    s = str(wordcount/adverb)
    stats = stats + s + ')\n'
  else:
    stats = stats + 'n)\n'
  if waswere*passivecounter>0:
    if periodcount*val/passivecounter<110:
      fw = fw + "<br>You have a high amount of usage of passive voice and/or conjugations of be, which may indicate telling.<br>"

  if adverb*periodcount > 0:
    if wordcount/adverb+20-wordcount/periodcount<50:
      fw = fw + "<br>You have a high usage of adverbs and a large average sentence size, which may be a sign of purple prose.<br>"

  fw = fw + "<br>This checks quotations to see if they end with proper punctuation and checks that they do not begin with a lowercase letter. This will flag anything that uses quotes as emphasis, so these may not necessarily be errors.<br>"
  fw = writetuple(fw,"Quote Punctuation Errors:",quotepunct)
  fw = fw + "<br><br>These words are primarily capitalised. These should be the major proper nouns in your fic (main characters and locations). If a word is here that is not one of those, then you may be capitalising it incorrectly. Also, this should approximately reflect the importance of each of the characters in the story. <br>Capitalised count <br>"
  charcount = 0
  for (k,v) in sorted_capslist:
    kfloat = float(wordlist[k.lower()])
    if kfloat/v<1.1 and charcount < 10 and k!="I" and k!="I'm" and k!="I've" and k!="I'd" and k!="I'll" and wordcount/v<1500:
      fw = writetuple(fw,k,v)
      charcount+=1
    if v>=3 and kfloat/v<1.26 and k!="I" and k!="I'm" and k!="I've" and k!="I'd" and k!="I'll":
      chardict.add(k)
  current = 0
  toggled = False
  for lead in perregexlist:
    if lead[1] == 0:
      lead = lead[0]
      mack = lead
      lead = lead.split()
      lead = lead[1:]
      correct = False
      for word in lead:
        word = word.strip(',.?!-;:')
        if word in speak[current]:
          correct = True
          toggled = True
        elif word in speak[1-current]:
          current = 1-current
          correct = True
          if toggled:
            dummy = mack + ' | Check this: <a href="http://auto-reviewer.appspot.com/explanations#tensechange"> You change tenses here</a><br>'
            er = er + dummy
          else:
            toggled = True
      if correct:
        mack = mack + " | Right\n"
			#er.write(mack)
      else:
        mack = mack + ' | Check this: <a href="http://auto-reviewer.appspot.com/explanations#speakverb">This should have some sort of speaking verb</a><br>'
        er = er + mack
    elif lead[1] == 1:
      lead = lead[0]
      mack = lead
      lead = lead.split()
      lead = lead[1:]
      correct = True
      for word in lead:
        word = word.strip(',.?!-;:')
        if word in resspeak[current]:
          correct = False
          toggled = True
          if dipercheck.search(mack) and lead[0].strip(',.?!-;:') in chardict:
            correct = True
        elif word in resspeak[1-current]:
          correct = False
          if dipercheck.search(mack) and lead[0].strip(',.?!-;:') in chardict:
            correct = True
          current = 1-current
          if toggled:
            dummy = mack + ' | Check this: <a href="http://auto-reviewer.appspot.com/explanations#tensechange"> You change tenses here</a><br>'
            er = er + dummy
          else:
            toggled = True
      if correct:
        mack = mack + " | Right\n"
      #er.write(mack)
      else:
        mack = mack + ' | Check this: <a href="http://auto-reviewer.appspot.com/explanations#pererror">Dialogue attribution should not be capitalised or period error</a><br>'
        er = er + mack
    elif lead[1] == 2:
      lead = lead[0]
      mack = lead
      lead = lead.split()
      lead = lead[:-1]
      correct = False
      for word in lead:
        word = word.strip(',.?!-;:')
        if word in speak[current]:
          correct = True
          toggled = True
        elif word in speak[1-current]:
          correct = True
          if toggled:
            dummy = mack + ' | Check this: <a href="http://auto-reviewer.appspot.com/explanations#tensechange"> You change tenses here</a><br>'
            er = er + dummy
          else:
            toggled = True
      if correct:
        mack = mack + " | Right\n"
        #er = er + mack
      else:
        mack = mack + ' | Check this: <a href="http://auto-reviewer.appspot.com/explanations#speakverb">This should have some sort of speaking verb</a><br>'
        er = er + mack

  for lead in capsregexlist:
    mack = lead
    lead = lead.split()
    correct = False
    for word in lead:
      word = word.strip(',;\'')
      #check capitalised word
      if capslist.has_key(word):
        kfloat = float(wordlist[word.lower()])/capslist[word]
      if kfloat < 1.25:
        correct = True
    if correct:
      mack = mack + " | Right\n"
      #er.write(mack)
    else:
      mack = mack + ' | Check this: <a href="http://auto-reviewer.appspot.com/explanations#rarecaps">Rarely capitalised word is capitalised here.</a><br>'
      er = er + mack
  #er.close()
  #fv.close()
  # review formatting, everything in one doc
  #er = open(sys.argv[1]+'derrors','r')
  #fv = open(sys.argv[1]+'words','r')
  fw = fw + '<br><br>Here is a list of suspected errors:<br>'
  #for line in er:
  #  fw.write(line)
  fw = fw + er
  fw = fw + '<br><br>Here is a wordlist ordered by number of occurrences.<br>The first number is the number of total occurrences. If there is a second, that is the number of capitalised occurrences<br>'
  #for line in fv:
  #  fw.write(line)
  fw = fw + fv
  #fw.close()
  #er.close()
  #fv.close()
  return [fw, stats]

def passiveprocess(string):
  #passivevoice = (re.compile('[A-Za-z\'-]+ was\s[A-Za-z]+ed[\s\.]([A-Za-z\'-]+ )?'),re.compile('[A-Za-z\'-]+ were\s[A-Za-z]+ed\s'),re.compile(r'\sis\s[A-Za-z]+ed\s'),re.compile(r'\sare\s[A-Za-z]+ed\s'),re.compile(r'\swas\s[A-Za-z]+en\s'),re.compile(r'\swere\s[A-Za-z]+en\s'),re.compile(r'\sis\s[A-Za-z]+en\s'),re.compile(r'\sare\s[A-Za-z]+en\s'),re.compile('\sget\s[A-Za-z]+ed\s'),re.compile('\sget\s[A-Za-z]+en\s'),re.compile('\sgot\s[A-Za-z]+ed\s'),re.compile('\sgot\s[A-Za-z]+en\s'),re.compile('\shad\sbeen\s[A-Za-z]+ed\sby\s'),re.compile('\shad\sbeen\s[A-Za-z]+en\sby\s'))
#'([A-Za-z\'-]+ was|(were)|(is)|(are)|(get)|(got)|(had been)|(has been)) [A-Za-z]+((en)|(ed))[ \.,]([A-Za-z\'-]+)?)'
  passivevoice = map(re.compile,('([A-Za-z\'-]+ was [A-Za-z]+en[ \.,]([A-Za-z\'-]+)?)','([A-Za-z\'-]+ was [A-Za-z]+ed[ \.,]([A-Za-z\'-]+)?)','([A-Za-z\'-]+ were [A-Za-z]+en[ \.,]([A-Za-z\'-]+)?)','([A-Za-z\'-]+ were [A-Za-z]+ed[ \.,]([A-Za-z\'-]+)?)','([A-Za-z\'-]+ are [A-Za-z]+en[ \.,]([A-Za-z\'-]+)?)','([A-Za-z\'-]+ are [A-Za-z]+ed[ \.,]([A-Za-z\'-]+)?)','([A-Za-z\'-]+ is [A-Za-z]+en[ \.,]([A-Za-z\'-]+)?)','([A-Za-z\'-]+ is [A-Za-z]+ed[ \.,]([A-Za-z\'-]+)?)','([A-Za-z\'-]+ get [A-Za-z]+en[ \.,]([A-Za-z\'-]+)?)','([A-Za-z\'-]+ get [A-Za-z]+ed[ \.,]([A-Za-z\'-]+)?)','([A-Za-z\'-]+ got [A-Za-z]+en[ \.,]([A-Za-z\'-]+)?)','([A-Za-z\'-]+ got [A-Za-z]+ed[ \.,]([A-Za-z\'-]+)?)','([A-Za-z\'-]+ has been [A-Za-z]+en[ \.,]([A-Za-z\'-]+)?)','([A-Za-z\'-]+ has been [A-Za-z]+ed[ \.,]([A-Za-z\'-]+)?)','([A-Za-z\'-]+ had been [A-Za-z]+en[ \.,]([A-Za-z\'-]+)?)','([A-Za-z\'-]+ had been [A-Za-z]+ed[ \.,]([A-Za-z\'-]+)?)'))
  f = string.split('\n')
  er = ''
  for line in f:
	#handling " and ' in line
    word = ''
    for i in line:
      j = ord(i)
      if j<256:
        word = word + i
      elif j==8217 or j==8216:
        word = word + '\''
      elif j==8220 or j==8221:
        word = word + '\"'
      elif j==8212 or j==8211:
        word = word + '-'
      elif j==8230:
        word = word + '...'
    line = word
    for reg in passivevoice:
      matchObj = reg.findall(line)
      if matchObj != []:
        for lead in matchObj:
          lead = [lead[0]]
          er = er + expregstringout(lead, '<br>')
  return er
