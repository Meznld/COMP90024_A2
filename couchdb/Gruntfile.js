module.exports = function (grunt) {
    grunt
      .initConfig({
        "couch-compile": {
          dbs: {
            files: {
              "/tmp/housing.json": "couchdb/housing/views/housing",
              "/tmp/covid.json": "couchdb/covid/views/covid",
              "/tmp/election.json": "couchdb/election/views/election",
              "/tmp/crypto.json": "couchdb/crypto/views/crypto"
            }
          }
        },
        "couch-push": {
          options: {
            user: process.env.user,
            pass: process.env.pass
          },
          twitter: {
            files: {
              "http://admin:XlkLSNezrwOlQ0fIx5C6@172.26.128.201:30396/housing": "/tmp/housing.json",
              "http://admin:XlkLSNezrwOlQ0fIx5C6@172.26.128.201:30396/covid": "/tmp/covid.json",
              "http://admin:XlkLSNezrwOlQ0fIx5C6@172.26.128.201:30396/election": "/tmp/election.json",
              "http://admin:XlkLSNezrwOlQ0fIx5C6@172.26.128.201:30396/crypto": "/tmp/crypto.json"
            }
          }
        }
      });
  
    grunt.loadNpmTasks("grunt-couch");
  };