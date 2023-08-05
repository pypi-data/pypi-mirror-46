import typing
import json

def namedtuple_to_json(input: typing.NamedTuple):
    root = input._asdict()
    my_stash = [root]
    while len(my_stash) > 0:
        subroot = my_stash.pop()
        for key in subroot:
            print(key)
            print(subroot[key])
            if hasattr(subroot[key], "_asdict"):
                print("here")
                subroot[key] = subroot[key]._asdict()
                my_stash.append(subroot[key])
    return json.dumps(root)