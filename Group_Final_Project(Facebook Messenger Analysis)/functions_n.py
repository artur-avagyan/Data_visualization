import json
import datetime
from datetime import datetime
from pytz import timezone
import pandas as pd
import numpy as np
import re
import random
import os
from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt

def arm_eng(text):
    '''
    Parameters:
        text -> text
    Returns:
        text -> converted text from armenian to english
    Example: arm_eng('\u00d4\u00b2\u00d5\u00a1\u00d6\u0080\u00d6\u0087') returns 'Barev'
    ''' 
    text=text.replace('\u00d5\u0088\u00d6\u0082','U')
    text=text.replace('\u00d5\u00b8\u00d6\u0082','u')
    text=text.replace('\u00d5\u0088\u00d5\u00be','Ov')
    text=text.replace('\u00d5\u00b8\u00d5\u00be','ov')
    text=text.replace('\u00d5\u00b8','o')
    text=text.replace('\u00d4\u00b5\u00d5\u00be','Ev')
    text=text.replace('\u00d4\u00b1','A')
    text=text.replace('\u00d5\u00a1','a')
    text=text.replace('\u00d4\u00b2','B')
    text=text.replace('\u00d5\u00a2','b')
    text=text.replace('\u00d4\u00b3','G')
    text=text.replace('\u00d5\u00a3','g')
    text=text.replace('\u00d4\u00b4','D')
    text=text.replace('\u00d5\u00a4','d')
    text=text.replace('\u00d4\u00b5','E')
    text=text.replace('\u00d5\u00a5','e')
    text=text.replace('\u00d4\u00b6','Z')
    text=text.replace('\u00d5\u00a6','z')
    text=text.replace('\u00d4\u00b7','E')
    text=text.replace('\u00d5\u00a7','e')
    text=text.replace('\u00d4\u00b8','Y')
    text=text.replace('\u00d5\u00a8','y')
    text=text.replace('\u00d4\u00b9','T')
    text=text.replace('\u00d5\u00a9','t')
    text=text.replace('\u00d4\u00ba','Zh')
    text=text.replace('\u00d5\u00aa','zh')
    text=text.replace('\u00d4\u00bb','I')
    text=text.replace('\u00d5\u00ab','i')
    text=text.replace('\u00d4\u00bc','L')
    text=text.replace('\u00d5\u00ac','l')
    text=text.replace('\u00d4\u00bd','X')
    text=text.replace('\u00d5\u00ad','x')
    text=text.replace('\u00d4\u00be','C')
    text=text.replace('\u00d5\u00ae','c')
    text=text.replace('\u00d4\u00bf','K')
    text=text.replace('\u00d5\u00af','k')
    text=text.replace('\u00d5\u0080','H')
    text=text.replace('\u00d5\u00b0','h')
    text=text.replace('\u00d5\u0081','Dz')
    text=text.replace('\u00d5\u00b1','dz')
    text=text.replace('\u00d5\u0082','Gh')
    text=text.replace('\u00d5\u00b2','gh')
    text=text.replace('\u00d5\u0083','Ch')
    text=text.replace('\u00d5\u00b3','ch')
    text=text.replace('\u00d5\u0084','M')
    text=text.replace('\u00d5\u00b4','m')
    text=text.replace('\u00d5\u0085','Y')
    text=text.replace('\u00d5\u00b5','y')
    text=text.replace('\u00d5\u0086','N')
    text=text.replace('\u00d5\u00b6','n')
    text=text.replace('\u00d5\u0087','Sh')
    text=text.replace('\u00d5\u00b7','sh')
    text=text.replace('\u00d5\u0088','Vo')
    text=text.replace('\u00d5\u0089','Ch')
    text=text.replace('\u00d5\u00b9','ch')
    text=text.replace('\u00d5\u008a','P')
    text=text.replace('\u00d5\u00ba','p')
    text=text.replace('\u00d5\u008b','J')
    text=text.replace('\u00d5\u00bb','j')
    text=text.replace('\u00d5\u008c','R')
    text=text.replace('\u00d5\u00bc','r')
    text=text.replace('\u00d5\u008d','S')
    text=text.replace('\u00d5\u00bd','s')
    text=text.replace('\u00d5\u008e','V')
    text=text.replace('\u00d5\u00be','v')
    text=text.replace('\u00d5\u008f','T')
    text=text.replace('\u00d5\u00bf','t')
    text=text.replace('\u00d5\u0090','R')
    text=text.replace('\u00d6\u0080','r')
    text=text.replace('\u00d5\u0091','C')
    text=text.replace('\u00d6\u0081','c')
    text=text.replace('\u00d5\u0088\u00d6\u0082','U')
    text=text.replace('\u00d5\u00b8\u00d6\u0082','u')
    text=text.replace('\u00d5\u0093','P')
    text=text.replace('\u00d6\u0083','p')
    text=text.replace('\u00d5\u0094','Q')
    text=text.replace('\u00d6\u0084','q')
    text=text.replace('\u00d4\u00b5\u00d5\u00be','Ev')
    text=text.replace('\u00d6\u0087','ev')
    text=text.replace('\u00d5\u0095','O')
    text=text.replace('\u00d6\u0085','o')
    text=text.replace('\u00d5\u0096','F')
    text=text.replace('\u00d6\u0086','f')
    return text

