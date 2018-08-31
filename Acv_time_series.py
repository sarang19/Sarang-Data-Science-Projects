# Import pandas and numpy
In [1]:
import pandas as pd
import numpy as np
In [ ]:
#everything is awesome.
In [ ]:
#importing the two datasets
In [2]:
df=pd.read_csv('/Users/sarang/Desktop/dta1.csv')
In [3]:
df2=pd.read_csv('/Users/sarang/Desktop/dta2.csv')
In [ ]:
# attaching the two datasets to form a single dataset.
In [4]:
df3=df.append(df2)
In [5]:
df3.head()
Out[5]:
user	joined_timestamp	num_auctions_engaged
0	buyer	2018-01-01 03:29:38	28
1	seller	2018-01-01 05:22:53	12
2	buyer	2018-01-01 05:33:32	27
3	buyer	2018-01-01 06:58:19	28
4	buyer	2018-01-01 12:42:00	30
In [8]:
df3=df.append(df2)
In [9]:
df3.head()
Out[9]:
user	joined_timestamp	num_auctions_engaged
0	buyer	2016-01-03 02:20:27	22
1	buyer	2016-01-03 07:57:13	17
2	buyer	2016-01-05 00:43:05	25
3	buyer	2016-01-05 03:22:16	20
4	buyer	2016-01-05 06:15:42	18
In [ ]:
#Removing the rows with missing values.
In [10]:
df3.dropna(inplace=True)
In [11]:
df3.tail()
Out[11]:
user	joined_timestamp	num_auctions_engaged
2348	buyer	2018-03-31 05:58:48	23
2349	buyer	2018-03-31 06:21:29	26
2350	buyer	2018-03-31 08:21:23	28
2351	buyer	2018-03-31 08:27:26	33
2352	buyer	2018-03-31 09:39:29	29
In [12]:
df3.info()
<class 'pandas.core.frame.DataFrame'>
Int64Index: 6109 entries, 0 to 2352
Data columns (total 3 columns):
user                    6109 non-null object
joined_timestamp        6109 non-null object
num_auctions_engaged    6109 non-null int64
dtypes: int64(1), object(2)
memory usage: 190.9+ KB
In [ ]:
#Importing time and datetime to convert object into datetime64
In [13]:
import time
import datetime
In [15]:
df3.joined_timestamp = pd.to_datetime(df3.joined_timestamp)
In [16]:
df3.info()
<class 'pandas.core.frame.DataFrame'>
Int64Index: 6109 entries, 0 to 2352
Data columns (total 3 columns):
user                    6109 non-null object
joined_timestamp        6109 non-null datetime64[ns]
num_auctions_engaged    6109 non-null int64
dtypes: datetime64[ns](1), int64(1), object(1)
memory usage: 190.9+ KB
In [17]:
df3.head()
Out[17]:
user	joined_timestamp	num_auctions_engaged
0	buyer	2016-01-03 02:20:27	22
1	buyer	2016-01-03 07:57:13	17
2	buyer	2016-01-05 00:43:05	25
3	buyer	2016-01-05 03:22:16	20
4	buyer	2016-01-05 06:15:42	18
In [18]:
#above I have imported , joined two datasets and cleaned the data for missing values i.e - date. 
#cleaned for missing values cause we dont need noise while predicting a metric otherwise the results would be deemed uselss
In [ ]:
#Checking how user engagements varies monthly.
In [28]:
df3['EVERY_Month'] = df.joined_timestamp.dt.to_period('M')
In [29]:
df3.head()
Out[29]:
user	joined_timestamp	num_auctions_engaged	EVERY_15_MIN	EVERY_45_MIN	EVERY_Month
0	buyer	2016-01-03 02:20:27	22	2016-01-03 02:20	2016-01-03 02:20	2016-01
1	buyer	2016-01-03 07:57:13	17	2016-01-03 07:57	2016-01-03 07:57	2016-01
2	buyer	2016-01-05 00:43:05	25	2016-01-05 00:43	2016-01-05 00:43	2016-01
3	buyer	2016-01-05 03:22:16	20	2016-01-05 03:22	2016-01-05 03:22	2016-01
4	buyer	2016-01-05 06:15:42	18	2016-01-05 06:15	2016-01-05 06:15	2016-01
In [30]:
#trying to check for trends and seasonality in user engagement monthly.
In [31]:
#Timestamp as index
In [32]:
df3.set_index('EVERY_Month', inplace=True)
In [39]:
groupby_month=df3.groupby('EVERY_Month').agg(np.mean)
In [42]:
groupby_month.head()
Out[42]:
num_auctions_engaged
EVERY_Month	
2016-01	22.181818
2016-02	22.408333
2016-03	21.539062
2016-04	20.911111
2016-05	21.976562
In [43]:
groupby_month.tail()
Out[43]:
num_auctions_engaged
EVERY_Month	
2017-08	21.324742
2017-09	21.318759
2017-10	23.943689
2017-11	26.640827
2017-12	24.392202
In [5]:
plt.show()
In [3]:
import matplotlib.pyplot as plt
In [ ]:
#plotting Num of auctions enagegd
In [50]:
plt.show()


