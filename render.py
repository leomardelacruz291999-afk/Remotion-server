from flask import Flask, request, jsonify, send_from_directory
from gtts import gTTS
from moviepy.editor import *
import requests
import os
import uuid

app = Flask(__name__)
OUTPUT_DIR = "outputs"
os.makedirs(OUTPUT_DIR, exist_ok=True)

@app.route("/render", methods=["POST"])
def render_video():
    try:
        data = request.get_json()
        quote = data.get("quote", "Stay positive and keep going!")
        image_url = data.get("image_url")
        audio_lang = data.get("lang", "en")

        # Download background image
        img_path = os.path.join(OUTPUT_DIR, f"bg_{uuid.uuid4().hex}.jpg")
        with open(img_path, "wb") as f:
            f.write(requests.get(image_url).content)

        # Generate TTS
        tts_path = os.path.join(OUTPUT_DIR, f"tts_{uuid.uuid4().hex}.mp3")
        tts = gTTS(text=quote, lang=audio_lang)
        tts.save(tts_path)

        # Build video
        clip = ImageClip(img_path, duration=10)
        audio = AudioFileClip(tts_path)
        final = clip.set_audio(audio)

        out_path = os.path.join(OUTPUT_DIR, f"video_{uuid.uuid4().hex}.mp4")
        final.write_videofile(out_path, fps=24, codec="libx264", audio_codec="aac")

        return jsonify({
            "status": "success",
            "video_url": f"/files/{os.path.basename(out_path)}"
        })

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


@app.route("/files/<path:filename>", methods=["GET"])
def serve_file(filename):
    return send_from_directory(OUTPUT_DIR, filename)


if __name__ == "__main__":
    # ✅ Required for Docker/Render/Railway
    app.run(host="0.0.0.0", port=8080)
