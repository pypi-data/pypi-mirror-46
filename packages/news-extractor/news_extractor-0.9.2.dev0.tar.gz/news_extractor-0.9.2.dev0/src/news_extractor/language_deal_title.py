# -*- coding: utf-8 -*-
import nltk,operatorimport jieba_fast as jieba
import jieba_fast.posseg as pseg

def title_filter(title_list,text):
    # title_list = [a,b,c,d,e,f,g,h,i]
    # data_one=jieba.lcut(text)
    
    word_filter = []
    for word in pseg.cut(text):
        if word.flag in ['n','vn','v','eng','nr','ng','l','nt','ns','nz','ng','nrj','nrf','nsf']:
            word_filter.append(word)

    word_count = {}
    for word in word_filter:
        info = nltk.text.Text(jieba.lcut(text))
        word_count[word]=info.count(word.word)/len(word_filter)
    # print(word_count)
    sorted_word = sorted(word_count.items(),key=operator.itemgetter(1),reverse = True)
    # print(sorted_word[0:5])
    k = sum([i[1] for i in sorted_word[0:5]])/5
    # print(k)
    for word,value in word_count.items():
        if word.flag in ['nr','nr1','nr2','nrj','nrf','ns','nsf','nt']:
            if value < k:
                word_count[word]=k

    sorted_word = sorted(word_count.items(),key=operator.itemgetter(1),reverse = True)
    # print(sorted_word)
    finally_info = {}
    for title in title_list:
        if title not in finally_info.keys():
            finally_info[title]=0
        for i in jieba.lcut(title):
            for j,k in word_count.items():
                if i == j.word:
                    finally_info[title] += k

    sorted_title = sorted(finally_info.items(),key=operator.itemgetter(1),reverse = True)[0]
    # print(sorted_title)
    return sorted_title[0]


