mod=5000
from asyncio.windows_events import NULL
from itertools import count
from logging import NullHandler
from queue import Empty
from tkinter import W
import pandas as pd
import math
pd.options.mode.chained_assignment = None  # default='warn'
idf = pd.read_excel(r'tut02\input_octant_transition_identify.xlsx')


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
count1=[0]*n     
T_count_1=0
count2=[0]*n
T_count_2=0
count3=[0]*n
T_count_3=0
count4=[0]*n
T_count_4=0
count_minus_1=[0]*n
T_count_min_1=0
count_minus_2=[0]*n
T_count_min_2=0
count_minus_3=[0]*n
T_count_min_3=0
count_minus_4=[0]*n
T_count_min_4=0
t=0
temp_mod=mod # temp_mod will get updated when loop runs mod times  
idf['octant']=0
idf[""]=""
idf.loc[1,""]="User Input"
for i in range(idf['U'].size):
    u = idf.loc[i,"U'=U-U_avg"]
    v = idf.loc[i,"V'=V-V_avg"]
    w = idf.loc[i,"W'=W-W_avg"]
    if i>temp_mod:
        t=t+1
        temp_mod=temp_mod+mod    # updating temp_mod  5000 to 10000 , 10000 to 15000 and so on
    if u>0 and v>0:
        if w>0:
            idf['octant'][i]=1
            count1[t]+=1
    if u>0 and v>0:
        if w<0:
            idf['octant'][i]=-1
            count_minus_1[t]+=1
    if u<0 and v>0:
        if w>0:
            idf['octant'][i]=2
            count2[t]+=1
    if u<0 and v>0:
        if w<0:
            idf['octant'][i]=-2
            count_minus_2[t]+=1
    if u<0 and v<0:
        if w>0:
            idf['octant'][i]=3
            count3[t]+=1
    if u<0 and v<0:
        if w<0:
            idf['octant'][i]=-3
            count_minus_3[t]+=1
    if u>0 and v<0:
        if w>0:
            idf['octant'][i]=4
            count4[t]+=1
    if u>0 and v<0:
        if w<0:
            idf['octant'][i]=-4
            count_minus_4[t]+=1

# 
for i in range(n):
    T_count_1+=count1[i]
    T_count_2+=count2[i]
    T_count_3+=count3[i]
    T_count_4+=count4[i]
    T_count_min_1+=count_minus_1[i]
    T_count_min_2+=count_minus_2[i]
    T_count_min_3+=count_minus_3[i]
    T_count_min_4+=count_minus_4[i]


# inserting all calculated  values using idf
idf.loc[0,"Octant ID"] = "Overall Count"
strM = "Mod "
idf.loc[1,"Octant ID"] = strM + str(mod)
idf.loc[0,"1"] = T_count_1
idf.loc[0,"-1"] = T_count_min_1
idf.loc[0,"2"] = T_count_2
idf.loc[0,"-2"] = T_count_min_2
idf.loc[0,"3"] = T_count_3
idf.loc[0,"-3"] = T_count_min_3
idf.loc[0,"4"] = T_count_4
idf.loc[0,"-4"] = T_count_min_4
temp_string = "Mod " + str(mod)


idf.loc[1,"Octant ID"] = "" # Creating Octant ID colm
start_int = 0000
end_int = 5000
for i in range(t+1):
    temp_string = str(start_int)+ "-" + str(end_int) # string for 'Octant ID' colm
    idf.loc[i+2,"Octant ID"] = temp_string
    idf.loc[i+2,"1"] = count1[i]
    idf.loc[i+2,"-1"] = count_minus_1[i]
    idf.loc[i+2,"2"] = count2[i]
    idf.loc[i+2,"-2"] = count_minus_2[i]
    idf.loc[i+2,"3"] = count3[i]
    idf.loc[i+2,"-3"] = count_minus_3[i]
    idf.loc[i+2,"4"] = count4[i]
    idf.loc[i+2,"-4"] = count_minus_4[i]
    start_int+=mod
    end_int=min(end_int+mod-1,idf['U'].size-1)


 
# Tutorial 2 main code

# transition matrice list , initailising with zero
tr_matrice={}
for i in range(-4,5):
    for j in range(-4,5):
        temp_str = ""
        temp_str = str(i)+str(j)
        tr_matrice[temp_str]=0




for i in range(idf['U'].size-1):
      key =""
      key = str(idf['octant'][i]) + str(idf['octant'][i+1])
      tr_matrice[key]+=1
    





