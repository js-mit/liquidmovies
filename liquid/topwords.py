def gettopwords(data, topnum):

    key = "Name"
    
    # find occurence of each key
    def findOcc(arr, key):
        arr2 = []
        for object in arr: 
            name = object["Label"][key]
            nameexist = False
            for obj in arr2:
                if (obj[key] == name):
                    nameexist = True 
                    break 
            if (nameexist): 
                for obj in arr2:
                    if (obj[key] == name):
                        obj["occurrence"] += 1
            else: 
                newobj = {}
                newobj[key] = name
                newobj["occurrence"] = 1
                arr2.append(newobj)
        return arr2
        
    def sortOcc (obj):
        return obj["occurrence"]

    # sort the array 
    list = findOcc(data, key)
    list.sort(key=sortOcc, reverse=True)
   
    toplist = []
    for i in range(topnum):
        toplist.append(list[i][key])

    return toplist

