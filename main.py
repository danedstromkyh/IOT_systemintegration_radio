import datetime
import json
import urllib.request

BASE_URL = "http://api.sr.se/api/v2/"


def clean_dict(json_dict):
    cleaned_list = []

    for channel in json_dict:
        cleaned_list.append({"id": channel['id'], "name": channel['name'], "audio_url": channel['liveaudio']['url']})

    return cleaned_list


def date_conversion(length_of_subcategory, json_dict, subcategory):
    for i in range(length_of_subcategory):
        json_date_start = json_dict[subcategory][i]['starttimeutc']
        json_date_end = json_dict[subcategory][i]['endtimeutc']
        json_date_start = datetime.datetime.fromtimestamp(int(json_date_start[6:19]) / 1000)
        json_date_end = datetime.datetime.fromtimestamp(int(json_date_end[6:19]) / 1000)
        json_dict[subcategory][i]['starttimeutc'] = json_date_start
        json_dict[subcategory][i]['endtimeutc'] = json_date_end


# Takes params and subcategories of the API call allowing us to build an url specific to our current needs.
def url_builder(subcategories, params):
    api_url = BASE_URL
    for item in subcategories:
        api_url += item + "/"
    api_url += "?format=json&pagination=false"
    if params != None:
        for key, value in params.items():
            api_url += "&" + key + "=" + str(value)
    return api_url


# Consumes an API resource at the input url, returning a dict of the json response.
def response_json_to_dict(api_url):
    response = urllib.request.urlopen(api_url)
    answer = response.read()
    json_dict = json.loads(answer)
    return json_dict


# Loops through the schedule of a specific channel and returns program info of the upcoming (input) number of programs
def print_schedule_return_program_info(json_dict_channel, subcategory, number_of_episodes_to_be_printed):
    counter = 0
    program_info = []
    for program_object in json_dict_channel[subcategory]:
        if counter > number_of_episodes_to_be_printed:
            return program_info
        if program_object["endtimeutc"] >= datetime.datetime.now():
            if counter < number_of_episodes_to_be_printed:
                try:
                    program_info.append(
                        {"title": program_object['title'], "subtitle": program_object['subtitle'], "program_id": program_object['program']['id'], "episode_id":
                            program_object['episodeid']})
                except KeyError:
                    program_info.append(
                        {"title": program_object['title'], "program_id": program_object['program']['id']})
            counter += 1
            try:
                print(
                    f"{program_object['starttimeutc'].strftime('%H:%M:%S')} - {program_object['endtimeutc'].strftime('%H:%M:%S')}  {program_object['title']} {program_object['subtitle']}")
            except KeyError:
                print(
                    f"{program_object['starttimeutc'].strftime('%H:%M:%S')} - {program_object['endtimeutc'].strftime('%H:%M:%S')}  {program_object['title']}")


def enumerate_dict_objects(json_dict, level_string):
    enumeration_object = (clean_dict(json_dict[level_string]))
    for i, object_of_dict in enumerate(enumeration_object, start=1):
        print(i, object_of_dict["name"])
    return enumeration_object


def menu(dict_scope):
    # Print currents scope actions
    # Take user input
    # return current scope
    pass


def helper_function():
    pass


def main():
    api_url = url_builder(["channels"], None)
    json_dict = response_json_to_dict(api_url)
    channels = enumerate_dict_objects(json_dict, "channels")

    choose_channel = input('Choose a channel: ')

    import webbrowser

    chosen_channel = int(choose_channel) - 1  # Conversion to 00 format is completely unnecessary
    radio_station_id = channels[chosen_channel]['id']
    api_url_channel = url_builder(["scheduledepisodes"], {"channelid": radio_station_id})
    json_dict_channel = response_json_to_dict(api_url_channel)

    date_conversion(len(json_dict_channel['schedule']), json_dict_channel, "schedule")
    program_info = print_schedule_return_program_info(json_dict_channel, "schedule", 5)

    reply = input(f"Vill du spela upp {program_info[0]['title']}? Svara med Y eller N.")
    reply = reply.lower()
    if reply == "y":
        webbrowser.open_new(channels[chosen_channel]["audio_url"])
    reply = input(f"Vill du veta mer om {program_info[0]['title']}? Svara med Y eller N.")
    if reply == "y":
        try:
            episode_info_url = url_builder(["episodes", "get"], {"id": program_info[0]["episode_id"]})
            episode_info = response_json_to_dict(episode_info_url)
            print(episode_info["episode"]["title"])
        except KeyError:
            print("Ingen information om programmet tillgängligt")


if __name__ == '__main__':
    main()
