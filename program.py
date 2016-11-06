import requests
import bs4


def main():
    html = get_html()
    laptops = parse_html(html)
    for laptop in laptops:
        for detail in laptop:
            print(detail)
        print()
    send_email()


def get_html():
    #url = 'http://www.apple.com/shop/browse/home/specialdeals/mac/macbook_pro/15'
    url = 'http://www.apple.com/shop/browse/home/specialdeals/mac/macbook_air/11'
    response = requests.get(url)
    return response.text


def parse_html(html):
    laptops = []
    # cityCss = 'div#location h1'
    # weatherConditionCss = 'div#curCond span.wx-value'
    # weatherTempCss = 'div#curTemp span.wx-data span.wx-value'
    # weatherScaleCss = 'div#curTemp span.wx-data span.wx-unit'

    """
    soup = bs4.BeautifulSoup(html, 'html.parser')
    location = soup.find(id='location').find('h1').get_text()
    condition = soup.find(id='curCond').find(class_='wx-value').get_text()
    temp = soup.find(id='curTemp').find(class_='wx-value').get_text()
    scale = soup.find(id='curTemp').find(class_='wx-unit').get_text()
    """

    soup = bs4.BeautifulSoup(html, 'html.parser')
    spec_rows = soup.find(id='primary').find_all(class_='specs')
    price_rows = soup.find(id='primary').find_all(class_='current_price')
    for spec, price in zip(spec_rows, price_rows):
        cleaned_spec = clean_text(spec.get_text())
        cleaned_spec.append(clean_text(price.get_text())[0])  # Add price to device specs
        laptops.append(cleaned_spec)

    return laptops


def clean_text(s):
    cleaned_list = []

    s = s.split('\n')
    for k in s:
        k = k.strip()
        if k:
            cleaned_list.append(k)
    return cleaned_list


def send_email():
    pass


if __name__ == '__main__':
    main()
