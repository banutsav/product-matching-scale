#!/bin/bash

import time
import pandas as pd
import re
from ftfy import fix_text
import numpy as np
from scipy.sparse import csr_matrix
import sparse_dot_topn.sparse_dot_topn as ct
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.neighbors import NearestNeighbors

# Create ngrams
def ngrams(string, n=3):
    string = fix_text(string) # fix text
    string = string.encode("ascii", errors="ignore").decode() #remove non ascii chars
    string = string.lower()
    chars_to_remove = [")","(",".","|","[","]","{","}","'"]
    rx = '[' + re.escape(''.join(chars_to_remove)) + ']'
    string = re.sub(rx, '', string)
    string = string.replace('&', 'and')
    string = string.replace(',', ' ')
    string = string.replace('-', ' ')
    string = string.title() # normalise case - capital at start of each word
    string = re.sub(' +',' ',string).strip() # get rid of multiple spaces and replace with a single
    string = ' '+ string +' ' # pad names for ngrams...
    string = re.sub(r'[,-./]|\sBD',r'', string)
    ngrams = zip(*[string[i:] for i in range(n)])
    return [''.join(ngram) for ngram in ngrams]

# Co-sine distance matching
def awesome_cossim_top(A, B, ntop, lower_bound=0):
    # force A and B as a CSR matrix.
    # If they have already been CSR, there is no overhead
    A = A.tocsr()
    B = B.tocsr()
    M, _ = A.shape
    _, N = B.shape
 
    idx_dtype = np.int32
 
    nnz_max = M*ntop
 
    indptr = np.zeros(M+1, dtype=idx_dtype)
    indices = np.zeros(nnz_max, dtype=idx_dtype)
    data = np.zeros(nnz_max, dtype=A.dtype)

    ct.sparse_dot_topn(
        M, N, np.asarray(A.indptr, dtype=idx_dtype),
        np.asarray(A.indices, dtype=idx_dtype),
        A.data,
        np.asarray(B.indptr, dtype=idx_dtype),
        np.asarray(B.indices, dtype=idx_dtype),
        B.data,
        ntop,
        lower_bound,
        indptr, indices, data)

    return csr_matrix((data,indices,indptr),shape=(M,N))

# Matching query
def getNearestN(query):
  queryTFIDF_ = vectorizer.transform(query)
  distances, indices = nbrs.kneighbors(queryTFIDF_)
  return distances, indices

if __name__ == '__main__':

	t1 = time.time()
	# Read data
	company = pd.read_csv('company-items.csv', error_bad_lines=False, engine='python')
	master = pd.read_csv('master-items.csv', error_bad_lines=False, engine='python')
	companylist = company['EXISTING DATA'].unique()
	masterlist = master['NameToDisplay'].unique()
	
	# Print lengths
	print('Company List:',len(companylist), 'records')
	print('Master List:',len(masterlist), 'records')
	
	# Vectorize
	print('Vectorizing the data - this could take a few minutes for large datasets...')
	vectorizer = TfidfVectorizer(min_df=1, analyzer=ngrams)
	tfidf = vectorizer.fit_transform(masterlist)
	print('Vectorizing completed...')
	
	# Nearest N
	nbrs = NearestNeighbors(n_neighbors=1, n_jobs=-1).fit(tfidf)
	unique_company = set(companylist)
	print('Getting nearest N...')
	distances, indices = getNearestN(unique_company)
	t = time.time()-t1
	print('Completed in:', round(t,2), 'secs')
	
	# Get Matches
	unique_company = list(unique_company)
	print('Finding matches...')
	matches = []
	for i,j in enumerate(indices):
  		temp = [round(distances[i][0],2), masterlist[j],unique_company[i]]
  		matches.append(temp)

  	# Build dataframe and save to CSV	
	print('Building data frame...')  
	matches = pd.DataFrame(matches, columns=['Match confidence (lower is better)','Matched name','Original name'])
	matches.to_csv('matched.csv')
	print('Done')
=======
#!/bin/bash

