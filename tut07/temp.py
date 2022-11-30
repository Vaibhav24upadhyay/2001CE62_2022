mod=5000
from asyncio.windows_events import NULL
from itertools import count
from logging import NullHandler
from queue import Empty
from tkinter import W
import pandas as pd
import math
pd.options.mode.chained_assignment = None  # default='warn'
idf = pd.read_excel(r'tut07\input\1.0.xlsx')
m =idf['U'].size-1
print(idf.loc[m,"U"])