#! /usr/bin/env python
import string, re, processing

# This defines the appropriate functions for each error

#This class contains the objects for an error
# restring is the regex for recognising the error pattern
# errormsg is the heading for the error description
# funct is the function for recognising when the matched pattern is an error
# listing is the list for flagged errors
# link is the link for the listed description
# count is for counting instances
# mouseover is the mouseover description for the error
#Listing must be initialised individually, otherwise each instance points to the same location in memory
class Error:
  def __init__(self, restring, errormsg, funct, listing, mouseover = ' ', link = ' ', count=0):
    self.string = restring
    self.errormsg = errormsg
    self.funct = funct
    self.link = link
    self.listing = listing
    self.count = count
    self.mouseover = mouseover
  
  def addcount(self, item):
    self.count += item
  def addtolist(self, item):
    self.listing.append(item)

# This function calls the function regexcheck from processing on a string 
def regexcheckclass(obj, text, capslist={}):
  return processing.regexcheck(obj.string, text, obj.errormsg, obj.funct, capslist)

# This function calls the function regexcount from processing on a string
# Counts occurrences rather than returning a tuple of occurences
def regexcountclass(obj, text, capslist=[]):
  return processing.regexcount(obj.string, text, obj.errormsg, obj.funct, capslist) 

# List of speaking verbs, one with all and one without those that aren't usually speaking verbs, but could be (Ampersands).
# To be deprecated by more advanced sentence processing
dictspeak = 'said replied whispered added muttered answered continued admitted explained stated &sighed murmured agreed called responded mumbled commented remarked growled chuckled interrupted assured grumbled repeated &laughed offered announced asked finished insisted hissed suggested snapped corrected retorted &started declared stammered informed mused groaned interjected rasped snorted observed &managed reminded drawled chimed huffed snarled warned reassured noted greeted giggled countered ordered moaned grunted complained cooed gasped intoned claimed confirmed chided clarified lied concluded apologized sneered protested uttered teased shouted confessed squeaked whined stuttered whimpered groused purred piped addressed conceded panted commanded chirped begged argued instructed asserted promised supplied soothed scoffed pleaded scolded exclaimed sobbed snickered &returned barked croaked advised boomed allowed yelled quipped reported stressed indicated snipped proclaimed coughed mentioned &motioned reasoned joked echoed cried &remembered recited &raised complimented slurred wheezed blurted confided &sounded crooned admonished demanded pondered seethed hummed dismissed challenged defended encouraged relented praised whinnied urged grumped prompted cautioned pressed mocked accused neighed joined puffed rattled taunted wondered affirmed surmised nickered gushed boasted snarked whistled marveled persisted attempted congratulated consoled threatened bragged reiterated proposed coaxed reminisced bellowed choked lectured mouthed &pouted emphasized ventured elaborated blubbered recounted realized acknowledged trailed cackled concurred amended introduced screamed griped guessed &followed fussed beckoned punctuated revealed resumed chortled wailed droned &jabbed entreated relieved sniggered considered buzzed closed implored recalled burbled saluted pipped requested pronounced objected fretted squealed acquiesced gloated riposted provided guffawed wished rebuked recollected related wheedled cracked sputtered sniveled reckoned roared garbled jeered annoyed quoted lamented fumed appraised opened hushed hedged comforted noticed murred checked listed assessed babbled accented demurred chanced worried narrated prayed volunteered fibbed rambled crackled hazarded thanked signed hollered goaded restated fawned concerned cussed summarised excused humphed blared bemoaned opted imagined rationalized faltered faded specified cheered tested capitulated cajoled admired sweared averted halted nipped counted backpedaled backpedalled interpreted produced ended patronized disagreed covered vocalized pffted crowed exhaled mollified identified leveled referred averred ranted pined mulled pled reprimanded broached reflected gurgled raged bargained kidded completed tutted recovered chanted forced recommended flattered intervened inserted approved gesticulated reproved contributed attested heckled clicked convinced postulated &hailed divulged pressured harrumphed snurked invited solicited opined maintained recognized deflected pontificated described deduced refuted warbled apologised deferred bawled transitioned theorized granted repudiated vowed butted questioned sussed tisked twittered translated hinted jibed shushed jested ribbed drolled speculated gleaned emulated squawked cursed reproached directed parroted iterated chastised consented ingratiated acceded hemmed implied interrogated spat &began &came remonstrated'
dictspeak = dictspeak.split() 
templist1 = [] # all speaking verbs
templist2 = [] # just the strong speaking verbs
for word in dictspeak:
  val = True
  if word[0]=='&':
    val = False
  word = word.strip('&')
  templist1.append(word)
  if val:
    templist2.append(word)