def create_data_frame(folder_path='./'):
	weekDays = ("Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday")

	df=pd.DataFrame(columns=['Date','Sender','Message','Reactions','Photos','Video','Voice-message','File',
	                         'Sticker','GIF','Link','Year','Month','Day','WeekDay','Hour'])
	#Dictionary which has participants as key, and number of votes in polls as value
	df_poll_voted={}
	json_count=0
	for i in os.listdir('./'):
		if i[-5:]=='.json':
			json_count=json_count+1
	for i in range(1,json_count+1):
	    with open(folder_path+'/message_{i}.json'.format(i=i),encoding='utf-8') as json_file:
	        json_data = json.load(json_file)
	    for message in json_data["messages"]:
	        #Using datetime module to convert 'timestamp' format
	        date = datetime.fromtimestamp(message["timestamp_ms"] / 1000).astimezone(timezone('Asia/Yerevan')).strftime("%Y-%m-%d %H:%M")
	        date=datetime.strptime(date, "%Y-%m-%d %H:%M") #Converted from 'string' format to 'datetime64[ns]'
	        Day=date.day #Get day of message
	        Month=date.strftime('%B')#Get month of message
	        Year=date.year #Get year of message
	        WeekDay = weekDays[date.weekday()] #Get weekday of message
	        Hour=date.hour #Get hour of message
	        sender = arm_eng(message["sender_name"]) #Converted senders' names from armenian to english

	        #Count of reactions to the message
	        if 'reactions' in message:
	            count_reactions=0
	            for j in message['reactions']:
	                count_reactions+=1
	        else:
	            count_reactions=0

	        #Check if the message is a video
	        if 'videos' in message:
	            video=1
	        else:
	            video=0

	        #Check if the message is a sticker
	        if 'sticker' in message:
	            sticker=1
	        else:
	            sticker=0

	        #Check if the message is a GIF
	        if "gifs" in message:
	            gif=1
	        else:
	            gif=0

	        #Count of files in the message
	        if 'files' in message:
	            count_files=0
	            for j in message['files']:
	                count_files+=1
	        else:
	            count_files=0

	        #Check if the message is a voice-message
	        if "audio_files" in message:
	            voice=1
	        else:
	            voice=0

	        #Count of photos in the message
	        if 'photos' in message:
	            count_photos=0
	            for j in message['photos']:
	                count_photos+=1
	        else:
	            count_photos=0

	        #Check if the message is a text
	        if 'content' in message:
	            content = arm_eng(message["content"])

	            #Check if the message is a link
	            if message['type']=='Share':
	                content=''
	                link=1
	            else: 
	                link=0

	            #Don't include some actions as message
	            if (('as a group admin.' in content) or ('set the emoji to' in content)) or\
	                ((('the group' in content) or ('created a poll' in content)) or\
	                (('removed their vote for' in content) and ('in the poll' in content))):
	                continue

	            #Count of votes in polls
	            if (('voted for' in content) and ('in the poll' in content)) or ('This poll is no longer available' in content):
	                if sender in df_poll_voted.keys():
	                    df_poll_voted[sender]+=1
	                else:
	                    df_poll_voted[sender]=1
	                continue
	        else:
	            content=''
	            link=0
	        #Every message was added as a unique row
	        df =df.append({'Date':date,
	                       'Sender':sender,
	                       'Message':content,
	                       'Reactions': count_reactions,
	                       'Photos': count_photos,
	                       'Video': video,
	                       'Voice-message': voice,
	                       'File': count_files,
	                       'Sticker': sticker,
	                       'GIF': gif,
	                       'Link': link,
	                       'Year':Year,
	                       'Month':Month,
	                       'Day':Day,
	                       'WeekDay':WeekDay,
	                       'Hour':Hour},ignore_index=True)
	df['Sender'] = df['Sender'].astype('category')
	df['Message'] = df['Message'].astype(str)
	df['Reactions'] = df['Reactions'].astype(int)
	df['Photos'] = df['Photos'].astype(int)
	df['Video'] = df['Video'].astype(int)
	df['Voice-message'] = df['Voice-message'].astype(int)
	df['File'] = df['File'].astype(int)
	df['Sticker'] = df['Sticker'].astype(int)
	df['GIF'] = df['GIF'].astype(int)
	df['Link'] = df['Link'].astype(int)
	df['Year'] = df['Year'].astype('category')
	df['Month'] = df['Month'].astype('category')
	df['WeekDay'] = df['WeekDay'].astype('category')
	df['Day'] = df['Day'].astype('category')
	df['Hour'] = df['Hour'].astype('category')
	return df

