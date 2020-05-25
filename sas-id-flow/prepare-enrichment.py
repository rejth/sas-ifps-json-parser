import json

def execute(enrichmentGridString):
    'Output: enrichmentFiredEventsStr'
    eventDict = {}
    # Получаем список полей enrichments
    enrichmentFieldList = json.loads(enrichmentGridString)[0]['metadata']
    # Получаем данные полей enrichments
    enrichmentDataList = json.loads(enrichmentGridString)[1]['data'][0]
    # Создаем валидный словарь Python с полями и данными enrichments
    for field in range(len(enrichmentFieldList)):
        key = list(enrichmentFieldList[field].keys())
        eventDict[key[0]] = enrichmentDataList[field]
    # Получаем строку с полями и данными enrichments
    enrichmentFiredEventsStr = json.dumps(eventDict)
    return print(enrichmentFiredEventsStr)

execute('[{"metadata":[{"ALERTINGEVENTID":"string"},{"REGION":"string"}]},{"data":[["194834970003810275","Moscow"]]}]')
