import asyncio
import time
from fetch_videos import fetch_trending_videos
from download_videos import download_videos
from modify_videos import modify_videos
from generate_report import generate_report

async def main():
    """
    Основная асинхронная функция для выполнения полного цикла обработки видео:
    - Получение трендовых видео с TikTok.
    - Загрузка видео.
    - Модификация видео (уменьшение размера, скорости и добавление аудиодорожки).
    - Генерация отчета о выполненной работе и возникших ошибках.

    Возвращает:
    str или list: Сообщение об успешном завершении процесса или список сообщений об ошибках.
    """
    start_time = time.time()
    
    videos, fetch_error = await fetch_trending_videos()
    download_errors = []
    modify_errors = []
    
    if fetch_error:
        all_errors = [fetch_error]
    else:
        download_errors = download_videos(videos, 'videos/original')
        modify_errors = modify_videos('videos/original', 'videos/modified', 'Never_Gonna_Give_You_Up.mp3')
        all_errors = download_errors + modify_errors
    
    end_time = time.time()
    time_taken = end_time - start_time
    
    generate_report(len(videos), time_taken, all_errors, 'reports/summary_report.md')
    
    if all_errors:
        return all_errors

    return "Pipeline completed successfully!"

if __name__ == "__main__":
    errors = asyncio.run(main())
    if errors != "Pipeline completed successfully!":
        print("Errors occurred during processing:")
        for error in errors:
            print(error)
