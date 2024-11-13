import json

from aiogram.types import ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

from config import STATUS_EMOJI_TRANSLATIONS


#################################################################################################################################
async def kb_construct(keyboard = None, q = None, row_width = 2):
	if q is None:
		q = {}
	if not keyboard:
		keyboard = InlineKeyboardMarkup(row_width)
	if type(q) is dict:
		for x in q:
			_ = q[x].split('^')
			if _[0] == 'url': keyboard.insert(InlineKeyboardButton(x,url=_[1]))

			elif _[0] == 'cd': keyboard.insert(InlineKeyboardButton(x,callback_data=_[1]))
	else:
		for x in q: keyboard.insert(x)

	return keyboard
#################################################################################################################################

async def kb_menu(is_admin: bool) -> InlineKeyboardMarkup:
	q = {
		'Создать задачу': 'cd^user:task:create',
		'Мои задачи': 'cd^user:task:my_tasks'
	}
	keyboard = await kb_construct(InlineKeyboardMarkup(), q)
	return keyboard

async def kb_user_tasks(tasks: list, page: int = 1) -> InlineKeyboardMarkup:
	keyboard = InlineKeyboardMarkup(row_width=2)
	tasks_per_page = 6  # Количество задач на одной странице
	total_pages = (len(tasks) + tasks_per_page - 1) // tasks_per_page  # Общее количество страниц

	start_index = (page - 1) * tasks_per_page
	end_index = start_index + tasks_per_page
	this_page_tasks = tasks[start_index:end_index]

	for task in this_page_tasks:
		text = f"{task['id']}| {task['already_completed_minutes']}/{task['task_ttl']} | {STATUS_EMOJI_TRANSLATIONS[task['status']]}"
		keyboard.add(InlineKeyboardButton(text, callback_data=f'user:task:show:{page}:{task["id"]}'))

	if page > 1 and page < total_pages:
		keyboard.add(InlineKeyboardButton('❮❮', callback_data=f'user:task:my_tasks:{page - 1}'))
		keyboard.insert(InlineKeyboardButton('❯❯', callback_data=f'user:task:my_tasks:{page + 1}'))
	elif page > 1:
		keyboard.add(InlineKeyboardButton('❮❮', callback_data=f'user:task:my_tasks:{page - 1}'))
	elif page < total_pages:
		keyboard.insert(InlineKeyboardButton('❯❯', callback_data=f'user:task:my_tasks:{page + 1}'))

	keyboard.add(InlineKeyboardButton('↪ Назад', callback_data=f'user:menu'))
	return keyboard

async def kb_search_video_comments() -> InlineKeyboardMarkup:
	q = {
		'По тексту': 'cd^text',
		'По юзернейму': 'cd^username'
	}
	keyboard = await kb_construct(InlineKeyboardMarkup(row_width=2), q)
	keyboard.add(InlineKeyboardButton('↪ Назад', callback_data='back'))
	return keyboard

async def kb_add_proxies() -> InlineKeyboardMarkup:
	q = {
		'Создать задачу': 'cd^create_task',
		'↪ Назад': 'cd^back'
	}
	keyboard = await kb_construct(InlineKeyboardMarkup(row_width=1), q)
	return keyboard

### UTILS ###
async def kb_close() -> InlineKeyboardMarkup:
	keyboard = await kb_construct(InlineKeyboardMarkup(), {'❌ Закрыть':'cd^utils:delete'})
	return keyboard

async def kb_back(callback_data = 'user:menu', text = '↪ Назад') -> InlineKeyboardMarkup:
	keyboard = InlineKeyboardMarkup()
	keyboard.add(InlineKeyboardButton(text, callback_data=callback_data))
	return keyboard