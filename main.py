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

    choose_channel = input('Choose a channel: ')

    test = int(choose_channel) -1
    convert = f'0{test}'

    radio_station_id = channels[int(convert)]['id']
    api_url_channel = f'https://api.sr.se/api/v2/scheduledepisodes/rightnow?format=json&channelid={radio_station_id}'
    response2 = urllib.request.urlopen(api_url_channel)
    answer2 = response2.read()
    json_dict2 = json.loads(answer2)

    print(json_dict2['channel']['currentscheduledepisode']['starttimeutc'])
    print(json_dict2['channel']['currentscheduledepisode']['program']['name'])

if __name__ == '__main__':
    main()