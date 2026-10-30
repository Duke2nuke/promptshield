# PromptShield, LLM Firewall on Nemotron

PromptShield screens a prompt before it reaches an LLM app. It blocks injection style prompts, explains why, and allows benign prompts through. It is built for the Nebius x NVIDIA Global AI Hackathon, Best Apps and Agents track.

## What it does, in one demo

1. Type a prompt, or click an example.
2. The guard returns BLOCKED or ALLOWED, with a risk score, a baseline verdict, and an explanation.
3. The evaluation page shows accuracy, false positives, and false negatives separately, not just accuracy.
4. The Tavily section loads recent injection research, or clearly labelled fallback links if no Tavily key is set.
5. The image section preprocesses an uploaded image with OpenCV, extracts text with OCR if tesseract is available, and screens the extracted text.

## Modes, stated honestly

- Local demo mode: no Nebius key set. Screening uses the TF-IDF baseline plus rules. Every response says mode is local_demo. This is not a Nemotron call, and the app does not claim otherwise.
- Live Nemotron mode: set NEBIUS_API_KEY in a .env file. The guard calls Nebius Token Factory at https://api.tokenfactory.nebius.com/v1/chat/completions with the model in NEBIUS_MODEL. The default model name in .env.example is a placeholder to change to the exact model ID in your Token Factory account.
- Tavily live mode: set TAVILY_API_KEY. Without it, the app shows curated fallback links and says so.
- PyTorch mode: if torch is installed, /api/pytorch trains a small MLP on TF-IDF features. If torch is missing, that endpoint reports unavailable, and the main guard still works.
- OpenCV mode: if opencv-python-headless and tesseract are installed, image checking works. If they are missing, that endpoint reports unavailable, and the main guard still works.

A guard is a layer, not a guarantee. Results on the small demo dataset are not real world security claims.

## Run it locally

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install Flask requests scikit-learn python-dotenv
python3 app.py
```

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
