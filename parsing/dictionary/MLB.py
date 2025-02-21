def getDictionary(key: str, value: str) -> str:


    dictionary = {
        'full_time': [value[-2],value[-1]],
        '1st_half': [value[0]+value[2]+value[4]+value[6]+value[8],value[1]+value[3]+value[5]+value[7]+value[9]],
        '2nd_half': [value[10]+value[12]+value[14]+value[16],value[11]+value[13]+value[15]+value[17]],
        '1st_inning': [value[0],value[1]],
        '2nd_inning': [value[2],value[3]],
        '3rd_inning': [value[4],value[5]],
        '4th_inning': [value[6],value[7]],
        '5th_inning': [value[8],value[9]],
        '6th_inning': [value[10],value[11]],
        '7th_inning': [value[12],value[13]],
        '8th_inning': [value[14],value[15]],
        '9th_inning': [value[16],value[17]],

    }


    return dictionary.get(key)
