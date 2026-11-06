from pathlib import Path

code = r'''import json
import re
import time
import requests
import pandas as pd

from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score

API_KEY = "YOUR_OPENROUTER_API_KEY"
URL = "https://openrouter.ai/api/v1/chat/completions"
MODEL = "nvidia/nemotron-3-ultra-550b-a55b:free"

INPUT_FILE = "phishing_email_detection_2026_dataset(1).csv"
OUTPUT_FILE = "llm_1500_results.csv"
MAX_RETRIES = 3
TIMEOUT = 120
ECE_BINS = 10


def classify_email(row):
    prompt = f"""
Classify this email as phishing or legitimate using only the supplied information.

Email ID: {row['email_id']}
Sender: {row['sender_email']}
Subject: {row['subject']}
Has link: {row['has_link']}
Has attachment: {row['has_attachment']}
Urgency score: {row['urgency_score']}
Spelling errors: {row['spelling_errors']}
Email length in words: {row['email_length_words']}

Return exactly this format:
LABEL: phishing
CONFIDENCE: 0.95
REASON: short explanation

The label must be either phishing or legitimate.
Confidence must be a number from 0 to 1 representing confidence in the selected label.
"""

    payload = {
        "model": MODEL,
        "messages": [
            {
                "role": "system",
                "content": "You are an email phishing classification system. Follow the requested output format."
            },
            {"role": "user", "content": prompt}
        ],
        "temperature": 0
    }

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    last_error = None

    for attempt in range(MAX_RETRIES):
        start = time.perf_counter()

        try:
            response = requests.post(
                URL,
                json=payload,
                headers=headers,
                timeout=TIMEOUT
            )

            elapsed = time.perf_counter() - start

            if response.status_code == 429 or response.status_code >= 500:
                last_error = f"API Error {response.status_code}: {response.text}"
                time.sleep(2 ** attempt)
                continue

            if response.status_code != 200:
                raise RuntimeError(
                    f"API Error {response.status_code}: {response.text}"
                )

            result = response.json()
            raw_output = result["choices"][0]["message"]["content"].strip()
            text = raw_output.lower()

            label_match = re.search(
                r"label\s*:\s*(phishing|legitimate)",
                text
            )

            confidence_match = re.search(
                r"confidence\s*:\s*(0(?:\.\d+)?|1(?:\.0+)?)",
                text
            )

            if label_match:
                prediction = label_match.group(1)
            elif re.search(r"\bphishing\b", text):
                prediction = "phishing"
            elif re.search(r"\blegitimate\b", text):
                prediction = "legitimate"
            else:
                prediction = "unknown"

            confidence = (
                float(confidence_match.group(1))
                if confidence_match else 0.5
            )

            if prediction == "phishing":
                phishing_probability = confidence
            elif prediction == "legitimate":
                phishing_probability = 1 - confidence
            else:
                phishing_probability = 0.5

            usage = result.get("usage", {})
            input_tokens = usage.get("prompt_tokens", 0) or 0
            output_tokens = usage.get("completion_tokens", 0) or 0
            total_tokens = usage.get(
                "total_tokens",
                input_tokens + output_tokens
            ) or 0

            actual_cost = usage.get("cost", 0) or 0

            return {
                "prediction": prediction,
                "confidence": confidence,
                "phishing_probability": phishing_probability,
                "raw_output": raw_output,
                "input_tokens": input_tokens,
                "output_tokens": output_tokens,
                "total_tokens": total_tokens,
                "actual_cost": float(actual_cost),
                "time_seconds": elapsed,
                "error": ""
            }

        except Exception as error:
            last_error = str(error)
            if attempt == MAX_RETRIES - 1:
                break
            time.sleep(2 ** attempt)

    return {
        "prediction": "ERROR",
        "confidence": 0,
        "phishing_probability": 0.5,
        "raw_output": "",
        "input_tokens": 0,
        "output_tokens": 0,
        "total_tokens": 0,
        "actual_cost": 0,
        "time_seconds": 0,
        "error": str(last_error)
    }


def calculate_ece(y_true, probabilities, bins=10):
    data = pd.DataFrame({
        "actual": y_true,
        "probability": probabilities
    })

    ece = 0.0

    for index in range(bins):
        lower = index / bins
        upper = (index + 1) / bins

        if index == bins - 1:
            group = data[
                (data["probability"] >= lower) &
                (data["probability"] <= upper)
            ]
        else:
            group = data[
                (data["probability"] >= lower) &
                (data["probability"] < upper)
            ]

        if len(group) == 0:
            continue

        average_confidence = group["probability"].mean()
        observed_rate = group["actual"].mean()

        ece += (
            len(group) / len(data)
        ) * abs(average_confidence - observed_rate)

    return ece


def main():
    if API_KEY == "YOUR_OPENROUTER_API_KEY":
        raise ValueError("Replace YOUR_OPENROUTER_API_KEY with your API key.")

    df = pd.read_csv(INPUT_FILE)

    required_columns = [
        "email_id",
        "sender_email",
        "subject",
        "has_link",
        "has_attachment",
        "urgency_score",
        "spelling_errors",
        "email_length_words",
        "is_phishing"
    ]

    missing = [column for column in required_columns if column not in df.columns]

    if missing:
        raise ValueError(
            f"Missing columns: {missing}. Found columns: {list(df.columns)}"
        )

    df = df[required_columns].copy()
    df["true_label"] = df["is_phishing"].apply(
        lambda value: "phishing"
        if str(value).strip().lower() in ["1", "1.0", "true", "yes", "phishing"]
        else "legitimate"
    )

    print("=" * 65)
    print("PHISHING EMAIL DETECTION - MODEL EVALUATION")
    print("=" * 65)
    print(f"Model: {MODEL}")
    print(f"Dataset: {INPUT_FILE}")
    print(f"Emails: {len(df)}")
    print("=" * 65)

    results = []
    total_start = time.perf_counter()

    for index, row in df.iterrows():
        result = classify_email(row)

        record = {
            "email_id": row["email_id"],
            "sender_email": row["sender_email"],
            "subject": row["subject"],
            "true_label": row["true_label"],
            **result
        }

        results.append(record)

        completed = index + 1

        if result["prediction"] == "ERROR":
            print(f"{completed}/{len(df)} | ERROR | {result['error'][:180]}")
        else:
            print(
                f"{completed}/{len(df)} | "
                f"Prediction: {result['prediction'].upper()} | "
                f"Confidence: {result['confidence']:.3f} | "
                f"Time: {result['time_seconds']:.2f}s | "
                f"Tokens: {result['total_tokens']}"
            )

        if completed % 50 == 0:
            pd.DataFrame(results).to_csv(OUTPUT_FILE, index=False)
            print(f"--- {completed} emails processed; interim results saved ---")

    total_time = time.perf_counter() - total_start

    results_df = pd.DataFrame(results)
    results_df.to_csv(OUTPUT_FILE, index=False)

    valid = results_df[results_df["prediction"].isin(
        ["phishing", "legitimate"]
    )].copy()

    if len(valid) == 0:
        print("No successful predictions. Check your API key, model name and API errors.")
        print(f"Error details saved in {OUTPUT_FILE}")
        return

    y_true = (valid["true_label"] == "phishing").astype(int)
    y_pred = (valid["prediction"] == "phishing").astype(int)
    probabilities = valid["phishing_probability"].astype(float)

    accuracy = accuracy_score(y_true, y_pred)
    precision = precision_score(y_true, y_pred, zero_division=0)
    recall = recall_score(y_true, y_pred, zero_division=0)
    f1 = f1_score(y_true, y_pred, zero_division=0)

    brier_score = ((probabilities - y_true) ** 2).mean()
    ece = calculate_ece(y_true, probabilities, ECE_BINS)

    total_input_tokens = results_df["input_tokens"].sum()
    total_output_tokens = results_df["output_tokens"].sum()
    total_tokens = results_df["total_tokens"].sum()
    actual_cost = results_df["actual_cost"].sum()

    average_latency = valid["time_seconds"].mean()
    first_response_time = (
        results[0]["time_seconds"] if results else 0
    )

    cost_per_1000 = (
        actual_cost / len(valid) * 1000
        if actual_cost > 0 else 0
    )

    print()
    print("=" * 65)
    print("FINAL EVALUATION RESULTS")
    print("=" * 65)
    print(f"Model                    : {MODEL}")
    print(f"Dataset emails           : {len(df)}")
    print(f"Successful predictions   : {len(valid)}")
    print(f"Failed predictions       : {len(df) - len(valid)}")
    print("-" * 65)
    print(f"Accuracy                 : {accuracy * 100:.2f}%")
    print(f"Precision                : {precision * 100:.2f}%")
    print(f"Recall                   : {recall * 100:.2f}%")
    print(f"F1 Score                 : {f1 * 100:.2f}%")
    print("-" * 65)
    print(f"Brier Score              : {brier_score:.4f}")
    print(f"ECE                      : {ece:.4f}")
    print("-" * 65)
    print(f"Total execution time     : {total_time:.2f} seconds")
    print(f"Total execution time     : {total_time / 60:.2f} minutes")
    print(f"First response time      : {first_response_time:.2f} seconds")
    print(f"Average latency          : {average_latency:.2f} seconds/email")
    print("-" * 65)
    print(f"Input tokens              : {total_input_tokens}")
    print(f"Output tokens             : {total_output_tokens}")
    print(f"Total tokens              : {total_tokens}")
    print("-" * 65)

    if actual_cost > 0:
        print(f"Actual API cost           : ${actual_cost:.8f}")
        print(f"Cost per 1,000 decisions  : ${cost_per_1000:.6f}")
    else:
        print("Actual API cost           : Not reported by API")
        print("Cost per 1,000 decisions  : Not available")

    print("-" * 65)
    print(f"Results saved             : {OUTPUT_FILE}")
    print("=" * 65)


if __name__ == "__main__":
    main()
'''

path = Path("/mnt/data/phishing_single_model.py")
path.write_text(code, encoding="utf-8")
print(path)
