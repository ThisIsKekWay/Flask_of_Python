import os
import requests
import asyncio
import threading
import multiprocessing
import time
import argparse
from pathlib import Path


image_urls = []
with open('urls.txt', 'r', encoding='utf-8') as images:
    for image_url in images.readlines():
        image_urls.append(image_url.strip())

image_path = Path('images')


def download_image_sync(url):
    start_time = time.time()
    file_name = image_path.joinpath(os.path.basename(url))
    with open(file_name, 'wb') as f:
        for chunk in requests.get(url).iter_content(chunk_size=1024):
            if chunk:
                f.write(chunk)
    print(f'{file_name} was downloaded in {time.time() - start_time}s')


async def download_image_async (url):
    start_time = time.time()
    responce = await asyncio.get_event_loop().run_in_executor(None, requests.get, url, {'stream': True})
    file_name = image_path.joinpath(os.path.basename(url))
    with open(file_name, 'wb') as f:
        for chunk in responce.iter_content(chunk_size=1024):
            if chunk:
                f.write(chunk)
    print(f'{file_name} was downloaded in {time.time() - start_time}s')


def download_image_thread (urls):
    start_time = time.time()
    threads = []
    for url in urls:
        t = threading.Thread(target=download_image_sync, args=(url,))
        t.start()
        threads.append(t)

    for t in threads:
        t.join()

    print(f'All images was downloaded in {time.time() - start_time}s')


def download_image_process (urls):
    start_time = time.time()
    processes = []
    for url in urls:
        p = multiprocessing.Process(target=download_image_sync, args=(url,))
        p.start()
        processes.append(p)

    for p in processes:
        p.join()

    print(f'All images was downloaded in {time.time() - start_time}s')


async def download_images_asyncio(urls):
    start_time = time.time()
    tasks = []
    for url in urls:
        task = asyncio.ensure_future(download_image_async(url))
        tasks.append(task)

    await asyncio.gather(*tasks)
    print(f'All images was downloaded in {time.time() - start_time}s')


if __name__ == '__main__':

    if not os.path.isdir('images'):
        os.mkdir('images')

    parser = argparse.ArgumentParser(description='Программа для загрузки изображений по URL')
    parser.add_argument('--func',
                        choices=['M', 'P', 'S', 'A'],
                        default='S',
                        help='Выберите режим работы программы: '
                             'M для мультипоточного скачивания, '
                             'P для мультипроцессорного скачивания, '
                             'S для синхронного скачивания, '
                             'A для асинхронного скачивания.')
    parser.add_argument("--urls", nargs="+", default=image_urls ,
                        help="Перечень URL-адресов для загрузки изображений."
                             "Имеет тип списка")
    args = parser.parse_args()

    if args.func == 'M':
        download_image_thread(args.urls)
    elif args.func == 'P':
        download_image_process(args.urls)
    elif args.func == 'S':
        for url in args.urls:
            download_image_sync(url)
    elif args.func == 'A':
        loop = asyncio.get_event_loop()
        loop.run_until_complete(download_images_asyncio(args.urls))
    else:
        print('Wrong function')
