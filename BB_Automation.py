from selenium import webdriver
from selenium.webdriver import Chrome
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

import win32com.client as win32
import time
import json
import pandas as pd
import pyodbc
from datetime import datetime,timedelta
import ctypes
import sys
import os
import calendar

st_time= datetime.now()
print (st_time)

#change to local path
source_path="C:\\Users\\asimo04\\Downloads\\BB\\BB_files\\Final_Run\\"
file_sourcepath="C:/Users/asimo04/Downloads/BB/BB_files/Final_Run/"
unpswd_file="credentials.txt"

try:
    with open(source_path+unpswd_file) as f:
        try:
            cd=json.load(f)
            username = cd['username']
            password = cd['password']
        except ValueError:
            ctypes.windll.user32.MessageBoxA(0, unpswd_file+" "+"File is Empty", "Error!", 1)
            print ("File Empty")
            sys.exit(1)
except IOError:
    ctypes.windll.user32.MessageBoxA(0, unpswd_file+"-"+"Check File name", "Error!", 1)
    print ("Please check credentials file name")
    sys.exit(1)
	
def sendemail(content, to, subject):
    outlook = win32.Dispatch('outlook.application')
    ns = outlook.GetNameSpace("MAPI")
    mail = outlook.CreateItem(0)
    mail.To = to
    mail.Subject = subject
    mail.body = '*THIS IS AN AUTOMATED EMAIL*\n\n'+ 'Hi,\n\n' + content + '\n'+'\n \n \n Thanks and Regards \n' + str(ns.CurrentUser)
    mail.send
	
def upload_job(source_path,upload_file,job_name):
    actionChains = ActionChains(dm)
    dm.implicitly_wait(20)
    #actionChains.double_click(dm.find_element_by_xpath("//*[@id='"+job_name+"_upl']/span[2]")).perform()
    actionChains.double_click(WebDriverWait(dm, 60).until(EC.presence_of_element_located((By.XPATH,"//*[@id='"+job_name+"_upl']/span[2]")))).perform()
    dm.find_element_by_xpath("//input[@id='multipartFile']").send_keys(source_path+upload_file+".xlsx")
    time.sleep(1)
    dm.find_element_by_xpath("//button[text()='Next']").click()
    dm.implicitly_wait(60)
    time.sleep(1)
    dm.find_element_by_xpath("//button[text()='Next']").click()
    time.sleep(5)
    #dm.find_element_by_xpath("//button[text()='Rescan Schema']").click()
    #time.sleep(5)
    dm.find_element_by_xpath("//button[text()='Next']").click()
    time.sleep(1)
    dm.find_element_by_xpath("//button[text()='Next']").click()
    time.sleep(1)
    dm.find_element_by_xpath("//button[text()='Save']").click()
    time.sleep(10)
	
def import_job(job):
    WebDriverWait(dm, 60).until(EC.presence_of_element_located((By.XPATH,"//*[@id='"+job+"_imp']"))).click()
    time.sleep(1)
    dm.find_element_by_xpath("//label[@tip='Run (&nbsp;Alt C&nbsp;)']").click()
    time.sleep(5)    

def goals_product_dimension(database,hive_conn):
    gph_query = 'select prod_no,prod_lvl_5,prod_lvl_6 FROM '+database+'.stg_product_hierarchy;'
    goals_product_hierarchy =pd.read_sql(gph_query,hive_conn)
    print ("gph",goals_product_hierarchy.shape)
    def apply_goals_prod_key(row):
        if row['prod_lvl_5']=='Business DDA':
            return 1
        elif row['prod_lvl_5'] in ('Referred Merchant Services','PayChex','SurePayroll Services'):
            return 2
        elif row['prod_lvl_5'] in ('Business Money Market','Business Savings','CDs / IRAs','CDs / IRAs'):
            return 3    
        elif row['prod_lvl_5']=='Business Credit Card':
            return 4
        elif row['prod_lvl_5']=='Business Loan':
            return 5
        elif row['prod_lvl_5']=='SRC':
            return 6
        elif row['prod_lvl_5']=='Other Products':
            if row['prod_lvl_6'] in ('Other:  Cash Management','OLBB/ACH','Wire Module (OLBB)','Remote Deposit Capture'):
                return 2
            else:
                return 9999
        else:
            return 9999
    #create Plan_Product_Key 
    goals_product_hierarchy['goals_product_key']=goals_product_hierarchy.apply(apply_goals_prod_key,axis=1)
    goals_product_hierarchy.drop('prod_lvl_6',1,inplace=True)    
    goals_product_hierarchy.to_excel("Goals_Product.xlsx",index=False)

def product_hierarchy_dimension(database,hive_conn):
    #Product Dimension
    ph_query="select prod_no,prod_lvl_1,prod_lvl_2,prod_lvl_3,prod_lvl_4,prod_lvl_5,prod_lvl_6 from "+database+".stg_product_hierarchy;"
    gph_query="select * from "+database+".dw_goals_product_dimension;"
    product_hierarchy=pd.read_sql(ph_query,hive_conn)
    print ("ph",product_hierarchy.shape)
    goals_product_hierarchy=pd.read_sql(gph_query,hive_conn)
    print ("gph",goals_product_hierarchy.shape)
    #create Product_ID surrogate key
    product_hierarchy['product_id']=product_hierarchy.index+1
    ph_join1=product_hierarchy.merge(goals_product_hierarchy,how='inner',on=['prod_no','prod_lvl_5'])
    print ("ph_join1",ph_join1.shape)
    ph_join1.to_excel('Product_Hierarchy.xlsx', index=False)
	
def date_dimension(database,hive_conn):
    wt_query="select * from "+database+".stg_week_table"
    wt_df=pd.read_sql(wt_query,hive_conn)
    #create "DATE_ID" to use as surrogate Key
    wt_df['date_id']=wt_df.index+1
    wt_df['year_end_date']='31/10/2019'
    def convert_to_friday(row):
        return row-timedelta(days=1)
            
    wt_df['week_ending_date']=wt_df['week_ending_date'].apply(convert_to_friday)
    wt_df.to_excel('Date_Dimension.xlsx', index=False)
	
