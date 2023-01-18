# import toml
# toml_str = '''
# title = "Toml Example"
# [owner]
# name = "Roman"
# [database]
# server = "192.168.1.1"
# ports = [8000, 8001, 8002]
# '''
# toml_str = 'IS_START = 0'
# parser_toml = toml.loads(s=toml_str)
# print(parser_toml)
# with open('conf.toml', 'w') as f:
#     new = toml.dump(o=parser_toml, f=f)
# print(new)
# условно первый запуск и создание конфиг файла
# возможно обернуть в функцию, которая смотрит если файл в директории
# если нет, то создать файл
# toml_str = 'IS_START = 0'
# parser_toml = toml.loads(s=toml_str)
# with open('conf.toml', 'w') as f:
#     new = toml.dump(o=parser_toml, f=f)
# print(toml.load(f='conf.toml')) # чтение из файла
# o = {'IS_START': int(input())}
# oo = toml.dumps(o=o)
# print(oo)
# print(os.path.isfile(path='conf.toml')) # проверка существования файла
# chech_file = os.path.isfile(path='conf.toml')







# ==================================================================================
# import requests
# import multiprocessing as mp

# def get(url):
#     return requests.get(url)


# urls = [
#     'http://localhost:3000/posts',
#     'http://localhost:3000/profile',
#     'http://localhost:3000/comments',
#     'http://localhost:3000/public_data',
#     'http://localhost:3000/danger_data',
# ]

# with mp.Pool(mp.cpu_count()) as pool:
#     res = pool.map(get, urls)
# print(res)

# for i in res:
#     print('='*88)
#     print(i.__dict__)
# ==================================================================================
# import asyncio
# import aiohttp


# urls = [
#     'http://localhost:3000/posts',
#     'http://localhost:3000/profile',
#     'http://localhost:3000/comments',
#     'http://localhost:3000/public_data',
#     'http://localhost:3000/danger_data',
# ]


# async def get_data(session, url):
#     async with session.get(url=url, ssl=False) as resp:
#         print(resp)



# async def gather_data(urls):
#     async with aiohttp.ClientSession(trust_env=True) as session:
#         tasks = []
#         for url in urls:
#             task = asyncio.create_task(get_data(session, url))
#             tasks.append(task)
        
#         await asyncio.gather(*tasks)


# def main():
#     asyncio.run(gather_data(urls))



# if __name__ == '__main__':
#     main()

# ==================================================================================
import requests
urls = [
    'http://localhost:3000/posts',
    'http://localhost:3000/profile',
    'http://localhost:3000/comments',
    'http://localhost:3000/public_data',
    'http://localhost:3000/danger_data',
]



def gather_data(urls):
    for url in urls:
        resp = requests.get(url=url)
        print(resp)



if __name__ == '__main__':
    gather_data(urls)