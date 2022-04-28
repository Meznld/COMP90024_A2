
import couchdb


couch = couchdb.Server('http://admin:XlkLSNezrwOlQ0fIx5C6@172.26.128.201:30396/')
database = couch['historical']

for tweet in database:
    print(database[tweet]['suburb'] + ": " + database[tweet]['sentiment'] + "\n" + database[tweet]['text'] + "\n")