def group_wise_stats_string(data_frame):
	df_stat=pd.DataFrame(data_frame[['Reactions','Photos','File','Video','Voice-message','Sticker','GIF','Link']].sum(),columns=['Count'])
	df_stat.loc['Messages']=len(data_frame[data_frame['Message']!=''])
	df_stat=df_stat.sort_values(by='Count', ascending=False)
	string_list=[]
	for i in range(len(df_stat)):
		string_list.append(str(df_stat.index[i])+': '+str(df_stat['Count'][i]))
	return string_list

def all_information(data_frame):
	df1=pd.DataFrame(data_frame.groupby(['Sender'])[['Reactions','Photos','File','Video','Voice-message','Sticker','GIF','Link']].agg('sum'))
	df2=pd.DataFrame(data_frame[data_frame['Message']!=''].groupby(['Sender'])['Message'].agg('count'))
	#Add df2 in df1
	df1.insert(loc=0,column='Message',value=df2)
	return df1

smile=['\u00f0\u009f\u0098\u0080','\u00f0\u009f\u0098\u0083','\u00f0\u009f\u0098\u0084','\u00f0\u009f\u0098\u0081',
 '\u00f0\u009f\u0098\u0086','\u00f0\u009f\u0098\u0085','\u00f0\u009f\u0098\u0082','\u00f0\u009f\u00a4\u00a3',
 '\u00e2\u0098\u00ba\u00ef\u00b8\u008f','\u00f0\u009f\u0098\u008a','\u00f0\u009f\u0098\u0087','\u00f0\u009f\u0099\u0082',
 '\u00f0\u009f\u0099\u0083','\u00f0\u009f\u0098\u0089','\u00f0\u009f\u0098\u008d','\u00f0\u009f\u00a5\u00b0',
 '\u00f0\u009f\u0098\u0098','\u00f0\u009f\u00a4\u00a9','\u00f0\u009f\u00a5\u00b3','\u00f0\u009f\u008e\u0089',
 '\u00f0\u009f\u0098\u008e','\u00f0\u009f\u0098\u0095','\u00f0\u009f\u0098\u0092','\u00f0\u009f\u0098\u008f',
 '\u00f0\u009f\u0098\u009e','\u00e2\u0098\u00b9\u00ef\u00b8\u008f','\u00f0\u009f\u0098\u00a2','\u00f0\u009f\u00a5\u00ba',
 '\u00f0\u009f\u0098\u00ad','\u00f0\u009f\u0098\u00a1' ,'\u00f0\u009f\u0098\u00a0','\u00f0\u009f\u0091\u008d',
 '\u00e2\u009c\u008c\u00ef\u00b8\u008f','\u00f0\u009f\u0091\u008a','\u00f0\u009f\u00a4\u0099',
 '\u00f0\u009f\u00a4\u00a6\u00e2\u0080\u008d\u00e2\u0099\u0082\u00ef\u00b8\u008f',
 '\u00f0\u009f\u00a4\u00a6\u00e2\u0080\u008d\u00e2\u0099\u0080\u00ef\u00b8\u008f',
 '\u00f0\u009f\u00a4\u00b7\u00e2\u0080\u008d\u00e2\u0099\u0080\u00ef\u00b8\u008f',
 '\u00f0\u009f\u00a4\u00b7\u00e2\u0080\u008d\u00e2\u0099\u0082\u00ef\u00b8\u008f',
 '\u00f0\u009f\u008e\u0082','\u00f0\u009f\u008d\u00b0','\u00e2\u009d\u00a4\u00ef\u00b8\u008f','\u00f0\u009f\u00a7\u00a1',
 '\u00f0\u009f\u0092\u009b','\u00f0\u009f\u0092\u009a','\u00f0\u009f\u0092\u0099','\u00f0\u009f\u0092\u009c',
 '\u00f0\u009f\u00a4\u008e','\u00f0\u009f\u0096\u00a4','\u00f0\u009f\u00a4\u008d','\u00f0\u009f\u0092\u0094',
 '\u00e2\u009d\u00a3\u00ef\u00b8\u008f','\u00f0\u009f\u0092\u0095','\u00f0\u009f\u0092\u009e','\u00f0\u009f\u0092\u0093',
 '\u00e2\u009c\u0085','\u00f0\u009f\u0087\u00a6\u00f0\u009f\u0087\u00b2']

