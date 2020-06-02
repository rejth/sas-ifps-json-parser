package "${PACKAGE_NAME}" /inline;

    method execute(
        /* Variables from flow */
        varchar(32767) businessRuleOutputSerial,
        varchar(4000) oauth_token,
        varchar(1) ENABLE_ALERT_INPUT,
        varchar(100) actionableEntityId,
        varchar(100) actionableEntityLabel,
        varchar(100) actionableEntityType,
        varchar(100) alertingEventId,
        varchar(100) alertOriginCd,
        varchar(100) alertTriggerTxt,
        varchar(100) alertTypeCd,
        varchar(4) displayFlg,
        varchar(100) displayTypeCd,
        varchar(100) messageTemplateTxt,
        double P_fraudTrue,
        varchar(100) recQueueId,
        varchar(100) replicateFlg,
        varchar(100) scenarioDescription,
        varchar(100) scenarioFiredEventId,
        varchar(100) scenarioFiredEntityType,
        varchar(100) scenarioFiredEntityId,
        varchar(100) scenarioId,
        varchar(100) scenarioName,
        varchar(100) scenarioOriginCd,
        double score,
        double alertscore,
        double modelscore,
        double overall_risk_score,
        double minimumScore,
        double maximumScore,
        varchar(100) triggeringFlg,
        varchar(100) workspaceFlg,
        varchar(6) applicationtype,
        varchar(4) applicationsubtype,
        varchar(40) forename,
        varchar(40) surname,
        in_out varchar ALERT_RESPONSE,
        varchar(536870911) alertPayload
        );

        /* Declare DS2 Method Packages */
        dcl package http h();
        dcl package datagrid businessRulesOutputGrid();
        dcl package json scenario();

        /* Declare variables created as part of DS2 Code */
        dcl varchar(1048576) character set utf8 response;
        dcl int status;
        dcl int rc rowCount i;
        dcl varchar(50) businessRuleId;
        dcl double tokenType parseFlags;
        dcl varchar(3048) token;
        dcl varchar(1) ENABLE_ALERT;
        dcl int _initCalled;

        /* SAS Visual Investigator Alert API Header Information */
        h.createPostMethod('http://banff.ruspfraudvi.rus.sas.com/svi-alert/alertingEvents?');
        h.setRequestContentType('application/vnd.sas.fcs.tdc.alertingeventsdataflat+json;charset=UTF-8');
        h.addRequestHeader('Accept','application/vnd.sas.collection+json');

        /* Set variables for logic */
        rc = datagrid_create(businessRulesOutputGrid, businessRuleOutputSerial);
        rowCount = datagrid_count(businessRulesOutputGrid);

        /* Execute code logic */
        /* Create a JSON writer instance. */
        scenario.createWriter('PRETTY');
            scenario.writeObjOpen();
                scenario.writeString('alertingEvents', 32);
                scenario.writeArrayOpen();
                    /* Create alert JSON body */
                    scenario.writeObjOpen();
                        /* Using the following format for ease of writing-understanding of name; value pairs */
                        scenario.writeString('alertingEventId', 32); scenario.writeString(alertingEventId, 32);
                        /* actionableEntityType & other variables below generated in ruleset as part of the flow */
                        scenario.writeString('actionableEntityType', 32); scenario.writeString(actionableEntityType, 32);
                        scenario.writeString('actionableEntityId', 32); scenario.writeString(actionableEntityId, 32);
                        scenario.writeString('alertOriginCd', 32); scenario.writeString(alertOriginCd, 32);
                        scenario.writeString('alertTypeCd', 32); scenario.writeString(alertTypeCd, 32);
                        scenario.writeString('score', 32); scenario.writeDouble(overall_risk_score, 0, 0, 'integer');
                        scenario.writeString('recQueueId', 32); scenario.writeString(recQueueId, 32);
                        scenario.writeString('alertTriggerTxt', 32); scenario.writeString(alertTriggerTxt, 32);
                    scenario.writeClose();
                scenario.writeClose();

                scenario.writeString('scenarioFiredEvents', 32);
                scenario.writeArrayOpen();
                    do i = 1 to rowCount - 1; /* Shouldn't need -1 but for some reason an additional row is counted that is blank? */
                        /* Get data from datagrid */
                        scenarioFiredEventId = datagrid_get(businessRulesOutputGrid, 'scenarioFiredEventId', i);
                        scenarioFiredEntityType = datagrid_get(businessRulesOutputGrid, 'scenarioFiredEntityType', i);
                        scenarioFiredEntityId = datagrid_get(businessRulesOutputGrid, 'scenarioFiredEntityId', i);
                        scenarioId = datagrid_get(businessRulesOutputGrid, 'scenarioId', i);
                        scenarioName = datagrid_get(businessRulesOutputGrid, 'scenarioName', i);
                        scenarioDescription = datagrid_get(businessRulesOutputGrid, 'scenarioDescription', i);
                        scenarioOriginCd = datagrid_get(businessRulesOutputGrid, 'scenarioOriginCd', i);
                        score = datagrid_get(businessRulesOutputGrid, 'score', i);
                        messageTemplateTxt = datagrid_get(businessRulesOutputGrid, 'messageTemplateTxt', i);
                        minimumScore = datagrid_get(businessRulesOutputGrid, 'minimumScore', i);
                        maximumScore = datagrid_get(businessRulesOutputGrid, 'maximumScore', i);
                        displayTypeCd = datagrid_get(businessRulesOutputGrid, 'displayTypeCd', i);
                        displayFlg = datagrid_get(businessRulesOutputGrid, 'displayFlg', i);
                        recQueueId = datagrid_get(businessRulesOutputGrid, 'recQueueId', i);
                            /* Create scenario JSON body */
                        scenario.writeObjOpen();
                            scenario.writeString('alertingEventId', 32); scenario.writeString(alertingEventId, 32);
                            scenario.writeString('scenarioFiredEventId', 32); scenario.writeString(scenarioFiredEventId, 32); /* Need a consistent value to tie back to contributing objects? */
                            scenario.writeString('scenarioFiredEntityType', 32); scenario.writeString(scenarioFiredEntityType, 32);
                            scenario.writeString('scenarioFiredEntityId', 32); scenario.writeString(scenarioFiredEntityId, 32);
                            scenario.writeString('scenarioId', 32); scenario.writeString(scenarioId, 32);
                            scenario.writeString('scenarioDescription', 32); scenario.writeString(scenarioDescription,32);
                            scenario.writeString('messageTemplateTxt', 32); scenario.writeString(messageTemplateTxt,32);
                            scenario.writeString('scenarioName', 32); scenario.writeString(scenarioName, 32); /* BusinessRuleID ????? */
                            scenario.writeString('scenarioOriginCd', 32); scenario.writeString(scenarioOriginCd, 32);
                            scenario.writeString('score', 32); scenario.writeDouble(score, 0, 0, 'integer');
                            scenario.writeString('minimumScore', 32); scenario.writeDouble(minimumScore, 0, 0, 'integer');
                            scenario.writeString('maximumScore', 32); scenario.writeDouble(maximumScore, 0, 0, 'integer');
                            scenario.writeString('displayTypeCd', 32); scenario.writeString(displayTypeCd, 32);
                            scenario.writeString('displayFlg', 32); scenario.writeString(displayFlg, 32);
                            scenario.writeString('recQueueId', 32); scenario.writeString(recQueueId, 32);
                        scenario.writeClose();
                    end;
                scenario.writeClose();

                scenario.writeString('contributingObjects', 32);
                scenario.writeArrayOpen();
                    do i = 1 to rowCount - 1; /* Shouldn't need -1 but for some reason an additional row is counted that is blank? */
                        /* Get data from datagrid */
                        scenarioFiredEventId = datagrid_get(businessRulesOutputGrid, 'scenarioFiredEventId', i);
                        scenarioFiredEntityType = datagrid_get(businessRulesOutputGrid, 'scenarioFiredEntityType', i);
                        scenarioFiredEntityId = datagrid_get(businessRulesOutputGrid, 'scenarioFiredEntityId', i);
                        /* Create contributing objects JSON body */
                        scenario.writeObjOpen();
                            scenario.writeString('alertingEventId', 32); scenario.writeString(alertingEventId, 32);
                            scenario.writeString('scenarioFiredEventId', 32); scenario.writeString(scenarioFiredEventId, 32);
                            scenario.writeString('contributingObjectType', 32); scenario.writeString(scenarioFiredEntityType, 32);
                            scenario.writeString('contributingObjectId', 32); scenario.writeString(scenarioFiredEntityId, 32);
                            scenario.writeString('triggeringFlg', 32); scenario.writeString(triggeringFlg, 32);
                            scenario.writeString('workspaceFlg', 32); scenario.writeString(workspaceFlg, 32);
                            scenario.writeString('replicateFlg', 32); scenario.writeString(replicateFlg, 32);
                        scenario.writeClose();
                    end;
                scenario.writeClose();

                scenario.writeString('enrichment', 32);
                scenario.writeArrayOpen();
                    /* Create enrichments JSON body */
                    scenario.writeObjOpen();
                        scenario.writeString('alertingEventId', 32); scenario.writeString(alertingEventId, 32);
                        scenario.writeString('forename', 32); scenario.writeString(forename, 32);
                        scenario.writeString('surname', 32); scenario.writeString(surname, 32);
                        scenario.writeString('applicationtype', 32); scenario.writeString(applicationtype, 32);
                        scenario.writeString('applicationsubtype', 32); scenario.writeString(applicationsubtype, 32);
                    scenario.writeClose();
                scenario.writeClose();

            scenario.writeClose();

        scenario.writerGetText(rc, alertPayload);
        scenario.delete();

        /* Post alert JSON payload to SAS Visual Investigator */
        if inMas() then h.setOAuthToken(oauth_Token); else h.addSASOAuthToken();
        h.setRequestBodyAsString(alertPayload);
        h.executeMethod();
        status = h.getStatusCode();
        put status;
        h.getResponseBodyAsString(response, rc);
        put response;
        put alertPayload;
        ALERT_RESPONSE = 'SUCCESS';

    end; /*end of execute*/
endpackage;
