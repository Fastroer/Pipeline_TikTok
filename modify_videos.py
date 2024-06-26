import os
import cv2
from moviepy.editor import AudioFileClip, VideoFileClip, concatenate_audioclips, vfx
import concurrent.futures
import threading

lock = threading.Lock()

def process_video(input_path, output_path, audio_path, errors):
    """
    Обрабатывает видео: уменьшает размер, скорость и добавляет аудиодорожку.

    Параметры:
    input_path (str): Путь к исходному видеофайлу.
    output_path (str): Путь к сохраненному видеофайлу с внесенными изменениями.
    audio_path (str): Путь к аудиофайлу, который будет добавлен к видео.
    errors (list): Список для сохранения сообщений об ошибках.

    Возвращает:
    None
    """
    temp_output_path = output_path.replace(".mp4", "_temp.mp4")
    try:
        cap = cv2.VideoCapture(input_path)

        if not cap.isOpened():
            raise Exception(f"Ошибка открытия видеофайла {input_path}")

        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH) * 0.9)
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT) * 0.9)
        fps = cap.get(cv2.CAP_PROP_FPS) * 0.9

        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        out = cv2.VideoWriter(temp_output_path, fourcc, fps, (width, height))

        while True:
            ret, frame = cap.read()
            if not ret:
                break

            frame = cv2.resize(frame, (width, height))
            out.write(frame)

        cap.release()
        out.release()

        add_audio_to_video(temp_output_path, output_path, audio_path, fps)

    except Exception as e:
        errors.append(f"Ошибка обработки видео {input_path}: {e}")
    finally:
        with lock:
            if os.path.exists(temp_output_path):
                try:
                    os.remove(temp_output_path)
                except Exception as e:
                    errors.append(f"Ошибка удаления временного файла {temp_output_path}: {e}")

def add_audio_to_video(temp_video_path, final_video_path, audio_path, fps):
    """
    Добавляет аудиодорожку к видеофайлу.

    Параметры:
    temp_video_path (str): Путь к временно сохраненному видеофайлу.
    final_video_path (str): Путь к финальному видеофайлу с добавленной аудиодорожкой.
    audio_path (str): Путь к аудиофайлу, который будет добавлен к видео.
    fps (float): Частота кадров видеофайла.

    Возвращает:
    None
    """
    try:
        with VideoFileClip(temp_video_path) as video:
            with AudioFileClip(audio_path) as audio:
                audio = audio.fx(vfx.speedx, 1/0.9)

                if audio.duration < video.duration:
                    num_repeats = int(video.duration / audio.duration) + 1
                    audio = concatenate_audioclips([audio] * num_repeats)
                
                audio = audio.set_duration(video.duration)
                video = video.set_audio(audio)
                video.write_videofile(final_video_path, codec='libx264', audio_codec='aac', fps=fps)

    except Exception as e:
        raise Exception(f"Ошибка добавления аудио к видео {temp_video_path}: {e}")

def modify_video(input_file, output_folder, audio_path, errors):
    """
    Модифицирует видеофайл: обрабатывает его и добавляет аудиодорожку.

    Параметры:
    input_file (str): Путь к исходному видеофайлу.
    output_folder (str): Путь к папке для сохранения измененного видео.
    audio_path (str): Путь к аудиофайлу, который будет добавлен к видео.
    errors (list): Список для сохранения сообщений об ошибках.

    Возвращает:
    None
    """
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    input_path = input_file
    output_path = os.path.join(output_folder, os.path.basename(input_file))
    process_video(input_path, output_path, audio_path, errors)

def modify_videos(input_folder, output_folder, audio_path):
    """
    Модифицирует все видеофайлы в указанной папке и добавляет к ним аудиодорожки.

    Параметры:
    input_folder (str): Путь к папке с исходными видеофайлами.
    output_folder (str): Путь к папке для сохранения измененных видеофайлов.
    audio_path (str): Путь к аудиофайлу, который будет добавлен к видео.

    Возвращает:
    list: Список сообщений об ошибках, возникших при обработке видеофайлов.
    """
    input_files = [os.path.join(input_folder, f) for f in os.listdir(input_folder) if f.endswith('.mp4')]
    errors = []

    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = [executor.submit(modify_video, input_file, output_folder, audio_path, errors) for input_file in input_files]

        for future in concurrent.futures.as_completed(futures):
            try:
                future.result()
            except Exception as e:
                errors.append(str(e))

    return errors
