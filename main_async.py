import os
import toml
import asyncio
import aiohttp

from typing import Union
from datetime import datetime


NAME_CONFIG_FILE = 'conf.toml'


urls = [
    'http://localhost:3000/posts',
    'http://localhost:3000/profile',
    'http://localhost:3000/comments',
    'http://localhost:3000/public_data',
    'http://localhost:3000/danger_data',
]


async def get_http_response(urls: Union[list, str]) -> dict:
    '''
    Принимает список url адресов или единичный адресс в виде строки.
    Возращаемое значение словарь, где ключ - это url, значение - 
    ответ сервера.
    '''
    tasks = []
    async with aiohttp.ClientSession() as session:
        if type(urls) == list:
            tasks = [
                asyncio.ensure_future(session.get(url=url))
                for url in urls
            ]
            responses = await asyncio.gather(*tasks)
            responses_data = {response.url: response for response in responses}
            return responses_data
        else:
            task = asyncio.ensure_future(session.get(url=urls))
            tasks.append(task)
            responses = await asyncio.gather(*tasks)
            responses_data = {response.url: response for response in responses}
            return responses_data


async def checking_status_requests(data: dict) -> dict:
    '''
    Примает только словарь(где ключ - это url, значение - 
    ответ сервера).
    Проверяет статус ответов в полученном словаре.
        Если все 200 - вернет полученный словарь.
        Если есть 500 - осуществит запрос на адресс ресурса,
            который вернул этот статус ответа.
            !!! Так до тех пор пока не вернет 200 !!!
    '''
    for k, v in data.items():
        print(f'[INFO]: url: {k} --> status_code: {v.status}')
        if v.status != 200:
            while True:
                new_data = await get_http_response(k)
                if new_data[k].status != 200:
                    print(f'[ATTENTION]: re-inquiry at: {new_data[k].url}')
                    continue
                else:
                    data.update(new_data)
                    print(
                        f'[INFO]: url: {new_data[k].url} --> status_code: {new_data[k].status}')
                    return data


def writer_config(data: dict) -> None:
    '''
    Функция создает конфигурационный файл.
    Принимает словарь, где ключ - имя переменной в файле,
    значение - значение этой переменной.
    Ничего не возращает.
    '''
    with open(NAME_CONFIG_FILE, 'w') as f:
        toml.dump(o=data, f=f)


def main(urls: list) -> dict:
    '''
    Основная функция.
    Возращает словарь, как следствие выполнение подфункции:
        checking_status_requests.
    В ней прописана логика валидации пользовательского ввода,
    а так же проверки существования конфиг файла, и
    валидация содердимого этого файла.
    Если пройдены все проверки - выполняется блок:
        if content_file['IS_START'] с запуском вложенных в него
        функций: get_http_response, checking_status_requests
    '''
    while True:
        chech_file = os.path.isfile(path=NAME_CONFIG_FILE)

        if chech_file:
            content_file = toml.load(f=NAME_CONFIG_FILE)
            try:
                value_is_start = content_file['IS_START']
                if value_is_start != 1 and value_is_start != 0:
                    print(
                        f'Invalid IS_START value in configuration file: {NAME_CONFIG_FILE}.')
                    break
            except KeyError:
                print(
                    f'IS_START parameter not found in configuration file: {NAME_CONFIG_FILE}.')
                break
            if content_file['IS_START']:
                data = asyncio.run(get_http_response(urls=urls))
                asyncio.run(checking_status_requests(data=data))
                break
            else:
                try:
                    val = int(input('Enter value [0 or 1]: '))
                    if val == 0:
                        continue
                    elif val == 1:
                        content_file['IS_START'] = val
                        writer_config(data=content_file)
                    else:
                        print('Only [0 or 1] can be entered.')
                except ValueError as e:
                    print('Value cannot be a character or string.')
        else:
            writer_config(data={'IS_START': 0})


if __name__ == '__main__':
    start_time = datetime.now()
    main(urls=urls)
    print(datetime.now() - start_time)
