import dash
import dash_table
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_html_components as html
from dash.dependencies import Input, Output


import pandas as pd
import numpy as np
import plotly.graph_objects as go
from pprint import pprint
import functions_n

import json
import datetime
from datetime import datetime
from pytz import timezone
import re
import random
import os
from wordcloud import WordCloud, STOPWORDS
import io
import base64


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__,external_stylesheets=external_stylesheets)

df=functions_n.create_data_frame()
df['By days']=df['Year'].astype(str)+'/'+df['Month'].astype(str)+'/'+df['Day'].astype(str)

########################################################################################
###############################           ##############################################
############################### PARAMETRS ##############################################
###############################           ##############################################
########################################################################################



color_choices = {
	'light-blue': '#7FAB8',
	'light-grey': '#F7EFED',
	'light-red':  '#F1485B',
	'dark-blue':  '#33546D',
	'middle-blue': '#61D4E2'
}


colors = {
		'full-background':		color_choices['light-grey'],
		'chart-background':		color_choices['light-grey'],
		'block-borders':		color_choices['dark-blue']
}

margins = {
		'block-margins': '10px 10px 10px 10px',
		'block-margins': '4px 4px 4px 4px'
}

sizes = {
		'subblock-heights': '290px'
}

####################################################################################
###############################       ##############################################
############################### TITLE ##############################################
###############################       ##############################################
####################################################################################

div_title = html.Div(children =	[html.H1('Messenger Data Interactive Analysis From    {from_}    to    {to_}'.format(from_=df['By days'][len(df['By days'])-1],
																											to_=df['By days'][0])),
								 html.Img(src='/assets/mess_logo.png')],
	className='banner'
					)


####################################################################################
###############################       ##############################################
############################### DIV 1 ##############################################
###############################       ##############################################
####################################################################################



div_1_1_stats=[]
div_1_1_stats.append(html.Div(children =html.H2('Chat Information' ),className="banner h2",
					style ={
							#'border': '3px {} solid'.format(colors['block-borders']),
							# 'margin': margins['block-margins'],
							'text-align': 'center',
							# 'color': 'white'
							}
					))
for i in range(9):
	div_1_1_stats.append(html.Div(children =html.H4(functions_n.group_wise_stats_string(df)[i],
								  className="menu-title"),
					style ={
							#'border': '3px {} solid'.format(colors['block-borders']),
							'margin': margins['block-margins'],
							'text-align': 'center'
							}
					))



div_1_1 = html.Div(children = div_1_1_stats,

					style = {
							'border': '1px {} solid'.format(colors['block-borders']),
							'margin': margins['block-margins'],
							'width': '20%',
							'height': 600,
					},
					        

				)


div_figure_1_2=go.Figure()
div_figure_1_2.add_trace(go.Bar(
	y=df['Sender'].value_counts().sort_values(ascending=True).index,
	x=df['Sender'].value_counts().sort_values(ascending=True),
	name='Name of plot',orientation='h',
	text=df['Sender'].value_counts().sort_values(ascending=True),
	textposition='outside'))
div_figure_1_2.update_layout(dict(
								title='Count of messages written by each member',
					    		xaxis={'title': 'Count of messages',
					   					
					   					},
					            yaxis={'title': 'Names', 
					            		# 'showgrid': False,
					            		#'showticklabels': False
					            		},
					            # autosize=False,
					           	paper_bgcolor = colors['chart-background'],
					           	plot_bgcolor = colors['chart-background'],
					           	# margin={'l': 0, 'b': 0, 't': 0, 'r': 10},
					            legend={'x': 0, 'y': 1},
					            boxmode='group'
					            )
	)
div_1_2_graph = dcc.Graph(
						id = 'bar_plot_type',
						figure=div_figure_1_2,
						style={'height': 600,})

						
div_1_2 = html.Div(children = [div_1_2_graph],
					style = {
							'border': '1px {} solid'.format(colors['block-borders']),
							'margin': margins['block-margins'],
							'width': '80%',
							'height': 600,
							
					}
				)


							

div_row1 = html.Div(children =	[div_1_1,
								div_1_2],
					style ={
							# 'border': '3px {} solid'.format(colors['block-borders']),
							'margin': margins['block-margins'],
							'display': 'flex',
							'flex-flaw': 'row-wrap',
							'height': 600,
							})



####################################################################################
###############################       ##############################################
############################### DIV 2 ##############################################
###############################       ##############################################
####################################################################################



option_year=[]
for i in df['Year'].value_counts().sort_index(ascending=True).index:
    option_year.append(
        {'label': str(i), 'value': i}
    )

