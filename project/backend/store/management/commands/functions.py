from bs4 import BeautifulSoup
import requests

def load_data(book_category_link, page, headers):
    url = 'https://aldebaran.ru%spagenum-%d/' % (book_category_link, page)
    request = requests.get(url, headers=headers)
    return request.text


def contain_books_data(text):
    soup = BeautifulSoup(text, 'html.parser')
    book_list = soup.findAll('div', {'class': 'info-wr'})
    return book_list is not None


