import requests
from zefoy import *

ses = requests.session()
ses.proxies = {'http': 'http://modeler_gdSGv9:xyXfKa8Xe8gg@194.71.107.64:10197', 'https': 'http://modeler_gdSGv9:xyXfKa8Xe8gg@194.71.107.64:10197'}
# cookies = {
#     'cf_clearance': 'JobEU.JRENA0FVPHzlJQs7R52pAc7JqRrYiiUpuc20Y-1732953375-1.2.1.1-CznvT0D32oNBRZAwu3uB9YOezWg33nf5V4J.KhBUsyNbTPGJgvl9F2RqikL6HEf67B0Yan5I_OZbbQs2DVl7zLKwtTr5lyAKiRALpLXpUdI6V5DNssWI14pFlEi3_y5xg0TusuXqOKYYcJNCTB6KSnN8ZibD1zOjMFPrsi3Kw2DdqPrcTZtT8t3Na37ox84uyg_cllrmZHk2zmEtWXVOCfe5NN.w82hhayhiU50sUUs3n0tfgWEa0wcicTvj4OMzEy5q.RcdrjyREUwdi5vUd1yZfE1taCOgSAAseDf1CPy3jwFCHRUL9TA41asV33ksiLBX81eHA48Ck8B4WZh14cKKkCW_UtcGaGYmoPrBasYVC_aZ7vm4acUeQGrYF7pFKJ8_k5EhxYZO9ry8ykl.JRZPnWYHZm745r6fF_Y39nrLYMZKQZKr8L4a1o5jRihB',
# }
#
# headers = {'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7','accept-language': 'ru,en-US;q=0.9,en;q=0.8,ru-RU;q=0.7','cache-control': 'no-cache','pragma': 'no-cache','priority': 'u=0, i','sec-ch-ua': '"Google Chrome";v="131", "Chromium";v="131", "Not_A Brand";v="24"','sec-ch-ua-arch': '"x86"','sec-ch-ua-bitness': '"64"','sec-ch-ua-full-version': '"131.0.6778.86"','sec-ch-ua-full-version-list': '"Google Chrome";v="131.0.6778.86", "Chromium";v="131.0.6778.86", "Not_A Brand";v="24.0.0.0"','sec-ch-ua-mobile': '?0','sec-ch-ua-model': '""','sec-ch-ua-platform': '"Windows"','sec-ch-ua-platform-version': '"15.0.0"','sec-fetch-dest': 'document','sec-fetch-mode': 'navigate','sec-fetch-site': 'same-origin','sec-fetch-user': '?1','upgrade-insecure-requests': '1','user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36'}
# # GET MAIN PAGE
# req = ses.get('https://zefoy.com/', cookies=cookies, headers=headers)
# exit(req)
if False:
    cookies = {
        '__cf_bm': '9pFd1hPtHOoVNJwaW9ZY2pXBnAL2qTdc8jfosCrV2So-1732952378-1.0.1.1-G1FKge3bM8VFoBG0wlYO62i0Jko8k09K0BiHL872lRQZ1rfSVRk3USUpM1NQzSlcxA2Ze.xIi5DMFhsWqqapVA',
        'cf_clearance': 'vJ5mFt1DcXCa5ecS9fZKfe84HVIiIW4YyZ56y2SH9MQ-1732952378-1.2.1.1-5IjKlfFkl_tM6VISJ2EY17qWSGKtwmwUTv3AIRmMDQhmZwQEQDdXykBVXN069RCrgra2MuGL0calov3mMVc5X2bd8zvaXWbbZe9NNYxEGPnQyB279YGrlcc5BDYIDhuqHAF57ZNkZRmUNGYNYW9KzR0AQFV3wVq2dFeVdZjn_6k_BvOTxhi.wUsvAaMGU8mC6Cj4nCrgBlhUu2wYeGIENnc1kTh47GN.MsaGajojgIi6FH3SD7yz8qJ8UM2QYzQ55uRJeJzi5YH96SfPwJNRLgCDP3tS.gyXwuD_sbTUTUC8xdivj2FXhd5alJpa3S51ZLOmGmaOGXfzJB353hzmzi_wLIdNZx5hURdKM3AN__.QDRnaxBDnAy4A4srWvrM3OeUlvrcfaYigGl5hKbiC3loXWiEY60ZfLXr7dU16Qgu3C975_FvnKejtnjVgUSY_',
        'PHPSESSID': 'k9k05qno0ipthr3msn1eq1a8d0',
        'window_size': '1920x911',
        'user_agent': 'Mozilla%2F5.0%20(Windows%20NT%2010.0%3B%20Win64%3B%20x64)%20AppleWebKit%2F537.36%20(KHTML%2C%20like%20Gecko)%20Chrome%2F123.0.0.0%20Safari%2F537.36',
        'language': 'de-AT',
        'languages': 'de-AT,de,en-US,en',
        'time_zone': 'Europe/Vienna',
        '_ga': 'GA1.1.1438765437.1732952387',
        'FCCDCF': '%5Bnull%2Cnull%2Cnull%2C%5B%22CQI51cAQI51cAEsACBENBSFoAP_gAAAAAAYgINJD7C7FbSFCwH5zaLsAMAhXRsAAQoQAAASBAmABQAKQIAQCkkAQFASgBAACAAAAICRBIQIECAAAAUAAQAAAAAAEAAAAAAAIIAAAgAEAAAAIAAACAIAAEAAIAAAAEAAAmQgAAIIACAAAgAAAIAAAAAAAAAAAAgCAAAAAAAAAAAAAAAAAAQAAADBIDAACwAKgAcABAADIAGgAPAAiABMACqAH4AQkAiACJAGAAMMAZQA9gB-gGKAOIApEBTYC8wGTjoEAACwAKgAcABAADIAGgAPAAiABMACqAF0AMQAfoBEAESAJwAUYAwABhgDKAGiAPYAfoBFgDFAHEAOoAi8BTYC8wF9AMnAaqQgEgALACqAGIAYABigDqAKbAZOA1UlAQAAWABwAHgARAAmABVADFAIgAiQBRgDAAMUAdQBF4CmwF5gMnKQGwAFgAVAA4ACAAGQANAAeABEACYAFIAKoAYgA_QCIAIkAUYAwABlADRAH6ARYAxQB1AEXgKbAXmAvoBk5aAEAMABTYA%22%2C%222~70.89.93.108.122.149.196.236.259.311.313.323.358.415.449.486.494.495.540.574.609.864.981.1029.1048.1051.1095.1097.1126.1205.1276.1301.1365.1415.1449.1514.1570.1577.1598.1651.1716.1735.1753.1765.1870.1878.1889.1958.1960.2072.2253.2299.2373.2415.2506.2526.2531.2568.2571.2575.2624.2677.2778~dv.%22%2C%22314751CB-734F-4647-A986-601778C4F987%22%5D%5D',
        '_ga_1WEXNS5FFP': 'GS1.1.1732952387.1.1.1732952405.0.0.0',
        '__gads': 'ID=255cd0420fc11bfb:T=1732952405:RT=1732952405:S=ALNI_MYHCpaU5hTnBL_xXg1XxRR95Nj5Gg',
        '__gpi': 'UID=00000f5df19e51aa:T=1732952405:RT=1732952405:S=ALNI_Ma1AqBlMiyvoCD5D9p4WA3bg-pNkA',
        '__eoi': 'ID=4e7a6cefd2909fab:T=1732952405:RT=1732952405:S=AA-AfjYHjku2CwYkOw_7_sa0IopX',
        'FCNEC': '%5B%5B%22AKsRol_07VIIrHruLE_3Q6BlVvYljZNfE9yJTgcdANonjmlNqX3DNZqT60-Y5dGZuiBIKwyKUqA9dqs_mzHcnfhRGGPraR5CZgp6erk1xrC0gm-PfAdW3x2lIVeZ571Dk3P47KsWbPCvAYyYiBKv86QvM985HdOvIA%3D%3D%22%5D%5D',
    }

    headers = {'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7','accept-language': 'de-AT,de;q=0.9,en-US;q=0.8,en;q=0.7','cache-control': 'no-cache','pragma': 'no-cache','priority': 'u=0, i','sec-ch-ua': '"Google Chrome";v="123", "Not:A-Brand";v="8", "Chromium";v="123"','sec-ch-ua-arch': '"x86"','sec-ch-ua-bitness': '"64"','sec-ch-ua-full-version': '"123.0.6312.46"','sec-ch-ua-full-version-list': '"Google Chrome";v="123.0.6312.46", "Not:A-Brand";v="8.0.0.0", "Chromium";v="123.0.6312.46"','sec-ch-ua-mobile': '?0','sec-ch-ua-model': '""','sec-ch-ua-platform': '"Windows"','sec-ch-ua-platform-version': '"15.0.0"','sec-fetch-dest': 'document','sec-fetch-mode': 'navigate','sec-fetch-site': 'same-origin','sec-fetch-user': '?1','upgrade-insecure-requests': '1','user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36'}
    # GET MAIN PAGE
    req = ses.get('https://zefoy.com/', cookies=cookies, headers=headers)


    cookies = {
        '__cf_bm': '9pFd1hPtHOoVNJwaW9ZY2pXBnAL2qTdc8jfosCrV2So-1732952378-1.0.1.1-G1FKge3bM8VFoBG0wlYO62i0Jko8k09K0BiHL872lRQZ1rfSVRk3USUpM1NQzSlcxA2Ze.xIi5DMFhsWqqapVA',
        'cf_clearance': 'vJ5mFt1DcXCa5ecS9fZKfe84HVIiIW4YyZ56y2SH9MQ-1732952378-1.2.1.1-5IjKlfFkl_tM6VISJ2EY17qWSGKtwmwUTv3AIRmMDQhmZwQEQDdXykBVXN069RCrgra2MuGL0calov3mMVc5X2bd8zvaXWbbZe9NNYxEGPnQyB279YGrlcc5BDYIDhuqHAF57ZNkZRmUNGYNYW9KzR0AQFV3wVq2dFeVdZjn_6k_BvOTxhi.wUsvAaMGU8mC6Cj4nCrgBlhUu2wYeGIENnc1kTh47GN.MsaGajojgIi6FH3SD7yz8qJ8UM2QYzQ55uRJeJzi5YH96SfPwJNRLgCDP3tS.gyXwuD_sbTUTUC8xdivj2FXhd5alJpa3S51ZLOmGmaOGXfzJB353hzmzi_wLIdNZx5hURdKM3AN__.QDRnaxBDnAy4A4srWvrM3OeUlvrcfaYigGl5hKbiC3loXWiEY60ZfLXr7dU16Qgu3C975_FvnKejtnjVgUSY_',
        'PHPSESSID': 'k9k05qno0ipthr3msn1eq1a8d0',
        'window_size': '1920x911',
        'user_agent': 'Mozilla%2F5.0%20(Windows%20NT%2010.0%3B%20Win64%3B%20x64)%20AppleWebKit%2F537.36%20(KHTML%2C%20like%20Gecko)%20Chrome%2F123.0.0.0%20Safari%2F537.36',
        'language': 'de-AT',
        'languages': 'de-AT,de,en-US,en',
        'time_zone': 'Europe/Vienna',
        '_ga': 'GA1.1.1438765437.1732952387',
        'FCCDCF': '%5Bnull%2Cnull%2Cnull%2C%5B%22CQI51cAQI51cAEsACBENBSFoAP_gAAAAAAYgINJD7C7FbSFCwH5zaLsAMAhXRsAAQoQAAASBAmABQAKQIAQCkkAQFASgBAACAAAAICRBIQIECAAAAUAAQAAAAAAEAAAAAAAIIAAAgAEAAAAIAAACAIAAEAAIAAAAEAAAmQgAAIIACAAAgAAAIAAAAAAAAAAAAgCAAAAAAAAAAAAAAAAAAQAAADBIDAACwAKgAcABAADIAGgAPAAiABMACqAH4AQkAiACJAGAAMMAZQA9gB-gGKAOIApEBTYC8wGTjoEAACwAKgAcABAADIAGgAPAAiABMACqAF0AMQAfoBEAESAJwAUYAwABhgDKAGiAPYAfoBFgDFAHEAOoAi8BTYC8wF9AMnAaqQgEgALACqAGIAYABigDqAKbAZOA1UlAQAAWABwAHgARAAmABVADFAIgAiQBRgDAAMUAdQBF4CmwF5gMnKQGwAFgAVAA4ACAAGQANAAeABEACYAFIAKoAYgA_QCIAIkAUYAwABlADRAH6ARYAxQB1AEXgKbAXmAvoBk5aAEAMABTYA%22%2C%222~70.89.93.108.122.149.196.236.259.311.313.323.358.415.449.486.494.495.540.574.609.864.981.1029.1048.1051.1095.1097.1126.1205.1276.1301.1365.1415.1449.1514.1570.1577.1598.1651.1716.1735.1753.1765.1870.1878.1889.1958.1960.2072.2253.2299.2373.2415.2506.2526.2531.2568.2571.2575.2624.2677.2778~dv.%22%2C%22314751CB-734F-4647-A986-601778C4F987%22%5D%5D',
        '__gads': 'ID=255cd0420fc11bfb:T=1732952405:RT=1732952405:S=ALNI_MYHCpaU5hTnBL_xXg1XxRR95Nj5Gg',
        '__gpi': 'UID=00000f5df19e51aa:T=1732952405:RT=1732952405:S=ALNI_Ma1AqBlMiyvoCD5D9p4WA3bg-pNkA',
        '__eoi': 'ID=4e7a6cefd2909fab:T=1732952405:RT=1732952405:S=AA-AfjYHjku2CwYkOw_7_sa0IopX',
        '_ga_1WEXNS5FFP': 'GS1.1.1732952387.1.1.1732952583.0.0.0',
        'FCNEC': '%5B%5B%22AKsRol8OVIJy1Szs6Ezh0DLTk52fK4WleEHCEG6LERnEv5cpjpXojpZ7-bsws8BKiRRH2lGGwziL6RRYzCcstnAKKtsdBgWnYW0MYazXlhkvlilzedsIYkH2jiS0OehhxLCDf4cfxr3BAK_1osER3YN5t44mtvNoyw%3D%3D%22%5D%5D',
    }

    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'accept-language': 'de-AT,de;q=0.9,en-US;q=0.8,en;q=0.7',
        'cache-control': 'max-age=0',
        'content-type': 'application/x-www-form-urlencoded',
        'origin': 'null',
        'priority': 'u=0, i',
        'sec-ch-ua': '"Google Chrome";v="123", "Not:A-Brand";v="8", "Chromium";v="123"',
        'sec-ch-ua-arch': '"x86"',
        'sec-ch-ua-bitness': '"64"',
        'sec-ch-ua-full-version': '"123.0.6312.46"',
        'sec-ch-ua-full-version-list': '"Google Chrome";v="123.0.6312.46", "Not:A-Brand";v="8.0.0.0", "Chromium";v="123.0.6312.46"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-model': '""',
        'sec-ch-ua-platform': '"Windows"',
        'sec-ch-ua-platform-version': '"15.0.0"',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36',
    }

    data = {
        '726b026e91ef543c3': 'go',
    }
    # SEND CAPTCHA
    req = ses.post('https://zefoy.com/', cookies=cookies, headers=headers, data=data)


