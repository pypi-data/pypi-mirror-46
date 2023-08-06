# PySearch

A Python package that solves word searches

## Usage

Create Word search, add words, dolve

'''
search = '''(multiline string of letters, aka the actual word search)'''

words = [list of words]

my_search = PySearch.WordSearch(search)
my_search.Words(words)
final_search = my_search.solve()

for x in final_search:
	print(x)
'''