def number_each_emojis(df):
	data_smile={}
	members=df['Sender'].unique()
	for i in members:
		data_smile[i]={}
		df_member_message=df[df['Sender']==i]['Message']
		for j in df_member_message:
			for k in range(len(smile)):
				if smile[k] in j:
					if k not in data_smile[i]:
						data_smile[i][k]=len(re.findall(smile[k], j))
					else:
						data_smile[i][k]+=len(re.findall(smile[k], j))
				else:
					continue
		if len(data_smile[i])==0:
			data_smile.pop(i)
	return data_smile

def emojis_by_member(df):
	data_smile={}
	members=df['Sender'].unique()
	for a in range(len(smile)):
		data_smile[str(a)]={}
		for i in members:
			df_member_message=df[df['Sender']==i]['Message']
			for j in df_member_message:
				if smile[a] in j:
					if i not in data_smile[str(a)]:
						data_smile[str(a)][i]=len(re.findall(smile[a], j))
					else:
						data_smile[str(a)][i]+=len(re.findall(smile[a], j))
				else:
					continue
		if len(data_smile[str(a)])==0:
			data_smile.pop(str(a))
	return data_smile

def number_of_emijis_per_member(df):
	#create DataFrame to count emojis
	df_smile=pd.DataFrame(df['Sender'].unique(),columns=['sender']) 
	df_smile['count_smile']=pd.DataFrame(np.zeros(shape=(len(df_smile),1)))
	count_smile_index=([0]*len(smile))
	for i in range(len(df)):
	    count=0 #create variable for that unique message
	    for sm in range(len(smile)): # loop to find every smile from smiles' list
	        count += len(re.findall(smile[sm], df['Message'][i]))
	        count_smile_index[sm]+=len(re.findall(smile[sm], df['Message'][i]))
	    for j in range(len(df_smile)): # loop to update counts per member
	        if df_smile['sender'][j]==df['Sender'][i]:
	            df_smile.count_smile[j]+=count
	df_smile=df_smile.sort_values(by=['count_smile'], ascending=False,ignore_index=True)
	return df_smile[df_smile.count_smile>0]  # view members who used emojis

