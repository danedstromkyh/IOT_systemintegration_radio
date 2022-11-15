import json
import urllib.request


def radio_dict(d):
    my_list = []
    index = 1
    for channel in d:
        my_list.append({"index": index, "id": channel['id'], "name": channel['name']})
        index += 1

    return my_list


def main():
    api_url = 'http://api.sr.se/api/v2/channels/?format=json'
    response = urllib.request.urlopen(api_url)

    answer = response.read()
    json_dict = json.loads(answer)

    channels = (radio_dict(json_dict['channels']))

    for station in channels:
        print(f'{station["index"]} : {station["name"]}')

    input("Choose a radio station: ")


if __name__ == '__main__':
    main()