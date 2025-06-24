import time
import re
import os
from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

folder_name = "leetcode"
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
driver.get("https://cses.fi/problemset/")

time.sleep(5)
html = driver.page_source
soup = BeautifulSoup(html, 'html.parser')
# print(soup)
all_ques_div = soup.find_all("li", class_="task")
titles = [li.contents[0].get_text(strip=True) for li in all_ques_div]
urls = ["https://cses.fi"+li.contents[0]['href'] for li in all_ques_div]
# print(titles)
# print(urls)
acceptance_text = [li.contents[1].get_text(strip=True) for li in all_ques_div]
acceptance = [f"{(int(item.split(' / ')[0].strip()) / int(item.split(' / ')[1].strip())) * 100:.2f}%" for item in acceptance_text]
difficulty = [
    "Easy" if float(p.replace('%', '')) > 80
    else "Medium" if 60 <= float(p.replace('%', '')) <= 80
    else "Hard"
    for p in acceptance
]
# print(acceptance)
# print(difficulty)

problems_description = []

i = 0
while i < len(urls):
    url = urls[i]
    driver.get(url)
    time.sleep(4)
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    problem_statement_div = soup.find('div', class_='md')
    problem_full_text = problem_statement_div.get_text(strip=True)
    problems_description.append(problem_full_text)
    i=i+1



file_name = "problems_url.txt"
folder_path = os.path.join(os.getcwd(), folder_name)
file_path = os.path.join(folder_path, file_name)

with open(file_path,"a") as f:
    f.write("\n")
    f.write("\n".join(urls))
file_name="problems_title.txt"
file_path = os.path.join(folder_path, file_name)
with open(file_path,"a") as f:
    f.write("\n")
    f.write("\n".join(titles))

file_name="acceptance.txt"
file_path = os.path.join(folder_path, file_name)
with open(file_path,"a") as f:
    f.write("\n")
    f.write("\n".join(acceptance))

file_name="difficulty_data.txt"
file_path = os.path.join(folder_path, file_name)
with open(file_path,"a") as f:
    f.write("\n")
    f.write("\n".join(difficulty))

folder_name="leetcode"
main_folder_path = os.path.join(os.getcwd(), folder_name)
folder_name="problems_desc"
folder_path = os.path.join(main_folder_path, folder_name)
cnt=678
for description in problems_description:
    cnt += 1
    file_name="problem"+str(cnt)+".txt"
    file_path = os.path.join(folder_path, file_name)
    with open(file_path,"w+",encoding="utf-8") as f:
        f.write(description)