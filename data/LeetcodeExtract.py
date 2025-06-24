import time
import re
import os
from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

folder_name = "leetcode"
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
driver.get("https://leetcode.com/problem-list/bit-manipulation/")
time.sleep(5)
html = driver.page_source
soup = BeautifulSoup(html, 'html.parser')
# print(soup)
all_ques_div=soup.find_all('div', {"class":"ellipsis"})
all_ques = [div.get_text(strip=True) for div in all_ques_div]
titles = [re.sub(r'^\d+\.\s*', '', q) for q in all_ques]
urls_atag=[]
for div in all_ques_div:
    parent = div
    for _ in range(5):
        if parent:
            parent = parent.parent
        else:
            break
    urls_atag.append(parent)

urls = ["https://leetcode.com"+tag.get('href') for tag in urls_atag if tag and tag.name == 'a']

acceptance = []
difficulty = []

for ellipsis_div in all_ques_div:
    parent_of_ellipsis = ellipsis_div.parent

    current_acceptance_text = None
    current_difficulty_text = None

    if parent_of_ellipsis:
        grandparent_of_ellipsis = parent_of_ellipsis.parent

        if grandparent_of_ellipsis:
            next_element_to_grandparent = grandparent_of_ellipsis.find_next_sibling()
            if next_element_to_grandparent:
                current_acceptance_text = next_element_to_grandparent.get_text(strip=True)

            first_next_sibling = grandparent_of_ellipsis.find_next_sibling()
            if first_next_sibling:
                second_next_sibling = first_next_sibling.find_next_sibling()
                if second_next_sibling:
                    current_difficulty_text = second_next_sibling.get_text(strip=True)

    acceptance.append(current_acceptance_text)
    difficulty.append(current_difficulty_text)


problems_description = []
cnt = 0
deleted_urls_count = 0

i = 0
while i < len(urls):
    url = urls[i]
    driver.get(url)
    time.sleep(5)
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')

    # Find the div with class "elfjS"
    problem_div = soup.find('div', {"class": "elfjS"})

    if problem_div:
        problem_text = problem_div.get_text(strip=True)
        problems_description.append(problem_text)
        i += 1
    else:
        urls.pop(i)
        acceptance.pop(i)
        difficulty.pop(i)
        titles.pop(i)
        deleted_urls_count += 1


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
cnt=587
for description in problems_description:
    cnt += 1
    file_name="problem"+str(cnt)+".txt"
    file_path = os.path.join(folder_path, file_name)
    with open(file_path,"w+",encoding="utf-8") as f:
        f.write(description)