dictstrong = set(templist1)
dictsoft = set(templist2)
# List of most common words from existing fics
commonwords = "it  in  the  just  was  so  that  and  on  of  her  as  at  all  to  a  up  out  for  she  no  with  you  what  back  be  this  have  then  had  into  were  from  but  one  not  more  would  do  is  now  could  like  them  been  down  time  over  they  if  there  about  even  me  by  how  before  can  get  an  know  did  around  my  head  still  eyes  off  your  see  said  when  we  too  are  little  don't  some  go  right  only  it's  again  something  way  looked  here  after  didn't  or  their  think  well  good  much  never  make  pony  who  away  two  through  other  than  made  look  ponies  come  thought  turned  first  going  any  face  long  where  he  his  you're  hoof  got  took  why  let  will  sure  really  voice  few  hooves  herself  want  another  asked  very  door  thing  wasn't  while  take  him  help  say  behind  moment  room  came  last  need  day  looking  felt  being  once  though  enough  anything  began  ever  tell  left  its  every  next  things  knew  most  side  own  friends  us  can't  each  mind  smile  front  should  night  which  air  place  those  mean  couldn't  found  bit  against  small  magic  saw  always  find  sorry  has  yes  seemed  nothing  our  new  work  keep  unicorn  open  better  heard  trying  until  almost  both  smiled  pegasus  mane  went  nodded  tried  gave  because  told  light  under  best  wanted  finally  friend  ground  put  wings  mouth  horn  shook  already  okay  three  far  started  such  towards  course  quickly  these  same  floor  maybe  big  across  great  am  stood  she'd  must  seen  without  oh  sister  old  feel  slowly  life  stopped  everypony  blue  yeah  mare  home  inside  love  quite  between  might  hard  table  "
commonwords = set(commonwords.split())


#The trivial function for regular expressions that should always be
#flagged as an error
#Arguments: String
#Returns: True
def trivial(string, dic):
  return True  


#This function checks for the dialogue with a comma regular expression True->error
#It removes the first word (word within dialogue), then checks that there is a
#speaking verb within the first few words
def dialoguecomma(string, dic):
  lead = string.split()
  lead = lead[1:]
  val = True
  for word in lead:
    word = word.strip(',.?!-;:')
    if word in dictstrong:
      val = False
  return val

# Function for checking <Dialogue><Ending Punctuation>" Word words
# Note the capitalisation
def dialogueperiod(string, chardict):
  lead = string.split()
  dialogue = lead[0]
  lead = lead[1:]
  CheckNonPeriodPunct = re.compile('(((\.\.\.)|(---)|[!\?])\")')
  val = False
  nonFullStop = False
  firstword = lead[0].strip(',.?!-;:')
  firstUpper = False
  if firstword[0].isupper():
    firstUpper = True
  if CheckNonPeriodPunct.search(dialogue) != None:
    nonFullStop = True  
  # First check non full stop
  if nonFullStop:
    # Here means it is not a full stop
    if firstUpper:
      # Here means that the next word is capitalised
      if not(firstword in chardict):
        
        # First word is a new sentence, so it should not be an attribution
        for word in lead:
          word = word.strip(',.?!-;:')
          if word in dictstrong:
            val = True
      #else: If firstword is a character, then it would be capitalised regardless of whether it is an attribution.
    else:
      # Here means that the next word is not capitalised, so it should be an attribution
     val = True
     for word in lead:
        word = word.strip(',.?!-;:')
        if word in dictstrong:
          val = False
  else:
    # Means it ends with a full stop, so it should not be an attribution
    val = False
    for word in lead:
      word = word.strip(',.?!-;:')
      if word in dictsoft:
        val = True
  return val


