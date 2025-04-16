from flask import Flask, request, send_file, jsonify
import yt_dlp
import os
import uuid

app = Flask(__name__)

@app.route('/download', methods=['GET'])
def download():
    url = request.args.get('url')
    format_type = request.args.get('format', 'video')  # video or audio

    if not url:
        return jsonify({"error": "Missing URL"}), 400

    unique_id = str(uuid.uuid4())
    output_path = f"{unique_id}.%(ext)s"

    ydl_opts = {
        'quiet': True,
        'skip_download': True,
        'format': 'bestaudio/best' if format_type == 'audio' else 'best',
        'outtmpl': output_path,
        'cookiefile': 'cookies.txt',
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filepath = ydl.prepare_filename(info)

        return send_file(filepath, as_attachment=True)

    except Exception as e:
        return jsonify({'error': str(e)}), 500

    finally:
        # optional: clean up file after sending (if needed)
        pass