div_2_button_year = html.Div(
	children=[
	html.Label(
		['Year'],
		style={
		'font-weight': 'bold',
		"text-align": "center"
		}
		, className="menu-title"
		),
	dcc.Dropdown(
		id = 'dropdown_year',
		options=option_year,
		value=df['Year'].value_counts().sort_index(ascending=True).index[0],
		# className="dropdown"
		# style=
		)
	]
)

div_2_button_month = html.Div(
	children=[
	html.Label(
		['Month'],
		style={
		'font-weight': 'bold',
		"text-align": "center"
		},
		className="menu-title"
		),
	dcc.Dropdown(
		id = 'dropdown_month',
		options=[]
		)
	]
)

div_2_1_graph = dcc.Graph(
					id = 'time_wise_stat',
					style={'width': '90%'}

					)



div_2_buttons = html.Div(children =	[div_2_button_year, div_2_button_month],
					style ={
							# 'border': '3px {} solid'.format(colors['block-borders']),
							# 'margin': margins['block-margins'],
							'width': '10%',
							# 'display': 'flex',
							# 'flex-flaw': 'row-wrap'
							})
div_row2 = html.Div(children =	[div_2_buttons, div_2_1_graph],
					style ={
							'border': '3px {} solid'.format(colors['block-borders']),
							'height': 700,
							'margin': margins['block-margins'], 
							'display': 'flex',
							'flex-flaw': 'row-wrap'
							})


####################################################################################
###############################       ##############################################
############################### DIV 3 ##############################################
###############################       ##############################################
####################################################################################


option_member=[]
for i in df['Sender'].value_counts().sort_index(ascending=True).index:
    option_member.append(
        {'label': str(i), 'value': i}
    )

div_3_button_member = html.Div(
	children=[
	html.Label(
		['Member'],
		style={
		'font-weight': 'bold',
		"text-align": "center"
		}
		),
	dcc.Dropdown(
		id = 'dropdown_member_div3',
		options=option_member,
		value=df['Sender'].value_counts().sort_index(ascending=True).index[0],
		)
	],
	style={'width': '25%'},
)

div_3_tab_1_graph = dcc.Graph(
						id = 'div_3_tab_1_graph',
						style={'width': '75%'},
						)

div_row3_tab_1 = html.Div(children =[div_3_button_member, div_3_tab_1_graph],
					style ={
							'border': '3px {} solid'.format(colors['block-borders']),
							'height': 700,
							'margin': margins['block-margins'], 
							'display': 'flex',
							'flex-flaw': 'row-wrap'
							})


option_type=[]
for i in functions_n.all_information(df).columns:
    option_type.append(
        {'label': str(i), 'value': i}
    )

div_3_button_type = html.Div(
	children=[
	html.Label(
		['Message type'],
		style={
		'font-weight': 'bold',
		"text-align": "center"
		}
		),
	dcc.Dropdown(
		id = 'dropdown_type_div3',
		options=option_type,
		value=functions_n.all_information(df).columns[0],
		)
	],
	style={'width': '25%'},
)

div_3_tab_2_graph = dcc.Graph(
						id = 'div_3_tab_2_graph',
						style={'width': '75%'},
						)

div_row3_tab_2 = html.Div(children =[div_3_button_type, div_3_tab_2_graph],
					style ={
							'border': '3px {} solid'.format(colors['block-borders']),
							'height': 700,
							'margin': margins['block-margins'], 
							'display': 'flex',
							'flex-flaw': 'row-wrap'
							})





div_row_3_tab_3=dash_table.DataTable(
	id='table',
    columns=[{"name": i, "id": i} for i in functions_n.all_information(df).reset_index().columns],
    data=functions_n.all_information(df).reset_index().to_dict('records'),
)

div_row_3_tab_3 = html.Div(children =[div_row_3_tab_3],
					style ={
							'border': '3px {} solid'.format(colors['block-borders']),
							'height': 700,
							'margin': margins['block-margins'], 
							# 'display': 'flex',
							# 'flex-flaw': 'row-wrap'
							})


div_row3_tabs = dcc.Tabs(
        id="tabs-with-classes",
        value='barplot_tab',
        parent_className='custom-tabs',
        className='custom-tabs-container',
        children=[
            dcc.Tab(
                label='Count of messages by type',
                value='barplot_tab',
                className='custom-tab',
                selected_className='custom-tab--selected',
            ),
            dcc.Tab(
                label='Count of messages by member',
                value='type_bar_plot',
                className='custom-tab',
                selected_className='custom-tab--selected'
            ),
            dcc.Tab(
                label='Informative table',
                value='table_tab',
                className='custom-tab',
                selected_className='custom-tab--selected'
            )
        ])

