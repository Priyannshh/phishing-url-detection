import gradio as gr
import pandas as pd
import joblib
from urllib.parse import urlsplit

artifact = joblib.load("phishing_detector_final.joblib")
model = artifact["model"]
columns = artifact["feature_columns"]

def extract_features(url):
    return {
        "url_length": len(url),
        "digit_count": sum(c.isdigit() for c in url),
        "dot_count": url.count("."),
        "hyphen_count": url.count("-"),
        "at_count": url.count("@"),
        "slash_count": url.count("/"),
        "has_https": int(url.startswith("https://"))
    }

def detect(url):
    url = str(url).strip()

    if not url:
        return "Please enter a URL."

    parsed = urlsplit(url)
    if parsed.scheme not in ("http", "https") or not parsed.hostname:
        return "Enter a complete URL starting with http:// or https://"

    features = pd.DataFrame(
        [extract_features(url)],
        columns=columns
    )

    prediction = int(model.predict(features)[0])
    probabilities = model.predict_proba(features)[0]

    probs = {
        int(label): float(value)
        for label, value in zip(model.classes_, probabilities)
    }

    result = artifact["label_mapping"][prediction]

    return (
        f"## Prediction: {result}\n\n"
        f"Phishing probability: {probs.get(0, 0) * 100:.2f}%\n\n"
        f"Legitimate probability: {probs.get(1, 0) * 100:.2f}%\n\n"
        f"Domain-separated test accuracy: "
        f"{artifact['accuracy'] * 100:.3f}%\n\n"
        "Research prototype only. This tool does not visit or scan websites."
    )

with gr.Blocks(title="Phishing URL Detection System") as demo:
    gr.Markdown("# Phishing URL Detection System")
    url = gr.Textbox(label="Website URL", placeholder="https://example.com")
    button = gr.Button("Check URL", variant="primary")
    output = gr.Markdown()
    button.click(detect, inputs=url, outputs=output)
    url.submit(detect, inputs=url, outputs=output)

if __name__ == "__main__":
    demo.launch()
