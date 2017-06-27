import requests

from pyquery import PyQuery as pq
from urllib import parse

class QuiBai(object):
    def __init__(self):
        self.haeders = {
            'User-Agent': ('Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_4) '
                           'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36')
        }
        self.queue = []
        self.start_url = 'https://www.qiushibaike.com/text'
        self.num = 1
        self.sign = {'s': 4995149}
        self.requests = requests

    @staticmethod
    def url_concat(url, args=None):
        if not args:
            return url
        if url[-1] not in ('?', '&'):
            url += '?' if '?' not in url else '&'
        return url+parse.urlencode(args)

    def get_next_ur(self):
        url = self.start_url + '/page' + str(self.num) + '/'
        return self.url_concat(url, args=self.sign)

    def fetch_url(self, url):
        resp = self.requests.get(url)
        self.num += 1
        self.num = self.num if self.num < 36 else 1
        return resp.content

    def parse_resp(self, content):
        e = pq(content)
        items = e('.article')
        texts = [self.text_from_spam(item) for item in items]
        return texts

    def text_from_spam(self, content):
        e = pq(content)
        text = e('span').text()
        score = int(pq(e('.stats-vote'))('i').text())
        print(score, text)

    def start(self):
        for i in range(36):
            url = self.start_url if self.num == 1 else self.get_next_ur()
            resp_content = self.fetch_url(url)
            self.parse_resp(resp_content)

if __name__ == '__main__':
    quibai = QuiBai()
    quibai.start()

