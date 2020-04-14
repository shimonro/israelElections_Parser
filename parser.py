import pandas as pd
import numpy as np
from itertools import groupby 
from collections import OrderedDict
import json    

path = '/home/shimon/workspace/Projects/IsraelElection/israelElections_Parser/'
inputCSV = 'israelElections.csv'
outputJson = 'israelElections2020.json'

#there is a matching problem between pandas and json so we need to cutumize teh encoder for generic casting 
class NpEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        elif isinstance(obj, np.floating):
            return float(obj)
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        else:
            return super(NpEncoder, self).default(obj)

# read the raw data file
df = pd.read_csv(path + inputCSV, dtype={
            "Parlament" : int,
            "Government" : int,
            "Year" : int,
            "PMHeb" : str,
            "PMEng" : str,
            "PMID" : int,
            "PartyHeb" : str,
            "PartyEng" : str,
            "PartyID" : int,
            "Mandates" : int,
            "BlockHeb" : str,
            "BlockEng" : str,
            "BlockID" : int
        })

# init the results list
parsed = []

# parse the pandas
for (Parlament, Government, year), rest in df.groupby(["Parlament", "Government", "Year"]):
    for (PMHeb, PMEng, PMID), reminader in rest.groupby(["PMHeb", "PMEng", "PMID"]):
        PM = {}
        PM['PMHeb'] = PMHeb
        PM['PMEng'] = PMEng
        PM['PMID'] = PMID
        reduced_df = rest.drop(["Parlament", "Government", "Year", "PMHeb", "PMEng", "PMID"], axis=1)
        results = [OrderedDict(row) for i,row in reduced_df.iterrows()]
        parsed.append(OrderedDict([("Parlament", Parlament),
                                    ("Government", Government),
                                    ("Year", year),
                                    ("PM", PM),
                                    ("Results", results)]))

print (json.dumps(parsed[0], indent=4, cls=NpEncoder))

with open(path + outputJson, 'w') as outfile:
    outfile.write(json.dumps(parsed, indent=4, cls=NpEncoder))