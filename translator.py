import json
import requests

list = []

def fromJson(path, json_file):
    for key in json_file:
        value = json_file[key]
        if isinstance(value, dict):
            fromJson(path + "." + key, value)
        else:
            list.append({
                "key": path + "." + key,
                "value": value.replace("\n", "<0\>")
            })


def toJson(list):
    json = {}

    for entry in list:
        value = entry["value"].replace("<0\>", "\n")
        key = entry["key"]

        split = key.split(".")

        json_builder = json

        for i in range(0, len(split) - 1):
            if not split[i] in json_builder:
                json_builder[split[i]] = {}
            json_builder = json_builder[split[i]]

        json_builder[split[len(split) - 1]] = value

    return json

def tranlate_yandex(value, from_language, to_language):
    if value is None:
        return None
    if value == "":
        return ""

    if from_language == to_language:
        return value
    else:
        url = "https://translate.yandex.net/api/v1.5/tr.json/translate"
        params = {
            "key": "",
            "text": value,
            "lang": from_language + "-" + to_language,
            "options": 1
        }
        response = requests.get(url, params=params)

        if response.status_code == 200:
            return response.json()["text"][0]
        else:
            print("Error: " + str(response.status_code))
            print(response.text)
            return value

def tranlate_deepl_free(value, from_language, to_language):
    if value is None:
        return None
    if value == "":
        return ""

    if from_language == to_language:
        return value
    else:
        url = "https://api-free.deepl.com/v2/translate";
        header = {
           "auth_key" : ""
        }
        params = {
            "target_lang" : to_language,
            "source_lang" : from_language,
            "text" : value
        }
        response = requests.post(url, headers=header, data=params)
        if response.status_code == 200:
            return response.json()["translations"][0]["text"]
        else:
            print("Error: " + str(response.status_code))
            print(response.text)
            return value


def write_json(file_name, data):
    with open(file_name, 'w', encoding="utf8") as f:
        f.write(json.dumps(data, ensure_ascii=False, indent=4))

def load_json(file_name):
    with open(file_name, 'r', encoding="utf8") as f:
        data = json.loads(f.read())

        for key in data:
            value = data[key]

            if isinstance(value, dict):
                fromJson(key, value)
            else:
                list.append({
                    "key": key,
                    "value": value.replace("\n", "<0\>")
                })


from_language = "en";
to_language = "ru"
file = from_language + ".json";

print("Read File")
load_json(file)

print("Translate")
for key in list:
    key["value"] = tranlate_yandex(key["value"], from_language, to_language)

print("Write File")
write_json(to_language + ".json", toJson(list))

print("Done!")