n=n+3
idf.loc[n,"Octant ID"] = "Overall Transition Count"
idf.loc[n+1,"1"] = "To"
idf.loc[n+2,"Octant ID"]="Count"
idf.loc[n+3,"Octant ID"]="+1"
idf.loc[n+4,"Octant ID"]="-1"
idf.loc[n+5,"Octant ID"]="+2"
idf.loc[n+6,"Octant ID"]="-2"
idf.loc[n+7,"Octant ID"]="+3"
idf.loc[n+8,"Octant ID"]="-3"
idf.loc[n+9,"Octant ID"]="+4"
idf.loc[n+10,"Octant ID"]="-4"
idf.loc[n+3,""] = "From"
idf.loc[n+2,"1"] = "+1"
idf.loc[n+2,"-1"] = "-1"
idf.loc[n+2,"2"] = "+2"
idf.loc[n+2,"-2"] = "-2"
idf.loc[n+2,"3"] = "+3"
idf.loc[n+2,"-3"] = "-3"
idf.loc[n+2,"4"] = "+4"
idf.loc[n+2,"-4"] = "-4"

for i in range(-4,5):
    temp_i=n+2
    if(i==0):
        continue
    if(i==1):
        temp_i +=1
    if(i==-1):
        temp_i +=2
    if(i==2):
        temp_i +=3
    if(i==-2):
        temp_i +=4
    if(i==3):
        temp_i +=5
    if(i==-3):
        temp_i +=6
    if(i==4):
        temp_i +=7
    if(i==-4):
        temp_i +=8
    for j in range(-4,5):
        temp_j=""
        if(j==0):
            continue
        temp_j = temp_j + str(j)
        key=""
        key = str(i)+str(j)
        idf.loc[temp_i,temp_j] = tr_matrice[key]

# diffrent ranges {transition matrice}
# creating data for diffrent ranges
No_Of_Mod_tr = int((idf['U'].size+mod)/mod)
new_temp_mod=0
st=0
for k in range(No_Of_Mod_tr):
    last_tr=0
    n+=14
    st=new_temp_mod
    if(new_temp_mod==0):
        new_temp_mod=-1
    new_temp_mod+=mod
    mtr_matrice={}
    for i in range(-4,5):
        for j in range(-4,5):
            mtemp_str = ""
            mtemp_str = str(i)+str(j)
            mtr_matrice[mtemp_str]=0 
    for i in range(st,new_temp_mod):
      if(i>(idf['U'].size-2)):
        break
      key =""
      key = str(idf['octant'][i]) + str(idf['octant'][i+1])
      mtr_matrice[key]+=1
    idf.loc[n,"Octant ID"] = "Overall Transition Count"
    range_str =""
    if(new_temp_mod>idf['U'].size):
        range_str= str(st+1)+"-"+str(idf['U'].size)
    elif(st==0):
        range_str= str(st)+"-"+str(new_temp_mod)
    else:
        range_str= str(st+1)+"-"+str(new_temp_mod)
    idf.loc[n+1,"Octant ID"] = range_str
    idf.loc[n+1,"1"] = "To"
    idf.loc[n+2,"Octant ID"]="Count"
    idf.loc[n+3,"Octant ID"]="+1"
    idf.loc[n+4,"Octant ID"]="-1"
    idf.loc[n+5,"Octant ID"]="+2"
    idf.loc[n+6,"Octant ID"]="-2"
    idf.loc[n+7,"Octant ID"]="+3"
    idf.loc[n+8,"Octant ID"]="-3"
    idf.loc[n+9,"Octant ID"]="+4"
    idf.loc[n+10,"Octant ID"]="-4"
    idf.loc[n+3,""] = "From"
    idf.loc[n+2,"1"] = "+1"
    idf.loc[n+2,"-1"] = "-1"
    idf.loc[n+2,"2"] = "+2"
    idf.loc[n+2,"-2"] = "-2"
    idf.loc[n+2,"3"] = "+3"
    idf.loc[n+2,"-3"] = "-3"
    idf.loc[n+2,"4"] = "+4"
    idf.loc[n+2,"-4"] = "-4"

    for i in range(-4,5):
        temp_i=n+2
        if(i==0):
            continue
        if(i==1):
            temp_i +=1
        if(i==-1):
            temp_i +=2
        if(i==2):
            temp_i +=3
        if(i==-2):
            temp_i +=4
        if(i==3):
            temp_i +=5
        if(i==-3):
            temp_i +=6
        if(i==4):
            temp_i +=7
        if(i==-4):
            temp_i +=8
        for j in range(-4,5):
            temp_j=""
            if(j==0):
                continue
            temp_j = temp_j + str(j)
            key=""
            key = str(i)+str(j)
            idf.loc[temp_i,temp_j] = mtr_matrice[key]

# inserting all data in file
idf.to_excel('tut02\output_octant_transition_identify.xlsx')
    
    
    
    
    











