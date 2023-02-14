import json
import logging

def read_json_(pathname):
    try:
        with open(pathname, 'r') as f:
            content = json.load(f)
        return content
    except Exception(e):
        logging.debug("read json error, may not be in json format %s",str(e))
        return


def save_json_(pathname,data):
    data_to_json = json.dumps(data, ensure_ascii=False, indent=2)
    try:
        file_json = open(pathname, 'w+')
        file_json.write(data_to_json)
    except Exception(e):
        logging.debug("write data to json error, because %s",str(e))
        return
    finally:
        file_json.close()
