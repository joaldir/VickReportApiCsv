# Author Joaldir

from datetime import datetime
import requests
import json
import datetime
import sys

# add apikey in topia 
# ex. 'eAU6Fs3sc0WVLXQUMgJt6K0wIkWJFgBG8X1IJIHRyaaZr3djtFkGGaid5o1q8W895sPm0obLo03WuCZzWcZtn7ECBGKwYiuID571hBe6dpiQVcHw4Vsizz'
apikey = '<API Key>'

#ex. 'https://company-dashboard.vicarius.cloud'
urldashboard = 'https://<company>.vicarius.cloud' 

f = open('reportcsv_Tasks.csv', 'w', encoding='UTF8')

f.write('Asset,TaskType,PublisherName,PathOrProduct,PathOrProductDesc,ActionStatus,MessageStatus,Username,CreateAt,UpdateAt\n')

def getCountTasksEvents(apikey,urldashboard):
    headers = {
        'Accept': 'application/json',
        'Vicarius-Token': apikey,
    }
    response = requests.get(urldashboard + '/vicarius-external-data-api/taskEndpointsEvent/count', headers=headers)

    jsonresponse = json.loads(response.text)
    responsecount = jsonresponse['serverResponseCount']

    return responsecount
    
def timestamptodatetime(timestamp_with_ms):

    timestamp, ms = divmod(timestamp_with_ms, 1000)
    dt = datetime.datetime.fromtimestamp(timestamp) + datetime.timedelta(milliseconds=ms)    
    formatted_time = dt.strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
  
    return formatted_time

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

        asset = i['taskEndpointsEventEndpoint']['endpointName']
        username = i['taskEndpointsEventTask']['taskUser']['userFirstName']
        username = username + " " + i['taskEndpointsEventTask']['taskUser']['userLastName']
        taskType = i['taskEndpointsEventTask']['taskTaskType']['taskTypeName']
        
        try:
            publisherName = i['taskEndpointsEventTask']['taskPublisher']['publisherName']
        except:
            publisherName = ""

        pathproduct = ""
        pathproductdesc = ""

        if 'patchName' in i['taskEndpointsEventTask']['taskPatch']:            
            pathproduct = i['taskEndpointsEventTask']['taskPatch']['patchName']
            pathproductdesc = i['taskEndpointsEventTask']['taskPatch']['patchDescription']

        
        if 'productName' in i['taskEndpointsEventTask']['taskProduct']:
            pathproduct = i['taskEndpointsEventTask']['taskProduct']['productName']
        
        if 'ActivateTopia' in (i['taskEndpointsEventTask']['taskTaskType']['taskTypeName']):
            actionStatus = taskType
            messageStatus = ""
            
        else:
            try:
                actionStatus = i['taskEndpointsEventOrganizationEndpointPatchPatchPackages']['organizationEndpointPatchPatchPackagesActionStatus']['actionStatusName']
                messageStatus = i['taskEndpointsEventOrganizationEndpointPatchPatchPackages']['organizationEndpointPatchPatchPackagesStatusMessage']
            except:
                actionStatus = ""
                messageStatus = ""
        
        createAt = timestamptodatetime(i['analyticsEventCreatedAt'])
        updateAt = timestamptodatetime(i['analyticsEventUpdatedAt'])
        
        f.write(asset + "," + taskType + "," + publisherName + "," + pathproduct + ",\"" + pathproductdesc + "\"," + actionStatus + ",\"" + messageStatus + "\"," + username + "," + createAt + "," + updateAt + "\n")
        
    fr0m = fr0m + siz3

    if fr0m < count:
        getTasksEndopintsEvents(apikey,urldashboard,fr0m,siz3,count)
    else:
        f.close()
        sys.exit()
    
fr0m = 0
siz3 = 50
count = getCountTasksEvents(apikey,urldashboard)
getTasksEndopintsEvents(apikey,urldashboard,fr0m,siz3,count)

    