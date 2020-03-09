import pandas as pd
import numpy as np
df=pd.read_excel('//officechihome32.office.adroot.bmogc.net/UserData32$/skatkar/Desktop/KPI report/0306_KPIDashboard_Jan.xlsm',sheet_name = 'TOH Customer by Month')
df2=pd.read_excel('//officechihome32.office.adroot.bmogc.net/UserData32$/skatkar/Desktop/KPI report/0306_KPIDashboard_Jan.xlsm',sheet_name = 'Consumer Customer by Month')
df3=pd.read_excel('//officechihome32.office.adroot.bmogc.net/UserData32$/skatkar/Desktop/KPI report/0306_KPIDashboard_Jan.xlsm',sheet_name = 'Consumer Acq & Attr & Net')
df4=pd.read_excel('//officechihome32.office.adroot.bmogc.net/UserData32$/skatkar/Desktop/KPI report/0306_KPIDashboard_Jan.xlsm',sheet_name = 'Small Business Customer by Mont')
df5=pd.read_excel('//officechihome32.office.adroot.bmogc.net/UserData32$/skatkar/Desktop/KPI report/0306_KPIDashboard_Jan.xlsm',sheet_name = 'IndirectAAN')
df6=pd.read_excel('//officechihome32.office.adroot.bmogc.net/UserData32$/skatkar/Desktop/KPI report/0306_KPIDashboard_Jan.xlsm',sheet_name = 'TOH Acq & Attr & Net')
df7=pd.read_excel('//officechihome32.office.adroot.bmogc.net/UserData32$/skatkar/Desktop/KPI report/0306_KPIDashboard_Jan.xlsm',sheet_name = 'Small Business Acq & Attr & Net')
df8=pd.read_excel('//officechihome32.office.adroot.bmogc.net/UserData32$/skatkar/Desktop/KPI report/0306_KPIDashboard_Jan.xlsm',sheet_name = 'Customer # by Product Group')
import pandas as pd
import numpy as np
df3=pd.read_excel('//officechihome32.office.adroot.bmogc.net/UserData32$/skatkar/Desktop/KPI report/0306_KPIDashboard_Jan.xlsm',sheet_name = 'Consumer Acq & Attr & Net')
a=pd.melt(df3, id_vars =['YEAR', 'MONTH'], value_vars =['ACQUISITION', 'ATTRITION', 'NET'])
df2=pd.read_excel('//officechihome32.office.adroot.bmogc.net/UserData32$/skatkar/Desktop/KPI report/0306_KPIDashboard_Jan.xlsm',sheet_name = 'Consumer Customer by Month')
df9=pd.read_excel('//officechihome32.office.adroot.bmogc.net/UserData32$/skatkar/Desktop/KPI report/0306_KPIDashboard_Jan.xlsm',sheet_name = 'CustGoals')
merge_cust_test=pd.merge(df2,df3 , left_on=['YEAR','MONTH'], right_on=['YEAR','MONTH'])
merge_cust_test.columns
merge_cust_test = merge_cust_test[['DataDate_x', 'YEAR', 'MONTH', 'TOTAL # OF CUSTOMER', 'ACQUISITION', 'ATTRITION', 'NET']]
merge_cust_test=pd.melt(merge_cust_test, id_vars =['DataDate_x','YEAR', 'MONTH'], value_vars =['TOTAL # OF CUSTOMER', 'ACQUISITION', 'ATTRITION', 'NET'])
df9.columns
df9=df9.dropna(how='any')
test=df9.loc[df9['Type'] == 'Acq', 'Type'] = 'ACQUISITION'
test2=df9.loc[df9['Type'] == 'NetNew', 'Type'] = 'NET'
test3=df9.loc[df9['Type'] == 'Att', 'Type'] = 'ATTRITION'
merge_cust_test2=pd.merge(merge_cust_test,df9 , left_on=['YEAR','MONTH','variable'], right_on=['YEAR','MONTH', 'Type'])
merge_cust_test2=pd.merge(merge_cust_test,df9 , left_on=['YEAR','MONTH','variable'], right_on=['YEAR','MONTH', 'Type'], how='left')
merge_cust_test2['PPA'] = merge_cust_test2.groupby([merge_cust_test2['DataDate_x'].dt.month])['value'].shift()
merge_cust_test2.columns
merge_cust_test2 = merge_cust_test2[['DataDate_x', 'YEAR', 'MONTH', 'variable', 'value', 'Goal', 'PPA']]
merge_cust_test2.columns = ['DataDate_x', 'YEAR', 'MONTH', 'Metric', 'value', 'Goal', 'PPA']
merge_cust_test2['Label']='Retail'
merge_cust_test2.info()
merge_cust_test2['DataDate_x'] = pd.to_datetime(merge_cust_test2['DataDate_x'])
merge_cust_test2['DataDate_x'] = merge_cust_test2['DataDate_x'].dt.date
#######################################################################
df3 = df3[['DataDate', 'YEAR', 'MONTH', 'NET']]
df5 = df5[['DataDate', 'YEAR', 'MONTH', 'NET']]
df7 = df7[['DataDate', 'YEAR', 'MONTH', 'NET']]
df6 = df6[['DataDate', 'YEAR', 'MONTH', 'NET']]
df3.columns = ['DataDate', 'YEAR', 'MONTH', 'Consumer Net New']
df5.columns = ['DataDate', 'YEAR', 'MONTH', 'Indirect Net New']
df7.columns = ['DataDate', 'YEAR', 'MONTH', 'Business Net New']
df6.columns = ['DataDate', 'YEAR', 'MONTH', 'Total Net New']
merge_net_test=pd.merge(df3,df5 , left_on=['YEAR','MONTH'], right_on=['YEAR','MONTH'], how='left')

merge_net_test_a=pd.merge(merge_net_test, df7, left_on=['YEAR','MONTH'], right_on=['YEAR','MONTH'], how='left')

merge_net_test_b=pd.merge(merge_net_test_a, df6, left_on=['YEAR','MONTH'], right_on=['YEAR','MONTH'], how='left')
merge_net_test_b = merge_net_test_b[['DataDate_x', 'YEAR', 'MONTH', 'Consumer Net New',
       'Indirect Net New', 'Business Net New', 'Total Net New']]
merge_net_test_c=pd.melt(merge_net_test_b, id_vars =['YEAR', 'MONTH'], value_vars =['Consumer Net New', 'Indirect Net New', 'Business Net New','Total Net New'])
merge_net_test_c['Day']=1
merge_net_test_c['Date'] = pd.to_datetime(merge_net_test_c[['YEAR','MONTH','Day']])
merge_net_test_c.columns
merge_net_test_c = merge_net_test_c[['Date','YEAR', 'MONTH', 'variable', 'value']]
################################################################
df9_1=df9
test5=df9_1.loc[df9_1['Type'] == 'NET', 'Type'] = 'Consumer Net New'
merge_net_test_c=pd.merge(merge_net_test_c,df9_1 , left_on=['YEAR','MONTH','variable'], right_on=['YEAR','MONTH', 'Type'], how='left')
merge_net_test_c.columns
merge_net_test_c = merge_net_test_c[['Date', 'YEAR', 'MONTH', 'variable', 'value','Goal']]
##################################################################
merge_net_test_c['PPA'] = merge_net_test_c.groupby([merge_net_test_c['Date'].dt.month])['value'].shift()
merge_net_test_c.to_excel('KPI_Customer_Net_ver1.xlsx')
merge_cust_test2.to_excel('KPI_CustomerAAN.xlsx')
