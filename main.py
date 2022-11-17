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
        json_date_start = json_dict2['schedule'][i]['starttimeutc']
        json_date_end = json_dict2['schedule'][i]['endtimeutc']
        json_date_start = datetime.datetime.fromtimestamp(int(json_date_start[6:19]) / 1000)
        json_date_end = datetime.datetime.fromtimestamp(int(json_date_end[6:19]) / 1000)
        json_dict2['schedule'][i]['starttimeutc'] = json_date_start
        json_dict2['schedule'][i]['endtimeutc'] = json_date_end


def url_builder(subcategories, params):
    api_url = BASE_URL
    for item in subcategories:
        api_url += item + "/"
    api_url += "?format=json&pagination=false"
    if params != None:
        for key, value in params.items():
            api_url += "&" + key + "=" + str(value)
    return api_url


def response_json_to_dict(api_url):
    response = urllib.request.urlopen(api_url)
    answer = response.read()
    json_dict = json.loads(answer)
    return json_dict


def print_schedule(json_dict_channel):
    counter = 0
    program_info = []
    for program in json_dict_channel["schedule"]:
        if counter > 4:
            return program_info
        if program["endtimeutc"] >= datetime.datetime.now():
            if counter == 0:
                program_info.append({"title": program['title'], "program_id": program['program']['id'], "episode_id": program['episodeid']})
            counter+=1
            print(f"{program['title']}: börjar sändas: {program['starttimeutc'].strftime('%H:%M:%S')}, slutar: {program['endtimeutc'].strftime('%H:%M:%S')}.")


def enumerate_dict_objects(json_dict, level_string):
    enumeration_object = (radio_dict(json_dict[level_string]))
    for i, object_of_dict in enumerate(enumeration_object, start=1):
        print(i, object_of_dict["name"])
    return enumeration_object


def main():
    api_url = url_builder(["channels"], None)
    json_dict = response_json_to_dict(api_url)
    channels = enumerate_dict_objects(json_dict, "channels")

    choose_channel = input('Choose a channel: ')

    import webbrowser

    chosen_channel = int(choose_channel) - 1  # Conversion to 00 format is completely unnecessary
    radio_station_id = channels[chosen_channel]['id']
    # webbrowser.open_new(channels[int(convert)]["audio_url"])
    api_url_channel = url_builder(["scheduledepisodes"], {"channelid": radio_station_id})
    json_dict_channel = response_json_to_dict(api_url_channel)

    date_conversion(len(json_dict_channel['schedule']), json_dict_channel)
    program_info = print_schedule(json_dict_channel)
    reply = input(f"Vill du spela upp {program_info[0]['title']}? Svara med Y eller N.")
    reply = reply.lower()
    if reply == "y":
        webbrowser.open_new(channels[chosen_channel]["audio_url"])
    reply = input(f"Vill du veta mer om {program_info[0]['title']}? Svara med Y eller N.")
    if reply == "y":
        episode_info_url = url_builder(["episodes", "get"], {"id": program_info[0]["episode_id"]})
        episode_info = response_json_to_dict(episode_info_url)
        print(episode_info["episode"]["title"])

    print()
    # print(json_dict2['channel']['currentscheduledepisode']['program']['name'])
    # print(json_dict2['channel']['nextscheduledepisode']['program']['name'])


if __name__ == '__main__':
    main()
