INTRODUCTION TO THE PROBLEM:
Airline delays cost the airline company a significant amount of money and is one of the major reasons of financial losses. We want to dig some of the popular airlines and their cause of delay and then predict what factors contribute to a flight arriving late.

#Data Loading
airdf=pd.read_csv('/Users/sarang/Desktop/318750629_72017_4040_airline_delay_causes.csv')


#Data Cleaning
1.x=airdf.dropna(subset=['year',' month', 'carrier', 'carrier_name', 'airport', 'airport_name','arr_flights', 'arr_del15', 'carrier_ct', ' weather_ct', 'nas_ct', 'security_ct', 'late_aircraft_ct', 'arr_cancelled', 'arr_diverted', ' arr_delay', ' carrier_delay', 'weather_delay', 'nas_delay', 'security_delay', 'late_aircraft_delay'], how='any')

2. x.airport.astype('category')
3. x.carrier_name.astype('category')


#Exploratory Data Analysis (Visual and Quantitative) /Data Analysis

#Linear Regression
_ = plt.plot(x['carrier_ct'], x['late_aircraft_delay'], marker='.', linestyle='none')
plt.margins(0.02)
_ = plt.xlabel('Carrier conditions')
_ = plt.ylabel('Late aircraft delay')

# Perform a linear regression using np.polyfit(): a, b
a, b = np.polyfit(x['carrier_ct'], x['late_aircraft_delay'],1)

# Print the results to the screen
print('slope =', a, 'late aircraft delay/ carrier_ct')
print('intercept =', b, 'when carrier conditions are normal or 0')

# Make theoretical line to plot
x = np.array([0,100])
y = a *x+ b

# Add regression line to your plot
_ = plt.plot(y)

# Draw the plot
plt.show()




('slope =', 86.038634937641177, 'late aircraft delay/ carrier_ct')
('intercept =', -235.46580372421607, 'when carrier conditions are normal or 0')






INFERENCE: Shows that carrier conditions doesn’t actually follow a linear trend hence it wont be a significant factor in late aircraft delay.(As many of data points fall below even if carrier conditions gets worse)





plt.scatter(x='arr_diverted',y='late_aircraft_delay' ,alpha=0.2, data=x)

#Linear Regression
_ = plt.plot(x['arr_diverted'], x['late_aircraft_delay'], marker='.', linestyle='none')
plt.margins(0.02)
_ = plt.xlabel('airline diverted condition')
_ = plt.ylabel('Late aircraft delay')

# Perform a linear regression using np.polyfit(): a, b
a, b = np.polyfit(x['arr_diverted'], x['late_aircraft_delay'],1)

# Print the results to the screen
print('slope =', a, 'late aircraft delay/ arr_diverted')
print('intercept =', b, 'when flights are not diverted conditions are normal or 0')

# Make theoretical line to plot
x = np.array([0,100])
y = a *x+ b

# Add regression line to your plot
_ = plt.plot(y)

# Draw the plot
plt.show()

('slope =', 811.94556956550741, 'late aircraft delay/ arr_diverted')
('intercept =', 951.64900741112774, 'when flights are not diverted conditions are normal or 0')



Inference: Given the slope=811 and given how slant it is, we can say that a diverted flight is certainly going to cause delay. 



#Correlation between  security conditions and late aircraft delay
1.correlation=np.corrcoef(x['security_ct'], x['late_aircraft_delay'])

correlation
Out[98]: 
array([[ 1.        ,  0.42960708],
       [ 0.42960708,  1.        ]])
Inference: shows some correlation between security conditions and delay. But it is weak 0.42.



#covariance between carrier conditions and late aircraft delay
2.covariance_matrix=np.cov(x['carrier_ct'], x['late_aircraft_delay'])
covariance_matrix
Out[100]: 
array([[  2.35531691e+03,   2.02648252e+05],
       [  2.02648252e+05,   2.62728747e+07]])

Inference: shows carrier conditions and late aircraft don’t vary the same way. Hence not a factor to be relied upon for prediction. We can use lasso regressor to find it out.


#covariance between security conditions and late aircraft 
3. covariance_matrix_security=np.cov(x['security_ct'], x['late_aircraft_delay'])

covariance_matrix_security
Out[105]: 
array([[  7.91576198e-01,   1.95916758e+03],
       [  1.95916758e+03,   2.62728747e+07]])

Inference: It confirms that they don’t vary similarly as increase in security delay wont necessarily cause  aircraft to get late.







# Seaborn’s linear plot, National aviation security vs Late_aircarft_delay
sns.lmplot(x='nas_ct', y='late_aircraft_delay',data=x, hue='carrier_name', palette='Set1')

# Display the plot
plt.show()

















Inference:
Grouped by different airlines we see the relation that National Aviation security/ systems contributes in getting a airline to get late (linearly).



