"""Run PromptShield evaluation on the TEST set in data.py.

Prints accuracy, false positives, false negatives, and per case results.
Run: python3 evaluate.py
"""
from data import TEST
from guard import check_prompt


def main():
    tp = fp = tn = fn = 0
    rows = []
    for text, label in TEST:
        result = check_prompt(text)
        pred = 1 if result["verdict"] == "BLOCKED" else 0
        if label == 1 and pred == 1:
            tp += 1
        elif label == 0 and pred == 1:
            fp += 1
        elif label == 0 and pred == 0:
            tn += 1
        else:
            fn += 1
        rows.append({"prompt": text, "label": label, "predicted": pred, "verdict": result["verdict"], "mode": result["mode"]})
    total = len(TEST)
    acc = (tp + tn) / total if total else 0
    print(f"Total: {total}")
    print(f"Accuracy: {acc:.3f} ({tp + tn}/{total})")
    print(f"True positives (injection blocked): {tp}")
    print(f"False positives (benign blocked): {fp}")
    print(f"True negatives (benign allowed): {tn}")
    print(f"False negatives (injection allowed): {fn}")
    for r in rows:
        print(f"- label={r['label']} pred={r['predicted']} {r['verdict']} :: {r['prompt']}")
    return {"total": total, "accuracy": acc, "tp": tp, "fp": fp, "tn": tn, "fn": fn, "rows": rows}


if __name__ == "__main__":
    main()
