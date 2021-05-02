import dash
import dash_core_components as dcc
import dash_html_components as html

import pandas as pd
import numpy as np
import plotly.graph_objects as go



external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__,external_stylesheets=external_stylesheets)



# -------------------------------------------------------------------------------------------------------------- 

#											PART 1: DESIGN PARAMETERS

# --------------------------------------------------------------------------------------------------------------
# Here we will set the colors, margins, DIV height&weight and other parameters

colors = {
		'full-background': 	'#DCDCDC',
		'block-borders': 	'black'
}

margins = {
		'title-margins': '10px 10px 10px 10px',
		'block-margins': '10px 10px 10px 10px'
}

sizes = {
		'subblock-heights': '350px',
}



# -------------------------------------------------------------------------------------------------------------- 

#											PART 2: ACTUAL LAYOUT

# --------------------------------------------------------------------------------------------------------------
# Here we will set the DIV-s and other parts of our layout
# We need too have a 2x2 grid
# I have also included 1 more grid on top of others, where we will show the title of the app



# -------------------------------------------------------------------------------------- DIV for TITLE
div_title = html.Div(children =	html.H1('Homework 6(Dash/Plotly)'),
					style ={
							'border': '3px {} solid'.format(colors['block-borders']),
							'margin': margins['title-margins'],
							'text-align': 'center'
							}
					)

# -------------------------------------------------------------------------------------- DIV for first raw (1.1 and 1.2)
chess_df = pd.read_csv('games.csv')
turns_hist = go.Figure([go.Histogram(x=chess_df['turns'],
									 name='Histogram of turns')])

graph_1=html.Div(children =dcc.Graph (id = 'histogram',
					figure = turns_hist,
					style = {'margin': margins['block-margins'],
							'height': sizes['subblock-heights']}
					))

div_1_1 = html.Div(children = graph_1,
					style = {
							'border': '1px {} solid'.format(colors['block-borders']),
							'margin': margins['block-margins'],
							'width': '49%',
							'height': sizes['subblock-heights'],
					}
				)

box_plot=go.Figure(go.Box(x=chess_df['white_rating'],
                     # hovertext=chess_df['winner'],
                     name='Box plot'))


graph_2=html.Div(children=dcc.Graph(id='box_plot',
	figure=box_plot,
	style = {'margin': margins['block-margins'],
			'height': sizes['subblock-heights']}))

div_1_2 = html.Div(children = graph_2,
					style = {
							'border': '1px {} solid'.format(colors['block-borders']),
							'margin': margins['block-margins'],
							'width': '49%',
							'height': sizes['subblock-heights']
					}
				)




# Collecting DIV 1.1 and 1.2 into the DIV of first raw.
# Pay attention to the 'display' and 'flex-flaw' attributes.
# With this configuration you are able to let the DIV-s 1.1 and 1.2 be side-by-side to each other.
# If you skip them, the DIV-s 1.1 and 1.2 will be ordered as separate rows.
# Pay also attention to the 'width' attributes, which specifiy what percentage of full row will each DIV cover.
div_raw1 = html.Div(children =[div_1_1,
								div_1_2
								],
					style ={
							'border': '3px {} solid'.format(colors['block-borders']),
							'margin': margins['block-margins'],
							'display': 'flex',
							'flex-flaw': 'row-wrap'
							})


# -------------------------------------------------------------------------------------- DIV for second raw (2.1 and 2.2)
scatter_plot=go.Figure(go.Scatter(x=chess_df['white_rating'],y=chess_df['black_rating'],
                     hovertext=chess_df['winner']
								  ,name='Scatter plot'
								  ,mode = 'markers'))
graph_3=html.Div(children=dcc.Graph(id='scatter_plot',
	figure=scatter_plot,
	style = {'margin': margins['block-margins'],
			'height': sizes['subblock-heights']}))

div_2_1 = html.Div(children = graph_3,
					style ={
							'border': '1px {} solid'.format(colors['block-borders']),
							'margin': margins['block-margins'],
							'width': '49%',
							'height': sizes['subblock-heights']
					}
				)


scatter_plot_2=go.Figure(go.Scatter(x=chess_df['white_rating'],y=chess_df['turns'],
                     hovertext=chess_df['opening_name'],
						  name='Scatter plot 2',
									mode = 'markers'))
graph_4=html.Div(children=dcc.Graph(id='scatter_plot_2',
	figure=scatter_plot_2,
	style = {'margin': margins['block-margins'],
			'height': sizes['subblock-heights']}))

div_2_2 = html.Div(children = graph_4,
					style = {
							'border': '1px {} solid'.format(colors['block-borders']),
							'margin': margins['block-margins'],
							'width': '49%',
							'height': sizes['subblock-heights']
					}
				)



div_raw2 = html.Div(children =	[div_2_1,
								div_2_2
								],
					style ={
							'border': '3px {} solid'.format(colors['block-borders']),
							'margin': margins['block-margins'],
							'display': 'flex',
							'flex-flaw': 'row-wrap'
							})

# -------------------------------------------------------------------------------------- Collecting all DIV-s in the final layout
# Here we collect all DIV-s into a final layout DIV

app.layout = html.Div(	[
						div_title,
						div_raw1,
						div_raw2
						],
						style = {
							'backgroundColor':colors['full-background']
						}
					)




# -------------------------------------------------------------------------------------------------------------- 

#											PART 3: RUNNING THE APP

# --------------------------------------------------------------------------------------------------------------
# >> use __ debug=True __ in order to be able to see the changes after refreshing the browser tab,
#			 don't forget to save this file before refreshing
# >> use __ port = 8081 __ or other number to be able to run several apps simultaneously
app.run_server(debug=True,  port = 8083)