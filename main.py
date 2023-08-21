import os
import yt_dlp
import sys
from pydub import AudioSegment

def download_video(url, output_path):
    ydl_opts = {
        'format': 'm4a/bestaudio/best',
        # ℹ️ See help(yt_dlp.postprocessor) for a list of available Postprocessors and their arguments
        'postprocessors': [{  # Extract audio using ffmpeg
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'wav',
        }],
        'outtmpl': f"{output_path}%(uploader)s/audio_%(id)s"
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)
        info = ydl.sanitize_info(info)
        error_code = ydl.download(url)
        split_audio(f"{output_path}{info.get('uploader')}/",
                    f"{output_path}{info.get('uploader')}/", 30)


def split_audio(input_path, output_path, max_duration):
    if not os.path.exists(output_path):
        os.makedirs(output_path)

    for filename in os.listdir(input_path):
        if filename.endswith(".wav"):
            input_file = os.path.join(input_path, filename)
            audio = AudioSegment.from_wav(input_file)

            start_time = 0
            chunk_num = 1

            while start_time < len(audio):
                end_time = start_time + max_duration * 60 * 1000
                if end_time > len(audio):
                    end_time = len(audio)

                chunk = audio[start_time:end_time]
                output_filename = os.path.join(output_path, f"{os.path.splitext(filename)[0]}_part{chunk_num}.wav")
                chunk.export(output_filename, format="wav")

                start_time = end_time
                chunk_num += 1
            os.remove(input_file)
            print(f"Archivo original '{filename}' dividido y eliminado.")


if __name__ == "__main__":
    if len(sys.argv) > 0:
        youtube_url = sys.argv[1]
        output_directory = "dataset/"

        download_video(youtube_url, output_directory)
