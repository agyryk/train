
1) Install CB, create empty bucket

2) load "salaries" dataset by running 'generate_salaries_dataset.py'

3) run the parser by running  primitive_v3/run.py
   
   APIs:
    http://localhost:5000/api/ping  - returns pong
    http://localhost:5000/api/run - POST request to start indexing (need to post cb server settigns and tags rules
    http://localhost:5000/api/progress - general status of the parser

4) run indexer using post to api/run. Example of the data:

    curl -i -H "Content-Type: application/json" -XPOST  http://localhost:5000/api/run -d '{"server": {"name":"localhost", "bucket":"train", "port":"8091", "password":"password"},"rules":[{"name": "city", "source":"city", "value":"*", "filter":"*"},{"name":"position", "source": "position", "value":"any java positions", "filter":"include(java)"},{"name":"position", "source": "position", "value":"any developer position", "filter":"include(developer)"},{"name":"position", "source": "position", "value":"only java developers", "filter":"include(java, developer)"},{"name":"position", "source": "position", "value":"all qa", "filter":"include(qa)"}, {"name":"salary", "source": "salary", "value":"below 150K", "filter":"range(<150)"},{"name":"salary", "source": "salary", "value":"above 150K", "filter":"range(>=150)"}]}'

    json structure:

    {
        "server": {"name":"localhost", "bucket":"train", "port":"8091", "password":"password"}},
        "rules":[
            {"name": "city", "source":"city", "value":"*", "filter":"*"},
            {"name":"position", "source": "position", "value":"any java positions", "filter":"include(java)"},
            {"name":"position", "source": "position", "value":"any developer position", "filter":"include(developer)"},
            {"name":"position", "source": "position", "value":"only java developers", "filter":"include(java, developer)"},
            {"name":"position", "source": "position", "value":"all qa", "filter":"include(qa)"},
            {"name":"salary", "source": "salary", "value":"below 150K", "filter":"range(<150)"},
            {"name":"salary", "source": "salary", "value":"above 150K", "filter":"range(>150)"},
            {"name": "experience", "source":"experience", "value":"*", "filter":"*"}
         ]
    }

    the POC supports 3 types of filters: all values, include(test) and range(number)

5) Indexer APIs:

      /api/index_stats - returns size of the index
      /api/query - post request to run query

6) Queries supported:

    get_all_tags
    get_values_by_tag
    get_docids_by_tag_and_value
    get_tags_by_docid
    get_values_by_docid_and_tag

    Examples:
        curl -i -H "Content-Type: application/json" -XPOST  http://localhost:5000/api/query -d '{"type":"all_tags"}'
        curl -i -H "Content-Type: application/json" -XPOST  http://localhost:5000/api/query -d '{"type":"values_by_tag", "tag":"city:}''
        curl -i -H "Content-Type: application/json" -XPOST  http://localhost:5000/api/query -d '{"type":"ids_by_tag_and_value", "tag":"city", "value":"Chicago"}''
        curl -i -H "Content-Type: application/json" -XPOST  http://localhost:5000/api/query -d '{"type":"tags_by_id", "id":"13"}''
        curl -i -H "Content-Type: application/json" -XPOST  http://localhost:5000/api/query -d '{"type":"value_by_id_and_tag", "tag":"city", "id":"23"}'
