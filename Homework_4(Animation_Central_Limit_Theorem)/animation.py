import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import matplotlib.gridspec as gridspec
import time
import sqlite3
from scipy import stats
import seaborn as sns
import warnings
warnings.filterwarnings('ignore')

connection = sqlite3.connect('data_db.db')
c = connection.cursor()

plt.xkcd()

fig = plt.figure(constrained_layout=True,figsize=(10,10))
gs = fig.add_gridspec(2, 4)

fg_ax1 = fig.add_subplot(gs[0, 0])

fg_ax2 = fig.add_subplot(gs[0, 1])

fg_ax3 = fig.add_subplot(gs[1, 0])

fg_ax4 = fig.add_subplot(gs[1, 1])

fg_ax5 = fig.add_subplot(gs[0:, 2:])


i=0

def animate(i):
	query = ('SELECT * FROM two_values')
	data = pd.read_sql_query(query, connection)
	list_mean=data.iloc[:,1:].mean(axis=1)
	
	fg_ax1.cla()
	fg_ax1.set_title('Distribution of means',size=15,pad=10)
	sns.distplot(ax=fg_ax1,a=list_mean)
	# fg_ax1.hist(list_mean,bins=15)

	fg_ax3.cla()
	fg_ax3.set_title('Normality test p-value',size=15,pad=10)
	if data.iloc[-1,0]>=3:
		anno_opts = dict(xy=(0.5, 0.5), xycoords='axes fraction',
	                 va='center', ha='center',size=15)
		fg_ax3.annotate('p-value: {k}'.format(k=str(np.round(stats.shapiro(list_mean)[1],4))), **anno_opts)
	fg_ax3.axis('off')

	fg_ax2.cla()
	fg_ax2.set_title('Probability plot',size=15,pad=10)
	stats.probplot(list_mean, dist="norm", plot=fg_ax2)


	fg_ax4.cla()
	fg_ax4.set_title('Historical p-values',size=15,pad=10)
	if i>=3:
		query = ('SELECT * FROM p_value_historical')
		data_p_value = pd.read_sql_query(query, connection)
		x=data_p_value.ID
		y=data_p_value.p_value
		fg_ax4.plot(x,y)

	fg_ax5.cla()
	fg_ax5.set_title('Original distribution',size=15,pad=10)
	output_list=[]
	for i in range(data.shape[0]):
		for j in range(1,data.shape[1]):
			output_list.append(data.iloc[i,j])
	sns.countplot(output_list,ax=fg_ax5)

ani = FuncAnimation(plt.gcf(), animate, interval = 500)
plt.show()
c.close()