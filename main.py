import os
import subprocess
from pydub import AudioSegment

def convert_mp3_to_wav(input_file, output_file):
    # FFmpegを使用してMP3をWAVに変換
    subprocess.run([
        'ffmpeg',
        '-i', input_file,
        '-acodec', 'pcm_s16le',
        '-ac', '1',
        '-ar', '16000',
        output_file
    ])

    # pydubを使用して音声ファイルの情報を確認
    audio = AudioSegment.from_wav(output_file)
    print(f"Converted file: {output_file}")
    print(f"Channels: {audio.channels}")
    print(f"Sample width: {audio.sample_width * 8} bits")
    print(f"Frame rate: {audio.frame_rate} Hz")

def main():
    input_dir = '/app/input'
    output_dir = '/app/output'

    # 出力ディレクトリが存在しない場合は作成
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # 入力ディレクトリ内のすべてのMP3ファイルを変換
    for filename in os.listdir(input_dir):
        if filename.endswith('.mp3'):
            input_path = os.path.join(input_dir, filename)
            output_path = os.path.join(output_dir, f"{os.path.splitext(filename)[0]}.wav")
            convert_mp3_to_wav(input_path, output_path)

if __name__ == "__main__":
    main()

    import subprocess
    subprocess.call('PAUSE', shell=True)
