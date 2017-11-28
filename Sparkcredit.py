from pyspark import SparkConf, SparkContext

from pyspark import SparkConf, SparkContext

conf = SparkConf().setMaster("local").setAppName("SparkCredit")


import os.path
import csv


ccRaw = sc.textFile("/Users/sarang/Desktop/SparkPythonDoBigDataAnalytics-Resources/credit-card-default-1000.csv")
ccRaw.take(5)



ccRaw = sc.textFile("/Users/sarang/Desktop/SparkPythonDoBigDataAnalytics-Resources/credit-card-default-1000.csv")
ccRaw.take(5)


#removing lines that are no "CSV"
filteredLines = dataLines.filter(lambda x : x.find("aaaaaa") < 0 )
filteredLines.count()



def rowconvert(record) :
    attList = record.split(",")

    # rounding the ages to range 10s.    
    ageRound = round(float(attList[5]) / 10.0) * 10

    #Normalizing sex with values 1 for male and 2 for female.
    sex = attList[2]
    if sex =="M":
        sex=1
    elif sex == "F":
        sex=2
        #average pay amount
    avgPayAmt = (float(attList[18]) +  \
                    float(attList[19]) + \
                    float(attList[20]) + \
                    float(attList[21]) + \
                    float(attList[22]) + \
                    float(attList[23]) ) / 6.0
    #Find average billed Amount
    avgBillAmt = (float(attList[12]) +  \
                    float(attList[13]) + \
                    float(attList[15]) + \
                    float(attList[16]) + \
                    float(attList[16]) + \
                    float(attList[17]) ) / 6.0
    #Find average pay duration. 
    avgPayDuration = round((abs(float(attList[6])) + \
                        abs(float(attList[7])) + \
                        abs(float(attList[8])) +\
                        abs(float(attList[9])) +\
                        abs(float(attList[10])) +\
                        abs(float(attList[11]))) / 6)
    #Average percentage paid.                    
    perPay = round((avgPayAmt/(avgBillAmt+1) * 100) / 25) * 25

    values = Row (  CUSTID = attList[0], \
                    LIMIT_BAL = float(attList[1]), \
                    SEX = float(sex),\
                    EDUCATION = float(attList[3]),\
                    MARRIAGE = float(attList[4]),\
                    AGE = float(ageRound), \
                    AVG_PAY_DUR = float(avgPayDuration),\
                    AVG_BILL_AMT = abs(float(avgBillAmt)), \
                    AVG_PAY_AMT = float(avgPayAmt), \
                    PER_PAID= abs(float(perPay)), \
                    DEFAULTED = float(attList[24]) 
                    )
    return values





#Cleaned RDD    
ccRows = cleanedLines.map(rowconvert)
ccRows.take(60)

from pyspark.sql import SQLContext, Row

ccDf = spark.createDataFrame(ccRows)

ccDf.cache()
ccDf.show(10)

+----+------------------+------------------+-----------+------+---------+---------+---------+--------+---------+---+
| AGE|      AVG_BILL_AMT|       AVG_PAY_AMT|AVG_PAY_DUR|CUSTID|DEFAULTED|EDUCATION|LIMIT_BAL|MARRIAGE| PER_PAID|SEX|
+----+------------------+------------------+-----------+------+---------+---------+---------+--------+---------+---+
|20.0|               0.0|           27000.0|        2.0|   530|      0.0|      2.0|  20000.0|     2.0|2700000.0|2.0|
|20.0|               0.0| 262.6666666666667|        1.0|    38|      0.0|      2.0|  60000.0|     2.0|  26275.0|2.0|
|20.0|               0.0|             250.0|        1.0|    43|      0.0|      2.0|  10000.0|     2.0|  25000.0|1.0|
|20.0|             334.0|21969.166666666668|        1.0|    47|      0.0|      1.0|  20000.0|     2.0|   6550.0|2.0|
|20.0|3277.3333333333335|           28651.5|        1.0|    70|      0.0|      4.0|  20000.0|     2.0|    875.0|1.0|
|20.0|             960.0|            7358.0|        1.0|    79|      0.0|      2.0|  30000.0|     2.0|    775.0|2.0|
|20.0|             145.5|             829.5|        0.0|    99|      0.0|      3.0|  50000.0|     1.0|    575.0|2.0|
|20.0| 408.3333333333333|3328.3333333333335|        0.0|   104|      0.0|      3.0|  50000.0|     2.0|    825.0|2.0|
|20.0|61.333333333333336| 359.8333333333333|        1.0|   135|      0.0|      2.0|  30000.0|     2.0|    575.0|2.0|
|20.0|            4652.0|            6896.5|        1.0|   170|      0.0|      2.0|  50000.0|     2.0|    150.0|2.0|
+----+------------------+------------------+-----------+------+---------+---------+---------+--------+---------+---+
only showing top 10 rows


