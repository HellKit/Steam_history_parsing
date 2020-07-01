def read_file_get_data(file_name, cell, symbol):
    with open(file_name, encoding='utf-8') as f:
        data = [
            elem.split(symbol)[-1].strip()[:-5]
            for elem in
            f.readlines() if cell in elem.lower()
        ]
    data = [float(elem.replace(',', '.')) for elem in data]
    return data


print('Потрачено денег: ', round(sum(read_file_get_data(
    file_name='steam_data.txt', cell='куплено', symbol='--->')), 2))

print('Получено денег: ', round(sum(read_file_get_data(
    file_name='steam_data.txt', cell='продано', symbol='--->')), 2))
