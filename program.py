#! /home/janderson/PycharmProjects/refurbquery/env/bin/python
# 0 6-22 * * * /home/janderson/PycharmProjects/refurbquery/env/bin/python /home/janderson/PycharmProjects/refurbquery/program.py

import requests
import bs4
import send_email
import collections

MacBook = collections.namedtuple('MacBook',
                                 'title, released, screen, memory, storage, camera, graphics, cost, discount, percent')


def main():
    email_body = ''

    urls = {
        'macpro_13': 'http://www.apple.com/shop/browse/home/specialdeals/mac/macbook_pro/13',
        'macpro_15': 'http://www.apple.com/shop/browse/home/specialdeals/mac/macbook_pro/15',
        'macair_11': 'http://www.apple.com/shop/browse/home/specialdeals/mac/macbook_air/11'
    }

    all_laptops = []

    for key, url in urls.items():
        html = get_html(url)
        laptop_model = parse_html(html)
        all_laptops.append(laptop_model)

    for laptop in all_laptops:
        if laptop:
            for spec in laptop:
                email_body += '\n'.join(spec)  # join the tuple adding a new line between the values
                email_body += '\n\n'

    # send an email
    send_email.create_send_email(email_body)


def get_html(url):
    response = requests.get(url)
    return response.text


def parse_html(html):
    laptops = []

    soup = bs4.BeautifulSoup(html, 'html.parser')
    spec_rows = soup.find(id='primary').find_all(class_='specs')
    price_rows = soup.find(id='primary').find_all(class_='current_price')
    savings_rows = soup.find(id='primary').find_all(class_='savings')

    for spec, price, saving in zip(spec_rows, price_rows, savings_rows):
        title, released, screen, memory, storage, camera, graphics = clean_text(spec.get_text())
        cost, = clean_text(price.get_text())  # cost has trailing comma so it unpacks the first value only
        discount, percent = clean_text(saving.get_text())
        laptop = MacBook(title=title, released=released, screen=screen, memory=memory, storage=storage, camera=camera,
                         graphics=graphics, cost=cost, discount=discount, percent=percent)
        laptops.append(laptop)

    return laptops


def clean_text(s):
    cleaned_list = []

    s = s.split('\n')
    for k in s:
        k = k.strip()
        if k:
            cleaned_list.append(k)
    return cleaned_list


if __name__ == '__main__':
    main()