#brm_hierarchy_dimension
def brm_hierarchy_dimension(database,hive_conn):
    empmstr_query="select idp_data_date,bmo_ein,spfullname,buc_no,plancode,status_conv_rate,ramp_pct from "+database+".stg_empmstr_hist_by_week where plancode in ('Q','ZQ','R','ZR') and idp_data_date>'2018-11-01';"
    empmstr=pd.read_sql(empmstr_query,hive_conn)

    bbgoals_query="select role,quarter,product,quarterly_goal from "+database+".stg_bb_goals"
    bbgoals_df=pd.read_sql(bbgoals_query,hive_conn)

    bbgoals_df.drop(bbgoals_df.loc[bbgoals_df['product']!='SRC'].index,inplace=True)
    bbgoals_df.rename(columns={'quarterly_goal':'src_points_standard_qtrly_goal'},inplace=True)
    bbgoals_df.drop(['product'],1,inplace=True)
    
    brmhrcy_query="select buc_ as buc_no,brm_region from "+database+".stg_brm_hierarchy"
    brm_df=pd.read_sql(brmhrcy_query,hive_conn)

    #empmstr['BUC_NO']=empmstr['BUC_NO'].astype(int)
    brm_join2=empmstr.merge(brm_df,how='inner',on='buc_no')
    print ("brm_join2", brm_join2.shape)

    def role_fn(row):
        if (row['plancode'] in ('Q','ZQ') and str(row['buc_no'])=='70161'):
            return 'Remote BRM'
        elif row['plancode'] in ('Q','ZQ'):
            return 'Field BRM'
        elif str(row['bmo_ein']) in ('300019967','300007448') and row['plancode'] in ('R','ZR'):
            return 'ADA BRM'
        elif str(row['bmo_ein']) in ('100723184','100757966') and row['plancode'] in ('R','ZR'):
            return 'AG BRM'
        else:
            return ''
    brm_join2['role']=brm_join2.apply(role_fn,axis=1)

    def brm_region(row):
        if row['role']=='AG BRM':
            return 'AG'
        elif row['role']=='ADA BRM':
            return 'ADA'
        else:
            return row['brm_region']

    brm_join2['brm_region']=brm_join2.apply(brm_region,axis=1)

    def toh(row):
        if row['role'] in ('Field BRM', 'Remote BRM'):
            return 'BRM TOH Goal'
        elif row['role'] in ('ADA BRM', 'AG BRM'):
            return 'BRM TOH Non-Goal'

    brm_join2['toh']=brm_join2.apply(toh,axis=1)

    brm_join2.drop('buc_no',1,inplace=True)

        
    def idp_date_to_weekend(row):
        #convert week_ending_date to friday
        if row.weekday()>=5:
            return row+timedelta(days=11-row.weekday())
        else:
            return row+timedelta(days=4-row.weekday())


    brm_join2['idp_data_date']=brm_join2['idp_data_date'].apply(idp_date_to_weekend)

    def create_quarter_for_src(row):
        qtr_dict={1:[11,12,1],2:[2,3,4],3:[5,6,7],4:[8,9,10]}
        k=[x for x,y in qtr_dict.iteritems() if row.month in y]
        return k[0]

    brm_join2['quarter']=brm_join2['idp_data_date'].apply(create_quarter_for_src)

    def create_ein_date_key(row):
        return str(row['idp_data_date'].date())+' '+str(row['bmo_ein'])

    brm_join2['ein_date_key']=brm_join2.apply(create_ein_date_key,axis=1)

    brm_join2.rename(columns={'idp_data_date':'week_ending_date'},inplace=True)

    print ("brm_join2",brm_join2.shape)

    brm_join3=brm_join2.merge(bbgoals_df, how='left', on =['quarter','role'])

    brm_join3['src_points_standard_qtrly_goal'].fillna(0,inplace=True)
    brm_join3['src_points_adj_weekly_goal']=(brm_join3['src_points_standard_qtrly_goal']*brm_join3['status_conv_rate']*brm_join3['ramp_pct']/13).round(5)
    brm_join3['src_points_adj_monthly_goal']=(brm_join3['src_points_standard_qtrly_goal']*brm_join3['status_conv_rate']*brm_join3['ramp_pct']/3).round(5)
    
    #create adjusted quarterly goal
    brm_temp_df=brm_join3[['bmo_ein','week_ending_date','quarter','src_points_adj_monthly_goal']].copy()
    
    def month_to_qtr(row):
        return row.month
    brm_temp_df['month']=brm_temp_df['week_ending_date'].apply(month_to_qtr)
    brm_temp_df.drop_duplicates(['bmo_ein','month','src_points_adj_monthly_goal'],inplace=True)
    brm_temp1=brm_temp_df.pivot_table(index=['bmo_ein','quarter'],values='src_points_adj_monthly_goal',aggfunc=sum)
    brm_temp1.rename(columns={'src_points_adj_monthly_goal':'src_points_adj_qtrly_goal'},inplace=True)
    
    brm_join3a=brm_join3.merge(brm_temp1,how='left', on=['bmo_ein','quarter'])
    
    brm_join3a.drop(['quarter','status_conv_rate','ramp_pct'],1,inplace=True)

    print ("brm_join3",brm_join3a.shape)
    brm_join3a['brm_hierarchy_id']=brm_join3a.index+1
    brm_join3a['src_count']=1

    rearrange_cols=['brm_hierarchy_id','ein_date_key','week_ending_date','bmo_ein','spfullname','plancode',
                    'brm_region','role','toh','src_points_adj_weekly_goal',
                    'src_points_adj_monthly_goal','src_points_adj_qtrly_goal','src_points_standard_qtrly_goal',
                   'src_count']

    brm_join3a=brm_join3a[rearrange_cols]

    brm_join3a.to_excel('BRM_Hierarchy_Dimension.xlsx',index=False)
	
