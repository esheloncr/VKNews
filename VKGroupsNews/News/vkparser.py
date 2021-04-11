from datetime import datetime
from .models import Article
import vk_api
import json

data = {"login": "", "password": "", "group_id": "-"}


def convert_time(date):
    return datetime.utcfromtimestamp(int(date)).strftime('%Y-%m-%d %H:%M:%S')


def parse_posts():
    vk_session = vk_api.VkApi(data['login'], data['password'])
    vk_session.auth()
    vk = vk_session.get_api()
    posts = vk.wall.get(owner_id=data['group_id'], count=50)
    json.dumps(posts, sort_keys=True, ensure_ascii=False)
    posts_data = posts.get("items")
    print(posts_data[0])
    for post in posts_data:
        if "attachments" in post:
            if "text" in post:
                post_text = post['text']
                if 'photo' in post['attachments'][0]:
                    image_url = post.get('attachments')[0].get("photo").get("sizes")[0].get("url")
                else:
                    image_url = None
                date = convert_time(post["date"])
                owner_id = post['owner_id']
                wall_id = post['id']
                urls = "http://vk.com/wall" + str(owner_id) + "_" + str(wall_id)
                db_record = Article(date_published=date, image=image_url, local_post_link=wall_id, post_link=urls,
                                    text=post_text)
                db_record.save()
            else:
                if 'photo' in post['attachments']:
                    image_url = post.get('attachments')[0].get("photo").get("sizes")[0].get("url")
                else:
                    image_url = None
                date = convert_time(post["date"])
                owner_id = post['owner_id']
                wall_id = post['id']
                urls = "http://vk.com/wall" + str(owner_id) + "_" + str(wall_id)
                db_record = Article(date_published=date, image=image_url, local_post_link=wall_id, post_link=urls,
                                    text=None)
                db_record.save()
        else:
            if "text" in post:
                post_text = post['text']
                date = convert_time(post["date"])
                owner_id = post['owner_id']
                wall_id = post['id']
                urls = "http://vk.com/wall" + str(owner_id) + "_" + str(wall_id)
                db_record = Article(date_published=date, image=None, local_post_link=wall_id, post_link=urls,
                                    text=post_text)
                db_record.save()
            else:
                date = convert_time(post["date"])
                owner_id = post['owner_id']
                wall_id = post['id']
                urls = "http://vk.com/wall" + str(owner_id) + "_" + str(wall_id)
                db_record = Article(date_published=date, image=None, local_post_link=wall_id, post_link=urls,
                                    text=None)
                db_record.save()
    return


def get_post_by_hook(hook):
    if not hook:
        return
    if hook["type"] == "wall_post_new":
        wall_post = hook['object']
        if "attachments" in wall_post:
            if "text" in wall_post:
                post_text = wall_post['text']
                if 'photo' in wall_post['attachments'][0]:
                    image_url = wall_post.get('attachments')[0].get("photo").get("photo_130")
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
                    image_url = wall_post.get('attachments')[0].get("photo").get("photo_130")
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
