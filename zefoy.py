import asyncio, random, httpx, base64, re
import time

from PIL import Image
from io import BytesIO
from urllib.parse import urlparse, unquote

class Zefoy:
    def __init__(self, proxy: str = None):
        self.base_url = 'https://zefoy.com'
        self.service_url = f'{self.base_url}'
        self.proxy = proxy if len(proxy.split(':')) == 2 or '@' in proxy else f"{proxy.split(':')[2]}:{proxy.split(':')[3]}@{proxy.split(':')[0]}:{proxy.split(':')[1]}"
        if self.proxy: self.client = httpx.AsyncClient(proxies={'http://': f'http://{self.proxy}', 'https://': f'http://{self.proxy}'}, timeout=120)
        else: self.client = httpx.AsyncClient(timeout=120)
        self.aclient = httpx.AsyncClient(timeout=120)
        self.captcha = {}
        self.captcha_token = None
        self.video_key = None
        self.services = {}
        self.services_ids = {}
        self.services_status = {}
        self.video_info = None

    async def login(self, retry: int = 0):
        if retry >= 5: print(f'[+] Logging in. Retry №{retry+1}')
        if self.proxy: self.client = httpx.AsyncClient(proxies={'http://': f'http://{self.proxy}', 'https://': f'http://{self.proxy}'}, timeout=120)
        else: self.client = httpx.AsyncClient(timeout=120)
        try:
            for x in range(3):
                await self.client.get(f'https://google.com')
                break
        except:
            print(f'Invalid proxy: {self.proxy}')
            self.client = httpx.AsyncClient(timeout=120)

        captcha = await self.get_captcha()
        if not captcha: return
        solve = await self.solve_captcha(captcha)
        authed = await self.send_captcha(solve)
        if not authed:
            return await self.login(retry+1)

    async def solve_captcha(self, image_obj: BytesIO, delete_tag: list = ['\n','\r']):
        # print('[+] Solving captcha...')
        req = (await self.aclient.post("https://plowsidecaptcha.pythonanywhere.com/captcha", files={"file": ("captcha.png", image_obj, "image/png")})).json()
        solved_text = req['captcha_text']
        for x in delete_tag: solved_text = solved_text.replace(x,'')
        return solved_text

    async def get_captcha(self):
        resp = await self.client.get(self.base_url, headers = {'Host': 'zefoy.com', 'Sec-Ch-Ua': '"Not?A_Brand";v="99", "Chromium";v="130"', 'Sec-Ch-Ua-Mobile': '?0', 'Sec-Ch-Ua-Platform': '"Windows"', 'Accept-Language': 'ru-RU,ru;q=0.9', 'Upgrade-Insecure-Requests': '1', 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.6723.70 Safari/537.36', 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7', 'Sec-Fetch-Site': 'none', 'Sec-Fetch-Mode': 'navigate', 'Sec-Fetch-User': '?1', 'Sec-Fetch-Dest': 'document', 'Priority': 'u=0, i', 'Connection': 'keep-alive'})
        if 'Enter Video URL' in resp.text: # Already authed
            self.video_key = resp.text.split('" placeholder="Enter Video URL"')[0].split('name="')[-1]
            return None
        elif '<title>Just a moment...</title>' in resp.text: # 403
            print('[-] Cloudflare')
            return False

        try:
            for x in re.findall(r'<input type="hidden" name="(.*)" value="(.*)">', resp.text): self.captcha[x[0]] = x[1]
            self.captcha_token = resp.text.split('type="text" name="')[1].split('" oninput="this.value=this.value.toLowerCase()"')[0]
            captcha_url = resp.text.split('<img src="')[1].split('" onerror="imgOnError()" class="')[0].replace('amp;', '')
            req = await self.client.get(f"{self.base_url}/{captcha_url}", headers = {'Host': 'zefoy.com', 'Cache-Control': 'max-age=0', 'Sec-Ch-Ua': '"Not?A_Brand";v="99", "Chromium";v="130"', 'Sec-Ch-Ua-Mobile': '?0', 'Sec-Ch-Ua-Platform': '"Windows"', 'Accept-Language': 'ru-RU,ru;q=0.9', 'Origin': 'null', 'Content-Type': 'application/x-www-form-urlencoded', 'Upgrade-Insecure-Requests': '1', 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.6723.70 Safari/537.36', 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7', 'Sec-Fetch-Site': 'same-origin', 'Sec-Fetch-Mode': 'navigate', 'Sec-Fetch-User': '?1', 'Sec-Fetch-Dest': 'document', 'Priority': 'u=0, i'})
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
        resp = await self.client.post(self.base_url, data={self.captcha_token: solve}, headers={'Host': 'zefoy.com','Cache-Control': 'max-age=0','Sec-Ch-Ua': '"Not?A_Brand";v="99", "Chromium";v="130"','Sec-Ch-Ua-Mobile': '?0','Sec-Ch-Ua-Platform': '"Windows"','Accept-Language': 'ru-RU,ru;q=0.9','Origin': 'null','Content-Type': 'application/x-www-form-urlencoded','Upgrade-Insecure-Requests': '1','User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.6723.70 Safari/537.36','Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7','Sec-Fetch-Site': 'same-origin','Sec-Fetch-Mode': 'navigate','Sec-Fetch-User': '?1','Sec-Fetch-Dest': 'document','Priority': 'u=0, i'})
        if 'Enter Video URL' in resp.text:
            self.video_key = resp.text.split('" placeholder="Enter Video URL"')[0].split('name="')[-1]
            await self.get_services(resp.text)
            self.client.cookies.set("user_agent", "Mozilla%2F5.0%20(Windows%20NT%2010.0%3B%20Win64%3B%20x64)%20AppleWebKit%2F537.36%20(KHTML%2C%20like%20Gecko)%20Chrome%2F130.0.6723.70%20Safari%2F537.36", 'zefoy.com')
            self.client.cookies.set("window_size", "1589x917", 'zefoy.com')
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
            if self.video_info is None:

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
        resp = await self.client.post(self.service_url, files={self.video_key: (None, url)}, headers={'Host': 'zefoy.com','Sec-Ch-Ua-Platform': '"Windows"','Accept-Language': 'ru-RU,ru;q=0.9','Sec-Ch-Ua': '"Not?A_Brand";v="99", "Chromium";v="130"','Sec-Ch-Ua-Mobile': '?0','X-Requested-With': 'XMLHttpRequest','User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.6723.70 Safari/537.36','Accept': '*/*','Origin': 'https://zefoy.com','Sec-Fetch-Site': 'same-origin','Sec-Fetch-Mode': 'cors','Sec-Fetch-Dest': 'empty','Priority': 'u=1, i'})

        resp = self.get_payload(resp.text)
        if 'Session expired. Please re-login' in resp:
            print('[-] Session expired')
            await self.login()
            return await self.get_video(url)
        elif 'service is currently not working' in resp:
            print('[-] Service is currently not working')
        elif 'onsubmit="showHideElements' in resp:
            self.video_info = [
                resp.split('" name="')[1].split('"')[0],
                resp.split('value="')[1].split('"')[0]
            ]
        elif 'Checking Timer...' in resp or 'The server is too busy. Please try again in' in resp:
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
            return await self.get_video(url)
        elif 'Too many requests. Please slow' in resp:
            print('[-] Too many requests')
            await asyncio.sleep(2)
            return await self.get_video(url)
        elif 'No an comment found' in resp:
            return 'No an comment found'
        else:
            print('[+] Video_resp', resp)
        return resp

    async def send_service(self, service: str, comment_id: str = None, retry: int = 0):
        print(f'[+] Sending service {service}...')
        resp = await self.client.post(self.service_url, files={self.video_info[0]: (None, self.video_info[1])}, headers={'Host': 'zefoy.com','Sec-Ch-Ua-Platform': '"Windows"','Accept-Language': 'ru-RU,ru;q=0.9','Sec-Ch-Ua': '"Not?A_Brand";v="99", "Chromium";v="130"','Sec-Ch-Ua-Mobile': '?0','X-Requested-With': 'XMLHttpRequest','User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.6723.70 Safari/537.36','Accept': '*/*','Origin': 'https://zefoy.com','Sec-Fetch-Site': 'same-origin','Sec-Fetch-Mode': 'cors','Sec-Fetch-Dest': 'empty','Priority': 'u=1, i'})
        resp = self.get_payload(resp.text)

        if service == 'Comments Hearts':
            v = re.search(r'<i class="text-red fa fa-heart"><\/i><\/div>\n<input type="hidden" name="([^"]+)".*\n<input type="hidden" name="([^"]+)"', resp)
            if not v:
                await asyncio.sleep(3)
                return await self.send_service(service, comment_id, retry+1)

            resp = await self.client.post(self.service_url, files={v.group(1): (None, comment_id), v.group(2): (None, self.video_info[1])}, headers={'Host': 'zefoy.com','Sec-Ch-Ua-Platform': '"Windows"','Accept-Language': 'ru-RU,ru;q=0.9','Sec-Ch-Ua': '"Not?A_Brand";v="99", "Chromium";v="130"','Sec-Ch-Ua-Mobile': '?0','X-Requested-With': 'XMLHttpRequest','User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.6723.70 Safari/537.36','Accept': '*/*','Origin': 'https://zefoy.com','Sec-Fetch-Site': 'same-origin','Sec-Fetch-Mode': 'cors','Sec-Fetch-Dest': 'empty','Priority': 'u=1, i'})
            resp = self.get_payload(resp.text)

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
        elif 'Please try again later. Server too busy' in self.video_info:(
            print('[-] Error on submit: Please try again later. Server too busy.'))
        else:
            if "sans-serif;text-align:center;color:green;'>" in resp:
                print('[+] send_service', resp.split("sans-serif;text-align:center;color:green;'>")[1].split("</")[0].strip())
            else:
                print('[+] send_service', resp)


    def get_payload(self, payload: str, is_encrypt: bool = False):
        if is_encrypt:
            return payload
        else:
            return base64.b64decode(unquote(payload.encode()[::-1])).decode()