def actuals_fact(database,hive_conn):    
    prod_hierarchy_query="select prod_no,product_id,goals_product_key from "+database+".dw_product_hierarchy_dimension;"
    prod_hierarchy = pd.read_sql(prod_hierarchy_query,hive_conn)
    brm_dim_query="select ein_date_key,brm_hierarchy_id from "+database+".dw_brm_hierarchy_dimension;"
    brm_df=pd.read_sql(brm_dim_query,hive_conn)
    bmo_br_mkt_query="select sp_br_no as credited_branch,sp_mkt as credited_market,sp_rgn as credited_region from "+database+".stg_bmo_codes;"
    bmo_br_mkt_df=pd.read_sql(bmo_br_mkt_query,hive_conn)
    print (bmo_br_mkt_df.columns)
    
    emp_names="select distinct bmo_ein,spfullname,sf_role from "+database+".stg_empmstr_hist_by_week where idp_data_date>'2018-11-01';"
    emp_names_df=pd.read_sql(emp_names,hive_conn)
    print (emp_names_df.shape)
    emp_names_df.drop_duplicates('bmo_ein',keep='last',inplace=True)
    print ("emp_dropped",emp_names_df.shape)
    
    data_load_timestamps_query="select a.data_load_ts from \
                                (select max(data_load_ts) as data_load_ts, month(opendate) from "+database+".stg_cumulative_hdp \
                                where (month(opendate) in (01,02,03,04,05,06,07,08,09,10) and year(opendate)=2019) \
                                or (month(opendate) in (11,12) and year(opendate)=2018) \
                                group by month(opendate)) a;"
    
    data_load_timestamps=pd.read_sql(data_load_timestamps_query,hive_conn)
    print (data_load_timestamps)
    data_load_timestamps.drop_duplicates(inplace=True)
    print (data_load_timestamps)
    dataloadts_list=list(data_load_timestamps['data_load_ts'].astype(str))

    hdp_prim_query="select data_load_ts,adj_acct_nbr,customer_n,opendate,credited_branch,credited_branch_name,\
                       adj_empid as primref_empid,finadjrefemp as primref_empid_2, \
                       adj_empid as name_1,finadjrefemp as name_2, \
                       essprimplan as primref_plan,src_prim_indicator as src_primref_indicator,\
                       prod_no,xps_code,prod_code,category,cd_indica,xpsbal1,adj_total_dlr,\
                       sales_count,ess_week,primemp as primref_emp,loanutili,total_prim_src as total_primref_src,\
                       capped_xps_bal,capped_adj_total,newcustindc,fymonth_nbr,account,\
                       xpsbal2,capped_xps_bal2,prod_dlr_br2,prod_dlr_br_fullheli2,prod_dlr_br_uncapped2,\
                       prod_dlr_br_uncapped_fullheli2,prod_dlr_br_fullloan_dlr,prod_dlr_br_uncapfullloan_dlr,srctoagg \
                       from "+database+".stg_cumulative_hdp\
                       where essprimplan in ('Q','ZQ','R','ZR')\
                       and string(data_load_ts) in ("+','.join("'" + ts + "'" for ts in dataloadts_list)+");"

    hdp_prim=pd.read_sql(hdp_prim_query,hive_conn)
    hdp_prim['src_primref_y_n_indicator']='Y'
    print ("hdp1", hdp_prim.shape)

    hdp_ref_query="SELECT data_load_ts,adj_acct_nbr,customer_n,opendate,credited_branch,credited_branch_name,\
                       finadjrefemp as primref_empid,adj_empid as primref_empid_2, \
                       adj_empid as name_1,finadjrefemp as name_2,essrefplan as primref_plan,\
                       src_ref_final_indicator as src_primref_indicator,\
                       prod_no,xps_code,prod_code,category,cd_indica,xpsbal1,adj_total_dlr,\
                       sales_count,ess_week,refemp as primref_emp,loanutili,total_ref_src as total_primref_src,\
                       capped_xps_bal,capped_adj_total,newcustindc,fymonth_nbr,account,\
                       xpsbal2,capped_xps_bal2,prod_dlr_br2,prod_dlr_br_fullheli2,prod_dlr_br_uncapped2,\
                       prod_dlr_br_uncapped_fullheli2,prod_dlr_br_fullloan_dlr,prod_dlr_br_uncapfullloan_dlr,srctoagg \
                       from "+database+".stg_cumulative_hdp\
                       where essrefplan in ('Q','ZQ','R','ZR')\
                       and string(data_load_ts) in ("+','.join("'" + ts + "'" for ts in dataloadts_list)+");"

    hdp_ref=pd.read_sql(hdp_ref_query,hive_conn)
    hdp_ref['src_primref_y_n_indicator']='N'
    hdp_ref['sales_count']=0

    print ("hdp2", hdp_ref.shape)

    actuals_fact=pd.concat([hdp_prim,hdp_ref],ignore_index=True,sort=False)

    print ("af", actuals_fact.shape)

    actuals_fact['name_1']=pd.to_numeric(actuals_fact['name_1'],errors='coerce')
    actuals_fact['name_2']=pd.to_numeric(actuals_fact['name_2'],errors='coerce')
    actuals_fact['primref_empid_2']=pd.to_numeric(actuals_fact['primref_empid_2'],errors='coerce')

    def opendate_to_weekend(row):
        #convert week_end_date to Friday
        if row.weekday()>=5:
            return row+timedelta(days=11-row.weekday())
        else:
            return row+timedelta(days=4-row.weekday())

    actuals_fact['opendate_weekend']=actuals_fact['opendate'].apply(opendate_to_weekend)
    
    def create_mtd_date(row):
        if (row['opendate'].month == row['opendate_weekend'].month):
            return row['opendate_weekend']
        else:
            return (row['opendate_weekend'].replace(day=1)-timedelta(days=1))

    actuals_fact['opendate_mtd']=actuals_fact.apply(create_mtd_date,axis=1)

    def create_ein_date_key(row):
        return str(row['opendate_weekend'].date())+' '+str(row['primref_empid'])

    actuals_fact['ein_date_key']=actuals_fact.apply(create_ein_date_key,axis=1)
     
    af_join1=actuals_fact.merge(prod_hierarchy,how='inner',on='prod_no')
    print ("af_join1",af_join1.shape)

    af_join2=af_join1.merge(brm_df, how='left', on='ein_date_key')

    print ("af_join2",af_join2.shape)
    
    #count no of duplicates
    dup_rows= pd.DataFrame(af_join2.pivot_table(index=['ein_date_key','goals_product_key'],aggfunc='size'))
    dup_rows.rename(columns={0:'num_of_trans'},inplace=True)
    
    def create_no_of_days(row):
        start_date=row['opendate_weekend']-timedelta(days=6)
        if start_date.month==row['opendate_weekend'].month:
            return 7
        else:
            if row['opendate'].month<row['opendate_weekend'].month:
                return (row['opendate_weekend'].replace(day=1)-start_date).days
            else:
                return (row['opendate_weekend']-(row['opendate_weekend'].replace(day=1)-timedelta(days=1))).days
                
    af_join2['no_of_days']=af_join2.apply(create_no_of_days,axis=1)

    af_join3=af_join2.merge(dup_rows, how='inner', on=['ein_date_key','goals_product_key'])
    print (af_join3.shape)
    
    af_join4=af_join3.merge(bmo_br_mkt_df, how='left', on='credited_branch')
    print ("join4",af_join4.shape)
    
    emp_names_df['bmo_ein']=pd.to_numeric(emp_names_df['bmo_ein'],errors='coerce')
    
    af_join5=af_join4.merge(emp_names_df,how='left',left_on='name_1', right_on='bmo_ein')
    af_join5.drop(['bmo_ein','name_1'],1,inplace=True)
    af_join5.rename(columns={'sf_role':'role_1','spfullname':'primary_name'},inplace=True)
    print (af_join5.shape)
    
    af_join6=af_join5.merge(emp_names_df,how='left', left_on='name_2',right_on='bmo_ein')
    af_join6.drop(['bmo_ein','name_2','sf_role'],1,inplace=True)
    af_join6.rename(columns={'spfullname':'referring_name'},inplace=True)
    print (af_join6.shape)
    
    af_join7=af_join6.merge(emp_names_df,how='left', left_on='primref_empid_2',right_on='bmo_ein')
    af_join7.drop(['bmo_ein','spfullname'],1,inplace=True)
    af_join7.rename(columns={'sf_role':'role_2'},inplace=True)
    print (af_join7.shape)

    rearrange_cols=['product_id','goals_product_key','brm_hierarchy_id','ein_date_key','data_load_ts','adj_acct_nbr',
                    'customer_n','opendate','opendate_weekend','opendate_mtd',
                    'credited_branch','credited_branch_name','credited_market','credited_region',
                    'primref_empid','primref_empid_2','primref_plan','src_primref_indicator',
                    'prod_no','xps_code','prod_code','category','cd_indica','xpsbal1','adj_total_dlr','sales_count',
                    'ess_week','primref_emp','loanutili','total_primref_src','src_primref_y_n_indicator',
                    'capped_xps_bal','capped_adj_total','newcustindc','fymonth_nbr',
                    'account','xpsbal2','capped_xps_bal2','prod_dlr_br2',
                    'prod_dlr_br_fullheli2','prod_dlr_br_uncapped2','prod_dlr_br_uncapped_fullheli2',
                    'prod_dlr_br_fullloan_dlr','prod_dlr_br_uncapfullloan_dlr','srctoagg','primary_name','referring_name',
                    'role_1','role_2','num_of_trans','no_of_days']

    af_join7=af_join7[rearrange_cols]

    af_join7.to_excel('Actuals_Fact.xlsx', index=False)
	
