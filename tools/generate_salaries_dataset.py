import couchbase
from couchbase.bucket import  Bucket
import random


SERVER = "<ip>"
PWD = "<pwd>"
TOTAL_DOCS = 1000
BUCKET_NAME = "<bucketname>"

cities = [
                "Chicago","Chicago","Chicago",
                "New York","New York","New York","New York","New York","New York","New York",
                "San Francisco","San Francisco","San Francisco","San Francisco",
                "San Francisco","San Francisco","San Francisco","San Francisco",
                "Los Angeles","Los Angeles","Los Angeles","Los Angeles","Los Angeles",
                "Denver","Denver","Denver",
                "Seattle","Seattle","Seattle","Seattle","Seattle",
                "Miami",
                "Detroit",
                "San Diego",
                "Salt Lake City"
         ]
positions = [
                    "software developer","software developer","software developer","software developer",
                    "developer",
                    "qa"
                    "automaiton qa",
                    "java developer","java developer","java developer",
                    "developer in test",
                    "frontend developer",
                    "java fronted developer",
                    "backend develper",
                    "java backend developer",
                    ".NET backend developer",
                    "c++ game developer",
                    "javascript developer",
                    "c++ developer",
                    "java automation tester",
                    "java performance tester",
                    "python developer",
                    "software developer with python",
                    "java enterprise developer",
                    "performance qa",
                    "support of java application",
          ]

experience = [
                    "intern",
                    "junior","junior",
                    "midlevel","midlevel","midlevel","midlevel","midlevel",
                    "senior","senior","senior","senior"
              ]

salary_min = 100000
salary_max = 200000

connection_string = "couchbase://{}/{}".format(SERVER,BUCKET_NAME)
cb = Bucket(connection_string, password=PWD)

counter = 0
for docid in range(0, TOTAL_DOCS):
    key = str(docid)
    doc = {}
    doc["city"] = random.choice(cities)
    doc["position"] = random.choice(positions)
    doc["experience"] = random.choice(experience)
    doc["salary"] = random.randint(salary_min, salary_max)

    cb.upsert(key, doc)
    counter += 1
    print "{} documents created".format(counter)

