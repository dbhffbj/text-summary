from heapq import nlargest
import pandas as pd

import spacy
from spacy.lang.en.stop_words import STOP_WORDS
from string import punctuation

#text="One of the most important aspects of reading for academic study is reading so you can make use of the ideas of other people. This is important as you need to show that you have understood the materials you have read and that you can use their ideas and findings in your own way. In fact, this is an essential skill for every student. Spack (1988, p. 42) has pointed out that the most important skill a student can engage in is the complex activity to write from other texts, which is a major part of their academic experience. It is very important when you do this to make sure you use your own words, unless you are quoting. You must make it clear when the words or ideas that you are using are your own and when they are taken from another writer. You must not use another person's words or ideas as if they were your own: this is Plagiarism and plagiarism is regarded as a very serious offence."

def summarizer(rawdocs):
    stopwords=list(STOP_WORDS)
    #print(stopwords)


    nlp=spacy.load('en_core_web_sm')
    doc=nlp(rawdocs)#changed from text
    #print(doc)

    tokens= [token.text for token in doc]
    #print(tokens)

    word_freq={}
    for word in doc:
        if word.text.lower() not in stopwords and word.text.lower() not in punctuation:
            if word.text not in word_freq.keys():
                word_freq[word.text]= 1
            else:
                word_freq[word.text] += 1

    #print(word_freq)


    max_freq = max(word_freq.values())  
    #print(max_freq) 



    for word in word_freq.keys():  
        word_freq[word] = (word_freq[word]/max_freq)
    #print(word_freq)


    sent_tokens = [sent for sent in doc.sents]
    #print(sent_tokens)


    sent_scores = {}
    for sent in sent_tokens:
        for word in sent:
            if word.text in word_freq.keys():
                if sent not in sent_scores.keys():
                    sent_scores[sent] = word_freq[word.text]
                else:
                    sent_scores[sent] += word_freq[word.text]

    #print(sent_scores)

    select_len= int(len(sent_tokens) * 0.3)
    #print(select_len)



    summary= nlargest(select_len,sent_scores, key=sent_scores.get)
    #print(summary)

    final_summary=(word.text for word in summary)
    summary=' '.join(final_summary)

    #print(text)
    #print(final_summary)
    #print("Length of original text ",len(text.split(' ')))
    #print("Length of summary ",len(summary.split(' ')))

    return summary,doc,len(rawdocs.split(' ')),len(summary.split(' '))

