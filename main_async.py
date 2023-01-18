import os
import toml
import asyncio
import aiohttp


NAME_CONFIG_FILE = 'conf.toml'


urls = [
    # 'http://localhost:3000/posts',
    # 'http://localhost:3000/profile',
    # 'http://localhost:3000/comments',
    'http://localhost:3000/public_data',
    'http://localhost:3000/danger_data',
]


# async def get_data(session, url):
#     async with session.get(url=url, ssl=False) as resp:
#         print(f'url: {resp.url} --> status_code: {resp.status}')

#         # if resp.status != 200:
#         #     ff = await get_data(session=session, url=url)
#         #     return ff
#         # return resp


# async def gather_data(urls):
#     async with aiohttp.ClientSession(trust_env=True) as session:
#         tasks = []
#         for url in urls:
#             task = asyncio.create_task(get_data(session, url))
#             tasks.append(task)
#         await asyncio.gather(*tasks)

async def cr_task(sess, url):
    return asyncio.create_task(sess.get(url))


async def htt_get(urls):
    async with aiohttp.ClientSession() as session:
        tasks = []
        for url in urls:
            task = await cr_task(sess=session, url=url)
            tasks.append(task)
        print(tasks)
        resp = await asyncio.gather(*tasks)
        print(resp)
        
        # l = [r.status for r in resp if r.status == 200 else cr_task(session, r.url)]
        l = [r.status if r.status==200 else  asyncio.gather(cr_task(sess=session, url=r.url)) for r in resp]
        print(l)


        
        


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
                asyncio.run(htt_get(urls=urls))           
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