
# Pipeline TikTok

Этот проект реализует конвейер обработки видео TikTok, который выполняет следующие шаги:

1. **Получение трендовых видео TikTok**:
   - Извлекает 100 трендовых видео TikTok для указанного местоположения.
   - Использует API или веб-скрейпинг для получения списка трендовых видео.

2. **Скачивание видео без водяных знаков**:
   - Скачивает видео по URL, полученным на предыдущем шаге, без водяных знаков.

3. **Модификация видео**:
   - Уменьшает скорость видео на 90%.
   - Уменьшает разрешение видео на 90%.
   - Заменяет аудиодорожку на песню "Never Gonna Give You Up" Рика Эстли.

4. **Генерация отчета**:
   - Создает отчет, суммирующий выполненные действия.
   - Отчет включает:
     - Количество обработанных видео.
     - Время, затраченное на весь процесс.
     - Любые возникшие проблемы и способы их решения.
   - Форматирует отчет в удобочитаемом виде, например, в PDF или Markdown файле.

## Установка и запуск

### Клонирование репозитория

```bash
git clone https://github.com/Fastroer/Pipeline_TikTok.git
cd Pipeline_TikTok
```

### Установка зависимостей

Создайте виртуальное окружение и установите зависимости:

```bash
python -m venv env
source env/bin/activate  # На Windows используйте `env\Scripts\activate`
pip install -r requirements.txt
```

### Запуск

```bash
python main.py
```

## Структура проекта

- `fetch_videos.py`: Модуль для получения трендовых видео TikTok.
- `download_videos.py`: Модуль для скачивания видео.
- `modify_videos.py`: Модуль для модификации видео.
- `generate_report.py`: Модуль для генерации отчета.
- `main.py`: Основной скрипт, который выполняет весь процесс.

## Пример использования

1. Получение трендовых видео:

```python
videos, error = await fetch_trending_videos()
if error:
    print(error)
else:
    print(videos)
```

2. Скачивание видео:

```python
errors = download_videos(videos, 'videos/original')
if errors:
    for error in errors:
        print(error)
```

3. Модификация видео:

```python
errors = modify_videos('videos/original', 'videos/modified', 'Never_Gonna Give You Up.mp3')
if errors:
    for error in errors:
        print(error)
```

4. Генерация отчета:

```python
generate_report(len(videos), time_taken, errors, 'reports/summary_report.md')
```

## Зависимости

- opencv-python-headless
- moviepy
- requests
- beautifulsoup4
- TikTokApi
- playwright
