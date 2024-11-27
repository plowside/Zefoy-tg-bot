import hashlib
import os
import asyncio
import time
import zipfile
import undetected_chromedriver as uc
import aiofiles.os



class SeleniumProxyManager:
    @classmethod
    async def create_extension(cls, proxy: str):
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
    async def get_proxy(cls, proxy: str):
        extension_filename = f'{hashlib.md5(proxy.encode()).hexdigest()}'
        files = await aiofiles.os.listdir('proxy_extensions')
        files = [f for f in files if await aiofiles.os.path.isfile(os.path.join('proxy_extensions', f)) if extension_filename in f]
        if not files:
            await cls.create_extension(proxy)

        extension_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), f'proxy_extensions/{extension_filename}')
        return extension_path

proxy_extension = asyncio.run(SeleniumProxyManager.get_proxy('5213tonystark5213:MDKeQwiY4e@82.211.3.236:50101'))
options = uc.ChromeOptions()
options.add_argument(f'--load-extension={proxy_extension}')
driver = uc.Chrome(options=options)
driver.get("http://eth0.me")
time.sleep(3)
driver.quit()