# linear / diverted flight vs late aircraft delay
sns.lmplot(x='arr_diverted', y='late_aircraft_delay',data=x, hue='carrier_name', palette='Set1')

# Display the plot
plt.show()



Inference: it supplements to the hypothesis that a diverted aircraft will cause an aircraft to be late.




#Group by different airlines and their count on cancelled flights
Groupby
by_class = x.groupby('carrier_name')

count_by_class = by_class['arr_cancelled'].count()

count_by_class
Out[143]: 
carrier_name
ATA Airlines d/b/a ATA            918
AirTran Airways Corporation      6955
Alaska Airlines Inc.             8790
Aloha Airlines Inc.               253
America West Airlines Inc.       1579
American Airlines Inc.          13940
American Eagle Airlines Inc.    15404
Atlantic Coast Airlines          1253
Atlantic Southeast Airlines     12158
Comair Inc.                      7685
Continental Air Lines Inc.       6908
Delta Air Lines Inc.            19822
Endeavor Air Inc.                 564
Envoy Air                        2521
ExpressJet Airlines Inc.        22287
Frontier Airlines Inc.           7125
Hawaiian Airlines Inc.           2540
Independence Air                  670
JetBlue Airways                  7949
Mesa Airlines Inc.               9418
Northwest Airlines Inc.          8068
Pinnacle Airlines Inc.           6434
SkyWest Airlines Inc.           25069
Southwest Airlines Co.          12238
Spirit Air Lines                 1068
US Airways Inc.                 10692
United Air Lines Inc.           13480
Virgin America                   1219
Name: arr_cancelled, dtype: int64





#Group by different airlines and their average traffic in the airports
by_carrier_sub=by_carrier['arr_flights']

aggregated=by_carrier_sub.agg(['mean'])

aggregated
Out[166]: 
                                     mean
carrier_name                             
ATA Airlines d/b/a ATA         197.672113
AirTran Airways Corporation    349.067146
Alaska Airlines Inc.           254.054494
Aloha Airlines Inc.            353.940711
America West Airlines Inc.     318.658645
American Airlines Inc.         651.870230
American Eagle Airlines Inc.   336.566152
Atlantic Coast Airlines        298.680766
Atlantic Southeast Airlines    207.827027
Comair Inc.                    229.775667
Continental Air Lines Inc.     354.250579
Delta Air Lines Inc.           488.177126
Endeavor Air Inc.              212.677305
Envoy Air                      232.979770
ExpressJet Airlines Inc.       304.703056
Frontier Airlines Inc.         150.858667
Hawaiian Airlines Inc.         355.144488
Independence Air               293.188060
JetBlue Airways                357.560825
Mesa Airlines Inc.             180.948184
Northwest Airlines Inc.        343.027764
Pinnacle Airlines Inc.         189.950886
SkyWest Airlines Inc.          323.767442
Southwest Airlines Co.        1328.326034
Spirit Air Lines               324.082397
US Airways Inc.                485.279742
United Air Lines Inc.          501.147997
Virgin America                 279.526661






 #Group by different airlines and their average weather conditions, carrier delay, late_aircarft_delay

by_factors=by_carrier[[' weather_ct', ' carrier_delay', 'late_aircraft_delay']]

aggregated=by_factors.agg(['mean', 'max'])

aggregated
Out[170]: 
                              weather_ct          carrier_delay            \
                                                             mean     max           mean       max   
carrier_name                                                                
ATA Airlines d/b/a ATA               0.262952   15.32     441.725490    6063.0   
AirTran Airways Corporation     0.622456   58.82     623.882962   17960.0   
Alaska Airlines Inc.            0.813841   43.96     721.506143   36808.0   
Aloha Airlines Inc.             0.160316    3.43     572.814229    3942.0   
America West Airlines Inc.      0.597600   32.03    1076.281191   22669.0   
American Airlines Inc.          6.775189  475.82    2454.635438   85312.0   
American Eagle Airlines Inc.    3.564982  207.05    1104.875682   49306.0   
Atlantic Coast Airlines         2.926345   74.73     849.162809   19780.0   
Atlantic Southeast Airlines     4.779562  641.54    1138.144925  134693.0   
Comair Inc.                     9.506951  717.94    1094.992843   70666.0   
Continental Air Lines Inc.      2.632892  128.88     938.166039   29824.0   
Delta Air Lines Inc.            2.509886  240.79    1565.604177  196944.0   
Endeavor Air Inc.               0.879433   43.26     633.746454   18434.0   
Envoy Air                       3.095442  149.48     830.722729   27747.0   
ExpressJet Airlines Inc.        1.594827  295.28    1142.451878   47003.0   
Frontier Airlines Inc.          0.495499   58.11     418.671018   12696.0   
Hawaiian Airlines Inc.          0.504024   88.93     816.700000   14517.0   
Independence Air                0.637985   17.43     453.770149    8924.0   
JetBlue Airways                 1.280267   40.71    1416.540697   25675.0   
Mesa Airlines Inc.              1.322687   86.00     943.719261   29798.0   
Northwest Airlines Inc.         3.725844  298.62    1455.754462   48770.0   
Pinnacle Airlines Inc.          1.188365   90.95     678.452129   33261.0   
SkyWest Airlines Inc.           1.731854  240.00    1038.320196   51250.0   
Southwest Airlines Co.          6.236887  182.37    3048.090211   30816.0   
Spirit Air Lines                1.133736   15.89    1017.025281    8798.0   
US Airways Inc.                 1.697978   86.69    1281.730733   39873.0   
United Air Lines Inc.           2.528145   81.10    1648.621142   40363.0   
Virgin America                  5.509844   86.75     578.940935    6472.0   





