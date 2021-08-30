from django.conf import settings
import requests


def get_discourse_index_data():
    try:
        categories_url = settings.DISCOURSE_UPSTREAM + '/categories.json'
        categories = requests.get(categories_url).json()
        categories = categories['category_list']['categories']

        latest_url = settings.DISCOURSE_UPSTREAM + '/latest.json'
        latest = requests.get(latest_url).json()
        latest = latest['topic_list']['topics']

        topics = []
        for topic in latest[:10]:
            topic_category = None

            for category in categories:
                subcategories = category.get('subcategory_ids', [])
                if category['id'] == topic['category_id']:
                    topic_category = category
                elif topic['category_id'] in subcategories:
                    topic_category = category

            topic['category_name'] = topic_category['name']
            topic['category_slug'] = topic_category['slug']

            topics.append(topic)
    except:
        topics = 500 # Server Error

    return topics
