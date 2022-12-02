import streamlit as st
import pandas as pd
import io
import os
import pandas as pd
from io import BytesIO
from asyncio.windows_events import NULL
from itertools import count
from logging import NullHandler
from queue import Empty
from tkinter import W
import math
import datetime
from pathlib import Path
import glob
from openpyxl.styles import Border,Side
import openpyxl
from openpyxl import Workbook
import xlsxwriter
from openpyxl.styles import PatternFill

pd.options.mode.chained_assignment = None  # default='warn'




def octant_analysis(mod=5000):
    
    try:
        if data_file is not None:
            Dataframe = pd.read_excel(data_file,nrows=300)
            # st.write("INPUT FILE Content :")
            st.dataframe(Dataframe)
        # Dataframe = pd.read_excel('inpt.xlsx')
    except Exception as e:
        print("File not found or Not relevant file type")
        print(e)
    #if no exeption is found then doing further operation    
    else:
        #trying if mean can be calculated or not like if data is number then "try" will execute otherwise it will go in exception
        try:
            # finding mean and printing them in the avg column
            Dataframe.at[0, 'U Avg'] = Dataframe['U'].mean()
            Dataframe.at[0, 'V Avg'] = Dataframe['V'].mean()
            Dataframe.at[0, 'W Avg'] = Dataframe['W'].mean()
        except Exception as e:
            print(e)
        else:
            z = len(Dataframe)
            # z = 200
            # creating a function that will print U-U avg

            def oct(a, b, c, d):
                for i in range(d):
                    Dataframe.at[i, c] = Dataframe.at[i, a] - Dataframe.at[0, b]

            octant_name_id_mapping = {
                "1": "Internal outward interaction",
                "-1": "External outward interaction",
                "2": "External Ejection",
                "-2": "Internal Ejection",
                "3": "External inward interaction",
                "-3": "Internal inward interaction",
                "4": "Internal sweep",
                "-4": "External sweep"
            }

            # calling oct function that will print U-Uavg and same for V and W
            oct("U", "U Avg", "U'=U-U Avg", z)
            oct("V", "V Avg", "V'=V-V Avg", z)
            oct("W", "W Avg", "W'=W-W Avg", z)
            # Getting value of octant based on definition
            for i in range(z):
                if(Dataframe.at[i, "U'=U-U Avg"] >= 0 and Dataframe.at[i, "V'=V-V Avg"] >= 0 and Dataframe.at[i, "W'=W-W Avg"] >= 0):
                    Dataframe.at[i, "Octant"] = 1
                if(Dataframe.at[i, "U'=U-U Avg"] >= 0 and Dataframe.at[i, "V'=V-V Avg"] >= 0 and Dataframe.at[i, "W'=W-W Avg"] < 0):
                    Dataframe.at[i, "Octant"] = -1
                if(Dataframe.at[i, "U'=U-U Avg"] < 0 and Dataframe.at[i, "V'=V-V Avg"] >= 0 and Dataframe.at[i, "W'=W-W Avg"] >= 0):
                    Dataframe.at[i, "Octant"] = 2
                if(Dataframe.at[i, "U'=U-U Avg"] < 0 and Dataframe.at[i, "V'=V-V Avg"] >= 0 and Dataframe.at[i, "W'=W-W Avg"] < 0):
                    Dataframe.at[i, "Octant"] = -2
                if(Dataframe.at[i, "U'=U-U Avg"] < 0 and Dataframe.at[i, "V'=V-V Avg"] < 0 and Dataframe.at[i, "W'=W-W Avg"] >= 0):
                    Dataframe.at[i, "Octant"] = 3
                if(Dataframe.at[i, "U'=U-U Avg"] < 0 and Dataframe.at[i, "V'=V-V Avg"] < 0 and Dataframe.at[i, "W'=W-W Avg"] < 0):
                    Dataframe.at[i, "Octant"] = -3
                if(Dataframe.at[i, "U'=U-U Avg"] >= 0 and Dataframe.at[i, "V'=V-V Avg"] < 0 and Dataframe.at[i, "W'=W-W Avg"] >= 0):
                    Dataframe.at[i, "Octant"] = 4
                if(Dataframe.at[i, "U'=U-U Avg"] >= 0 and Dataframe.at[i, "V'=V-V Avg"] < 0 and Dataframe.at[i, "W'=W-W Avg"] < 0):
                    Dataframe.at[i, "Octant"] = -4
            # creating another column of user input and also printing string at desired place according to output file
            Dataframe.at[0,'                             '] = "     "
            Dataframe.at[0, 'octant ID'] = 'overall count'

            def rankCounter(k, list_rank):
                list_Base = [1, -1, 2, -2, 3, -3, 4, -4]
                Rank_list = [1, 2, 3, 4, 5, 6, 7, 8]
                list_rank_1 = list_rank[:]
                for i in range(8):
                    a = list_Base[list_rank_1.index(max(list_rank))]
            #         print(a)
                    Dataframe.at[k, f" {a}"] = Rank_list[0]

                    list_rank.remove(max(list_rank))
                    Rank_list.pop(0)
                Dataframe.at[k, "Rank1 Octant ID"] = list_Base[list_rank_1.index(max(list_rank_1))]
                Dataframe.at[k, "Rank1 Octant Name"] = octant_name_id_mapping[f"{list_Base[list_rank_1.index(max(list_rank_1))]}"]

            oct_1 = 0
            oct_n1 = 0
            oct_2 = 0
            oct_n2 = 0
            oct_3 = 0
            oct_n3 = 0
            oct_4 = 0
            oct_n4 = 0
            # counting octant count in entire data point
            for i in range(z):
                if Dataframe.at[i, 'Octant'] == 1:
                    oct_1 = (oct_1)+1
                elif Dataframe.at[i, 'Octant'] == -1:
                    oct_n1 = (oct_n1)+1
                elif Dataframe.at[i, 'Octant'] == 2:
                    oct_2 = (oct_2)+1
                elif Dataframe.at[i, 'Octant'] == -2:
                    oct_n2 = (oct_n2)+1
                elif Dataframe.at[i, 'Octant'] == 3:
                    oct_3 = (oct_3)+1
                elif Dataframe.at[i, 'Octant'] == -3:
                    oct_n3 = (oct_n3)+1
                elif Dataframe.at[i, 'Octant'] == 4:
                    oct_4 = (oct_4)+1
                elif Dataframe.at[i, 'Octant'] == -4:
                    oct_n4 = (oct_n4)+1

            list_overall = [oct_1, oct_n1, oct_2, oct_n2, oct_3, oct_n3, oct_4, oct_n4]
            # rankCounter(0,list_overall)
            # printing overall count value at desired places
            Dataframe.at[0, '1'] = oct_1
            Dataframe.at[0, '-1'] = oct_n1
            Dataframe.at[0, '2'] = oct_2
            Dataframe.at[0, '-2'] = oct_n2
            Dataframe.at[0, '3'] = oct_3
            Dataframe.at[0, '-3'] = oct_n3
            Dataframe.at[0, '4'] = oct_4
            Dataframe.at[0, '-4'] = oct_n4
            # priniting mod ranges according to mod value
            min_value = 0
            # getting number of row that will have exact interval as nod value
            freq = z//mod
            for i in range(freq):
                if i == 0:
                    Dataframe.at[i+2, 'octant ID'] = f".0000-{mod*i+mod-1}"
                else:
                    Dataframe.at[i+2, 'octant ID'] = f"{mod*i}-{mod*i+mod-1}"
            Dataframe.at[freq + 2, 'octant ID'] = f"{mod*freq}-{z-1}"
            # counting number of octant in each mod ranges(excludong last row0]]]

            list_mod = []

            for k in range(freq):
                oct_1 = 0
                oct_n1 = 0
                oct_2 = 0
                oct_n2 = 0
                oct_3 = 0
                oct_n3 = 0
                oct_4 = 0
                oct_n4 = 0

                for i in range(mod*k, mod*k+mod):
                    if Dataframe.at[i, 'Octant'] == 1:
                        oct_1 = (oct_1)+1
                    elif Dataframe.at[i, 'Octant'] == -1:
                        oct_n1 = (oct_n1)+1
                    elif Dataframe.at[i, 'Octant'] == 2:
                        oct_2 = (oct_2)+1
                    elif Dataframe.at[i, 'Octant'] == -2:
                        oct_n2 = (oct_n2)+1
                    elif Dataframe.at[i, 'Octant'] == 3:
                        oct_3 = (oct_3)+1
                    elif Dataframe.at[i, 'Octant'] == -3:
                        oct_n3 = (oct_n3)+1
                    elif Dataframe.at[i, 'Octant'] == 4:
                        oct_4 = (oct_4)+1
                    elif Dataframe.at[i, 'Octant'] == -4:
                        oct_n4 = (oct_n4)+1

                temp = [oct_1, oct_n1, oct_2, oct_n2, oct_3, oct_n3, oct_4, oct_n4]
                list_mod.append(temp)
            #     print(list_mod)

                # printing count values
                Dataframe.at[k+2, '1'] = oct_1
                Dataframe.at[k+2, '-1'] = oct_n1
                Dataframe.at[k+2, '2'] = oct_2
                Dataframe.at[k+2, '-2'] = oct_n2
                Dataframe.at[k+2, '3'] = oct_3
                Dataframe.at[k+2, '-3'] = oct_n3
                Dataframe.at[k+2, '4'] = oct_4
                Dataframe.at[k+2, '-4'] = oct_n4
            # counting octant values for last row
            oct_1 = 0
            oct_n1 = 0
            oct_2 = 0
            oct_n2 = 0
            oct_3 = 0
            oct_n3 = 0
            oct_4 = 0
            oct_n4 = 0
            for i in range(mod*freq, z):
                if Dataframe.at[i, 'Octant'] == 1:
                    oct_1 = (oct_1)+1
                elif Dataframe.at[i, 'Octant'] == -1:
                    oct_n1 = (oct_n1)+1
                elif Dataframe.at[i, 'Octant'] == 2:
                    oct_2 = (oct_2)+1
                elif Dataframe.at[i, 'Octant'] == -2:
                    oct_n2 = (oct_n2)+1
                elif Dataframe.at[i, 'Octant'] == 3:
                    oct_3 = (oct_3)+1
                elif Dataframe.at[i, 'Octant'] == -3:
                    oct_n3 = (oct_n3)+1
                elif Dataframe.at[i, 'Octant'] == 4:
                    oct_4 = (oct_4)+1
                elif Dataframe.at[i, 'Octant'] == -4:
                    oct_n4 = (oct_n4)+1

            temp1 = [oct_1, oct_n1, oct_2, oct_n2, oct_3, oct_n3, oct_4, oct_n4]
            list_mod.append(temp1)
            # print(list_mod)
            # printing octant values for last row
            Dataframe.at[freq + 2, '1'] = oct_1
            Dataframe.at[freq + 2, '-1'] = oct_n1
            Dataframe.at[freq + 2, '2'] = oct_2
            Dataframe.at[freq + 2, '-2'] = oct_n2
            Dataframe.at[freq + 2, '3'] = oct_3
            Dataframe.at[freq + 2, '-3'] = oct_n3
            Dataframe.at[freq + 2, '4'] = oct_4
            Dataframe.at[freq + 2, '-4'] = oct_n4

            Dataframe.at[0, ' 1'] = "Rank 1"
            Dataframe.at[0, ' -1'] = "Rank 2"
            Dataframe.at[0, ' 2'] = "Rank 3"
            Dataframe.at[0, ' -2'] = "Rank 4"
            Dataframe.at[0, ' 3'] = "Rank 5"
            Dataframe.at[0, ' -3'] = "Rank 6"
            Dataframe.at[0, ' 4'] = "Rank 7"
            Dataframe.at[0, ' -4'] = "Rank 8"
            Dataframe.at[0, "Rank1 Octant ID"] = 0
            Dataframe.at[0, "Rank1 Octant Name"] = 0

            # print(list_overall)

            rankCounter(0, list_overall)
            for i in range(freq+1):
                rankCounter(i+2, list_mod[i])

            Dataframe.at[freq+6, '1'] = "Octant ID"
            Dataframe.at[freq+6, '-1'] = "Octant Name"
            Dataframe.at[freq+6, '2'] = "Count of Rank 1 Mod Values"
            list_Base1 = [1, -1, 2, -2, 3, -3, 4, -4]
            list_count = []
            for i in range(6):
                list_count.append(Dataframe.at[i+2, "Rank1 Octant Name"])

            # print(list_count)

            for i in range(8):
                Dataframe.at[freq+7+i,'1'] = list_Base1[i]
                Dataframe.at[freq+7+i,'-1'] = octant_name_id_mapping[f"{list_Base1[i]}"]
                Dataframe.at[freq+7+i,'2'] = list_count.count(Dataframe.at[freq+7+i, '-1'])

            Dataframe.rename(columns = {' 1':'Rank of 1', ' -1':"Rank of -1",' 2':"Rank of 2",' -2':"Rank of -2",' 3':"Rank of 3",' -3':"Rank of -3",
            ' 4':"Rank of 4",' -4':"Rank of -4"}, inplace = True)
            Dataframe.at[1,'                               '] = '                                 '
            Dataframe.at[1, '                                 '] = '        '
            Dataframe.at[0, 'Octant #'] = 'overall count'
            Dataframe.at[1, 'Octant #'] = f"Mod:{mod}"
            oct_1 = 0
            oct_n1 = 0
            oct_2 = 0
            oct_n2 = 0
            oct_3 = 0
            oct_n3 = 0
            oct_4 = 0
            oct_n4 = 0
            # counting octant count in entire data point
            for i in range(z):
                if Dataframe.at[i, 'Octant'] == 1:
                    oct_1 = (oct_1)+1
                elif Dataframe.at[i, 'Octant'] == -1:
                    oct_n1 = (oct_n1)+1
                elif Dataframe.at[i, 'Octant'] == 2:
                    oct_2 = (oct_2)+1
                elif Dataframe.at[i, 'Octant'] == -2:
                    oct_n2 = (oct_n2)+1
                elif Dataframe.at[i, 'Octant'] == 3:
                    oct_3 = (oct_3)+1
                elif Dataframe.at[i, 'Octant'] == -3:
                    oct_n3 = (oct_n3)+1
                elif Dataframe.at[i, 'Octant'] == 4:
                    oct_4 = (oct_4)+1
                elif Dataframe.at[i, 'Octant'] == -4:
                    oct_n4 = (oct_n4)+1
            # pinting overall count value at desired places
            Dataframe.at[0, 'Trans +1'] = oct_1
            Dataframe.at[0, 'Trans -1'] = oct_n1
            Dataframe.at[0, 'Trans +2'] = oct_2
            Dataframe.at[0, 'Trans -2'] = oct_n2
            Dataframe.at[0, 'Trans +3'] = oct_3
            Dataframe.at[0, 'Trans -3'] = oct_n3
            Dataframe.at[0, 'Trans +4'] = oct_4
            Dataframe.at[0, 'Trans -4'] = oct_n4
            # piniting mod ranges according to mod value
            min_value = 0
            # getting number of row that will have exact interval as mod value
            freq = z//mod  
            for i in range(freq):
                if i == 0:
                    Dataframe.at[i+2, 'Octant #'] = f".0000-{mod*i+mod-1}"
                else:
                    Dataframe.at[i+2, 'Octant #'] = f"{mod*i}-{mod*i+mod-1}"
            Dataframe.at[freq + 2, 'Octant #'] = f"{mod*freq}-{z-1}"
            # counting number of octant in each mod ranges(excludong last row)
            for k in range(freq):
                oct_1 = 0
                oct_n1 = 0
                oct_2 = 0
                oct_n2 = 0
                oct_3 = 0
                oct_n3 = 0
                oct_4 = 0
                oct_n4 = 0
                for i in range(mod*k, mod*k+mod):
                    if Dataframe.at[i, 'Octant'] == 1:
                        oct_1 = (oct_1)+1
                    elif Dataframe.at[i, 'Octant'] == -1:
                        oct_n1 = (oct_n1)+1
                    elif Dataframe.at[i, 'Octant'] == 2:
                        oct_2 = (oct_2)+1
                    elif Dataframe.at[i, 'Octant'] == -2:
                        oct_n2 = (oct_n2)+1
                    elif Dataframe.at[i, 'Octant'] == 3:
                        oct_3 = (oct_3)+1
                    elif Dataframe.at[i, 'Octant'] == -3:
                        oct_n3 = (oct_n3)+1
                    elif Dataframe.at[i, 'Octant'] == 4:
                        oct_4 = (oct_4)+1
                    elif Dataframe.at[i, 'Octant'] == -4:
                        oct_n4 = (oct_n4)+1
                # printing count values
                Dataframe.at[k+2, 'Trans +1'] = oct_1
                Dataframe.at[k+2, 'Trans -1'] = oct_n1
                Dataframe.at[k+2, 'Trans +2'] = oct_2
                Dataframe.at[k+2, 'Trans -2'] = oct_n2
                Dataframe.at[k+2, 'Trans +3'] = oct_3
                Dataframe.at[k+2, 'Trans -3'] = oct_n3
                Dataframe.at[k+2, 'Trans +4'] = oct_4
                Dataframe.at[k+2, 'Trans -4'] = oct_n4
            # counting octant values for last row   
            oct_1 = 0
            oct_n1 = 0
            oct_2 = 0
            oct_n2 = 0
            oct_3 = 0
            oct_n3 = 0
            oct_4 = 0
            oct_n4 = 0
            for i in range(mod*freq, z):
                if Dataframe.at[i, 'Octant'] == 1:
                    oct_1 = (oct_1)+1
                elif Dataframe.at[i, 'Octant'] == -1:
                    oct_n1 = (oct_n1)+1
                elif Dataframe.at[i, 'Octant'] == 2:
                    oct_2 = (oct_2)+1
                elif Dataframe.at[i, 'Octant'] == -2:
                    oct_n2 = (oct_n2)+1
                elif Dataframe.at[i, 'Octant'] == 3:
                    oct_3 = (oct_3)+1
                elif Dataframe.at[i, 'Octant'] == -3:
                    oct_n3 = (oct_n3)+1
                elif Dataframe.at[i, 'Octant'] == 4:
                    oct_4 = (oct_4)+1
                elif Dataframe.at[i, 'Octant'] == -4:
                    oct_n4 = (oct_n4)+1
            # printing octant values for last row
            Dataframe.at[freq + 2, 'Trans +1'] = oct_1
            Dataframe.at[freq + 2, 'Trans -1'] = oct_n1
            Dataframe.at[freq + 2, 'Trans +2'] = oct_2
            Dataframe.at[freq + 2, 'Trans -2'] = oct_n2
            Dataframe.at[freq + 2, 'Trans +3'] = oct_3
            Dataframe.at[freq + 2, 'Trans -3'] = oct_n3
            Dataframe.at[freq + 2, 'Trans +4'] = oct_4
            Dataframe.at[freq + 2, 'Trans -4'] = oct_n4
            Dataframe.at[freq + 3,'Octant #'] = 'Verified'
            Dataframe.at[freq + 3,'Trans +1'] = Dataframe.at[0,'Trans +1']
            Dataframe.at[freq + 3,'Trans -1'] = Dataframe.at[0,'Trans -1']
            Dataframe.at[freq + 3,'Trans +2'] = Dataframe.at[0,'Trans +2']
            Dataframe.at[freq + 3,'Trans -2'] = Dataframe.at[0,'Trans -2']
            Dataframe.at[freq + 3,'Trans +3'] = Dataframe.at[0,'Trans +3']
            Dataframe.at[freq + 3,'Trans -3'] = Dataframe.at[0,'Trans -3']
            Dataframe.at[freq + 3,'Trans +4'] = Dataframe.at[0,'Trans +4']
            Dataframe.at[freq + 3,'Trans -4'] = Dataframe.at[0,'Trans -4']

            Dataframe.at[freq + 6,'Octant #'] = 'Overall Transition Count'
            Dataframe.at[freq + 7,'Trans +1'] = 'To'
            Dataframe.at[freq + 9,'                                 '] = 'from'
            Dataframe.at[freq + 8,'Octant #'] = 'Count'
            Dataframe.at[freq + 9,'Octant #'] = '+1'
            Dataframe.at[freq + 10,'Octant #'] = '-1'
            Dataframe.at[freq + 11,'Octant #'] = '+2'
            Dataframe.at[freq + 12,'Octant #'] = '-2'
            Dataframe.at[freq + 13,'Octant #'] = '+3'
            Dataframe.at[freq + 14,'Octant #'] = '-3'
            Dataframe.at[freq + 15,'Octant #'] = '+4'
            Dataframe.at[freq + 16,'Octant #'] = '-4'

            Dataframe.at[freq + 8,'Trans +1'] = '+1'
            Dataframe.at[freq + 8,'Trans -1'] = '-1'
            Dataframe.at[freq + 8,'Trans +2'] = '+2'
            Dataframe.at[freq + 8,'Trans -2'] = '-2'
            Dataframe.at[freq + 8,'Trans +3'] = '+3'
            Dataframe.at[freq + 8,'Trans -3'] = '-3'
            Dataframe.at[freq + 8,'Trans +4'] = '+4'
            Dataframe.at[freq + 8,'Trans -4'] = '-4'
        # putting strings in the desired shell of excel sheet according to output file 
            newfreq = z//mod
            for r in range(newfreq):
                if r == 0:
                    Dataframe.at[freq + 19,'Octant #'] = 'Mod Transition Count'
                    Dataframe.at[freq + 20,'Trans +1'] = 'To'
                    Dataframe.at[freq + 21,'Octant #'] = 'Count'
                    Dataframe.at[freq + 22,'                                 '] = 'from'
                    Dataframe.at[freq + 20,'Octant #'] = f".0000-{mod*r+mod-r}"

                    Dataframe.at[freq + 22,'Octant #'] = '+1'
                    Dataframe.at[freq + 23,'Octant #'] = '-1'
                    Dataframe.at[freq + 24,'Octant #'] = '+2'
                    Dataframe.at[freq + 25,'Octant #'] = '-2'
                    Dataframe.at[freq + 26,'Octant #'] = '+3'
                    Dataframe.at[freq + 27,'Octant #'] = '-3'
                    Dataframe.at[freq + 28,'Octant #'] = '+4'
                    Dataframe.at[freq + 29,'Octant #'] = '-4'

                    Dataframe.at[freq + 21,'Trans +1'] = '+1'
                    Dataframe.at[freq + 21,'Trans -1'] = '-1'
                    Dataframe.at[freq + 21,'Trans +2'] = '+2'
                    Dataframe.at[freq + 21,'Trans -2'] = '-2'
                    Dataframe.at[freq + 21,'Trans +3'] = '+3'
                    Dataframe.at[freq + 21,'Trans -3'] = '-3'
                    Dataframe.at[freq + 21,'Trans +4'] = '+4'
                    Dataframe.at[freq + 21,'Trans -4'] = '-4'
                else:
                    Dataframe.at[freq + 19 + 13*r,'Octant #'] = 'Mod Transition Count'
                    Dataframe.at[freq + 20 + 13*r,'Trans +1'] = 'To'
                    Dataframe.at[freq + 21 + 13*r,'Octant #'] = 'Count'
                    Dataframe.at[freq + 22 + 13*r,'                                 '] = 'from'
                    Dataframe.at[freq + 20 + 13*r,'Octant #'] = f"{mod*r}-{mod*r+mod-1}"
                    Dataframe.at[freq + 22 + 13*r,'Octant #'] = '+1'
                    Dataframe.at[freq + 23 + 13*r,'Octant #'] = '-1'
                    Dataframe.at[freq + 24 + 13*r,'Octant #'] = '+2'
                    Dataframe.at[freq + 25 + 13*r,'Octant #'] = '-2'
                    Dataframe.at[freq + 26 + 13*r,'Octant #'] = '+3'
                    Dataframe.at[freq + 27 + 13*r,'Octant #'] = '-3'
                    Dataframe.at[freq + 28 + 13*r,'Octant #'] = '+4'
                    Dataframe.at[freq + 29 + 13*r,'Octant #'] = '-4'

                    Dataframe.at[freq + 21 + 13*r,'Trans +1'] = '+1'
                    Dataframe.at[freq + 21 + 13*r,'Trans -1'] = '-1'
                    Dataframe.at[freq + 21 + 13*r,'Trans +2'] = '+2'
                    Dataframe.at[freq + 21 + 13*r,'Trans -2'] = '-2'
                    Dataframe.at[freq + 21 + 13*r,'Trans +3'] = '+3'
                    Dataframe.at[freq + 21 + 13*r,'Trans -3'] = '-3'
                    Dataframe.at[freq + 21 + 13*r,'Trans +4'] = '+4'
                    Dataframe.at[freq + 21 + 13*r,'Trans -4'] = '-4'

            Dataframe.at[freq + 19 + 13*newfreq,'Octant #'] = 'Mod Transition Count'
            Dataframe.at[freq + 20 + 13*newfreq,'Trans +1'] = 'To'
            Dataframe.at[freq + 21 + 13*newfreq,'Octant #'] = 'Count'
            Dataframe.at[freq + 22 + 13*newfreq,'                                 '] = 'from'
            Dataframe.at[freq + 20 + 13*newfreq,'Octant #'] = f"{mod*newfreq}-{z-1}"
            Dataframe.at[freq + 22 + 13*newfreq,'Octant #'] = '+1'
            Dataframe.at[freq + 23 + 13*newfreq,'Octant #'] = '-1'
            Dataframe.at[freq + 24 + 13*newfreq,'Octant #'] = '+2'
            Dataframe.at[freq + 25 + 13*newfreq,'Octant #'] = '-2'
            Dataframe.at[freq + 26 + 13*newfreq,'Octant #'] = '+3'
            Dataframe.at[freq + 27 + 13*newfreq,'Octant #'] = '-3'
            Dataframe.at[freq + 28 + 13*newfreq,'Octant #'] = '+4'
            Dataframe.at[freq + 29 + 13*newfreq,'Octant #'] = '-4'
            Dataframe.at[freq + 21 + 13*newfreq,'Trans +1'] = '+1'
            Dataframe.at[freq + 21 + 13*newfreq,'Trans -1'] = '-1'
            Dataframe.at[freq + 21 + 13*newfreq,'Trans +2'] = '+2'
            Dataframe.at[freq + 21 + 13*newfreq,'Trans -2'] = '-2'
            Dataframe.at[freq + 21 + 13*newfreq,'Trans +3'] = '+3'
            Dataframe.at[freq + 21 + 13*newfreq,'Trans -3'] = '-3'
            Dataframe.at[freq + 21 + 13*newfreq,'Trans +4'] = '+4'
            Dataframe.at[freq + 21 + 13*newfreq,'Trans -4'] = '-4'
        # Defining a funtion that will make initial values o in the transition count 
        # here r in matrix number i.e for r = 0 it will go to first matrix in which overall counts has to be placed
        # 13 is the diff between rows of two consecutive matrix so by multipliplying with r we can go to desired rows number
        # column no is same for all the matrix
            def make_zero(r):
                for n in range(8):
                    Dataframe.at[freq + 9 +13*r+n , 'Trans +1'] = 0 
                    Dataframe.at[freq + 9 +13*r+n , 'Trans -1'] = 0
                    Dataframe.at[freq + 9 +13*r+n , 'Trans +2'] = 0
                    Dataframe.at[freq + 9 +13*r+n , 'Trans -2'] = 0
                    Dataframe.at[freq + 9 +13*r+n , 'Trans +3'] = 0
                    Dataframe.at[freq + 9 +13*r+n , 'Trans -3'] = 0
                    Dataframe.at[freq + 9 +13*r+n , 'Trans +4'] = 0
                    Dataframe.at[freq + 9 +13*r+n , 'Trans -4'] = 0
            # calling the function for all matrix except last matrix
            for xt in range(freq+2):       
                make_zero(xt)
        # for last matrix transtition count end will be z-1 
        # Defining a function count_nos that will take r, start , end and count the transition and place it to desired cell
            def count_nos(r,start=0,end = z-1):  
                # creating a list that is containig octant values
                oct_lst=[1,-1,2,-2,3,-3,4,-4]

                for x in range(start,end):
                    fr = Dataframe.at[x,'Octant']
                    to = Dataframe.at[x+1,'Octant']
                    for y in range(len(oct_lst)):
                        if fr == oct_lst[y] and to == 1:
                            Dataframe.iloc[freq + 9+13*r + y , 33+1] += 1
                        elif fr == oct_lst[y] and to == -1:
                            Dataframe.iloc[freq + 9+13*r+ y  , 33+2] += 1
                        elif fr == oct_lst[y] and to == 2:
                            Dataframe.iloc[freq + 9+13*r+ y  , 33+3] += 1
                        elif fr == oct_lst[y]  and to == -2:
                            Dataframe.iloc[freq + 9+13*r+ y  , 33+4] += 1
                        elif fr == oct_lst[y] and to == 3:
                            Dataframe.iloc[freq + 9+13*r+ y  , 33+5] += 1
                        elif fr == oct_lst[y] and to == -3:
                            Dataframe.iloc[freq + 9+13*r+ y  , 33+6] += 1
                        elif fr == oct_lst[y] and to == 4:
                            Dataframe.iloc[freq + 9+13*r+ y  , 33+7] += 1
                        elif fr == oct_lst[y] and to == -4:
                            Dataframe.iloc[freq + 9+13*r+ y  , 33+8] += 1
            # giving r = 0 and default values of start and end will be 0 automatically 
            # This will count overall transition and place to the desired cell 
            count_nos(0)
            # calling function for mod transtion range except last range
            for xy in range(1,freq+1):       
                count_nos(xy,mod*(xy-1),mod*(xy-1) +mod)

            # calling function for last range 
            count_nos(freq+1,mod*freq,z-1)           

            Dataframe.at[0,' '] = ' '
            Dataframe.at[0,'  '] = 'Octant##'
            Dataframe.at[0,'     '] = 'Longest Subsquence Length'
            Dataframe.at[0,'      '] = 'Count'

            # creating a list1 that is containing octant values
            list1 = [1,-1,2,-2,3,-3,4,-4]
            list5 = ["+1","-1","+2","-2","+3","-3","+4","-4"]
            for i in range(8):
                Dataframe.at[i+1,'  '] = str(list5[i])

            # Also creating list2 and list3 these lists are used to store largest subsequence count and no of occurance using append 
            list2 = []
            list3 = []

            time_end = []
            # Creatind a function that will take a item and a list and give all occurances of that item no matter if it is repeating 
            def find_indices(list_to_check, item_to_find):
                return [idx for idx, value in enumerate(list_to_check) if value == item_to_find]
            hehe_list = []
            for n in list1:
                a = 0
                list = []
                time = []
                for i in range(z-1):
                    
                    if Dataframe.at[i,'Octant'] == n and Dataframe.at[i+1,'Octant'] == n:
                        a = a+1
                        # this a will be keep on adding till the same octant value is getting
                    elif Dataframe.at[i,'Octant'] == n and Dataframe.at[i+1,'Octant'] != n:
                        # Just after we get diff octant value nos of occ is stored in list using append
                        list.append(a+1)
                        time.append(i)#this will keep on adding end time i values 
                        # then again a =  0 for next cycle
                        a=0
                    
                largest_count = list[0]
                for counts in list:
                    if counts > largest_count:
                        largest_count = counts
                list2.append(largest_count)
                list3.append(list.count(largest_count))
                # print(list3)
                # print(list3)
                occ_list = find_indices(list, largest_count)
                for k in occ_list:
                    time_end.append(time[k])# this will keep on adding the end time of largest occurance 
                # print(time_end)
                

            for n in range(8):    
                Dataframe.at[n+1,'     '] = list2[n]
                Dataframe.at[n+1,'      '] = list3[n]
            #putting values in excel sheet as per output file 
            Dataframe.at[0,'        '] = ' '
            Dataframe.at[0,'           '] = 'Octant###'
            Dataframe.at[0,'              '] = 'Longest Subsquence Length'
            Dataframe.at[0,'                  '] = 'Count'
            # print(16+sum(list3))
            elemh=0
            elemp=1
            elemt=0
            elemg=0
            print(list2)
            for elem in range(8):
                Dataframe.at[elemp,'           '] = list1[elemh]
                Dataframe.at[elemp,'                  '] = list3[elemt]
                Dataframe.at[elemp,'              '] = list2[elemt]
                Dataframe.at[elemp+1,'           '] = 'Time'
                Dataframe.at[elemp+1,'              '] = 'From'
                Dataframe.at[elemp+1,'                  '] = 'To'
                for noss in range(int(list3[elemt])):
                    Dataframe.at[elemp+2+noss,'              '] = Dataframe.at[time_end[elemg+noss]-(list2[elemg]-1),'T'] 
                    Dataframe.at[elemp+2+noss,'                  '] = Dataframe.at[time_end[elemg+noss],'T']
                elemg+=1

                elemp=elemp+2+int(list3[elemt])
                elemh+=1
                elemt+=1
            Dataframe = Dataframe.fillna(' ')
            # Dataframe=Dataframe.style.highlight_max()
            # Dataframe.head(20)
            


            def to_excel(idf):
                output = BytesIO()
                writer = pd.ExcelWriter(output, engine='xlsxwriter')
                idf.to_excel(writer, index=False, sheet_name='Sheet1')
                workbook = writer.book
                worksheet = writer.sheets['Sheet1']
                format1 = workbook.add_format({'num_format': '0.00'}) 
                worksheet.set_column('A:A', None, format1)
                # full_border = workbook.add_format(
                #     {
                #         "border" : 1,
                #         "border_color": "#000000"
                #     }
                # )
                # for rows in ws.iter_rows(min_row=0, max_row=110, min_col=14,max_col=80):
                #     for cell in rows:
                #         if cell.value!=' ':
                #             full_border


                
                
                worksheet.set_column(
                    7,
                    9,
                    17
                )  
                worksheet.set_column(
                    "O:O",
                    30
                )  
                worksheet.set_column(
                    "AS:AS",
                    28
                )  
                worksheet.set_column(
                    "AW:AW",
                    28
                )  
                worksheet.set_column(
                    "P:P",
                    24
                )
                worksheet.set_column(
                    "AD:AD",
                    18
                )
                worksheet.set_column(
                    "AE:AE",
                    28
                )
                worksheet.set_column(
                    "AH:AH",
                    16
                )
                
                writer.save()
                processed_data = output.getvalue()
                return processed_data
                
            df_data = to_excel(Dataframe)
           
            outputfile_Name = f'{file_name1}mod({mod}){datetime.datetime.now()}.xlsx'
            # elif opt == 2:


            st.download_button(label='Download Result',data=df_data,file_name=outputfile_Name)	
        

