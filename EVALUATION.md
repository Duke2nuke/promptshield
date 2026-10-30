# PromptShield evaluation, run 30 Oct 2026

Run with: python3 evaluate.py, in local demo mode, no Nebius key set.

- Total test prompts: 14
- Accuracy: 1.000 (14 out of 14)
- True positives, injection blocked: 6
- False positives, benign blocked: 0
- True negatives, benign allowed: 8
- False negatives, injection allowed: 0

This is a small demo dataset, created for this project, with labels stated in data.py. It is not a real world security claim, and it does not replace the earlier external set results reported in the Devpost story, where the baseline alone scored lower and missed rewritten cases. The value of this run is that the demo app, guard, and evaluation endpoint all work end to end without errors, and the dashboard reports false positives and false negatives separately.
