
import os
import requests
import aiohttp
import asyncio
from urllib.parse import urlparse
from os import path
urls = []
for i in range(10):
    response = requests.get('https://source.unsplash.com/random')
    if response.status_code == 200:
        urls.append(response.url)



def file(folder, filename, content):
    os.makedirs(folder, exist_ok=True)
    with open(path.join(folder, filename), 'wb') as fh:
        fh.write(content)

async def img(url, folder):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as r:
                c = await r.read()
                loop = asyncio.get_event_loop()
                filename = os.path.basename(urlparse(url).path)
                await loop.run_in_executor(None, file, folder, filename, c)
async def download_images(urls):
    tasks = []
    for i, url in enumerate(urls, start=1):
        folder_name = f'images_{i}'
        os.makedirs(folder_name, exist_ok=True)
        task = asyncio.create_task(img(url, folder_name))
        tasks.append(task)
    await asyncio.gather(*tasks)

asyncio.run(download_images(urls))

for i in range(10):
    folder_name = f'r_images_{i+1}'
    os.makedirs(folder_name, exist_ok=True)
    response = requests.get('https://source.unsplash.com/random')
    filename = f'image_{i + 1}.jpg'
    with open(os.path.join(folder_name, filename), 'wb') as f:
        f.write(response.content)

