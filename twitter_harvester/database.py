
import couchdb

db_names = ['historical','harvest']
couch = couchdb.Server('http://admin:XlkLSNezrwOlQ0fIx5C6@172.26.128.201:30396/')

try:
    db_housing = couch.create('housing')
except:
    del couch['housing']
    db_housing = couch.create('housing')

try:
    db_crypto = couch.create('crypto')
except:
    del couch['crypto']
    db_crypto = couch.create('crypto')

try:
    db_election = couch.create('election')
except:
    del couch['election']
    db_election = couch.create('election')

try:
    db_covid = couch.create('covid')
except: 
    del couch['covid']
    db_covid = couch.create['covid']

housing = ['house price','housing price','rental price','rent price','mortgage','housing','pay rent','real estate','landlord','tenant'] 
crypto = ['crypto','btc','bitcoin','dogecoin','doge','etheruem','eth','cryptocurrency','bnb']
election = ['ausvote', 'auspol','auselectoralcom','election','campaign','vote','federal election','ausvotes2022','morrison','scottmorrisonmp','albomp','alboforpm','australianlabor','scottmorrison']
covid = ['covid','cov-19','covid-19','coronavirus','covid19']


for db in db_names:
    database = couch[db]
    for id in database:
        try:
            text = database[id]['text']
            text = text.lower()
        
            if any(k in text for k in housing):
                db_housing.save({'id': database[id]['id'], 'suburb': database[id]['suburb'], 'text': database[id]['text'], 'sentiment': database[id]['sentiment'], 'score': database[id]['score']})
            if any(k in text for k in crypto):
                db_crypto.save({'id': database[id]['id'], 'suburb': database[id]['suburb'], 'text': database[id]['text'], 'sentiment': database[id]['sentiment'], 'score': database[id]['score']})
            if any(k in text for k in election):
                db_election.save({'id': database[id]['id'], 'suburb': database[id]['suburb'], 'text': database[id]['text'], 'sentiment': database[id]['sentiment'], 'score': database[id]['score']})
            if any(k in text for k in covid):
                    db_election.save({'id': database[id]['id'], 'suburb': database[id]['suburb'], 'text': database[id]['text'], 'sentiment': database[id]['sentiment'], 'score': database[id]['score']})
        except:
            continue
# for tweet in database:
#     print(database[tweet]['suburb'] + ": " + database[tweet]['sentiment'] + "\n" + database[tweet]['text'] + "\n")