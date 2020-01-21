#!/bin/bash
import time
import csv
import pandas as pd

# check no of sales for items
def no_of_sales(items, sales, filename):
	with open(filename, mode='w', newline='') as file:
		writer = csv.writer(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
		# write header
		writer.writerow(['item','matched-name','description','marketing-company','count', 'total-sales'])
		total = 0
		# iterate over items
		for index, row in items.iterrows():
			# find how many matches in the sales list
			count = 0
			total_sales = 0
			total_qty = 0
			# find match
			match = sales.loc[sales['Product']==row['Original Name']]
			if match.shape[0] > 0:
				data = [row['Original Name'], row['Matched name'], row['Description']
				, match['MarketingCo'].unique()[0], match.shape[0], match['Sale Amount'].sum()]
				writer.writerow(data)
				total += 1
		print('total for', filename,total)

if __name__ == '__main__':
	t1 = time.time()
	# Read data
	items = pd.read_csv('data/matched-with-desc.csv', error_bad_lines=False, engine='python')
	print('total',items.shape[0])
	sales = pd.read_csv('data/running.csv', error_bad_lines=False, engine='python')
	# get only high confidence matches
	items_match = items.loc[items['Match Confidence (lower is better)']<=0.95]
	items_no_match = items.loc[items['Match Confidence (lower is better)']>0.95]
	print('good match',items_match.shape[0])
	print('bad match',items_no_match.shape[0])
	# no of sales of low confidence matches
	no_of_sales(items_no_match, sales, 'low.csv')
	# no of sales for high confidence matches
	no_of_sales(items_match, sales, 'high.csv')
	t = time.time()-t1
	print('Completed in:', round(t,2), 'secs')