import json


def beautify_json(json_obj):
    return json.dumps(json_obj, indent=2, sort_keys=True)


def print_pretty(data):
    if type(data) is str \
            or type(data) is dict \
            or type(data) is list:
        json_obj = data
        if type(data) is str:
            json_obj = json.loads(json)
        json_str = beautify_json(json_obj)
        print(json_str)
    else:
        print('print pretty failed')


def flatten_json(y):
    out = {}

    def flatten(x, name=''):
        if type(x) is dict:
            for a in x:
                flatten(x[a], name + a + '.')
        elif type(x) is list:
            i = 0
            for a in x:
                flatten(a, name + str(i) + '.')
                i += 1
        else:
            out[name[:-1]] = x

    flatten(y)
    return out
