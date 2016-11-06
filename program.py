import requests
import bs4
import send_email


def main():

    laptop_dict = {}
    email_body = ''

    urls = {
        'macpro_13': 'http://www.apple.com/shop/browse/home/specialdeals/mac/macbook_pro/13',
        'macpro_15': 'http://www.apple.com/shop/browse/home/specialdeals/mac/macbook_pro/15',
    }

    for key, url in urls.items():
        html = get_html(url)
        laptop_model = parse_html(html)
        laptop_dict[key] = laptop_dict.get(key, laptop_model)

    for model, device in laptop_dict.items():
        email_body = email_body + model + ':\n'
        for item in laptop_dict[model]:
            for spec in item:
                email_body = email_body + spec + '\n'
            email_body += '\n'

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
        cleaned_spec = clean_text(spec.get_text())
        cleaned_spec.append(clean_text(price.get_text())[0])  # Append price to device specs
        cleaned_spec.append(clean_text(saving.get_text())[0])  # Append dollars saved to specs
        cleaned_spec.append(clean_text(saving.get_text())[1])  # Append percentage saved to device specs
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


if __name__ == '__main__':
    main()
