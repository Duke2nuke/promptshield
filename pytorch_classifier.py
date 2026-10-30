"""PyTorch baseline classifier for PromptShield.

A small MLP on TF-IDF features, trained on the same dataset as the
scikit-learn baseline, so the two baselines can be compared. This module
only runs if torch is installed. If torch is missing, it reports
unavailable instead of crashing the app. Install torch to use it:
pip install torch --index-url https://download.pytorch.org/whl/cpu
"""
import numpy as np

try:
    import torch
    import torch.nn as nn

    TORCH_AVAILABLE = True

    class MLP(nn.Module):
        def __init__(self, in_dim):
            super().__init__()
            self.net = nn.Sequential(
                nn.Linear(in_dim, 64), nn.ReLU(),
                nn.Linear(64, 32), nn.ReLU(),
                nn.Linear(32, 1),
            )

        def forward(self, x):
            return self.net(x).squeeze(1)

except Exception:  # noqa: BLE001
    TORCH_AVAILABLE = False
    MLP = None


_cached = None


def _train_cached(train_texts, train_labels):
    """Train once and reuse for single-prompt scoring in guard.py.

    Same architecture, seed, epochs and optimiser as train_and_predict,
    so the cached single-prompt model and the evaluation model agree in
    design. Returns (vectorizer, model) or None if torch is unavailable.
    """
    global _cached
    if not TORCH_AVAILABLE:
        return None
    if _cached is not None:
        return _cached
    from sklearn.feature_extraction.text import TfidfVectorizer

    vec = TfidfVectorizer(lowercase=True, ngram_range=(1, 2), max_features=500)
    Xtr = vec.fit_transform(train_texts).toarray().astype(np.float32)
    ytr = np.array(train_labels, dtype=np.float32)
    torch.manual_seed(0)
    model = MLP(Xtr.shape[1])
    opt = torch.optim.Adam(model.parameters(), lr=0.01)
    loss_fn = nn.BCEWithLogitsLoss()
    Xt = torch.tensor(Xtr)
    yt = torch.tensor(ytr)
    model.train()
    for _ in range(120):
        opt.zero_grad()
        out = model(Xt)
        loss = loss_fn(out, yt)
        loss.backward()
        opt.step()
    model.eval()
    _cached = (vec, model)
    return _cached


def predict_probability(text, train_texts, train_labels):
    """Score one prompt with the cached PyTorch MLP, or None if unavailable.

    Returns a float in [0, 1], or None when torch is not installed.
    This is used by guard.check_prompt so every text check carries a
    second, PyTorch-scored baseline alongside the TF-IDF baseline.
    """
    cached = _train_cached(train_texts, train_labels)
    if cached is None:
        return None
    vec, model = cached
    X = vec.transform([text]).toarray().astype(np.float32)
    with torch.no_grad():
        prob = float(torch.sigmoid(model(torch.tensor(X))).numpy()[0])
    return prob


def train_and_predict(train_texts, train_labels, test_texts, vectorizer=None):
    if not TORCH_AVAILABLE:
        return {"available": False, "reason": "torch is not installed in this environment."}
    from sklearn.feature_extraction.text import TfidfVectorizer

    vec = vectorizer or TfidfVectorizer(lowercase=True, ngram_range=(1, 2), max_features=500)
    Xtr = vec.fit_transform(train_texts).toarray().astype(np.float32)
    Xte = vec.transform(test_texts).toarray().astype(np.float32)
    ytr = np.array(train_labels, dtype=np.float32)
    torch.manual_seed(0)
    model = MLP(Xtr.shape[1])
    opt = torch.optim.Adam(model.parameters(), lr=0.01)
    loss_fn = nn.BCEWithLogitsLoss()
    Xt = torch.tensor(Xtr)
    yt = torch.tensor(ytr)
    model.train()
    for _ in range(120):
        opt.zero_grad()
        out = model(Xt)
        loss = loss_fn(out, yt)
        loss.backward()
        opt.step()
    model.eval()
    with torch.no_grad():
        probs = torch.sigmoid(model(torch.tensor(Xte))).numpy().tolist()
    return {"available": True, "probabilities": probs, "model": "PyTorch MLP on TF-IDF features"}
