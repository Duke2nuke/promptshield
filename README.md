# PromptShield, LLM Firewall on Nemotron

## Try it live first, no login required

**Live demo: https://promptshield-tjnp.onrender.com**

Click the live demo link above, type a prompt, and try BLOCKED vs ALLOWED yourself. No login, no key, no install. Free Render tier, so the first load after inactivity may take up to about 50 seconds while it wakes up. The hosted demo runs in local_demo mode, TF-IDF baseline plus rules, with Nemotron live false, unless a Nebius key is set in the host dashboard. Run it locally from the instructions below if you prefer, or use the repo code directly.

PromptShield screens a prompt before it reaches an LLM app. It blocks injection style prompts, explains why, and allows benign prompts through. It is built for the Nebius x NVIDIA Global AI Hackathon, Best Apps and Agents track.

## What it does, in one demo

1. Type a prompt, or click an example.
2. The guard returns BLOCKED or ALLOWED, with a risk score, a baseline verdict, and an explanation.
3. The evaluation page shows accuracy, false positives, and false negatives separately, not just accuracy.
4. The Tavily section loads recent injection research, or clearly labelled fallback links if no Tavily key is set.
5. The image section preprocesses an uploaded image with OpenCV, extracts text with OCR if tesseract is available, and screens the extracted text.

## Modes, stated honestly

- Local demo mode: no Nebius key set. Screening uses the TF-IDF baseline plus rules. Every response says mode is local_demo. This is not a Nemotron call, and the app does not claim otherwise.
- Live Nemotron mode: set NEBIUS_API_KEY in a .env file. The guard calls Nebius Token Factory at https://api.tokenfactory.nebius.com/v1/chat/completions with the model in NEBIUS_MODEL. Verified model IDs, from a live models list call on 30 Oct 2026: Nano nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B, Super nvidia/nemotron-3-super-120b-a12b, Ultra nvidia/Nemotron-3-Ultra-550b-a55b. A live Nano screening test on a benign educational prompt returned ALLOWED, with 200 total tokens. A live Nano evaluation on the 14-prompt TEST set on 31 Oct 2026 returned 14/14 correct, TP 6, FP 0, TN 8, FN 0, with the caveat in EVALUATION.md about one benign reply not following the BLOCKED/ALLOWED format. This does not replace the external-set baseline results.
- Tavily live mode: set TAVILY_API_KEY. Without it, the app shows curated fallback links and says so.
- PyTorch mode, now core: if torch is installed, every /api/check response carries pytorch_probability, pytorch_verdict, and pytorch_available, and /api/evaluate reports the PyTorch MLP separately. Measured 30 Oct 2026 on the 14-prompt test set: PyTorch accuracy 0.857, TP 6, FP 2, TN 6, FN 0, versus main guard 1.000, TP 6, FP 0, TN 8, FN 0. The PyTorch verdict does not override the main verdict. If torch is missing, those fields report unavailable, and the main guard still works.
- OpenCV mode, now core: if opencv-python-headless and tesseract are installed, /api/image-check preprocesses with OpenCV, extracts text with OCR, and screens it with the same guard, including the PyTorch baseline. Measured 30 Oct 2026: benign test image ALLOWED, injection-style test image BLOCKED, both with OCR and OpenCV available. If they are missing, that endpoint reports unavailable, and the main guard still works.

A guard is a layer, not a guarantee. Results on the small demo dataset are not real world security claims.

## Run it locally

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install Flask requests scikit-learn python-dotenv
pip install --no-cache-dir opencv-python-headless pytesseract pillow
pip install --no-cache-dir torch --index-url https://download.pytorch.org/whl/cpu
python3 app.py
```

For the image check, tesseract must also be installed on the system
(for example, apt-get install tesseract-ocr). The Dockerfile installs
it. Without tesseract, OpenCV preprocessing still runs, but OCR reports
unavailable and no text is extracted.

Open http://127.0.0.1:5000

To run the evaluation only:

```bash
python3 evaluate.py
```

## Run it with Docker

```bash
docker build -t promptshield .
docker run -p 5000:5000 promptshield
```

Docker will also try to install torch and opencv from requirements.txt. If you want a light image, remove those two lines from requirements.txt before building. The app still works without them, with those endpoints reporting unavailable.

## Project structure

- app.py: Flask app and API routes
- guard.py: TF-IDF baseline, rules, Nemotron client, main check_prompt function
- data.py: training and test datasets, with labels stated in the file
- evaluate.py: evaluation runner, prints TP, FP, TN, FN
- pytorch_classifier.py: PyTorch MLP baseline, optional
- tavily_client.py: Tavily search client, with fallback
- image_guard.py: OpenCV preprocessing and OCR screening, optional
- templates/index.html, static/css/style.css, static/js/app.js: demo frontend
- Dockerfile, requirements.txt, .env.example

## Nebius and NVIDIA use, for judges

- Nebius Token Factory: Nemotron inference through its OpenAI compatible API, in guard.py, function nemotron_check.
- NVIDIA Nemotron: Nano for fast screening, Super for semantic analysis, Ultra for adjudication and explanation, as designed in the guard tiers. In local demo mode, the tier design is shown in the UI, and the actual model call happens only when a Nebius key is set.
- Tavily: recent injection research enrichment, in tavily_client.py.
- Feedback on Token Factory, AI Cloud, and Nemotron tools: add your real feedback to the Devpost submission form, based on your actual experience setting up the API key and model. Do not copy generic feedback from this README.

## Licence

MIT. See LICENSE.
