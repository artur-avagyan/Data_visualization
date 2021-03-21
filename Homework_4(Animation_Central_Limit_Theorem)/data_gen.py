import sqlite3
import numpy as np
import pandas as pd
import time
from scipy import stats

connection = sqlite3.connect('data_db.db')
c = connection.cursor()
#c.close()
c.execute("DROP TABLE IF EXISTS two_values")

c.execute('''CREATE TABLE two_values 
          (ID int,
          value1 int,
          value2 int,
          value3 int,
          value4 int,
          value5 int,
          value6 int,
          value7 int
          )''')
c.execute("DROP TABLE IF EXISTS p_value_historical")
c.execute('''CREATE TABLE p_value_historical 
          (ID int,
          p_value float)''')


i = 0

while i<10000:
	i += 1
	value_list = np.random.randint(low=1,high=7,size=7)
	c.execute("INSERT INTO two_values values ({},{},{},{},{},{},{},{})".format(*np.append(i,value_list)))
	connection.commit()

	query = ('SELECT * FROM two_values')
	data_1 = pd.read_sql_query(query, connection)
	list_mean=data_1.iloc[:,1:].mean(axis=1)
	if i>=3:
		c.execute("INSERT INTO p_value_historical values ({},{})".format(i,stats.shapiro(list_mean)[1]))
	
	time.sleep(0.5)