def most_emoji_table(df):
	data_most_emojis=pd.DataFrame(columns=['Member name','Emoji Index','Count'])
	for i in [*number_each_emojis(df).keys()]:
	    member=i
	    sorted_count=sorted(number_each_emojis(df)[i].items(), key=lambda x: x[1], reverse=True)
	    emoji_index=sorted_count[0][0]
	    count_=sorted_count[0][1]
	    data_most_emojis=data_most_emojis.append({'Member name':member,
	                       'Emoji Index':emoji_index,
	                       'Count':count_,},ignore_index=True)
	return data_most_emojis.sort_values('Member name',ignore_index=True)

def reaction_index(text):
    '''
    Define type of reactions
    '''
    text=text.replace('\u00e2\u009d\u00a4\u00ef\u00b8\u008f','Love')
    text=text.replace('\u00e2\u009d\u00a4','Love')
    text=text.replace('\u00f0\u009f\u0098\u008d','Love')
    text=text.replace('\u00f0\u009f\u0098\u0086','HaHa')
    text=text.replace('\u00f0\u009f\u0098\u00ae','Wow')
    text=text.replace('\u00f0\u009f\u0098\u00a2','Sad')
    text=text.replace('\u00f0\u009f\u0098\u00a1','Angry')
    text=text.replace('\u00f0\u009f\u0098\u00a0','Angry')
    text=text.replace('\u00f0\u009f\u0091\u008d\u00f0\u009f\u008f\u00bb','Like')
    text=text.replace('\u00f0\u009f\u0091\u008d','Like')
    text=text.replace('\u00f0\u009f\u0091\u008e','Unlike')
    return text

def reaction_data(folder_path='./'):
	df_reactions=pd.DataFrame(columns=['Message sender','Reaction sender','Reaction type'])
	json_count=0
	for i in os.listdir('./'):
		if i[-5:]=='.json':
			json_count=json_count+1
	for i in range(1,json_count+1):
	    with open(folder_path+'/message_{i}.json'.format(i=i),encoding='utf-8') as json_file:
	        json_data = json.load(json_file)
	    for message in json_data['messages']: #loop for messages
		    if 'reactions' in message: #check if the message has reaction
		    	for j in message['reactions']: #koop for reactions
		            if j['reaction']!=reaction_index(j['reaction']): #check if the reaction is in the top 7 reactions
		                df_reactions =df_reactions.append({'Message sender': arm_eng(message['sender_name']),
		                                                   'Reaction sender': arm_eng(j['actor']),
		                                                   'Reaction type': reaction_index(j['reaction'])},ignore_index=True)
		            else:
		                df_reactions =df_reactions.append({'Message sender': arm_eng(message['sender_name']),
		                                                   'Reaction sender': arm_eng(j['actor']),
		                                                   'Reaction type': 'Other'},ignore_index=True)
		    else:
		        continue
	return df_reactions

