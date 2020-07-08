from django.core.management.base import BaseCommand, CommandError
from backend.settings import DATA_DIR, MEDIA_ROOT
from store.models import Category, Product
from bs4 import BeautifulSoup

from .functions import load_data, contain_books_data
import requests
import os


class Command(BaseCommand):

    def handle(self, output_file=None, *args, **options):
        html_dir = os.path.join(DATA_DIR, 'parsed.html')
        book_html = os.path.join(DATA_DIR, 'book.html')
        book_2_html = os.path.join(DATA_DIR, 'book2.html')

        url = 'https://aldebaran.ru/genre/'

        headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,'
                      'application/signed-exchange;v=b3;q=0.9',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'uk-UA,uk;q=0.9,ru-UA;q=0.8,ru;q=0.7,en-US;q=0.6,en;q=0.5',
            'Cache-Control': 'max-age=0',
            'Connection': 'keep-alive',
            'Cookie': 'SID=5nakfm3x01c73m5s0idw6c4251f4550z; _ga=GA1.2.695853376.1594033752; '
                      '_gid=GA1.2.1533500083.1594033752; __utmc=267605726; '
                      '__utmz=267605726.1594043950.2.2.utmcsr=google|utmccn=(organic)|utmcmd=organic|utmctr=('
                      'not%20provided); __utma=267605726.695853376.1594033752.1594043950.1594064213.3; '
                      '__utmb=267605726.5.9.1594066559026',
            'DNT': '1',
            'Host': 'aldebaran.ru',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'none',
            'Sec-Fetch-User': '?1',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/83.0.4103.116 Safari/537.36'}

        print('Clearing DB')
        Category.objects.all().delete()
        Product.objects.all().delete()

        print('Start importing')

        r = requests.get(url, headers=headers)

        # parsing site to file
        with open(html_dir, 'w', encoding='utf8') as output_file:
            output_file.write(r.text)

        # reading file
        with open(html_dir, 'r', encoding='utf8') as source_file:
            soup = BeautifulSoup(source_file, 'html.parser')

        # searching categories
        res = soup.find('div', {'class': 'all_genres'}).find_all('a')

        # creating dictionary {category: link}
        c = {}
        for item in res:
            c[item.text] = item.get('href')

        # loading books pages by category to file
        for value in c.items():
            book_category = value[0]
            link = value[1]
            book = os.path.join(DATA_DIR, str(book_category) + '.html')

            print('Create a new category')
            cat = Category()
            cat.name = book_category
            cat.save()

            page = 1
            while page <= 2:
                data = load_data(link, page, headers)
                if contain_books_data(data):
                    with open(book, 'a', encoding='utf8') as output_file:
                        output_file.write(data)
                        page += 1
                else:
                    break

            with open(book, 'r', encoding='utf8') as source_file:
                soup = BeautifulSoup(source_file, 'html.parser')
            res = soup.find_all('div', {'class': 'wrap'})

            with open(book, 'w', encoding='utf8') as output_file:
                output_file.write(str(res))

            with open(book, 'r', encoding='utf8') as source_file:
                soup = BeautifulSoup(source_file, 'html.parser')

            res = soup.find_all('img')
            for item in res:
                img_url = 'http:' + item.get('src')
                req = requests.get(img_url)
                symbol = ['?', '/', '>', '<', '*', '|', '\\', '"']
                img_name = item.get('alt') + '.jpg'
                for s in symbol:
                    img_name = img_name.replace(s, '')
                img_path = os.path.join(MEDIA_ROOT, img_name)

                out = open(img_path, "wb")
                out.write(req.content)
                out.close()

                p = Product()
                p.name = item.get('alt')
                p.category = cat
                p.image.name = img_name
                p.save()
                print(p.image.path)
            os.remove(book)
        # reading file
        # with open(book_html, 'r', encoding='utf8') as source_file:
        #     soup = BeautifulSoup(source_file, 'html.parser')
        #
        # res = soup.find_all('div', {'class': 'wrap'})
        #
        # # rewriting file
        # with open(book_2_html, 'w', encoding='utf8') as output_file:
        #     output_file.write(str(res))
        #
        # # reading file
        # with open(book_2_html, 'r', encoding='utf8') as source_file:
        #     soup = BeautifulSoup(source_file, 'html.parser')
        #
        # res = soup.find_all('img')
        #
        # books = {'name': [], 'img': []}
        #
        # for item in res:
        #     books['name'].append(item.get('alt'))
        #     books['img'].append(item.get('src'))



