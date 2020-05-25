import json

def execute(scenarioGridString):
    "Output: scenarioFiredEventsStr"
    # Поля алерта по умолчанию
    alertDefaultFieldList = ["alertingEventId", "scenarioFiredEventId", "scenarioId", "scenarioName", "scenarioDescription", "scenarioOriginCd", "scenarioFiredEntityType","scenarioFiredEntityId", "score", "displayTypeCd", "displayFlg", "recQueueId", "messageTemplateTxt"] # to edit if needed
    # Валидный список сценариев, где каждый сценарий - это словарь Python
    scenarioEventsList = []
    # Получаем НЕвалидный список сценариев
    scenarioList = json.loads(scenarioGridString)[1]['data']
    # Создаем валидный список сценариев
    for scenario in range(len(scenarioList)):
        eventDict = {}
        for key in range(len(alertDefaultFieldList)):
            eventDict[alertDefaultFieldList[key]] = scenarioList[scenario][key]
        scenarioEventsList.append(eventDict)
    # Получаем строку со списком сценариев
    scenarioFiredEventsStr = json.dumps(scenarioEventsList)
    return print(scenarioFiredEventsStr)

execute('[{"metadata":[{"ALERTINGEVENTID":"string"},{"SCENARIOFIREDEVENTID":"string"},{"SCENARIOID":"string"},{"SCENARIONAME":"string"},{"SCENARIODESCRIPTION":"string"},{"SCENARIOORIGINCD":"string"},{"SCENARIOFIREDENTITYTYPE":"string"},{"SCENARIOFIREDENTITYID":"string"},{"SCORE":"decimal"},{"DISPLAYTYPECD":"string"},{"DISPLAYFLG":"string"},{"RECQUEUEID":"string"},{"MESSAGETEMPLATETXT":"string"}]},{"data":[["194834970003810275","474092461089218005","SAS_21010226","Account-recipient linked with an employee via contacts","Account-recipient linked with an employee via contacts","ID","vi_transaction","T000177842",50,"TEXT","true","queue_21010226","Account-recipient linked with an employee via contacts"],["194834970003810275","022527020301528011","SAS_21010226","Employee account","Employee account","ID","vi_transaction","T000177842",40,"TEXT","true","queue_21010226","Employee account"],["194834970003810275","674917014227778633","SAS_21010226","Accumulative account","Accumulative account","ID","vi_transaction","T000177842",70,"TEXT","true","queue_21010226","Accumulative account"]]}]')
