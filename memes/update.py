import os

import django
from facebook_scraper import get_posts

from manage import DEFAULT_SETTINGS_MODULE

os.environ.setdefault("DJANGO_SETTINGS_MODULE", DEFAULT_SETTINGS_MODULE)
django.setup()
# pseudo config
from memes.models import Meme

fanpages = [
    'convolutionalmemes',
    'artificialintelligencememes',
    'DeepLearningNewsAndMemes',
]
pages_to_search = 2

i = 0  # todo
memes = Meme.objects.all()
print('curr memes', len(memes))
for fanpage in fanpages:
    for post in get_posts(fanpage, pages=pages_to_search):  # todo get_posts
        post_url = post['post_url']
        post_id = post['post_id']
        image_url = post['image']

        if post_url and post_id and image_url:
            if not memes.filter(post_id=post_id).exists():
                new_meme = Meme(
                    post_id=post_id,
                    post_url=post_url,
                    image_url=image_url,
                    views=0,
                    valid=True
                )
                new_meme.save()

        print()
        print(i, post)
        i+=1
        print()