#Group by different airlines and their average weather conditions, carrier delay, late_aircarft_delay.

                             late_aircraft_delay            
                                            mean       max  
carrier_name                                                
ATA Airlines d/b/a ATA                794.807190   20899.0  
AirTran Airways Corporation          1987.212940  101087.0  
Alaska Airlines Inc.                  842.230148   67729.0  
Aloha Airlines Inc.                   384.972332    8188.0  
America West Airlines Inc.            737.570614   20454.0  
American Airlines Inc.               2859.008393  148181.0  
American Eagle Airlines Inc.         1632.210270  134763.0  
Atlantic Coast Airlines              1596.964086   90777.0  
Atlantic Southeast Airlines           734.940368  145680.0  
Comair Inc.                           139.776578    8721.0  
Continental Air Lines Inc.           1148.475825   50631.0  
Delta Air Lines Inc.                 1396.292402  147167.0  
Endeavor Air Inc.                     570.468085   28654.0  
Envoy Air                            1179.978183   73605.0  
ExpressJet Airlines Inc.             1618.503343  108742.0  
Frontier Airlines Inc.                666.261193   31759.0  
Hawaiian Airlines Inc.                355.648031   17186.0  
Independence Air                     1765.541791   97611.0  
JetBlue Airways                      2058.165807   66244.0  
Mesa Airlines Inc.                    771.338819   66911.0  
Northwest Airlines Inc.               742.962072   53260.0  
Pinnacle Airlines Inc.                659.813025   54486.0  
SkyWest Airlines Inc.                1380.686745   94384.0  
Southwest Airlines Co.               6726.256006   79382.0  
Spirit Air Lines                        1465.727528   14350.0  
US Airways Inc.                      1492.250748   55902.0  
United Air Lines Inc.                2507.853561   91633.0  
Virgin America                       1232.049221   17331.0  







#Group by Airports for American airlines and their late_aircraft_delay


american_airlines_delay
Out[22]: 
airport
ABQ     1238.294118
ALB      220.360000
AMA      135.600000
ANC      277.571429
ATL     2637.294118
AUS     3665.658824
BDL      961.188235
BHM      412.496552
BNA     1781.435294
BOI      183.040000
BOS     5244.429412
BTR      103.800000
BUF      242.000000
BUR      449.923810
BWI     1442.805882
BZN      155.000000
CHS      195.434783
CLE      627.543478
CLT     3956.647059
CMH      537.923529
COS      704.964706
CRP      298.173913
CVG      644.250000
DAB        0.000000
DAL      540.714286
DAY      366.205882
DCA     4118.229412
DEN     2771.188235
DFW    57049.800000
DSM      440.506667
    
PNS      290.187500
PSP      426.488235
PVD      845.883333
PWM      124.320000
RDU     2340.229412
RIC      442.576471
RNO      614.476471
ROC      128.347826
RST      415.200000
RSW      644.958824
SAN     2343.458824
SAT     2335.547059
SAV       28.375000
SBA       14.750000
SDF      326.094675
SEA     2224.276471
SFO     4324.658824
SJC     1518.617647
SJU     2595.752941
SLC     1053.370588
SMF      729.864706
SNA     1447.264706
STL     5411.717647
STT      423.694118
STX      117.576471
SYR      176.520000
TPA     2762.423529
TUL     1586.447059
TUS     1528.911765
XNA      325.412162
Name: late_aircraft_delay, Length: 115, dtype: float64

max(american_airlines_delay)
Out[23]: 57049.800000000003









INFERENECE: 
we came to know that southwest airlines had the highest
average delay in aircrafts of 6726mins. Followed by American airlines with
an average of 2859.But since the airline traffic is higher in  American
airlines i.e-651, so we want to dig deeper into American airlines.




