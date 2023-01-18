import os
import toml
import requests
import multiprocessing as mp


NAME_CONFIG_FILE = 'conf.toml'


urls = [
    # 'http://localhost:3000/posts',
    # 'http://localhost:3000/profile',
    # 'http://localhost:3000/comments',
    'http://localhost:3000/public_data',
    'http://localhost:3000/danger_data',
]


def get_request(url: str):
    try:
        resp = requests.get(url=url)
        print(f'url: {resp.url} --> status_code: {resp.status_code}')
        if resp.status_code != 200:
            return get_request(url=url)
        return resp
    except:
        print(f'unavailable {url}')


def getting_request_data(urls: list):
    with mp.Pool(mp.cpu_count()) as pool:
        resp = pool.map(func=get_request, iterable=urls)
        print(resp)
        return resp
        


def writer_config(data: dict) -> None:
    with open(NAME_CONFIG_FILE, 'w') as f:
            toml.dump(o=data, f=f)


def main(urls: list) -> None:
    while True:
        chech_file = os.path.isfile(path=NAME_CONFIG_FILE)

        if chech_file:
            content_file = toml.load(f=NAME_CONFIG_FILE)
            try:
                value_is_start = content_file['IS_START']
                if value_is_start != 1 and value_is_start != 0:
                    print('ne dopustimoe znachenie IS_START v file config')
                    break
            except KeyError:
                print('param IS_START ne nayden in conf.toml')
                break
            if content_file['IS_START']:
                getting_request_data(urls=urls)            
                break
            else:
                try:
                    val = int(input('input int value: '))
                    if val == 0:
                        continue
                    elif val == 1:
                        content_file['IS_START'] = val
                        writer_config(data=content_file)
                    else:
                        print('input only 0 or 1')
                except ValueError as e:
                    print('value dojno but INT!')
        else:
            writer_config(data={'IS_START': 0})





if __name__ == '__main__':
    main(urls=urls)