def goals_fact(database,hive_conn):
    gdf_query="select role,quarter,product,goal_type,quarterly_goal from "+database+".stg_bb_goals;"
    gdf=pd.read_sql(gdf_query,hive_conn)

    gdf.drop(gdf.loc[gdf['product']=='SRC'].index, inplace=True)
    gdf1=gdf.pivot_table(index=['quarter','role','product'],columns='goal_type',values='quarterly_goal')
    gdf1.columns=[x.lower()+'_standard_qtrly_goal' for x in gdf1.columns]
        
    #==============================================================================================================================
    empmstr_query="select idp_data_date,bmo_ein,plancode,buc_no,status_conv_rate,ramp_pct \
                    from "+database+".stg_empmstr_hist_by_week \
                    where plancode in ('Q','ZQ','R','ZR') and idp_data_date>'2018-11-01';"
    #==============================================================================================================================
    empmstr_df=pd.read_sql(empmstr_query,hive_conn)
    #empmstr_df.drop_duplicates(subset='bmo_ein',inplace=True)
    empmstr_df['key']=0

    print (empmstr_df.shape)

    def role_fn(row):
        if (row['plancode'] in ('Q','ZQ') and str(row['buc_no'])=='70161'):
            return 'Remote BRM'
        elif row['plancode'] in ('Q','ZQ'):
            return 'Field BRM'
        elif str(row['bmo_ein']) in ('300019967','300007448') and row['plancode'] in ('R','ZR'):
            return 'ADA BRM'
        elif str(row['bmo_ein']) in ('100723184','100757966') and row['plancode'] in ('R','ZR'):
            return 'AG BRM'
        else:
            return ''
    empmstr_df['role']=empmstr_df.apply(role_fn,axis=1)

    wt_query="select week_ending_date,quarter from "+database+".stg_week_table;"
    date_dim_df=pd.read_sql(wt_query,hive_conn)
    
    def convert_to_friday(row):
        #convert weekend date from saturday to friday
        return row-timedelta(days=1)
    date_dim_df['week_ending_date']=date_dim_df['week_ending_date'].apply(convert_to_friday)
    #date_dim_df['key']=0

    bbgoals_query="select product as goal_category from "+database+".stg_bb_goals;"
    bbgoals_df=pd.read_sql(bbgoals_query,hive_conn)
    bbgoals_df.drop(bbgoals_df.loc[bbgoals_df['goal_category']=='SRC'].index, inplace=True)
    bbgoals_df.drop_duplicates(inplace=True)
    bbgoals_df['key']=0
    
    gf_join1=empmstr_df.merge(bbgoals_df, how='left', on='key')
    print ("gf_join1", gf_join1.shape)
    
    gf_join2=gf_join1.merge(date_dim_df, how='left', left_on='idp_data_date',right_on='week_ending_date')
    #gf_join2=gf_join1.merge(date_dim_df, how='left', on='key')
    print ("gf_join2", gf_join2.shape)

    def no_of_weeks():
        today=pd.Timestamp.today()
        perf_week = today - timedelta(days=today.weekday()+3)
        return pd.Timestamp.date(perf_week)

    dfIndex=gf_join2[(gf_join2['week_ending_date']>no_of_weeks())].index

    gf_join2.drop(dfIndex,inplace=True)

    gf_join3=gf_join2.merge(gdf1,how='left', left_on=['goal_category','quarter','role'], right_on=['product','quarter','role'])
    print ("gf_join3", gf_join3.shape)

    def stdqtrgoal(row):
        if pd.np.isnan(row):
            return 0
        else:
            return row

    goal_cols=[x.lower() for x in gdf['goal_type'].drop_duplicates()]

    #Derive the calculated columns based on "Standard Qtrly Goal" column
    for x in goal_cols:
        gf_join3[x+'_standard_qtrly_goal']=gf_join3[x+'_standard_qtrly_goal'].apply(stdqtrgoal)
    
    for x in goal_cols:
        gf_join3[x+'_adj_weekly_goal']=(gf_join3[x+'_standard_qtrly_goal']*gf_join3['status_conv_rate']*gf_join3['ramp_pct']/13).round(5)
        gf_join3[x+'_adj_monthly_goal']=(gf_join3[x+'_standard_qtrly_goal']*gf_join3['status_conv_rate']*gf_join3['ramp_pct']/3).round(5)
        
    #create adjusted quarterly goals
    temp_df_cols=[x for x in gf_join3.columns[gf_join3.columns.str.contains('monthly')]]
    temp_df=gf_join3[['bmo_ein','goal_category','week_ending_date','quarter']+[x for x in gf_join3.columns[gf_join3.columns.str.contains('monthly')]]].copy()
    def month_to_qtr(row):
        return row.month
    temp_df['month']=temp_df['week_ending_date'].apply(month_to_qtr)
    temp_df.drop_duplicates(['bmo_ein','goal_category','month']+temp_df_cols,inplace=True)
    temp1=temp_df.pivot_table(index=['bmo_ein','goal_category','quarter'],values=temp_df_cols,aggfunc=sum)
    colnames_dict={}
    for x in temp_df_cols:
        colnames_dict[x]=x.replace('monthly','qtrly')
    print (colnames_dict)
    temp1.rename(columns=colnames_dict,inplace=True)
        
    gf_join3a=gf_join3.merge(temp1,how='left',on=['bmo_ein','goal_category','quarter'])
    gf_join3a.drop(['idp_data_date','plancode','buc_no','key',
                   'status_conv_rate','ramp_pct','role','quarter'],1,inplace=True)

    print ("gf_join3-droppped", gf_join3a.shape)
    
    def create_ein_date_key(row):
        return str(row['week_ending_date'].date())+' '+str(row['bmo_ein'])

    gf_join3a['ein_date_key']=gf_join3a.apply(create_ein_date_key,axis=1)

    gf_join3a['product_id']=''
    gf_join3a['bmo_ein']=gf_join3a['bmo_ein'].astype(int)

    ################################
    #Joining Dimensions to Goals Fact
    ################################
    
    brm_dim_query="select ein_date_key,brm_hierarchy_id,plancode from "+database+".dw_brm_hierarchy_dimension;"
    brm_dim_df=pd.read_sql(brm_dim_query,hive_conn)
    pph_dim_query="select prod_lvl_5,goals_product_key from "+database+".dw_goals_product_dimension;"
    pph_dim_df=pd.read_sql(pph_dim_query,hive_conn)
    print (pph_dim_df.shape)
    pph_dim_df.drop_duplicates(inplace=True)
    print ("pph-dropped",pph_dim_df.shape)
    print ("gf_join3",gf_join3a.shape)
   
    gf_join5=gf_join3a.merge(brm_dim_df, how='inner', on='ein_date_key')
    print ("gf__join5",gf_join5.shape)
    gf_join6=gf_join5.merge(pph_dim_df, how='left', left_on='goal_category',right_on='prod_lvl_5')
    print ("gf_join6",gf_join6.shape)
    
    gf_join6.drop(gf_join6.loc[(gf_join6['goal_category']=='Other Products') & (gf_join6['goals_product_key']==2)].index,inplace=True)
    
    gf_join6.drop(['prod_lvl_5'],1,inplace=True)

    rearrange_cols=['product_id','brm_hierarchy_id','goals_product_key','ein_date_key','bmo_ein','goal_category',
                    'plancode','week_ending_date',
                    'units_adj_weekly_goal','units_adj_monthly_goal','units_adj_qtrly_goal',
                    'units_standard_qtrly_goal',
                    'net_new_dollar_adj_weekly_goal','net_new_dollar_adj_monthly_goal','net_new_dollar_adj_qtrly_goal',
                    'net_new_dollar_standard_qtrly_goal','commit_dollar_adj_weekly_goal','commit_dollar_adj_monthly_goal',
                    'commit_dollar_adj_qtrly_goal',
                    'commit_dollar_standard_qtrly_goal','util_dollar_adj_weekly_goal',
                    'util_dollar_adj_monthly_goal','util_dollar_adj_qtrly_goal',
                    'util_dollar_standard_qtrly_goal']

    gf_join6=gf_join6[rearrange_cols]

    gf_join6.to_excel('Goals_Fact.xlsx',index=False)
	