async def main():
    client = Zefoy('bhca01efho:xwtzgchwfy_country-us@priv-resi.enigmaproxy.net:12321')
    print((await client.client.get('https://eth0.me')).text)
    # {'Followers': 'c2VuZF9mb2xsb3dlcnNfdGlrdG9r', 'Hearts': 'c2VuZE9nb2xsb3dlcnNfdGlrdG9r', 'Comments Hearts': 'c2VuZC9mb2xsb3dlcnNfdGlrdG9r', 'Views': 'c2VuZC9mb2xeb3dlcnNfdGlrdG9V', 'Shares': 'c2VuZC9mb2xsb3dlcnNfdGlrdG9s', 'Favorites': 'c2VuZF9mb2xsb3dlcnNfdGlrdG9L', 'Live Stream [VS+LIKES]': 'c2VuZC9mb2xsb3dlcnNfdGlrdGLL'}
    # {'Followers': 'c2VuZF9mb2xsb3dlcnNfdGlrdG9r', 'Hearts': 'c2VuZE9nb2xsb3dlcnNfdGlrdG9r', 'Comments Hearts': 'c2VuZC9mb2xsb3dlcnNfdGlrdG9r', 'Views': 'c2VuZC9mb2xeb3dlcnNfdGlrdG9V', 'Shares': 'c2VuZC9mb2xsb3dlcnNfdGlrdG9s', 'Favorites': 'c2VuZF9mb2xsb3dlcnNfdGlrdG9L', 'Live Stream [VS+LIKES]': 'c2VuZC9mb2xsb3dlcnNfdGlrdGLL'}
    await client.login()
    # await client.use_service('Views', 'https://vt.tiktok.com/ZSjB6EknW')
    await client.use_service('Comments Hearts', 'https://vt.tiktok.com/ZSjB6EknW', '7376686389230699265')
    await client.client.aclose()



if __name__ == '__main__':
    asyncio.run(main())