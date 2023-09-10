import re


def update_memory(scrath_memory, logs):
    """
    receive the object and location, return the event happened nearby
    :param scrath_memory:
    :param objects: ""
    :return: the most possible events can be realized, list["build a house"]
    """
    status = get_status_from_log(logs)
    object = get_object_from_log(logs)
    if status:
        scrath_memory["currently"] = status
    if object:
        scrath_memory["objects"] = object
    # print(scrath_memory)
    return scrath_memory


def summary_memory(scrath_memory):
    """
    summary ai's_memory and update it
    :param persona:
    :return: new memory
    """
    pass


def get_status_from_log(logs):
    """
    get the current state from the log
    :logs: list['','']
    :return: latest action or status the agent gets
    """

    # get the agent's current status
    pattern_status = r'Tag Als\.Gait\.(\w+) (Added|Removed)! Time: (\d+\.\d+)'

    status_data = {}
    for log in logs:
        match = re.search(pattern_status, log)
        if match:
            tag = match.group(1)
            op = match.group(2)
            timestamp = match.group(3)

            if op == 'Added':
                status_data[tag] = timestamp
            elif op == 'Removed' and tag in status_data and float(timestamp) > float(status_data[tag]):
                del status_data[tag]
    # print(status_data)
    return list(status_data.keys())[-1]


def get_object_from_log(logs):
    """
    get the nearby object from the log
    :logs: list['','']
    :return: a str which contains the object near the agent
    """
    # get the agent's nearby object
    pattern_object = r'Component .+? with tag \w+\.(\w+) in actor .+? with tag Entity\.(\w+) (entered|leaved) (\d+(?:\.\d+)?)m! Time: (\d+\.\d+)'

    object_data = {}
    for log in logs:
        match = re.search(pattern_object, log)
        if match:
            tag = match.group(1)
            entity = match.group(2)
            op = match.group(3)
            distance = match.group(4)
            timestamp = match.group(5)
            # print(tag, entity, op, distance, 'm at time:' , timestamp)
            if op == 'entered':
                object_data[entity] = distance
            elif op == 'leaved' and entity in object_data:
                if float(distance) >= 10:
                    del object_data[entity]

    # print(object_data)
    object_str = ""
    for key in object_data.keys():
        object_str = object_str + key + ","
    return object_str


# if __name__ == '__main__':
#     update_memory(scrath_memory, logs)
