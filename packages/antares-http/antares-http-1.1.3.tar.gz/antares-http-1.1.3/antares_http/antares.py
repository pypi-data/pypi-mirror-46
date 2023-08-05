'''
Antares Python v1.0.0

Available functions:

setAccessKey()
getAccessKey()

get()
getAll() 
getAllId()
getDevices()
getSpecific()
send()

'''

import requests
import json

_antaresAccessKey = ''
_debug = False

def getDebug():
    global _debug;
    return _debug;

def setDebug(debugStatus):
    global _debug
    _debug = debugStatus

def test():
    print('Hello from antares package!')

def setAccessKey(accessKey):
    global _antaresAccessKey
    _antaresAccessKey = accessKey

    if(getDebug()):
        print('Access key:', _antaresAccessKey)

def getAccessKey():
    global _antaresAccessKey
    return _antaresAccessKey

def get(projectName, deviceName, debug=True):
    # print(getDebug())
    # print('Requesting...')
    url = 'https://platform.antares.id:8443/~/antares-cse/antares-id/{}/{}/la'.format(projectName, deviceName)
    
    # print('Access key: ', getAccessKey())

    headers = {
        'X-M2M-Origin' : getAccessKey(),
        'Content-Type' : 'application/json;ty=4',
        'Accept' : 'application/json'
    }

    r = requests.get(url, headers=headers)
    response = r.json()
    data = response['m2m:cin']
    
    parsedContent = {}
    try:
        parsedContent = json.loads(data['con'])
    except:
        parsedContent = data['con']

    finalResponse = {
        'resource_name': data['rn'],
        'resource_identifier': data['ri'],
        'parent_id': data['pi'],
        'created_time': data['ct'],
        'last_modified_time': data['lt'],
        'content' : parsedContent
    }
    
    if(getDebug()):
        print(json.dumps(finalResponse, indent=4))
    # print(finalResponse['content'])
    return finalResponse

def getDevices(projectName, debug=True):
    # print('Requesting...')
    url = 'https://platform.antares.id:8443/~/antares-cse/antares-id/{}?fu=1&ty=3'.format(projectName)
    
    # print('Access key: ', getAccessKey())

    headers = {
        'X-M2M-Origin' : getAccessKey(),
        'Content-Type' : 'application/json;ty=3',
        'Accept' : 'application/json'
    }

    r = requests.get(url, headers=headers)
    response = r.json()
    deviceUrl = response['m2m:uril']

    devicesList = []
    for device in deviceUrl:
        device = device.split('/');
        devicesList.append(device[4]) 
    
    if(getDebug()):
        print(json.dumps(devicesList, indent=4))
    # print(finalResponse['content'])
    return devicesList

def getAll(projectName, deviceName, limit=0):
    # print('Requesting...')
    if(limit != 0):
        url = 'https://platform.antares.id:8443/~/antares-cse/antares-id/{}/{}?fu=1&ty=4&drt=1&lim={}'.format(projectName, deviceName, limit)
    else:
        url = 'https://platform.antares.id:8443/~/antares-cse/antares-id/{}/{}?fu=1&ty=4&drt=1'.format(projectName, deviceName)

    # print('Access key: ', getAccessKey())

    headers = {
        'X-M2M-Origin' : getAccessKey(),
        'Content-Type' : 'application/json',
        'Accept' : 'application/json'
    }

    r = requests.get(url, headers=headers)
    response = r.json()
    allData = response['m2m:uril']
    dataCounter = 0
    dataStorage = []
    for urlInd in allData:
        # print(urlInd)
        url = 'https://platform.antares.id:8443/~{}'.format(urlInd)
        r = requests.get(url, headers=headers)
        response = r.json()['m2m:cin']
        dataCounter+=1

        # Parse content
        parsedContent = {}
        try:
            parsedContent = json.loads(response['con'])
        except:
            parsedContent = response['con']

        finalResponse = {
            'resource_name': response['rn'],
            'resource_identifier': response['ri'],
            'parent_id': response['pi'],
            'created_time': response['ct'],
            'last_modified_time': response['lt'],
            'content' : parsedContent
        }

        if(getDebug()):
            print('Get success:{} out of {}'.format(dataCounter, len(allData)))
        
        dataStorage.append(finalResponse)
        if(limit > 0):
            if(dataCounter >= limit):
                if(getDebug()):
                    print(json.dumps(dataStorage, indent=4))
                    print('Data size: {}'.format(len(dataStorage)))
                return dataStorage
        else:
            if(dataCounter >= len(allData)):
                if(getDebug()):
                    print(json.dumps(dataStorage, indent=4))
                    print(len(dataStorage))
                return dataStorage

def getAllId(projectName, deviceName, limit=0):
    # print('Requesting...')
    if(limit != 0):
        url = 'https://platform.antares.id:8443/~/antares-cse/antares-id/{}/{}?fu=1&ty=4&drt=1&lim={}'.format(projectName, deviceName, limit)
    else:
        url = 'https://platform.antares.id:8443/~/antares-cse/antares-id/{}/{}?fu=1&ty=4&drt=1'.format(projectName, deviceName)

    # print('Access key: ', getAccessKey())

    headers = {
        'X-M2M-Origin' : getAccessKey(),
        'Content-Type' : 'application/json',
        'Accept' : 'application/json'
    }

    r = requests.get(url, headers=headers)
    response = r.json()
    allData = response['m2m:uril']
    
    dataIds = []
    for url in allData:
        url = url.split('/')
        dataIds.append(url[5])

    if(getDebug()):
        print(json.dumps(dataIds, indent=4))
        print('Length: {} data'.format(len(dataIds)))
    return dataIds

