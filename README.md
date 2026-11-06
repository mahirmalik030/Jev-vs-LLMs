Jev vs LLMs: Comparative Analysis for Phishing Email Detection

This repository contains the dataset, Python implementation, and supporting research materials for a comparative study of Jev 1.13 and Large Language Models (LLMs) for phishing email detection. The study examines classification performance, probability calibration, response time, token consumption, and API cost.

The LLM experiments use the OpenRouter API to send email classification requests to the selected language model.

About

Phishing emails attempt to deceive recipients into sharing information or taking unsafe actions. This research compares AI-based approaches for identifying phishing and legitimate emails.

The project evaluates models using classification metrics, calibration metrics, and efficiency measurements. The same dataset and evaluation approach should be used when comparing model results.

Models Evaluated

The research considers the following models:

Jev 1.13

Gemini 3.5 Flash-Lite

NVIDIA Nemotron 3 Ultra

Meta Llama 4 Maverick

Note: The supplied Python script is configured to call one OpenRouter model at a time. To evaluate another OpenRouter model, change the model identifier in the script and run the experiment again. Jev must be run using the Jev implementation and procedure used in the research; the OpenRouter script does not execute Jev.

Repository Contents

The project folder contains the following main files:

phishing_metrics_evaluation.py — Python script that sends email records to the configured OpenRouter model, records responses and usage information, and calculates evaluation metrics.

phishing_email_detection_2026_dataset(1).csv — labelled email dataset used by the script.

Keep the Python script and CSV dataset in the same folder unless you update the dataset path in the script.

Tools and Libraries

Python — programming language used for the implementation.

Visual Studio Code (VS Code) — code editor used to open and run the project.

Pandas — reads and processes the CSV dataset.

Requests — sends HTTP requests to the OpenRouter API.

Scikit-learn — calculates accuracy, precision, recall, and F1-score.

OpenRouter API — provides access to the selected LLMs through a common API.

Evaluation Metrics

1. Classification Performance

Accuracy: Percentage of evaluated emails classified correctly.

Precision: Of the emails predicted as phishing, the proportion that were actually phishing.

Recall: Of the actual phishing emails, the proportion correctly identified.

F1-score: Harmonic mean of precision and recall.

2. Probability Calibration

Brier Score: Measures the squared difference between predicted phishing probabilities and the actual labels. Lower values indicate better probability accuracy.

Expected Calibration Error (ECE): Compares average predicted confidence with observed accuracy across confidence bins. Lower values indicate better calibration.

3. Efficiency and Cost

Inference latency: Time taken for an API request to return a model response.

Token consumption: Number of input, output, and total tokens reported by the API.

API cost: Cost reported in the API response, when available.

Initial Configurations

You need the following to run the supplied LLM evaluation script:

A computer running Windows, macOS, or Linux.

Python installed.

Visual Studio Code or another code editor.

An internet connection.

An OpenRouter account and an API key.

The CSV dataset included with the project.

The script sends one API request for each dataset row. Running the complete dataset may take time and may use API credits. Check the selected model's availability, rate limits, and pricing on OpenRouter before starting.

Setup and Running Instructions

Follow the steps below in order. The commands are shown for a typical Windows setup. If python is not recognized on your computer, try py instead.

Step 1: Install Python

Download and install Python from:

https://www.python.org/downloads/

On Windows, select Add Python to PATH during installation if the installer offers that option.

Open Command Prompt or the VS Code terminal and check the installation:

python --version

Step 2: Install Visual Studio Code

Download and install Visual Studio Code:

https://code.visualstudio.com/

Open VS Code after installation.

Step 3: Download the Repository

On the GitHub repository page:

Select the green **Code** button.

Select **Download ZIP**.

Extract the ZIP file to a folder on your computer.

You can also use Git:

git clone YOUR_GITHUB_REPOSITORY_URL

Step 4: Open the Project Folder

In VS Code:

Select **File**.

Select **Open Folder**.

Choose the folder containing the downloaded project.

Confirm that the Python script and CSV dataset are in the same folder.

The folder should look similar to this:

Jev-vs-LLMs/
├── phishing_metrics_evaluation.py
└── phishing_email_detection_2026_dataset(1).csv

