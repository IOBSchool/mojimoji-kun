# もじもじくん 裏方サーバー：FB/インスタのリンクから音声だけを取り出して返す
import os, tempfile, glob
from flask import Flask, request, send_file, jsonify, after_this_request
import yt_dlp

app = Flask(__name__)
TOKEN = os.environ.get("TOKEN", "")


@app.after_request
def cors(resp):
    resp.headers["Access-Control-Allow-Origin"] = "*"
    return resp


@app.get("/")
def health():
    return "mojimoji ok"


@app.get("/audio")
def audio():
    if not TOKEN or request.args.get("token") != TOKEN:
        return jsonify(error="合言葉がちがいます"), 403
    url = request.args.get("url", "")
    if not url.startswith("http"):
        return jsonify(error="リンクが正しくありません"), 400
    tmp = tempfile.mkdtemp()
    opts = {
        # ffmpegを使わずに済むよう、音声だけのファイルをそのまま取る（無ければ動画ごと）
        "format": "ba[ext=m4a]/ba/b[ext=mp4]/b",
        "outtmpl": os.path.join(tmp, "a.%(ext)s"),
        "quiet": True,
        "noplaylist": True,
        "max_filesize": 100 * 1024 * 1024,
    }
    try:
        with yt_dlp.YoutubeDL(opts) as ydl:
            ydl.download([url])
    except Exception as e:
        return jsonify(error="音声を取り出せませんでした：" + str(e)[:200]), 502
    files = glob.glob(os.path.join(tmp, "a.*"))
    if not files:
        return jsonify(error="音声を取り出せませんでした"), 502

    @after_this_request
    def cleanup(resp):
        for f in files:
            try:
                os.remove(f)
            except OSError:
                pass
        return resp

    return send_file(files[0])