def goals_actuals_fact(database,hive_conn):
    actuals_query="select * from "+database+".dw_actuals_fact;"
    actuals=pd.read_sql(actuals_query,hive_conn)
    #actuals.drop('product_id',1,inplace=True)
    goals_query="select * from "+database+".dw_goals_fact;"
    goals=pd.read_sql(goals_query,hive_conn)
    #goals.drop('product_id',1,inplace=True)
    goals.drop(['product_id','brm_hierarchy_id'],1,inplace=True)
    brm_dimension_query="select ein_date_key,src_points_adj_weekly_goal,src_points_adj_monthly_goal, \
                         src_points_adj_qtrly_goal,brm_region,role \
                         from "+database+".dw_brm_hierarchy_dimension;"
    brm_dimension_df=pd.read_sql(brm_dimension_query,hive_conn)
    print (actuals.shape)
    print (goals.shape)
    ag_df=goals.merge(actuals, how='left', on =['ein_date_key','goals_product_key'])
    print (ag_df.shape)
    def fill_zero(row):
        if pd.np.isnan(row):
            return 0
        else:
            return row
    ag_df['sales_count']=ag_df['sales_count'].apply(fill_zero)
    ag_df['capped_xps_bal2']=ag_df['capped_xps_bal2'].apply(fill_zero)
    ag_df['xpsbal2']=ag_df['xpsbal2'].apply(fill_zero)
    goal_type=[x.split('_adj')[0] for x in ag_df.columns[ag_df.columns.str.contains('weekly')]]
    
    def get_mon_days(row):
        if str(row.month)=='2':
            if calendar.isleap(row.year):
                return 29
            else:
                return 28
        elif str(row.month) in ('4','6','9','11'):
            return 30
        else:
            return 31
        
    ag_df['mon_days']=ag_df['opendate'].apply(get_mon_days)
    
    def fill_opendate_mtd(row):
        if isinstance(row['opendate_mtd'],pd._libs.tslibs.nattype.NaTType):
            return row['week_ending_date']
        else:
            return row['opendate_mtd']
    ag_df['opendate_mtd']=ag_df.apply(fill_opendate_mtd,axis=1)
    
    for gtype in goal_type:
        ag_df[gtype+'_adj_weekly_goal_v2']=(ag_df[gtype+'_adj_weekly_goal']/ag_df['num_of_trans']).round(5)
        ag_df[gtype+'_adj_monthly_goal_v2']=((ag_df[gtype+'_adj_monthly_goal']/ag_df['mon_days'])*ag_df['no_of_days'])/ag_df['num_of_trans']
        
    
    ag_df1=ag_df.merge(brm_dimension_df,how='left',on='ein_date_key')
    print (ag_df1.shape)
    
    dup_ein_date_key_df= pd.DataFrame(ag_df1.pivot_table(index=['ein_date_key'],aggfunc='size'))
    dup_ein_date_key_df.rename(columns={0:'count_of_ein_date_key'},inplace=True)
    ag_df2=ag_df1.merge(dup_ein_date_key_df,how='inner', on='ein_date_key')
    ag_df2['src_points_adj_weekly_goal_v2']=(ag_df2['src_points_adj_weekly_goal']/ag_df2['count_of_ein_date_key']).round(5)
    ag_df2['src_points_adj_monthly_goal_v2']=((ag_df2['src_points_adj_monthly_goal']/ag_df2['mon_days'])*ag_df2['no_of_days'])/ag_df2['count_of_ein_date_key']
    
    def fill_goals(row):
        if 'goal_v2' in x:
            if pd.np.isnan(row[x]):
                if 'weekly' in str(x):
                    return row[x[:-3]]
            else:
                if row['plancode'] in ('ZQ','ZR') and row['sales_count']==1:
                    return 0
                else:
                    return row[x]
        else:
            if row['plancode'] in ('ZQ','ZR') and row['sales_count']==1:
                return 0
            else:
                return row[x]
        
    for x in ag_df2.columns[ag_df2.columns.str.contains('_goal')]:
        ag_df2[x]=ag_df2.apply(fill_goals,axis=1)
    
    #Remove "Z" in plancode and no sales activity
    ag_df2.drop(ag_df2.loc[((ag_df2['plancode']=='ZQ') | (ag_df2['plancode']=='ZR')) & (ag_df2['sales_count']==0)].index, inplace=True)
    ag_df2.drop('plancode',1,inplace=True)
        
    ag_df2.to_excel('Goals_Actuals_Fact.xlsx', index=False) 

