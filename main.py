from pathlib import Path
import pandas as pd
import os
from collections import Counter

"""
1. retrieve data from each file
2. calculate total count / median count / count rate (how many epc values were > 0)
3. use these three columns to determine if we fail (fail if one area or 2+ areas fail)
"""


parentPath = Path(r'C:\Users\Ranfe\Music\sensorCheck\Reader test') # update path

antLists = {n: [] for n in range(1, 5)}
finalStats = {n: [] for n in range(1, 5)}

"""
Reads parent directory, and each subdirectory for all csv files.
Calculates mean, median, and rate (items > count 0) for Count
"""
def readFile():
    for subdir in parentPath.iterdir():
        if not subdir.is_dir():
            print(f"Skipped {subdir}")
            continue
        
        for x in range(1, 5):
            file_path = subdir / f"Reader{str(subdir)[46:]}_ANT{x}.csv"  
            if not file_path.exists():
                print(f"File: Reader{str(subdir)[46:]}_ANT{x} is not present")
                continue

            df = pd.read_csv(file_path, header=35) # Make sure this aligns with the column titles   
            df.columns = df.columns.str.strip()
            
            stats = pd.Series({
                'total': df['Count'].sum(),
                'median': df['Count'].median(),
                'rate': (df['Count'] > 0).mean()
            })

            antLists[x].append(stats)

    return antLists

# calculate mean, median, and rate across all four antennas
allStats = readFile()

finalStats = {}

for x, statsList in allStats.items():
    n = len(statsList)
    if n == 0:
        continue
        
    total = sum(s['total'] for s in statsList) / n
    median = sum(s['median'] for s in statsList) / n
    rate = sum(s['rate'] for s in statsList) / n

    finalStats[x] = pd.Series({
        'total': total,
        'median': median,
        'rate': rate
    })

for x in finalStats.items():
    print(x)
    
"""
Check if any antennas are +- 10% from average total/median/rate
"""

