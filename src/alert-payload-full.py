
# НАЗНАЧЕНИЕ ФУНКЦИИ:
# Функция предназначена для подготовки сценариев алерта в соответствии с заданной структурой JSON-объекта для последующей загрузки алертов в SVI,
# а именно, для парсинга JSON-строки и создания нового JSON-объекта заданной структуры

# ВХОДНЫЕ ПАРАМЕТРЫ ФУНКЦИИ:
# 1. JSONGridString - поле типа String, которое содержит список сценариев в формате JSON-строки
# 2. alertingEventId - ID алерта
# 3. actionableEntityType - Тип бизнес-объекта
# 4. score - Скоринговый балл сценария
# 5. actionableEntityId - ID бизнес-объекта
# 6. alertOriginCd - Источник алерта
# 7. alertTypeCd - Тип алерта
# 8. recQueueId - Очередь

# Импорт библиотек
import requests
import json
# Функция парсинга строки JSON


def execute(JSONGridString, alertingEventId, actionableEntityType, score, actionableEntityId, alertOriginCd, alertTypeCd, recQueueId):
    # Выходная переменная - синтаксис SID
    "Output: response"
    # Получаем конечный список сценариев для загрузки в SVI вида [{ scenario1 }, { scenario2 }, { scenario3 }...]
    scenarioFiredEventsList = []
    # Получаем список сценариев вида [[scenario1], [scenario2], [scenario3]...], где JSONGridString - это список словарей вида [{ metadata: [] }, { data: [] }],
    # где metadata - список полей, а data - список значений этих полей
    scenarioList = json.loads(JSONGridString)[1]['data']
    # Цикл по сценариям из списка scenarioList - для каждого сценария нужно создать словарь определенной структуры
    for scenario in range(len(scenarioList)):
        # Персональный словарь для каждого сценария
        scenarioEventsDict = {}
        # Список ключей словаря - структура словаря scenarioEventsDict
        scenarioKeysList = [
            "alertingEventId",
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
        # Цикл по списку scenarioKeysList - перебираем ключи и в каждое из них записываем соответствующее значение из scenarioList
        for index in range(len(scenarioKeysList)):
            scenarioEventsDict[scenarioKeysList[index]
                               ] = scenarioList[scenario][index]
        # Добавляем каждый сценарий в конечный список сценариев scenarioFiredEventsList
        scenarioFiredEventsList.append(scenarioEventsDict)
    # Превращаем словарь в JSON-строку - это для отладки, опциональный шаг, чтобы проверить в SID
    scenarioFiredEventsStr = json.dumps(scenarioFiredEventsList)
    # Имя сервера, где развернут SVI - для авторизации на сервере
    oauthUrl = 'http://pdcesx15013.exnet.sas.com/SASLogon/oauth/token'
    oauthPayload = {
        'grant_type': 'password',
        'username': 'user',
        'password': 'password'
    }
    # Default headers
    oauthHeaders = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Accept': 'application/json',
        'Authorization': 'Basic c2FzLmVjOg=='
    }
    # Токен авторизации
    # TODO: добавить блок try-except для отладки
    accessToken = requests.post(
        oauthUrl, headers=oauthHeaders, params=oauthPayload).json().get('access_token')
    token = 'Bearer ' + accessToken
    # Имя сервера, где развернут SVI - для загрузки алертов в SVI
    url = 'http://pdcesx15013.exnet.sas.com/svi-alert/alertingEvents'
    # Тело POST-запроса - уникальный алерт и соответствующие ему сценарии
    body = {
        "alertingEvents": [
            {
                "alertingEventId": "{}".format(alertingEventId),
                "actionableEntityType": "{}".format(actionableEntityType),
                "score": score,
                "actionableEntityId": "{}".format(actionableEntityId),
                "alertOriginCd": "{}".format(alertOriginCd),
                "alertTypeCd": "{}".format(alertTypeCd),
                "recQueueId": "{}".format(recQueueId)
            }
        ],
        "scenarioFiredEvents": json.loads(scenarioFiredEventsStr)
    }
    # Headers
    headers = {
        'Content-Type': 'application/vnd.sas.fcs.tdc.alertingeventsdataflat+json',
        'Accept': 'application/vnd.sas.collection+json',
        'Authorization': token
    }
    # Ответ от сервера - 201 - ОK, 500 - DATA ERROR, 404 - NOT FOUND
    # TODO: добавить блок try-except для отладки
    response = requests.post(url, headers=headers, json=body)
    return response
