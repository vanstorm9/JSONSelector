import json
import re

jsonPath = 'data/SystemViewController.json'
with open(jsonPath) as json_data:
    data = json.load(json_data,)

#class, (.) classNames , (#) identifier 
# There are helper classes to help work with compound selectors and selector chains

def parseSelChain(key,val,targetAr):
  # To help deal with selector chains (we iterate through chain string, split it, and append target attributes in a list of search values)
  searchList = []
  for targetVal in targetAr:
    # We will have to find the chain
    delimitSplit = re.split('([#.])',targetVal)
    if len(delimitSplit) == 3 and val == delimitSplit[0]:
      # We retrieve list of  
      searchList.append(delimitSplit[1] + delimitSplit[2])

  return searchList

def matchJSON(key,val,targetAr):
  # So that we match the correct values to tags when dealing with compound chains
  for targetVal in targetAr:
    if len(targetVal) == 0:
      continue
    
    if targetVal[1:] == val:
      # Check to see if values match (with assumption attribute delimiter exists)
      if key.lower() == 'identifier' and targetVal[0] == '#':
        return True
      elif key.lower() == 'classnames' and targetVal[0] == '.':
        return True
      
    elif targetVal == val and key.lower() == 'class':
        # Check to see if values does match and if it is a class 
        return True
      
  return False


def iterateJSON(data,prevData,keyPrev,targetAr,resList,searchList,savedData):
  # The main recursive function

  if isinstance(data,dict):
    for key,value in data.items():
      
      if matchJSON(key,value,targetAr):
        # Dealing with compound selectors
        resList.append(data)

      if matchJSON(key,value,searchList)  and savedData not in resList: 
        # Ths means we found the target attribute (classname/identifier) associated with our parent class
        resList.append(savedData)
        return resList
      else:
        if len(searchList) == 0:
          # Based on the class we found, we extract the target attributes from the selector chain strings
          searchList = parseSelChain(key,value,targetAr)
          savedData = data # We take the current section of JSON and add to resList if target attribute is present
 
        iterateJSON(value,data,key,targetAr,resList,searchList,savedData)
          
  elif isinstance(data,list):
    for i,subdata in enumerate(data):
      if isinstance(subdata,str):
        if matchJSON(keyPrev,subdata,targetAr):
          # Dealing with compound selectors
          resList.append(prevData)
        if matchJSON(keyPrev,subdata,searchList) and savedData not in resList:
          resList.append(savedData)
          return resList

      iterateJSON(subdata,data,keyPrev,targetAr,resList,searchList,savedData)
      
  
  return resList
  
def main():
  # subviews, contentView, input and control
  print("Type in a JSON selector input string:")
  inputStr = input()

  inputAr = inputStr.split(" ") # For compund selector

  result = iterateJSON(data,data,'',inputAr,[], [],None)

  for i,resEle in enumerate(result):
    print("------------------")
    print(i, ": ", resEle)
  return

if __name__ == "__main__":
  main()