div_row3_each_tab=html.Div(id='tabs-content-classes')


div_row3 = html.Div(children =	[div_row3_tabs ,div_row3_each_tab],
					style ={
							# 'border': '3px {} solid'.format(colors['block-borders']),
							'margin': margins['block-margins'], 
							# 'display': 'flex',
							# 'flex-flaw': 'row-wrap'
							}
							)


####################################################################################
###############################       ##############################################
############################### DIV 4 ##############################################
###############################       ##############################################
####################################################################################







# -------------------------------------------------------------------------------------

div_4_button_member = html.Div(
	children=[
	html.Label(
		['Select members'],
		style={
		'font-weight': 'bold',
		"text-align": "center"
		}
		),
	dcc.Dropdown(
		id = 'dropdown_member_div4',
		options=option_member,
		value=df['Sender'].value_counts().sort_index(ascending=True).index,
		multi=True)
	]
)


div_4_graph = dcc.Graph(
						id = 'daily_boxplot',
						# style={'width': '80%'},
						)



div_4_button_member = html.Div(children =	[div_4_button_member],
					style ={
							# 'border': '3px {} solid'.format(colors['block-borders']),
							# 'margin': margins['block-margins'],
							# 'width': '10%',
							# 'display': 'flex',
							'flex-flaw': 'row-wrap'
							})
div_row4 = html.Div(children =	[div_4_button_member, div_4_graph],
					style ={
							'border': '3px {} solid'.format(colors['block-borders']),
							'height': 700,
							'margin': margins['block-margins'], 
							# 'display': 'flex',
							'flex-flaw': 'row-wrap'
							})



####################################################################################
###############################       ##############################################
############################### DIV 5 ##############################################
###############################       ##############################################
####################################################################################


option_member=[]
for i in [*functions_n.number_each_emojis(df).keys()]:
    option_member.append(
        {'label': str(i), 'value': i}
    )


div_5_smile_index=html.Img(src='data:image/png;base64,{}'.format(base64.b64encode(open('smile_index.jpg', 'rb').read()).decode('ascii')),
			style={'height': 350,'width':450})

div_5_button_member = html.Div(
	children=[
	html.Label(
		['Member'],
		style={
		'font-weight': 'bold',
		"text-align": "center"
		}
		),
	dcc.Dropdown(
		id = 'dropdown_member_div5',
		options=option_member,
		value=option_member[0]['value'],
		),
	div_5_smile_index
	],
	style={'width': '25%'},
)

div_5_tab_1_graph = dcc.Graph(
						id = 'div_5_tab_1_graph',
						style={'width': '75%'},
						)

div_row5_tab_1 = html.Div(children =[div_5_button_member, div_5_tab_1_graph],
					style ={
							'border': '3px {} solid'.format(colors['block-borders']),
							'height': 700,
							'margin': margins['block-margins'], 
							'display': 'flex',
							'flex-flaw': 'row-wrap'
							})



option_type=[]
for i in [*functions_n.emojis_by_member(df).keys()]:
    option_type.append(
        {'label': str(i), 'value': i}
    )


div_5_button_type = html.Div(
	children=[
	html.Label(
		['Emojis type'],
		style={
		'font-weight': 'bold',
		"text-align": "center"
		}
		),
	dcc.Dropdown(
		id = 'dropdown_type_div5',
		options=option_type,
		value=option_type[0]['value'],
		),
	div_5_smile_index
	],
	style={'width': '25%'},
)

div_5_tab_2_graph = dcc.Graph(
						id = 'div_5_tab_2_graph',
						style={'width': '75%'},
						)

div_row5_tab_2 = html.Div(children =[div_5_button_type, div_5_tab_2_graph],
					style ={
							'border': '3px {} solid'.format(colors['block-borders']),
							'height': 700,
							'margin': margins['block-margins'], 
							'display': 'flex',
							'flex-flaw': 'row-wrap'
							})


div_5_smile_index_tab_3=html.Img(src='data:image/png;base64,{}'.format(base64.b64encode(open('smile_index.jpg', 'rb').read()).decode('ascii')),
			style={'width':'30%',
					'height': 350})

div_row5_tab_3=html.Div(
	children=dash_table.DataTable(
									id='table_5_3',
								    columns=[{"name": i, "id": i} for i in functions_n.most_emoji_table(df).columns],
								    data=functions_n.most_emoji_table(df).to_dict('records')
								  ),
    style={'width': '70%'},
)

div_row5_tab_3 = html.Div(children =[div_5_smile_index_tab_3,div_row5_tab_3],
					style ={
							'border': '3px {} solid'.format(colors['block-borders']),
							'height': 700,
							'margin': margins['block-margins'], 
							'display': 'flex',
							'flex-flaw': 'row-wrap'
							})



