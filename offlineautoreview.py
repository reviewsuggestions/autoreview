#! /usr/bin/env python
import string, processing, sys, re, errorlisting, mainreview, operator

# To use this, put the text in a file

def optionsdefine():
  introtexts = ['Missing Capitalisation:', 'Passive Voice Check:', 'Dialogue Punctuation-Attributed:', 'Dialogue Punctuation-Non-Attributed:', 'Front Dialogue Punctuation:','Missing Space After Punctuation:','Extra Space:','Unnecessary Capitalisation:','Punctuation Outside of Quotes:','Capitalisation at Beginning of Paragraph:','Punctuation at End of Paragraph:']
  optionslist = []
  print "For each item, input 1 for a full check, 2 for just a count, anything else to omit"
  for item in introtexts:
    obj = raw_input(item)
    if obj == '1' or obj == '2':
      optionslist.append(int(obj))
    else:
      optionslist.append(0)
  return optionslist  

def suppressdefine():
  otherintros = ['Word List with Counts:','Adverb Checking:', 'Uncommon Word List:', 'Character List']
  print "For each item, input 1 to include in output, anything else to omit"
  suppresslist = []
  for item in otherintros:
    obj = raw_input(item)
    if obj == '1' or obj == '2':
      suppresslist.append(int(obj))
    else:
      suppresslist.append(0)
  return suppresslist  
  pass

def review():
  f = open(sys.argv[1],'r')
  example = f.read()
  f.close()
  if len(sys.argv)<=2 or sys.argv[2]!='-a':
    lis = mainreview.mainprocess(example)
  else:
    optionslist = optionsdefine()
    suppresslist = suppressdefine()
    lis = mainreview.mainprocess(example, optionslist, suppresslist)
  f = open('review.html', 'w')
  f.write(lis[0])
  f.close()

def main():
    review()

if __name__ == "__main__":
    main()