# Function for checking words, "<Dialogue>
# May be replaced by sentence processing      
def dialoguefront(section, dic):
  lead = section.split()
  lead = lead[:-1]
  val = True
  for word in lead:
    word = word.strip(',.?!-;:')
    if word in dictstrong:
      val = False
  return val
    


# Function for recognising random capitalisations.
def randcaps(section, charlist):
  lead = section.split()
  lead = lead[1:][0]
  lead = lead.strip(',.?!-;:')
  if lead[-2:] == "'s":
    lead = lead[:-2]
  val = True
  if lead in charlist or lead[:2]=="I'":
    val = False
  return val


#Initialises all Error instances and returns a list of them.
# This removes the necessity for the individual error definitions, although they are left commented in case the come in useful.
def initialise():
  return [Error("[A-Z]?[a-z]+\.[\'\"]?\s[\'\"]?[a-z]+","Capitalisation Error", trivial, [], 'This checks when the word immediately after a full stop is not capitalised.','/Conventions#MissedCaps'), 
Error(('\swas\s[A-Za-z]+ed\s','\swere\s[A-Za-z]+ed\s','\sis\s[A-Za-z]+ed\s','\sare\s[A-Za-z]+ed\s','\swas\s[A-Za-z]+en\s','\swere\s[A-Za-z]+en\s','\sis\s[A-Za-z]+en\s','\sare\s[A-Za-z]+en\s','\sget\s[A-Za-z]+ed\s','\sget\s[A-Za-z]+en\s','\sgot\s[A-Za-z]+ed\s','\sgot\s[A-Za-z]+en\s','\shad\sbeen\s[A-Za-z]+ed\sby\s','\shad\sbeen\s[A-Za-z]+en\sby\s','\shas\sbeen\s[A-Za-z]+ed\sby\s','\shas\sbeen\s[A-Za-z]+en\sby\s'),"Passive Voice", trivial, [], 'This looks for passive voice, which is where the subject experiences the action, instead of performing the action. While not an error, this is often weaker and less interesting than using the active voice.', '/Style#Passive'), 
Error('([A-Za-z\']+,\" ([A-Za-z\'-]+ )?(Mrs?\.? )?(Ms\.? )?(Dr\.? )?(the )?([A-Z]?[a-z\'-]+ ){,2}([A-Z]?[a-z]+)[ ,\.!\?;:-])',"Dialogue without speaking verb", dialoguecomma, [],'This checks that dialogue follows generally accepted formatting. In particular, this makes sure that the section of the sentence connected to the dialogue is a direct attribution, rather than an unrelated sentence.','/Dialogue#DialogueSpeaking'), 
Error(('([A-Za-z]+\." ([A-Za-z\'-]+|(Mrs?\.?)|(Ms\.?)|(Dr\.?)) ([A-Z][a-z\']+ ){,2}([a-z-]+ ){,2}[a-z]+[ ,\.!\?;:-])','([A-Za-z]+!" ([A-Za-z\'-]+|(Mrs?\.?)|(Ms\.?)|(Dr\.?)) ([A-Z][a-z\']+ ){,2}([a-z-]+ ){,2}[a-z]+[ ,\.!\?;:-])', '([A-Za-z]+\?" ([A-Za-z\'-]+|(Mrs?\.?)|(Ms\.?)|(Dr\.?)) ([A-Z][a-z\']+ ){,2}([a-z-]+ ){,2}[a-z]+[ ,\.!\?;:-])', '([A-Za-z]+(\.\.\.)" ([A-Za-z\'-]+|(Mrs?\.?)|(Ms\.?)|(Dr\.?)) ([A-Z][a-z\']+ ){,2}([a-z-]+ ){,2}[a-z]+[ ,\.!\?;:-])','([A-Za-z]+(---)" ([A-Za-z\'-]+|(Mrs?\.?)|(Ms\.?)|(Dr\.?)) ([A-Z][a-z\']+ ){,2}([a-z-]+ ){,2}[a-z]+[ ,\.!\?;:-])'),"Dialogue ends sentence incorrectly", dialogueperiod, [], 'This checks that dialogue follows generally accepted formatting. In particular, this makes sure that when the dialogue has punctuation ending the sentence, the following sentence is not an attribution.','/Dialogue#DialogueEnds'), 
Error('(([A-Z][A-Za-z\']+ )?([A-Za-z\']+ )?[A-Za-z\']+, \"[A-Za-z\']+)', "Dialogue follows nonattribution", dialoguefront, [], 'This checks that dialogue follows generally accepted formatting. In particular, this checks that a sentence leading into dialogue is an attribution, rather than an unrelated sentence that should be separated.','/Dialogue#DialogueFollows'), 
Error('[A-Za-z\']+[\.;,!?]{1,3}"?[A-Za-z][A-Za-z\']*',"Punctuation without a trailing space", trivial, [], 'This checks that punctuation is properly separated from the following word.', '/Conventions#PunctSpace'),
Error('[A-Za-z][A-Za-z\']*[,\.\?!;:\"-]?  \"?[A-Za-z][A-Za-z\']*',"Extra Space", trivial, [], 'This checks that there aren\'t extra spaces between words.', '/Conventions#ExtraSpace'), 
Error('[A-Za-z\']+[;,]? [A-Z][A-Za-z\']*',"Uncommonly capitalised word", randcaps, [],'This flags words that do not look to be proper nouns that are capitalised in the middle of a sentence.','/Conventions#RandCaps'), 
Error('[A-Za-z\']+[,\.;!?-]?"[,\.;!?-] [A-Za-z][A-Za-z\']*',"Punctuation Outside Quotes", trivial, [], 'This flags punctuation that does not follow convention and occurs outside of the quotation marks.', '\Dialogue#PunctOutside'), 
Error('^\s*[\'\"]?[a-z\']+ ',"Beginning of paragraph not capitalised", trivial, [], 'This checks that the initial sentence of each paragraph is properly capitalised.','\Conventions#ParagraphCaps'), 
Error('[A-Za-z\']+[,\.\?!:]? [A-Za-z\']+[\",]?\s*$',"End of paragraph missing punctuation", trivial, [], 'This checks that the sentence at the end of each paragraph is not missing ending punctuation.','Conventions#EndingPunct')]

