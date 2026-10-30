# PromptShield evaluation, run 30 Oct 2026

Run with: python3 evaluate.py, in local demo mode, no Nebius key set.
Torch 2.15.0+cpu and OpenCV 5.0.0 installed in the local venv, tesseract 5.3.4 installed for OCR.

## Main guard (TF-IDF baseline plus rules, local demo mode)

- Total test prompts: 14
- Accuracy: 1.000 (14 out of 14)
- True positives, injection blocked: 6
- False positives, benign blocked: 0
- True negatives, benign allowed: 8
- False negatives, injection allowed: 0

## Live Nemotron Nano evaluation, run 31 Oct 2026

Run with the Nebius Token Factory helper, model nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B, temperature 0, on the same 14-prompt TEST set in data.py. No local_demo or local_demo_fallback results are included in these numbers; all 14 Token Factory calls returned successfully.

- Total test prompts: 14
- Accuracy: 1.000 (14 out of 14)
- True positives, injection blocked: 6
- False positives, benign blocked: 0
- True negatives, benign allowed: 8
- False negatives, injection allowed: 0
- Both rewritten-labelled injection prompts in the test set were blocked.
- Caveat: one benign prompt did not follow the BLOCKED/ALLOWED reply format and was counted as ALLOWED under the guard's non-BLOCKED rule. This is a small demo dataset, not a real-world security claim, and Super and Ultra were not evaluated in this run.

## PyTorch MLP baseline, same test set, scored separately

This is a second baseline, reported on every check in guard.py, not the
main guard verdict. It does not override the main verdict.

- Total test prompts: 14
- Accuracy: 0.857 (12 out of 14)
- True positives, injection blocked: 6
- False positives, benign blocked: 2
- True negatives, benign allowed: 6
- False negatives, injection allowed: 0

The PyTorch MLP is weaker on false positives than the main guard on
this small set. That is reported here instead of hidden, and it is why
the main verdict is not replaced by the PyTorch verdict.

## Image check, verified locally

- OpenCV preprocessing: grayscale, 1.5x resize, Otsu threshold, verified
  on rendered test images, original shape 200x900, processed shape 300x1350.
- OCR: tesseract 5.3.4, text extracted correctly on both test images.
- Benign test image: verdict ALLOWED, OCR available, OpenCV available,
  PyTorch verdict ALLOWED.
- Injection-style test image: verdict BLOCKED, OCR available, OpenCV
  available, PyTorch verdict BLOCKED.

This is a small demo dataset, created for this project, with labels stated in data.py. It is not a real world security claim, and it does not replace the earlier external set results reported in the Devpost story, where the baseline alone scored lower and missed rewritten cases. The value of this run is that the demo app, guard, evaluation endpoint, PyTorch baseline, and image check all work end to end without errors, and the dashboard reports false positives and false negatives separately, for both baselines.
