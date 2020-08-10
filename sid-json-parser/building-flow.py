# CREATED BY:
# Ilya Kirsanov, Junior Consultant, Pre-Sales Fraud Practice, Customer Advisory, Russia, Moscow
# SAS Institute Russia,
# ilia.kirsanov@sas.com
#/*********************************************************************************************************************************************************************************************
# НАЗНАЧЕНИЕ БЛОКА:
# Блок предназначен для создания валидной структуры JSON-объекта алерта, его сценариев, а также для загрузки алерта в SAS Visual Investigator
# Создание этого блока обусловлено необходимостью создавать алерты в SAS Visual Investigator в результате работы бизнес-правил в SAS Intelligent Decisioning
# SAS Intelligent Decisioning - на текущий момент это основной движок для создания бизнес-правил и генерации алертов.
# Этот блок позволяет обойти некоторые ограничения интерфейса, в частности, на создание алертов и подготовить валидный JSON-объект для загрузки согласно документации
# Официальная документация по SAS Visual Investigator 10.6 - https://go.documentation.sas.com/?cdcId=vicdc&cdcVersion=10.6&docsetId=visgatorag&docsetTarget=json_examples.htm&locale=ru
# Официальная документация по SAS Intelligent Decisioning 5.4 - https://go.documentation.sas.com/?cdcId=edmcdc&cdcVersion=5.4&docsetId=edmug&docsetTarget=titlepage.htm&locale=ru
#/*********************************************************************************************************************************************************************************************
# ВХОДНЫЕ ПАРАМЕТРЫ БЛОКА:
# 1. scenarioGridString - поле типа String, которое содержит список мошеннических сценариев алерта в формате JSON-строки
# 2. enrichmentGridString - поле типа String, которое содержит список добавочных полей для алерта - enrichments, в формате JSON-строки
# 3. alertingEventId - ID алерта
# 4. actionableEntityType - Тип бизнес-объекта
# 5. score - Скоринговый балл алерта
# 6. actionableEntityId - ID бизнес-объекта
# 7. alertOriginCd - Источник создания алерта
# 8. alertTypeCd - Тип алерта
# 9. recQueueId - Очередь, в которую загружается алерт
#/*********************************************************************************************************************************************************************************************

import json
import requests

host = 'http://banff.ruspfraudvi.rus.sas.com' # to edit if needed
user = 'user1' # to edit if needed
password = 'Go4thsas' # to edit if needed

# Функция для подготовки валидной структуры сценариев алерта
# scenarioGridString - поле типа String, которое содержит список мошеннических сценариев алерта в формате JSON-строки
def prepareScenario(scenarioGridString):
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
    return scenarioFiredEventsStr

# Функция для подготовки валидной структуры добавочных полей для алерта - enrichments
# enrichmentGridString - поле типа String, которое содержит список добавочных полей для алерта - enrichments, в формате JSON-строки
def prepareEnrichment(enrichmentGridString):
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
    return enrichmentFiredEventsStr

# Функция для загрузки валидной структуры алерта в SAS Visual Investigator
def alertPayload(scenarioFiredEventsStr, enrichmentFiredEventsStr, alertingEventId, actionableEntityType, scoreMain, actionableEntityId, alertOriginCd, alertTypeCd, recQueueId):
    "Output: body"
    # Аутентификация в SASLogon для получения токена
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
    # POST запрос для получения токена аутентификации
    try:
        accessToken = requests.post(oauthUrl, headers=oauthHeaders, params=oauthPayload).json().get('access_token')
    except:
        print('Authentification Error: try to verify authentification url, username and password')
    token = 'Bearer ' + accessToken
    # Загрузка алерта в SAS Visual Investigator
    url = host + '/svi-alert/alertingEvents'
    # Валидное тело запроса
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
    # POST запрос на загрузку алертов
    try:
        response = requests.post(url, headers=headers, json=body).status_code
    except:
        print('POST-request Error: it seems there are some problems with loading alerts. Try to verify connection establishing, connection paramaters and body request')
    # Переменная со статусом выполнения и телом POST запроса для отладки в интерфейсе SAS Intelligent Decisioning
    bodyRequest = 'Alert payload status: ' + str(response) + '\n' + 'Request body' + ':' + '\n' + str(body)

    return print(bodyRequest)

def execute(scenarioGridString, enrichmentGridString, alertingEventId, actionableEntityType, scoreMain, actionableEntityId, alertOriginCd, alertTypeCd, recQueueId):
    "Output: bodyRequest"
    scenarioFiredEventsStr = prepareScenario(scenarioGridString)
    enrichmentFiredEventsStr = prepareEnrichment(enrichmentGridString)
    return alertPayload(scenarioFiredEventsStr, enrichmentFiredEventsStr, alertingEventId, actionableEntityType, scoreMain, actionableEntityId, alertOriginCd, alertTypeCd, recQueueId)

execute('[{"metadata":[{"ALERTINGEVENTID":"string"},{"SCENARIOFIREDEVENTID":"string"},{"SCENARIOID":"string"},{"SCENARIONAME":"string"},{"SCENARIODESCRIPTION":"string"},{"SCENARIOORIGINCD":"string"},{"SCENARIOFIREDENTITYTYPE":"string"},{"SCENARIOFIREDENTITYID":"string"},{"SCORE":"decimal"},{"DISPLAYTYPECD":"string"},{"DISPLAYFLG":"string"},{"RECQUEUEID":"string"},{"MESSAGETEMPLATETXT":"string"}]},{"data":[["194834970003810275","474092461089218005","SAS_21010226","Account-recipient linked with an employee via contacts","Account-recipient linked with an employee via contacts","ID","vi_transaction","T000177842",50,"TEXT","true","queue_21010226","Account-recipient linked with an employee via contacts"],["194834970003810275","022527020301528011","SAS_21010226","Employee account","Employee account","ID","vi_transaction","T000177842",40,"TEXT","true","queue_21010226","Employee account"],["194834970003810275","674917014227778633","SAS_21010226","Accumulative account","Accumulative account","ID","vi_transaction","T000177842",70,"TEXT","true","queue_21010226","Accumulative account"]]}]', '[{"metadata":[{"ALERTINGEVENTID":"string"},{"REGION":"string"}]},{"data":[["194834970003810275","Moscow"]]}]', "194834970003810275", "vi_transaction", 280, "T000177842", "SA", "DEFAULT", "queue_21010226")
