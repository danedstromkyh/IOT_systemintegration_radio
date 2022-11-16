import datetime
import json
import urllib.request

BASE_URL = "http://api.sr.se/api/v2/"


def radio_dict(json_dict):
    my_list = []

    for channel in json_dict:
        my_list.append({"id": channel['id'], "name": channel['name'], "audio_url": channel['liveaudio']['url']})

    return my_list


def date_conversion(convert, json_dict2):
    for i in range(convert):
        json_date = json_dict2['schedule'][i]['starttimeutc']
        json_date = datetime.datetime.utcfromtimestamp(int(json_date[6:19]) / 1000)
        json_dict2['schedule'][i]['starttimeutc'] = json_date


def url_builder(subcategories, params):
    api_url = BASE_URL
    for item in subcategories:
        api_url += item + "/"
    api_url += "?format=json&pagination=false"
    if params != None:
        for key, value in params:
            api_url += "&" + key + "=" + value
    return api_url


def response_json_to_dict(api_url):
    response = urllib.request.urlopen(api_url)
    answer = response.read()
    json_dict = json.loads(answer)
    return json_dict


def main():
    api_url = url_builder(["channels"], None)
    json_dict = response_json_to_dict(api_url)
    channels = (radio_dict(json_dict['channels']))

    for i, station in enumerate(channels, start=1):
        print(i, station["name"])

    choose_channel = input('Choose a channel: ')

    import webbrowser

    chosen_channel = int(choose_channel) - 1  # Conversion to 00 format is completely unnecessary

    radio_station_id = channels[chosen_channel]['id']
    # webbrowser.open_new(channels[int(convert)]["audio_url"])
    api_url_channel = url_builder(["scheduledepisodes"], {"channelid":radio_station_id})
    response2 = urllib.request.urlopen(api_url_channel)
    answer2 = response2.read()
    json_dict2 = json.loads(answer2)
    date_conversion(len(json_dict2['schedule']), json_dict2)
    print(json_dict2['schedule'][chosen_channel]['starttimeutc'])
    # print(json_dict2['channel']['currentscheduledepisode']['program']['name'])
    # print(json_dict2['channel']['nextscheduledepisode']['program']['name'])


if __name__ == '__main__':
    main()
