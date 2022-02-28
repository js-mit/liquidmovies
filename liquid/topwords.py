def get_topwords(data, topnum):
    topwords_lookup = {}
    confidence_threshold = 0.8
    for obj in data: 
        if obj['Label']['Confidence']>confidence_threshold:
            name = obj['Label']['Name']
            if name in topwords_lookup:
                topwords_lookup[name] += 1
            else:
                topwords_lookup[name] = 1

            for parent in obj['Label']['Parents']:
                name = parent['Name']
                if name in topwords_lookup:
                    topwords_lookup[name] += 1
                else:
                    topwords_lookup[name] = 1
    
    topwords_lookup = sorted(topwords_lookup.items(), key=lambda item: item[1], reverse=True)
    
    topwords_list = []
    for i in range(topnum):
        topwords_list.append(topwords_lookup[i][0])

    return topwords_list
