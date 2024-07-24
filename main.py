import os
import subprocess
from pydub import AudioSegment

def convert_mp3_to_wav(input_file, output_file):
    subprocess.run([
        'ffmpeg',
        '-i', input_file,
        '-acodec', 'pcm_s16le',
        '-ac', '1',
        '-ar', '16000',
        output_file
    ])

    audio = AudioSegment.from_wav(output_file)
    print(f"Converted file: {output_file}")
    print(f"Channels: {audio.channels}")
    print(f"Sample width: {audio.sample_width * 8} bits")
    print(f"Frame rate: {audio.frame_rate} Hz")
    print(f"Duration: {len(audio) / 1000} seconds")
    return audio

def split_audio(audio, output_dir, base_name, split_duration):
    total_duration = len(audio)
    for i in range(0, total_duration, split_duration * 1000):
        start = i
        end = min(i + split_duration * 1000, total_duration)
        split = audio[start:end]
        split_file = os.path.join(output_dir, f"{base_name}_{i//1000}_{end//1000}.wav")
        split.export(split_file, format="wav")
        print(f"Created split file: {split_file}")

def main():
    split_duration = int(os.environ.get('SPLIT_DURATION', '0'))
    print(f"Split duration: {split_duration} seconds")

    input_dir = '/app/input'
    output_dir = '/app/output'

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    for filename in os.listdir(input_dir):
        if filename.endswith('.mp3'):
            input_path = os.path.join(input_dir, filename)
            base_name = os.path.splitext(filename)[0]
            output_path = os.path.join(output_dir, f"{base_name}.wav")

            audio = convert_mp3_to_wav(input_path, output_path)

            if split_duration > 0:
                print(f"Splitting audio into {split_duration} second segments")
                split_audio(audio, output_dir, base_name, split_duration)
                os.remove(output_path)  # 元のWAVファイルを削除
            else:
                print(f"No splitting requested. Full WAV file saved: {output_path}")

if __name__ == "__main__":
    main()
