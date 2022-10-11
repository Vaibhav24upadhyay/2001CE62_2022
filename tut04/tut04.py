mod=5000
from asyncio.windows_events import NULL
from itertools import count
from logging import NullHandler
from operator import length_hint
from queue import Empty
from tkinter import W
import pandas as pd
import math
pd.options.mode.chained_assignment = None  # default='warn'
idf = pd.read_excel(r'tut04\input_octant_longest_subsequence_with_range.xlsx')


# Calculating mean of U , V , W
U_Avg = idf["U"].mean()
V_Avg= idf["V"].mean()
W_Avg = idf["W"].mean()

# inserting mean values
idf.loc[0,"U Avg"] = U_Avg
idf.loc[0,"V Avg"] = V_Avg
idf.loc[0,"W Avg"] = W_Avg

# Calculating U' , V' , W' ,
idf["U'=U-U_avg"] =""
idf["V'=V-V_avg"] =""
idf["W'=W-W_avg"] =""
idf["U'=U-U_avg"] = idf["U"]-U_Avg
idf["V'=V-V_avg"] = idf["V"]-V_Avg
idf["W'=W-W_avg"] = idf["W"]-W_Avg


# finding total number of interval {0-5000 ,5001-10000 , -->> so on}
n=int((idf['U'].size+mod)/mod)

# initializing variables for counting required counts

octant_colm = [] # for storing value of octant

# count1[0] will count '1' comes in 0 to 5000 and count1[0] will count '1' in 5001 to 10000 and so on-->   
     


temp_mod=mod # temp_mod will get updated when loop runs mod times  
idf['octant']=0
idf[""]=""
# idf.loc[1,""]="User Input"
for i in range(idf['U'].size):
    u = idf.loc[i,"U'=U-U_avg"]
    v = idf.loc[i,"V'=V-V_avg"]
    w = idf.loc[i,"W'=W-W_avg"]
 # updating temp_mod  5000 to 10000 , 10000 to 15000 and so on
    if u>0 and v>0:
        if w>0:
            idf['octant'][i]=1
    if u>0 and v>0:
        if w<0:
            idf['octant'][i]=-1
    if u<0 and v>0:
        if w>0:
            idf['octant'][i]=2
    if u<0 and v>0:
        if w<0:
            idf['octant'][i]=-2
    if u<0 and v<0:
        if w>0:
            idf['octant'][i]=3
    if u<0 and v<0:
        if w<0:
            idf['octant'][i]=-3
    if u>0 and v<0:
        if w>0:
            idf['octant'][i]=4
    if u>0 and v<0:
        if w<0:
            idf['octant'][i]=-4



# finding Maximum length of octant consecutive
Total_count_max=[0]*9
max_length=[0]*9 # max length of octant (list) 

for i in range(1,9):
    int_temp=i
    if(i==5):
        int_temp=-1
    if(i==6):
        int_temp=-2
    if(i==7):
        int_temp=-3
    if(i==8):
        int_temp=-4
    curr_len=1
    for j in range(idf['U'].size-1):# 
        if(idf.loc[j]['octant']!=int_temp):
            curr_len=1
            continue
        if(idf.loc[j]['octant']==idf.loc[j+1]['octant']):
            curr_len+=1
        if(curr_len>max_length[i]):
            max_length[i]=curr_len



# finding count  
n1=idf['U'].size
md1={-1:0,-2:0,-3:0,-4:0,1:0,2:0,3:0,4:0} 
md1[-1]=max_length[5]
md1[-2]=max_length[6]
md1[-3]=max_length[7]
md1[-4]=max_length[8]
md1[1]=max_length[1]
md1[2]=max_length[2]
md1[3]=max_length[3]
md1[4]=max_length[4]

# Main code for Tutorial 4  

# making colms
idf[""]=""
idf["Count"] =""
idf["Longest Subsquence Length"] =""
idf["count"] =""
idf["  "]=""
idf["COUNT"]=""
idf["LONGEST SUBSQUENCE LENGHTH"]=""
idf["FREQUENCE"]=""

md2={-1:0,-2:0,-3:0,-4:0,1:0,2:0,3:0,4:0}
count=0
n=0

# calculating count/frequnce and insertingdata in file
for i in range(-4,5):
    if i==0:
        continue
    idf.loc[n,"COUNT"]=str(i)
    idf.loc[n,"LONGEST SUBSQUENCE LENGHTH"]=md1[i]
    n=n+1
    idf.loc[n,"COUNT"]="Time"
    idf.loc[n,"LONGEST SUBSQUENCE LENGHTH"]="From"
    idf.loc[n,"FREQUENCE"]="To"
    n=n+1
    for j in range(n1):
        if(idf['octant'][j]==i):
            count+=1
        else:
            if(count==md1[i]):
                idf.loc[n,"LONGEST SUBSQUENCE LENGHTH"]=(j-md1[i])/100
                idf.loc[n,"FREQUENCE"]=(j-1)/100
                md2[i]+=1
                n=n+1
            count=0
q=0
for i in range(-4,5):
    if(i==0):
        continue
    idf.loc[q,"FREQUENCE"]=md2[i]
    q=q+2
    q=q+md2[i]
# inserting data in file
n=0
idf.loc[n,"Count"]="+1"
idf.loc[n+1,"Count"]="-1"
idf.loc[n+2,"Count"]="+2"
idf.loc[n+3,"Count"]="-2"
idf.loc[n+4,"Count"]="+3"
idf.loc[n+5,"Count"]="-3"
idf.loc[n+6,"Count"]="+4"
idf.loc[n+7,"Count"]="-4"
idf.loc[n,"Longest Subsquence Length"]=md1[1]
idf.loc[n+1,"Longest Subsquence Length"]=md1[-1]
idf.loc[n+2,"Longest Subsquence Length"]=md1[2]
idf.loc[n+3,"Longest Subsquence Length"]=md1[-2]
idf.loc[n+4,"Longest Subsquence Length"]=md1[3]
idf.loc[n+5,"Longest Subsquence Length"]=md1[-3]
idf.loc[n+6,"Longest Subsquence Length"]=md1[4]
idf.loc[n+7,"Longest Subsquence Length"]=md1[-4]
idf.loc[n,"count"]=md2[1]
idf.loc[n+1,"count"]=md2[-1]
idf.loc[n+2,"count"]=md2[2]
idf.loc[n+3,"count"]=md2[-2]
idf.loc[n+4,"count"]=md2[3]
idf.loc[n+5,"count"]=md2[-3]
idf.loc[n+6,"count"]=md2[4]
idf.loc[n+7,"count"]=md2[-4]
idf.to_excel('tut04\output_octant_longest_subsequence_with_range.xlsx')

