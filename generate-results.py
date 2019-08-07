#!/bin/bash

import time
import pandas as pd
import re

if __name__ == '__main__':

	t1 = time.time()
	# Read data
	desc = pd.read_csv('master-with-desc.csv', error_bad_lines=False, engine='python', skip_blank_lines=True)
	desc.dropna(how='all', inplace=True)
	matched = pd.read_csv('matched.csv', error_bad_lines=False, engine='python')
	print('Master File: ', desc.shape)
	print('Matches File:', matched.shape)
	
	# Set counts
	count = 0
	nomatch = 0
	matches = []

	# Iterate over the items
	for index, row in matched.iterrows():
		count += 1

		item = row['Matched name']
		name = item[2:len(item)-2]
		
		# Find any matched rows
		descrow = desc.loc[desc['NameToDisplay']==name]
		if descrow.empty:
			nomatch += 1; print('No match for: ', name); continue
		
		# Create record for a match
		temp = [row['Original name'], name, row['Match confidence (lower is better)'], descrow['Description'].values[0], descrow['GroupName'].values[0], 
		descrow['HSNCODE'].values[0], descrow['Strength'].values[0], descrow['SalesTax'].values[0], 
		descrow['Product'].values[0], descrow['Category'].values[0], descrow['Unit1'].values[0], descrow['Unit2'].values[0]]
		matches.append(temp)

	print('Total records:', count)
	print('No matches found: ', nomatch)

	# Build dataframe and save to CSV	
	print('Building data frame...')  
	matches = pd.DataFrame(matches, columns=['Original Name','Matched name','Match Confidence (lower is better)', 
		'Description', 'GroupName', 'HSNCODE', 'Strength', 'SalesTax', 'Product', 'Category', 'Unit1', 'Unit2'])
	matches.to_csv('matched-with-desc.csv')
	print('Done')
	
	t = time.time()-t1
	print('Completed in:', round(t,2), 'secs')