cookies = {
    'cf_clearance': 'JobEU.JRENA0FVPHzlJQs7R52pAc7JqRrYiiUpuc20Y-1732953375-1.2.1.1-CznvT0D32oNBRZAwu3uB9YOezWg33nf5V4J.KhBUsyNbTPGJgvl9F2RqikL6HEf67B0Yan5I_OZbbQs2DVl7zLKwtTr5lyAKiRALpLXpUdI6V5DNssWI14pFlEi3_y5xg0TusuXqOKYYcJNCTB6KSnN8ZibD1zOjMFPrsi3Kw2DdqPrcTZtT8t3Na37ox84uyg_cllrmZHk2zmEtWXVOCfe5NN.w82hhayhiU50sUUs3n0tfgWEa0wcicTvj4OMzEy5q.RcdrjyREUwdi5vUd1yZfE1taCOgSAAseDf1CPy3jwFCHRUL9TA41asV33ksiLBX81eHA48Ck8B4WZh14cKKkCW_UtcGaGYmoPrBasYVC_aZ7vm4acUeQGrYF7pFKJ8_k5EhxYZO9ry8ykl.JRZPnWYHZm745r6fF_Y39nrLYMZKQZKr8L4a1o5jRihB',
    'PHPSESSID': 'k9k05qno0ipthr3msn1eq1a8d0',
}

