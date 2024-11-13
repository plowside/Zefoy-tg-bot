import asyncio, logging, aiosqlite
import io
from datetime import datetime

from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, BotCommand, InputFile
from aiogram.utils import executor
from aiogram.dispatcher.filters import BoundFilter
from pyexpat.errors import messages

from config import *
from database import Database as db
from keyboards import *
from functions import *

from tiktok import TikTok
#################################################################################
logging.basicConfig(
    format=u'%(filename)s [LINE:%(lineno)d] #%(levelname)-8s [%(asctime)s]  %(message)s',
    level=logging.INFO
)
logging.getLogger("aiogram").setLevel(logging.INFO)
logging.getLogger("asyncio").setLevel(logging.WARNING)
logging.getLogger("httpx").setLevel(logging.WARNING)

bot = Bot(token=BOT_TOKEN, parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot, storage=MemoryStorage())
#################################################################################

async def init_db():
    """Инициализация базы данных."""
    await db.create_tables()


class CheckUserInDB(BoundFilter):
    key = "is_authed"

    def __init__(self, *args, **kwargs):
       ...

    async def check(self, message: types.Message) -> bool:
        user_id = message.from_user.id
        username = message.from_user.username
        first_name = message.from_user.first_name
        if user_id not in ADMINS:
            return False

        user_in_db = await db.get_user(user_id)
        if not user_in_db:
            await db.create_user(user_id, username, first_name)
        elif user_in_db["username"] != username or user_in_db["first_name"] != first_name:
            await db.update_user(user_id, username, first_name)

        return True

class CreateTask(StatesGroup):
    InputVideoUrl: State = State()
    SelectCommentSearchType: State = State()
    InputSearchText: State = State()
    InputCommentID: State = State()
    InputTaskTTL: State = State()
    InputTaskProxy: State = State()

dp.filters_factory.bind(CheckUserInDB)
################################################################################



@dp.message_handler(commands=['start'], is_authed=True, state='*')
async def cmd_start(message: types.Message):
    """Обработка команды /start."""
    user_id = message.from_user.id
    is_admin = user_id in ADMINS

    await message.answer("Добро пожаловать! Выберите действие:", reply_markup=await kb_menu(is_admin))


@dp.callback_query_handler(text_startswith="user", is_authed=True)
async def handle_user(call: types.CallbackQuery, state: FSMContext):
    await state.finish()
    cd = call.data.split(':')
    user_id = call.from_user.id
    is_admin = user_id in ADMINS

    if cd[1] == 'menu':
        await call.message.edit_text("Добро пожаловать! Выберите действие:", reply_markup=await kb_menu(is_admin))
    elif cd[1] == "task":
        sub_act = cd[2]

        if sub_act == "create":
            await state.set_state(CreateTask.InputVideoUrl)
            await call.message.edit_text("<b>⚙️ Создание задачи</b>\n\n<i>Отправьте ссылку на видео</i>", reply_markup=await kb_back('user:menu'))

        elif sub_act == "my_tasks":
            if len(cd) > 3: page = int(cd[3])
            else: page = 1
            tasks = await db.get_task(user_id=user_id)
            await call.message.edit_text(f"<b>🚀 Мои задачи</b>\n\n<i>Всего задач:  <code>{len(tasks)} шт.</code></i>", reply_markup=await kb_user_tasks(tasks, page))

        elif sub_act == "show":
            page = int(cd[3])
            task_id = int(cd[4])
            task = await db.get_task(task_id=task_id)
            # print('show_task', task)
            await call.message.edit_text(f"<b>ℹ️ Информация о задаче</b>\n\n{STATUS_EMOJI_TRANSLATIONS[task['status']]} ID Задачи: <code>{task['id']}</code>\n├ Ссылка на видео:  <code>{task['video_url']}</code>\n├ ID комментария:  <code>{task['comment_id']}</code>\n├ Время работы:  <code>{task['task_ttl']} минут</code>\n├ Уже выполнено:  <code>{task['already_completed_minutes']} минут</code>\n├ Дата создания:  <code>{datetime.fromtimestamp(task['create_ts']).strftime('%d.%m.%Y %H:%M')}</code>\n└ Статус:  <code>{STATUS_TRANSLATIONS[task['status']]}</code>", reply_markup=await kb_back(f'user:task:my_tasks:{page}'))