import time
import pandas as pd
import re
from ftfy import fix_text
import numpy as np
from scipy.sparse import csr_matrix
import sparse_dot_topn.sparse_dot_topn as ct
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.neighbors import NearestNeighbors

# Create ngrams
def ngrams(string, n=3):
    string = fix_text(string) # fix text
    string = string.encode("ascii", errors="ignore").decode() #remove non ascii chars
    string = string.lower()
    chars_to_remove = [")","(",".","|","[","]","{","}","'"]
    rx = '[' + re.escape(''.join(chars_to_remove)) + ']'
    string = re.sub(rx, '', string)
    string = string.replace('&', 'and')
    string = string.replace(',', ' ')
    string = string.replace('-', ' ')
    string = string.title() # normalise case - capital at start of each word
    string = re.sub(' +',' ',string).strip() # get rid of multiple spaces and replace with a single
    string = ' '+ string +' ' # pad names for ngrams...
    string = re.sub(r'[,-./]|\sBD',r'', string)
    ngrams = zip(*[string[i:] for i in range(n)])
    return [''.join(ngram) for ngram in ngrams]

# Co-sine distance matching
def awesome_cossim_top(A, B, ntop, lower_bound=0):
    # force A and B as a CSR matrix.
    # If they have already been CSR, there is no overhead
    A = A.tocsr()
    B = B.tocsr()
    M, _ = A.shape
    _, N = B.shape
 
    idx_dtype = np.int32
 
    nnz_max = M*ntop
 
    indptr = np.zeros(M+1, dtype=idx_dtype)
    indices = np.zeros(nnz_max, dtype=idx_dtype)
    data = np.zeros(nnz_max, dtype=A.dtype)

    ct.sparse_dot_topn(
        M, N, np.asarray(A.indptr, dtype=idx_dtype),
        np.asarray(A.indices, dtype=idx_dtype),
        A.data,
        np.asarray(B.indptr, dtype=idx_dtype),
        np.asarray(B.indices, dtype=idx_dtype),
        B.data,
        ntop,
        lower_bound,
        indptr, indices, data)

    return csr_matrix((data,indices,indptr),shape=(M,N))

# Matching query
def getNearestN(query):
  queryTFIDF_ = vectorizer.transform(query)
  distances, indices = nbrs.kneighbors(queryTFIDF_)
  return distances, indices

if __name__ == '__main__':

	t1 = time.time()
	# Read data
	company = pd.read_csv('company-items.csv', error_bad_lines=False, engine='python')
	master = pd.read_csv('master-items.csv', error_bad_lines=False, engine='python')
	companylist = company['EXISTING DATA'].unique()
	masterlist = master['NameToDisplay'].unique()
	
	# Print lengths
	print('Company List:',len(companylist), 'records')
	print('Master List:',len(masterlist), 'records')
	
	# Vectorize
	print('Vectorizing the data - this could take a few minutes for large datasets...')
	vectorizer = TfidfVectorizer(min_df=1, analyzer=ngrams)
	tfidf = vectorizer.fit_transform(masterlist)
	print('Vectorizing completed...')
	
	# Nearest N
	nbrs = NearestNeighbors(n_neighbors=1, n_jobs=-1).fit(tfidf)
	unique_company = set(companylist)
	print('Getting nearest N...')
	distances, indices = getNearestN(unique_company)
	t = time.time()-t1
	print('Completed in:', round(t,2), 'secs')
	
	# Get Matches
	unique_company = list(unique_company)
	print('Finding matches...')
	matches = []
	for i,j in enumerate(indices):
  		temp = [round(distances[i][0],2), masterlist[j],unique_company[i]]
  		matches.append(temp)

  	# Build dataframe and save to CSV	
	print('Building data frame...')  
	matches = pd.DataFrame(matches, columns=['Match confidence (lower is better)','Matched name','Original name'])
	matches.to_csv('matched.csv')
	print('Done')
>>>>>>> 4bc6c5098244ca49c062e7884b25fdfa13a76580
=======
#!/bin/bash

