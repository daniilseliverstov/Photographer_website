import os
from datetime import datetime

from django.shortcuts import render
from .models import Gallery, PhotoMainPage
from django.conf import settings
import requests
import json
from django.core.paginator import Paginator


def get_reviews():
    access_token = '7335a4057335a4057335a405eb7011978f773357335a405140c7e4da65713e480ff0133'
    group_id = '-68207147'

    posts_url = f'https://api.vk.com/method/wall.get?owner_id={group_id}&count=5&access_token={access_token}&v=5.131'
    response = requests.get(posts_url)
    posts_data = response.json()

    reviews = []

    if 'response' in posts_data:
        posts = posts_data['response']['items'][:5]
        for post in posts:
            post_id = post['id']

            comments_url = (f'https://api.vk.com/method/wall.getComments?owner_id={group_id}&post_id={post_id}'
                            f'&count=10&sort=asc&access_token={access_token}&v=5.131')
            comment_response = requests.get(comments_url)
            comment_data = comment_response.json()

            if 'response' in comment_data:
                post_comments = comment_data['response']['items']

                for comment in post_comments:
                    if not comment['text'].strip():  # Проверка на пустой комментарий
                        continue  # Пропустить пустые комментарии

                    author_info = comment['from_id']
                    date = datetime.fromtimestamp(comment['date']).strftime('%Y-%m-%d %H:%M:%S')  # Форматирование даты

                    user_info_url = (f'https://api.vk.com/method/users.get?user_ids={author_info}'
                                     f'&fields=name&access_token={access_token}&v=5.131')
                    user_response = requests.get(user_info_url)
                    user_data = user_response.json()

                    if 'response' in user_data:
                        author_name = user_data['response'][0]['first_name'] + ' ' + user_data['response'][0][
                            'last_name']
                    else:
                        author_name = 'Автор не найден'

                    comment_info = {
                        'text': comment['text'],
                        'author': author_name,
                        'date': date
                    }
                    reviews.append(comment_info)
            else:
                print(f"Ошибка при получении комментариев к посту {post_id}:", comment_data.get('error'))
    else:
        print("Ошибка при получении постов:", posts_data.get('error'))

    return reviews


def home(request):
    photos_main_page = PhotoMainPage.objects.all()
    photos_per_page = int(request.GET.get('photos_per_page', 8))
    page_number = request.GET.get('page', 1)
    paginator = Paginator(photos_main_page, photos_per_page)
    page_obj = paginator.get_page(page_number)
    reviews = get_reviews()
    context = {
        'photos_main_page': page_obj,
        'reviews': reviews,
        'paginator': paginator,
    }
    return render(request, 'home.html', context)


def portfolio(request):
    galleries = Gallery.objects.all()
    images = {}

    for gallery in galleries:
        gallery_path = os.path.join(settings.BASE_DIR, 'main_app', 'static', 'main_app', 'images', gallery.title)

        if os.path.exists(gallery_path):
            images[gallery.title] = {
                'images': [os.path.join('main_app', 'images', gallery.title, img) for img in os.listdir(gallery_path)],
                'title': gallery.title,
                'description': gallery.description,
            }
        else:
            print(f"Путь к галерее не существует: {gallery_path}")  # Для отладки

    return render(request, 'portfolio.html', {'galleries': galleries, 'images': images})


def contact(request):
    return render(request, 'contact.html')
