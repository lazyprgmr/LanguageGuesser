#Languages that can be detected ['danish', 'dutch', 'english', 'finnish', 'french', 'german', 'hungarian', 'italian', 'norwegian', 'portuguese', 'russian', 'spanish', 'swedish', 'turkish']


from nltk import wordpunct_tokenize			#We will split sentences into tokens without any consideration for contractions and punctuations
from nltk.corpus import stopwords

def _lang_ratios(text):
	lang_ratios={}								#initialize a dictionary called lang_ratios
	tokens = wordpunct_tokenize(text)			#tokenize text
	words = [word.lower() for word in tokens]	#convert to lower case 
	words_set = set(words)
	
	for language in stopwords.fileids():		#select a language from the list of available languages
		stopwords_set = set(stopwords.words(language))	
		common_set = words_set.intersection(stopwords_set)
		lang_ratios[language] = len(common_set)
	
	return lang_ratios
	
def detect_language(text):
	ratios = _lang_ratios(text)
	lang = max(ratios, key=ratios.get)			#the key option takes a function returns the key having the largest "value" in the iterable
	return lang

filename = raw_input("Enter the filename: ")
with open(filename, "r") as fileobject:	
	text = fileobject.read()
print detect_language(text)