div_row5_tabs = dcc.Tabs(
        id="tabs-with-classes_5",
        value='barplot_tab_5',
        parent_className='custom-tabs',
        className='custom-tabs-container',
        children=[
            dcc.Tab(
                label='Number of each type emojis',
                value='barplot_tab_5',
                className='custom-tab',
                selected_className='custom-tab--selected',
            ),
            dcc.Tab(
                label='Number of selected emoji by each member',
                value='type_bar_plot_5',
                className='custom-tab',
                selected_className='custom-tab--selected'
            ),
            dcc.Tab(
                label='Emoji table',
                value='table_tab_5',
                className='custom-tab',
                selected_className='custom-tab--selected'
            )
        ])

div_row5_each_tab=html.Div(id='tabs-content-classes_5')


div_row5 = html.Div(children =	[div_row5_tabs ,div_row5_each_tab],
					style ={
							# 'border': '3px {} solid'.format(colors['block-borders']),
							'margin': margins['block-margins'], 
							# 'display': 'flex',
							# 'flex-flaw': 'row-wrap'
							}
							)


####################################################################################
###############################       ##############################################
############################### DIV 6 ##############################################
###############################       ##############################################
####################################################################################


reaction_df=functions_n.reaction_data()
option_member_1_div6=[]
for i in reaction_df['Reaction sender'].value_counts().sort_index(ascending=True).index:
    option_member_1_div6.append(
        {'label': str(i), 'value': i}
    )
option_member_2_div6=[]
for i in reaction_df['Message sender'].value_counts().sort_index(ascending=True).index:
    option_member_2_div6.append(
        {'label': str(i), 'value': i}
    )

div_6_member_1_button = html.Div(
	children=[
	html.Label(
		['Reaction sender name'],
		style={
		'font-weight': 'bold',
		"text-align": "center"
		}
		),
	dcc.Dropdown(
		id = 'dropdown_div_6_member_1',
		options=option_member_1_div6,
		value=option_member_1_div6[0]['value'],
		# style=
		)
	]
)

div_6_member_2_button = html.Div(
	children=[
	html.Label(
		['Message sender name'],
		style={
		'font-weight': 'bold',
		"text-align": "center"
		}
		),
	dcc.Dropdown(
		id = 'dropdown_div_6_member_2',
		options=option_member_2_div6,
		value=option_member_2_div6[0]['value'],
		# style=
		)
	]
)

div_6_type_1_button = html.Div(
	children=[
	html.Label(
		['Reaction sender Name'],
		style={
		'font-weight': 'bold',
		"text-align": "center"
		}
		),
	dcc.Dropdown(
		id = 'dropdown_div_6_type_1',
		options=[]
		)
	]
)

div_6_type_2_button = html.Div(
	children=[
	html.Label(
		['Message sender Name'],
		style={
		'font-weight': 'bold',
		"text-align": "center"
		}
		),
	dcc.Dropdown(
		id = 'dropdown_div_6_type_2',
		options=[]
		)
	]
)

div_6_graph = dcc.Graph(
						id = 'div_6_graph',
						style={'width': '80%'},
						)



div_6_buttons = html.Div(children =	[div_6_member_1_button, div_6_member_2_button,div_6_type_1_button,div_6_type_2_button],
					style ={
							# 'border': '3px {} solid'.format(colors['block-borders']),
							# 'margin': margins['block-margins'],
							'width': '20%',
							# 'display': 'flex',
							# 'flex-flaw': 'row-wrap'
							})
div_row6 = html.Div(children =	[div_6_buttons, div_6_graph],
					style ={
							'border': '3px {} solid'.format(colors['block-borders']),
							'height': 700,
							'margin': margins['block-margins'], 
							'display': 'flex',
							'flex-flaw': 'row-wrap'
							})




####################################################################################
###############################       ##############################################
############################### DIV 7 ##############################################
###############################       ##############################################
####################################################################################


div_row7_1=dash_table.DataTable(
	id='table_div7',
    columns=[{"name": i, "id": i} for i in functions_n.most_used_word(df).columns],
    data=functions_n.most_used_word(df).to_dict('records'),
)
div_7_title=html.Div(children =html.H2('Most used word by each member' ),className="banner h2",
					style ={
							#'border': '3px {} solid'.format(colors['block-borders']),
							# 'margin': margins['block-margins'],
							'text-align': 'center',
							# 'color': 'white'
							}
					)
div_row7_1 = html.Div(children =[div_7_title,div_row7_1],
					style = {
							'border': '1px {} solid'.format(colors['block-borders']),
							'margin': margins['block-margins'],
							'width': '40%',
							#'height': sizes['subblock-heights'],
					})


