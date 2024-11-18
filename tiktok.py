import asyncio, hashlib, base64, httpx, time, re

class TikTok:
    @staticmethod
    async def get_full_tiktok_url(short_url: str) -> str:
        """Получает полную ссылку из короткой ссылки TikTok."""
        async with httpx.AsyncClient() as client:
            response = None
            for x in range(3):
                try:
                    response = await client.get(short_url, headers={'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7', 'accept-language': 'ru,en-US;q=0.9,en;q=0.8,ru-RU;q=0.7', 'priority': 'u=0, i', 'sec-ch-ua': '"Google Chrome";v="131", "Chromium";v="131", "Not_A Brand";v="24"', 'sec-ch-ua-mobile': '?0', 'sec-ch-ua-platform': '"Windows"', 'sec-fetch-dest': 'document', 'sec-fetch-mode': 'navigate', 'sec-fetch-site': 'none', 'sec-fetch-user': '?1', 'upgrade-insecure-requests': '1', 'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36'}, follow_redirects=True)
                    break
                except: continue
            if not response:
                return short_url
            url = str(response.url).split('?')[0]
            return url if 'https://' in url else str(response.url)

    @staticmethod
    def extract_video_id(full_url: str) -> str:
        """Извлекает ID видео из полной ссылки TikTok."""
        match = re.search(r'/(photo|video)/(\d+)', full_url)
        return match.group(2) if match else None

    @classmethod
    async def get_video_comments(cls, aweme_id: int, author_username: str = None, search_text: str = None, search_comment_id: int = None) -> list:
        """
        :param aweme_id: ID видео в тиктоке
        :param search_text: Текст для поиска в комментарии
        :param author_username: Юзернейм автора для поиска
        :return: Список с комментариями
        """
        async with httpx.AsyncClient() as client:
            data = str(aweme_id)
            encoded_data = base64.b64encode(hashlib.sha256(data.encode()).digest()).decode('utf-8')
            count = 50
            retry = 0
            cursor = 0
            result_comments = []
            found_cid = []

            while True:
                ts = str(int(time.time()))
                headers = {
                    'Host': 'api16-normal-useast8.tiktokv.us',
                    'X-Tt-Request-Tag': 'n=0;nr=0',
                    'X-Tt-Pba-Enable': '1',
                    'Check_preload': 'true',
                    'X-Metasec-Event-Source': 'native',
                    'X-Tt-Dm-Status': 'login=0;ct=0;rt=7',
                    'Sdk-Version': '2',
                    'Passport-Sdk-Version': '60310',
                    'X-Vc-Bdturing-Sdk-Version': '2.3.8.i18n',
                    'X-Tt-Store-Region': 'us',
                    'X-Tt-Store-Region-Src': 'did',
                    'User-Agent': 'com.zhiliaoapp.musically/2023607040 (Linux; U; Android 9; ru_RU; OXF-AN10; Build/PQ3A.190605.09291615;tt-ok/3.12.13.4-tiktok)',
                    'X-Ladon': encoded_data,
                    'X-Khronos': ts,
                }
                req = await client.get(
                    f'https://api16-normal-useast8.tiktokv.us/aweme/v2/comment/list/?aweme_id={aweme_id}&cursor={cursor}&count={count}&forward_page_type=1&channel_id=0&user_avatar_shrink=96_96&ad_pricing_type=0&offline_pin_comment=1&author_relation_type=0&load_type=0&scenario=0&enter_from=homepage_hot&is_non_personalized=false&suggest_words&shown_cnt=16394&comment_preload=0&preload=1&net_level=0&perf_score=9.3513&zero_count_expire_time=-1&source=0&device_platform=android&os=android&ssmix=a&_rticket=1728987606928&cdid=38bd80a0-ab4e-492a-90e4-1c8c7e55c9ae&channel=googleplay&aid=1233&app_name=musical_ly&version_code=360704&version_name=36.7.4&manifest_version_code=2023607040&update_version_code=2023607040&ab_version=36.7.4&resolution=1080*1920&dpi=480&device_type=OXF-AN10&device_brand=Honor&language=ru&os_api=28&os_version=9&ac=wifi&is_pad=0&current_region=RU&app_type=normal&sys_region=RU&last_install_time={ts}&mcc_mnc=310004&timezone_name=Asia%2FNovosibirsk&carrier_region_v2=310&residence=US&app_language=ru&carrier_region=US&timezone_offset=25200&host_abi=arm64-v8a&locale=ru-RU&ac2=wifi5g&uoo=1&op_region=US&build_number=36.7.4&region=RU&ts={ts}&iid=7425942719073961774&device_id=7425942296624186926&openudid=3a55a65b1b646f2a',
                    headers=headers
                )
                if req.status_code == 200 and req.text == '':
                    if retry >= 2:
                        print(f'Retry: {retry}')
                    # print('Antifrod')
                    if retry > 50:
                        return []
                    retry += 1
                    continue
                try:
                    comments = [{'id': x.get('cid', None), 'text': x.get('text', None), 'likes_count': x.get('digg_count', 0), 'author': x.get('user', {}).get('unique_id', 'None'), 'nickname': x.get('user', {}).get('nickname', 'None'), 'video_id': aweme_id} for x in req.json()['comments'] if x.get('cid') not in found_cid]
                    if len(comments) == 0:
                        print('finish')
                        break
                    for x in comments:
                        found_cid.append(x['id'])
                    cursor += len(comments)
                    result_comments.extend(comments)
                    if search_comment_id is not None and str(search_comment_id) in found_cid:
                        return [x for x in result_comments if str(x['id']) == str(search_comment_id)]
                    print(f"Parsed comments: {len(result_comments)} | Comments count: {len(comments)} | First-Last comment cid: {comments[0]['id']}-{comments[-1]['id']}")
                    retry = 0
                except Exception as e:
                    print(req, e)
                    print(req.text)

            if search_comment_id is not None:
                return [x for x in result_comments if str(x['id']) == str(search_comment_id)]
            searched_comments = cls.search_comments(result_comments, author_username if author_username is not None else search_text, search_by_text=search_text is not None, search_by_username=author_username is not None)
            return searched_comments

    @staticmethod
    def search_comments(comments: list, text_to_search: str = None, search_by_text: bool = False, search_by_username: bool = False, search_by_comment_id: bool = False) -> list:
        searched_comments = []
        if not search_by_text and not search_by_username:
            return comments
        if search_by_username:
            text_to_search = text_to_search.replace('@', '')

        for comment in comments:
            # text_to_search in f"{comment['video_id']}|{comment['id']}"
            if search_by_text:
                if text_to_search in comment['text'].lower():
                    searched_comments.append(comment)
            elif search_by_username:
                if text_to_search in f"{comment['nickname'].lower()}|{comment['author'].lower()}":
                    searched_comments.append(comment)
            elif search_by_comment_id:
                if text_to_search == str(comment['id']):
                    searched_comments.append(comment)

        return searched_comments


async def main():
    full_url = await TikTok.get_full_tiktok_url('https://vm.tiktok.com/ZMhneJg7k/')
    video_id = TikTok.extract_video_id(full_url)
    print(video_id, full_url)
    comments = await TikTok.get_video_comments(video_id, search_comment_id=7376686389230699265)
    print(len(comments), comments)

if __name__ == '__main__':
    asyncio.run(main())