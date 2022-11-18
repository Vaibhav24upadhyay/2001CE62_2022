mod=5000
from asyncio.windows_events import NULL
from itertools import count
from logging import NullHandler
from queue import Empty
from tkinter import W
import pandas as pd
import math
pd.options.mode.chained_assignment = None  # default='warn'
idf = pd.read_csv(r'input_registered_students.csv')
at_file = pd.read_csv(r'input_attendance.csv')
at_file[['Date','time']]=at_file["Timestamp"].str.split(' ', expand=True)
date_input = at_file['Date'].tolist()
time_input = at_file['time'].tolist()
def time_in_range(start, end, current):
    """Returns whether current is in the range [start, end]"""
    if(start<= current and current <= end):
        return True
    else:
        return False
class_date = ['28-07-2022','01-08-2022','04-08-2022','08-08-2022','11-08-2022','22-08-2022','25-08-2022','29-08-2022','01-09-2022','05-09-2022','08-09-2022','12-09-2022']
for i in range(idf["Name"].size):
    total_att_count = {'28-07-2022':0,'01-08-2022':0,'04-08-2022':0,'08-08-2022':0,'11-08-2022':0,'22-08-2022':0,'25-08-2022':0,'29-08-2022':0,'01-09-2022':0,'05-09-2022':0,'08-09-2022':0,'12-09-2022':0}
    total_corr_att_count = {'28-07-2022':0,'01-08-2022':0,'04-08-2022':0,'08-08-2022':0,'11-08-2022':0,'22-08-2022':0,'25-08-2022':0,'29-08-2022':0,'01-09-2022':0,'05-09-2022':0,'08-09-2022':0,'12-09-2022':0}
    _RollNo = idf.loc[i,'Roll No']
    _name = idf.loc[i,'Name']
    st = _RollNo + ' ' + _name
    for j in range(at_file['Timestamp'].size):
        if(at_file.loc[j,'Attendance'].lower()==st.lower()):
            for k in range(len(class_date)):
                if(date_input[j]==class_date[k]):
                    total_att_count[date_input[j]]=total_att_count[date_input[j]]+1
                    if time_in_range("14:00:00", "15:00:00", time_input[j+1]):
                        total_corr_att_count[date_input[j]]=total_corr_att_count[date_input[j]]+1
    t = len(total_att_count)
    st_file = pd.DataFrame()
    st_file["Date"]=""
    st_file.loc[0,"Roll"]=_RollNo
    st_file.loc[0,"Name"]=_name
    st_file["Total Attendance Count"]=""
    st_file["Real"]=""
    st_file["Duplicate"]=""
    st_file["Invalid"]=""
    st_file["Absent"]=""
    for n in range(t):
        st_file.loc[n+1,"Real"]=0
        st_file.loc[n+1,"Duplicate"]=0
        st_file.loc[n+1,"Absent"]=0
        st_file.loc[n+1,"Date"]=class_date[n]
        st_file.loc[n+1,"Total Attendance Count"]=total_att_count[class_date[n]]
        if(total_corr_att_count[class_date[n]]!=0):
            st_file.loc[n+1,"Real"]=1
            st_file.loc[n+1,"Absent"]=0
        else:
            st_file.loc[n+1,"Real"]=0
            st_file.loc[n+1,"Absent"]=1
        st_file.loc[n+1,"Invalid"]=total_corr_att_count[date_input[n]]-1
    st_file.to_excel(f'output\{_RollNo}.xlsx')
    # print(st_file)