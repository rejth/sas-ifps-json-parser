import requests

server = 'pdcesx16100.exnet.sas.com'

oauthUrl = 'http://' + server + '/SASLogon/oauth/token'
oauthPayload = {
            'grant_type': 'password',
            'username': 'videmo',
            'password': 'Orion123'
}
oauthHeaders = {
            'Content-Type': 'application/x-www-form-urlencoded',
            'Accept': 'application/json',
            'Authorization': 'Basic c2FzLmVjOg=='
}

accessToken = requests.post(oauthUrl, headers=oauthHeaders, params=oauthPayload).json().get('access_token')

url = 'http://' + server + '/svi-datahub/admin/asyncJobs?new'
body = {
    "parameters": {
        "type": "SEARCH_INDEX_LOADER"
    },
    "tasks": [{
        "parameters": {
            "type": "LOAD_DOCUMENT",
            "name": "vi_transaction"
        }
    }]
}
headers = {
            'Content-Type': 'application/json;charset=UTF-8',
            'Accept': 'application/json',
            'Authorization' : 'Bearer ' + accessToken
}
response = requests.post(url, headers=headers, json=body)