def clean_text_split(text):
    smile=['\u00f0\u009f\u0098\u0080','\u00f0\u009f\u0098\u0083','\u00f0\u009f\u0098\u0084','\u00f0\u009f\u0098\u0081',
 '\u00f0\u009f\u0098\u0086','\u00f0\u009f\u0098\u0085','\u00f0\u009f\u0098\u0082','\u00f0\u009f\u00a4\u00a3',
 '\u00e2\u0098\u00ba\u00ef\u00b8\u008f','\u00f0\u009f\u0098\u008a','\u00f0\u009f\u0098\u0087','\u00f0\u009f\u0099\u0082',
 '\u00f0\u009f\u0099\u0083','\u00f0\u009f\u0098\u0089','\u00f0\u009f\u0098\u008d','\u00f0\u009f\u00a5\u00b0',
 '\u00f0\u009f\u0098\u0098','\u00f0\u009f\u00a4\u00a9','\u00f0\u009f\u00a5\u00b3','\u00f0\u009f\u008e\u0089',
 '\u00f0\u009f\u0098\u008e','\u00f0\u009f\u0098\u0095','\u00f0\u009f\u0098\u0092','\u00f0\u009f\u0098\u008f',
 '\u00f0\u009f\u0098\u009e','\u00e2\u0098\u00b9\u00ef\u00b8\u008f','\u00f0\u009f\u0098\u00a2','\u00f0\u009f\u00a5\u00ba',
 '\u00f0\u009f\u0098\u00ad','\u00f0\u009f\u0098\u00a1' ,'\u00f0\u009f\u0098\u00a0','\u00f0\u009f\u0091\u008d',
 '\u00e2\u009c\u008c\u00ef\u00b8\u008f','\u00f0\u009f\u0091\u008a','\u00f0\u009f\u00a4\u0099',
 '\u00f0\u009f\u00a4\u00a6\u00e2\u0080\u008d\u00e2\u0099\u0082\u00ef\u00b8\u008f',
 '\u00f0\u009f\u00a4\u00a6\u00e2\u0080\u008d\u00e2\u0099\u0080\u00ef\u00b8\u008f',
 '\u00f0\u009f\u00a4\u00b7\u00e2\u0080\u008d\u00e2\u0099\u0080\u00ef\u00b8\u008f',
 '\u00f0\u009f\u00a4\u00b7\u00e2\u0080\u008d\u00e2\u0099\u0082\u00ef\u00b8\u008f',
 '\u00f0\u009f\u008e\u0082','\u00f0\u009f\u008d\u00b0','\u00e2\u009d\u00a4\u00ef\u00b8\u008f','\u00f0\u009f\u00a7\u00a1',
 '\u00f0\u009f\u0092\u009b','\u00f0\u009f\u0092\u009a','\u00f0\u009f\u0092\u0099','\u00f0\u009f\u0092\u009c',
 '\u00f0\u009f\u00a4\u008e','\u00f0\u009f\u0096\u00a4','\u00f0\u009f\u00a4\u008d','\u00f0\u009f\u0092\u0094',
 '\u00e2\u009d\u00a3\u00ef\u00b8\u008f','\u00f0\u009f\u0092\u0095','\u00f0\u009f\u0092\u009e','\u00f0\u009f\u0092\u0093',
 '\u00e2\u009c\u0085','\u00f0\u009f\u0087\u00a6\u00f0\u009f\u0087\u00b2']
    for sm in smile:
        if sm in text:
            text=re.sub(sm, '', text)
    text = text.lower()
    text = re.sub('\[.*?\]', '', text)
    text = re.sub('\w*\d\w*', '', text)
    text = re.sub('[‘’“”…]', '', text)
    text = re.sub('\n', '', text)
    text=re.split(' ',text)
    return text

def most_used_word(df):
	senders=sorted(df['Sender'].unique()) # select members of chat
	data_text=pd.DataFrame(columns=['Message sender','Most used word']) # create DataFrame
	data_text['Message sender']=senders #column for members
	data_text['Most used word']='' #empty column, then it will be most used word per members
	for i in range(len(data_text)): # loop for dataframe
	    sender_text=[] #empty list for word
	    df_member=df[df['Sender']==data_text['Message sender'][i]].reset_index() #filter main Dataframe by Message sender
	    for j in range(len(df_member)): #loop for that filter dataframe
	        for h in clean_text_split(df_member['Message'][j]): #loop for words
	            if len(h)>4: # check if word consist more than 4 letters
	                sender_text.append(h) #append word to list
	    try: #exception for index 0
	        data_text['Most used word'][i]=pd.Series(sender_text).value_counts().index[0]
	    except IndexError:
	        data_text['Most used word'][i]=''
	return data_text #view data frame

