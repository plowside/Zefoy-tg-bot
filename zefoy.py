import hashlib
import json
import os.path
import random

import aiofiles.os
import aiohttp
from selenium.webdriver.common.action_chains import ActionChains
import undetected_chromedriver as uc
import aiofiles, asyncio, httpx, base64, re
import time

from PIL import Image
from io import BytesIO
from urllib.parse import unquote

class Zefoy:
    def __init__(self, proxy: str = None, likes_to_send_count: int = 300):
        self.base_url = 'https://zefoy.com'
        self.service_url = f'{self.base_url}'
        self.proxy = (proxy if len(proxy.split(':')) == 2 or '@' in proxy else f"{proxy.split(':')[2]}:{proxy.split(':')[3]}@{proxy.split(':')[0]}:{proxy.split(':')[1]}") if proxy else None
        if self.proxy: self.client = httpx.AsyncClient(proxies={'http://': f'http://{self.proxy}', 'https://': f'http://{self.proxy}'}, timeout=120)
        else: self.client = httpx.AsyncClient(timeout=120)
        self.aclient = httpx.AsyncClient(timeout=120)
        self.captcha_token = None
        self.video_key = None
        self.services = {}
        self.services_ids = {}
        self.services_status = {}
        self.video_info = None
        self.likes_to_send_count = str(likes_to_send_count)

        # self.default_headers = {'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7','accept-language': 'de-AT,de;q=0.9,en-US;q=0.8,en;q=0.7','cache-control': 'no-cache','pragma': 'no-cache','priority': 'u=0, i','sec-ch-ua': '"Google Chrome";v="123", "Not:A-Brand";v="8", "Chromium";v="123"','sec-ch-ua-arch': '"x86"','sec-ch-ua-bitness': '"64"','sec-ch-ua-full-version': '"123.0.6312.46"','sec-ch-ua-full-version-list': '"Google Chrome";v="123.0.6312.46", "Not:A-Brand";v="8.0.0.0", "Chromium";v="123.0.6312.46"','sec-ch-ua-mobile': '?0','sec-ch-ua-model': '""','sec-ch-ua-platform': '"Windows"','sec-ch-ua-platform-version': '"15.0.0"','sec-fetch-dest': 'document','sec-fetch-mode': 'navigate','sec-fetch-site': 'same-origin','sec-fetch-user': '?1','upgrade-insecure-requests': '1','user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36'}
        # self.post_headers = {'accept': '*/*','accept-language': 'de-AT,de;q=0.9,en-US;q=0.8,en;q=0.7','origin': 'https://zefoy.com','priority': 'u=1, i','sec-ch-ua': '"Google Chrome";v="123", "Not:A-Brand";v="8", "Chromium";v="123"','sec-ch-ua-arch': '"x86"','sec-ch-ua-bitness': '"64"','sec-ch-ua-full-version': '"123.0.6312.46"','sec-ch-ua-full-version-list': '"Google Chrome";v="123.0.6312.46", "Not:A-Brand";v="8.0.0.0", "Chromium";v="123.0.6312.46"','sec-ch-ua-mobile': '?0','sec-ch-ua-model': '""','sec-ch-ua-platform': '"Windows"','sec-ch-ua-platform-version': '"15.0.0"','sec-fetch-dest': 'empty','sec-fetch-mode': 'cors','sec-fetch-site': 'same-origin','user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36','x-requested-with': 'XMLHttpRequest'}
        self.default_headers = {'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7','accept-language': 'ru,en-US;q=0.9,en;q=0.8,ru-RU;q=0.7','cache-control': 'no-cache','pragma': 'no-cache','priority': 'u=0, i','sec-ch-ua': '"Google Chrome";v="131", "Chromium";v="131", "Not_A Brand";v="24"','sec-ch-ua-arch': '"x86"','sec-ch-ua-bitness': '"64"','sec-ch-ua-full-version': '"131.0.6778.86"','sec-ch-ua-full-version-list': '"Google Chrome";v="131.0.6778.86", "Chromium";v="131.0.6778.86", "Not_A Brand";v="24.0.0.0"','sec-ch-ua-mobile': '?0','sec-ch-ua-model': '""','sec-ch-ua-platform': '"Windows"','sec-ch-ua-platform-version': '"15.0.0"','sec-fetch-dest': 'document','sec-fetch-mode': 'navigate','sec-fetch-site': 'same-origin','sec-fetch-user': '?1','upgrade-insecure-requests': '1','user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36'}
        self.post_headers = {'accept': '*/*','accept-language': 'ru,en-US;q=0.9,en;q=0.8,ru-RU;q=0.7','cache-control': 'no-cache','origin': 'https://zefoy.com','pragma': 'no-cache','priority': 'u=1, i','sec-ch-ua': '"Google Chrome";v="131", "Chromium";v="131", "Not_A Brand";v="24"','sec-ch-ua-arch': '"x86"','sec-ch-ua-bitness': '"64"','sec-ch-ua-full-version': '"131.0.6778.86"','sec-ch-ua-full-version-list': '"Google Chrome";v="131.0.6778.86", "Chromium";v="131.0.6778.86", "Not_A Brand";v="24.0.0.0"','sec-ch-ua-mobile': '?0','sec-ch-ua-model': '""','sec-ch-ua-platform': '"Windows"','sec-ch-ua-platform-version': '"15.0.0"','sec-fetch-dest': 'empty','sec-fetch-mode': 'cors','sec-fetch-site': 'same-origin','user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36','x-requested-with': 'XMLHttpRequest'}
        self.cf_clearance = None

    async def new_client(self, force_no_proxy: bool = False):
        if self.proxy and not force_no_proxy: self.client = httpx.AsyncClient(proxies={'http://': f'http://{self.proxy}', 'https://': f'http://{self.proxy}'}, timeout=120)
        else:
            self.proxy = None
            self.client = httpx.AsyncClient(timeout=120)
        user_agents = [
            'Mozilla%2F5.0%20(Windows%20NT%2010.0%3B%20Win64%3B%20x64)%20AppleWebKit%2F537.36%20(KHTML%2C%20like%20Gecko)%20Chrome%2F131.0.0.0%20Safari%2F537.36'
        ]
        self.client.cookies.set("user_agent", random.choice(user_agents))
        self.client.cookies.set("window_size", f"{random.randint(1911, 1920)}x{random.choice((900, 911, 940, 1000))}")
        self.client.cookies.set("language", "de-AT")
        self.client.cookies.set("languages", "de-AT,de,en-US,en")
        self.client.cookies.set("time_zone", "Europe/Vienna")
        if not self.cf_clearance and os.path.exists('.sessions'):
            this_ip = await self.get_ip()
            if not this_ip: return await self.new_client(force_no_proxy=True)
            try:
                async with aiofiles.open('.sessions', 'r', encoding='utf-8') as f:
                    file_content = json.loads(await f.read())
            except json.decoder.JSONDecodeError:
                file_content = {}
            except Exception as e:
                file_content = {}
                print(f'[-] Error while trying to get saved cf_clearance values: type={type(e)}|error={e}')
            self.cf_clearance = file_content.get(this_ip, None)
        if self.cf_clearance: self.client.cookies.set("cf_clearance", self.cf_clearance, 'zefoy.com')
        # print(f'new_client force_no_proxy={force_no_proxy} | cf_clearance={self.cf_clearance}')



    async def login(self, retry: int = 0):
        await self.new_client()
        if retry >= 5: print(f'[+] Logging in. Retry №{retry+1}')
        if self.proxy:
            try:
                for x in range(3):
                    await self.get_ip()
                    break
            except:
                print(f'[-] Invalid proxy: {self.proxy}')
                self.proxy = None
                await self.new_client(True)

        captcha = await self.get_captcha()
        # print(captcha, isinstance(captcha, str) and captcha == '_retry')
        if isinstance(captcha, str) and captcha == '_retry':
            return await self.login(retry+1)
        if not captcha: return
        solve = await self.solve_captcha(captcha)
        authed = await self.send_captcha(solve)
        if not authed:
            return await self.login(retry+1)

    async def solve_captcha(self, image_obj: BytesIO, delete_tag: list = ['\n','\r']):
        print('[+] Solving captcha...')
        req = (await self.aclient.post("https://plowsidecaptcha.pythonanywhere.com/captcha", files={"file": ("captcha.png", image_obj, "image/png")})).json()
        solved_text = req['captcha_text']
        for x in delete_tag: solved_text = solved_text.replace(x,'')
        return solved_text

    async def get_captcha(self):
        resp = await self.client.get(self.base_url, headers=self.default_headers)
        if 'Enter Video URL' in resp.text: # Already authed
            self.video_key = resp.text.split('" placeholder="Enter Video URL"')[0].split('name="')[-1]
            return None
        elif '<title>Attention Required! | Cloudflare</title>' in resp.text:
            print('[-] Your ip region blocked for zefoy.com')
            return False
        elif '<title>Just a moment...</title>' in resp.text: # 403
            print('[-] Cloudflare, trying to solve...')
            cf_clearance = await asyncio.get_event_loop().run_in_executor(None, self.get_cf_clearance)
            if cf_clearance:
                this_ip = await self.get_ip()
                if os.path.exists('.sessions'):
                    try:
                        async with aiofiles.open('.sessions', 'r', encoding='utf-8') as f:
                            file_content = json.loads(await f.read())
                    except Exception as e:
                        print(f'[-] Error getting .sessions: type={type(e)}|error={e}')
                        file_content = {}
                else:
                    file_content = {}
                async with aiofiles.open('.sessions', 'w', encoding='utf-8') as f:
                    file_content[this_ip] = cf_clearance
                    await f.write(json.dumps(file_content))
                self.cf_clearance = cf_clearance
                return '_retry'
            else:
                print('[-] Cloudflare, cant solve...')
                return False
        try:
            if 'Too many requests. Please slow down.</h1' in resp.text:
                print('[-] Slow down')
                await asyncio.sleep(120)
                return await self.get_captcha()
            self.captcha_token = resp.text.split('type="text" name="')[1].split('"')[0]
            captcha_url = resp.text.split('<img src="')[1].split('"')[0].replace('amp;', '')
            req = await self.client.get(f"{self.base_url}/{captcha_url}", headers=self.default_headers)
            image = Image.open(BytesIO(req.content))
            image_obj = BytesIO()
            image.save(image_obj, format="PNG")
            image_obj.seek(0)
            return image_obj
        except Exception as e:
            print(f"Can\'t get captcha: {e}", type(e))
            await asyncio.sleep(2)
            return await self.get_captcha()

    async def send_captcha(self, solve: str):
        resp = await self.client.post(self.base_url, data={self.captcha_token: solve}, headers=self.default_headers)
        if 'Join our' in resp.text:
            self.video_key = resp.text.split('" placeholder="Enter Video URL"')[0].split('name="')[-1]
            await self.get_services(resp.text)
            # print('[+] Session was created')
            return True
        else:
            if resp.text != '': print('[-] send_captcha', resp.text)
            return False

    async def get_services(self, html: str):
        for _ in range(3):
            for x in re.findall(r'<h5 class="card-title">.+</h5>\n.+\n.+', html): self.services[x.split('<h5 class="card-title">')[1].split('<')[0].strip()] = x.split('d-sm-inline-block">')[1].split('</small>')[0].strip()
            for x in re.findall(r'<h5 class="card-title mb-3">.+</h5>\n<form action=".+">', html): self.services_ids[x.split('title mb-3">')[1].split('<')[0].strip()] = x.split('<form action="')[1].split('">')[0].strip()
            for x in re.findall(r'<h5 class="card-title">.+</h5>\n.+<button .+', html): self.services_status[x.split('<h5 class="card-title">')[1].split('<')[0].strip()] = False if 'disabled class' in x else True
            if len(self.services_ids) > 0:
                break
            else:
                await asyncio.sleep(2)
                resp = await self.client.get(self.base_url, headers = {'Host': 'zefoy.com', 'Sec-Ch-Ua': '"Not?A_Brand";v="99", "Chromium";v="130"', 'Sec-Ch-Ua-Mobile': '?0', 'Sec-Ch-Ua-Platform': '"Windows"', 'Accept-Language': 'ru-RU,ru;q=0.9', 'Upgrade-Insecure-Requests': '1', 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.6723.70 Safari/537.36', 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7', 'Sec-Fetch-Site': 'none', 'Sec-Fetch-Mode': 'navigate', 'Sec-Fetch-User': '?1', 'Sec-Fetch-Dest': 'document', 'Priority': 'u=0, i', 'Connection': 'keep-alive'})
                html = resp.text

    async def use_service(self, service: str, url: str, comment_id: str = None, ttl: int = None, once: bool = False):
        """
        :param service: Сервис для накрутки
        :param url: Ссылка на видео
        :param comment_id: id комментария (Указывать, если service == "Comments Hearts")
        :param ttl: Время накрутки в секундах
        :return: Bool - успешна завершена накрутка
        """
        if service not in self.services_ids:
            return False
        self.service_url = f'{self.base_url}/{self.services_ids[service]}'

        current_ttl = 0
        while True:
            start = time.time()
            resp = await self.get_video(url)
            if resp in ['No an comment found']:
                print('ret', 1, 'return resp')
                return resp
            elif self.video_info is None:
                print('ret', 2, 'return False')
                return False
            await self.send_service(service, comment_id)
            if once:
                print('ret', 3, 'return True')
                return True
            if ttl is not None and ttl >= 0:
                current_ttl += time.time() - start
                if current_ttl >= ttl:
                    print('ret', 4, 'return True')
                    return True

    async def get_video(self, url: str):
        # print('[+] Getting video...')
        resp = await self.client.post(self.service_url, files={self.video_key: (None, url)}, headers=self.post_headers)

        resp = self.get_payload(resp.text)
        if 'Session expired. Please re-login' in resp:
            print('[-] Session expired')
            await self.login()
            return await self.get_video(url)
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
                await asyncio.sleep(time_to_sleep+1)
            else:
                print(f'[-] Your IP was banned: {time_to_sleep}s')
                return None
            return await self.get_video(url)
        elif 'Too many requests. Please slow' in resp:
            print('[-] Too many requests')
            await asyncio.sleep(2)
            return await self.get_video(url)
        elif 'No an comment found' in resp:
            return 'No an comment found'
        elif 'An error occurred. Please try again' in resp:
            await self.login()
            return await self.get_video(url)
        else:
            print('[+] Video_resp', resp)
        return resp

    async def send_service(self, service: str, comment_id: str = None, retry: int = 0):
        print(f'[+] Sending service {service}...')
        resp = await self.client.post(self.service_url, files={self.video_info[0]: (None, self.video_info[1])}, headers=self.post_headers)#{'Host': 'zefoy.com','Sec-Ch-Ua-Platform': '"Windows"','Accept-Language': 'ru-RU,ru;q=0.9','Sec-Ch-Ua': '"Not?A_Brand";v="99", "Chromium";v="130"','Sec-Ch-Ua-Mobile': '?0','X-Requested-With': 'XMLHttpRequest','User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.6723.70 Safari/537.36','Accept': '*/*','Origin': 'https://zefoy.com','Sec-Fetch-Site': 'same-origin','Sec-Fetch-Mode': 'cors','Sec-Fetch-Dest': 'empty','Priority': 'u=1, i'})
        resp = self.get_payload(resp.text)

        if service == 'Comments Hearts':
            v = re.search(r'<i class="text-red fa fa-heart"><\/i><\/div>\n<input type="hidden" name="([^"]+)".*\n<input type="hidden" name="([^"]+)"', resp)
            if not v:
                if 'Too many requests. Please slow' in resp or 'Checking Timer' in resp:
                    if 'Checking Timer' in resp:
                        if 'The server is too busy. Please try again in' in resp:
                            time_to_sleep = int(re.findall(r'Please try again in (\d*)', resp)[0])
                        elif 'next time in' in resp:
                            time_to_sleep = int(re.findall(r'next time in (\d*);', resp)[0])
                        elif 'service is currently not working' in resp:
                            time_to_sleep = 0
                            print('[-] Service is currently not working (Next time in)')
                        else:
                            time_to_sleep = int(re.findall(r'ltm=(\d*);', resp)[0])
                        if time_to_sleep >= 0 and time_to_sleep <= 1000:
                            print(f'[-] Time to next use: {time_to_sleep}')
                            await asyncio.sleep(time_to_sleep+1)
                        else:
                            print(f'[-] Your IP was banned: {time_to_sleep}s')
                            return None
                    else:
                        print('[-] Too many requests')
                else:
                    await asyncio.sleep(3)
                return await self.send_service(service, comment_id, retry+1)
            print('zzz', {v.group(1): (None, comment_id), v.group(2): (None, self.video_info[1]), self.video_info[2]: (None, self.video_info[3]), 'select_lmt': (None, self.likes_to_send_count)})
            resp = await self.client.post(self.service_url, files={v.group(1): (None, comment_id), v.group(2): (None, self.video_info[1]), self.video_info[2]: (None, self.video_info[3]), 'select_lmt': (None, self.likes_to_send_count)}, headers=self.post_headers)#{'Host': 'zefoy.com','Sec-Ch-Ua-Platform': '"Windows"','Accept-Language': 'ru-RU,ru;q=0.9','Sec-Ch-Ua': '"Not?A_Brand";v="99", "Chromium";v="130"','Sec-Ch-Ua-Mobile': '?0','X-Requested-With': 'XMLHttpRequest','User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.6723.70 Safari/537.36','Accept': '*/*','Origin': 'https://zefoy.com','Sec-Fetch-Site': 'same-origin','Sec-Fetch-Mode': 'cors','Sec-Fetch-Dest': 'empty','Priority': 'u=1, i'})
            resp = self.get_payload(resp.text)
            print(resp)


        if 'Session expired. Please re-login' in resp:
            print('[-] Session expired')
            await self.login()
            return await self.send_service(service, comment_id)
        elif 'sans-serif;text-align:center;color:green;\'>' in resp:
            print(resp.split("sans-serif;text-align:center;color:green;'>")[1].split("</")[0].strip())
        elif 'Too many requests. Please slow' in resp or 'Checking Timer' in resp:
            if 'Checking Timer' in resp:
                if 'The server is too busy. Please try again in' in resp:
                    time_to_sleep = int(re.findall(r'Please try again in (\d*)', resp)[0])
                else:
                    time_to_sleep = int(re.findall(r'ltm=(\d*);', resp)[0])
                if time_to_sleep >= 0 and time_to_sleep <= 1000:
                    print(f'[-] Time to next use: {time_to_sleep}')
                    await asyncio.sleep(time_to_sleep+1)
                else:
                    print(f'[-] Your IP was banned: {time_to_sleep}s')
                    return None
            else:
                print('[-] Too many requests')
            await asyncio.sleep(5)
        elif 'service is currently not working' in resp:
            return 'service is currently not working'
        elif 'Please try again later. Server too busy' in self.video_info:
            print('[-] Error on submit: Please try again later. Server too busy.')
        elif 'An error occurred. Please try again' in resp:
            print('[-] Error on submit: Please try again. (Maybe code error, site fixed)')
        elif 'Please use another browser' in resp:
            print('[-] Error on submit: Please use another browser.')
            await asyncio.sleep(5)
        else:
            if "sans-serif;text-align:center;color:green;'>" in resp:
                print('[+] send_service', resp.split("sans-serif;text-align:center;color:green;'>")[1].split("</")[0].strip())
            else:
                print('[+] send_service', resp)

    async def get_ip(self, service: str = 'https://eth0.me'):
        async with aiohttp.ClientSession() as session:
            try: resp = await session.get(service, proxy=f'http://{self.proxy}' if self.proxy else None)
            except aiohttp.client_exceptions.ClientProxyConnectionError:
                print(f'[-] Invalid proxy: {self.proxy}')
                self.proxy = None
                await self.new_client(True)
                return None
            except aiohttp.client_exceptions.ClientHttpProxyError:
                print(f'[-] Invalid proxy: {self.proxy}')
                self.proxy = None
                await self.new_client(True)
                return None
        return (await resp.text()).strip()

    def get_cf_clearance(self):
        options = uc.ChromeOptions()
        options.page_load_strategy = 'eager'
        kwargs = {
            'use_subprocess': False,
            'headless': False,
            'options': options
        }
        if self.proxy:
            proxy_extension = SeleniumProxyManager.get_proxy(self.proxy)
            options.add_argument(f'--load-extension={proxy_extension}')
        driver = uc.Chrome(proxy=self.proxy, **kwargs)
        driver.set_window_size(100, 400)
        driver.get("https://zefoy.com")
        time.sleep(3)
        retry = 0
        while True:
            x_coord = 0
            y_coord = 0

            # Выполнение клика по координатам
            action = ActionChains(driver)
            action.move_by_offset(x_coord, y_coord).click().perform()

            cookies = driver.get_cookies()
            cf_clearance_cookie = next(
                (cookie for cookie in cookies if cookie['name'] == 'cf_clearance'), None
            )
            if cf_clearance_cookie:
                cf_clearance_cookie = cf_clearance_cookie['value']
                print(f"[+] Got cf_clearance_cookie: {cf_clearance_cookie}")
                driver.quit()
                return cf_clearance_cookie
            if retry >= 150:
                print('[-] Cloudflare')
                driver.quit()
                return None
            time.sleep(.5)
            retry += 1

    def get_payload(self, payload: str, is_encrypt: bool = False):
        if is_encrypt:
            return payload
        else:
            try:
                return base64.b64decode(unquote(payload.encode()[::-1])).decode()
            except:
                print(f'[-] Error on getting payload: {payload}')




