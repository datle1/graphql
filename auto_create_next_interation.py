# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import datetime
import json
import requests
import sys

NUMBER_NEW_ITERATION = 4
ACCESS_TOKEN = ''

def rest_api_post(body_data):
    auth = 'Bearer ' + ACCESS_TOKEN
    resp = requests.post('http://10.240.203.2:8180/api/graphql',
                         data=json.dumps(body_data),
                         headers={'Content-Type': 'application/json',
                                  'Authorization': auth})
    if resp.status_code != 200:
        # This means something went wrong.
        raise Exception('GraphQL API create error: {}'.format(resp.json()))
    return resp.json()


def get_all_iteration():
    body_data = {"query": "query {group(fullPath:\"sdn\")"
                          "{iterations{nodes{title dueDate}}}}"}
    return rest_api_post(body_data)


def next_weekday(d, weekday):
    days_ahead = weekday - d.weekday()
    if days_ahead <= 0:
        days_ahead += 7
    return d + datetime.timedelta(days_ahead)


def get_next_iteration(last_ind, last_d):
    d = last_d.split('-')
    day = datetime.datetime(int(d[0]), int(d[1]), int(d[2]))
    next_monday = next_weekday(day, 0)
    next_friday = next_weekday(day, 4)
    start = str(next_monday).split(' ')[0]
    end = str(next_friday).split(' ')[0]
    if not start or not end:
        raise Exception('Can not get next date')
    return (last_ind+1), start, end


def generate_iteration_name(num, start, due):
    return "Sprint " + str(num) + " [" + str(start) + " " + str(due) + "]"


def get_nodes_iteration(all_iter):
    return all_iter['data']['group']['iterations']['nodes']


def find_last_date(list_node):
    last_day = None
    max_index = 0
    for node in list_node:
        index = int(node['title'].split(' ')[1])
        if index > max_index:
            max_index = index
            last_day = node['dueDate']
    if not last_day or max_index == 0:
        raise Exception('Can not get last date')
    return max_index, last_day


def create_next_iteration(name, start, due):
    create_data = "title:\"" + name + "\",startDate:\"" + start + "\",dueDate:\"" + due + "\""
    body_data = {"query": "mutation{createIteration(input:{groupPath:\"sdn\","
                          + create_data
                          + "}){ iteration{id title} errors}}"}
    rest_api_post(body_data)


if __name__ == '__main__':
    ACCESS_TOKEN = sys.argv[1] 
    all_iterations = get_all_iteration()
    list_node_content = get_nodes_iteration(all_iterations)
    last_index, last_date = find_last_date(list_node_content)
    for i in range(0, NUMBER_NEW_ITERATION):
        number, startDate, dueDate = get_next_iteration(last_index, last_date)
        iteration_name = generate_iteration_name(number, startDate, dueDate)
        print(iteration_name)
        create_next_iteration(iteration_name, startDate, dueDate)
        last_index += 1
        last_date = dueDate
    print("Success create " + str(NUMBER_NEW_ITERATION) + " iteration")