def send(data, projectName, deviceName):
    # print('Requesting...')
    url = 'https://platform.antares.id:8443/~/antares-cse/antares-id/{}/{}'.format(projectName, deviceName)
    
    # print('Access key: ', getAccessKey())

    headers = {
        'X-M2M-Origin' : getAccessKey(),
        'Content-Type' : 'application/json;ty=4',
        'Accept' : 'application/json',
    }

    strData = ''
    try:
        strData = json.dumps(data)    
    except:
        strData = data

    dataTemplate = {
        "m2m:cin" : {
            "con" : strData,
        }
    }
    dataTemplate = json.dumps(dataTemplate)

    # print(dataTemplate)
    # print(url)

    r = requests.post(url, headers=headers, data=dataTemplate)
    response = r.json()
    data = response['m2m:cin']

    parsedContent = {}

    try:
        parsedContent = json.loads(data['con'])
    except:
        parsedContent = data['con']

    finalData = {
        'resource_name' : data['rn'],
        'resource_identifier' : data['ri'],
        'parent_id' : data['pi'],
        'created_time' : data['ct'],
        'last_modified_time' : data['lt'],
        'content' : parsedContent
    }

    if(getDebug()):
        print(json.dumps(finalData, indent=4))

    return(finalData)

def createDevice(projectName, newDeviceName):
    # print('Requesting...')
    url = 'https://platform.antares.id:8443/~/antares-cse/antares-id/{}'.format(projectName)
    
    # print('Access key: ', getAccessKey())

    headers = {
        'X-M2M-Origin' : getAccessKey(),
        'Content-Type' : 'application/json;ty=3',
        'Accept' : 'application/json',
    }

    dataTemplate = {
        "m2m:cnt" : {
            "rn" : newDeviceName,
        }
    }
    dataTemplate = json.dumps(dataTemplate)

    # print(dataTemplate)
    # print(url)

    r = requests.post(url, headers=headers, data=dataTemplate)
    response = r.json()
    data = response['m2m:cnt']

    newData = {
        'resource_name' : data['rn'],
        'resource_identifier' : data['ri'],
        'parent_id' : data['pi'],
        'created_time' : data['ct'],
        'last_modified_time' : data['lt'],
        'acpi' : data['acpi'],
        'et' : data['et'],
    }

    if(getDebug()):
        print(json.dumps(newData, indent=4))

    return(newData)

def getSpecific(projectName, deviceName, identifier):
    # print('Requesting...')
    url = 'https://platform.antares.id:8443/~/antares-cse/antares-id/{}/{}/{}'.format(projectName, deviceName, identifier)
    # print(url)

    # print('Access key: ', getAccessKey())

    headers = {
        'X-M2M-Origin' : getAccessKey(),
        'Content-Type' : 'application/json;ty=4',
        'Accept' : 'application/json'
    }

    r = requests.get(url, headers=headers)
    response = r.json()
    # resText = r.text
    # print(resText)
    data = response['m2m:cin']
    
    parsedContent = {}
    try:
        parsedContent = json.loads(data['con'])
    except:
        parsedContent = data['con']

    finalResponse = {
        'resource_name': data['rn'],
        'resource_identifier': data['ri'],
        'parent_id': data['pi'],
        'created_time': data['ct'],
        'last_modified_time': data['lt'],
        'content' : parsedContent
    }
    
    if(getDebug()):
        print(json.dumps(finalResponse, indent=4))
    # print(finalResponse['content'])
    return finalResponse

def getDeviceId(projectName, deviceName):
    url = 'https://platform.antares.id:8443/~/antares-cse/antares-id/{}/{}'.format(projectName, deviceName)
    
    # print('Access key: ', getAccessKey())

    headers = {
        'X-M2M-Origin' : getAccessKey(),
        'Content-Type' : 'application/json',
        'Accept' : 'application/json',
    }

    r = requests.get(url, headers=headers)
    response = r.json()
    # print(response)
    data = response['m2m:cnt']['ri']
    data = data.split('/')[2]
    
    parsedContent = {}

    if(getDebug()):
        print(data)
    return data

def sendById(data, deviceId):
    # print('Requesting...')
    url = 'https://platform.antares.id:8443/~/antares-cse/{}'.format(deviceId)
    
    # print('Access key: ', getAccessKey())

    headers = {
        'X-M2M-Origin' : getAccessKey(),
        'Content-Type' : 'application/json;ty=4',
        'Accept' : 'application/json',
    }

    strData = ''
    try:
        strData = json.dumps(data)    
    except:
        strData = data

    dataTemplate = {
        "m2m:cin" : {
            "con" : strData,
        }
    }
    dataTemplate = json.dumps(dataTemplate)

    # print(dataTemplate)
    # print(url)

    r = requests.post(url, headers=headers, data=dataTemplate)
    response = r.json()
    # print(response)
    data = response['m2m:cin']

    parsedContent = {}

    try:
        parsedContent = json.loads(data['con'])
    except:
        parsedContent = data['con']

    finalData = {
        'resource_name' : data['rn'],
        'resource_identifier' : data['ri'],
        'parent_id' : data['pi'],
        'created_time' : data['ct'],
        'last_modified_time' : data['lt'],
        'content' : parsedContent
    }

    if(getDebug()):
        print(json.dumps(finalData, indent=4))

    return(finalData)