most_used_data=functions_n.most_used_word(df)
option_div7_2=[]
for i in most_used_data['Message sender']:
    option_div7_2.append(
        {'label': str(i), 'value': i}
    )

div_7_2_button = html.Div(
	children=[
	html.Label(
		['Select member name'],
		style={
		'font-weight': 'bold',
		"text-align": "center"
		}
		),
	dcc.Dropdown(
		id = 'dropdown_div_7_2',
		options=option_div7_2,
		value=option_div7_2[0]['value'],
		# style=
		)
	]
)

div_7_2_cloud=html.Div(children = [],
					   id='word_cloud',
					   style={
					   'height': 600,
					   })

div_row7_2 = html.Div(children = [div_7_2_button,div_7_2_cloud],
					style = {
							'border': '1px {} solid'.format(colors['block-borders']),
							'margin': margins['block-margins'],
							'width': '60%',
							'height': 600,
					}
				)


div_row7 = html.Div(children =	[div_row7_1,
								div_row7_2
								],
					style ={
							'border': '3px {} solid'.format(colors['block-borders']),
							'margin': margins['block-margins'],
							'display': 'flex',
							'flex-flaw': 'row-wrap'
							})



app.layout = html.Div(	[
						div_title,
						div_row1,
						div_row2,
						div_row3,
						div_row4,
						div_row5,
						div_row6,
						div_row7
						],
						style = {
							'backgroundColor': colors['full-background']
						}
					)

####################################################################################
###############################           ##########################################
############################### CALLBACKS ##########################################
###############################           ##########################################
####################################################################################


####################################################################################
###############################           ##########################################
############################### CALLBACKS ##########################################
###############################   ROW 2   ##########################################
###############################           ##########################################
####################################################################################

@app.callback(
    [Output('dropdown_month', 'options'),
    Output('dropdown_month', 'value')],
    [Input('dropdown_year', 'value')])
def set_month_option(year_value):
    month_by_year={}
    for i in df['Year'].value_counts().sort_index(ascending=True).index:
        month_by_year[i]=list(df[df['Year']==i]['Month'].unique())
    output_options = []
    output_options.extend(month_by_year[year_value])

    return [{'label': i, 'value': i} for i in output_options], output_options[0]


@app.callback(
    Output('time_wise_stat', 'figure'),
    [Input('dropdown_month', 'value'),
     Input('dropdown_year', 'value')]
)
def graph_create(months,year):
    traces = []
    if months:
    	from plotly.subplots import make_subplots
    	fig=make_subplots(rows=2,cols=2,
		                  specs=[[{}, {}],[{"colspan": 2}, None]],
		                  subplot_titles=("Count of messages by hour",
		                                  "Count of messages by weekday",
		                                  "Count of messages by day"))
    	df['Hour'] = pd.Categorical(df['Hour'],
		                           categories=list(np.arange(24)),
		                           ordered=True)
    	fig.add_trace(go.Bar(x=df[((df['Year']==year) & (df['Month']==months))]['Hour'].value_counts().sort_values(ascending=True).index,
		                     y=df[((df['Year']==year) & (df['Month']==months))]['Hour'].value_counts().sort_values(ascending=True),
		                     name='By hour',
		                     orientation='v',
		                     showlegend=False
		#                      text=df['Hour'].value_counts().sort_values(ascending=True),
		#                      textposition='outside'
		                    ), #legend name
		              row=1,col=1)
    	df['WeekDay'] = pd.Categorical(df['WeekDay'],
		                            categories=["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"],
		                            ordered=True)
    	fig.add_trace(go.Bar(x=df[((df['Year']==year) & (df['Month']==months))]['WeekDay'].value_counts().sort_index(ascending=True).index,
		                     y=df[((df['Year']==year) & (df['Month']==months))]['WeekDay'].value_counts().sort_index(ascending=True),
		                     name='By weekday',
		                     orientation='v',
		                     showlegend=False
		#                      text=df['Hour'].value_counts().sort_values(ascending=True),
		#                      textposition='outside'
		                    ), #legend name
		              row=1,col=2)
    	df['Day'] = pd.Categorical(df['Day'],
		                           categories=list(np.arange(32)),
		                           ordered=True)
    	fig.add_trace(go.Bar(x=df[((df['Year']==year) & (df['Month']==months))]['Day'].value_counts().sort_index(ascending=True).index,
		                     y=df[((df['Year']==year) & (df['Month']==months))]['Day'].value_counts().sort_index(ascending=True),
		                     name='By day',
		                     orientation='v',
		                     showlegend=False
		#                      text=df['Hour'].value_counts().sort_values(ascending=True),
		#                      textposition='outside'
		                    ), #legend name
		              row=2,col=1)
    	fig.update_layout(
    	dict(#autosize=False,
    		title_text="Count of messages over time",
           	paper_bgcolor = colors['chart-background'],
           	plot_bgcolor = colors['chart-background'],
           	autosize=True,
            # margin={'l': 40, 'b': 40, 't': 10, 'r': 10},
            legend={'x': 0, 'y': 1},
            boxmode='group',
	        ) )
    return fig