@dp.message_handler(state=CreateTask.InputVideoUrl)
async def state_create_task_input_video_url(message: types.Message, state: FSMContext):
    """Ввод ссылки для накрутки"""
    short_url = message.text
    video_url = await TikTok.get_full_tiktok_url(short_url)
    video_id = TikTok.extract_video_id(video_url)

    if not video_id:
        await message.answer(f'<b>❌ Не удалось получить id видео</b>\nВведенная ссылка:  <code>{short_url}</code>\nСсылка для обработки:  <code>{video_url}</code>', reply_markup=await kb_back('back'))
        return

    message = await message.answer(f'<b>⚙️ Создание задачи</b>\nСсылка на видео:  <code>{video_url}</code>\nНайдено <code>...</code> комментариев\n\n<i>🔍 Поиск комментариев... (Обновление в реальном времени пока что не реализовано)</i>')
    video_comments = await TikTok.get_video_comments(video_id)
    if len(video_comments) == 0:
        await message.edit_text(f'<b>⚙️ Создание задачи</b>\nСсылка на видео:  <code>{video_url}</code>\n\n<i>❌ Найдено 0 комментариев</i>', reply_markup=await kb_back('back'))
        return
    await state.update_data(video_url=video_url, video_comments=video_comments)
    await state.set_state(CreateTask.SelectCommentSearchType)
    await message.edit_text(f'<b>⚙️ Создание задачи</b>\nСсылка на видео:  <code>{video_url}</code>\nНайдено <code>{len(video_comments)}</code> комментариев\n\n<i>Выберите тип поиска комментария</i>', reply_markup=await kb_search_video_comments())

@dp.callback_query_handler(state=CreateTask.InputVideoUrl)
async def state_create_task_input_video_url_callback(call: types.CallbackQuery, state: FSMContext):
    """Вернуться назад при вводе ссылки"""
    if call.data == 'back':
        call.data = 'user:menu'
    return await handle_user(call, state)



@dp.callback_query_handler(state=CreateTask.SelectCommentSearchType)
async def state_create_task_select_comment_search_type_callback(call: types.CallbackQuery, state: FSMContext, is_back: bool = False):
    """Выбор типа данных для поиска"""
    if is_back:
        state_data = await state.get_data()
        video_url = state_data['video_url']
        video_comments = state_data['video_comments']
        await call.message.edit_text(f'<b>⚙️ Создание задачи</b>\nСсылка на видео:  <code>{video_url}</code>\nНайдено <code>{len(video_comments)}</code> комментариев\n\n<i>Выберите тип поиска комментария</i>', reply_markup=await kb_search_video_comments())
        return
    if call.data == 'back':
        await state.set_state(CreateTask.InputVideoUrl)
        await call.message.edit_text("<b>⚙️ Создание задачи</b>\n\n<i>Отправьте ссылку на видео</i>", reply_markup=await kb_back('user:menu'))
        return
    elif call.data == 'text':
        await state.update_data(search_type='text')
        text = 'Введите полный текст или часть текста комментария для поиска'
    elif call.data == 'username':
        await state.update_data(search_type='username')
        text = 'Введите полный юзернейм или часть юзернейма создателя комментария для поиска'
    else:
        return await call.answer('Неизвестная кнопка')

    state_data = await state.get_data()
    video_url = state_data['video_url']
    video_comments = state_data['video_comments']
    await call.message.edit_text(f'<b>⚙️ Создание задачи</b>\nСсылка на видео:  <code>{video_url}</code>\nНайдено <code>{len(video_comments)}</code> комментариев\n\n<i>{text}</i>', reply_markup=await kb_back('back'))
    await state.set_state(CreateTask.InputSearchText)



@dp.message_handler(state=CreateTask.InputSearchText)
async def state_create_task_input_search_text(message: types.Message, state: FSMContext):
    """Ввод текста для поиска среди комментариев по заданному типу данных (юзернейм или текст комментария)"""
    to_search_value = message.text
    state_data = await state.get_data()
    if 'search_type' not in state_data:
        await message.answer('<b>❌ Вы не выбрали тип поиска комментария</b>', reply_markup=await kb_back('back'))
        return

    comment = {'id': None, 'text': 'None', 'author': None, 'nickname': None, 'video_id': None}
    video_url = state_data['video_url']
    video_comments = state_data['video_comments']
    search_type = state_data['search_type']
    video_comments = TikTok.search_comments(video_comments, to_search_value, search_type == 'text', search_type == 'username')
    if len(video_comments) == 0:
        await message.answer(f'<b>⚙️ Создание задачи</b>\nСсылка на видео:  <code>{video_url}</code>\n\n<i>❌ Найдено 0 комментариев по заданным критериям</i>', reply_markup=await kb_back('back'))
        return
    elif len(video_comments) == 1:
        comment = video_comments[0]
    elif len(video_comments) > 1:
        content = '\n'.join(f"ID: {comment['id']} | Автор: @{comment['author']} | Никнейм автора: {comment['nickname']} | Текст: {comment['text']}" for comment in video_comments)
        file_buffer = io.BytesIO()
        file_buffer.write(content.encode('utf-8'))
        file_buffer.seek(0)
        await message.answer_document(InputFile(file_buffer, filename='comments.txt'), caption=f'<b>⚙️ Создание задачи</b>\nСсылка на видео:  <code>{video_url}</code>\n\n<i>❌ Найдено {len(video_comments)} комментариев по заданным критериям.\nНайдите нужный комментарий в файле ниже и введите его id</i>', reply_markup=await kb_back('back'))
        await state.set_state(CreateTask.InputCommentID)
        return

    comment_text = comment["text"].split('\n')[0][:20]
    await state.update_data(comment_id=comment['id'], comment=comment)
    await message.answer(f'<b>⚙️ Создание задачи</b>\nСсылка на видео:  <code>{video_url}</code>\n\n📝 Найденный комментарий:\nID:  <code>{comment["id"]}</code>\nАвтор: <code>@{comment["author"]}</code>\nТекст: <i>{comment_text}</i>\n\n<i>⏳ Введите время накрутки в минутах</i>', reply_markup=await kb_back('back'))
    await state.set_state(CreateTask.InputTaskTTL)