st.set_page_config(page_title="Project 2",page_icon=":tada:" ,layout="wide")
st.title("PROJECT # 2")
option = st.selectbox('Choose a option:',('1.Single file Conversion','2.Bulk conversion'))
get_mod = st.number_input("Enter MOD Value:",step=1)
mod = int(get_mod)
# opt = 0
# opt = 0
if option=='1.Single file Conversion':
    att = 0
    # opt = 1
    st.write("Please upload your file down below :point_down:")
    data_file = st.file_uploader('INPUT FILE',type=['xlsx'])
    
    with st.form("submitbuton"):
        submitted = st.form_submit_button("Submit")
        if submitted:
            att=1            
    if att == 1:
        filenmae= data_file.name
        file_name1 = filenmae.split("xlsx")[0]
        octant_analysis(mod) 

elif option=='2.Bulk conversion':
    atn = 0
    # opt = 2
    path=st.text_input("Copy and paste folder path:")
    with st.form("submitbuton"):
        submitted = st.form_submit_button("Submit")
        if submitted:
            atn = 1
    if atn == 1:

        files = glob.glob(path + '/*xlsx')
        
        
        for file in files:
            file_name2 = os.path.basename(file)
            file_name1 = file_name2.split("xlsx")[0]

            data_file = f"{file}"
            octant_analysis(mod)