In [51]:
# I observed some the 2018 data is removed or not shown cause of missing values.
#Its good cause we dont want to include noise in our data
#plus a good metric in this data is obiously - user engagement.
#from histogram we get to know that 25 num of auctions one can normmaly expect to be engaged 
#As seen from the plot there is sudden surge in engagement in the month of dec 2016 and month of november  in 2017 
#There seems to seasonality in the data as we see user engagement increases later in the year.
In [13]:
import pandas as pd
import numpy as np
In [14]:
df=pd.read_csv('/Users/sarang/Desktop/dta1.csv')
In [7]:
from pandas.tools.plotting import autocorrelation_plot
In [15]:
df2=pd.read_csv('/Users/sarang/Desktop/dta2.csv')
In [16]:
df3=df.append(df2)
In [18]:
df3.dropna(inplace=True)
In [19]:
df3.joined_timestamp = pd.to_datetime(df3.joined_timestamp)
In [ ]:
#We want to know the Total number of auctions involved by sellers and buyers.
In [ ]:
groupby_user
In [30]:
#Group by type of user.
groupby_user=df3.groupby('user')['num_auctions_engaged'].count()
In [31]:
groupby_user
Out[31]:
user
buyer     4370
seller    1739
Name: num_auctions_engaged, dtype: int64
In [26]:
#inference: Total num of auctions involved by buyers are far more than sellers at ACV.
In [27]:
#we want to know the difference in engagement between sellers and buyers
#So lets plot it too
In [47]:
import matplotlib.pyplot as plt
In [48]:
df3.boxplot(column='num_auctions_engaged', by='user')
Out[48]:
<matplotlib.axes._subplots.AxesSubplot at 0x112044d10>
In [49]:
plt.title('how involvement varies between sellers and buyers')
Out[49]:
<matplotlib.text.Text at 0x112288950>
In [50]:
plt.show()

In [51]:
# from the plot we see that median engagment for buyers is 25 and that of sellers is around 15
# from the plot we see 
In [ ]:
 
In [1]:
#Creating a pivot table
In [3]:
import pandas as pd
import numpy as np
In [4]:
df=pd.read_csv('/Users/sarang/Desktop/dta1.csv')
In [5]:
df2=pd.read_csv('/Users/sarang/Desktop/dta2.csv')
In [6]:
df3=df.append(df2)
In [8]:
df3.dropna(inplace=True)
In [9]:
df3.joined_timestamp = pd.to_datetime(df3.joined_timestamp)
In [11]:
df3['EVERY_Month'] = df3.joined_timestamp.dt.to_period('M')
In [28]:
#CREATING A PIVOT TABLE.
x_pivot_table=pd.pivot_table(df3, index='EVERY_Month', values='num_auctions_engaged', columns='user')
In [30]:
#lets plot buyer and seller vary over time in thir engagement.
import matplotlib.pyplot as plt
x_pivot_table.plot(figsize=(20,10), linewidth=5, fontsize=20)
plt.xlabel('Year', fontsize=20);
In [31]:
plt.show()


In [32]:
# inferenece in the month of novemember we observe a surge in buyers especially and not sellers.
In [33]:
# optimizing Advertising spend in other months than novemeber  could significantly bring up the user engagement 
In [34]:
# Creating a time series forecasing model
In [35]:
from statsmodels.tsa.ar_model import AR
from sklearn.metrics import mean_squared_error
/Users/sarang/anaconda/lib/python2.7/site-packages/statsmodels/compat/pandas.py:56: FutureWarning: The pandas.core.datetools module is deprecated and will be removed in a future version. Please use the pandas.tseries module instead.
  from pandas.core import datetools
In [87]:
# create a difference transform of the dataset
def difference(dataset):
	diff = list()
	for i in range(1, len(dataset)):
		value = dataset[i] - dataset[i - 1]
		diff.append(value)
	return np.array(diff)
In [88]:
# Make a prediction give regression coefficients and lag obs
def predict(coef, history):
	yhat = coef[0]
	for i in range(1, len(coef)):
		yhat += coef[i] * history[-i]
	return yhat
In [89]:
groupby_month=df3.groupby('EVERY_Month').agg(np.mean)
import numpy as np
In [90]:
# split dataset
import numpy as np
X = difference(groupby_month.values)
size = int(len(X) * 0.66)
train, test = X[0:size], X[size:]
In [91]:
# train autoregression
model = AR(train)
model_fit = model.fit(maxlag=6, disp=False)
window = model_fit.k_ar
coef = model_fit.params
In [92]:
# walk forward over time steps in test
history = [train[i] for i in range(len(train))]
predictions = list()
for t in range(len(test)):
	yhat = predict(coef, history)
	obs = test[t]
	predictions.append(yhat)
	history.append(obs)
In [93]:
error = mean_squared_error(test, predictions)
print('Test MSE: %.3f' % error)
Test MSE: 4.658
In [98]:
# plot
plt.plot(test)
plt.plot(predictions, color='red')
plt.title('predictions vs actual monthly dataset line plot')
plt.show()
#the blue line is actual and the red one is predicted.

In [ ]:
# we can  infer that the model has predicted high and lows almost correctly and hence can estimate future demand fairly well.
# it can help us to know when the user engagement is going to be low
#so we can alter our plans to invest more in bringing in more customer during those period vua advertising etc.
# we observed a mean square error of 4.658, which is good and closer to 0. 
# we could test building other forecasting models to get even better accuracy.