def monthly_goals(database,hive_conn):
    goals_query="select bmo_ein,goal_category,week_ending_date,units_adj_monthly_goal, units_adj_qtrly_goal,\
                    net_new_dollar_adj_monthly_goal, net_new_dollar_adj_qtrly_goal, \
                    commit_dollar_adj_monthly_goal,commit_dollar_adj_qtrly_goal, \
                    util_dollar_adj_monthly_goal,util_dollar_adj_qtrly_goal, \
                    src_points_adj_monthly_goal,src_points_adj_qtrly_goal,brm_region,role \
                    from "+database+".dw_actuals_goals_fact;"
    
    goals_df=pd.read_sql(goals_query,hive_conn)
    
    emp_mstr_query="select distinct bmo_ein,spfullname \
                    from "+database+".stg_empmstr_hist_by_week \
                    where plancode in ('Q','ZQ','R','ZR') \
                    and idp_data_date>'2018-11-01';"
    
    emp_mstr_df=pd.read_sql(emp_mstr_query,hive_conn)
    emp_mstr_df['bmo_ein']=emp_mstr_df['bmo_ein'].astype('int64')
    print (emp_mstr_df.shape)
    emp_mstr_df.drop_duplicates('bmo_ein',keep='last',inplace=True)
    print (emp_mstr_df.shape)
    goals_v2_df=goals_df.merge(emp_mstr_df,how='left',on='bmo_ein')
    print (goals_v2_df.shape)
    def mon_to_remove_dups(row):
        return row.month
    
    goals_v2_df['months']=goals_v2_df['week_ending_date'].apply(mon_to_remove_dups)
    
    def qtr_to_remove_dups(row):
        qtr_dict={1:[11,12,1],2:[2,3,4],3:[5,6,7],4:[8,9,10]}
        k=[x for x,y in qtr_dict.iteritems() if row.month in y]
        return k[0]
    
    goals_v2_df['qtr']=goals_v2_df['week_ending_date'].apply(qtr_to_remove_dups)
    
    def divide_qtr_goals(row):        
        if 'src_points' in x:
            if 'qtrly' in x:
                return (row[x]/6)/3
            else:
                return row[x]/6
        elif 'qtrly' in x:
            return row[x]/3
        else:
            return row[x]
        
    #for x in goals_v2_df.columns[goals_v2_df.columns.str.contains('qtrly')]:
    for x in goals_v2_df.columns:
        goals_v2_df[x]=goals_v2_df.apply(divide_qtr_goals,axis=1)
    
    goals_v2_df.drop_duplicates(['bmo_ein','goal_category','brm_region','role','months','qtr'],inplace=True)
    goals_v2_df.to_excel('Monthly_Goals.xlsx',index=False)
	