import time
import pandas as pd
import re
from ftfy import fix_text
import numpy as np
from scipy.sparse import csr_matrix
import sparse_dot_topn.sparse_dot_topn as ct
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.neighbors import NearestNeighbors

# Create ngrams
def ngrams(string, n=3):
    string = fix_text(string) # fix text
    string = string.encode("ascii", errors="ignore").decode() #remove non ascii chars
    string = string.lower()
    chars_to_remove = [")","(",".","|","[","]","{","}","'"]
    rx = '[' + re.escape(''.join(chars_to_remove)) + ']'
    string = re.sub(rx, '', string)
    string = string.replace('&', 'and')
    string = string.replace(',', ' ')
    string = string.replace('-', ' ')
    string = string.title() # normalise case - capital at start of each word
    string = re.sub(' +',' ',string).strip() # get rid of multiple spaces and replace with a single
    string = ' '+ string +' ' # pad names for ngrams...
    string = re.sub(r'[,-./]|\sBD',r'', string)
    ngrams = zip(*[string[i:] for i in range(n)])
    return [''.join(ngram) for ngram in ngrams]

# Co-sine distance matching
def awesome_cossim_top(A, B, ntop, lower_bound=0):
    # force A and B as a CSR matrix.
    # If they have already been CSR, there is no overhead
    A = A.tocsr()
    B = B.tocsr()
    M, _ = A.shape
    _, N = B.shape
 
    idx_dtype = np.int32
 
    nnz_max = M*ntop
 
    indptr = np.zeros(M+1, dtype=idx_dtype)
    indices = np.zeros(nnz_max, dtype=idx_dtype)
    data = np.zeros(nnz_max, dtype=A.dtype)

    ct.sparse_dot_topn(
        M, N, np.asarray(A.indptr, dtype=idx_dtype),
        np.asarray(A.indices, dtype=idx_dtype),
        A.data,
        np.asarray(B.indptr, dtype=idx_dtype),
        np.asarray(B.indices, dtype=idx_dtype),
        B.data,
        ntop,
        lower_bound,
        indptr, indices, data)

    return csr_matrix((data,indices,indptr),shape=(M,N))

# Matching query
def getNearestN(query):
  queryTFIDF_ = vectorizer.transform(query)
  distances, indices = nbrs.kneighbors(queryTFIDF_)
  return distances, indices

if __name__ == '__main__':

	t1 = time.time()
	# Read data
	company = pd.read_csv('company-items.csv', error_bad_lines=False, engine='python')
	master = pd.read_csv('master-items.csv', error_bad_lines=False, engine='python')
	companylist = company['EXISTING DATA'].unique()
	masterlist = master['NameToDisplay'].unique()
	
	# Print lengths
	print('Company List:',len(companylist), 'records')
	print('Master List:',len(masterlist), 'records')
	
	# Vectorize
	print('Vectorizing the data - this could take a few minutes for large datasets...')
	vectorizer = TfidfVectorizer(min_df=1, analyzer=ngrams)
	tfidf = vectorizer.fit_transform(masterlist)
	print('Vectorizing completed...')
	
	# Nearest N
	nbrs = NearestNeighbors(n_neighbors=1, n_jobs=-1).fit(tfidf)
	unique_company = set(companylist)
	print('Getting nearest N...')
	distances, indices = getNearestN(unique_company)
	t = time.time()-t1
	print('Completed in:', round(t,2), 'secs')
	
	# Get Matches
	unique_company = list(unique_company)
	print('Finding matches...')
	matches = []
	for i,j in enumerate(indices):
  		temp = [round(distances[i][0],2), masterlist[j],unique_company[i]]
  		matches.append(temp)

  	# Build dataframe and save to CSV	
	print('Building data frame...')  
	matches = pd.DataFrame(matches, columns=['Match confidence (lower is better)','Matched name','Original name'])
	matches.to_csv('matched.csv')
	print('Done')
>>>>>>> 4bc6c5098244ca49c062e7884b25fdfa13a76580
