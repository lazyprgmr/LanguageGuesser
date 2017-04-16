#coding:utf-8

import unicodedata
import operator
import string
import glob
import os.path
from nltk.tokenize import word_tokenize
from nltk.util import ngrams

#file which contains the language to be detected
filename = raw_input("Enter the file name: ")
fp = open(filename)
text = fp.read().decode('utf8')
fp.close()

#tokenize the text of the file
#rawtext = text.translate(None, string.punctuation)
#words = [w.lower() for w in rawtext.split(" ")]
words = word_tokenize(text)

#generate ngrams for the text
gen_ngrams=[]
for word in words:
	for i in range(1,6):
		temp = ngrams(word, i, pad_left = True, pad_right = True, left_pad_symbol = ' ', right_pad_symbol =' ')
		#join the characters of individual ngrams
		for t in temp:
			ngram = ''.join(t)
			gen_ngrams.append(ngram)

#calculate ngram frequencies of the text
ngram_stats = {}
for n in gen_ngrams:
	if not ngram_stats.has_key(n):
		ngram_stats.update({n:1})
	else:
		ng_count = ngram_stats[n]
		ngram_stats.update({n:ng_count+1})

#now sort them, add an iterator to dict and reverse sort based on second column(count of ngrams)
ngrams_txt_sorted = sorted(ngram_stats.iteritems(), key=operator.itemgetter(1), reverse = True)[0:300]

#Load ngram language statistics
lang_stats={}
for filepath in glob.glob('./langdata/*.dat'):
	filename = os.path.basename(filepath)
	lang = os.path.splitext(filename)[0]
	ngram_stats = open(filepath,"r").readlines()
	ngram_stats = [x.rstrip() for x in ngram_stats]
	lang_stats.update({lang:ngram_stats})

#compare ngram frequency statistics by doing a rank order lookup
lang_ratios = {}
txt_ng = [ng[0] for ng in ngrams_txt_sorted]
max_out_of_place = len(txt_ng)
for lang, ngram_stat in lang_stats.iteritems():
	lang_ng = [ng[0] for ng in ngram_stat]
	doc_dist = 0
	for n in txt_ng:
		try:
			txt_ng_index = txt_ng.index(n)
			lang_ng_index = lang_ng.index(n.encode('utf8'))
		except ValueError:
			lang_ng_index = max_out_of_place
		doc_dist += abs(lang_ng_index - txt_ng_index)
	lang_ratios.update({lang:doc_dist})
for i in lang_ratios.iteritems():
	print i
predicted_lang = min(lang_ratios, key=lang_ratios.get)
print "The language is",predicted_lang
