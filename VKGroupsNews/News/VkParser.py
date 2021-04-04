from datetime import datetime
from .models import Article
import vk_api
import json


def convert_time(date):
    return datetime.utcfromtimestamp(int(date)).strftime('%Y-%m-%d %H:%M:%S')


def get_info(owner_id, login=None, password=None):
    if login and password:
        try:
            vk_session = vk_api.VkApi(login, password)
            vk_session.auth()
            vk = vk_session.get_api()
        except vk_api.exceptions.BadPassword:
            error = "Неверный пароль, попробуйте сначала"
            return error
    else:
        return None
    posts = vk.wall.get(owner_id=owner_id, count=50)
    json.dumps(posts, sort_keys=True, ensure_ascii=False)
    posts_data = posts.get("items")
    for i in posts_data:
        if "attachments" in i:
            if i.get("text") == "":
                date = convert_time(i.get("date"))
                wall_id = i.get("id")
                owner_id = i.get("owner_id")
                if "photo" in i.get("attachments")[0]:
                    image_url = i.get("attachments")[0].get("photo").get("sizes")[3].get("url")
                urls = "http://vk.com/wall" + str(owner_id) + "_" + str(wall_id)
                db_record = Article(date_published=date, image=image_url, local_post_link=wall_id, post_link=urls,
                                    text=None)
                db_record.save()
            else:
                text = i.get("text")
                date = convert_time(i.get("date"))
                wall_id = i.get("id")
                if "photo" in i.get("attachments")[0]:
                    image_url = i.get("attachments")[0].get("photo").get("sizes")[3].get("url")
                urls = "http://vk.com/wall" + str(owner_id) + "_" + str(wall_id)
                db_record = Article(text=text, date_published=date, image=image_url, local_post_link=wall_id,
                                    post_link=urls)
                db_record.save()
        else:
            if i.get("text") == "":
                date = convert_time(i.get("date"))
                wall_id = i.get("id")
                owner_id = i.get("owner_id")
                urls = "http://vk.com/wall" + str(owner_id) + "_" + str(wall_id)
                db_record = Article(date_published=date, local_post_link=wall_id, post_link=urls, text=None, image=None)
                db_record.save()
            else:
                text = i.get("text")
                date = convert_time(i.get("date"))
                owner_id = i.get("owner_id")
                wall_id = i.get("id")
                urls = "http://vk.com/wall" + str(owner_id) + "_" + str(wall_id)
                db_record = Article(text=text, date_published=date, local_post_link=wall_id, post_link=urls, image=None)
                db_record.save()
    return 1
