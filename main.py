import vk_api
from vk_api.upload import VkUpload
from vk_api.utils import get_random_id
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.keyboard import VkKeyboard, VkKeyboardColor

from random import randint

token = "ec882d06850e9776ab2c7d580be2d5216d304b9aa2321bd2f36a5cb2d3d619090611918746fffe481f96c"
vk_session = vk_api.VkApi(token=token)


def send_message(id, text):
    post = {
        "user_id": id,
        "message": text,
        "random_id": get_random_id()
    }

    vk_session.method("messages.send", post)


def send_keyboard(id, text):
    keyboard = VkKeyboard(one_time=True)
    keyboard.add_button("1", color=VkKeyboardColor.POSITIVE)
    keyboard.add_button("2", color=VkKeyboardColor.PRIMARY)
    keyboard.add_button("3", color=VkKeyboardColor.NEGATIVE)
    keyboard.add_line()
    keyboard.add_button("4", color=VkKeyboardColor.SECONDARY)
    keyboard.add_button("5", color=VkKeyboardColor.POSITIVE)

    post = {
        "user_id": id,
        "message": text,
        "random_id": get_random_id(),
        "keyboard": keyboard.get_keyboard()
    }

    vk_session.method("messages.send", post)


def send_image(id, text, images):
    post = {
        "user_id": id,
        "message": text,
        "random_id": get_random_id(),
        "attachment": ",".join(images)
    }
    vk_session.method("messages.send", post)


def random_image(upload, image_id):
    img = './images/%d.jpg' % image_id
    upload_image = upload.photo_messages(photos=img)[0]
    return 'photo{}_{}'.format(upload_image['owner_id'], upload_image['id'])


def start(id, upload):
    images_titles = {}
    images = []

    for el in open('words.txt', 'r', encoding='utf-8'):
        images_titles[el.split(':')[0]] = el.split(':')[1].split()

    set_id = []
    titles_images = {}
    for i in range(5):
        image_id = randint(1, 98)
        pr = True
        while pr:
            pr = False
            for el in set_id:
                if el == image_id:
                    pr = True
                    image_id = randint(1, 98)
                    break
        set_id.append(image_id)
        images.append(random_image(upload, image_id))

        for title in images_titles['%d.jpg' % image_id]:
            if titles_images.get(title):
                titles_images[title].append('%d.jpg' % image_id)
            else:
                titles_images[title] = ['%d.jpg' % image_id]

    set_unique_titles = []
    for key in titles_images.keys():
        if len(titles_images[key]) == 1:
            set_unique_titles.append(key)

    send_image(id, "Привет! Вот 5 изображений", images)
    
    send_keyboard(id, 'Какое из них больше подходит под описание: "' +
                  set_unique_titles[randint(0, len(set_unique_titles) - 1)] + '"?')


def main():
    session_api = vk_session.get_api()
    longpoll = VkLongPoll(vk_session)
    upload = VkUpload(session_api)

    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW:
            if event.message == "Старт":
                id = event.user_id
                start(id, upload)


if __name__ == '__main__':
    main()
