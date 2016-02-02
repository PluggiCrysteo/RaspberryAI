import json,task

with open('test.json') as json_file:
    data = json.load(json_file)
    print(data)

    tasks = []
    for uselesskey,json_dict in data.iteritems():
        tasks.append(task.Task(json_dict))

    for mTask in tasks:
        print mTask
