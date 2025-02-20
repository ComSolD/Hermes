from datetime import datetime
import numpy as np

def date_redact(dates: list):

    date = dates[1]

    date_obj = datetime.strptime(date, "%d %b %Y,")
    formatted_date = date_obj.strftime("%d-%m-%Y")

    return formatted_date


def date_redact_full_month(date: str):

    date_obj = datetime.strptime(date, "%B %d %Y")
    formatted_date = date_obj.strftime("%d-%m-%Y")

    return formatted_date


def time_redact(time: str):

    time_obj = datetime.strptime(time, "%I:%M %p")
    formatted_time = time_obj.strftime("%H:%M")

    return formatted_time


def total_odds_redact(total: list):

    split = np.array_split(total, len(total) // 6)

    result = list()

    for array in split:
        lst = list(map(str, array))

        if lst[-3] != '-' and lst[-2] != '-':

            lst.pop(-1)
            lst.pop(0)
            lst.pop(1)

            lst[0] = lst[0].replace('O/U +', '')
            lst[0] = lst[0].replace(' ', '')

            result.append(lst)


    return result


def handicap_odds_redact(handicap: list):

    split = np.array_split(handicap, len(handicap) // 6)

    result = list()

    for array in split:
        lst = list(map(str, array))

        if lst[-3] != '-' and lst[-2] != '-':

            lst.pop(-1)
            lst.pop(0)
            lst.pop(1)

            lst[0] = lst[0].replace('AH ', '')
            lst[0] = lst[0].replace(' ', '')

            result.append(lst)


    return result
