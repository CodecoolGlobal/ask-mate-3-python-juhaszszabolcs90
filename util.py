def generate_id():
    datas = get_all_user_story(filename)
    id = max([int(data['id']) for user_story in datas]) + 1
    return str(id)