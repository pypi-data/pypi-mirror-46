import requests
import json

def _asserter(testCaseInstance, msg):
  if testCaseInstance is None:
    raise Exception(msg)
  testCaseInstance.assertTrue(False, msg=msg)

#sends input as JSON
def callService(testCaseInstance, url, headers, method, dataDICT, expectedResponses):
  result = None
  targetURL = url
  headers = {}
  data = None
  requestsFn = None
  if method=='get':
    requestsFn = requests.get
  if method=='post':
    headers['content-type'] = 'application/json'
    data=json.dumps(dataDICT)
    requestsFn = requests.post
  if method=='put':
    headers['content-type'] = 'application/json'
    data=json.dumps(dataDICT)
    requestsFn = requests.put
  if method=='delete':
    requestsFn = requests.delete
    
  if requestsFn is None:
    _asserter(testCaseInstance,"Invalid method")
    return None, None
    
  numTries = 0
  unsucessful = True
  while unsucessful:
    unsucessful = False
    if numTries > 0:
      print(" Call failed (try " + str(numTries) + ") - retrying...")
      time.sleep(1)
    numTries = numTries + 1
    try:
      result = requestsFn(
        targetURL,
        data=data,
        headers=headers
      )
    except Exception as err:
      unsucessful = True
      if numTries > 60:
        print("We have been trying too many times - giving up")
        raise err 
      

  if result.status_code not in expectedResponses:
    print("Sending " + method + " to ", targetURL)
    if dataDICT is not None:
      print(" data:", dataDICT)
    print("Got response ",result.status_code)
    print("     ",result.text)
    
    _asserter(testCaseInstance,"Did not get expected response")
    return None, None
  return result.text, result.status_code
  
  
def callGetService(testCaseInstance, url, headers,expectedResponses):
  return callService(testCaseInstance, url, headers, "get", None, expectedResponses)

def callPostService(testCaseInstance, url, headers, POSTdict, expectedResponses):
  return callService(testCaseInstance, url, headers, "post", POSTdict, expectedResponses)

def callPutService(testCaseInstance, url, headers, PUTdict, expectedResponses):
  return callService(testCaseInstance, url, headers, "put", PUTdict, expectedResponses)

def callDeleteService(testCaseInstance, url, headers, expectedResponses):
  return callService(testCaseInstance, url, headers, "delete", None, expectedResponses)
