import os


class Data:

    __login = os.environ.get('FLASK_OK_EMAIL')
    __password = os.environ.get('FLASK_OK_PASSWORD')
    __data = {
                'st.email': __login,
                'st.password': __password,
                'st.posted': 'set',
                'st.fJS': 'on',
                'st.st.screenSize': '1360 x 768',
                'st.st.browserSize': '628',
                'st.st.flashVer': '0.0.0',
                'st.iscode': 'False'
            }

    @staticmethod
    def get_data():
        return Data.__data

    @staticmethod
    def get_login_and_password():
        return Data.__login, Data.__password

    @staticmethod
    def update_data(new_data):
        Data.__data.update(new_data)

    @staticmethod
    def update_login_and_password(login=None, password=None):
        if login is not None:
            Data.__login = login
        if password is not None:
            Data.__password = password
        Data.__data.update({'st.email': Data.__login, 'st.password': Data.__password})