####################################################################################
###############################           ##########################################
############################### CALLBACKS ##########################################
###############################   ROW 3   ##########################################
###############################           ##########################################
####################################################################################


@app.callback(Output('tabs-content-classes', 'children'),
              Input('tabs-with-classes', 'value'))
def render_content(tab):
    if tab == 'barplot_tab':
        return div_row3_tab_1
    elif tab == 'type_bar_plot':
    	return div_row3_tab_2
    elif tab == 'table_tab':
        return div_row_3_tab_3


@app.callback(
    Output('div_3_tab_1_graph', 'figure'),
    [Input('dropdown_member_div3', 'value')]
)
def graph_tab_3_1(member_name):
    #traces = []
    fig = go.Figure()
    if member_name:
    	data_all=functions_n.all_information(df).T.sort_values(by=member_name, ascending=True)
    	fig=go.Figure()
    	fig.add_trace(go.Bar(
    		y=data_all[member_name].index,
			x=data_all[member_name],
			name='Name of plot',orientation='h',
			text=data_all[member_name],
			textposition='outside'))
    	fig.update_layout(dict(
						    		xaxis={'title': 'Count',
						   					
						   					},
						            yaxis={'title': 'Type', 
						            		# 'showgrid': False,
						            		#'showticklabels': False
						            		},
						            #autosize=False,
						           	paper_bgcolor = colors['chart-background'],
						           	plot_bgcolor = colors['chart-background'],
						           	margin={'l': 40, 'b': 40, 't': 10, 'r': 10},
						            legend={'x': 0, 'y': 1},
						            # boxmode='group'
						            )
		)

    return fig



@app.callback(
    Output('div_3_tab_2_graph', 'figure'),
    [Input('dropdown_type_div3', 'value')]
)
def graph_tab_3_2(mess_type):
    #traces = []
    fig = go.Figure()
    if mess_type:
    	data_all=functions_n.all_information(df).sort_values(by=mess_type, ascending=True)
    	fig=go.Figure()
    	fig.add_trace(go.Bar(
    		y=data_all[mess_type].index,
			x=data_all[mess_type],
			name='Name of plot',orientation='h',
			text=data_all[mess_type],
			textposition='outside'))
    	fig.update_layout(dict(
						    		xaxis={'title': 'Count',
						   					
						   					},
						            yaxis={'title': 'Member', 
						            		# 'showgrid': False,
						            		#'showticklabels': False
						            		},
						            #autosize=False,
						           	paper_bgcolor = colors['chart-background'],
						           	plot_bgcolor = colors['chart-background'],
						           	margin={'l': 40, 'b': 40, 't': 10, 'r': 10},
						            legend={'x': 0, 'y': 1},
						            # boxmode='group'
						            )
		)

    return fig

####################################################################################
###############################           ##########################################
############################### CALLBACKS ##########################################
###############################   ROW 4   ##########################################
###############################           ##########################################
####################################################################################


@app.callback(
    Output('daily_boxplot', 'figure'),
    [Input('dropdown_member_div4', 'value')]
)
def graph_create(member_names):
	import plotly.figure_factory as ff
	df_group_day=df.groupby(['By days']).count()['Message'].values
	traces = []
	fig = go.Figure()
	if member_names:
		# colors = ['#333F44', '#37AA9C', '#94F3E4']
		for i in member_names:
			fig.add_trace(
		    			go.Box(
		    				y=df[df['Sender']==i].groupby(['By days']).count()['Message'].values,
		    				# x=member_names,
		    				name=i,
		    				showlegend=False
		    				# marker = dict(color=drug_colors[drug_name])
		    				)
		    			)
			fig.update_layout(
			dict(#autosize=False,
				title_text='Boxplots of daily messages by members',
		       	paper_bgcolor = colors['chart-background'],
		       	plot_bgcolor = colors['chart-background'],
		        margin={'l': 0, 'b': 0, 't': 50, 'r': 0},
		        legend={'x': 0, 'y': 1},
		        # boxmode='group',
		        ) )
	return fig


