from serpwow.google_search_results import GoogleSearchResults
import json

# create the serpwow object, passing in our API key
serpwow = GoogleSearchResults("1DA7CFA6")

# set the batch id and page
batchId = "553F5E75"
page = 1
searchTerm = "te"

# find the searches that match 'searchTerm' on the given page for the given batch
result = serpwow.find_batch_searches(batchId, page, searchTerm)

# pretty-print the result
print(json.dumps(result, indent=2, sort_keys=True))