from scholar import scholar
import json,csv


# Load disease list
f = open('data/diseases.json', 'r')
diseases = json.loads(f.read())[0]

# List of foods
food = 'meat'


def get_occurrences(food):
	querier = scholar.ScholarQuerier()
	settings = scholar.ScholarSettings()
	query = scholar.SearchScholarQuery()

	results = {}

	for disease in diseases:
		occurences_disease = []
		print disease[0]
		for synonym in disease:
			query.set_words(food)
			query.set_phrase(synonym)
			querier.send_query(query)
			if len(querier.articles) > 0:
				occurences_disease.append(querier.articles)
		
		if len(occurences_disease) > 0:
			results[disease[0]] = occurences_disease

		# Remove repeated articles

	return results



occurences = get_occurrences(food)
print occurences

print "Writing to file"

f = open('data/'+food+'.csv', 'w')
writer = csv.writer(f)
for key, value in occurences.iteritems():
	if len(value) > 0:
		writer.writerow((key, len(value)))
f.close()


