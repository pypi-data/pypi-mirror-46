from sparrow.src.helper import info, extract_info
import json


class SparrowManager:

    @staticmethod
    def extract(source, target, fname="output.json"):

        target_key = [k for k in target.keys()][0]

        temp_tags = []
        temp_triggers_ids = []
        temp_triggers = []
        not_found_tags = []

        for stp in source.get('containerVersion').get('tag'):
            if stp.get('setupTag'):
                for s in stp.get('setupTag'):
                    target[target_key].append(s['tagName'])

        for k in target[target_key]:
            for t in source['containerVersion']['tag']:
                if t['name'] == k:
                    temp_tags.append(t)
                    try:
                        temp_triggers_ids.append(t['firingTriggerId'])
                    except KeyError:
                        pass
                else:
                    not_found_tags.append(t['name'])

        for tri in source['containerVersion']['trigger']:
            for t in extract_info(temp_triggers_ids):
                if t == tri['triggerId']:
                    temp_triggers.append(tri)

        source['containerVersion']['tag'] = temp_tags
        source['containerVersion']['trigger'] = temp_triggers

        with open('output.json', "w") as f:
            json.dump(fp=f, obj=source)
            print("Successful > output.json generated")
        SparrowManager.info(source)

    @staticmethod
    def info(source):
        print(info(source))
