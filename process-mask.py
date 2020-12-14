import numpy as np
import pandas as pd
import calendar
import datetime

#months = {month: index for index, month in enumerate(calendar.month_abbr) if month}
#print(list(calendar.month_name).index('July'))
mandates = pd.read_csv("mask-mandate-old.tsv",sep="\t")

for i in range(len(mandates)):
    state = mandates.at[i,"State"]
    date = mandates.at[i,"Date"]
    degree = mandates.at[i,"Degree"]
    month,day = date.split()
    month = list(calendar.month_name).index(month)
    if len(str(month)) < 2:
        month = "0" + str(month)
    if degree > 1:
        print(f"20-{month}-{day}\t{state}")
