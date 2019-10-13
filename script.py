import pandas as pd
from datetime import date
filepath="messy.xlsx"
df=pd.read_excel(filepath,sheet_name="test")
df.columns = [col.strip().replace(" ","_").lower() for col in df.columns] # modify column
df = df.drop('unnamed:_2',1) #drop column 
#-----------change title with Upercase first letter----------------------------------------------
df.fll_nam = [str.capitalize(name.split()[1]) + " " + str.capitalize(name.split()[0]) for name in df.fll_nam]
#--------------------------------------------------------------------
#-----------Create new column "Email" with string format {lname}.{fname}.{id}@yourcompany.com------------------------
param1 = "{}.{}"
param2=".{}@yourcompany.com"
df["Email1"] = [param1.format(name.split()[1],name.split()[0]) for name in df.fll_nam]
df["Email"] = df.Email1 + [param2.format(id) for id in df.cust_id.map(str)]
df = df.drop('Email1',1)
#--------------------------------------------
#-----------------Change format Date YYYY-MM-DD-----------------------
df['join%_date'] = [date.split()[0] for date in df["join%_date"]]
df['join%_date']= pd.to_datetime(df["join%_date"])
df['join%_date']= pd.to_datetime(df["join%_date"], format="%d/%m/%Y")
#-------------------------------------------------------------------
#------------------add 84 for mobiles column------------------------
df.mobiles=[mobi if mobi.startswith('84') else "84"+ mobi for mobi in df.mobiles.map(str)]
#-------------------------------------------------------------------
df=df.sort_values("join%_date")
# Select duplicate rows except first occurrence based on all columns
duplicateRowsDF = df[df.duplicated("cust_id")]
 
print(duplicateRowsDF)

df=df.drop(duplicateRowsDF.index,axis=0)

df=df.sort_values("cust_id")
fil = pd.DatetimeIndex(df['join%_date']).year == 2019
today = date.today() #get current date
exportfile = "emp_{}.csv"
df[fil].to_csv(exportfile.format(today.strftime("%Y%m%d")))
df.head()
#---------------------------------------------