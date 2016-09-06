import requests
import re
import json
from string import ascii_lowercase
from bs4 import BeautifulSoup

parenthesis = re.compile('\(.*\)')

diseases_full_list = []

for c in ascii_lowercase:
	r = requests.get("http://www.medicinenet.com/diseases_and_conditions/alpha_%s.htm" % c)
	soup = BeautifulSoup(r.text, 'html.parser')
	results = soup.find_all(class_="AZ_results")[0].find_all('li')

	diseases = []

	for li in results:
		text = li.find_all('a')[0].string
		
		# Find & remove alternative names
		synonyms = []
		m = re.search(parenthesis, text)
		if m:
			match = m.group(0)
			synonyms.append(match[1:-1])
			text = text.replace(match, "")


		# Fix word order
		word_list = text.split(',')
		synonyms.append(word_list[0])
		
		# Remove trailing spaces
		synonyms = [s.strip() for s in synonyms]


		diseases.append(synonyms)

	diseases_full_list.append(diseases)

print 'Writing to file'
f = open('diseases.json', 'w')
f.write(json.dumps(diseases_full_list))
f.close()