@dp.callback_query_handler(state=CreateTask.InputSearchText)
async def state_create_task_input_search_text_callback(call: types.CallbackQuery, state: FSMContext):
    """Выбор типа данных для поиска"""
    if call.data == 'back':
        await state.set_state(CreateTask.SelectCommentSearchType)
        return await state_create_task_select_comment_search_type_callback(call, state)
    else:
        return await call.answer('Неизвестная кнопка')



@dp.message_handler(state=CreateTask.InputCommentID)
async def state_create_input_comment_id(message: types.Message, state: FSMContext):
    """Ввод ID комментария для накрутки, вызывается если найдено больше 1 комментария"""
    comment_id = message.text.strip()
    state_data = await state.get_data()
    video_url = state_data['video_url']
    video_comments = state_data['video_comments']
    video_comments = TikTok.search_comments(video_comments)
    searched_comments = [comment for comment in video_comments if comment['id'] == comment_id]
    if len(searched_comments) == 0:
        await message.answer(f'<b>⚙️ Создание задачи</b>\nСсылка на видео:  <code>{video_url}</code>\n\n<i>❌ Найдено 0 комментариев по введенному id</i>', reply_markup=await kb_back('back'))
        return
    comment = searched_comments[0]
    comment_text = comment["text"].split('\n')[0][:20]
    await state.update_data(comment_id=comment['id'], comment=comment)
    await state.set_state(CreateTask.InputTaskTTL)
    await message.answer(f'<b>⚙️ Создание задачи</b>\nСсылка на видео:  <code>{video_url}</code>\n\n📝 Найденный комментарий:\nID:  <code>{comment["id"]}</code>\nАвтор: <code>@{comment["author"]}</code>\nТекст: <i>{comment_text}</i>\n\n<i>⏳ Введите время накрутки в минутах</i>', reply_markup=await kb_back('back'))

@dp.callback_query_handler(state=CreateTask.InputCommentID)
async def state_create_input_comment_id_callback(call: types.CallbackQuery, state: FSMContext):
    """Ввод ID комментария для накрутки, вызывается если найдено больше 1 комментария"""
    if call.data == 'back':
        await state.set_state(CreateTask.SelectCommentSearchType)
        state_data = await state.get_data()
        video_url = state_data['video_url']
        video_comments = state_data['video_comments']
        await call.message.edit_text(f'<b>⚙️ Создание задачи</b>\nСсылка на видео:  <code>{video_url}</code>\nНайдено <code>{len(video_comments)}</code> комментариев\n\n<i>Выберите тип поиска комментария</i>', reply_markup=await kb_search_video_comments())
        return
    else:
        return await call.answer('<i>⛔️ Неизвестная кнопка</i>')



@dp.message_handler(state=CreateTask.InputTaskTTL)
async def state_create_task_input_task_ttl(message: types.Message, state: FSMContext):
    """Ввод времени накрутки в минутах"""
    try:
        task_ttl = int(message.text.strip())
    except:
        await message.answer('<i>⚠️ Введите число без посторонних символов</i>', reply_markup=await kb_back('back'))
        return

    state_data = await state.get_data()
    video_url = state_data['video_url']
    comment_id = state_data['comment_id']
    await state.update_data(task_ttl=task_ttl, proxies=[])
    await state.set_state(CreateTask.InputTaskProxy)
    await message.answer(f'<b>⚙️ Создание задачи</b>\nСсылка на видео:  <code>{video_url}</code>\n\nID комментария:  <code>{comment_id}</code>\nВремя накрутки:  <code>{task_ttl} минут</code>\n\n<i>📰 Отправьте прокси для задачи (принимаются файлы и просто сообщения), 1 строка = 1 прокси.\nДопустимые форматы прокси:\nip:port\nip:port:user:pass\nuser:pass@ip:pass\n\nДанный пункт можно пропустить, тогда будут использоваться прокси из конфига</i>', reply_markup=await kb_add_proxies())

