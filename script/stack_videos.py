import cv2
import os
import numpy as np
import time
import subprocess

def resize_frame(frame, width, height):
    return cv2.resize(frame, (width, height))

def adjust_fps(video_path, target_fps, temp_path):
    cap = cv2.VideoCapture(video_path)
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    
    out = cv2.VideoWriter(temp_path, fourcc, target_fps, (width, height))
    
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        out.write(frame)
    
    cap.release()
    out.release()
    
    os.remove(video_path)
    os.rename(temp_path, video_path)

def stack_videos_vertically(video1_path, video2_path, output_path, ffmpeg_path):
    print(f"Processando vídeos: {video1_path} e {video2_path}")
    start_time = time.time()
    
    cap1 = cv2.VideoCapture(video1_path)
    cap2 = cv2.VideoCapture(video2_path)

    if not cap1.isOpened() or not cap2.isOpened():
        print(f"Erro ao abrir um dos vídeos.")
        return
    
    width1 = int(cap1.get(cv2.CAP_PROP_FRAME_WIDTH))
    height1 = int(cap1.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps1 = cap1.get(cv2.CAP_PROP_FPS)
    
    width2 = int(cap2.get(cv2.CAP_PROP_FRAME_WIDTH))
    height2 = int(cap2.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps2 = cap2.get(cv2.CAP_PROP_FPS)
    
    target_width = min(width1, width2)
    target_height = min(height1, height2)
    target_fps = min(fps1, fps2)
    
    if width1 != target_width or height1 != target_height:
        temp1_path = video1_path.replace('.mp4', '_temp.mp4')
        adjust_fps(video1_path, target_fps, temp1_path)
        cap1.release()
        cap1 = cv2.VideoCapture(video1_path)

    if width2 != target_width or height2 != target_height:
        temp2_path = video2_path.replace('.mp4', '_temp.mp4')
        adjust_fps(video2_path, target_fps, temp2_path)
        cap2.release()
        cap2 = cv2.VideoCapture(video2_path)
    
    combined_height = target_height * 2
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    temp_output_path = output_path.replace('.mp4', '_no_audio.mp4')
    out = cv2.VideoWriter(temp_output_path, fourcc, target_fps, (target_width, combined_height))
    
    frame_count = 0
    while True:
        ret1, frame1 = cap1.read()
        ret2, frame2 = cap2.read()
        
        if not ret1 or not ret2:
            break
        
        frame1 = resize_frame(frame1, target_width, target_height)
        frame2 = resize_frame(frame2, target_width, target_height)
        combined_frame = np.vstack((frame1, frame2))
        out.write(combined_frame)
        frame_count += 1
        
        if frame_count % 50 == 0:
            print(f"Processado {frame_count} frames...")
    
    cap1.release()
    cap2.release()
    out.release()
    
    # Adicionar o áudio do primeiro vídeo (video1_path) ao vídeo combinado
    final_output_path = output_path
    subprocess.run([ffmpeg_path, '-i', temp_output_path, '-i', video1_path, '-c', 'copy', '-map', '0:v:0', '-map', '1:a:0', final_output_path])
    os.remove(temp_output_path)
    
    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"Vídeo combinado processado com sucesso: {final_output_path} em {elapsed_time:.2f} segundos")
    return elapsed_time

def get_unique_output_path(output_path):
    base, ext = os.path.splitext(output_path)
    counter = 1
    new_output_path = output_path
    while os.path.exists(new_output_path):
        new_output_path = f"{base}_{counter}{ext}"
        counter += 1
    return new_output_path

def create_example_video(path):
    width, height = 640, 480
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    fps = 30
    out = cv2.VideoWriter(path, fourcc, fps, (width, height))
    frame = np.zeros((height, width, 3), np.uint8)
    cv2.putText(frame, "Exemplo", (50, height // 2), cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 255), 3)
    for _ in range(fps * 5):  # 5 segundos de vídeo
        out.write(frame)
    out.release()

def create_directories_and_example_videos(base_dir):
    input_dir = os.path.join(base_dir, "video-input")
    output_dir = os.path.join(base_dir, "video-output")

    os.makedirs(input_dir, exist_ok=True)
    os.makedirs(output_dir, exist_ok=True)

    subdirs = [os.path.join(input_dir, d) for d in os.listdir(input_dir) if os.path.isdir(os.path.join(input_dir, d))]
    
    for subdir in subdirs:
        if len(os.listdir(subdir)) < 2:
            create_example_video(os.path.join(subdir, "example1.mp4"))
            create_example_video(os.path.join(subdir, "example2.mp4"))

    return input_dir, output_dir

base_dir = os.path.dirname(os.path.abspath(__file__))
input_directory, output_directory = create_directories_and_example_videos(base_dir)

ffmpeg_path = "C:\\ffmpeg\\bin\\ffmpeg.exe"  # Altere para o caminho do seu FFmpeg

subdirs = [os.path.join(input_directory, d) for d in os.listdir(input_directory) if os.path.isdir(os.path.join(input_directory, d))]

for subdir in subdirs:
    video_files = [f for f in os.listdir(subdir) if f.endswith(".mp4")]
    if len(video_files) < 2:
        print(f"Precisa de pelo menos dois vídeos na pasta {subdir} para empilhar.")
    else:
        video1_path = os.path.join(subdir, video_files[0])
        video2_path = os.path.join(subdir, video_files[1])
        output_path = os.path.join(output_directory, f"{os.path.basename(subdir)}_stacked_video.mp4")
        output_path = get_unique_output_path(output_path)
        stack_videos_vertically(video1_path, video2_path, output_path, ffmpeg_path)
