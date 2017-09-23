# HW7 - Q2 - Bag of words

import os
path = "c:\\users\\lavanya\\desktop\\financial Accounting\\week 8"
os.chdir(path)
import re

file = open('HW7_Tesla_2015.txt', 'r')
data = file.read().lower()
file.close()
file = open('HW7_LM_pos_words.txt', 'r')
data_pos = file.read().lower()
file.close()
file = open('HW7_LM_neg_words.txt', 'r')
data_neg = file.read().lower()
file.close()

data = re.sub('[^a-z\ \']+', " ", data)
data_list = list(data.split())
pos_list = list(data_pos.split())
neg_list = list(data_neg.split())

len_data_list = len(data_list)
len_pos_list = len(pos_list)
len_neg_list = len(neg_list)

pos_count = 0
neg_count = 0
data_pos_list = []
data_neg_list = []
word_no_count = 0
word_not_count = 0
word_never_count = 0

for i in range(0,len_data_list):
    for j in range(0,len_pos_list):
        if data_list[i] == pos_list[j] :
            pos_count += 1
            data_pos_list.append(data_list[i])
    for k in range(0,len_neg_list):
        if data_list[i] == neg_list[k] :
            neg_count += 1
            data_neg_list.append(data_list[i])
    if data_list[i] == "no" :
        word_no_count += 1
    if data_list[i] == "not" :
        word_not_count += 1
    if data_list[i] == "never" :
        word_never_count += 1

print '\nTotal no of words : {}'.format(len_data_list)

print '\nNo of positive words : {}\nPositive Words : '.format(pos_count)
print data_pos_list
print '\nNo of negative words : {}\nNegative Words : '.format(neg_count)
print data_neg_list

print '\nRelative percentage of positive words : {}'.format(float(pos_count - neg_count)/float(len_data_list)*100)
print 'Percentage of positive words : {}'.format(float(pos_count)/float(len_data_list)*100)
print 'Percentage of negative words : {}'.format(float(neg_count)/float(len_data_list)*100)

print '\nCount of word "no" : {}'.format(word_no_count)
print 'Count of word "not" : {}'.format(word_not_count)
print 'Count of word "never" : {}'.format(word_never_count)

pos_count = 0
neg_count = 0
data_pos_list = []
data_neg_list = []

####################################

for i in range(0,len_data_list):
    for j in range(0,len_pos_list):
        if data_list[i] == pos_list[j] or (data_list[i] == neg_list[j] and (data_list[i-1] == "no" or data_list[i-1] == "not" or data_list[i-1] == "never"  )) :
            pos_count += 1
            data_pos_list.append(data_list[i])
    for k in range(0,len_neg_list):
        if data_list[i] == neg_list[k]  or (data_list[i] == pos_list[j] and (data_list[i-1] == "no" or data_list[i-1] == "not" or data_list[i-1] == "never"  )) :
            neg_count += 1
            data_neg_list.append(data_list[i])
    
print '\nTotal no of words : {}'.format(len_data_list)

print '\nNo of positive words : {}\nPositive Words : '.format(pos_count)
print data_pos_list
print '\nNo of negative words : {}\nNegative Words : '.format(neg_count)
print data_neg_list

print '\nRelative percentage of positive words : {}'.format(float(pos_count - neg_count)/float(len_data_list)*100)
print 'Percentage of positive words : {}'.format(float(pos_count)/float(len_data_list)*100)
print 'Percentage of negative words : {}'.format(float(neg_count)/float(len_data_list)*100)