@dp.callback_query_handler(state=CreateTask.InputTaskTTL)
async def state_create_task_input_task_ttl_callback(call: types.CallbackQuery, state: FSMContext):
    """Ввод времени накрутки в минутах"""
    if call.data == 'back':
        await state.set_state(CreateTask.SelectCommentSearchType)
        state_data = await state.get_data()
        video_url = state_data['video_url']
        video_comments = state_data['video_comments']
        await call.message.edit_text(f'<b>⚙️ Создание задачи</b>\nСсылка на видео:  <code>{video_url}</code>\nНайдено <code>{len(video_comments)}</code> комментариев\n\n<i>Выберите тип поиска комментария</i>', reply_markup=await kb_search_video_comments())
        return
    else:
        return await call.answer('Неизвестная кнопка')



@dp.message_handler(state=CreateTask.InputTaskProxy, content_types=[types.ContentType.TEXT, types.ContentType.DOCUMENT])
async def state_create_task_input_task_proxy(message: types.Message, state: FSMContext):
    """Добавление прокси для задачи"""
    if message.content_type == types.ContentType.TEXT:
        proxy = message.text.splitlines()
    elif message.content_type == types.ContentType.DOCUMENT:
        file_in_io = io.BytesIO()
        await message.document.download(destination_file=file_in_io)
        file_in_io.seek(0)
        content = file_in_io.read().decode('utf-8')
        proxy = content.splitlines()
    else:
        await message.answer(f'<i>⛔️ Данный формат данных (<code>{message.content_type}</code>) не поддерживается</i>')
        return

    parsed_proxies = await parse_proxy(proxy)
    state_data = await state.get_data()
    await state.update_data(proxies=[*state_data['proxies'], *parsed_proxies])
    await message.answer(f'<b>⚙️ Создание задачи</b>\n<i>Добавлено прокси: {len(parsed_proxies)} шт.</i>', reply_markup=await kb_add_proxies())

@dp.callback_query_handler(state=CreateTask.InputTaskProxy)
async def state_create_task_input_task_proxy_callback(call: types.CallbackQuery, state: FSMContext):
    """Добавление прокси для задачи"""
    if call.data == 'create_task':
        state_data = await state.get_data()
        if len(state_data['proxies']) == 0:
            try: proxy = ','.join(open(DEFAULT_PROXY_PATH, 'r', encoding='utf-8').read().splitlines())
            except:
                proxy = ''
                await call.answer(f'❌ Файл с прокси не найден', show_alert=True)
        else:
            proxy = ','.join(state_data['proxies'])
        task = await db.create_task(call.from_user.id, state_data['video_url'], state_data['comment_id'], proxy, state_data['task_ttl'])
        message = await call.message.answer('<i>⚙️ Создание задачи...</i>')
        asyncio.get_event_loop().create_task(run_task(task['id']))
        await message.edit_text(f'<i>Задача создана. ID задачи: {task["id"]}</i>', reply_markup=await kb_back('user:task:my_tasks', 'Перейти к задаче'))
        await state.finish()
    elif call.data == 'back':
        state_data = await state.get_data()
        video_url = state_data['video_url']
        comment = state_data['comment']
        comment_text = comment["text"].split('\n')[0][:20]
        await state.update_data(comment_id=comment['id'], comment=comment)
        await state.set_state(CreateTask.InputTaskTTL)
        await call.message.edit_text(f'<b>⚙️ Создание задачи</b>\nСсылка на видео:  <code>{video_url}</code>\n\n📝 Найденный комментарий:\nID:  <code>{comment["id"]}</code>\nАвтор: <code>@{comment["author"]}</code>\nТекст: <i>{comment_text}</i>\n\n<i>⏳ Введите время накрутки в минутах</i>', reply_markup=await kb_back('back'))











async def on_startup(dp: Dispatcher):
    """Инициализация базы данных при запуске."""
    await init_db()
    await run_tasks()

    await bot.set_my_commands([
        BotCommand(command="start", description="Начало работы"),
    ])


if __name__ == '__main__':
    executor.start_polling(dp, on_startup=on_startup)