The filenames must match the names configured in the Python script. If you rename either file, update the corresponding filename in the script.

Step 5: Install the Required Python Libraries

In VS Code, open the terminal:

Select **Terminal** from the top menu.

Select **New Terminal**.

Run:

python -m pip install pandas requests scikit-learn

Wait for the installation to finish. These are the external Python libraries imported by the supplied script. The script also uses modules included with Python.

Step 6: Create an OpenRouter API Key

The LLM script uses OpenRouter to send requests to the selected model.

Visit https://openrouter.ai/

Sign in or create an account.

Open https://openrouter.ai/keys

Create an API key.

Copy the key and keep it private.

Some models may require credits, and free models may have usage limits. Check the pricing and availability of the model you plan to use.

Step 7: Add Your API Key to the Local Python Script

Open phishing_metrics_evaluation.py in VS Code.

Find the API key setting near the top of the file:

API_KEY = "YOUR_OPENROUTER_API_KEY"

For your local run, replace the placeholder with your own key:

API_KEY = "paste_your_openrouter_key_here"

Save the file.

Security: Do not publish a real API key on GitHub. Before uploading the code, replace your personal key with the placeholder YOUR_OPENROUTER_API_KEY. If a real key has already been published, revoke it and create a new one.

Step 8: Check the Model and Dataset Settings

Near the top of the Python script, check these settings:

MODEL = "nvidia/nemotron-3-ultra-550b-a55b:free"

INPUT_FILE = "phishing_email_detection_2026_dataset(1).csv"

OUTPUT_FILE = "llm_1500_results.csv"

MODEL identifies the OpenRouter model to call. Use a model identifier exactly as listed by OpenRouter.

INPUT_FILE must match the name of your CSV dataset.

OUTPUT_FILE is the name of the CSV file where the script saves its predictions and recorded results.

To test another OpenRouter model, change MODEL and run the script again. Save or rename the previous output file before the next run because the script writes to the same output filename.

Step 9: Run the Python Script

Make sure the VS Code terminal is open in the project folder. Run:

python phishing_metrics_evaluation.py

The script will:

Read the CSV dataset.

Check that the required dataset columns are present.

Send each email record to the configured OpenRouter model.

Read the model's predicted label and confidence.

Record response time, token usage, API cost when provided, and any errors.

Save interim results after every 50 processed records.

Calculate the evaluation metrics for successful predictions.

Save the final per-email results to the output CSV file.

The script prints progress and a final evaluation summary in the terminal.

Dataset Format

The supplied script expects the CSV file to contain these column names:

email_id

sender_email

subject

has_link

has_attachment

urgency_score

spelling_errors

email_length_words

is_phishing

The is_phishing column contains the actual label. The script interprets values such as 1, true, yes, or phishing as phishing; other values are treated as legitimate. Check your dataset labels before running the experiment.

Only share the dataset if you have permission to redistribute it. Do not include private or personally identifying email information unless you have the right to share it.

Output and Results

The script saves per-email predictions and request information to:

llm_1500_results.csv

The output includes fields such as the email ID, actual label, predicted label, confidence, phishing probability, raw model response, token counts, reported API cost, response time, and error information.

The terminal summary reports:

Number of dataset rows.

Number of successful and failed predictions.

Accuracy, precision, recall, and F1-score.

Brier Score and ECE.

Total execution time and average latency.

Input, output, and total tokens.

API cost when the API reports it.

Failed requests are not included in the classification and calibration metrics. Review the error information in the output CSV when requests fail.

Important: The script records API cost only when the OpenRouter response includes a cost value. A displayed cost of zero or “not reported” does not prove that the experiment was free.

Troubleshooting

Python is not recognized: Reinstall Python and enable Add Python to PATH, or try py instead of python.

A module is missing: Run python -m pip install pandas requests scikit-learn again using the same Python environment.

Dataset file not found: Keep the CSV in the same folder as the script and check that INPUT_FILE matches its exact filename.

Missing dataset columns: Check that the CSV column names match the required names listed above.

API authentication error: Check that the API key is correct, active, and entered in the local script.

Rate limit or server error: Check OpenRouter limits and model availability. The script retries certain temporary errors, but a request can still fail.

No successful predictions: Check the API key, model identifier, internet connection, and error details in the output CSV.
