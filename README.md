# PDF Q&A with Crew AI

This repository contains a script (**`pdf_qa.py`**) that uses the **Crew AI** framework and an **OpenAI** LLM to answer questions from a PDF document. It leverages a **`PDFSearchTool`** (RAG approach) for semantic search over the PDF, then returns concise answers.

## Features

- **Single Script Usage**  
  Easily run `pdf_qa.py` to ask questions about any PDF.
- **Reusability**  
  Sets up a single RAG tool and agent once, then processes multiple questions.
- **Customizable**  
  Adjust the temperature, model name, or PDF path as desired.

## Prerequisites

- **Python 3.10** or higher
- **Git** (to clone the repository)
- **OpenAI API Key** (store it in an environment variable or directly in the code)

## Installation

1. **Clone this repository**:

    ```bash
    git clone https://github.com/<YOUR_USERNAME>/<YOUR_REPO>.git
    cd <YOUR_REPO>
    ```

2. **Create and activate a Python 3.10 virtual environment**:

    ```bash
    python3.10 -m venv venv
    source venv/bin/activate
    ```
    On Windows:
    ```bash
    python -m venv venv
    venv\Scripts\activate
    ```

3. **Install dependencies**:

    ```bash
    pip install -r requirements.txt
    ```

4. **(Optional) Set your OpenAI API Key**:

    - You can **edit** `pdf_qa.py` to include your OpenAI API key, or
    - **Export** it as an environment variable:

      ```bash
      export OPENAI_API_KEY="sk-..."
      ```

## Usage

1. **Prepare your PDF**  
   Rename or copy your target PDF to `handbook.pdf` (or any PDF file name you wish). Place it in the same directory as `pdf_qa.py` (or note the path you’ll pass as the first argument).

2. **Run the script**:

    ```bash
    python pdf_qa.py handbook.pdf --questions '["What is the name of the company?", "Who is the CEO?", "What is their vacation policy?", "What is the termination policy?", "Who is Arshaan?"]'
    ```

    - The first argument (`handbook.pdf`) is the path to your PDF.
    - `--questions` takes a **list of strings** in JSON format:  
      `["question1", "question2", ...]`

3. **View Results**:  
   The script prints partial results after each question, then prints a final JSON with answers to all questions.

### Example Command

```bash
python pdf_qa.py handbook.pdf --questions '["What is the name of the company?", "Who is the CEO?", "What is their vacation policy?", "What is the termination policy?", "Who is Arshaan?"]'
