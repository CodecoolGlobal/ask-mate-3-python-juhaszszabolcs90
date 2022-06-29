import connection


def generate_id(filename):
    datas = connection.read_data(filename)
    id = max([int(data['id']) for data in datas]) + 1
    return str(id)