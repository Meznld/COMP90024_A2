module.exports = function (grunt) {
    grunt
      .initConfig({
        "couch-compile": {
          dbs: {
            files: {
              "/tmp/housing.json": "couchdbviews/topics/housing",
              "/tmp/covid.json": "couchdbviews/topics/covid",
              "/tmp/election.json": "couchdbviews/topics/election",
              "/tmp/crypto.json": "couchdbviews/topics/crypto"
            }
          }
        },
        "couch-push": {
          options: {
            user: admin,
            pass: XlkLSNezrwOlQ0fIx5C6
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