
# Jev vs LLMs – Comparative Analysis for Phishing Email Detection

This repository contains the Python implementation and dataset used in a comparative research study of Jev 1.13 and Large Language Models (LLMs) for phishing email detection. The research evaluates classification performance, probability calibration, inference latency, token consumption, and API costs.

The LLM experiments use the OpenRouter API to access different language models through a common API interface.

## About

Phishing emails are a common cybersecurity threat used to deceive users and obtain sensitive information. This research explores the effectiveness of Jev and LLM-based approaches in identifying phishing and legitimate emails.

The project compares different AI models using classification metrics, calibration metrics, and computational efficiency measurements.

## Models Evaluated

The research evaluates the following models:

1. Jev 1.13
2. Gemini 3.5 Flash-Lite
3. NVIDIA Nemotron 3 Ultra
4. Meta Llama 4 Maverick

## Repository Contents

The repository contains the following main files.

### 1. Python Codebase

This file contains the Python implementation used for email classification and model evaluation.

### 2. Dataset

This file contains the labelled email dataset used in the experiments. It includes phishing and legitimate email samples.

### 3. Evaluation Metrics

The evaluation process includes classification performance, probability calibration, inference latency, token consumption, and API cost.

## Technologies and Tools Used

- **Python:** Programming language used for implementation.
- **Visual Studio Code:** Code editor used to develop and run the project.
- **Pandas:** Used to read and process the CSV dataset.
- **Requests:** Used to send requests to the OpenRouter API.
- **Scikit-learn:** Used to calculate classification metrics.
- **OpenRouter API:** Used to access the selected Large Language Models.

# Evaluation Metrics

The research evaluates the models using the following metrics.

### 1. Classification Performance

- **Accuracy:** Measures the percentage of correct predictions.
- **Precision:** Measures how many emails predicted as phishing were actually phishing.
- **Recall:** Measures how many actual phishing emails were correctly identified.
- **F1-Score:** Measures the balance between precision and recall.

### 2. Probability Calibration

- **Brier Score:** Measures the difference between predicted probabilities and actual outcomes. Lower values indicate better calibration.
- **Expected Calibration Error (ECE):** Measures the difference between predicted confidence and actual accuracy across confidence groups. Lower values indicate better calibration.

### 3. Computational Efficiency

- **Inference Latency:** Measures the time taken to receive a model response.
- **Token Consumption:** Measures the input, output, and total tokens used.
- **API Cost:** Measures the API cost reported by OpenRouter when available.

# Initial Configurations

To set up and run this project, you will require:

- A computer running Windows, macOS, or Linux.
- Python installed on your computer.
- Visual Studio Code.
- An active internet connection.
- An OpenRouter API key.
- The research dataset included in this repository.

## Setting Up the Python Environment

### Step 1: Install Python

Download Python from:

https://www.python.org/downloads/

During installation on Windows, select **Add Python to PATH**.

Verify the installation by opening Command Prompt or the VS Code terminal and running:

```bash
python --version
```

### Step 2: Install Visual Studio Code

Download Visual Studio Code from:

https://code.visualstudio.com/

Install and open the application.

### Step 3: Download the Repository

Open the GitHub repository.

1. Click the green **Code** button.
2. Select **Download ZIP**.
3. Extract the downloaded ZIP file to your computer.

