"""Run PromptShield evaluation on the TEST set in data.py.

Prints accuracy, false positives, false negatives, and per case results.
Run: python3 evaluate.py
"""
from data import TEST, TRAIN
from guard import check_prompt


def pytorch_evaluation():
    """Score the same TEST set with the PyTorch MLP alone, honestly.

    Returns TP/FP/TN/FN for the PyTorch verdict at 0.5, or
    available=False when torch is not installed. This is a second
    baseline, not the main guard verdict.
    """
    try:
        from pytorch_classifier import train_and_predict

        texts = [t for t, _ in TRAIN]
        labels = [y for _, y in TRAIN]
        test_texts = [t for t, _ in TEST]
        result = train_and_predict(texts, labels, test_texts)
        if not result.get("available"):
            return {"available": False, "reason": result.get("reason", "torch not available")}
        probs = result["probabilities"]
        tp = fp = tn = fn = 0
        for prob, (_, label) in zip(probs, TEST):
            pred = 1 if prob >= 0.5 else 0
            if label == 1 and pred == 1:
                tp += 1
            elif label == 0 and pred == 1:
                fp += 1
            elif label == 0 and pred == 0:
                tn += 1
            else:
                fn += 1
        total = len(TEST)
        return {
            "available": True,
            "model": result.get("model"),
            "total": total,
            "accuracy": (tp + tn) / total if total else 0,
            "tp": tp,
            "fp": fp,
            "tn": tn,
            "fn": fn,
        }
    except Exception as e:  # noqa: BLE001
        return {"available": False, "reason": str(e)}


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
    pytorch = pytorch_evaluation()
    print("PyTorch MLP baseline:")
    print(pytorch)
    return {"total": total, "accuracy": acc, "tp": tp, "fp": fp, "tn": tn, "fn": fn, "rows": rows, "pytorch": pytorch}


if __name__ == "__main__":
    main()
