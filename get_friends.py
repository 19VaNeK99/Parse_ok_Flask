import pickle
import requests
import time
from bs4 import BeautifulSoup
from sess_ok import CreateSession
from data import Data


class GetFriends:
    def __init__(self, timeout=5):

        self.timeout = timeout
        self.start = time.time()
        self.session = requests.Session()

    @staticmethod
    def load_data(cookies_pick='cookies.pickle', header_pick='header.pickle'):

        with open(cookies_pick, 'rb') as f:
            cookies_dict = pickle.load(f)

        with open(header_pick, 'rb') as f:
            header = pickle.load(f)

        return header, cookies_dict

    def load_session(self, header_pick, cookies_pick):

        try:
            header, cookies_dict = GetFriends.load_data(cookies_pick=cookies_pick, header_pick=header_pick)
        except:
            print("создадим сессию")
            # if cookies_dict is None or header is None:
            login, password = Data.get_login_and_password()
            CreateSession(login=login, password=password, timeout=self.timeout)
            header, cookies_dict = GetFriends.load_data()

        for cookies in cookies_dict:
            self.session.cookies.set(**cookies)

        self.session.headers = header

    def parse_friends(self, print_response=False, id_user="563955862689",
                      limit=None, header_pick='header.pickle', cookies_pick='cookies.pickle'):

        if self.check_timeout():
            return {'error': 'timeout', 'result': []}

        self.load_session(header_pick, cookies_pick)

        if self.check_timeout():
            return {'error': 'timeout', 'result': []}

        friends_link = f'https://ok.ru/profile/{id_user}/friends'
        try:
            friends_responce = self.session.get(friends_link, timeout=self.timeout - (time.time()-self.start))
        except:
            return {'error': 'error getting user friends', 'result': []}

        if self.check_timeout():
            return {'error': 'timeout', 'result': []}

        if friends_responce.status_code != 200:
            return {'error': 'error getting user friends', 'result': []}

        friends_responce = friends_responce.text

        if "авторизованным пользователям" in friends_responce.lower():
            return {'error': 'authentication failed', 'result': []}

        if print_response:
            print(friends_responce)

        result = []
        count_friends = 0
        page = 2

        friends_with_only_html = self.parse_html(friends_responce, count_friends, limit)
        result.extend(friends_with_only_html[0])
        count_friends = friends_with_only_html[1]

        page += 1

        if result:
            return {'result': result}

    def parse_html(self, friends_responce, count_friends, limit):
        try:
            soup = BeautifulSoup(friends_responce, 'lxml')
        except:
            return [], count_friends
        body = soup.find_all("div", {"class": "ucard-w __rounded"})
        result = []
        for i in body:
            try:
                data_user = GetFriends.parse_user(i)
                result.append(data_user)
            except:
                print("Какой то невалидный дружок!")

            count_friends += 1

            if limit is not None and count_friends >= limit:
                break
            if self.timeout is not None and time.time() - self.start > self.timeout:
                return result, count_friends

        if result:
            return result, count_friends
        else:
            return [], count_friends

    @staticmethod
    def parse_user(div):

        id_user = div.find("span", {"class": "__l"})
        id_user = str(id_user).split('data-id')[1].split('"')[1]
        name = div.find("a", {"class": "o"}).text
        photo = str(div.find("img", {"class": "photo_img"}))
        photo = photo.split("photo_img")[1].split("&")[0].split('"')[-1]

        return {'id': id_user, 'name': name, 'photo': photo}

    def check_timeout(self):
        if time.time() - self.start > self.timeout:
            return True
        else:
            return False


if __name__ == "__main__":
    print(GetFriends().parse_friends())
