"""PromptShield demo app.

Flask app, no database, no login. Runs in local demo mode without API
keys, and in live mode when NEBIUS_API_KEY and TAVILY_API_KEY are set.
Every response says which mode it used, so a demo video never claims
a local check was a live Nemotron or Tavily call.
"""
import os
from flask import Flask, jsonify, render_template, request

from data import EXAMPLES, TEST
from evaluate import main as run_evaluation
from guard import check_prompt
from tavily_client import search_latest

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("index.html", examples=EXAMPLES)


@app.route("/api/check", methods=["POST"])
def api_check():
    data = request.get_json(force=True, silent=True) or {}
    result = check_prompt(data.get("prompt", ""))
    if "error" in result:
        return jsonify(result), 400
    return jsonify(result)


@app.route("/api/evaluate")
def api_evaluate():
    return jsonify(run_evaluation())


@app.route("/api/tavily")
def api_tavily():
    return jsonify(search_latest())


@app.route("/api/pytorch")
def api_pytorch():
    try:
        from data import TRAIN
        from pytorch_classifier import train_and_predict

        texts = [t for t, _ in TRAIN]
        labels = [y for _, y in TRAIN]
        test_texts = [t for t, _ in TEST[:4]]
        return jsonify(train_and_predict(texts, labels, test_texts))
    except Exception as e:  # noqa: BLE001
        return jsonify({"available": False, "reason": str(e)})


@app.route("/api/image-check", methods=["POST"])
def api_image_check():
    if "image" not in request.files:
        return jsonify({"error": "No image uploaded. Choose a PNG or JPG file."}), 400
    from image_guard import check_image

    return jsonify(check_image(request.files["image"].read()))


@app.route("/api/health")
def health():
    import shutil

    try:
        from pytorch_classifier import TORCH_AVAILABLE
    except Exception:  # noqa: BLE001
        TORCH_AVAILABLE = False
    try:
        import cv2  # noqa: F401

        opencv_available = True
    except Exception:  # noqa: BLE001
        opencv_available = False
    return jsonify({
        "status": "ok",
        "app": "PromptShield",
        "nemotron_live": bool(os.environ.get("NEBIUS_API_KEY")),
        "tavily_live": bool(os.environ.get("TAVILY_API_KEY")),
        "torch_available": bool(TORCH_AVAILABLE),
        "opencv_available": opencv_available,
        "tesseract_available": shutil.which("tesseract") is not None,
    })


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", "5000")), debug=False)
