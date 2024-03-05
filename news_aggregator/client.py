import requests


class NewsClient:
    def __init__(self, base_url):
        self.base_url = base_url

    def login(self, username, password):
        url = f"{self.base_url}/login/"
        data = {'username': username, 'password': password}
        response = requests.post(url, data=data)
        return response.json()

    def logout(self, token):
        url = f"{self.base_url}/logout/"
        headers = {'Authorization': f'Token {token}'}
        response = requests.post(url, headers=headers)
        return response.json()

    def post_story(self, token, headline, category, region, details):
        url = f"{self.base_url}/stories/"
        headers = {'Authorization': f'Token {token}'}
        data = {'headline': headline, 'category': category, 'region': region, 'details': details}
        response = requests.post(url, headers=headers, data=data)
        return response.json()

    def get_story(self, token, category, region, date):
        url = f"{self.base_url}/stories/"
        payload = f'story_cat={category}&story_region={region}&story_date={date}'
        headers = {'Authorization': f'Token {token}'}
        response = requests.post(url, headers=headers, data=payload)
        return response.json()

    def delete_story(self, token, story_key):
        url = f"{self.base_url}/stories/{story_key}/"
        headers = {'Authorization': f'Token {token}'}
        response = requests.delete(url, headers=headers)
        return response.json()
