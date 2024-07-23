import cv2
import os
import numpy as np
import time

def stack_videos_vertically(video1_path, video2_path, output_path):
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
    
    if width1 != width2 or fps1 != fps2:
        print("Os vídeos devem ter a mesma largura e taxa de quadros.")
        return
    
    combined_height = height1 + height2
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_path, fourcc, fps1, (width1, combined_height))
    
    frame_count = 0
    while True:
        ret1, frame1 = cap1.read()
        ret2, frame2 = cap2.read()
        
        if not ret1 or not ret2:
            break
        
        combined_frame = np.vstack((frame1, frame2))
        out.write(combined_frame)
        frame_count += 1
        
        if frame_count % 50 == 0:
            print(f"Processado {frame_count} frames...")
    
    cap1.release()
    cap2.release()
    out.release()
    
    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"Vídeo combinado processado com sucesso: {output_path} em {elapsed_time:.2f} segundos")
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

    if len(os.listdir(input_dir)) < 2:
        create_example_video(os.path.join(input_dir, "example1.mp4"))
        create_example_video(os.path.join(input_dir, "example2.mp4"))

    return input_dir, output_dir

base_dir = os.path.dirname(os.path.abspath(__file__))
input_directory, output_directory = create_directories_and_example_videos(base_dir)

video_files = [f for f in os.listdir(input_directory) if f.endswith(".mp4")]
if len(video_files) < 2:
    print("Precisa de pelo menos dois vídeos na pasta de entrada para empilhar.")
else:
    video1_path = os.path.join(input_directory, video_files[0])
    video2_path = os.path.join(input_directory, video_files[1])
    output_path = os.path.join(output_directory, "stacked_video.mp4")
    output_path = get_unique_output_path(output_path)
    stack_videos_vertically(video1_path, video2_path, output_path)
