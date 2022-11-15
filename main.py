import json
import urllib.request


def radio_dict(d):
    my_list = []

    for channel in d:
        my_list.append({"id": channel['id'], "name": channel['name']})

    return my_list


def main():
    api_url = 'http://api.sr.se/api/v2/channels/?format=json'
    response = urllib.request.urlopen(api_url)

    answer = response.read()
    json_dict = json.loads(answer)

    channels = (radio_dict(json_dict['channels']))

    for i, station in enumerate(channels, start=1):
        print(i, station["name"])


if __name__ == '__main__':
    main()