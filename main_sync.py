import os
import toml
import requests

from datetime import datetime


NAME_CONFIG_FILE = 'conf.toml'


urls = [
    'http://localhost:3000/posts',
    'http://localhost:3000/profile',
    'http://localhost:3000/comments',
    'http://localhost:3000/public_data',
    'http://localhost:3000/danger_data',
]


def get_http_response(url: str):
    '''
    Получить http ответ.
    Функция принимает url адрес в виде строки.
    Возращает объект response.
    Функция рекурсивная:
        условия рекурсии: статус ответа не равно 200,
        условия выхода: статус ответа 200.
    '''
    try:
        response = requests.get(url=url)
        print(
            f'[INFO]: url: {response.url} --> status_code: {response.status_code}')
        if response.status_code != 200:
            return get_http_response(url=url)
        return response
    except:
        print(f'[INFO]: unavailable {url}.')


def combine_response_information(urls: list) -> list:
    '''
    Обьединить информацию ответов после выполненых запросов.
    Принимает список url адресов.
    Возращает список объектов response.
    '''
    list_responses = list(map(get_http_response, urls))
    return list_responses


def writer_config(data: dict) -> None:
    '''
    Функция создает конфигурационный файл.
    Принимает словарь, где ключ - имя переменной в файле,
    значение - значение этой переменной.
    Ничего не возращает.
    '''
    with open(NAME_CONFIG_FILE, 'w') as f:
        toml.dump(o=data, f=f)


def main(urls: list) -> list:
    '''
    Основная функция.
    Возращает список, как следствие выполнение подфункции:
        combine_response_information.
    В ней прописана логика валидации пользовательского ввода,
    а так же проверки существования конфиг файла, и
    валидация содердимого этого файла.
    Если пройдены все проверки - выполняется блок:
        if content_file['IS_START'] с запуском вложенных в него
        функций: get_http_response, combine_response_information
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
                combine_response_information(urls=urls)
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
