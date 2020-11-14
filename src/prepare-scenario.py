import json
def execute(JSONGridString):
    # "Output: scenarioFiredEventsStr"
    scenarioFiredEventsList = []
    scenarioList = json.loads(JSONGridString)[1]['data']
    for scenario in range(len(scenarioList)):
        scenarioEventsDict = {}
        scenarioKeysList = ["alertingEventId", 
                            "scenarioFiredEventId", 
                            "scenarioId", 
                            "scenarioName", 
                            "scenarioDescription", 
                            "scenarioOriginCd", 
                            "scenarioFiredEntityType",
                            "scenarioFiredEntityId", 
                            "score", 
                            "displayTypeCd", 
                            "displayFlg", 
                            "recQueueId", 
                            "messageTemplateTxt"
       ]
        for index in range(len(scenarioKeysList)):
            scenarioEventsDict[scenarioKeysList[index]] = scenarioList[scenario][index]
        scenarioFiredEventsList.append(scenarioEventsDict)
    scenarioFiredEventsStr = json.dumps(scenarioFiredEventsList)
    return scenarioFiredEventsStr
