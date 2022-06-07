#POWEREDBY: RAFAEL MOURA (ISH)

from datetime import datetime
import requests
import json
import datetime
import sys

#APIKEY - TOPIA SOLUTION 
apikey = ''

#HTTPS URL DASHBOARD - TOPIA SOLUTION
urldashboard = '' 

#CRIAÇÃO ARQUIVO CSV
f = open('ISH_ActivityLogReport.csv', 'w', encoding='UTF8')

#ESCRITA COLUNAS CSV
f.write('AutomationName,Asset,SO,TaskType,PublisherName,PathOrProduct,pathFileName,ActionStatus,MessageStatus,Username,CreateAt,UpdateAt\n')

#GET COUNT EVENTS
def getCountTasksEvents(apikey,urldashboard):
    headers = {
        'Accept': 'application/json',
        'Vicarius-Token': apikey,
    }
    response = requests.get(urldashboard + '/vicarius-external-data-api/taskEndpointsEvent/count', headers=headers)

    jsonresponse = json.loads(response.text)
    responsecount = jsonresponse['serverResponseCount']

    print('Count: ', responsecount)

    return responsecount

#FORMATAÇÃO DATA E HORA   
def timestamptodatetime(timestamp_with_ms):

    timestamp, ms = divmod(timestamp_with_ms, 1000)
    dt = datetime.datetime.fromtimestamp(timestamp) + datetime.timedelta(milliseconds=ms)    
    formatted_time = dt.strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
  
    return formatted_time

#GET TASKS E ESCRITA ARQUIVO
def getTasksEndopintsEvents(apikey,urldashboard,fr0m,siz3,count):
    headers = {
        'Accept': 'application/json',
        'Vicarius-Token': apikey,
    }

    params = {
        'from': fr0m,
        'size': siz3,
    }

    response = requests.get(urldashboard + '/vicarius-external-data-api/taskEndpointsEvent/filter', params=params, headers=headers)
    parsed = json.loads(response.text)


    for i in parsed['serverResponseObject']:
        #print(json.dumps(i, indent=4, sort_keys=True))

        try:
            asset = i['taskEndpointsEventEndpoint']['endpointName']
            systemope = i['taskEndpointsEventEndpoint']['endpointOperatingSystem']['operatingSystemName']
            taskType = str(i['taskEndpointsEventTask']['taskTaskType']['taskTypeId'])
            taskType = taskType + "_" + i['taskEndpointsEventTask']['taskTaskType']['taskTypeName']

            pathproduct = ""
            pathFileName = ""
        except:
            asset = "ERROR"
            systemope = ""
            taskType = ""

