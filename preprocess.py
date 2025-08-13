import os
import json
import cv2
import shutil
from pathlib import Path

# Base storage directory on your external hard drive
BASE_DIR = Path(r"D:\videos")
RAW_DIR = BASE_DIR / "raw_videos_mp4"
PROCESSED_DIR = BASE_DIR / "processed"

def convert_everything_to_mp4():
    cmd = 'bash scripts/swf2mp4.sh'
    os.system(cmd)

def video_to_frames(video_path, size=None):
    cap = cv2.VideoCapture(str(video_path))
    frames = []
    while True:
        ret, frame = cap.read()
        if ret:
            if size:
                frame = cv2.resize(frame, size)
            frames.append(frame)
        else:
            break
    cap.release()
    return frames

def convert_frames_to_video(frame_array, path_out, size, fps=25):
    out = cv2.VideoWriter(str(path_out), cv2.VideoWriter_fourcc(*'mp4v'), fps, size)
    for frame in frame_array:
        out.write(frame)
    out.release()

def extract_frame_as_video(src_video_path, start_frame, end_frame):
    frames = video_to_frames(src_video_path)
    return frames[start_frame: end_frame+1]

def extract_all_yt_instances(content):
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
    cnt = 1
    for entry in content:
        for inst in entry['instances']:
            url = inst['url']
            video_id = inst['video_id']

            if 'youtube' in url or 'youtu.be' in url:
                cnt += 1
                yt_identifier = url[-11:]
                src_video_path = RAW_DIR / f"{yt_identifier}.mp4"
                dst_video_path = PROCESSED_DIR / f"{video_id}.mp4"

                if not src_video_path.exists():
                    continue
                if dst_video_path.exists():
                    print(f"{dst_video_path} exists.")
                    continue

                start_frame = inst['frame_start'] - 1
                end_frame = inst['frame_end'] - 1

                if end_frame <= 0:
                    shutil.copyfile(src_video_path, dst_video_path)
                    continue

                selected_frames = extract_frame_as_video(src_video_path, start_frame, end_frame)
                size = selected_frames[0].shape[:2][::-1]
                convert_frames_to_video(selected_frames, dst_video_path, size)

                print(cnt, dst_video_path)
            else:
                cnt += 1
                src_video_path = RAW_DIR / f"{video_id}.mp4"
                dst_video_path = PROCESSED_DIR / f"{video_id}.mp4"

                if dst_video_path.exists():
                    print(f"{dst_video_path} exists.")
                    continue
                if not src_video_path.exists():
                    continue

                print(cnt, dst_video_path)
                shutil.copyfile(src_video_path, dst_video_path)

def main():
    
    content = json.load(open('WLASL_v0.3.json'))
    extract_all_yt_instances(content)

if __name__ == "__main__":
    main()
