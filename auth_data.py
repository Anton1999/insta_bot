from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from us_data import  username, password
import time
import requests
from selenium.common.exceptions import NoSuchElementException
import os
import random

class InstagramBot():
    def __init__(self, USERNAME, PASSWORD):
        self.username = USERNAME
        self.password = PASSWORD
        self.browser = webdriver.Chrome(executable_path="chromedriver/chromedriver.exe")

    def close_browser(self):
        self.browser.close()
        self.browser.quit()

    def login(self):
        browser = self.browser
        browser.get('https://www.instagram.com')
        time.sleep(random.randrange(3, 5))

        username_input = browser.find_element_by_name('username')
        username_input.clear()
        username_input.send_keys(username)

        time.sleep(2)

        password_input = browser.find_element_by_name('password')
        password_input.clear()
        password_input.send_keys(password)

        password_input.send_keys(Keys.ENTER)

        time.sleep(10)

    def like_photo_by_hashtag(self, hashtag):
        browser = self.browser
        browser.get(f'https://www.instagram.com/explore/tags/{hashtag}/')
        time.sleep(5)

        for i in range(1, 4):
            browser.execute_script('window.scrollTo(0, document.body.scrollHeight);')
            time.sleep((random.randrange(3, 5)))

        hrefs = browser.find_elements_by_tag_name('a')

        posts_urls = []

        for item in hrefs:
            href = item.get_attribute('href')

            if '/p/' in href:
                posts_urls.append(href)
                print(posts_urls)

        for url in posts_urls[0:1]:
            try:
                browser.get(url)

                like_button = browser.find_element_by_class_name('fr66n').click()
                time.sleep(10)

                browser.close()
                browser.quit()

            except Exception as ex:
                print(ex)
                self.close_browser()

    def xpath_exists(self, url):

        browser = self.browser
        try:
            browser.find_element_by_xpath(url)
            exist = True
        except NoSuchElementException:
            exist = False
        return exist

    def put_exactly_like(self, userpost):
        browser = self.browser

        browser.get(userpost)
        time.sleep(4)

        wrong_userpage = '/html/body/div[1]/section/main/div/h2'

        if self.xpath_exist(wrong_userpage):
            print('Вы ошиблись, такого поста не существует')
            self.close_browser()
        else:
            print('Пост найден - лайк')
            time.sleep(2)
            like_button = 'fr66n'
            browser.find_element_by_class_name(like_button).click()

    def put_many_likes(self, userpage):
        browser = self.browser
        browser.get(userpage)
        time.sleep(2)

        wrong_userpage = '/html/body/div[1]/section/main/div/h2'

        if self.xpath_exist(wrong_userpage):
            print('Вы ошиблись, такого поользователя не существует')
            self.close_browser()
        else:
            print('Пользователь найден - лайк')
            time.sleep(2)

            posts_count = int(browser.find_element_by_xpath("/html/body/div[1]/section/main/div/header/section/ul/li[1]/span/span").text)
            loops_count = int(posts_count / 12)
            print(loops_count)

            posts_urls = []

            for i in range(0, loops_count):
                hrefs = browser.find_elements_by_tag_name('a')
                hrefs = [item.get_attribute('href') for item in hrefs if "/p/" in item.get_attribute('href')]

                for href in hrefs:
                    posts_urls.append(href)

                browser.execute_script('window.scrollTo(0, document.body.scrollHeight);')
                time.sleep(random.randrange(2, 4))
                print(f'Интерация#{i}')

                file_name = userpage.split('/')[-2]
                with open(f'{file_name}.txt', 'a') as file:
                    for post_url in posts_urls:
                        file.write(post_url + "\n")

                set_posts_urls = set(posts_urls)
                set_posts_urls = list(set_posts_urls)

                with open(f'{file_name}_set.txt', 'a') as file:
                    for post_url in set_posts_urls:
                        file.write(post_url + '\n')

                with open(f'{file_name}_set.txt') as file:
                    urls_list = file.readlines()
                for post_url in urls_list[0:6]:
                    try:
                        browser.get(post_url)
                        time.sleep(2)

                        like_button = browser.find_element_by_class_name('fr66n').click()

                        time.sleep(2)

                        print(f"Лайк на пост: {post_url} успешно поставлен!")


                    except Exception as ex:
                        print(ex)
                        self.close_browser()()

    def get_all_followers(self, userpage):
        browser = self.browser
        browser.get(userpage)
        time.sleep(4)
        file_name = userpage.split("/")[-2]

        # создаём папку с именем пользователя для чистоты проекта
        if os.path.exists(f"{file_name}"):
            print(f"Папка {file_name} уже существует!")
        else:
            print(f"Создаём папку пользователя {file_name}.")
            os.mkdir(file_name)

        wrong_userpage = "/html/body/div[1]/section/main/div/h2"

        if self.xpath_exists(wrong_userpage):
            print(f"Пользователя {file_name} не существует, проверьте URL")
            self.close_browser()
        else:
            print(f"Пользователь {file_name} успешно найден, начинаем скачивать ссылки на подписчиков!")
            time.sleep(2)

            followers_button = browser.find_element_by_xpath(
                "/html/body/div[1]/section/main/div/header/section/ul/li[2]/a/span")
            followers_count = followers_button.text
            followers_count = int(followers_count.split(' ')[0])
            print(f"Количество подписчиков: {followers_count}")
            time.sleep(2)

            loops_count = int(followers_count / 12)
            print(f"Число итераций: {loops_count}")
            time.sleep(4)

            followers_button.click()
            time.sleep(4)

            followers_ul = browser.find_element_by_xpath("/html/body/div[4]/div/div/div[2]")

            try:
                followers_urls = []
                for i in range(1, loops_count + 1):
                    browser.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", followers_ul)
                    time.sleep(random.randrange(2, 4))
                    print(f"Итерация #{i}")

                all_urls_div = followers_ul.find_elements_by_tag_name("li")

                for url in all_urls_div:
                    url = url.find_element_by_tag_name("a").get_attribute("href")
                    followers_urls.append(url)

                # сохраняем всех подписчиков пользователя в файл
                with open(f"{file_name}/{file_name}.txt", "a") as text_file:
                    for link in followers_urls:
                        text_file.write(link + "\n")

                with open(f"{file_name}/{file_name}.txt") as text_file:
                    users_urls = text_file.readlines()

                    for user in users_urls:
                        try:
                            try:
                                with open(f'{file_name}/{file_name}_subscribe_list.txt',
                                          'r') as subscribe_list_file:
                                    lines = subscribe_list_file.readlines()
                                    if user in lines:
                                        print(f'Мы уже подписаны на {user}, переходим к следующему пользователю!')
                                        continue

                            except Exception as ex:
                                print('Файл со ссылками ещё не создан!')
                                # print(ex)

                            browser = self.browser
                            browser.get(user)
                            page_owner = user.split("/")[-2]

                            if self.xpath_exists("/html/body/div[1]/section/main/div/header/section/div[1]/div/a"):

                                print("Это наш профиль, уже подписан, пропускаем итерацию!")
                            elif self.xpath_exists(
                                    "/html/body/div[1]/section/main/div/header/section/div[1]/div[2]/div/span/span[1]/button/div/span"):
                                print(f"Уже подписаны, на {page_owner} пропускаем итерацию!")
                            else:
                                time.sleep(random.randrange(4, 8))

                                if self.xpath_exists(
                                        "/html/body/div[1]/section/main/div/div/article/div[1]/div/h2"):
                                    try:
                                        follow_button = browser.find_element_by_xpath(
                                            "/html/body/div[1]/section/main/div/header/section/div[1]/div[1]/button").click()
                                        print(f'Запросили подписку на пользователя {page_owner}. Закрытый аккаунт!')
                                    except Exception as ex:
                                        print(ex)
                                else:
                                    try:
                                        if self.xpath_exists(
                                                "/html/body/div[1]/section/main/div/header/section/div[1]/div[1]/button"):
                                            follow_button = browser.find_element_by_xpath(
                                                "/html/body/div[1]/section/main/div/header/section/div[1]/div[1]/button").click()
                                            print(f'Подписались на пользователя {page_owner}. Открытый аккаунт!')
                                        else:
                                            follow_button = browser.find_element_by_xpath(
                                                "/html/body/div[1]/section/main/div/header/section/div[1]/div[1]/div/div").click()
                                            print(f'Подписались на пользователя {page_owner}. Открытый аккаунт!')
                                    except Exception as ex:
                                        print(ex)

                                # записываем данные в файл для ссылок всех подписок, если файла нет, создаём, если есть - дополняем
                                with open(f'{file_name}/{file_name}_subscribe_list.txt',
                                          'a') as subscribe_list_file:
                                    subscribe_list_file.write(user)

                                time.sleep(random.randrange(7, 15))

                        except Exception as ex:
                            print(ex)
                            self.close_browser()

            except Exception as ex:
                print(ex)
                self.close_browser()

        self.close_browser()


bot = InstagramBot(username,password)
bot.login()
# Описание функций для самых маленьких
bot.get_all_followers('https://www.instagram.com/vet.stein/')
