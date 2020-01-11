from facebook_scraper import get_posts

# pseudo config
fanpages = [
    'convolutionalmemes',
    'artificialintelligencememes',
    'DeepLearningNewsAndMemes',
]
pages_to_search = 30

i = 0
for post in get_posts('DeepLearningNewsAndMemes', pages=pages_to_search):  # todo get_posts
    post_url = post['post_url']
    post_id = post['post_id']
    post_text = post['post_text']
    image_url = post['image']


    print()
    print(i, post)
    i+=1
    print()
