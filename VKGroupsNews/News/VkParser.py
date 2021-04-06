from datetime import datetime
from .models import Article
import vk_api
import json


def convert_time(date):
    return datetime.utcfromtimestamp(int(date)).strftime('%Y-%m-%d %H:%M:%S')


def get_info(owner_id=None, login=None, password=None, hook=None):
    if hook:
        if hook["type"] == "wall_post_new":
            wall_post = hook['object']
            if "attachments" in wall_post:
                if "text" in wall_post:
                    post_text = wall_post['text']
                    if 'photo' in wall_post['attachments']:
                        post_picture = wall_post.get("attachments")[0].get("photo").get("sizes")[3].get("url")
                    else:
                        image_url = None
                    date = convert_time(wall_post["date"])
                    owner_id = wall_post['owner_id']
                    wall_id = wall_post['id']
                    urls = "http://vk.com/wall" + str(owner_id) + "_" + str(wall_id)
                    db_record = Article(date_published=date, image=image_url, local_post_link=wall_id, post_link=urls,
                                        text=post_text)
                    db_record.save()
                else:
                    if 'photo' in wall_post['attachments']:
                        post_picture = wall_post.get("attachments")[0].get("photo").get("sizes")[3].get("url")
                    else:
                        image_url = None
                    date = convert_time(wall_post["date"])
                    owner_id = wall_post['owner_id']
                    wall_id = wall_post['id']
                    urls = "http://vk.com/wall" + str(owner_id) + "_" + str(wall_id)
                    db_record = Article(date_published=date, image=image_url, local_post_link=wall_id, post_link=urls,
                                        text=None)
                    db_record.save()
            else:
                if "text" in wall_post:
                    post_text = wall_post['text']
                    date = convert_time(wall_post["date"])
                    owner_id = wall_post ['owner_id']
                    wall_id = wall_post['id']
                    urls = "http://vk.com/wall" + str(owner_id) + "_" + str(wall_id)
                    db_record = Article(date_published=date, image=None, local_post_link=wall_id, post_link=urls,
                                        text=post_text)
                    db_record.save()
                else:
                    date = convert_time(wall_post["date"])
                    owner_id = wall_post ['owner_id']
                    wall_id = wall_post['id']
                    urls = "http://vk.com/wall" + str(owner_id) + "_" + str(wall_id)
                    db_record = Article(date_published=date, image=None, local_post_link=wall_id, post_link=urls,
                                        text=None)
                    db_record.save()
        return
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
                else:
                    image_url = None
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
                else:
                    image_url = None
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
