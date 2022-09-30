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
idf = pd.read_excel(r'tut03\input_octant_longest_subsequence.xlsx')


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


    