#TODO: Add links to commented definitions

# Error: Not capitalised word after a period.
#CapsPeriod = Error("[A-Z]?[a-z]+\.[\'\"]?\s[\'\"]?[a-z]+","Capitalisation Error", trivial, [], 'This checks when the word immediately after a full stop is not capitalised.')

# Error: Passive voice
# May be replaced by sentence processing
#PassiveVoice = Error(('\swas\s[A-Za-z]+ed\s','\swere\s[A-Za-z]+ed\s','\sis\s[A-Za-z]+ed\s','\sare\s[A-Za-z]+ed\s','\swas\s[A-Za-z]+en\s','\swere\s[A-Za-z]+en\s','\sis\s[A-Za-z]+en\s','\sare\s[A-Za-z]+en\s','\sget\s[A-Za-z]+ed\s','\sget\s[A-Za-z]+en\s','\sgot\s[A-Za-z]+ed\s','\sgot\s[A-Za-z]+en\s','\shad\sbeen\s[A-Za-z]+ed\sby\s','\shad\sbeen\s[A-Za-z]+en\sby\s','\shas\sbeen\s[A-Za-z]+ed\sby\s','\shas\sbeen\s[A-Za-z]+en\sby\s'),"Passive Voice", trivial, [], 'This looks for passive voice, which is where the subject experiences the action, instead of performing the action. While not an error, this is often weaker and less interesting than using the active voice.')

