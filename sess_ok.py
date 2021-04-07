import requests
import fake_useragent
import pickle
from data import Data


class CreateSession:
    def __init__(self, login=None, password=None, timeout=2, user=None, link=None, auto=True):

        self.login = login
        self.password = password
        self.timeout = timeout

        if self.login is not None:
            Data.update_login_and_password(login=login)

        if self.password is not None:
            Data.update_login_and_password(password=password)

        if user is None:
            user = fake_useragent.UserAgent().random
        self.user = user

        if link is None:
            link = "https://ok.ru"
        self.link = link
        self.session = None

        self.header = {
            'user-agent': self.user
        }
        self.params = {
            'cmd': 'AnonymLogin',
            'st.cmd': 'anonymLogin'
        }
        if auto:
            self.create_session()
            self.save_session()

    def create_session(self):

        self.session = requests.Session()

        data = Data.get_data()

        responce = self.session.post(self.link, data=data, headers=self.header, params=self.params, timeout=self.timeout)
        # print(responce.text)

    def save_session(self, name_cookies='cookies', name_header='header'):
        cookies_dict = [
            {'domain': key.domain, "name": key.name, "path": key.path, "value": key.value}
            for key in self.session.cookies
        ]

        with open(f'{name_cookies}.pickle', 'wb') as f:
            pickle.dump(cookies_dict, f)

        with open(f'{name_header}.pickle', 'wb') as f:
            pickle.dump(self.header, f)


if __name__ == "__main__":
    CreateSession()
