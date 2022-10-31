mod=5000
from asyncio.windows_events import NULL
from itertools import count
from logging import NullHandler
from queue import Empty
from tkinter import W
import pandas as pd
import math
pd.options.mode.chained_assignment = None  # default='warn'
try:
    idf = pd.read_excel(r'tut05\octant_input.xlsx')
except:
    print ("File not found")
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

# Creating colms
idf["Rank of 1"]=""
idf["Rank of -1"]="" 
idf["Rank of 2"]="" 
idf["Rank of -2"]=""
idf["Rank of 3"]=""
idf["Rank of -3"]=""
idf["Rank of 4"]=""
idf["Rank of -4"]=""
idf["Rank1 Octant ID"]=""
idf["Rank1 Octant Name"]=""

# Creating dictionary for octant name 
Oct_name={ "1":"Internal outward interaction","-1":"Exteranl outward interaction","2":"External Ejection","-2" :"Internal Ejection", "3":"External inward interaction","-3":"Internal inward interaction","4":"Internal sweep","-4": "External sweep"}
# Creating dictionary for ranking of octant 
temp_rnk={ "1": T_count_1,"-1":T_count_min_1,"2":T_count_2,"-2" :T_count_min_2, "3":T_count_3,"-3":T_count_min_3,"4":T_count_4,"-4":T_count_min_4}
# # Creating dictionary for storing count of octant rank 1 
count_rnk={ "1":0,"-1":0,"2":0,"-2" :0, "3":0,"-3":0,"4":0,"-4":0}
srt_by_val={k:v for k, v in sorted(temp_rnk.items(),key = lambda v:v[1]) }
ranking = 8
max_ranking=""
for r in srt_by_val.keys():
    if ranking == 1:
        max_ranking = r
        # marking first rank
    idf.loc[0,"Rank of "+r]=ranking
    ranking =ranking - 1
idf.loc[0,"Rank1 Octant ID"] = int(max_ranking)
idf.loc[0,"Rank1 Octant Name"] = Oct_name[max_ranking]

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
    temp_rank={ "1": count1[i],"-1":count_minus_1[i],"2":count2[i],"-2" :count_minus_2[i], "3":count3[i],"-3":count_minus_3[i],"4":count4[i],"-4":count_minus_4[i]}
    sort_by_val={k:v for k, v in sorted(temp_rank.items(),key = lambda v:v[1]) }
    ranking = 8
    max_ranking=""
    for r in sort_by_val.keys():
        if ranking == 1:
            max_ranking = r
            # marking first rank
            count_rnk[r]=count_rnk[r]+1
        idf.loc[i+2,"Rank of "+r]=ranking
        ranking =ranking - 1
    idf.loc[i+2,"Rank1 Octant ID"] = int(max_ranking)
    idf.loc[i+2,"Rank1 Octant Name"] = Oct_name[max_ranking]

# shifting down in colm
x = t+5
try :
    idf.loc[x,"Rank of 1"] = "Octant ID"
    idf.loc[x+1,"Rank of 1"] = 1
    idf.loc[x+2,"Rank of 1"] = -1
    idf.loc[x+3,"Rank of 1"] = 2
    idf.loc[x+4,"Rank of 1"] = -2
    idf.loc[x+5,"Rank of 1"] = 3
    idf.loc[x+6,"Rank of 1"] = -3
    idf.loc[x+7,"Rank of 1"] = 4
    idf.loc[x+8,"Rank of 1"] = -4
    idf.loc[x,"Rank of 1"] = "Octant Name"
    idf.loc[x+1,"Rank of -1"] = "Internal outward interaction"
    idf.loc[x+2,"Rank of -1"] = "Exteranl outward interaction"
    idf.loc[x+3,"Rank of -1"] = "External Ejection"
    idf.loc[x+4,"Rank of -1"] = "Internal Ejection"
    idf.loc[x+5,"Rank of -1"] = "External inward interaction"
    idf.loc[x+6,"Rank of -1"] = "Internal inward interaction"
    idf.loc[x+7,"Rank of -1"] = "Internal sweep"
    idf.loc[x+8,"Rank of -1"] = "External sweep"
    idf.loc[x,"Rank of 2"] = "Count of Rank 1 Mod Values"
except:
    print("Column not found")
for i in count_rnk.keys():
    x=x+1
    idf.loc[x,"Rank of 2"] =count_rnk[i]

# insering data in file       
idf.to_excel('tut05\octant_output_ranking_excel.xlsx')
