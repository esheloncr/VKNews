from datetime import datetime
from .models import Article
import vk_api
import json

vk_session = vk_api.VkApi('89991380403', 'Ezb4hxd6u7F!')
vk_session.auth()
vk = vk_session.get_api()


def convert_time(date):
    return datetime.utcfromtimestamp(int(date)).strftime('%Y-%m-%d %H:%M:%S')

asdasd = -201788787


def get_info(owner_id,counter):
    #test mode
    if counter == 1:
        posts = vk.wall.get(owner_id=owner_id)
        json.dumps(posts, sort_keys=True, ensure_ascii=False)
        posts_data = posts.get("items")
        for i in posts_data:
            if "attachments" in i:
                if i.get("text") == "":
                    date = convert_time(i.get("date"))
                    wall_id = i.get("id")
                    owner_id = i.get("owner_id")
                    image_url = i.get("attachments")[0].get("photo").get("sizes")[4].get("url")
                    urls = "http://vk.com/wall" + str(owner_id) + "_" + str(wall_id)
                    db_record = Article(date_published=date, image=image_url, local_post_link=wall_id, post_link=urls)
                else:
                    text = i.get("text")
                    date = convert_time(i.get("date"))
                    wall_id = i.get("id")
                    owner_id = i.get("owner_id")
                    image_url = i.get("attachments")[0].get("photo").get("sizes")[4].get("url")
                    urls = "http://vk.com/wall" + str(owner_id) + "_" + str(wall_id)
                    db_record = Article(text=text,date_published=date, image=image_url, local_post_link=wall_id, post_link=urls)
            else:
                if i.get("text") == "":
                    date = convert_time(i.get("date"))
                    wall_id = i.get("id")
                    owner_id = i.get("owner_id")
                    urls = "http://vk.com/wall" + str(owner_id) + "_" + str(wall_id)
                    db_record = Article(date_published=date, local_post_link=wall_id, post_link=urls)
                else:
                    text = i.get("text")
                    date = convert_time(i.get("date"))
                    owner_id = i.get("owner_id")
                    wall_id = i.get("id")
                    urls = "http://vk.com/wall" + str(owner_id) + "_" + str(wall_id)
                    db_record = Article(text=text,date_published=date, local_post_link=wall_id, post_link=urls)
            return
        else:
            return