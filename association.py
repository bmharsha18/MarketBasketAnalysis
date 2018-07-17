#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar 30 12:23:02 2018

@author: harshabm
"""
from sys import exit
import csv
import itertools

def findsubsets(S,m):
    return list(set(itertools.combinations(S,m)))

def calculate_count(temp):
    count = 0
    ctr = 0
    for i in dataset:
        ctr=0
        for j in range(len(temp)):
            if(temp[j] in i):
                ctr+=1
        if(ctr==len(temp)):
            count+=1            
    return count

def count_single(temp):
    count=0
    for i in dataset:
        if(temp in i):
            count+=1
    return count

def print_output(temp,t2):
    print("\n",str(temp[0]),"->",str(temp[1]),"\nwith confidence = ",t2)
    
    
dataset = list()
fp = open('groceries.txt','r')
reader = csv.reader(fp , delimiter=',')
for row in reader:
    dataset.append(row)
no_of_transactions = len(dataset)


distinct = list()
for i in dataset:
    for j in i:
        if j not in distinct:
            distinct.append(j)

occurance = {}
for i in distinct:
    count = 0
    for j in dataset:
        for item in j:
            if (str(item)==str(i)):
                count+=1
    occurance.update({i:count})
    
s1 = "Enter minimum support count out of "+str(len(dataset))+" transactions :"
print("\nPREFERABLY-----Enter support count value between 318 and 557")
min_support = float(input(s1))
#min_support = (min_support/100)*no_of_transactions
#min_support = round(min_support)
min_confidence = float(input("Enter minimum confidence percentage: "))
min_confidence = min_confidence/100.0
print("\nMarket basket analysis !!")
print("\nNumber of transactions in dataset : ",len(dataset))

temp_dict = occurance.copy()
for i in temp_dict:
    if(temp_dict[i] < min_support):
        occurance.pop(i)
        
distinct_one = list()
for i in occurance:
    distinct_one.append(i)

dict_2 = {}
if(len(distinct_one)>1):
    a1 = findsubsets(distinct_one,2)
    for i in range(len(a1)):
        counter=0
        for j in range(len(dataset)):
            if(a1[i][0] in dataset[j] and a1[i][1] in dataset[j]):
                counter+=1
        dict_2.update({a1[i]:counter})

    temp_dict = dict_2.copy()
    for i in temp_dict:
        if(temp_dict[i] < min_support):
            dict_2.pop(i)

    distinct_two = list()
    for i in dict_2:
        for j in i:
            if j not in distinct_two:
                distinct_two.append(j)

else:
    distinct_two = list()

dict_3={}

if(len(distinct_two)>2):
    a2 = findsubsets(distinct_two,3)
    for i in range(len(a2)):
        counter=0
        for j in range(len(dataset)):
            if((a2[i][0] in dataset[j]) and (a2[i][1] in dataset[j]) and (a2[i][2] in dataset[j])):
                counter+=1
        dict_3.update({a2[i]:counter})

    temp_dict = dict_3.copy()
    for i in temp_dict:
        if(temp_dict[i] <min_support):
            dict_3.pop(i)

    distinct_three = list()
    for i in dict_3:
        for j in i:
            if j not in distinct_three:
                distinct_three.append(j)
else:
    distinct_three = list()

dict_4={}

if(len(distinct_three)>3):
    a3 = findsubsets(distinct_three,4)
    for i in range(len(a3)):
        counter=0
        for j in range(len(dataset)):
             if((a3[i][0] in dataset[j]) and (a3[i][1] in dataset[j]) and (a3[i][2] in dataset[j]) and (a3[i][3] in dataset[j])):
                 counter+=1
        dict_4.update({a3[i]:counter})

    temp_dict = dict_4.copy()
    for i in temp_dict:
        if(temp_dict[i] <min_support):
            dict_4.pop(i)


frequent = list()

if(len(dict_4)!=0):
    frequent = list(dict_4)
    #print("dict4")
elif(len(dict_3)!=0):
    frequent = list(dict_3)
    #print("dict3")
elif(len(dict_2)!=0):
    frequent = list(dict_2)
    #print("dict2")

frequent_item_set = list()
for i in frequent:
    for j in i:
        if j not in frequent_item_set:
            frequent_item_set.append(j)
    
rules = {}

if(len(frequent_item_set)>1):
    for i in frequent_item_set:
        rules.update({i:(set(frequent_item_set)-set([i]))})

for i in range(2,len(frequent_item_set)+1):
    if(len(frequent_item_set)>i):
        a = findsubsets(frequent_item_set,i)
        for j in a:
            rules.update({j:(set(frequent_item_set)-set(j))})

if(len(rules)!=0):
    confidence = calculate_count(frequent_item_set)
    if(confidence==0):
        print("Increase the support percentage!!")
        exit()  
    sigma = list()
    for i in rules:
        sigma.append(i)

    count_values = list()
    for i in sigma:
        if(len(i)>1):
            count_values.append(calculate_count(i))
        else:
            count_values.append(count_single(i))

    final_confidence = list()
    for i in count_values:
        if i!=0:
            temp = confidence/i
            final_confidence.append(temp)
        else:
            temp = 0
            final_confidence.append(temp)
            
    final_support = list()
    
    tp = list(rules.items())
    ctr = 0
    print("RULES GENERATED!!")
    for i in range(len(final_confidence)):
        t2 = final_confidence[i]
        if t2 >= min_confidence:
            print_output(tp[i],t2)
            ctr+=1
        else:
            del rules[tp[i][0]]
            
    if(ctr==0):
        print(len(rules)," rules generated with less than given confidence percentage!")
        print("Reduced the confidence percentage!!")
    
    if(ctr>0):
        print("\nNumber of rules generated are : ",ctr)
            
elif(len(rules)==0):
    print("\nNo rules generated with given support and confidence!!")
    print("\nRUN AGAIN\n and reduce the support_percentage")












