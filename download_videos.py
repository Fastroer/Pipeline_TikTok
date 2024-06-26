import os
import time
from urllib.request import urlopen
import requests
from bs4 import BeautifulSoup

def save_tiktok(url, save_path):
    """
    Сохраняет видео с TikTok по указанному URL в указанное местоположение.

    Параметры:
    url (str): URL видео на TikTok, которое нужно сохранить.
    save_path (str): Путь, по которому будет сохранено видео.

    Возвращает:
    str: Сообщение об ошибке, если произошла ошибка во время сохранения видео, иначе None.
    """
    cookies = {
        '_ga': 'GA1.1.414356179.1719409171',
        'FCCDCF': '%5Bnull%2Cnull%2Cnull%2C%5B%22CQA0YQAQA0YQAEsACBENA6EoAP_gAEPgACgAINJB7C7FbSFCwH5zaLsAMAhHRsAAQoQAAASBAmABQAKQIAQCgkAQFASgBAACAAAAICZBIQIECAAACUAAQAAAAAAEAAAAAAAIIAAAgAEAAAAIAAACAAAAEAAIAAAAEAAAmAgAAIIACAAAhAAAAAAAAAAAAAAAAgAAAAAAAAAAAAAAAAAAAQOhQD2F2K2kKFkPCmQWYAQBCijYAAhQAAAAkCBIAAgAUgQAgFIIAgAIFAAAAAAAAAQEgCQAAQABAAAIACgAAAAAAIAAAAAAAQQAABAAIAAAAAAAAEAAAAAAAQAAAAIAABEhCAAQQAEAAAAAAAQAAAAAAAAAAABAAA%22%2C%222~70.89.93.108.122.149.196.236.259.311.313.323.358.415.449.486.494.495.540.574.609.827.864.981.1029.1048.1051.1095.1097.1126.1205.1211.1276.1301.1365.1415.1423.1449.1514.1570.1577.1598.1651.1716.1735.1753.1765.1870.1878.1889.1958.2072.2253.2299.2357.2373.2415.2506.2526.2568.2571.2575.2624.2677~dv.%22%2C%229246D723-A702-4CF2-8E05-AE59F5B18739%22%5D%5D',
        'FCNEC': '%5B%5B%22AKsRol_KUh7Feso6TA0F9pOGXeatwoO0WXwxIw_C428VONiWzrKJH5P41JZlmNNGR1cLBO_diB-3BrLuDPXKemYvuKtMWKG2XHCxkoS2ob-8WMey-D12LadPmfdUVDjomMMzt-0Y1LzWRjajaOgnH1EapUoyvSmkTQ%3D%3D%22%5D%5D',
        '_ga_ZSF3D6YSLC': 'GS1.1.1719409171.1.1.1719410477.0.0.0',
    }

    headers = {
        'accept': '*/*',
        'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
        'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'hx-current-url': 'https://ssstik.io/en-1',
        'hx-request': 'true',
        'hx-target': 'target',
        'hx-trigger': '_gcaptcha_pt',
        'origin': 'https://ssstik.io',
        'referer': 'https://ssstik.io/en-1',
        'sec-ch-ua': '"Opera GX";v="109", "Not:A-Brand";v="8", "Chromium";v="123"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36 OPR/109.0.0.0',
    }

    params = {
        'url': 'dl',
    }

    data = {
        'id': url,
        'locale': 'en',
        'tt': 'dDFDaW1k',
    }

    try:
        response = requests.post('https://ssstik.io/abc', params=params, cookies=cookies, headers=headers, data=data)
        downloadSoup = BeautifulSoup(response.text, "html.parser")
        downloadLink = downloadSoup.a["href"]
        mp4File = urlopen(downloadLink)

        with open(save_path, "wb") as output:
            while True:
                data = mp4File.read(4096)
                if data:
                    output.write(data)
                else:
                    break

    except Exception as e:
        return f"Ошибка сохранения видео {url}: {e}"

def download_videos(videos, download_folder):
    """
    Скачивает список видео с TikTok и сохраняет их в указанную папку.

    Параметры:
    videos (list): Список словарей с информацией о видео. Каждый словарь должен содержать ключи 'author' (с уникальным идентификатором автора) и 'id' (с идентификатором видео).
    download_folder (str): Путь к папке, в которую будут сохранены видео.

    Возвращает:
    list: Список сообщений об ошибках, возникших при скачивании видео.
    """

    if not os.path.exists(download_folder):
        os.makedirs(download_folder)

    errors = []
    for video in videos:
        author = video['author']['uniqueId']
        video_id = video['id']
        video_url = f"https://www.tiktok.com/@{author}/video/{video_id}/"
        save_path = os.path.join(download_folder, f"{video_id}.mp4")
        error = save_tiktok(video_url, save_path)
        if error:
            errors.append(error)
        time.sleep(10)

    return errors