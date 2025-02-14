def getDictionary(key: str, value: str) -> str:


    dictionary = {
        'full_time': [value[-2],value[-1]],
        '1st_half': [value[0]+value[2],value[1]+value[3]],
        '2st_half': [value[4]+value[6],value[5]+value[7]],
        '1st_quarter': [value[0],value[1]],
        '2nd_quarter': [value[2],value[3]],
        '3rd_quarter': [value[4],value[5]],
        '4th_quarter': [value[6],value[7]],
    }


    return dictionary.get(key)