import pandas as pd
# adding an extra column for sex in terms of their name

genderDict = [{"SEX" : 1.0, "SEX_NAME" : "Male"}, \
                {"SEX" : 2.0, "SEX_NAME" : "Female"}]                
genderDf = spark.createDataFrame(pd.DataFrame(genderDict, \
            columns=['SEX', 'SEX_NAME']))
genderDf.collect()
ccDf1 = ccDf.join( genderDf, ccDf.SEX== genderDf.SEX ).drop(genderDf.SEX)
ccDf1.take(5)



#adding column for education and naimng them
eduDict = [{"EDUCATION" : 1.0, "ED_STR" : "Graduate"}, \
                {"EDUCATION" : 2.0, "ED_STR" : "University"}, \
                {"EDUCATION" : 3.0, "ED_STR" : "High School" }, \
                {"EDUCATION" : 4.0, "ED_STR" : "Others"}]                
eduDf = spark.createDataFrame(pd.DataFrame(eduDict, \
            columns=['EDUCATION', 'ED_STR']))
eduDf.collect()
ccDf2 = ccDf1.join( eduDf, ccDf1.EDUCATION== eduDf.EDUCATION ).drop(eduDf.EDUCATION)
ccDf2.take(5)






# adding columns with names for type of status i.e married or single.
marrDict = [{"MARRIAGE" : 1.0, "MARR_DESC" : "Single"}, \
                {"MARRIAGE" : 2.0, "MARR_DESC" : "Married"}, \
                {"MARRIAGE" : 3.0, "MARR_DESC" : "Others"}]                
marrDf = spark.createDataFrame(pd.DataFrame(marrDict, \
            columns=['MARRIAGE', 'MARR_DESC']))
marrDf.collect()
ccFinalDf = ccDf2.join( marrDf, ccDf2.MARRIAGE== marrDf.MARRIAGE ).drop(marrDf.MARRIAGE)
ccFinalDf.cache()
ccFinalDf.take(5)





#Creating a temporary df
ccFinalDf.createOrReplaceTempView("CCDATA")


spark.sql("SELECT SEX_NAME, count(*) as Total, " + \
                " SUM(DEFAULTED) as Defaults, " + \
                " ROUND(SUM(DEFAULTED) * 100 / count(*)) as PER_DEFAULT " + \
                "FROM CCDATA GROUP BY SEX_NAME"  ).show()
+--------+-----+--------+-----------+
|SEX_NAME|Total|Defaults|PER_DEFAULT|
+--------+-----+--------+-----------+
|  Female|  591|   218.0|       37.0|
|    Male|  409|   185.0|       45.0|
+--------+-----+--------+-----------+



ccLp = ccFinalDf.rdd.repartition(2).map(transformToLabeledPoint)
ccLp.collect()
ccNormDf = spark.createDataFrame(ccLp,["label", "features"])
ccNormDf.select("label","features").show(10)
ccNormDf.cache()









spark.sql("SELECT MARR_DESC, ED_STR, count(*) as Total," + \
                " SUM(DEFAULTED) as Defaults, " + \
                " ROUND(SUM(DEFAULTED) * 100 / count(*)) as PER_DEFAULT " + \
                "FROM CCDATA GROUP BY MARR_DESC,ED_STR " + \
                "ORDER BY 1,2").show()
+---------+-----------+-----+--------+-----------+
|MARR_DESC|     ED_STR|Total|Defaults|PER_DEFAULT|
+---------+-----------+-----+--------+-----------+
|  Married|   Graduate|  268|    69.0|       26.0|
|  Married|High School|   55|    24.0|       44.0|
|  Married|     Others|    4|     2.0|       50.0|
|  Married| University|  243|    65.0|       27.0|
|   Others|   Graduate|    4|     4.0|      100.0|
|   Others|High School|    8|     6.0|       75.0|
|   Others| University|    7|     3.0|       43.0|
|   Single|   Graduate|  123|    71.0|       58.0|
|   Single|High School|   87|    52.0|       60.0|
|   Single|     Others|    3|     2.0|       67.0|
|   Single| University|  198|   105.0|       53.0|







spark.sql("SELECT AVG_PAY_DUR, count(*) as Total, " + \
                " SUM(DEFAULTED) as Defaults, " + \
                " ROUND(SUM(DEFAULTED) * 100 / count(*)) as PER_DEFAULT " + \
                "FROM CCDATA GROUP BY AVG_PAY_DUR ORDER BY 1"  ).show()
