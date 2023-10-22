import requests
from bs4 import BeautifulSoup
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import yaml
import os

def read_yaml(yaml_path):
    print(os.path.exists(yaml_path))
    with open(yaml_path, 'r',encoding='utf-8') as f:
        yaml_content = yaml.safe_load(f)
    return yaml_content

config_path = "configs/config.yaml"
configs = read_yaml(config_path)

MY_EMAIL = configs["MY_EMAIL]"
PASSWORD = configs["PASSWORD]"
SENDING_MAIL = configs["SENDING_MAIL]"

#get HTML page in bs4 for extraction
URL = "https://www.amazon.nl/K3-Mechanisch-Toetsenbord-Ultra-Compact-TPU-veerkabel/dp/B0B9M6477S/ref=sr_1_17?crid=XNMJVDZUE4B9&keywords=toetsenbord&qid=1697904930&refinements=p_n_free_shipping_eligible%3A17033278031%2Cp_72%3A4993218031%2Cp_36%3A20314670031&rnid=16332312031&s=videogames&sprefix=toetsenbor%2Cvideogames%2C69&sr=1-17&th=1"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7"
    }

response = requests.get(url=URL, headers=headers)
response.raise_for_status()
amazon_webpage = response.text

soup = BeautifulSoup(amazon_webpage, 'html.parser')

category = soup.find_all(name= "a",class_="a-link-normal a-color-tertiary")
last_item= category[-1].text.strip()
print(last_item)

keyboard = soup.find(name="span", id="productTitle", class_="a-size-large product-title-word-break")
keyboard = keyboard.text.strip()

price = soup.find(name="span", class_="a-offscreen")
print(price.text)
price = int(price.text[1:3])

if price < 70:
    message = MIMEMultipart()
    message["From"] = MY_EMAIL
    message["To"] = SENDING_MAIL
    message["subject"] = f'Amazon price alert for item: {last_item}'

    email_body = f'you were looking for {keyboard} on Amazon.com.\n' \
                  f'The price of this product is now below EUR {price},-\n' \
                  f'go to the following URL to buy this product: {URL}'
    body = MIMEText(email_body, "plain")
    message.attach(body)

    with smtplib.SMTP("smtp.gmail.com") as connection:
        connection.starttls()
        connection.login(user=MY_EMAIL, password=PASSWORD)
        connection.sendmail(from_addr=MY_EMAIL, to_addrs=SENDING_MAIL, msg=message.as_string())