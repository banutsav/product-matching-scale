#!/bin/bash

import time
import pandas as pd
import re
from yattag import Doc
import html
import plotly.express as px
import plotly.graph_objects as go
import plotly.offline as opy
from plotly.subplots import make_subplots

# Save plotted figures to file
def writeResults(figures):
	doc, tag, text = Doc().tagtext()
	# Generate HTML
	with tag('html'):
		with tag('head'):
			with tag('script', src="https://cdn.plot.ly/plotly-latest.min.js"):
				pass
			with tag('title'):
				text('Product Analysis')
		with tag('body'):
			for fig in figures:
				with tag('div'):
					text(fig)
				
	result = doc.getvalue()
	f = open("results.html", "w")
	f.write(html.unescape(result))
	f.close() 

# Bar with data broken down by groups but in separate categories
def barItemsGroupsBins(items):
	groups = items['GroupName'].value_counts()
	size = items.shape[0]
	cat = ['Over 800', '800-500', '500-300','300-200', '100-200']
	counts = [0, 0, 0, 0, 0]
	colors = ['lightsalmon', 'lightblue', 'lightgreen', 'lightseagreen', 'lightgray']
	products = [0, 0, 0, 0, 0]
	bigproducer_count = 0

	# Populate groups based on the categories defines
	for val, cnt in groups.iteritems():
		if cnt<100:
			continue

		if cnt>800:
			counts[0] += 1; products[0] += cnt
		elif cnt>500:
			counts[1] += 1; products[1] += cnt
		elif cnt>300:
			counts[2] += 1; products[2] += cnt
		elif cnt>200:
			counts[3] += 1; products[3] += cnt
		else:
			counts[4] += 1; products[4] += cnt
		bigproducer_count += cnt	

	# Big producer product percentage
	percent = str(round((bigproducer_count/size)*100,2)) + '% from Big Producers'
	# Plot bar graph
	fig = make_subplots(rows=1, cols=2, specs=[[{"type": "xy"}, {"type": "domain"}]]
		, subplot_titles=('',''))		
	fig.add_trace(go.Bar(x=cat, y=counts, marker_color=colors), row=1, col=1)
	fig.add_trace(go.Pie(labels=cat, values=products, marker_colors=colors,hole=.3), row=1, col=2)

	# Set title and hover
	
	hovertext = [str(counts[i])+' producers, selling '+str(products[i])+' products, '+str(round((products[i]/size)*100,2))+'% of Total' 
	for i in range(0,5)]
	fig.update(layout_title_text=str(size)+' products | '+percent, layout_showlegend=False)
	fig.update_traces(hovertext=hovertext, hoverinfo='text')
	plot = opy.plot(fig, auto_open=False, output_type='div', include_plotlyjs=False)
	return plot

# Bar graph of data break-up by group
def barItemsByGroup(items):
	x = []; y = []; colors = []; hovertext = []
	groups = items['GroupName'].value_counts()
	highestgroups = 0; highestgroups_tot = 0
	# Find counts of the highest supplying groups
	for val, cnt in groups.iteritems():
		if cnt<100:
			continue
		x.append(val); y.append(cnt)
		highestgroups += 1; highestgroups_tot += cnt

		# Set colors
		if cnt>800:
			colors.append('lightsalmon')
		elif cnt>500:
			colors.append('lightblue')
		elif cnt>300:
			colors.append('lightgreen')
		elif cnt>200:
			colors.append('lightseagreen')
		else:
			colors.append('lightgray')

		# Create hover text	
		hovertext.append(str(val) + '<br>' + str(cnt) + ' products')

	# Create Title
	title = str(highestgroups) + ' Big Producers contribute ' + str(highestgroups_tot) + ' products'
	# Plotly Bar
	fig = go.Figure()
	fig.add_trace(go.Bar(x=x, y=y, marker_color=colors))
	fig.update_layout(title='A Big Producer contributes over a 100 products', xaxis_title=title)
	fig.update_xaxes(showticklabels=False)
	fig.update_traces(hovertext=hovertext, hoverinfo='text')
	plot = opy.plot(fig, auto_open=False, output_type='div', include_plotlyjs=False)
	return plot

# Call functions to generate visualization figures
def generateFigures(items):
	figures = []
	figures.append(barItemsGroupsBins(items))
	figures.append(barItemsByGroup(items))
	return figures

if __name__ == '__main__':

	t1 = time.time()
	# Read data
	df = pd.read_csv('matched-with-desc.csv', error_bad_lines=False, engine='python', skip_blank_lines=True)
	df.dropna(how='all', inplace=True)
	print('Dataset:',df.shape[0])
	
	# Get values for confidence level between 0-1
	items = df.loc[df['Match Confidence (lower is better)']<1]
	size = items.shape[0]
	print('Confidence Dataset:', size)
	
	# Generate plots and write to file
	figs = generateFigures(items)
	writeResults(figs)

	t = time.time()-t1
	print('Completed in:', round(t,2), 'secs')