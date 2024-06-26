from TikTokApi import TikTokApi
from playwright.async_api import async_playwright
import asyncio

async def get_ms_token():
    """
    Асинхронная функция для получения msToken из cookies сайта TikTok.

    Возвращает:
    tuple: Кортеж, содержащий msToken (str) и сообщение об ошибке (str). Если msToken успешно получен, сообщение об ошибке будет None.
    """
    try:
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=False)
            context = await browser.new_context()
            page = await context.new_page()
            
            await page.goto("https://www.tiktok.com/")
            await asyncio.sleep(5)
            
            cookies = await context.cookies()
            ms_token = None
            for cookie in cookies:
                if (cookie['name'] == 'msToken'):
                    ms_token = cookie['value']
                    break

            await browser.close()
            return ms_token, None
    except Exception as e:
        return None, f"Ошибка получения msToken: {e}"

async def fetch_trending_videos():
    """
    Асинхронная функция для получения списка трендовых видео с TikTok.

    Возвращает:
    tuple: Кортеж, содержащий список видео (list) и сообщение об ошибке (str). Если видео успешно получены, сообщение об ошибке будет None.
    """
    context_options = {
        'viewport': {'width': 1280, 'height': 1024},
        'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36'
    }

    ms_token, error = await get_ms_token()
    if error:
        return [], error

    if ms_token:
        try:
            async with TikTokApi() as api:
                await api.create_sessions(ms_tokens=[ms_token], num_sessions=1, sleep_after=3, context_options=context_options)
                all_videos = []
                count = 30
                
                while len(all_videos) < 100:
                    try:
                        videos = [video.as_dict async for video in api.trending.videos(count=count)]
                        all_videos.extend(videos)
                        if len(videos) == 0:
                            break
                    except Exception as e:
                        return [], f"Ошибка загрузки видео: {e}"
                
                return all_videos[:100], None
        except Exception as e:
            return [], f"Ошибка при создании сессии API: {e}"
    return [], "msToken не найден"
