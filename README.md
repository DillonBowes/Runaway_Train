# Recursive Self-Improvement and the Runaway Train

An autonomous research pipeline and evolving living paper investigating recursive self-improvement (RSI) in artificial intelligence. The pipeline discovers newly published preprints from arXiv, analyzes them against an existing academic draft using Google's Gemini API, updates the paper with new findings, maintains an evolution journal, and pushes changes to GitHub.

This project was built to run locally on Windows using free-tier tools and APIs without requiring dedicated server infrastructure.

## Features

- Queries arXiv automatically for new preprints on recursive self-improvement and autonomous research agents.
- Deduplicates papers against a local registry so sources are only processed once.
- Evaluates new research findings against the existing paper using Google Gemini.
- Updates the living paper (paper.md) with new citations, arguments, and counterpoints.
- Maintains an Evolution Journal (journal.md) documenting hypothesis changes, evidence evaluated, and rationale for every update.
- Backs up previous paper revisions to a timestamped history/ directory before writing changes.
- Automatically commits and pushes updated documents to GitHub.
- Operates entirely on zero-cost infrastructure (open arXiv API and Gemini free tier).
- Can run on startup or on a recurring schedule using Windows Task Scheduler.

## How It Works

The application combines three components:

1. arXiv API: Searches for recent academic preprints matching recursive self-improvement, AI agents, and code generation, extracting metadata and abstracts without requiring an API key.
2. Google Gemini API: Compares new candidate abstracts against the current paper, assesses whether findings challenge or support the core thesis, and generates revisions and journal entries.
3. Local File Pipeline and Git: Handles transactional file writes, creates timestamped backups in history/, updates local tracking indexes, and pushes changes to GitHub.

The pipeline queries arXiv, checks returned paper IDs against sources.json, and halts early if no new research is found. When new papers exist, the script streams the text through Gemini using explicit markdown section delimiters, updates paper.md, appends the reasoning to journal.md, and runs Git commands to sync the repository.

## Requirements

- Windows 10 or Windows 11
- Python 3.10 or newer
- Git for Windows
- A Google Gemini API key (free tier from Google AI Studio)
- Command Prompt or PowerShell

## Project Setup

### 1. Clone the Repository

Open Command Prompt and navigate to the directory where you want to store the project:

git clone https://github.com/DillonBowes/Runaway_Train.git
cd Runaway_Train

### 2. Create and Activate a Virtual Environment

Create a Python virtual environment to manage dependencies:

python -m venv venv

Activate the environment:

venv\Scripts\activate

When activated, (venv) will appear at the start of your command line.

### 3. Install Dependencies

Install the required Python packages:

pip install google-genai requests python-dotenv

### 4. Configure Your API Key

Get a free API key from Google AI Studio (https://aistudio.google.com/).

Create a .env file in the project folder to store your key:

echo GEMINI_API_KEY=your_actual_key_here> .env

Verify that the .env file was created properly:

type .env

(Note: The .env file is listed in .gitignore and is never uploaded to GitHub).

### 5. Run the Pipeline Manually

Run the pipeline from your virtual environment:

python runner.py

The script will query arXiv, stream the analysis, update paper.md and journal.md, back up the previous version to history/, and push the changes to GitHub.

## Weekly Automation Setup

To have the script run automatically once per week without manual intervention:

1. Open the Windows Start menu, type Task Scheduler, and press Enter.
2. Click Create Basic Task in the Actions panel on the right.
3. Enter a name (e.g., RSI Research Pipeline) and click Next.
4. Select Weekly and configure your preferred day and time.
5. Select Start a program and fill in the following:
   - Program/script: C:\Users\dbvan\rsi_pipeline\venv\Scripts\python.exe
   - Add arguments: runner.py
   - Start in: C:\Users\dbvan\rsi_pipeline
6. Click Finish.

## Repository Structure

- paper.md — The current living paper.
- journal.md — The evolution log tracking changes, hypotheses, and evaluations across iterations.
- history/ — Timestamped backups of prior paper drafts.
- sources.json — A record of previously evaluated arXiv paper IDs.
- runner.py — The Python orchestration script.
- .env — Local environment file holding the API key (untracked).
- .gitignore — Specifies files untracked by Git (.env, venv/, etc.).

## NOTES
The purpose of this project is to explore recursive self-improvement in artificial intelligence through both research and practice. 
There is an intentional irony at its core: a paper investigating the possibility of AI systems recursively improving themselves is itself maintained by an automated pipeline that continually researches, evaluates, and revises its own contents. 
It serves as both a thought piece on the potential for runaway AI development and a small proof of concept demonstrating how an AI-assisted research process can evolve over time. 
While this does not demonstrate true recursive self-improvement, it offers a practical way to examine the ideas, limitations, and implications behind it.