+-----------+-----+--------+-----------+
|AVG_PAY_DUR|Total|Defaults|PER_DEFAULT|
+-----------+-----+--------+-----------+
|        0.0|  277|   115.0|       42.0|
|        1.0|  631|   244.0|       39.0|
|        2.0|   82|    39.0|       48.0|
|        3.0|    7|     4.0|       57.0|
|        4.0|    3|     1.0|       33.0|
+-----------+-----+--------+-----------+








#Correlation analysis
for i in ccDf.columns:
    if not( isinstance(ccDf.select(i).take(1)[0][0], str)) :
        print( "Correlation to DEFAULTED for ", i,\
            ccDf.stat.corr('DEFAULTED',i))
        
('Correlation to DEFAULTED for ', 'AGE', 0.5165602202876683)
('Correlation to DEFAULTED for ', 'AVG_BILL_AMT', 0.18782747215913168)
('Correlation to DEFAULTED for ', 'AVG_PAY_AMT', -0.1635960889097275)
('Correlation to DEFAULTED for ', 'AVG_PAY_DUR', 0.01419191559847904)




from pyspark.ml.feature import StringIndexer
stringIndexer = StringIndexer(inputCol="label", outputCol="indexed")
si_model = stringIndexer.fit(ccNormDf)
td = si_model.transform(ccNormDf)
td.collect()





#Split into training and testing data
(trainingData, testData) = td.randomSplit([0.7, 0.3])
trainingData.count()
testData.count()



from pyspark.ml.classification import RandomForestClassifier
from pyspark.ml.classification import DecisionTreeClassifier
from pyspark.ml.classification import NaiveBayes, NaiveBayesModel
from pyspark.ml.evaluation import MulticlassClassificationEvaluator

evaluator = MulticlassClassificationEvaluator(predictionCol="prediction", \
                    labelCol="indexed",metricName="accuracy")




#Creating the Decision Trees model
dtClassifer = DecisionTreeClassifier(labelCol="indexed", \
                featuresCol="features")
dtModel = dtClassifer.fit(trainingData)
#Predicting on the test data
predictions = dtModel.transform(testData)
predictions.select("prediction","indexed","label","features").collect()
print("Results of Decision Trees : ",evaluator.evaluate(predictions))

('Results of Decision Trees : ', 0.6905537459283387)





#Create the Random Forest model
rmClassifer = RandomForestClassifier(labelCol="indexed", \
                featuresCol="features")
rmModel = rmClassifer.fit(trainingData)
#Predict on the test data
predictions = rmModel.transform(testData)
predictions.select("prediction","indexed","label","features").collect()
print("Results of Random Forest : ",evaluator.evaluate(predictions)  )

('Results of Random Forest : ', 0.739413680781759)




#Creating the Random Forest model
rmClassifer = RandomForestClassifier(labelCol="indexed", \
                featuresCol="features")
rmModel = rmClassifer.fit(trainingData)
#Predicting on the test data
predictions = rmModel.transform(testData)
predictions.select("prediction","indexed","label","features").collect()
print("Results of Random Forest : ",evaluator.evaluate(predictions)  )

('Results of Random Forest : ', 0.739413680781759)






#Create the Naive Bayes model
nbClassifer = NaiveBayes(labelCol="indexed", \
                featuresCol="features")
nbModel = nbClassifer.fit(trainingData)
#Predict on the test data
predictions = nbModel.transform(testData)
predictions.select("prediction","indexed","label","features").collect()
print("Results of Naive Bayes : ",evaluator.evaluate(predictions)  )

('Results of Naive Bayes : ', 0.6384364820846905)





#Creating a Spark Data Frame with the features
ccFClustDf = spark.createDataFrame(ccMap)
ccFClustDf.cache()

ccFClustDf.select("features").show(10)

#Performing clustering
from pyspark.ml.clustering import KMeans
kmeans = KMeans(k=4, seed=1)
model = kmeans.fit(ccFClustDf)
predictions = model.transform(ccFClustDf)
predictions.select("*").show()

