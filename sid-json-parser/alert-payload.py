import json
import requests

host = 'http://banff.ruspfraudvi.rus.sas.com' # to edit if needed
user = 'user1' # to edit if needed
password = 'Go4thsas' # to edit if needed

def execute(scenarioFiredEventsStr, enrichmentFiredEventsStr, alertingEventId, actionableEntityType, scoreMain, actionableEntityId, alertOriginCd, alertTypeCd, recQueueId):
    "Output: response"
    oauthUrl = host + '/SASLogon/oauth/token'
    oauthPayload = {
                'grant_type': 'password',
                'username': user,
                'password': password
    }
    oauthHeaders = {
                'Content-Type': 'application/x-www-form-urlencoded',
                'Accept': 'application/json',
                'Authorization': 'Basic c2FzLmVjOg=='
    }
    accessToken = requests.post(oauthUrl, headers=oauthHeaders, params=oauthPayload).json().get('access_token')
    token = 'Bearer ' + accessToken
    url = host + '/svi-alert/alertingEvents'
    body = {
                "alertingEvents": [
                    {
                        "alertingEventId": "{}".format(alertingEventId),
                        "actionableEntityType": "{}".format(actionableEntityType),
                        "score": scoreMain,
                        "actionableEntityId": "{}".format(actionableEntityId),
                        "alertOriginCd": "{}".format(alertOriginCd),
                        "alertTypeCd": "{}".format(alertTypeCd),
                        "recQueueId": "{}".format(recQueueId)
                    }
                ],
                "scenarioFiredEvents": json.loads(scenarioFiredEventsStr),
                "enrichment": [json.loads(enrichmentFiredEventsStr)]
            }
    headers = {
                'Content-Type': 'application/vnd.sas.fcs.tdc.alertingeventsdataflat+json',
                'Accept': 'application/vnd.sas.collection+json',
                'Authorization' : token
    }
    response = requests.post(url, headers=headers, json=body).status_code
    bodyRequest = 'Alert payload status: ' + str(response) + '\n' + 'Request body' + ':' + '\n' + str(body)
    return bodyRequest
