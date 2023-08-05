# Antares Python
<img src="https://antares.id/assets/img/antarespy.png" width="300">  

This is a Python library to simplify the connection to Antares IoT Platform. For more information about the platform itself, please visit the ![official site](https://antares.id).  

## Installation
Make sure you have Python (2 or 3) and pip installed.
```
pip install antares-http
```

### Usage Example
#### Send data
```python
from antares_http import antares

antares.setDebug(True)
antares.setAccessKey('your-access-key')

myData = {
    'temp' : 77,
    'windsp' : 10
}

antares.send(myData, 'your-project-name', 'your-device-name')
```

#### Get latest data
```python
from antares_http import antares

antares.setDebug(False)
antares.setAccessKey('your-access-key')

latestData = antares.get('your-project-name', 'your-device-name')
print(latestData['content'])
```

### API Reference
* `setAccessKey(access-key)`  
Set the `access-key` parameter to your Antares access key.  

* `setDebug(status)`  
Set whether you want to show debug results of every HTTP request to Antares or not, can be set to `True` or `False`.  

* `get(projectName, deviceName)`  
    Get the latest data from your Antares device.  
    return: latest data (json)  
* `getAll(projectName, deviceName, limit=integer)`  
    Get a chunk of data from your Antares project, you can set the limitation by setting the `limit` parameter.  
    return: Chunk of data from your Antares device  

* `getAllId(projectName, deviceName, limit=integer)`  
    Get a chunk of data IDs from your Antares project, you can set the limitation by setting the `limit` parameter.  
    return: Chunk of data IDs from your Antares device  

* `getSpecific(projectName, deviceName, data-id)`  
    Get specific data from your Antares device, the `data-id` parameter looks like this: `cin_81723819`.  
    return: Specific device data  

* `getDeviceId(projectName, deviceName)`  
    Get your Antares device ID.  
    return: antares device ID (i.e. `cnt-44637281`)  

* `send(data, projectName, deviceName)`  
    Send data to your Antares project. This can be a python dictionary or string.  
    return: POST response data from Antares  

* `sendById(data, device-id)`  
    Send data to your Antares device through Antares device ID which looks like `cnt-281727372`  
    return: POST response data from Antares  

* `createDevice(projectName, newDeviceName)`  
    Create an Antares device in your Project.  
    return: device creation response  

* `getDevices(projectName)`  
    Get all device names of Antares project  
    return: antares device names  