+--------------------+
|            features|
+--------------------+
|[-1.2014752545458...|
|[-1.2014752545458...|
|[-1.2014752545458...|
|[-1.2014752545458...|
|[-1.2014752545458...|
|[-1.2014752545458...|
|[-1.2014752545458...|
|[-1.2014752545458...|
|[-1.2014752545458...|
|[-1.2014752545458...|
+--------------------+
only showing top 10 rows





+------+--------------------+----------+
|CUSTID|            features|prediction|
+------+--------------------+----------+
|   103|[-1.2014752545458...|         3|
|   932|[-1.2014752545458...|         3|
|   466|[-1.2014752545458...|         3|
|    35|[-1.2014752545458...|         3|
|    66|[-1.2014752545458...|         3|
|   553|[-1.2014752545458...|         3|
|   603|[-1.2014752545458...|         3|
|   576|[-1.2014752545458...|         3|
|   452|[-1.2014752545458...|         3|
|    91|[-1.2014752545458...|         3|
|   375|[-1.2014752545458...|         3|
|   997|[-1.2014752545458...|         3|
|   874|[-1.2014752545458...|         3|
|   840|[-1.2014752545458...|         3|
|   596|[-1.2014752545458...|         3|
|   587|[-1.2014752545458...|         3|
|    97|[-1.2014752545458...|         3|
|   971|[-1.2014752545458...|         3|
|   956|[-1.2014752545458...|         3|
|   862|[-1.2014752545458...|         3|
+------+--------------------+----------+
only showing top 20 rows










# -*- coding-*-
from pyspark import SparkConf, SparkContext
conf = SparkConf().setMaster("local").setAppName("SparkCredit")
import os.path
import csv




ccRaw = sc.textFile("/Users/sarang/Desktop/SparkPythonDoBigDataAnalytics-Resources/credit-card-default-1000.csv")
ccRaw.take(5)
#removing lines that are no "CSV"
filteredLines = dataLines.filter(lambda x : x.find("aaaaaa") < 0 )
filteredLines.count()


def rowconvert(record) :
attList = record.split(",")




# rounding the ages to range 10s. 
ageRound = round(float(attList[5]) / 10.0) * 10

#Normalizing sex with values 1 for male and 2 for female.
sex = attList[2]
if sex =="M":
sex=1
elif sex == "F":
sex=2
#average pay amount
avgPayAmt = (float(attList[18]) + \
float(attList[19]) + \
float(attList[20]) + \
float(attList[21]) + \
float(attList[22]) + \
float(attList[23]) ) / 6.0
#Find average billed Amount
avgBillAmt = (float(attList[12]) + \
float(attList[13]) + \
float(attList[15]) + \
float(attList[16]) + \
float(attList[16]) + \
float(attList[17]) ) / 6.0
#Find average pay duration. 
avgPayDuration = round((abs(float(attList[6])) + \
abs(float(attList[7])) + \
abs(float(attList[8])) +\
abs(float(attList[9])) +\
abs(float(attList[10])) +\
abs(float(attList[11]))) / 6)
#Average percentage paid. 
perPay = round((avgPayAmt/(avgBillAmt+1) * 100) / 25) * 25

values = Row ( CUSTID = attList[0], \
LIMIT_BAL = float(attList[1]), \
SEX = float(sex),\
EDUCATION = float(attList[3]),\
MARRIAGE = float(attList[4]),\
AGE = float(ageRound), \
AVG_PAY_DUR = float(avgPayDuration),\
AVG_BILL_AMT = abs(float(avgBillAmt)), \
AVG_PAY_AMT = float(avgPayAmt), \
PER_PAID= abs(float(perPay)), \
DEFAULTED = float(attList[24]) 
)
return values
#Cleaned RDD 
ccRows = cleanedLines.map(rowconvert)
ccRows.take(60)

from pyspark.sql import SQLContext, Row

ccDf = spark.createDataFrame(ccRows)

ccDf.cache()
ccDf.show(10)
import pandas as pd
# adding an extra column for sex in terms of their name

genderDict = [{"SEX" : 1.0, "SEX_NAME" : "Male"}, \
{"SEX" : 2.0, "SEX_NAME" : "Female"}] 
genderDf = spark.createDataFrame(pd.DataFrame(genderDict, \
columns=['SEX', 'SEX_NAME']))
genderDf.collect()
ccDf1 = ccDf.join( genderDf, ccDf.SEX== genderDf.SEX ).drop(genderDf.SEX)
ccDf1.take(5)
#adding column for education and naimng them
eduDict = [{"EDUCATION" : 1.0, "ED_STR" : "Graduate"}, \
{"EDUCATION" : 2.0, "ED_STR" : "University"}, \
{"EDUCATION" : 3.0, "ED_STR" : "High School" }, \
{"EDUCATION" : 4.0, "ED_STR" : "Others"}] 
eduDf = spark.createDataFrame(pd.DataFrame(eduDict, \
columns=['EDUCATION', 'ED_STR']))
eduDf.collect()
ccDf2 = ccDf1.join( eduDf, ccDf1.EDUCATION== eduDf.EDUCATION ).drop(eduDf.EDUCATION)
ccDf2.take(5)






# adding columns with names for type of status i.e married or single.
marrDict = [{"MARRIAGE" : 1.0, "MARR_DESC" : "Single"}, \
{"MARRIAGE" : 2.0, "MARR_DESC" : "Married"}, \
{"MARRIAGE" : 3.0, "MARR_DESC" : "Others"}] 
marrDf = spark.createDataFrame(pd.DataFrame(marrDict, \
columns=['MARRIAGE', 'MARR_DESC']))
marrDf.collect()
ccFinalDf = ccDf2.join( marrDf, ccDf2.MARRIAGE== marrDf.MARRIAGE ).drop(marrDf.MARRIAGE)
ccFinalDf.cache()
ccFinalDf.take(5)





#Creating a temporary df
ccFinalDf.createOrReplaceTempView("CCDATA")


spark.sql("SELECT SEX_NAME, count(*) as Total, " + \
" SUM(DEFAULTED) as Defaults, " + \
" ROUND(SUM(DEFAULTED) * 100 / count(*)) as PER_DEFAULT " + \
"FROM CCDATA GROUP BY SEX_NAME" ).show()
ccLp = ccFinalDf.rdd.repartition(2).map(transformToLabeledPoint)
ccLp.collect()
ccNormDf = spark.createDataFrame(ccLp,["label", "features"])
ccNormDf.select("label","features").show(10)
ccNormDf.cache()




spark.sql("SELECT MARR_DESC, ED_STR, count(*) as Total," + \
" SUM(DEFAULTED) as Defaults, " + \
" ROUND(SUM(DEFAULTED) * 100 / count(*)) as PER_DEFAULT " + \
"FROM CCDATA GROUP BY MARR_DESC,ED_STR " + \
"ORDER BY 1,2").show()
spark.sql("SELECT AVG_PAY_DUR, count(*) as Total, " + \
" SUM(DEFAULTED) as Defaults, " + \
" ROUND(SUM(DEFAULTED) * 100 / count(*)) as PER_DEFAULT " + \
"FROM CCDATA GROUP BY AVG_PAY_DUR ORDER BY 1" ).show() 
#Correlation analysis
for i in ccDf.columns:
if not( isinstance(ccDf.select(i).take(1)[0][0], str)) :
print( "Correlation to DEFAULTED for ", i,\
ccDf.stat.corr('DEFAULTED',i))
from pyspark.ml.feature import StringIndexer
stringIndexer = StringIndexer(inputCol="label", outputCol="indexed")
si_model = stringIndexer.fit(ccNormDf)
td = si_model.transform(ccNormDf)
td.collect()

#Split into training and testing data
(trainingData, testData) = td.randomSplit([0.7, 0.3])
trainingData.count()
testData.count()
from pyspark.ml.classification import RandomForestClassifier
from pyspark.ml.classification import DecisionTreeClassifier
from pyspark.ml.classification import NaiveBayes, NaiveBayesModel
from pyspark.ml.evaluation import MulticlassClassificationEvaluator

evaluator = MulticlassClassificationEvaluator(predictionCol="prediction", \
labelCol="indexed",metricName="accuracy")

#Creating the Decision Trees model
dtClassifer = DecisionTreeClassifier(labelCol="indexed", \
featuresCol="features")
dtModel = dtClassifer.fit(trainingData)
#Predicting on the test data
predictions = dtModel.transform(testData)
predictions.select("prediction","indexed","label","features").collect()
print("Results of Decision Trees : ",evaluator.evaluate(predictions))
#Create the Random Forest model
rmClassifer = RandomForestClassifier(labelCol="indexed", \
featuresCol="features")
rmModel = rmClassifer.fit(trainingData)
#Predict on the test data
predictions = rmModel.transform(testData)
predictions.select("prediction","indexed","label","features").collect()
print("Results of Random Forest : ",evaluator.evaluate(predictions) )

#Create the Naive Bayes model
nbClassifer = NaiveBayes(labelCol="indexed", \
featuresCol="features")
nbModel = nbClassifer.fit(trainingData)
#Predict on the test data
predictions = nbModel.transform(testData)
predictions.select("prediction","indexed","label","features").collect()
print("Results of Naive Bayes : ",evaluator.evaluate(predictions) )
#Creating a Spark Data Frame with the features
ccFClustDf = spark.createDataFrame(ccMap)
ccFClustDf.cache()

ccFClustDf.select("features").show(10)

#Performing clustering
from pyspark.ml.clustering import KMeans
kmeans = KMeans(k=4, seed=1)
model = kmeans.fit(ccFClustDf)
predictions = model.transform(ccFClustDf)
predictions.select("*").show()

