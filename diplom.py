def find_groups():
    import requests
    import json
    import time
    import pprint
    TOKEN = 'b759f7c046868edeb57b6360e3b507fef5d425a1b34c681de0d378a9fadbc08db9c552f02f968b221ad91'


    #Получаем id пользователя, на котором вся функция выполняется, id его друзей и id его групп
    main_user = input('Введите id ')
    response_main_user_id = requests.get('https://api.vk.com/method/users.get', {'access_token': TOKEN, 'user_ids': main_user, 'v': '5.92'})
    main_user_id = response_main_user_id.json()['response'][0]['id']
    main_params = {
        'access_token': TOKEN,
        'user_id': main_user_id,
        'v': '5.92'
    }
    response_groups_main = requests.get('https://api.vk.com/method/groups.get', main_params)
    groups_main_ids = response_groups_main.json()['response']['items']
    response_friends = requests.get('https://api.vk.com/method/friends.get', main_params)
    friends_ids = response_friends.json()['response']['items']


    #Перебираем всех друзей по id и собираем id всех групп
    groups_for_compare = []

    for id in friends_ids:
        params = {
            'access_token': TOKEN,
            'user_id': id,
            'v': '5.92'
        }
        groups_of_friend_response = requests.get('https://api.vk.com/method/groups.get', params)
        if 'response' in groups_of_friend_response.json():
            groups_of_friend = groups_of_friend_response.json()['response']['items']
            groups_for_compare.append(groups_of_friend)
        time.sleep(0.4)
        print('.')


    #Сравниваем полученый список со списком главного пользователя, если находим совпадение - вычеркиваем группу
    for list_of_groups in groups_for_compare:
        for group in list_of_groups:
            if group in groups_main_ids:
                groups_main_ids.remove(group)


    #Делаем из списка оставшихся id строку для дальнейшего получения полной инфы о группах
    i = 0
    while i < len(groups_main_ids):
        groups_main_ids[i] = str(groups_main_ids[i])
        i+=1
    groups_main_ids_str = ','.join(groups_main_ids)


    #Получаем нужную инфу по группам
    params_for_groups = {
        'access_token': TOKEN,
        'group_ids': groups_main_ids_str,
        'v': '5.92',
        'fields': 'members_count'
    }
    groups_info_responce = requests.get('https://api.vk.com/method/groups.getById', params_for_groups)
    groups_info = groups_info_responce.json()['response']


    #Создаем json файл
    for_json = []
    for group in groups_info:
        cell = {
            "name": "{}".format(group['name']),
            "gid": "{}".format(group['id']),
            "members_count": group['members_count']
        }
        for_json.append(cell)
    json_file = json.dumps(for_json)
    with open('groups.json', 'w') as file:
        file.write(json_file)

    print('Работа программы завершена')


find_groups()