class SeleniumProxyManager:
    @classmethod
    def create_extension(cls, proxy: str):
        if '@' in proxy:
            proxy_host = proxy.split('@')[1].split(':')[0]
            proxy_port = proxy.split('@')[1].split(':')[1]
            proxy_user = proxy.split('@')[0].split(':')[0]
            proxy_pass = proxy.split('@')[0].split(':')[1]
        else:
            proxy_host, proxy_port, proxy_user, proxy_pass = proxy.split(':')
        extension_filename = f'{hashlib.md5(proxy.encode()).hexdigest()}'
        extension_path = f'proxy_extensions/{extension_filename}'


        manifest_json = """
        {
            "version": "<ext_ver>",
            "manifest_version": 3,
            "name": "<ext_name>",
            "permissions": [
                "proxy",
                "tabs",
                "storage",
                "webRequest",
                "webRequestAuthProvider"
            ],
            "host_permissions": [
                "<all_urls>"
            ],
            "background": {
                "service_worker": "background.js"
            },
            "minimum_chrome_version": "22.0.0"
        }
        """

        background_js = """
        var config = {
            mode: "fixed_servers",
            rules: {
                singleProxy: {
                    scheme: "http",
                    host: "<proxy_host>",
                    port: parseInt("<proxy_port>")
                },
                bypassList: ["localhost"]
            }
        };
    
        chrome.proxy.settings.set({
            value: config,
            scope: "regular"
        }, function() {});
    
        function callbackFn(details) {
            return {
                authCredentials: {
                    username: "<proxy_username>",
                    password: "<proxy_password>"
                }
            };
        }
    
        chrome.webRequest.onAuthRequired.addListener(
            callbackFn, {
                urls: ["<all_urls>"]
            },
            ['blocking']
        );
        """

        manifest = manifest_json
        js = background_js
        js = js.replace("<proxy_host>", proxy_host)
        js = js.replace("<proxy_port>", str(proxy_port))
        js = js.replace("<proxy_username>", proxy_user)
        js = js.replace("<proxy_password>", proxy_pass)

        manifest = manifest.replace("<ext_name>", 'Chrome Proxy')
        manifest = manifest.replace("<ext_ver>", '1.0.0')

        manifest_path = os.path.join(extension_path, "manifest.json")
        background_path = os.path.join(extension_path, "background.js")

        os.makedirs(extension_path, exist_ok=True)

        with open(manifest_path, mode="w") as manifest_file:
            manifest_file.write(manifest)

        with open(background_path, mode="w") as background_file:
            background_file.write(js)

        return extension_path

    @classmethod
    def get_proxy(cls, proxy: str):
        extension_filename = f'{hashlib.md5(proxy.encode()).hexdigest()}'
        os.makedirs('proxy_extensions', exist_ok=True)
        files = os.listdir('proxy_extensions')
        files = [f for f in files if os.path.isfile(os.path.join('proxy_extensions', f)) if extension_filename in f]
        if not files:
            cls.create_extension(proxy)

        extension_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), f'proxy_extensions/{extension_filename}')
        return extension_path


    @classmethod
    async def acreate_extension(cls, proxy: str):
        if '@' in proxy:
            proxy_host = proxy.split('@')[1].split(':')[0]
            proxy_port = proxy.split('@')[1].split(':')[1]
            proxy_user = proxy.split('@')[0].split(':')[0]
            proxy_pass = proxy.split('@')[0].split(':')[1]
        else:
            proxy_host, proxy_port, proxy_user, proxy_pass = proxy.split(':')
        extension_filename = f'{hashlib.md5(proxy.encode()).hexdigest()}'
        extension_path = f'proxy_extensions/{extension_filename}'

        manifest_json = """
        {
            "version": "<ext_ver>",
            "manifest_version": 3,
            "name": "<ext_name>",
            "permissions": [
                "proxy",
                "tabs",
                "storage",
                "webRequest",
                "webRequestAuthProvider"
            ],
            "host_permissions": [
                "<all_urls>"
            ],
            "background": {
                "service_worker": "background.js"
            },
            "minimum_chrome_version": "22.0.0"
        }
        """

        background_js = """
        var config = {
            mode: "fixed_servers",
            rules: {
                singleProxy: {
                    scheme: "http",
                    host: "<proxy_host>",
                    port: parseInt("<proxy_port>")
                },
                bypassList: ["localhost"]
            }
        };
    
        chrome.proxy.settings.set({
            value: config,
            scope: "regular"
        }, function() {});
    
        function callbackFn(details) {
            return {
                authCredentials: {
                    username: "<proxy_username>",
                    password: "<proxy_password>"
                }
            };
        }
    
        chrome.webRequest.onAuthRequired.addListener(
            callbackFn, {
                urls: ["<all_urls>"]
            },
            ['blocking']
        );
        """

        manifest = manifest_json
        js = background_js
        js = js.replace("<proxy_host>", proxy_host)
        js = js.replace("<proxy_port>", str(proxy_port))
        js = js.replace("<proxy_username>", proxy_user)
        js = js.replace("<proxy_password>", proxy_pass)

        manifest = manifest.replace("<ext_name>", 'Chrome Proxy')
        manifest = manifest.replace("<ext_ver>", '1.0.0')

        manifest_path = os.path.join(extension_path, "manifest.json")
        background_path = os.path.join(extension_path, "background.js")

        await aiofiles.os.makedirs(extension_path, exist_ok=True)

        async with aiofiles.open(manifest_path, mode="w") as manifest_file:
            await manifest_file.write(manifest)

        async with aiofiles.open(background_path, mode="w") as background_file:
            await background_file.write(js)

        return extension_path

    @classmethod
    async def aget_proxy(cls, proxy: str):
        extension_filename = f'{hashlib.md5(proxy.encode()).hexdigest()}'
        files = await aiofiles.os.listdir('proxy_extensions')
        files = [f for f in files if await aiofiles.os.path.isfile(os.path.join('proxy_extensions', f)) if extension_filename in f]
        if not files:
            await cls.create_extension(proxy)

        extension_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), f'proxy_extensions/{extension_filename}')
        return extension_path



async def main():
    client = Zefoy('194.71.107.64:10197:modeler_gdSGv9:xyXfKa8Xe8gg')
    await client.login()

    try: await client.use_service('Comments Hearts', 'https://www.tiktok.com/@flowsideee/video/7376686071742074129', '7383771955814417158')
    except Exception as e:
        print('await client.use_service', type(e), '|', e)
    await client.client.aclose()

    # {'Followers': 'c2VuZF9mb2xsb3dlcnNfdGlrdG9r', 'Hearts': 'c2VuZE9nb2xsb3dlcnNfdGlrdG9r', 'Comments Hearts': 'c2VuZC9mb2xsb3dlcnNfdGlrdG9r', 'Views': 'c2VuZC9mb2xeb3dlcnNfdGlrdG9V', 'Shares': 'c2VuZC9mb2xsb3dlcnNfdGlrdG9s', 'Favorites': 'c2VuZF9mb2xsb3dlcnNfdGlrdG9L', 'Live Stream [VS+LIKES]': 'c2VuZC9mb2xsb3dlcnNfdGlrdGLL'}



if __name__ == '__main__':
    asyncio.run(main())