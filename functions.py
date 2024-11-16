import asyncio
import logging
import random
import re
import time

import httpx

from config import BOT_TOKEN
from database import Database as db
from zefoy import Zefoy


async def parse_proxy(proxy_list: list[str]) -> list[str]:
    """Парсит и приводит прокси к единому формату."""
    parsed_proxies = []
    for proxy in proxy_list:
        proxy = proxy.strip()
        if not proxy:
            continue

        # Формат: user:pass@domain:port
        match = re.match(r'(\w+):(\w+)@([a-zA-Z0-9.-]+):(\d+)', proxy)
        if match:
            user, password, domain, port = match.groups()
            parsed_proxies.append(f"{domain}:{port}:{user}:{password}")
            continue

        # Формат: ip:port:user:pass
        match = re.match(r'([\d.]+):(\d+):(\w+):(\w+)', proxy)
        if match:
            ip, port, user, password = match.groups()
            parsed_proxies.append(f"{ip}:{port}:{user}:{password}")
            continue

        # Формат: domain:port:user:pass
        match = re.match(r'([a-zA-Z0-9.-]+):(\d+):(\w+):(\w+)', proxy)
        if match:
            domain, port, user, password = match.groups()
            parsed_proxies.append(f"{domain}:{port}:{user}:{password}")
            continue

        # Формат: ip:port
        match = re.match(r'([\d.]+):(\d+)', proxy)
        if match:
            ip, port = match.groups()
            parsed_proxies.append(f"{ip}:{port}")
            continue

        # Формат: domain:port
        match = re.match(r'([a-zA-Z0-9.-]+):(\d+)', proxy)
        if match:
            domain, port = match.groups()
            parsed_proxies.append(f"{domain}:{port}")

    return parsed_proxies


async def notify(user_id: int, text: str):
    async with httpx.AsyncClient() as client:
        response = await client.get(f'https://api.telegram.org/bot{BOT_TOKEN}/sendMessage', params={"chat_id": user_id, "text": text, "parse_mode": "HTML"})
        if response.status_code != 200:
            logging.warning(f'Ошибка при уведомлении пользователя ({response.status_code}): {response.json()}')

async def run_tasks():
    for task in await db.get_task(for_start=True):
        asyncio.get_event_loop().create_task(run_task(task['id']))
        await asyncio.sleep(10)

async def run_task(task_id: int):
    task = await db.get_task(task_id)
    print('running_task', task)
    if task['status'] == 'created':
        await db.update_task(task_id, status='in_progress')
    elif task['status'] == 'completed':
        return await notify(task['user_id'], f'<b>🔔 Уведомление о задаче</b>\nID задачи:  <code>{task["id"]}</code>\n\n<i>Задача успешно выполнена</i>')
    elif task['status'] == 'error':
        return await notify(task['user_id'], f'<b>🔔 Уведомление о задаче</b>\nID задачи:  <code>{task["id"]}</code>\n\n<i>Задача завершена с ошибкой</i>')

    await run_zefoy_comments(task['id'])

async def run_zefoy_comments(task_id: int, retry: int = 0):
    task = await db.get_task(task_id)
    proxies = task['proxy'].split(',')
    zefoy_client = Zefoy(proxy=random.choice(proxies))
    await zefoy_client.login()
    last_ts = int(time.time())
    while True:
        task = await db.get_task(task_id)
        ttl = task['task_ttl'] - task['already_completed_minutes']
        print('zzz', task['task_ttl'], task['already_completed_minutes'], ttl)
        if ttl <= 0:
            logging.info(f'Task {task_id} finished success')
            await notify(task['user_id'], f'<b>🔔 Уведомление о задаче</b>\nID задачи:  <code>{task["id"]}</code>\n\n<i>Задача успешно завершена</i>')
            return await db.update_task(task_id, status='error')
        try:
            future = asyncio.get_event_loop().create_task(zefoy_client.use_service('Comments Hearts', task['video_url'], task['comment_id'], ttl=ttl*60))
            while True:
                await asyncio.sleep(1)
                if int(time.time()) - last_ts >= 60:
                    last_ts = int(time.time())
                    task = await db.update_task(task_id, already_completed_minutes=1)
                    print('VVV', task['task_ttl'], task['already_completed_minutes'], task['task_ttl'] - task['already_completed_minutes'])
                    if task['already_completed_minutes'] >= task['task_ttl']:
                        logging.info(f'Task {task_id} finished success')
                        future.cancel()
                        await notify(task['user_id'], f'<b>🔔 Уведомление о задаче</b>\nID задачи:  <code>{task["id"]}</code>\n\n<i>Задача успешно завершена</i>')
                        return await db.update_task(task_id, status='error')
                if not future.done():
                    continue
                if future.done():
                    result = future.result()
                    if result == False:
                        if retry > 5:
                            logging.info(f'Task {task_id} finished with error')
                            await notify(task['user_id'], f'<b>🔔 Уведомление о задаче</b>\nID задачи:  <code>{task["id"]}</code>\n\n<i>Задача завершена с ошибкой</i>')
                            return await db.update_task(task_id, status='error')
                        retry += 1
                    elif result == 'No an comment found':
                        logging.info(f'Task {task_id} finished with error (No comment found)')
                        await notify(task['user_id'], f'<b>🔔 Уведомление о задаче</b>\nID задачи:  <code>{task["id"]}</code>\n\n<i>Задача завершена с ошибкой, ошибка: Комментарий не найден</i>')
                        return await db.update_task(task_id, status='error')
                    continue
                break
        # except httpx.RemoteProtocolError:
        #     ...
        # except httpx.TimeoutException:
        #     ...
        except Exception as e:
            logging.error(f"Ошибка в run_zefoy_comments({type(e)}): {e}")
        await asyncio.sleep(10)




if __name__ == '__main__':
    print(asyncio.run(parse_proxy([
    '192.168.1.1:8080',
    'priv-resi.enigmaproxy.net:12321:bhca01efho:xwtzgchwfy_country-us',
    '192.168.1.2:9090:user:pass',
    'priv-resi.enigmaproxy.net:12321:user:pass',
    '''212.103.125.48:1080:asd:zxc''',
    'zxc:124:asd:asd',
    'zzz:0'
]
)))