user_agents = [
    'Mozilla%2F5.0%20(Windows%20NT%2010.0%3B%20Win64%3B%20x64)%20AppleWebKit%2F537.36%20(KHTML%2C%20like%20Gecko)%20Chrome%2F123.0.0.0%20Safari%2F537.36'
]
# import random
ses.cookies.set("user_agent", random.choice(user_agents))
ses.cookies.set("window_size", f"{random.randint(1911, 1920)}x{random.choice((900, 911, 940, 1000))}")
ses.cookies.set("language", "de-AT")
ses.cookies.set("languages", "de-AT,de,en-US,en")
ses.cookies.set("time_zone", "Europe/Vienna")
headers = {'accept': '*/*','accept-language': 'ru,en-US;q=0.9,en;q=0.8,ru-RU;q=0.7','cache-control': 'no-cache','origin': 'https://zefoy.com','pragma': 'no-cache','priority': 'u=1, i','sec-ch-ua': '"Google Chrome";v="131", "Chromium";v="131", "Not_A Brand";v="24"','sec-ch-ua-arch': '"x86"','sec-ch-ua-bitness': '"64"','sec-ch-ua-full-version': '"131.0.6778.86"','sec-ch-ua-full-version-list': '"Google Chrome";v="131.0.6778.86", "Chromium";v="131.0.6778.86", "Not_A Brand";v="24.0.0.0"','sec-ch-ua-mobile': '?0','sec-ch-ua-model': '""','sec-ch-ua-platform': '"Windows"','sec-ch-ua-platform-version': '"15.0.0"','sec-fetch-dest': 'empty','sec-fetch-mode': 'cors','sec-fetch-site': 'same-origin','user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36','x-requested-with': 'XMLHttpRequest'}#{'accept': '*/*','accept-language': 'de-AT,de;q=0.9,en-US;q=0.8,en;q=0.7','origin': 'https://zefoy.com','priority': 'u=1, i','sec-ch-ua': '"Google Chrome";v="123", "Not:A-Brand";v="8", "Chromium";v="123"','sec-ch-ua-arch': '"x86"','sec-ch-ua-bitness': '"64"','sec-ch-ua-full-version': '"123.0.6312.46"','sec-ch-ua-full-version-list': '"Google Chrome";v="123.0.6312.46", "Not:A-Brand";v="8.0.0.0", "Chromium";v="123.0.6312.46"','sec-ch-ua-mobile': '?0','sec-ch-ua-model': '""','sec-ch-ua-platform': '"Windows"','sec-ch-ua-platform-version': '"15.0.0"','sec-fetch-dest': 'empty','sec-fetch-mode': 'cors','sec-fetch-site': 'same-origin','user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36','x-requested-with': 'XMLHttpRequest'}

