import numpy as np
import matplotlib.pyplot as plt
from sklearn import svm, preprocessing, metrics
import pandas as pd
from matplotlib import style
style.use('ggplot')

FEATURES =  ['DE Ratio',
             'Trailing P/E',
             'Price/Sales',
             'Price/Book',
             'Profit Margin',
             'Operating Margin',
             'Return on Assets',
             'Return on Equity',
             'Revenue Per Share',
             'Market Cap',
             'Enterprise Value',
             'Forward P/E',
             'PEG Ratio',
             'Enterprise Value/Revenue',
             'Enterprise Value/EBITDA',
             'Revenue',
             'Gross Profit',
             'EBITDA',
             'Net Income Avl to Common ',
             'Diluted EPS',
             'Earnings Growth',
             'Revenue Growth',
             'Total Cash',
             'Total Cash Per Share',
             'Total Debt',
             'Current Ratio',
             'Book Value Per Share',
             'Cash Flow',
             'Beta',
             'Held by Insiders',
             'Held by Institutions',
             'Shares Short (as of',
             'Short Ratio',
             'Short % of Float',
             'Shares Short (prior ']

def Build_Data_Set():
    data_df = pd.DataFrame.from_csv('Key_Stats.csv')

    # data_df = data_df[:100]
    print(data_df)
    data_df = data_df.sort_values(by=['Unix'])
    print(data_df)
    X = data_df[FEATURES].as_matrix()#values#.tolist())
    # print(X)
    # X = np.sort(X, order=['unix'])
    # print(X)
    y = (data_df['Status']
        .replace('underperform',0)
        .replace('outperform',1)
        .values)

    X = preprocessing.scale(X)

    return X,y

def Analysis():
    test_size = 500
    X, y = Build_Data_Set()


    clf = svm.SVC(kernel='linear', C=1.0)
    clf.fit(X[:-test_size],y[:-test_size])

    correct_count = 0

    correct_count = np.sum(clf.predict(X[-test_size:]) == y[-test_size:])
    print("Accuracy:", (correct_count/test_size) * 100.00)

    sk_score = metrics.accuracy_score(y_true=y[-test_size:],
                                      y_pred=clf.predict(X[-test_size:]))
    print('sklearn.metrics.accuracy_score = ', sk_score)
    # for x in range(1, test_size+1):
    #     if clf.predict(X[-x])[0] == y[-x]:
    #         correct_count += 1



    # w = clf.coef_[0]
    # a = -w[0] / w[1]
    # xx = np.linspace(min(X[:, 0]), max(X[:, 0]))
    # yy = a * xx - clf.intercept_[0] / w[1]
    #
    # h0 = plt.plot(xx,yy,'k-',label='non weighted')
    #
    # plt.scatter(X[:, 0],X[:, 1],c=y)
    # plt.ylabel('Trailing P/E')
    # plt.xlabel('DE Ratio')
    #
    # plt.show()

Analysis()
