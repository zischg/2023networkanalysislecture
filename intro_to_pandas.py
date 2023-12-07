#pandas is a fast, powerful, flexible and easy to use open source data analysis and manipulation tool,
#built on top of the Python programming language

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

#Creating a Data Frame
# Dictionary of key pair values called data
data = {'Name':['Ashika', 'Tanu', 'Ashwin', 'Mohit', 'Sourabh'],'Age': [24, 23, 22, 19, 10]}
data
df = pd.DataFrame(data)
df
df.describe()

#Performing operations on Rows and Columns
# Selecting column
df2=df[['Age']]

#Selecting a Row
row = df.loc[1, "Age"]
row

#Selecting a single cell using numerical indexes - iloc
onevalue = df.iloc[1,1]
onevalue
df.iloc[0:3, :]


#Data Selection, addition, deletion
#adding a column and calculate values
df['Age2']=df['Age']-18

#iterating through rows
#add a new columns
df['isadult']=0
for index, row in df.iterrows():
    if row['Age']>=18:
        df.loc[index, 'isadult']=1

#do the same again without iteration
df['isadult']=0
df.loc[df['Age']>=18, 'isadult']=1


#Filtering Rows
names_of_adults=df[df["isadult"] ==1]["Name"].tolist()
names_of_adults=df[df["isadult"] ==1]["Name"].unique().tolist()
#select rows having an attribute in the list
df[df.Name.isin(['Ashika', 'Tanu'])]
df[df["Name"].isin(['Ashika', 'Tanu'])]
#same, but opposite filter
df[~df.Name.isin(['Ashika', 'Tanu'])]

#Returns the mean of all columns
df.mean()
#Returns the correlation between columns in a data frame
df.corr()
#Returns the number of non-null values in each data frame
df.count()
#Returns the highest value in each column
df.max()
#Returns the lowest value in each column
df.min()
#Returns the median of each column
df.median()
#Returns the standard deviation of each column
df.std()

#sorting
df.sort_values("Age")
df.sort_values("Age",ascending=False)

#Grouping and Statistical operations of single columns
df["Age"].sum()
df[["Age"]].mean()
df[["Age"]].min()
df[["Age"]].max()
df[["Age"]].median()

df.groupby(["isadult"])["Age"].mean()
#More than one aggregation
df.groupby(["isadult"]).agg({'Age':['sum', 'max'],'Age2':'mean'})

#data cleaning
#check for null values
df.isnull()
df.notnull()
#get rid of null values, or drop them
#drop rows
df.dropna(inplace=True)

#plot
df["Age"].plot()
df["Age"].hist()
plt.scatter(df.Age, df.Age2)


#read a csv file
df = pd.read_csv("C:/DATA/infile.csv", encoding='ANSI', delimiter=";")
df.head()
#manipulate the dataframe
df["E"]=df["D"]*1000
#write a csv file
df.to_csv("C:/DATA/outfile.csv", index=False)

#
import joblib
joblib.dump(df,"C:/DATA/df.sav")
df=joblib.load("C:/DATA/df.sav")


#read an excel file
import xlrd
import openpyxl
df = pd.read_excel("C:/DATA/develops/ccwgrsensi/Matrix_Baum_inkl_collin_export.xlsx",sheet_name='Baumschicht', engine='openpyxl')
df.head()


#read from database
import psycopg2
import sqlalchemy
import geoalchemy2
from sqlalchemy import create_engine
db_connection_url = "postgres://username:mypassword@localhost:5432/pythonspatial";
engine = create_engine(db_connection_url)
sqlstatement='SELECT "bestand_id", "BAUMART_ID", "GDICKnum" FROM public."BK_BAUMART"'
bk_df=pd.read_sql_query(sqlstatement,con=engine)

#time series
from datetime import datetime
date_rng = pd.date_range(start='1/1/2021', end='1/08/2021', freq='H')
type(date_rng[0])
df = pd.DataFrame(date_rng, columns=['date'])
df['data'] = np.random.randint(0,100,size=(len(date_rng)))
df.head(15)

#Convert the data frame index to a datetime index
df['datetime'] = pd.to_datetime(df['date'])
df = df.set_index('datetime')
df.drop(['date'], axis=1, inplace=True)
df.head()
#extract one day
df[df.index.day == 2]
df['2021-01-02']
#extract a period
df['2021-01-04':'2021-01-06']
#window statistics such as a rolling mean or a rolling sum
df['rolling_sum'] = df.rolling(3).sum()
df.head(10)


#create, open and write to a file
outfile=open("C:/DATA/test.txt", "w")
outfile.write("this is the first line\n")
outfile.write("this is the second line\n")
outfile.close()