def clean_text_no_split(text):
    smile=['\u00f0\u009f\u0098\u0080','\u00f0\u009f\u0098\u0083','\u00f0\u009f\u0098\u0084','\u00f0\u009f\u0098\u0081',
 '\u00f0\u009f\u0098\u0086','\u00f0\u009f\u0098\u0085','\u00f0\u009f\u0098\u0082','\u00f0\u009f\u00a4\u00a3',
 '\u00e2\u0098\u00ba\u00ef\u00b8\u008f','\u00f0\u009f\u0098\u008a','\u00f0\u009f\u0098\u0087','\u00f0\u009f\u0099\u0082',
 '\u00f0\u009f\u0099\u0083','\u00f0\u009f\u0098\u0089','\u00f0\u009f\u0098\u008d','\u00f0\u009f\u00a5\u00b0',
 '\u00f0\u009f\u0098\u0098','\u00f0\u009f\u00a4\u00a9','\u00f0\u009f\u00a5\u00b3','\u00f0\u009f\u008e\u0089',
 '\u00f0\u009f\u0098\u008e','\u00f0\u009f\u0098\u0095','\u00f0\u009f\u0098\u0092','\u00f0\u009f\u0098\u008f',
 '\u00f0\u009f\u0098\u009e','\u00e2\u0098\u00b9\u00ef\u00b8\u008f','\u00f0\u009f\u0098\u00a2','\u00f0\u009f\u00a5\u00ba',
 '\u00f0\u009f\u0098\u00ad','\u00f0\u009f\u0098\u00a1' ,'\u00f0\u009f\u0098\u00a0','\u00f0\u009f\u0091\u008d',
 '\u00e2\u009c\u008c\u00ef\u00b8\u008f','\u00f0\u009f\u0091\u008a','\u00f0\u009f\u00a4\u0099',
 '\u00f0\u009f\u00a4\u00a6\u00e2\u0080\u008d\u00e2\u0099\u0082\u00ef\u00b8\u008f',
 '\u00f0\u009f\u00a4\u00a6\u00e2\u0080\u008d\u00e2\u0099\u0080\u00ef\u00b8\u008f',
 '\u00f0\u009f\u00a4\u00b7\u00e2\u0080\u008d\u00e2\u0099\u0080\u00ef\u00b8\u008f',
 '\u00f0\u009f\u00a4\u00b7\u00e2\u0080\u008d\u00e2\u0099\u0082\u00ef\u00b8\u008f',
 '\u00f0\u009f\u008e\u0082','\u00f0\u009f\u008d\u00b0','\u00e2\u009d\u00a4\u00ef\u00b8\u008f','\u00f0\u009f\u00a7\u00a1',
 '\u00f0\u009f\u0092\u009b','\u00f0\u009f\u0092\u009a','\u00f0\u009f\u0092\u0099','\u00f0\u009f\u0092\u009c',
 '\u00f0\u009f\u00a4\u008e','\u00f0\u009f\u0096\u00a4','\u00f0\u009f\u00a4\u008d','\u00f0\u009f\u0092\u0094',
 '\u00e2\u009d\u00a3\u00ef\u00b8\u008f','\u00f0\u009f\u0092\u0095','\u00f0\u009f\u0092\u009e','\u00f0\u009f\u0092\u0093',
 '\u00e2\u009c\u0085','\u00f0\u009f\u0087\u00a6\u00f0\u009f\u0087\u00b2']
    for sm in smile:
        if sm in text:
            text=re.sub(sm, '', text)
    text = text.lower()
    text = re.sub('\[.*?\]', '', text)
    text = re.sub('\w*\d\w*', '', text)
    text = re.sub('[‘’“”…]', '', text)
    text = re.sub('\n', '', text)
    return text

def create_word_cloud(df,member_name):
	k=df['Sender'].unique()
	dt = {'name': [], 'write': []}
	data=pd.DataFrame.from_dict(dt)
	data['name']=k
	data['write']=str(data['write'])
	for i in range(len(data)):
	    dict_=' '
	    member_message=df[df['Sender']==data['name'][i]]['Message']
	    for j in member_message:
	        if (clean_text_no_split(j)!=''):
	            dict_=clean_text_no_split(j)+dict_
	    data['write'][i]=dict_

	  
	comment_words = ' '
	stopwords = set(STOPWORDS) 
	
	for val in data[data['name']==member_name].write:
	    val = str(val)
	    tokens = val.split()
	    for i in range(len(tokens)): 
	        tokens[i] = tokens[i].lower() 
	          
	    for words in tokens:
	    	if len(words)>4:
	    		comment_words = comment_words + words + ' '
	  
	  
	wordcloud = WordCloud(width = 800, height = 800, 
	                    background_color ='white', 
	                    stopwords = stopwords, 
	                    min_font_size = 10).generate(str(comment_words)) 
	                      
	plt.figure(figsize = (8, 8), facecolor = None) 
	plt.title('Wordcloud of {anun}'.format(anun=member_name))
	plt.imshow(wordcloud) 
	plt.axis("off") 
	plt.tight_layout(pad = 0) 
	plt.savefig("wordcloud.png")

if __name__=='__main__':
	pass