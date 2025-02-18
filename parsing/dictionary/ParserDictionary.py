def getDictionary(dictionary: str, tournament:str, key: str) -> str:
    parsers = {'Espn': 'Parsing' + tournament + '(str(self.ui.FirstDate.date().toPyDate()), str(self.ui.SecondDate.date().toPyDate())).date_cycle()',
        'Odds': 'Odds' + tournament + '(str(way), str(self.ui.SecondDate.date().toPyDate())).get_matches_link()',
        'NFL': 'ParsingNFL(year, stage, parser_type).date_cycle()',
    }


    parsers_option ={
        'Wild Card': [1, 3],
        'Divisional Round': [2, 3],
        'Conf. Champ.': [3, 3],
        'Super Bowl': [5,3],
        'Весь сезон': [True],

        'Собрать исходы': 'past',
        'Собрать предикты': 'bet',
    }

    if dictionary == 'parsers':
        if tournament != 'NFL':
            return parsers.get(key)
        else:
            return parsers.get('NFL')
    else:
        return parsers_option.get(key)
    