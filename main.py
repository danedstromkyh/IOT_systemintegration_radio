import datetime
import json
import urllib.request


def radio_dict(json_dict):
    my_list = []

    for channel in json_dict:
        my_list.append({"id": channel['id'], "name": channel['name'], "audio_url": channel['liveaudio']['url']})

    return my_list


# def indices_conversion(dict, category):
#     for i in range (10):
#         dict[category][i] = dict[category].items.pop(int(f"0{i}"))


def date_conversion(convert, json_dict2):
    for i in range ():
        json_date = json_dict2['schedule'][int(f"0{i}")]['starttimeutc']
        json_date = datetime.datetime.utcfromtimestamp(int(json_date[6:19]) / 1000)
        json_dict2['schedule'][int(f"0{i}")]['starttimeutc'] = json_date


def main():
    api_url = 'http://api.sr.se/api/v2/channels/?format=json&pagination=false'
    response = urllib.request.urlopen(api_url)

    answer = response.read()
    json_dict = json.loads(answer)
    indices_conversion(json_dict, "channels")
    channels = (radio_dict(json_dict['channels']))

    for i, station in enumerate(channels, start=1):
        print(i, station["name"])

    choose_channel = input('Choose a channel: ')

    import webbrowser


    test = int(choose_channel) -1
    convert = f'0{test}'

    radio_station_id = channels[int(convert)]['id']
    # webbrowser.open_new(channels[int(convert)]["audio_url"])
    api_url_channel = f"http://api.sr.se/api/v2/scheduledepisodes?format=json&pagination=false&channelid={radio_station_id}" # 'https://api.sr.se/api/v2/scheduledepisodes/rightnow?format=json&channelid={radio_station_id}'
    response2 = urllib.request.urlopen(api_url_channel)
    answer2 = response2.read()
    json_dict2 = json.loads(answer2)
    date_conversion(int(convert), json_dict2)
    print(json_dict2['schedule'][int(convert)]['starttimeutc'])
    # print(json_dict2['channel']['currentscheduledepisode']['program']['name'])
    # print(json_dict2['channel']['nextscheduledepisode']['program']['name'])


if __name__ == '__main__':
    main()