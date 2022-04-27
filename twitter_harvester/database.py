

import couchdb
import os



couch = couchdb.Server('http://admin:XlkLSNezrwOlQ0fIx5C6@172.26.128.201:30396/')
def create_database(db_name):
    try:
        database = couch.create(db_name)
    except:
        database = couch[db_name]




