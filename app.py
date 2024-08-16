from flask import Flask, render_template, request, send_file
import yt_dlp
import os
import uuid

app = Flask(__name__)

DOWNLOAD_FOLDER = 'downloads'
if not os.path.exists(DOWNLOAD_FOLDER):
    os.makedirs(DOWNLOAD_FOLDER)

def download_video(url, output_path):
    ydl_opts = {
        'outtmpl': os.path.join(output_path, '%(title)s.%(ext)s'),
        'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/mp4'
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        filename = ydl.prepare_filename(info)
        return filename

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        video_url = request.form['url']
        try:
            unique_folder = os.path.join(DOWNLOAD_FOLDER, str(uuid.uuid4()))
            os.makedirs(unique_folder)
            file_path = download_video(video_url, unique_folder)
            return send_file(file_path, as_attachment=True)
        except Exception as e:
            return f"An error occurred: {str(e)}"
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)