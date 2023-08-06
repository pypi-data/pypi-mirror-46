import json
import re


def read_json_to_dict(file_name):
    with open(file_name) as fh:
        return json.load(fh)


def json_to_dict(json_str):
    return json.load(json_str)


def read_mean_time(pattern, folder_name):
    result = read_json_to_dict(f'{folder_name}/statistics.json')
    for key, value in result.items():
        if re.match(pattern, key):
            for k, v in value.items():
                if k == "meanResTime":
                    return v