def function_caller(func,db_name,hive_conn_name):
    func(db_name,hive_conn_name)
	
def to_check_job_completion(job_name):    
    wait_flag=1
    while wait_flag:
        status=0
        WebDriverWait(dm, 120).until(EC.presence_of_element_located((By.XPATH,"//*[@id='"+job_name+"']"))).click()
        time.sleep(1)
        while True:
            try:
                status = WebDriverWait(dm, 120).until(EC.presence_of_element_located((By.XPATH,"//*[@id='status_"+job_name+"']/a"))).get_attribute('tip')
                break
            except:
                time.sleep(10)
                pass
        #print status,"STATUS"
        if status=="COMPLETED":
            print ("Completed")
            wait_flag=0
            last_run_time=WebDriverWait(dm, 100).until(EC.presence_of_element_located((By.CSS_SELECTOR,"div.slick-cell.l3.r3.selected"))).text
            print (last_run_time)
            tm=last_run_time.split(",")[0].split(" ")
            if ((tm[1]=='sec') and (int(tm[0])<=59)) or ((tm[1]=='mins') and (int(tm[0])<=2)):
                print ("1",tm[1],tm[0])
            else:
                print ("Execution completion time is more than 2 mins - "+last_run_time)
        elif status in ("ERROR","COMPLETED WITH WARNINGS"):
            wait_flag=0
            dm.quit()
            content=job_name + " Failed. Kindly check for errors and Try again "
            to="antony.simon@bmo.com"
            sub="Job Execution Failed!"
            sendemail(content,to,sub)
        else:
            time.sleep(10)

def open_browser():
    options = webdriver.ChromeOptions()
    options.add_experimental_option("useAutomationExtension", False)
    #++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    # Check for presence of webdriver in the given path
    #++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    try:
        dm_wd = webdriver.Chrome(executable_path=source_path+'chromedriver.exe',options=options)
    except Exception as e:
        ctypes.windll.user32.MessageBoxA(0,str(e),"Warning!!", 1)
        sys.exit(1)
    dm_wd.get('https://datameer.bmocm.com/browser')

    #++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    # Check for Datameer availability. If unavailable, sends a mail to the 
    # list of receipients. A screen shot of the error page will be saved 
    # in the given path with the name "screen_shot_<yyyymmddHHMMSS>"
    #++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    try:
        WebDriverWait(dm_wd, 60).until(EC.presence_of_element_located((By.XPATH,"//input[@id='username']")))
        flag=1
    except Exception as e:
        #print(e)
        #print(dm_wd.page_source)
        dm_wd.save_screenshot('screen_shot_'+datetime.today().strftime('%Y%m%d%H%M%S%f')+'.png')
        dm_wd.quit()
        content="Datameer is down.The URL is unreachable.\n\n Please Find below the error.\n\n"+str(e)
        to='antony.simon@bmo.com'
        subject='Bussiness Banking Process Terminated!!'
        sendemail(content,to,subject)
        flag=0
    return flag,dm_wd
	
def upload_input(dm,upload_files,count):
    try:
        for f in upload_files:
            dm.find_element_by_xpath("//a[text()='Import_Jobs']").click()
            time.sleep(1)
            dm.find_element_by_xpath("//div[@class='ui-state-default slick-header-column slick-header-sortable slick-header-column-sorted']").click()
            time.sleep(1)
            upload_job(source_path,f,f)
            time.sleep(1)
            to_check_job_completion(f+"_upl")
            time.sleep(1)
            dm.find_element_by_xpath("//a[text()='Workbooks']").click()
            time.sleep(1)
            dm.find_element_by_xpath("//div[@class='ui-state-default slick-header-column slick-header-sortable slick-header-column-sorted']").click()
            time.sleep(1) 
            to_check_job_completion(f+"_wbk")
            time.sleep(1)
            dm.find_element_by_xpath("//a[text()='Export_Jobs']").click()
            time.sleep(1)
            dm.find_element_by_xpath("//div[@class='ui-state-default slick-header-column slick-header-sortable slick-header-column-sorted']").click()
            time.sleep(1)
            #+++++++++++++++++++++++++++++++++++++++++++++++++++++++
            # Checks for corresponding export job completion before
            # proceeding to the next job execution
            #+++++++++++++++++++++++++++++++++++++++++++++++++++++++
            to_check_job_completion(f+"_EJ_exp")
            time.sleep(1)
            print (f,"\n")
            #count=0
        return "Upload Completed"
    except Exception as err:
        print ("upload stale")
        if type(err).__name__=="StaleElementReferenceException":
            count+=1
            if count>3:
                return type(err).__name__
            else:
                time.sleep(10)
                return upload_input(dm,upload_files[upload_files.index(f):],count)
        else:
            raise err