#------------------------------------------------------------------------------------------------#
#CONDIÇÕES CADASTRADAS POR "TASKTYPE"
#ID =  4 - "ActivateTopiaMonitor",
#ID =  5 - "ActivateTopiaProtection",
#ID =  6 - "ApplyPublisherProductVersionsPatchs",
#ID =  16 - "ActivateTopiaAnalysis",
#ID =  19 - "UploadOrganizationEndpointLog"       
#ID =  20 - "ApplyPublisherOperatingSystemVersionsPatchs"
#ID =  21 - "21_RunScript"

          
        if i['taskEndpointsEventTask']['taskTypeId'] == 4:
            try:
                automationName = i['taskEndpointsEventTask']['taskAutomation']['automationName']
                username = i['taskEndpointsEventTask']['taskUser']['userFirstName']
                username = username + " " + i['taskEndpointsEventTask']['taskUser']['userLastName']
                publisherName = i['taskEndpointsEventTask']['taskPublisher']['publisherName']
                pathproduct = i['taskEndpointsEventTask']['taskEndpointGroupAdditionalInfo']
                pathFileName = i['taskEndpointsEventTask']['taskProduct']['productName']
                actionStatus = i['taskEndpointsEventTask']['taskTaskType']['taskTypeName']
                messageStatus = i['taskEndpointsEventTask']['taskTaskStatus']['taskStatusName']
            except:
                automationName = ""
                username = ""
                publisherName = ""
                pathproduct = ""
                pathFileName = ""
                actionStatus = ""
                messageStatus = ""
            
        elif i['taskEndpointsEventTask']['taskTypeId'] == 5:
            try:
                automationName = i['taskEndpointsEventTask']['taskAutomation']['automationName']
                username = i['taskEndpointsEventTask']['taskUser']['userFirstName']
                username = username + " " + i['taskEndpointsEventTask']['taskUser']['userLastName']
                publisherName = i['taskEndpointsEventTask']['taskPublisher']['publisherName']
                pathproduct = i['taskEndpointsEventTask']['taskEndpointGroupAdditionalInfo']
                pathFileName = i['taskEndpointsEventTask']['taskProduct']['productName']
                actionStatus = i['taskEndpointsEventTask']['taskTaskType']['taskTypeName']
                messageStatus = i['taskEndpointsEventTask']['taskTaskStatus']['taskStatusName']
            except:
                automationName = ""
                username = ""
                publisherName = ""
                pathproduct = ""
                pathFileName = ""
                actionStatus = ""
                messageStatus = ""
            
        elif i['taskEndpointsEventTask']['taskTypeId'] == 6:
            try:
                automationName = i['taskEndpointsEventTask']['taskAutomation']['automationName']
                username = i['taskEndpointsEventTask']['taskUser']['userFirstName']
                username = username + " " + i['taskEndpointsEventTask']['taskUser']['userLastName']
                publisherName = i['taskEndpointsEventTask']['taskPublisher']['publisherName']
                pathproduct =  i['taskEndpointsEventTask']['taskProduct']['productName']
                pathFileName = i['taskEndpointsEventTask']['taskPatch']['patchName']
                actionStatus = i['taskEndpointsEventOrganizationEndpointPatchPatchPackages']['organizationEndpointPatchPatchPackagesActionStatus']['actionStatusName']
                messageStatus = i['taskEndpointsEventOrganizationEndpointPatchPatchPackages']['organizationEndpointPatchPatchPackagesStatusMessage']
            except:
                automationName = ""
                username = ""
                publisherName = ""
                pathproduct = ""
                pathFileName = ""
                actionStatus = ""
                messageStatus = ""
            

        elif i['taskEndpointsEventTask']['taskTypeId'] == 16:
            try:
                automationName = i['taskEndpointsEventTask']['taskAutomation']['automationName']
                username = i['taskEndpointsEventTask']['taskUser']['userFirstName']
                username = username + " " + i['taskEndpointsEventTask']['taskUser']['userLastName']
                publisherName = i['taskEndpointsEventTask']['taskPublisher']['publisherName']
                pathproduct = i['taskEndpointsEventTask']['taskEndpointGroupAdditionalInfo']
                pathFileName = i['taskEndpointsEventTask']['taskProduct']['productName']
                actionStatus = i['taskEndpointsEventTask']['taskTaskType']['taskTypeName']
                messageStatus = i['taskEndpointsEventTask']['taskTaskStatus']['taskStatusName']
            except:
                automationName = ""
                username = ""
                publisherName = ""
                pathproduct = ""
                pathFileName = ""
                actionStatus = ""
                messageStatus = ""
           
        elif i['taskEndpointsEventTask']['taskTypeId'] == 19:
            username = ""
            automationName = ""
            publisherName = ""
            pathproduct = ""
            actionStatus = ""
            messageStatus = ""
            pathFileName = ""

        elif i['taskEndpointsEventTask']['taskTypeId'] == 20:
            try:
                automationName = i['taskEndpointsEventTask']['taskAutomation']['automationName']
                username = i['taskEndpointsEventTask']['taskUser']['userFirstName']
                username = username + " " + i['taskEndpointsEventTask']['taskUser']['userLastName']
                publisherName = i['taskEndpointsEventTask']['taskPublisher']['publisherName']
                pathproduct = i['taskEndpointsEventTask']['taskPatch']['patchName']
                actionStatus = i['taskEndpointsEventOrganizationEndpointPatchPatchPackages']['organizationEndpointPatchPatchPackagesActionStatus']['actionStatusName']
                pathFileName = i['taskEndpointsEventTask']['taskPatch']['patchDescription'] 
                messageStatus = i['taskEndpointsEventOrganizationEndpointPatchPatchPackages']['organizationEndpointPatchPatchPackagesStatusMessage']
            except:
                automationName = ""
                username = ""
                publisherName = ""
                pathproduct = ""
                pathFileName = ""
                actionStatus = ""
                messageStatus = ""

        elif i['taskEndpointsEventTask']['taskTypeId'] == 21:
            try:
                automationName = i['taskEndpointsEventTask']['taskAutomation']['automationName']
                username = i['taskEndpointsEventTask']['taskUser']['userFirstName']
                username = username + " " + i['taskEndpointsEventTask']['taskUser']['userLastName']
                publisherName = i['taskEndpointsEventOrganizationEndpointScriptCommands']['organizationEndpointScriptCommandsCommand']['commandOperatingSystemFamily']['operatingSystemFamilyName']
                pathproduct = i['taskEndpointsEventOrganizationEndpointScriptCommands']['organizationEndpointScriptCommandsCommand']['commandCommand']
                actionStatus = i['taskEndpointsEventOrganizationEndpointScriptCommands']['organizationEndpointScriptCommandsActionStatus']['actionStatusName']
                messageStatus = i['taskEndpointsEventOrganizationEndpointScriptCommands']['organizationEndpointScriptCommandsStatusMessage']
                pathFileName = i['taskEndpointsEventEndpoint']['endpointOperatingSystem']['operatingSystemName']
            except:
                automationName = ""
                username = ""
                publisherName = ""
                pathproduct = ""
                pathFileName = ""
                actionStatus = ""
                messageStatus = ""

        else:
            publisherName = "Cadastrar Condição"
            pathproduct = "Cadastrar Condição"
            pathFileName = "Cadastrar Condição"
            actionStatus = "Cadastrar Condição"
            messageStatus = "Cadastrar Condição"
            
#------------------------------------------------------------------------------------------------#            
            
        createAt = timestamptodatetime(i['analyticsEventCreatedAt'])
        updateAt = timestamptodatetime(i['analyticsEventUpdatedAt'])

#ESCRITA ARQUIVO CSV
        f.write(automationName + "," + asset + "," + systemope + "," + taskType + "," + publisherName + "," + pathproduct + ",\"" + pathFileName + "\"," + actionStatus + ",\"" + messageStatus + "\","  + username + "," + createAt + "," + updateAt + "\n")

        
    fr0m = fr0m + siz3

    if fr0m < count:
        getTasksEndopintsEvents(apikey,urldashboard,fr0m,siz3,count)
    else:
        f.close()
        sys.exit()        

#------------------------------------------------------------------------------------------------#
        
#EXEUÇÃO    
fr0m = 0
siz3 = 50
count = getCountTasksEvents(apikey,urldashboard)
getTasksEndopintsEvents(apikey,urldashboard,fr0m,siz3,count)

#TESTAR COM LIMITAÇÃO DO CONTADOR
#getTasksEndopintsEvents(apikey,urldashboard,fr0m,siz3,100)

#------------------------------------------------------------------------------------------------#