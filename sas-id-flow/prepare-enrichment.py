import json
def execute (enrichmentGridString):
    # 'Output: enrichmentFiredEventsStr'
    enrichmentFiredEventsList = []
    enrichmentDataList = json.loads(enrichmentGridString)[1]['data'][0]
    enrichmentFieldList = json.loads(enrichmentGridString)[0]['metadata']
    enrichmentEventsDict = {}
    for index in range(len(enrichmentFieldList)):
        key = list(enrichmentFieldList[index].keys())
        enrichmentEventsDict[key[0]] = enrichmentDataList[index]
    enrichmentFiredEventsList.append(enrichmentEventsDict)
    enrichmentFiredEventsStr = json.dumps(enrichmentFiredEventsList)
    return enrichmentFiredEventsStr
