
# coding: utf-8

# In[20]:


import pandas as pd
import os
import time
from datetime import datetime

from time import mktime

# get_ipython().magic('matplotlib notebook')
import matplotlib
# import matplotlib.pylab as plt
import matplotlib.pyplot as plt
from matplotlib import style
style.use('dark_background')

import re
import urllib

# In[21]:


def Key_Stats(gather="Total Debt/Equity (mrq)"):
    statspath = os.getcwd()+'/intraQuarter/_KeyStats'
    stock_list = [x[0] for x in os.walk(statspath)]
    #print (stock_list)

    stock_list_2 = []
    for root, dirs, files in os.walk(statspath):
        dirs.sort()
        for dirname in dirs:
            temp = os.path.join(root, dirname)
            #print(os.path.join(root, dirname),'\n')
            stock_list_2.append(temp)
    # print(stock_list_2)

    df = pd.DataFrame(columns = ['Date',
                                 'Unix',
                                 'Ticker',
                                 'DE Ratio',
                                 'Price',
                                 'stock_p_change',
                                 'SP500',
                                 'sp500_p_change',
                                 'Difference',
                                 'Status'])

    sp500_df = pd.DataFrame.from_csv('YAHOO_INDEX_GSPC.csv')

    ticker_list = []

    for each_dir in stock_list_2[1:]:
        each_file = sorted(os.listdir(each_dir))
        ticker = each_dir.split('/_KeyStats/')[1]
        ticker_list.append(ticker)

        starting_stock_value = False
        starting_sp500_value = False

        if len(each_file) > 0:
            for file in each_file:
                date_stamp = datetime.strptime(file, '%Y%m%d%H%M%S.html')
                unix_time = time.mktime(date_stamp.timetuple())

                full_file_path = each_dir+'/'+file

                source = open(full_file_path,'r').read()

                try:
                    try:
                        value = float(source.split(gather+':</td><td class="yfnc_tabledata1">')[1].split('</td>')[0])
                    except Exception as e:
                        try:
                            value = (source.split(gather+':</td>\n<td class="yfnc_tabledata1">')[1].split('</td>')[0])
                            # print(value)
                            # value = float(value)
                        except Exception as e:
                            pass
                            # print(str(e),ticker,file)

                    try:
                        sp500_date = datetime.fromtimestamp(unix_time).strftime('%Y-%m-%d')
                        row = sp500_df[(sp500_df.index == sp500_date)]
                        sp500_value = float(row["Adj Close"])
                    except:
                        sp500_date = datetime.fromtimestamp(unix_time-259200).strftime('%Y-%m-%d')
                        # 259200 = 3days in second, get out of weekend
                        row = sp500_df[(sp500_df.index == sp500_date)]
                        sp500_value = float(row["Adj Close"])

                    try:
                        stock_price = float(source.split('</small><big><b>')[1].split('</b></big>')[0])
                    except Exception as e:
                        # <span id="yfs_l10_afl">43.27</span>
                        # print('str(e) = ',str(e),'ticker = ',ticker,'file = ',file)
                        try:

                            stock_price = (source.split('</small><big><b>')[1].split('</b></big>')[0])
                            stock_price = re.search(r'(\d{1,8}\.\d{1,8})', stock_price)
                            # print('stock_price before group(1)', stock_price)
                            stock_price = float(stock_price.group(1))
                            # print('stock_price AFTER group(1)', stock_price)

                            # time.sleep(15)
                        except Exception as e:
                            stock_price = (source.split('<span class="time_rtq_ticker">')[1].split('</span>')[0])
                            stock_price = re.search(r'(\d{1,8}\.\d{1,8})', stock_price)
                            stock_price = float(stock_price.group(1))
                            # print('Latest:', stock_price)
                            # print('stock price Exception',str(e),'\nticker = ',ticker,'\nfile = ',file)
                            # time.sleep(15)
                    # print('stock_price:',stock_price,'ticker:',ticker)

                    if not starting_stock_value:
                        starting_stock_value = stock_price
                    if not starting_sp500_value:
                        starting_sp500_value = sp500_value

                    stock_p_change = ((stock_price - starting_stock_value) / starting_stock_value) * 100
                    sp500_p_change = ((sp500_value - starting_sp500_value) / starting_sp500_value) * 100

                    df = df.append({'Date':date_stamp,
                                    'Unix':unix_time,
                                    'Ticker':ticker,
                                    'DE Ratio':value,
                                    'Price':stock_price,
                                    'stock_p_change':stock_p_change,
                                    'SP500':sp500_value,
                                    'sp500_p_change':sp500_p_change,
                                    'Difference':stock_p_change - sp500_p_change}, ignore_index = True)
                except Exception as e:
                    pass

    for each_ticker in ticker_list:
        try:
            plot_df = df[(df['Ticker'] == each_ticker)]
            plot_df = plot_df.set_index(['Date'])

            plot_df['Difference'].plot(label=each_ticker)
            plt.legend()

        except:
            pass

    plt.show()

    save = gather.replace(' ','').replace(')','').replace('(','').replace('/','')+'.csv'
    # print(save)
    df.to_csv(save)
# print('ok')


# In[22]:


Key_Stats()
