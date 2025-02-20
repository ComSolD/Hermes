def getDictionary(key: str, value: str) -> str:


    dictionary = {
        'full_time': [value[-2],value[-1]],
        '1st_period': [value[0],value[1]],
        '2nd_period': [value[2],value[3]],
        '3rd_period': [value[4],value[5]],
    }


    return dictionary.get(key)