Alternatively, use Git:

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
```

### Step 4: Open the Project in Visual Studio Code

Open Visual Studio Code.

1. Click **File**.
2. Select **Open Folder**.
3. Select the downloaded project folder.
4. Make sure the Python file and CSV dataset are present.

Your project folder should look like this:

```text
Jev-vs-LLMs/
│
├── phishing_metrics_evaluation.py
│
└── phishing_email_detection_2026_dataset(1).csv
```

Keep both files in the same folder.

### Step 5: Install Required Python Libraries

Open the VS Code terminal:

1. Click **Terminal**.
2. Select **New Terminal**.
3. Run the following command:

```bash
python -m pip install pandas requests scikit-learn
```

Wait until all required libraries are installed.

### Step 6: Get an OpenRouter API Key

The LLM experiments use OpenRouter to communicate with the selected language models.

Follow these steps:

1. Visit https://openrouter.ai/
2. Create an account or sign in.
3. Open the API Keys section:

https://openrouter.ai/keys

4. Create a new API key.
5. Copy your API key and keep it private.

OpenRouter provides access to different language models through a common API.

**Note:** Some models require API credits. Free models may also have request limits.

### Step 7: Configure the OpenRouter API Key

Open `phishing_metrics_evaluation.py` in Visual Studio Code.

Find the API key configuration near the beginning of the code.

Replace the placeholder with your own API key:

```python
API_KEY = "YOUR_OPENROUTER_API_KEY"
```

Save the Python file.

**Important:** Never upload your actual API key to GitHub. Keep your API credentials private.

### Step 8: Configure the Model

The selected model is configured in the Python script.

For example:

```python
MODEL = "nvidia/nemotron-3-ultra-550b-a55b:free"
```

To evaluate another LLM, change the model identifier to the exact identifier available on OpenRouter.

The same API key can be used for different supported models.

Also check the dataset and output filenames in the script:

```python
INPUT_FILE = "phishing_email_detection_2026_dataset(1).csv"

OUTPUT_FILE = "llm_1500_results.csv"
```

Make sure the input filename matches your actual dataset filename.

### Step 9: Run the Python Code

After installing the libraries and configuring your API key, open the VS Code terminal.

Make sure you are inside the project folder.

Run the following command:

```bash
python phishing_metrics_evaluation.py
```

The script will:

1. Load the phishing email dataset.
2. Read the email information and actual labels.
3. Send email classification requests to the selected LLM through OpenRouter.
4. Receive the predicted label and confidence score.
5. Record response time and token consumption.
6. Record API cost when available.
7. Calculate the evaluation metrics.
8. Save the experimental results in a CSV file.

The script also saves interim results after every 50 processed records.

# Dataset Information

The research uses a labelled email dataset containing phishing and legitimate email samples.

The Python implementation expects the following dataset columns:

- `email_id`
- `sender_email`
- `subject`
- `has_link`
- `has_attachment`
- `urgency_score`
- `spelling_errors`
- `email_length_words`
- `is_phishing`

The `is_phishing` column contains the actual classification labels used to evaluate model predictions.

Make sure the dataset contains the required column names before running the code.

Only distribute the dataset if you have permission to share it.

# Experimental Results

After running the Python script, the results are saved in:

```text
llm_1500_results.csv
```

The output contains information such as:

- Email ID
- Actual label
- Predicted label
- Confidence score
- Phishing probability
- Model response
- Input tokens
- Output tokens
- Total tokens
- API cost
- Response time
- Error information

The final evaluation summary is also displayed in the VS Code terminal.

The summary includes classification performance, calibration measurements, execution time, token consumption, and available API cost information.

**Note:** Failed API requests are recorded separately and are not included in successful classification metric calculations.

# Running Experiments with Different Models

The same Python implementation can be used to evaluate different OpenRouter-supported LLMs.

For each experiment:

1. Open the Python script.
2. Change the `MODEL` identifier.
3. Keep your OpenRouter API key configured.
4. Run the Python command again.
5. Save the previous results file before starting another experiment.

This allows different models to be evaluated using the same dataset and evaluation approach.

# Troubleshooting

### Python is not recognized

Make sure Python is installed and added to PATH. Restart the terminal and try again.

### Required library is missing

Run:

```bash
python -m pip install pandas requests scikit-learn
```

### Dataset file not found

Make sure the CSV dataset and Python script are in the same folder. Check the filename in the code.

### OpenRouter API error

Check your API key, internet connection, available credits, and selected model identifier.

### Model request limit exceeded

Check the usage limits and availability of your selected model on OpenRouter.
