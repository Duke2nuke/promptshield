async function postJSON(url, body) {
  const r = await fetch(url, { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify(body) });
  return r.json();
}
function show(id, text) {
  const el = document.getElementById(id);
  el.classList.remove("hidden");
  el.textContent = text;
}
document.getElementById("checkBtn").onclick = async () => {
  const prompt = document.getElementById("prompt").value;
  const data = await postJSON("/api/check", { prompt });
  if (data.error) { show("result", "Error: " + data.error); return; }
  show("result", `Verdict: ${data.verdict}\nRisk: ${data.risk}\nMode: ${data.mode}\nBaseline: ${data.baseline_verdict} (${data.baseline_probability})\nExplanation: ${data.explanation}`);
};
document.getElementById("evalBtn").onclick = async () => {
  const data = await fetch("/api/evaluate").then(r => r.json());
  show("eval", `Evaluation on ${data.total} test prompts\nAccuracy: ${data.accuracy}\nTrue positives: ${data.tp}\nFalse positives: ${data.fp}\nTrue negatives: ${data.tn}\nFalse negatives: ${data.fn}`);
};
document.getElementById("tavilyBtn").onclick = async () => {
  const data = await fetch("/api/tavily").then(r => r.json());
  const lines = data.results.map(x => `- ${x.title}: ${x.url}`).join("\n");
  show("tavily", `Mode: ${data.mode}\n${data.note || ""}\n${lines}`);
};
document.getElementById("imageBtn").onclick = async () => {
  const file = document.getElementById("imageFile").files[0];
  if (!file) { show("imageResult", "Choose an image first."); return; }
  const form = new FormData();
  form.append("image", file);
  const data = await fetch("/api/image-check", { method: "POST", body: form }).then(r => r.json());
  show("imageResult", JSON.stringify(data, null, 2));
};
document.querySelectorAll(".example").forEach(btn => {
  btn.onclick = () => { document.getElementById("prompt").value = btn.dataset.text; };
});
