import asyncio
import time
import aiosqlite

def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

class Database:
	DB_PATH = 'db.db'

	@classmethod
	async def create_tables(cls):
		async with aiosqlite.connect(cls.DB_PATH) as db:
			await db.execute('''CREATE TABLE IF NOT EXISTS users (
									id INTEGER PRIMARY KEY AUTOINCREMENT,
									user_id INTEGER UNIQUE,
									username TEXT,
									first_name TEXT,
									registration_date INTEGER
								)''')
			await db.execute('''CREATE TABLE IF NOT EXISTS tasks (
									id INTEGER PRIMARY KEY AUTOINCREMENT,
									user_id INTEGER,
									video_url TEXT,
									comment_id TEXT,
									likes_count INTEGER DEFAULT 0,
									proxy TEXT,
									task_ttl INTEGER,
									already_completed_minutes INTEGER,
									status TEXT,
									create_ts INTEGER
								)''')
			await db.execute('''CREATE TABLE IF NOT EXISTS presets (
									id INTEGER PRIMARY KEY AUTOINCREMENT,
									user_id INTEGER,
									title TEXT,
									author_username TEXT,
									proxy TEXT,
									task_ttl INTEGER,
									create_ts INTEGER
								)''')
			await db.commit()

	@classmethod
	async def get_user(cls, user_id: str = None, username: str = None) -> dict:
		async with aiosqlite.connect(cls.DB_PATH) as db:
			if user_id is not None:
				async with db.execute(f'SELECT * FROM users WHERE user_id = ?', (user_id,)) as cur:
					cur.row_factory = dict_factory
					user = await cur.fetchone()
			else:
				async with db.execute(f'SELECT * FROM users WHERE username = ?', (username,))  as cur:
					cur.row_factory = dict_factory
					user = await cur.fetchone()
			return user

	@classmethod
	async def create_user(cls, user_id: str, username: str, first_name: str = None) -> dict:
		async with aiosqlite.connect(cls.DB_PATH) as db:
			ts = int(time.time())
			await db.execute('INSERT INTO users (user_id, username, first_name, registration_date) VALUES (?, ?, ?, ?)', [user_id, username, first_name, ts])
			await db.commit()

		return await cls.get_user(user_id)

	@classmethod
	async def update_user(cls, user_id: str, username: str = None, first_name: str = None) -> dict:
		async with aiosqlite.connect(cls.DB_PATH) as db:
			await db.execute('UPDATE users SET username = ?, first_name = ? WHERE user_id = ?', (username, first_name, user_id))
			await db.commit()

		return await cls.get_user(user_id)


	@classmethod
	async def get_task(cls, task_id: int = None, user_id: int = None, for_start: bool = False) -> dict|list:
		async with aiosqlite.connect(cls.DB_PATH) as db:
			if task_id is not None:
				async with db.execute(f'SELECT * FROM tasks WHERE id = ?', (task_id,)) as cur:
					cur.row_factory = dict_factory
					task = await cur.fetchone()
					return task
			elif user_id is not None:
				async with db.execute(f'SELECT * FROM tasks WHERE user_id = ? ORDER BY id DESC', (user_id,)) as cur:
					cur.row_factory = dict_factory
					tasks = await cur.fetchall()
					return tasks
			elif for_start:
				async with db.execute(f'SELECT * FROM tasks WHERE status = ? OR status = ? ORDER BY id DESC', ('in_progress', 'created')) as cur:
					cur.row_factory = dict_factory
					tasks = await cur.fetchall()
					return tasks
			else:
				async with db.execute(f'SELECT * FROM tasks ORDER BY id DESC') as cur:
					cur.row_factory = dict_factory
					tasks = await cur.fetchall()
					return tasks

	@classmethod
	async def create_task(cls, user_id: int, video_url: str, comment_id: str, proxy: str|list, task_ttl: int) -> dict:
		async with aiosqlite.connect(cls.DB_PATH) as db:
			ts = int(time.time())
			status = 'created'
			async with await db.execute('INSERT INTO tasks (user_id, video_url, comment_id, proxy, task_ttl, already_completed_minutes, status, create_ts) VALUES (?, ?, ?, ?, ?, ?, ?, ?)', (user_id, video_url, comment_id, proxy, task_ttl, 0, status, ts)) as cur:
				cur.row_factory = dict_factory
				task_id = cur.lastrowid
			await db.commit()

		return await cls.get_task(task_id)

	@classmethod
	async def update_task(cls, task_id: int, already_completed_minutes: int = None, status: str = None, likes_count: int = None) -> dict:
		async with aiosqlite.connect(cls.DB_PATH) as db:
			if status is not None:
				await db.execute('UPDATE tasks SET status = ? WHERE id = ?', (status, task_id))
			if already_completed_minutes is not None:
				await db.execute('UPDATE tasks SET already_completed_minutes = already_completed_minutes + ? WHERE id = ?', (already_completed_minutes, task_id))
			if likes_count is not None:
				await db.execute('UPDATE tasks SET likes_count = ? WHERE id = ?', (likes_count, task_id))
			await db.commit()

		return await cls.get_task(task_id)


	@classmethod
	async def get_preset(cls, preset_id: int = None, user_id: int = None) -> dict|list:
		async with aiosqlite.connect(cls.DB_PATH) as db:
			if preset_id is not None:
				async with db.execute(f'SELECT * FROM presets WHERE id = ?', (preset_id,)) as cur:
					cur.row_factory = dict_factory
					preset = await cur.fetchone()
					return preset
			elif user_id is not None:
				async with db.execute(f'SELECT * FROM presets WHERE user_id = ? ORDER BY id DESC', (user_id,)) as cur:
					cur.row_factory = dict_factory
					presets = await cur.fetchall()
					return presets
			else:
				async with db.execute(f'SELECT * FROM presets ORDER BY id DESC') as cur:
					cur.row_factory = dict_factory
					presets = await cur.fetchall()
					return presets

	@classmethod
	async def create_preset(cls, user_id: int, title: str, author_username: str, proxy: str|list, task_ttl: int) -> dict:
		async with aiosqlite.connect(cls.DB_PATH) as db:
			ts = int(time.time())

			async with await db.execute('INSERT INTO presets (user_id, title, author_username, proxy, task_ttl, create_ts) VALUES (?, ?, ?, ?, ?, ?)', (user_id, title, author_username, proxy, task_ttl, ts)) as cur:
				cur.row_factory = dict_factory
				preset_id = cur.lastrowid
			await db.commit()

		return await cls.get_preset(preset_id)

	@classmethod
	async def update_preset(cls, preset_id: int, title: str = None, author_username: str = None, proxy: str|list = None) -> dict:
		async with aiosqlite.connect(cls.DB_PATH) as db:
			if title is not None:
				await db.execute('UPDATE presets SET title = ? WHERE id = ?', (title, preset_id))
			if author_username is not None:
				await db.execute('UPDATE presets SET author_username = ? WHERE id = ?', (author_username, preset_id))
			if proxy is not None:
				await db.execute('UPDATE presets SET proxy = ? WHERE id = ?', (proxy, preset_id))
			await db.commit()

		return await cls.get_preset(preset_id)


	@classmethod
	async def delete_preset(cls, preset_id: int) -> dict:
		async with aiosqlite.connect(cls.DB_PATH) as db:
			await db.execute('DELETE FROM presets WHERE id = ?', (preset_id, ))
			await db.commit()

		return True

async def main():
	await Database.create_tables()
	user = await Database.get_task(47)
	print(user)


if __name__ == '__main__':
	asyncio.run(main())