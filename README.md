Installation & Setup

git clone https://github.com/dxli94/WLASL.git
cd WLASL/start_kit
Use yt-dlp (recommended) or youtube-dl for video downloading.

Download & Preprocess Videos
Download raw videos


python video_downloader.py
Extract video samples

python preprocess.py
Processed videos will be in videos/ (or your linked storage).

Handling Missing Videos

python find_missing.py
Submit missing.txt via the request form.

Training & Testing
I3D Model
Place videos in WLASL/data/ and download Kinetics-pretrained weights.

Train:

python train_i3d.py
Test with WLASL-pretrained weights:
python test_i3d.py
