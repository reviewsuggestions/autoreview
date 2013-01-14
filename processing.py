#! /usr/bin/env python
import string, re

DEBUG = False

# This function takes a typical string and transforms it to Ascii for the rest of the app. It returns a tuple containing the converted string and a list of any unknown characters that were omitted. It also transforms special characters
def uch(s,i):
  return ord(s[i])>226

def ucl(s,i):
  return ord(s[i])>200


def asciiconvert(s):
  s += "  " #Pads string so it comes out cleanly, regardless of unicode
  word = ""
  chartuple = []
  # Ord may get entire unicode code or just 8 bits at a time
  # TODO: Update each with unicoder
  unicoder = False
  i = 0
  while i < len(s)-2:
    #put character elimination here
    if ord(s[i])<128:
      word += s[i]
      i = i+1
    # Cases to replace special elements
    # single quotes
    elif (ord(s[i])==226 and ord(s[i+1])==128 and (ord(s[i+2])==153 or 
          ord(s[i+2])==152)) or (ord(s[i])==8216 or ord(s[i])==8217 or 
          ord(s[i])==8219):
      word += "\'"
      if uch(s,i): i+=1
      else:
        i += 3
    # double quotes
    elif (ord(s[i])==226 and ord(s[i+1])==128 and (ord(s[i+2])==157 or 
          ord(s[i+2])==156 or ord(s[i+2])==158)) or (ord(s[i])==8220 or 
          ord(s[i])==8221):
      word += "\""
      if uch(s,i): i+=1
      else:
        i += 3    
    #ellipses
    elif (ord(s[i])==226 and ord(s[i+1])==128 and (
          ord(s[i+2])==166)) or ord(s[i])==8230:
      word += "..."
      if uch(s,i): i+=1
      else:
        i += 3
    #dashes
    #may be handled separately
    elif (ord(s[i])==226 and ord(s[i+1])==128 and (ord(s[i+2])==147 or 
          ord(s[i+2])==148)) or (ord(s[i])==8211 or ord(s[i])==8212):
      word += "--"
      if uch(s,i): i+=1
      else:
        i += 3
    #interrobang
    elif (ord(s[i])==226 and ord(s[i+1])==128 and (
          ord(s[i+2])==189)) or (ord(s[i])==8253):
      word += "?!"
      if uch(s,i): i+=1
      else:
        i += 3
    # accented e, e backaccent,e umlaut
    elif ord(s[i])==195 and (ord(s[i+1]) in range(168,172)) or (
         ord(s[i]) in range(232,236)):
      word += "e"
      if ucl(s,i): i+=1
      else:
        i += 2
    # a hat, a backaccent, a umlaut, a circle
    elif (ord(s[i])==195 and (ord(s[i+1]) in range(160,166))) or (
          ord(s[i]) in range(224,229)):
      word += "a"
      if ucl(s,i): i+=1
      else:
        i += 2
    #ae
    elif (ord(s[i])==195 and ord(s[i+1])==166) or (ord(s[i])==229):
      word += "ae"
      if ucl(s,i): i+=1
      else:
        i += 2
    # i umlaut, i accent, i backaccent
    elif (ord(s[i])==195 and (ord(s[i+1]) in range(172,176))) or \
          ord(s[i])in range(236,240):
      word += "i"
      if ucl(s,i): i+=1
      else:
        i += 2
    # o umlaut, o accent
    elif (ord(s[i])==195 and (ord(s[i+1]) in range(179,183))) or \
          ord(s[i])in range(242,247):
      word += "o"
      if ucl(s,i): i+=1
      else:
        i += 2
    # u umlaut, u hat
    elif (ord(s[i])==195 and (ord(s[i+1]) in range(186,189))) or \
          ord(s[i])in range(249,253):
      word += "u"
      if ucl(s,i): i+=1
      else:
        i += 2
    # c cedilla?
    elif (ord(s[i])==195 and ord(s[i+1])==167) or ord(s[i])==231:
      word += "c"
      if ucl(s,i): i+=1
      else:
        i += 2
    # ~n
    elif (ord(s[i])==195 and ord(s[i+1])==177) or ord(s[i])==241:
      word += "n"
      if ucl(s,i): i+=1
      else:
        i += 2
    # ~N
    elif (ord(s[i])==195 and ord(s[i+1])==145) or ord(s[i])==209:
      word += "N"
      if ucl(s,i): i+=1
      else:
        i += 2
    # German ss replacement
    elif (ord(s[i])==195 and ord(s[i+1])==159) or ord(s[i])==223:
      word += "ss"
      if ucl(s,i): i+=1
      else:
        i += 2
    # Division symbol
    elif (ord(s[i])==195 and ord(s[i+1])==183) or ord(s[i])==247:
      word += "/"
      if ucl(s,i): i+=1
      else:
        i += 2
    # Center dot
    elif (ord(s[i])==194 and ord(s[i+1])==183) or ord(s[i])==167:
      word += "*"
      if ord(s[i])==167: i+=1
      else:
        i += 2
    # Bullet point
    elif (ord(s[i])==226 and ord(s[i+1])==128 and (ord(s[i+2])==162)) or ord(s[i])==8226:
      word += "*"
      if uch(s,i): i+=1
      else:
        i += 3
    #no break space?
    elif ord(s[i])==194 and ord(s[i+1])==160:
      i +=2
    #arrows, music note: no replacement
    elif ord(s[i])==226 and ((ord(s[i+1])==134 and ord(s[i+2]) in range(144,147)) or (ord(s[i+1])==153 and ord(s[i+2])==171)):
      i +=3
    else:
      chartuple.append(str(ord(s[i])))
      i+= 1
  return (word,chartuple)