####################################################################################
###############################           ##########################################
############################### CALLBACKS ##########################################
###############################   ROW 5   ##########################################
###############################           ##########################################
####################################################################################


@app.callback(Output('tabs-content-classes_5', 'children'),
              Input('tabs-with-classes_5', 'value'))
def render_content(tab):
    if tab == 'barplot_tab_5':
        return div_row5_tab_1
    elif tab == 'type_bar_plot_5':
    	return div_row5_tab_2
    elif tab == 'table_tab_5':
        return div_row5_tab_3


@app.callback(
    Output('div_5_tab_1_graph', 'figure'),
    [Input('dropdown_member_div5', 'value')]
)
def graph_tab_5_1(member_name):
    #traces = []
    fig = go.Figure()
    if member_name:
    	data_all=pd.DataFrame.from_dict(functions_n.number_each_emojis(df)[member_name],
								    	orient='index',
								    	columns=['Count']).reset_index().sort_values(by='Count', ascending=True)
    	data_all['index'] = data_all['index'].astype('str')
    	fig=go.Figure()
    	fig.add_trace(go.Bar(
    		y=data_all['index'],
			x=data_all['Count'],
			name='Name of plot',orientation='h',
			text=data_all['Count'],
			textposition='outside'))
    	fig.update_layout(dict(
						    		xaxis={'title': 'Count',
						   					
						   					},
						            yaxis={'title': 'Type', 
						            		# 'showgrid': False,
						            		#'showticklabels': False
						            		},
						            #autosize=False,
						           	paper_bgcolor = colors['chart-background'],
						           	plot_bgcolor = colors['chart-background'],
						           	margin={'l': 40, 'b': 40, 't': 10, 'r': 10},
						            legend={'x': 0, 'y': 1},
						            # boxmode='group'
						            )
		)

    return fig

@app.callback(
    Output('div_5_tab_2_graph', 'figure'),
    [Input('dropdown_type_div5', 'value')]
)
def graph_tab_5_2(index_type):
    #traces = []
    fig = go.Figure()
    if index_type:
    	data_all=pd.DataFrame.from_dict(functions_n.emojis_by_member(df)[index_type],
		                                orient='index',
		                                columns=['Count']).reset_index().sort_values(by='Count', ascending=True)
    	fig.add_trace(go.Bar(
    		y=data_all['index'],
			x=data_all['Count'],
			name='Name of plot',orientation='h',
			text=data_all['Count'],
			textposition='outside'))
    	fig.update_layout(dict(
						    		xaxis={'title': 'Count',
						   					
						   					},
						            yaxis={'title': 'Type', 
						            		# 'showgrid': False,
						            		#'showticklabels': False
						            		},
						            #autosize=False,
						           	paper_bgcolor = colors['chart-background'],
						           	plot_bgcolor = colors['chart-background'],
						           	margin={'l': 40, 'b': 40, 't': 10, 'r': 10},
						            legend={'x': 0, 'y': 1},
						            # boxmode='group'
						            )
		)

    return fig

####################################################################################
###############################           ##########################################
############################### CALLBACKS ##########################################
###############################   ROW 6   ##########################################
###############################           ##########################################
####################################################################################

@app.callback(
    [Output('dropdown_div_6_type_1', 'options'),
     Output('dropdown_div_6_type_1', 'value')],
    [Input('dropdown_div_6_member_1', 'value')])
def set_div6_options(member_1_name):
    type_by_member_1={}
    for i in reaction_df['Reaction sender'].value_counts().sort_index(ascending=True).index:
        type_by_member_1[i]=list(reaction_df[reaction_df['Reaction sender']==i]['Reaction type'].unique())
    output_options_type_1 = []
    output_options_type_1.extend(type_by_member_1[member_1_name])

    return [{'label': i, 'value': i} for i in output_options_type_1], output_options_type_1[0]


@app.callback(
    [Output('dropdown_div_6_type_2', 'options'),
     Output('dropdown_div_6_type_2', 'value')],
    [Input('dropdown_div_6_member_2', 'value')])
def set_div6_options(member_2_name):
    type_by_member_2={}
    for i in reaction_df['Message sender'].value_counts().sort_index(ascending=True).index:
        type_by_member_2[i]=list(reaction_df[reaction_df['Message sender']==i]['Reaction type'].unique())
    output_options_type_2 = []
    output_options_type_2.extend(type_by_member_2[member_2_name])

    return [{'label': i, 'value': i} for i in output_options_type_2], output_options_type_2[0]


