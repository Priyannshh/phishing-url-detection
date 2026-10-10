# Phishing URL Detection System

Random Forest research prototype for classifying URLs.

## Features
- Seven numerical URL-text features
- Interactive Gradio web interface
- Saved model for predictions without retraining

## Evaluation
- Domain-separated accuracy: 99.581%
- Phishing precision: 99.828%
- Phishing recall: 99.200%
- Phishing F1-score: 99.513%

Metrics apply to the selected dataset and split; real-world performance may differ.

## Dataset
PhiUSIIL Phishing URL Dataset, UCI Repository, ID 967.

## Run
1. Install compatible Python.
2. Run: pip install -r requirements.txt
3. Run: python app.py

## Limitations
Uses seven URL-text features; does not scan websites or guarantee safety.
Not intended for production blocking decisions.
