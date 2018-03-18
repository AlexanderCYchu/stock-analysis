import pandas as pd
import os
import quandl
import time

# put your api key in the auth.txt, to run the script
auth_tok = open('auth.txt','r').read().splitlines()

auth_tok = str(auth_tok[0])

quandl.ApiConfig.api_key = auth_tok

data = quandl.get("WIKI/KO", start_date = "2000-12-12", end_date = "2014-12-30")

print(data['Adj. Close'])
