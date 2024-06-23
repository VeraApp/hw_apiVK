import classVK
import datetime
import json
import classYanDisk
import log

# Количество фотографий, которые загружаются на Яндекс Диск
COUNT_PHOTOS = 5

# Получить удобочитаемое время
def get_readable_time(ts):
    return datetime.datetime.utcfromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')

# Создаем список с информацией о выбранных изображениях
def sort_json_photos(photos_info):
    items = photos_info['response']['items']
    list_data = []
    likes_list = count_likes_photos(items)
    for index, element in enumerate(items):
        if index >= COUNT_PHOTOS and COUNT_PHOTOS is not None:
            break
        like = element['likes']['count']
        date = get_readable_time(element['date'])
        if like in likes_list:
            like = f'{like}_{date}'
        size, url = get_size_url(element['sizes'])
        list_data.append((like, date, size, url))
    return list_data

# Отбор совпадающих значений лайков
def count_likes_photos(items):
    items = photos_info['response']['items']
    likes_list = []
    for index, element in enumerate(items):
        if index >= COUNT_PHOTOS and COUNT_PHOTOS is not None:
            break
        like = element['likes']['count']
        likes_list.append(like)
    return dict((x, likes_list.count(x)) for x in set(likes_list) if likes_list.count(x) > 1)

# Нахождение максимального размера изображения
def get_size_url(sizes):
    list_photo = []
    for idx, element in enumerate(sizes):
        list_photo.append((idx, element['height']))

    sorted_list = sorted(list_photo, key=lambda x: x[1], reverse=True)

    max_height_id = sorted_list[0][0]

    return sizes[max_height_id]["type"], sizes[max_height_id]["url"]

# Запись сведений по фотографиям в json-файл
def load_data_json(info_sort):
    final_json = []
    for idx, element in enumerate(info_sort):
        final_json.append({"file_name": f"{element[0]}.jpg", "size": f"{element[2]}"})

    with open('files/data.json', 'w') as file:
        json.dump(final_json, file)


if __name__ == '__main__':
    log.logging.info("Start program")
    token_vk = input("Введите access_token apiVK: ")
    user_id = input("Введите id пользователя VK: ")
    token_yd = input("Введите токен с полигона Яндекс.Диска: ")
    log.logging.info("Init example VK ")
    vk = classVK.VK(token_vk, user_id)
    log.logging.info("Get images ")
    photos_info = vk.get_profile_photos()
    log.logging.info("Sorting images ")
    list_photos_info = sort_json_photos(photos_info)
    log.logging.info("Upload to json file ")
    load_data_json(list_photos_info)
    log.logging.info("Init example YandexDisk ")
    yd = classYanDisk.YandexDisk(token_yd)
    yd.create_folder()
    yd.parse_photos(list_photos_info)




