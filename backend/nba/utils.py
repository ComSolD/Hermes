def calculate_statistic_display(statistic_values, mode):
    if not statistic_values:
        return None

    if mode == "avg":
        return round(sum(statistic_values) / len(statistic_values), 2)
    elif mode == "list":
        return statistic_values
    elif mode == "overdrawunder":
        from collections import Counter
        counts = Counter(statistic_values)

        # Отображаем в читаемом порядке
        result = []
        for key in ["Больше", "Равно", "Меньше"]:
            if key in counts:
                result.append(f"{key} — {counts[key]} раз(а)")
        return result