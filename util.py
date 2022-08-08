# import connection
# import datetime
# import data_manager
#
# headers = connection.DATA_HEADER
#
# def generate_id(filename):
#     datas = connection.read_data(filename)
#     id = max([int(data['id']) for data in datas]) + 1
#     return str(id)
#
# def convert_timestamp(timestamp):
#     return datetime.datetime.fromtimestamp(timestamp).strftime("%Y %B, %d")
#
# def generate_timestamp():
#     return datetime.datetime.timestamp(datetime.datetime.now())
#
# def vote(filename, headers, id, up=True):
#     datas = connection.read_data(filename)
#
#     for data in datas:
#         if data['id'] == id:
#             if not up and int(data['vote_number']) > 0:
#                 vote_num = int(data['vote_number'])
#                 vote_num -= 1
#                 data['vote_number'] = str(vote_num)
#             elif up:
#                 vote_num = int(data['vote_number'])
#                 vote_num += 1
#                 data['vote_number'] = str(vote_num)
#
#     data_manager.update_data(filename, datas, headers)
#
#
# def convert_headers(headers):
#     return [header.upper().replace('_', ' ') for header in headers]
#