@app.callback(
    Output('div_6_graph', 'figure'),
    [Input('dropdown_div_6_member_1', 'value'),
     Input('dropdown_div_6_member_2', 'value'),
     Input('dropdown_div_6_type_1', 'value'),
     Input('dropdown_div_6_type_2', 'value')]
)
def graph_create(member_1_name,member_2_name,type_1_name,type_2_name):
    traces = []
    if ([member_1_name,member_2_name,type_1_name,type_2_name]):
    	from plotly.subplots import make_subplots

    	if len(reaction_df[(reaction_df['Reaction sender']==member_1_name) & (reaction_df['Reaction type']==type_1_name)]['Message sender'].value_counts().index)<=5:
    		title_6_3='Members given {} reactions by {}'.format(type_1_name,member_1_name)
    		data_react_6_3=reaction_df[(reaction_df['Reaction sender']==member_1_name) & (reaction_df['Reaction type']==type_1_name)]['Message sender'].value_counts().sort_values(ascending=True)
    	else:
    		title_6_3='Top 5 members given {} reaction by {}'.format(type_1_name,member_1_name)
    		data_react_6_3=reaction_df[(reaction_df['Reaction sender']==member_1_name) & (reaction_df['Reaction type']==type_1_name)]['Message sender'].value_counts().sort_values(ascending=True)[:5]
    	
    	if len(reaction_df[(reaction_df['Message sender']==member_2_name) & (reaction_df['Reaction type']==type_2_name)]['Reaction sender'].value_counts().index)<=5:
    		title_6_4='Members gived {} reactions to {}'.format(type_2_name,member_2_name)
    		data_react_6_4=reaction_df[(reaction_df['Message sender']==member_2_name) & (reaction_df['Reaction type']==type_2_name)]['Reaction sender'].value_counts().sort_values(ascending=True)

    	else:
    		title_6_4='Top 5 members gived {} reaction to {}'.format(type_2_name,member_2_name)
    		data_react_6_4=reaction_df[(reaction_df['Message sender']==member_2_name) & (reaction_df['Reaction type']==type_2_name)]['Reaction sender'].value_counts().sort_values(ascending=True)[:5]

    	fig = make_subplots(2, 2, specs=[[{'type':'pie'},{'type':'pie'}],[{'type':'bar'},{'type':'bar'}]],
		                    subplot_titles=['Reactions given by {}'.format(member_1_name),
		                    				'Reactions given to {}'.format(member_2_name),
		                    				title_6_3,title_6_4]
		                   )
    	fig.add_trace(go.Pie(labels=reaction_df[reaction_df['Reaction sender']==member_1_name]['Reaction type'].value_counts().index,
		                     values=reaction_df[reaction_df['Reaction sender']==member_1_name]['Reaction type'].value_counts(),
		                    ), 1, 1)
    	fig.add_trace(go.Pie(labels=reaction_df[reaction_df['Message sender']==member_2_name]['Reaction type'].value_counts().index,
		                     values=reaction_df[reaction_df['Message sender']==member_2_name]['Reaction type'].value_counts(),
		                    ), 1, 2)

    	
    	fig.add_trace(go.Bar(
		    y=data_react_6_3.index,
		    x=data_react_6_3,
		    name='Name of plot_6_3',orientation='h',
		    text=data_react_6_3,
		    textposition='outside',showlegend=False), 2, 1)

    	fig.add_trace(go.Bar(
		    y=data_react_6_4.index,
		    x=data_react_6_4,
		    name='Name of plot_6_4',orientation='h',
		    text=data_react_6_4,
		    textposition='outside',showlegend=False), 2, 2)
    	fig.update_layout(
    	dict(#autosize=False,
			title_text='Reaction Statistics',
		   	paper_bgcolor = colors['chart-background'],
		   	plot_bgcolor = colors['chart-background'],
		    # margin={'l': 40, 'b': 40, 't': 10, 'r': 10},
		    legend={'x': 0, 'y': 1},
		    # boxmode='group',
		    ) )
    return fig


####################################################################################
###############################           ##########################################
############################### CALLBACKS ##########################################
###############################   ROW 7   ##########################################
###############################           ##########################################
####################################################################################

@app.callback(Output('word_cloud', 'children'),
              Input('dropdown_div_7_2', 'value'))
def render_content(member_name):
	df_copy=df.copy()
	functions_n.create_word_cloud(df_copy,member_name)

	test_base64 = base64.b64encode(open('wordcloud.png', 'rb').read()).decode('ascii')

	return  html.Img(src='data:image/png;base64,{}'.format(test_base64),
					style={'height': 500,
					# 'width':'10%'
					})



####################################################################################
###############################           ##########################################
###############################  RUNNING  ##########################################
###############################  THE APP  ##########################################
###############################           ##########################################
####################################################################################

if __name__ == '__main__':
	app.run_server(debug=True, port = 8081)