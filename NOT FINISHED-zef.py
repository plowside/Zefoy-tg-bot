import base64
import json
import os.path
import time

import requests
import re

from PIL import Image
from io import BytesIO
from urllib.parse import unquote



class Zefoy:
    def __init__(self, save_session: bool = False):
        self.save_session = save_session
        self.ses = requests.Session()

        self.services = {}
        self.services_ids = {}
        self.services_status = {}

        self.service_id = None
        self.video_key = None
        self.video_info = {}

    def solve_captcha(self, image_obj: BytesIO, delete_tag: list = ['\n','\r']):
        print('[+] Solving captcha...')
        req = (self.ses.post("https://plowsidecaptcha.pythonanywhere.com/captcha", files={"file": ("captcha.png", image_obj, "image/png")})).json()
        solved_text = req['captcha_text']
        for x in delete_tag: solved_text = solved_text.replace(x,'')
        return solved_text

    def get_services(self, html: str):
        for x in re.findall(r'<h5 class="card-title">.+</h5>\n.+\n.+', html): self.services[x.split('<h5 class="card-title">')[1].split('<')[0].strip()] = x.split('d-sm-inline-block">')[1].split('</small>')[0].strip()
        for x in re.findall(r'<h5 class="card-title mb-3">.+</h5>\n<form action=".+">', html): self.services_ids[x.split('title mb-3">')[1].split('<')[0].strip()] = x.split('<form action="')[1].split('">')[0].strip()
        for x in re.findall(r'<h5 class="card-title">.+</h5>\n.+<button .+', html): self.services_status[x.split('<h5 class="card-title">')[1].split('<')[0].strip()] = False if 'disabled class' in x else True


    def login(self):
        if self.save_session and os.path.exists('.session'):
            try:
                last_session = json.loads(open('.session', 'r', encoding='utf-8').read().strip())
                for k, v in last_session.items():
                    self.ses.cookies.set(k, v)
            except:
                ...
        index_headers = {
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'accept-language': 'ru,en-US;q=0.9,en;q=0.8,ru-RU;q=0.7',
            'cache-control': 'no-cache',
            'pragma': 'no-cache',
            'priority': 'u=0, i',
            'sec-ch-ua': '"Google Chrome";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
            'sec-ch-ua-arch': '"x86"',
            'sec-ch-ua-bitness': '"64"',
            'sec-ch-ua-full-version': '"131.0.6778.266"',
            'sec-ch-ua-full-version-list': '"Google Chrome";v="131.0.6778.266", "Chromium";v="131.0.6778.266", "Not_A Brand";v="24.0.0.0"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-model': '""',
            'sec-ch-ua-platform': '"Windows"',
            'sec-ch-ua-platform-version': '"15.0.0"',
            'sec-fetch-dest': 'document',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-site': 'none',
            'sec-fetch-user': '?1',
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
        }
        req = self.ses.get('https://zefoy.com/', headers=index_headers)
        # print(req.text)
        # print(req, '\n\n')
        if 'Enter Video URL' in req.text:
            ...
        else:
            captcha_token = req.text.split('type="text" name="')[1].split('"')[0]
            captcha_url = req.text.split('<img src="')[1].split('"')[0].replace('amp;', '')
            # print(f"captcha_token = '{captcha_token}' | captcha_url = '{captcha_url}'")


            captcha_img_headers = {
                'accept': 'image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8',
                'accept-language': 'ru,en-US;q=0.9,en;q=0.8,ru-RU;q=0.7',
                'cache-control': 'no-cache',
                'pragma': 'no-cache',
                'priority': 'u=2, i',
                'sec-ch-ua': '"Google Chrome";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
                'sec-ch-ua-arch': '"x86"',
                'sec-ch-ua-bitness': '"64"',
                'sec-ch-ua-full-version': '"131.0.6778.266"',
                'sec-ch-ua-full-version-list': '"Google Chrome";v="131.0.6778.266", "Chromium";v="131.0.6778.266", "Not_A Brand";v="24.0.0.0"',
                'sec-ch-ua-mobile': '?0',
                'sec-ch-ua-model': '""',
                'sec-ch-ua-platform': '"Windows"',
                'sec-ch-ua-platform-version': '"15.0.0"',
                'sec-fetch-dest': 'image',
                'sec-fetch-mode': 'no-cors',
                'sec-fetch-site': 'same-origin',
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
            }
            req = self.ses.get(f"https://zefoy.com/{captcha_url}", headers=captcha_img_headers)
            image = Image.open(BytesIO(req.content))
            image_obj = BytesIO()
            image.save(image_obj, format="PNG")
            image_obj.seek(0)
            captcha_solve = self.solve_captcha(image_obj)
            # print(f'captcha_solve = {captcha_solve}')

            cookies_to_set = {
                'window_size': '2560x1271',
                'user_agent': 'Mozilla%2F5.0%20(Windows%20NT%2010.0%3B%20Win64%3B%20x64)%20AppleWebKit%2F537.36%20(KHTML%2C%20like%20Gecko)%20Chrome%2F131.0.0.0%20Safari%2F537.36',
                'language': 'ru',
                'languages': 'ru,en-US,ru-RU,en',
                'time_zone': 'Asia/Novosibirsk',
                '_ga_1WEXNS5FFP': 'GS1.1.1737204399.1.0.1737204399.0.0.0',
                '_ga': 'GA1.1.1687897562.1737204399',
            }
            for k, v in cookies_to_set.items():
                self.ses.cookies.set(k, v)

            send_captcha_headers = {
                'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
                'accept-language': 'ru,en-US;q=0.9,en;q=0.8,ru-RU;q=0.7',
                'cache-control': 'no-cache',
                'content-type': 'application/x-www-form-urlencoded',
                'origin': 'null',
                'pragma': 'no-cache',
                'priority': 'u=0, i',
                'sec-ch-ua': '"Google Chrome";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
                'sec-ch-ua-arch': '"x86"',
                'sec-ch-ua-bitness': '"64"',
                'sec-ch-ua-full-version': '"131.0.6778.266"',
                'sec-ch-ua-full-version-list': '"Google Chrome";v="131.0.6778.266", "Chromium";v="131.0.6778.266", "Not_A Brand";v="24.0.0.0"',
                'sec-ch-ua-mobile': '?0',
                'sec-ch-ua-model': '""',
                'sec-ch-ua-platform': '"Windows"',
                'sec-ch-ua-platform-version': '"15.0.0"',
                'sec-fetch-dest': 'document',
                'sec-fetch-mode': 'navigate',
                'sec-fetch-site': 'same-origin',
                'sec-fetch-user': '?1',
                'upgrade-insecure-requests': '1',
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
            }

            data = {
                captcha_token: captcha_solve,
            }
            req = self.ses.post('https://zefoy.com/', data=data, headers=send_captcha_headers)
            # print(req.text)
            # print(req, '\n\n')

            is_captcha = '?_CAPTCHA' in req.text
            is_success = 'Enter Video URL' in req.text

            if is_captcha:
                print('[-] Invalid captcha solve')
                return 'invalid_captcha'
            elif is_success:
                print(f'[+] Session created')
            else:
                print('[-] login: Unknown response')
                return 'unknown_response'

        self.get_services(req.text)
        print('Available services =', json.dumps(self.services_ids, indent=4))

        self.video_key = req.text.split('" placeholder="Enter Video URL"')[0].split('name="')[-1]
        if self.save_session:
            try: open('.session', 'w', encoding='utf-8').write(json.dumps(self.ses.cookies.get_dict(), indent=4, ensure_ascii=False))
            except Exception as e:
                print(f'[-] Error when saving session: {e}')
        return 'success'

    def send_video(self, service: str, video_url: str):
        service_id = self.services_ids.get(service, None)
        self.service_id = service_id
        if not service_id:
            print(f"[-] send_video: Unknown service ({service}). Available services: {self.services_ids.keys()}")
            return 'error'

        send_video_headers = {
            'accept': '*/*',
            'accept-language': 'ru,en-US;q=0.9,en;q=0.8,ru-RU;q=0.7',
            'cache-control': 'no-cache',
            'origin': 'https://zefoy.com',
            'pragma': 'no-cache',
            'priority': 'u=1, i',
            'sec-ch-ua': '"Google Chrome";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
            'sec-ch-ua-arch': '"x86"',
            'sec-ch-ua-bitness': '"64"',
            'sec-ch-ua-full-version': '"131.0.6778.266"',
            'sec-ch-ua-full-version-list': '"Google Chrome";v="131.0.6778.266", "Chromium";v="131.0.6778.266", "Not_A Brand";v="24.0.0.0"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-model': '""',
            'sec-ch-ua-platform': '"Windows"',
            'sec-ch-ua-platform-version': '"15.0.0"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
            'x-requested-with': 'XMLHttpRequest',
        }
        files = {
            self.video_key: (None, video_url),
        }
        req = self.ses.post(f'https://zefoy.com/{self.service_id}', files=files, headers=send_video_headers)
        # print(req, req.text)
        resp = self.decode_payload(req.text)
        # print('send_video resp', resp)
        if 'onsubmit="showHideElements' in resp:
            # Success
            matches = re.findall(r'<input\s+type="hidden"\s+name="([^"]+)"\s+value="([^"]+)"\s*/?>', resp)
            self.video_info = {name: value for name, value in matches}
            # print('self.video_info', self.video_info)
            return 'success'
        else:
            is_sleep = self.handle_sleep(resp)
            if is_sleep:
                return self.send_video(service, video_url)
            print(resp)
            print('[-] send_video: Unknown response')
            return 'unknown_response'


    def send_views(self):
        send_views_headers = {
            'accept': '*/*',
            'accept-language': 'ru,en-US;q=0.9,en;q=0.8,ru-RU;q=0.7',
            'cache-control': 'no-cache',
            'origin': 'https://zefoy.com',
            'pragma': 'no-cache',
            'priority': 'u=1, i',
            'sec-ch-ua': '"Google Chrome";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
            'sec-ch-ua-arch': '"x86"',
            'sec-ch-ua-bitness': '"64"',
            'sec-ch-ua-full-version': '"131.0.6778.266"',
            'sec-ch-ua-full-version-list': '"Google Chrome";v="131.0.6778.266", "Chromium";v="131.0.6778.266", "Not_A Brand";v="24.0.0.0"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-model': '""',
            'sec-ch-ua-platform': '"Windows"',
            'sec-ch-ua-platform-version': '"15.0.0"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
            'x-requested-with': 'XMLHttpRequest',
        }
        files = {
            k: (None, v) for k, v in self.video_info.items()
        }
        time.sleep(2)
        req = self.ses.post(f'https://zefoy.com/{self.service_id}', files=files, headers=send_views_headers)
        # print(req, req.text)
        resp = self.decode_payload(req.text)
        # print('send_views resp', resp)

        if "text-align:center;color:green;'>" in resp:
            # Success
            result = resp.split("text-align:center;color:green;'>")[1].split("</")[0].strip()
            print(f'[+] {result}')
            return 'success'
        else:
            if self.handle_sleep(resp):
                self.send_views()
            print('[-] send_video: Unknown response')
            return 'unknown_response'

    def handle_sleep(self, resp: str):
        if "Checking Timer" in resp:
            time_to_sleep = int(resp.split('var ltm=')[1].split(';')[0])
        elif "seconds before trying" in resp:
            time_to_sleep = int(resp.split('var remainingTimelogin = ')[1].split(';')[0])
        else:
            return False
        print(f'[-] Sleeping before next request: {time_to_sleep} seconds')
        time.sleep(time_to_sleep+2)
        return True

    def decode_payload(self, payload: str, is_encrypt: bool = False):
        if is_encrypt:
            return payload
        else:
            try:
                return base64.b64decode(unquote(payload.encode()[::-1])).decode()
            except Exception as e:
                print(f'[-] Error on decoding payload ({e}): {payload}')


if __name__ == "__main__":
    z = Zefoy(save_session=True)
    result = z.login()
    if result != 'success':
        exit()
    result = z.send_video('Hearts', 'https://www.tiktok.com/@flowsideee/video/7376686071742074129')
    if result != 'success':
        exit()
    result = z.send_views()
