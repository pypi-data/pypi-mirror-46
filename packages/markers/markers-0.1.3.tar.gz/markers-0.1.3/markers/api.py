import requests, urllib.parse

class Api:
    def __init__(self, api_key, api_url):
        self.api_key = api_key
        self.api_url = api_url

    def get(self, uri):
        params = { 'key': self.api_key }
        uri = '/'.join([self.api_url, 'api', uri])

        res = requests.get(uri, params=params)
        res.raise_for_status()

        data = res.json()
        return data

    def post(self, uri, data):
        params = { 'key': self.api_key }
        uri = '/'.join([self.api_url, 'api', uri])

        res = requests.post(uri, params=params, json=data)
        res.raise_for_status()

        data = res.json()
        return data



# NOTE: reference graphql request in python
# import requests
# url = 'http://localhost:5001/graphql'
# query = """
# query {
#   projectById (id: "a509adcc-5d79-11e9-b5ae-d3399d6dcf54") {
#     id
#     name
#     cycles (filter: { id: { equalTo: "305195d5"}}) {
#       nodes {
#         id
#         tasks {
#           nodes {
#             id
#             document {
#               id
#               externalId
#               contents
#               metadata
#             }
#           }
#         }
#       }
#     }
#   }
# }
# """
# json = { 'query' : query }
# params = { 'api_key': '51af1c9d-8b84-469e-a54e-f754ca86ecbc' }

# res = requests.post(url=url, params=params, json=json)
# data = res.json()
# print(data)