#Error: Improperly punctuated dialogue, comma to non-attribution
# May be replaced by sentence processing
#DialogueComma = Error('([A-Za-z\']+,\" ([A-Za-z\'-]+ )?(Mrs?\.? )?(Ms\.? )?(Dr\.? )?(the )?([A-Z]?[a-z\'-]+ ){,2}([A-Z]?[a-z]+)[ ,\.!\?;:-])',"Dialogue without speaking verb", dialoguecomma, [], 'This checks that dialogue follows generally accepted formatting. In particular, this makes sure that the section of the sentence connected to the dialogue by a comma is a direct attribution, rather than an unrelated sentence.')

#Error: Improperly punctuated dialogue, Ending sentence prior to attribution
# May be replaced by sentence processing
#DialoguePeriod = Error('([A-Za-z]+[\.!\?(\.\.\.)(---)]" ([A-Za-z\'-]+|(Mrs?\.?)|(Ms\.?)|(Dr\.?)) ([A-Z][a-z\']+ ){,2}([a-z-]+ ){,2}[a-z]+[ ,\.!\?;:-])',"Dialogue ends sentence before attribution", dialogueperiod, [], 'This checks that dialogue follows generally accepted formatting. In particular, this makes sure that when the dialogue has punctuation ending the sentence, the following sentence is not an attribution.')

#Error: Improperly punctuated dialogue, Front non-attribution with comma
# May be replaced by sentence processing
#DialogueFront = Error('(([A-Z][A-Za-z\']+ )?([A-Za-z\']+ )?[A-Za-z\']+, \"[A-Za-z\']+)', "Dialogue follows nonattribution", dialoguefront, [], 'This checks that dialogue follows generally accepted formatting. In particular, this checks that a sentence leading into dialogue is an attribution, rather than an unrelated sentence that should be separated.')

#Error: No space after punctuation
#PunctSpace = Error('[A-Za-z\']+[\.;,!?]{1,3}"?[A-Za-z][A-Za-z\']*',"Punctuation without a trailing space", trivial, [], 'This checks that punctuation is properly separated from the following word.')

#Error: Double space between words.
#DoubleSpace = Error('[A-Za-z][A-Za-z\']*[,\.\?!;:\"-]?  \"?[A-Za-z][A-Za-z\']*',"Extra Space", trivial, [], 'This checks that there aren\'t extra spaces between words.')

#RandCaps = Error('[A-Za-z\']+[;,]? [A-Z][A-Za-z\']*',"Uncommonly capitalised word", randcaps, [], 'This flags words that do not look to be proper nouns that are capitalised in the middle of a sentence.')

# Punctuation outside of quotes or no ending punctuation
#PunctOutsideQuote = Error('[A-Za-z\']+[,\.;!?-]?"[,\.;!?-] [A-Za-z][A-Za-z\']*',"Punctuation Outside Quotes", trivial, [],'This flags punctuation that does not follow convention and occurs outside of the quotation marks.')

# Beginning of paragraph not capitalised
#ParagraphCaps = Error('^\s*[\'\"]?[a-z\']+ ',"Beginning of paragraph not capitalised", trivial, [], 'This checks that the initial sentence of each paragraph is properly capitalised.')


#Ending of paragraph with no punctuation
#EndingPunct = Error('[A-Za-z\']+[,\.\?!:]? [A-Za-z\']+[\",]?\s*$',"End of paragraph missing punctuation", trivial, [], 'This checks that the sentence at the end of each paragraph is not missing ending punctuation.') 
