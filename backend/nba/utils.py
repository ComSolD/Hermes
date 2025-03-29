def calculate_statistic_display(statistic_values, mode):
    if not statistic_values:
        return None

    if mode == "avg":
        return round(sum(statistic_values) / len(statistic_values), 2)
    elif mode == "list":
        return statistic_values