# This function handles gathering regular expressions in a list regardless of group status.
# Arguments: Regular expression, string
# Returns a list of the whole regular expression regardless of the presence of groups assuming the entire is in a group
def findallgroup(regex, line):
  values = re.findall(regex, line, flags=re.MULTILINE)
  if  ("(" in regex and ")" in regex):
    temp = []
    for item in values:
      temp.append(item[0])
    values = temp
  return values

#This function checks a line for a regular expression given by a string or a function that takes the string and returns a string, applies a function that returns a boolean, and depending on the return value returns this error. If there is an error, the function should return true.
# Arguments: string or tuple of strings for regular expression (if the regex contains groups, the string should be enclosed in parens) or a function taking a string or a tuple of functions that take a string and output a string, string to check, error message, function 
def regexcheck(regex, section, error, funct, charlist={}):
  res = []
  if (isinstance(regex, str)):
    res = findallgroup(regex, section)
  elif (isinstance(regex, tuple) or isinstance(regex, list)):
    for reg in regex:
      if isinstance(reg, str):
        res.extend(findallgroup(reg, section))
      else: 
        res.extend(reg(section))
  else:
   res = regex(section)
  firstinc = True
  inclist = []
  if DEBUG:
    firstcor = True
    corlist = []
  for elem in res:
    val = funct(elem, charlist)
    if val:
      # Here the program flags an error
      if firstinc == True:
        inclist.append(section)
        firstinc = False
      inclist.append(elem)
    elif DEBUG:
      # Here the program believes this is correct
      if firstcor == True:
        corlist.append(section)
        firstcor = False
      corlist.append(elem)
  if DEBUG:
    return (inclist, corlist)
  else:
    return inclist

#This function counts the occurrences  
def regexcount(regex, section, error, funct, charlist={}):
  count = 0
  res = []
  if (isinstance(regex, str)):
    res = findallgroup(regex, section)
  else:
    for reg in regex:
      res.extend(findallgroup(reg, section))
  for elem in res:
    if funct(elem, charlist):
      count += 1
  return count  


