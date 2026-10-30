# PromptShield demo video script, under 3 minutes

Total target: 2 minutes 30 seconds. Record the screen, no copyrighted music, no third party trademarks in the video other than the tools actually used.

## Shot list

0:00 to 0:15, Hook and problem
- Show the PromptShield home page.
- Say: "Every LLM app will follow instructions from anyone who can type into it. One prompt can undo the product around the model."
- Show the example injection prompt on screen.

0:15 to 0:45, Unprotected vs protected
- Say: "Without a guard, that prompt goes straight to the model. With PromptShield, it is blocked before it reaches the model."
- Click the obvious injection example, click Check prompt, show BLOCKED with explanation.
- Click the benign example, click Check prompt, show ALLOWED.

0:45 to 1:15, Baseline vs Nemotron, and rewritten injections
- Click the rewritten injection example.
- Say: "Keyword filters miss rewritten injections. That is why PromptShield uses Nemotron for semantic screening, with a TF-IDF baseline shown beside it for comparison."
- Show baseline verdict, rule hits, and mode. If you are in local demo mode, say so on camera: "This recording uses local demo screening. Live Nemotron mode uses the same guard code with a Token Factory key." Do not claim a local check was a Nemotron call.

1:15 to 1:50, Evaluation, Tavily, and image check
- Click Run evaluation. Read the numbers out loud: accuracy, false positives, false negatives, separately.
- Click Load Tavily results. Say whether it is live or fallback, exactly as shown on screen.
- If OpenCV and OCR are installed, upload an image with text and show the extracted text being screened. If they are not installed, skip this shot, do not fake it.

1:50 to 2:30, How it is built and close
- Show the repo structure briefly: guard.py, app.py, evaluate.py, Dockerfile, README.
- Say: "PromptShield is an LLM firewall on Nemotron, built on Nebius Token Factory. It screens every prompt, blocks injections with a reason, and lets benign prompts through. The code, setup steps, and evaluation are in the public repo."
- End on the home page with the title visible.

## Recording checklist, before you upload

- Demo app runs without errors, all buttons you click in the video work.
- Mode labels are visible: local_demo or nemotron, live or fallback for Tavily.
- Video is under 3 minutes, public on YouTube, and the link works.
- No placeholder numbers are read out. If evaluation numbers change after a new run, re-record that 20 second section or update the on screen numbers.