files = {
    'acd6b83393984716e3': (None, 'https://www.tiktok.com/@natallya.lis/video/7442610929977609527'),
}
z = Zefoy()
# GET VIDEO
req = ses.post('https://zefoy.com/c2VuZC9mb2xsb3dlcnNfdGlrdG9r', cookies=cookies, headers=headers, files=files)
# print(req.text)
print(req)
v = z.get_payload(req.text)
b = v.split('hidden" name="')[1].split('"')[0]








# cookies = {
#     'cf_clearance': 'vJ5mFt1DcXCa5ecS9fZKfe84HVIiIW4YyZ56y2SH9MQ-1732952378-1.2.1.1-5IjKlfFkl_tM6VISJ2EY17qWSGKtwmwUTv3AIRmMDQhmZwQEQDdXykBVXN069RCrgra2MuGL0calov3mMVc5X2bd8zvaXWbbZe9NNYxEGPnQyB279YGrlcc5BDYIDhuqHAF57ZNkZRmUNGYNYW9KzR0AQFV3wVq2dFeVdZjn_6k_BvOTxhi.wUsvAaMGU8mC6Cj4nCrgBlhUu2wYeGIENnc1kTh47GN.MsaGajojgIi6FH3SD7yz8qJ8UM2QYzQ55uRJeJzi5YH96SfPwJNRLgCDP3tS.gyXwuD_sbTUTUC8xdivj2FXhd5alJpa3S51ZLOmGmaOGXfzJB353hzmzi_wLIdNZx5hURdKM3AN__.QDRnaxBDnAy4A4srWvrM3OeUlvrcfaYigGl5hKbiC3loXWiEY60ZfLXr7dU16Qgu3C975_FvnKejtnjVgUSY_',
#     'PHPSESSID': 'k9k05qno0ipthr3msn1eq1a8d0',
#     'window_size': '1920x911',
#     'user_agent': 'Mozilla%2F5.0%20(Windows%20NT%2010.0%3B%20Win64%3B%20x64)%20AppleWebKit%2F537.36%20(KHTML%2C%20like%20Gecko)%20Chrome%2F123.0.0.0%20Safari%2F537.36',
#     'language': 'de-AT',
#     'languages': 'de-AT,de,en-US,en',
#     'time_zone': 'Europe/Vienna',
#     '_ga': 'GA1.1.1438765437.1732952387',
#     'FCCDCF': '%5Bnull%2Cnull%2Cnull%2C%5B%22CQI51cAQI51cAEsACBENBSFoAP_gAAAAAAYgINJD7C7FbSFCwH5zaLsAMAhXRsAAQoQAAASBAmABQAKQIAQCkkAQFASgBAACAAAAICRBIQIECAAAAUAAQAAAAAAEAAAAAAAIIAAAgAEAAAAIAAACAIAAEAAIAAAAEAAAmQgAAIIACAAAgAAAIAAAAAAAAAAAAgCAAAAAAAAAAAAAAAAAAQAAADBIDAACwAKgAcABAADIAGgAPAAiABMACqAH4AQkAiACJAGAAMMAZQA9gB-gGKAOIApEBTYC8wGTjoEAACwAKgAcABAADIAGgAPAAiABMACqAF0AMQAfoBEAESAJwAUYAwABhgDKAGiAPYAfoBFgDFAHEAOoAi8BTYC8wF9AMnAaqQgEgALACqAGIAYABigDqAKbAZOA1UlAQAAWABwAHgARAAmABVADFAIgAiQBRgDAAMUAdQBF4CmwF5gMnKQGwAFgAVAA4ACAAGQANAAeABEACYAFIAKoAYgA_QCIAIkAUYAwABlADRAH6ARYAxQB1AEXgKbAXmAvoBk5aAEAMABTYA%22%2C%222~70.89.93.108.122.149.196.236.259.311.313.323.358.415.449.486.494.495.540.574.609.864.981.1029.1048.1051.1095.1097.1126.1205.1276.1301.1365.1415.1449.1514.1570.1577.1598.1651.1716.1735.1753.1765.1870.1878.1889.1958.1960.2072.2253.2299.2373.2415.2506.2526.2531.2568.2571.2575.2624.2677.2778~dv.%22%2C%22314751CB-734F-4647-A986-601778C4F987%22%5D%5D',
#     '__gads': 'ID=255cd0420fc11bfb:T=1732952405:RT=1732952405:S=ALNI_MYHCpaU5hTnBL_xXg1XxRR95Nj5Gg',
#     '__gpi': 'UID=00000f5df19e51aa:T=1732952405:RT=1732952405:S=ALNI_Ma1AqBlMiyvoCD5D9p4WA3bg-pNkA',
#     '__eoi': 'ID=4e7a6cefd2909fab:T=1732952405:RT=1732952405:S=AA-AfjYHjku2CwYkOw_7_sa0IopX',
#     '_ga_1WEXNS5FFP': 'GS1.1.1732952387.1.1.1732952615.0.0.0',
#     'FCNEC': '%5B%5B%22AKsRol-pZ9FI_mzUIn4GU1NE8GVo1_5ONEiGX4BNpvYYEsreeYzqvomrGp3j-RJMtP3tA1RpRP50OOdqECzYqTK1lKhefuGM1p1d52xMcZXfH5auKgeTB2Sa8I9hrCq5w3D6eKZUMgm0luu71WrCmsLvQ6p0EQCGHw%3D%3D%22%5D%5D',
#     '__cf_bm': 'g7f6egQ2es1UQBmeXPTiVf2dvRJvliODI4oIXrfHDq0-1732954102-1.0.1.1-wwGiioZicjbPFL9oZe2R7K6XDqlqZX39KRSZ5SAqsCxCcWoFptzFgQ3NSlb3.Ospse.M1rB52IHqPC.x7a8F5Q',
# }
#
# headers = {
#     'accept': '*/*',
#     'accept-language': 'de-AT,de;q=0.9,en-US;q=0.8,en;q=0.7',
#     'origin': 'https://zefoy.com',
#     'priority': 'u=1, i',
#     'sec-ch-ua': '"Google Chrome";v="123", "Not:A-Brand";v="8", "Chromium";v="123"',
#     'sec-ch-ua-arch': '"x86"',
#     'sec-ch-ua-bitness': '"64"',
#     'sec-ch-ua-full-version': '"123.0.6312.46"',
#     'sec-ch-ua-full-version-list': '"Google Chrome";v="123.0.6312.46", "Not:A-Brand";v="8.0.0.0", "Chromium";v="123.0.6312.46"',
#     'sec-ch-ua-mobile': '?0',
#     'sec-ch-ua-model': '""',
#     'sec-ch-ua-platform': '"Windows"',
#     'sec-ch-ua-platform-version': '"15.0.0"',
#     'sec-fetch-dest': 'empty',
#     'sec-fetch-mode': 'cors',
#     'sec-fetch-site': 'same-origin',
#     'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36',
#     'x-requested-with': 'XMLHttpRequest',
# }
import re

files = {
    'a370af19bfa22': (None, '7442610929977609527'),
}
req = ses.post('https://zefoy.com/c2VuZC9mb2xsb3dlcnNfdGlrdG9r', cookies=cookies, headers=headers, files=files)
print(req)
v = z.get_payload(req.text)
v2 = re.search(r'<i class="text-red fa fa-heart"><\/i><\/div>\n<input type="hidden" name="([^"]+)".*\n<input type="hidden" name="([^"]+)"', v)

print(v2.group(1),
v2.group(2))
files={
    v2.group(1): (None, comment_id),
    v2.group(2): (None, self.video_info[1]),
    'select_lmt': (None, self.likes_to_send_count)
}

files = {
    'fce172ec8ad38baf': (None, '7442820602912310032'),
    b: (None, '7442610929977609527'),
    '29ac4aa6c6c15471713c4': (None, 'https://www.tiktok.com/@natallya.lis/video/7442610929977609527'),
    'select_lmt': (None, '25'),
}

req = ses.post('https://zefoy.com/c2VuZC9mb2xsb3dlcnNfdGlrdG9r', cookies=cookies, headers=headers, files=files)
print(req.text)
print(req)
print(z.get_payload(req.text))
