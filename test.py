import requests
from PIL import Image
from io import BytesIO
from urllib.parse import unquote
import base64, re, time



class Zefoy:
    def __init__(self):
        self.ses = requests.Session()
        self.ses.proxies = {'http': 'http://modeler_gdSGv9:xyXfKa8Xe8gg@194.71.107.64:10197', 'https': 'http://modeler_gdSGv9:xyXfKa8Xe8gg@194.71.107.64:10197'}

        self.video_key = None
        self.captcha_token = None
        self.services = {}
        self.services_ids = {}
        self.services_status = {}
        self.service_url = None

    def prepare_session(self):
        self.ses.cookies.set("cf_clearance", "pUMuWN7rOxM9ejJHU.zG3DDcD1SJdajFA59gbu6bxig-1733304601-1.2.1.1-BD6K7AyA7lFR2MJc.ENpXyCRozmDqyyZinQc8CKPSmwBskxT.Gi4PfwjQhBODzKbp2jyZOuZF4CkfZ_peC9t9HNzoJPT6xVb02YaGPsHgmCy.l7bQrGBOH8kXEKXiLnH1FWvA0skSR9C1sLQk21VTicYIILF0mQrd7b39Wzn5HexSgy4muI5jjRUxp7vqQ82UcC4grzPPnaRr30bsAGbm7dWBDQZKxYV6zza2e3vrR6Qf.P_rGW0nSFGDeYG1BTycig0UB_UYNwlveToNk5YsUgH9WbTOzwxgcaz3cqOrERPuE2HLxghexUwhe7h96JN6Ppv8xlJPgPTY69bamswNzUmT3DsxV0bmmRsh1rPEH_ZkvDgKDaeIpMNonI7mOAu2tSbiCe319kkKjoheuuoAA1sqc5Y0ovS6GB14KCrvvoR0ezDfoxy2BJAngedBMsi", domain="zefoy.com")
        self.ses.cookies.set("window_size", "1920x911", domain="zefoy.com")
        self.ses.cookies.set("user_agent", "Mozilla%2F5.0%20(Windows%20NT%2010.0%3B%20Win64%3B%20x64)%20AppleWebKit%2F537.36%20(KHTML%2C%20like%20Gecko)%20Chrome%2F129.0.0.0%20Safari%2F537.36", domain="zefoy.com")
        self.ses.cookies.set("language", "de-AT", domain="zefoy.com")
        self.ses.cookies.set("languages", "de-AT,de,en-US,en", domain="zefoy.com")
        self.ses.cookies.set("time_zone", "Europe/Vienna", domain="zefoy.com")
        self.ses.cookies.set("cf-locale", "de-AT", domain="zefoy.com")

    def run(self, video_url: str):
        self.prepare_session()
        captcha = self.get_captcha()
        solve = self.solve_captcha(captcha)
        print(solve)
        authed = self.send_captcha(solve)
        self.use_service()


    def get_captcha(self):
        get_captcha_headers = {
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'accept-language': 'de-AT,de;q=0.9,en-US;q=0.8,en;q=0.7',
            'cache-control': 'max-age=0',
            'priority': 'u=0, i',
            'sec-ch-ua': '"Google Chrome";v="129", "Not=A?Brand";v="8", "Chromium";v="129"',
            'sec-ch-ua-arch': '"x86"',
            'sec-ch-ua-bitness': '"64"',
            'sec-ch-ua-full-version': '"129.0.6668.71"',
            'sec-ch-ua-full-version-list': '"Google Chrome";v="129.0.6668.71", "Not=A?Brand";v="8.0.0.0", "Chromium";v="129.0.6668.71"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-model': '""',
            'sec-ch-ua-platform': '"Windows"',
            'sec-ch-ua-platform-version': '"10.0.0"',
            'sec-fetch-dest': 'document',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-site': 'same-origin',
            'sec-fetch-user': '?1',
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36',
        }
        resp = self.ses.get('https://zefoy.com/', headers=get_captcha_headers)

        if 'Enter Video URL' in resp.text: # Already authed
            self.video_key = resp.text.split('" placeholder="Enter Video URL"')[0].split('name="')[-1]
            return None
        elif '<title>Attention Required! | Cloudflare</title>' in resp.text:
            print('[-] Your ip region blocked for zefoy.com')
            return False
        elif '<title>Just a moment...</title>' in resp.text: # 403
            print('[-] Cloudflare, cant solve...')
            return False

        try:
            if 'Too many requests. Please slow down.</h1' in resp.text:
                print('[-] Slow down')
                time.sleep(120)
                return self.get_captcha()
            self.captcha_token = resp.text.split('type="text" name="')[1].split('"')[0]
            captcha_url = resp.text.split('<img src="')[1].split('"')[0].replace('amp;', '')

            get_captcha_headers = {
                'accept': 'image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8',
                'accept-language': 'de-AT,de;q=0.9,en-US;q=0.8,en;q=0.7',
                'priority': 'i',
                'sec-ch-ua': '"Google Chrome";v="129", "Not=A?Brand";v="8", "Chromium";v="129"',
                'sec-ch-ua-arch': '"x86"',
                'sec-ch-ua-bitness': '"64"',
                'sec-ch-ua-full-version': '"129.0.6668.71"',
                'sec-ch-ua-full-version-list': '"Google Chrome";v="129.0.6668.71", "Not=A?Brand";v="8.0.0.0", "Chromium";v="129.0.6668.71"',
                'sec-ch-ua-mobile': '?0',
                'sec-ch-ua-model': '""',
                'sec-ch-ua-platform': '"Windows"',
                'sec-ch-ua-platform-version': '"10.0.0"',
                'sec-fetch-dest': 'image',
                'sec-fetch-mode': 'no-cors',
                'sec-fetch-site': 'same-origin',
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36',
            }
            req = self.ses.get(f"https://zefoy.com/{captcha_url}", headers=get_captcha_headers)
            image = Image.open(BytesIO(req.content))
            image_obj = BytesIO()
            image.save(image_obj, format="PNG")
            image_obj.seek(0)
            return image_obj
        except Exception as e:
            print(f"Can\'t get captcha: {e}", type(e))
            time.sleep(2)
            return self.get_captcha()

    def solve_captcha(self, image_obj: BytesIO, delete_tag: list = ['\n','\r']):
        print('[+] Solving captcha...')
        req = (requests.post("https://plowsidecaptcha.pythonanywhere.com/captcha", files={"file": ("captcha.png", image_obj, "image/png")})).json()
        solved_text = req['captcha_text']
        for x in delete_tag: solved_text = solved_text.replace(x,'')
        return solved_text

    def send_captcha(self, solve: str):
        send_captcha_headers = {
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'accept-language': 'de-AT,de;q=0.9,en-US;q=0.8,en;q=0.7',
            'cache-control': 'max-age=0',
            'content-type': 'application/x-www-form-urlencoded',
            'origin': 'null',
            'priority': 'u=0, i',
            'sec-ch-ua': '"Google Chrome";v="129", "Not=A?Brand";v="8", "Chromium";v="129"',
            'sec-ch-ua-arch': '"x86"',
            'sec-ch-ua-bitness': '"64"',
            'sec-ch-ua-full-version': '"129.0.6668.71"',
            'sec-ch-ua-full-version-list': '"Google Chrome";v="129.0.6668.71", "Not=A?Brand";v="8.0.0.0", "Chromium";v="129.0.6668.71"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-model': '""',
            'sec-ch-ua-platform': '"Windows"',
            'sec-ch-ua-platform-version': '"10.0.0"',
            'sec-fetch-dest': 'document',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-site': 'same-origin',
            'sec-fetch-user': '?1',
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36',
        }
        resp = self.ses.post('https://zefoy.com/', data={self.captcha_token: solve}, headers=send_captcha_headers)
        if 'Join our' in resp.text:
            self.video_key = resp.text.split('" placeholder="Enter Video URL"')[0].split('name="')[-1]
            self.get_services(resp.text)
            print('[+] Session was created')
            return True
        else:
            if resp.text != '': print('[-] send_captcha', resp.text)
            return False

    def get_services(self, html: str):
        for _ in range(3):
            for x in re.findall(r'<h5 class="card-title">.+</h5>\n.+\n.+', html): self.services[x.split('<h5 class="card-title">')[1].split('<')[0].strip()] = x.split('d-sm-inline-block">')[1].split('</small>')[0].strip()
            for x in re.findall(r'<h5 class="card-title mb-3">.+</h5>\n<form action=".+">', html): self.services_ids[x.split('title mb-3">')[1].split('<')[0].strip()] = x.split('<form action="')[1].split('">')[0].strip()
            for x in re.findall(r'<h5 class="card-title">.+</h5>\n.+<button .+', html): self.services_status[x.split('<h5 class="card-title">')[1].split('<')[0].strip()] = False if 'disabled class' in x else True
            if len(self.services_ids) > 0:
                break
            else:
                time.sleep(2)
                get_captcha_headers = {
                    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
                    'accept-language': 'de-AT,de;q=0.9,en-US;q=0.8,en;q=0.7',
                    'cache-control': 'max-age=0',
                    'priority': 'u=0, i',
                    'sec-ch-ua': '"Google Chrome";v="129", "Not=A?Brand";v="8", "Chromium";v="129"',
                    'sec-ch-ua-arch': '"x86"',
                    'sec-ch-ua-bitness': '"64"',
                    'sec-ch-ua-full-version': '"129.0.6668.71"',
                    'sec-ch-ua-full-version-list': '"Google Chrome";v="129.0.6668.71", "Not=A?Brand";v="8.0.0.0", "Chromium";v="129.0.6668.71"',
                    'sec-ch-ua-mobile': '?0',
                    'sec-ch-ua-model': '""',
                    'sec-ch-ua-platform': '"Windows"',
                    'sec-ch-ua-platform-version': '"10.0.0"',
                    'sec-fetch-dest': 'document',
                    'sec-fetch-mode': 'navigate',
                    'sec-fetch-site': 'same-origin',
                    'sec-fetch-user': '?1',
                    'upgrade-insecure-requests': '1',
                    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36',
                }
                resp = self.ses.get('https://zefoy.com/', headers=get_captcha_headers)
                html = resp.text

    def get_payload(self, payload: str, is_encrypt: bool = False):
        if is_encrypt:
            return payload
        else:
            try:
                return base64.b64decode(unquote(payload.encode()[::-1])).decode()
            except:
                print(f'[-] Error on getting payload: {payload}')

    def use_service(self, service: str, video_url: str):
        self.service_url = f'https://zefoy.com/{self.services_ids[service]}'

        self.get_video(video_url)
        self.send_service(service)

    def send_service(self, service: str, video_url: str):
        self.service_url = f'https://zefoy.com/{self.services_ids[service]}'

        self.get_video(video_url)
        if service == 'Comments Hearts':
            ...

    def get_video(self, video_url: str):
        get_video_headers = {
            'accept': '*/*',
            'accept-language': 'de-AT,de;q=0.9,en-US;q=0.8,en;q=0.7',
            'origin': 'https://zefoy.com',
            'priority': 'u=1, i',
            'sec-ch-ua': '"Google Chrome";v="129", "Not=A?Brand";v="8", "Chromium";v="129"',
            'sec-ch-ua-arch': '"x86"',
            'sec-ch-ua-bitness': '"64"',
            'sec-ch-ua-full-version': '"129.0.6668.71"',
            'sec-ch-ua-full-version-list': '"Google Chrome";v="129.0.6668.71", "Not=A?Brand";v="8.0.0.0", "Chromium";v="129.0.6668.71"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-model': '""',
            'sec-ch-ua-platform': '"Windows"',
            'sec-ch-ua-platform-version': '"10.0.0"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36',
            'x-requested-with': 'XMLHttpRequest',
        }
        files = {
            self.video_key: (None, video_url),
        }
        resp = self.ses.post(self.service_url, headers=get_video_headers, files=files)
        resp = self.get_payload(resp.text)
        if 'Session expired. Please re-login' in resp:
            print('[-] Session expired')
            return False
        elif 'service is currently not working' in resp:
            print('[-] Service is currently not working')
        elif 'onsubmit="showHideElements' in resp:
            z = resp.split('="col-sm-12')[0].split('hidden" name="')[-1]
            self.video_info = [
                resp.split('" name="')[1].split('"')[0],
                resp.split('value="')[1].split('"')[0],
                z.split('"')[0],
                z.split('" value="')[1].split('"')[0],
            ]
        elif 'Checking Timer...' in resp or 'The server is too busy. Please try again in' in resp or 'seconds before trying again' in resp:
            if 'The server is too busy. Please try again in' in resp:
                time_to_sleep = int(re.findall(r'Please try again in (\d*)', resp)[0])
            elif 'seconds before trying again' in resp:
                time_to_sleep = int(re.findall(r'Please wait (\d*) seconds before trying again', resp)[0])
            else:
                time_to_sleep = int(re.findall(r'ltm=(\d*);', resp)[0])
            if time_to_sleep >= 0 and time_to_sleep <= 1000:
                print(f'[-] Time to next use: {time_to_sleep}')
                time.sleep(time_to_sleep+1)
            else:
                print(f'[-] Your IP was banned: {time_to_sleep}s')
                return None
            return self.get_video(video_url)
        elif 'Too many requests. Please slow' in resp:
            print('[-] Too many requests')
            time.sleep(2)
            return self.get_video(video_url)
        elif 'No an comment found' in resp:
            return 'No an comment found'
        elif 'An error occurred. Please try again' in resp:
            return self.get_video(video_url)
        else:
            print('[+] Video_resp', resp)
        return resp



if __name__ == '__main__':
    zf = Zefoy()
    zf.run('https://www.tiktok.com/@macocm7/video/7419555070087335211?is_from_webapp=1&sender_device=pc')
    print(zf.services)