#Time Series plot of American airlines by year and month
#American Airlines
american_airlines = x.loc[x['carrier_name']=='American Airlines Inc.']
american_airlines_delay_by_year = american_airlines_delay.unstack(level=' month')
american_airlines_delay = american_airlines.groupby(['year',' month'])['late_aircraft_delay'].mean()
american_airlines_delay_by_year.plot()
plt.show()





Inference:
It can be observed that in the year 2007 and especially in the month of june 
to august for almost all the following years the delay was maximum.





2. american_airlines_delay_by_year = american_airlines_delay.unstack(level='year')
american_airlines_delay_by_year.plot.area()
plt.show()






Inference:
It can be inferred that chances that of the American airlines flight
getting late are high in the month of June, July and August. 







american_airlines = x.loc[x['airport']=='JFK']
american_airlines_delay = american_airlines.groupby(['year'])['late_aircraft_delay'].mean()
american_airlines_delay.plot()
plt.title('Delay of American Airlines inc at JFK by year.')
plt.show()

















american_airlines = x.loc[x['airport']=='JFK']
american_airlines_delay = american_airlines.groupby([' month'])['late_aircraft_delay'].mean()
american_airlines_delay.plot()
plt.title('Delay of American Airlines inc at JFK by month.')
plt.show()





american_airlines = x.loc[x['airport']=='JFK']
american_airlines_delay
american_airlines.groupby(['carrier_name'])['late_aircraft_delay'].mean
()
plt.xticks(rotation=90)
american_airlines_delay.plot()
plt.xticks(rotation=90)
plt.title('Airline with the most traffic at JFK, is it american airline?')
plt.show()

















american_airlines = x.loc[x['carrier_name']=='American Airlines inc.']
american_airlines_delay = american_airlines.groupby(['year'])['late_aircraft_delay','security_delay','nas_delay','weather_delay',' carrier_delay'].mean()
american_airlines_delay.plot()
plt.title('Causes ofAmerican Airline Delay at Jfk airport')
plt.show()






american_airlines = x.loc[x['carrier_name']=='American Airlines inc.']
american_airlines_delay = american_airlines.groupby(['year'])['late_aircraft_delay','security_delay','nas_delay','weather_delay',' carrier_delay'].mean()
american_airlines_delay.plot()
plt.title('Causes ofAmerican Airline Delay at Jfk airport')
plt.show()


Inference:
The cause of delay of American airlines at JFK airport being majorly due to national aviation system/security process followed by carrier delay. Which they might have to improve upon.However it is observed there was no significant delay through weather at all ( almost negligible).


#Machine Learning


#Feature Selection/Feature Engineering and Dimensionality reduction
from sklearn.linear_model import Lasso

a=x[['arr_cancelled','arr_diverted','carrier_ct', ' weather_ct','nas_ct','security_ct', 'late_aircraft_ct']]

from sklearn.linear_model import Lasso

# Instantiate a lasso regressor: lasso
lasso = Lasso(alpha=0.4,normalize=True)

# Fit the regressor to the data
lasso.fit(a,y)

Out[57]: 
Lasso(alpha=0.4, copy_X=True, fit_intercept=True, max_iter=1000,
   normalize=True, positive=False, precompute=False, random_state=None,
   selection='cyclic', tol=0.0001, warm_start=False)

lasso_coef=lasso.coef_
print(lasso_coef)

[  4.65880749  41.37327142   0.           0.           2.31397039  -0.
  55.36691392]


# Linear Regression 

from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import train_test_split

# Create training and test sets
X_train, X_test, y_train, y_test = train_test_split(a, y, test_size = 0.3, random_state=42)


reg_all = LinearRegression()

# Fit the regressor to the training data
reg_all=reg_all.fit(X_train,y_train)

# Predict on the test data: y_pred
y_pred = reg_all.predict(X_test)

# Compute and print R^2 and RMSE
print("R^2: {}".format(reg_all.score(X_test, y_test)))
rmse = np.sqrt(mean_squared_error(y_test,y_pred))
print("Root Mean Squared Error: {}".format(rmse))

R^2: 0.964577207896
Root Mean Squared Error: 958.072984123


# 5 Fold cross validation
2.

from sklearn.linear_model import LinearRegression
from sklearn.model_selection import cross_val_score

# Create a linear regression object: reg
reg = LinearRegression()


cv_scores = cross_val_score(reg,a,y, cv=5)

# Print the 5-fold cross-validation scores
print(cv_scores)

print("Average 5-Fold CV Score: {}".format((np.mean(cv_scores))))

[ 0.94524707  0.96828198  0.97113696  0.97147914  0.95313221]
Average 5-Fold CV Score: 0.96185547261



Conclusion:
We conclude that factors such as national aviation system security, diverted flight, cancelled
Flight and not variables such as weather conditions, security check predicts the delay time of 
the aircraff accurately.