def import_input(dm,import_joblist,count):
    try:
        for i in import_joblist:
            dm.find_element_by_xpath("//a[text()='Import_Jobs']").click()
            time.sleep(1)
            dm.find_element_by_xpath("//div[@class='ui-state-default slick-header-column slick-header-sortable slick-header-column-sorted']").click()
            time.sleep(1)            
            import_job(i)
            to_check_job_completion(i+"_imp")
            time.sleep(1)
            dm.find_element_by_xpath("//a[text()='Workbooks']").click()
            time.sleep(1)
            dm.find_element_by_xpath("//div[@class='ui-state-default slick-header-column slick-header-sortable slick-header-column-sorted']").click()
            time.sleep(1) 
            to_check_job_completion(i+"_wbk")
            time.sleep(1)
            dm.find_element_by_xpath("//a[text()='Export_Jobs']").click()
            time.sleep(1)
            dm.find_element_by_xpath("//div[@class='ui-state-default slick-header-column slick-header-sortable slick-header-column-sorted']").click()
            time.sleep(1)            
            to_check_job_completion(i+"_EJ_exp")
            time.sleep(1)
            print (i,"\n")
            #count=0
        return "Import Completed"
    except Exception as err:
        if type(err).__name__=="StaleElementReferenceException":
            print ("import stale")
            count+=1
            if count>3:
                return type(err).__name__
            else:
                time.sleep(10)
                return import_input(dm,import_joblist[import_joblist.index(i):],count)  
        else:
            raise err

def facts_dimensions(dm,func_list,count):
    try:
        func_dict={"goals_product_dimension":"Goals_Product","product_hierarchy_dimension":"Product_Hierarchy",
                   "date_dimension":"Date_Dimension","brm_hierarchy_dimension":"BRM_Hierarchy_Dimension",
                   "actuals_fact":"Actuals_Fact","goals_fact":"Goals_Fact",
                   "goals_actuals_fact":"Goals_Actuals_Fact","monthly_goals":"Monthly_Goals"}

        #++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
        # Deletes all Dimensions and Fact Excel files 
        # from the given path to avoid using old data and 
        # starts the upload of dimensions and facts only 
        # if the new Excel file is available.
        #++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

        for fn in func_list:
            print (fn.__name__)
            file_job_name=func_dict[fn.__name__]            
            file_path=os.path.join(file_sourcepath,file_job_name+".xlsx")
            if os.path.exists(file_path):
                os.remove(file_path)
                print (file_path," deleted")
            else:
                print (file_job_name, "-No such file")
            function_caller(fn,db,hive_connection)
            time.sleep(10)
            while not os.path.exists(file_path):
                time.sleep(1)
            if fn.__name__!='monthly_goals':
                if os.path.isfile(file_path):
                    dm.find_element_by_xpath("//a[text()='Import_Jobs_Facts_Dimensions']").click()
                    time.sleep(1)                
                    upload_job(source_path,file_job_name,file_job_name)
                    time.sleep(1)
                    to_check_job_completion(file_job_name+"_upl")
                    time.sleep(1)
                    dm.find_element_by_xpath("//a[text()='Workbooks_Facts_Dimensions']").click()
                    time.sleep(1)                
                    to_check_job_completion(file_job_name+"_wbk")
                    time.sleep(1)
                    dm.find_element_by_xpath("//a[text()='Export_Jobs_Facts_Dimensions']").click()
                    time.sleep(1)
                    to_check_job_completion(file_job_name+"_EJ_exp")
                    time.sleep(1)            
        return "F and D Completed"
    except Exception as err:
        print ("F and D stale")
        if type(err).__name__=="StaleElementReferenceException":
            count+=1
            if count>3:
                return type(err).__name__
            else:
                time.sleep(10)
                return facts_dimensions(dm,func_list[func_list.index(fn):],count)

#change to the required database - sbx_us_pc_ba__common_data

db="sbx_us_pc_ba__common_data"
#db="sbx_us_pcba_cent__common_data"

hive_connection=pyodbc.connect("DSN=Hadoop;DATABASE=sbx_us_pcba_cent__common_data;UID="+username+";PWD="+password+";",autocommit=True)

import_joblist=['BMO_Codes','EMPMSTR_HIST_BY_WEEK','Product_Hierarchy','CUMULATIVE_HDP']

upload_files=['BB_Goals','BRM_Hierarchy','Week_Table']

func_list=[goals_product_dimension,product_hierarchy_dimension,date_dimension,brm_hierarchy_dimension,
           actuals_fact,goals_fact,goals_actuals_fact,monthly_goals]

imp_upl_flag,dm=open_browser()

while imp_upl_flag:
    count=0
    try:
        dm.find_element_by_xpath("//input[@id='username']").send_keys(username)
        dm.find_element_by_xpath("//input[@id='password']").send_keys(password)
        dm.find_element_by_xpath("//button[text()='Login']").click()
        dm.implicitly_wait(30)

        time.sleep(2)
        WebDriverWait(dm, 60).until(EC.presence_of_element_located((By.XPATH,"//a[text()='Data']"))).click()
        time.sleep(2)
        dm.find_element_by_xpath("//a[text()='US_PC_BA_Shared']").click()
        time.sleep(1)
        dm.find_element_by_xpath("//a[text()='Report Centralization']").click()
        time.sleep(1)
        dm.find_element_by_xpath("//a[text()='BB']").click()
        time.sleep(1)
        dm.find_element_by_xpath("//label[@tip='Inspector (&nbsp;Alt I&nbsp;)']").click()
        time.sleep(1)

        upl_msg=upload_input(dm,upload_files,count)
        print (upl_msg,"*")
        if "Completed" in upl_msg:
            count=0
            print ("Upload Completed")
        else:
            raise upl_msg
        imp_msg=import_input(dm,import_joblist,count)
        print (imp_msg,"*")
        if "Completed" in imp_msg:
            count=0
            print ("Import Completed")
        else:
            raise imp_msg
        fd_msg=facts_dimensions(dm,func_list,count)
        print (fd_msg,"*")
        if "Completed" in fd_msg:
            count=0
            print ("Facts and Dimensions Completed")
        else:
            raise fd_msg

        dm.quit()
        imp_upl_flag=0
        content = "Completed without errors."
        to='antony.simon@bmo.com'
        subject="Run completed Successfully"
        sendemail(content,to,subject)
    except Exception as e:
        dm.save_screenshot('screen_shot_'+datetime.today().strftime('%Y%m%d%H%M%S%f')+'.png')
        imp_upl_flag=0
        content="Run Failed with following errors.\n\n\n"+str(e)+"\n\n"
        to="antony.simon@bmo.com"
        subject="Run Unsuccessfull!!"
        sendemail(content,to,subject)
        dm.quit()

end_time=datetime.now()
print (end_time)

print (end_time-st_time)
