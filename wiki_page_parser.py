import requests
from bs4 import BeautifulSoup

url = "https://en.wikipedia.org/wiki/List_of_the_most_common_passwords"

response = requests.get(url)
response.raise_for_status()

soup = BeautifulSoup(response.content, "html.parser")

tables = soup.find_all('table', {'class': 'wikitable'})
target_caption = "Top 25 most common passwords by year according to SplashData"
target_table = None

for table in tables:
    caption = table.find('caption')
    if caption and caption.get_text(strip=True) == target_caption:
        target_table = table
        break

passwords = []

if target_table:
    for row in target_table.find_all('tr')[1:]:
        cells = row.find_all('td')
        for cell in cells[1:]:
            password = cell.get_text(strip=True)
            if password and not password.isdigit():
                passwords.append(password)

passwords_tuple = tuple(passwords)