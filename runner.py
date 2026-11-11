import os
import sys
import shutil
import time
import datetime
import xml.etree.ElementTree as ET
import requests
from dotenv import load_dotenv
from google import genai

load_dotenv()

# --- CONFIGURATION ---
API_KEY = os.getenv("GEMINI_API_KEY")
if not API_KEY:
    print("Error: GEMINI_API_KEY not found in .env.")
    sys.exit(1)

client = genai.Client(api_key=API_KEY)

# Using stable models
CANDIDATE_MODELS = [
    "gemini-3.5-flash",
    "gemini-3.8-flash",
    "gemini-3.5-flash-lite"
]

PAPER_FILE = "paper.md"
JOURNAL_FILE = "journal.md"
SOURCES_FILE = "sources.json"
HISTORY_DIR = "history"

SEARCH_QUERY = 'all:"recursive self-improvement" OR all:"AI research agent" OR all:"autonomous code generation"'
MAX_SEARCH_RESULTS = 5


def initialize_environment():
    import json
    os.makedirs(HISTORY_DIR, exist_ok=True)

    if not os.path.exists(SOURCES_FILE):
        with open(SOURCES_FILE, "w", encoding="utf-8") as f:
            json.dump({"processed_ids": ["2609.26457", "2607.07663", "2610.27610"]}, f, indent=2)

    if not os.path.exists(JOURNAL_FILE):
        with open(JOURNAL_FILE, "w", encoding="utf-8") as f:
            f.write("# Evolution Journal\n\n## Entry 001 — Version 0.1 (Baseline)\n- **Status**: Initial baseline paper generated.\n- **Core Hypotheses**: RSI is distinct from iterative refinement; evaluation reliability is the primary bottleneck.\n---\n")

    if not os.path.exists(PAPER_FILE):
        initial_paper = """# Recursive Self-Improvement and the Runaway Train
**Version 0.1 — Initial working draft**

## Abstract
Artificial intelligence systems are increasingly being developed to participate in the processes responsible for their own improvement. This paper explores recursive self-improvement (RSI) as a potential mechanism for accelerating artificial intelligence development.

## 1. Introduction: The Runaway Train
Technological progress has historically depended on human-directed processes of experimentation. Artificial intelligence introduces the possibility that increasingly large portions of these processes can themselves be automated.

## 2. Defining Recursive Self-Improvement
We distinguish:
1. Iterative refinement: Modifying an output for a better result.
2. Self-improvement: Modifying behavior or configurations for future performance.
3. Recursive self-improvement: Improving the mechanism responsible for producing future improvements.

## 3. The Mechanics of Recursive Improvement
System → Evaluation → Modification → Improved System → New Evaluation.

## 4. Emerging Evidence
Current systems demonstrate bounded refinement loops, but evidence for unrestricted runaway improvement remains insufficient.

## 5. The Evaluation Problem
A recursive system may eventually become responsible for both producing and judging its own improvements, risking benchmark overfitting and measurement corruption.

## 6. Constraints and Diminishing Returns
Hardware, algorithmic limits, and diminishing marginal returns constrain unbounded recursive gains.

## 7. Conditions for a Runaway Loop
Compounding returns require that modification quality, verification reliability, and resource availability all hold simultaneously.

## 8. Conclusion
The central challenge is not merely creating systems that improve themselves, but creating systems that reliably evaluate whether their improvements are real.

## References
1. Srikanth et al. (2026). Recursive self-improvement of AI research agents.
2. Chen et al. (2026). Recursive Self-Improvement in AI: From Bounded Self-Refinement to Autonomous Research Loops.
3. Chen et al. (2026). Auditing the Product, Not the Recursion.
"""
        with open(PAPER_FILE, "w", encoding="utf-8") as f:
            f.write(initial_paper)


def fetch_arxiv_papers(existing_ids):
    url = f"http://export.arxiv.org/api/query?search_query={requests.utils.quote(SEARCH_QUERY)}&start=0&max_results={MAX_SEARCH_RESULTS}&sortBy=submittedDate&sortOrder=descending"
    response = requests.get(url, timeout=15)
    
    if response.status_code != 200:
        print(f"Notice: arXiv returned status {response.status_code}")
        return []

    root = ET.fromstring(response.text)
    namespace = {"atom": "http://www.w3.org/2005/Atom"}
    
    new_papers = []
    for entry in root.findall("atom:entry", namespace):
        raw_id = entry.find("atom:id", namespace).text
        paper_id = raw_id.split("/abs/")[-1].split("v")[0]
        
        if paper_id in existing_ids:
            continue
            
        title = entry.find("atom:title", namespace).text.strip().replace("\n", " ")
        summary = entry.find("atom:summary", namespace).text.strip().replace("\n", " ")
        authors = [a.find("atom:name", namespace).text for a in entry.findall("atom:author", namespace)]
        published = entry.find("atom:published", namespace).text[:10]
        
        new_papers.append({
            "id": paper_id,
            "title": title,
            "authors": authors,
            "published": published,
            "summary": summary,
            "link": raw_id
        })
        
    return new_papers


def generate_revision(current_paper, current_journal, new_papers):
    papers_context = "\n\n".join([
        f"- ID: {p['id']}\n  Title: {p['title']}\n  Authors: {', '.join(p['authors'])}\n  Date: {p['published']}\n  Abstract: {p['summary']}"
        for p in new_papers
    ])

    prompt = f"""You are an autonomous research intelligence maintaining a living paper on "Recursive Self-Improvement in AI".

CURRENT LIVING PAPER:
{current_paper}

NEW RESEARCH DISCOVERED:
{papers_context}

INSTRUCTIONS:
1. Synthesize the new papers with the current paper. Integrate key findings and references into the paper.
2. Structure your complete response using EXACTLY these three delimiter headers:

=== REVISION SUMMARY ===
(Provide a 2-3 sentence overview of what changed)

=== UPDATED PAPER ===
(Provide the full, complete Markdown text of the updated paper)

=== JOURNAL ENTRY ===
(Provide the detailed markdown entry for the evolution journal explaining changes, evidence, and hypothesis evaluations)
"""

    for model in CANDIDATE_MODELS:
        try:
            print(f"Connecting to '{model}'...")
            print("Streaming output from Gemini: ", end="", flush=True)
            
            # Using streaming so you see tokens arrive immediately
            response = client.models.generate_content_stream(
                model=model,
                contents=prompt
            )
            
            full_text = ""
            for chunk in response:
                if chunk.text:
                    full_text += chunk.text
                    print(".", end="", flush=True)  # Visual progress indicator
            print(" Done!\n")

            # Parse out the sections using our explicit delimiters
            if "=== UPDATED PAPER ===" in full_text and "=== JOURNAL ENTRY ===" in full_text:
                parts_1 = full_text.split("=== UPDATED PAPER ===")
                summary = parts_1[0].replace("=== REVISION SUMMARY ===", "").strip()
                
                parts_2 = parts_1[1].split("=== JOURNAL ENTRY ===")
                updated_paper = parts_2[0].strip()
                journal_entry = parts_2[1].strip()

                return {
                    "revision_summary": summary,
                    "updated_paper": updated_paper,
                    "journal_entry": journal_entry
                }
            else:
                print("\nModel response missed headers. Retrying next model...")
        except Exception as e:
            print(f"\nModel {model} encountered an issue: {e}. Trying alternate...")
            time.sleep(2)
            
    raise RuntimeError("All models failed to generate content.")


def commit_changes(result, new_paper_ids):
    import json
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # 1. Backup old paper
    backup_path = os.path.join(HISTORY_DIR, f"paper_{timestamp}.md")
    shutil.copyfile(PAPER_FILE, backup_path)
    print(f"Backed up previous paper version to {backup_path}")

    # 2. Update paper.md
    with open(PAPER_FILE, "w", encoding="utf-8") as f:
        f.write(result["updated_paper"])

    # 3. Update journal.md
    date_str = datetime.date.today().isoformat()
    journal_append = f"\n\n## Iteration {timestamp} — {date_str}\n"
    journal_append += f"**Summary**: {result['revision_summary']}\n\n"
    journal_append += result["journal_entry"] + "\n---"
    
    with open(JOURNAL_FILE, "a", encoding="utf-8") as f:
        f.write(journal_append)

    # 4. Save processed IDs
    with open(SOURCES_FILE, "r", encoding="utf-8") as f:
        sources_data = json.load(f)
        
    sources_data["processed_ids"].extend(new_paper_ids)
    
    with open(SOURCES_FILE, "w", encoding="utf-8") as f:
        json.dump(sources_data, f, indent=2)

    print("SUCCESS: Updated paper.md, journal.md, and sources.json!")


def main():
    import json
    print(f"[{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Starting autonomous research run...")
    initialize_environment()
    
    with open(SOURCES_FILE, "r", encoding="utf-8") as f:
        sources_data = json.load(f)
    existing_ids = set(sources_data.get("processed_ids", []))
    
    print("Checking arXiv for new preprints...")
    new_papers = fetch_arxiv_papers(existing_ids)
    
    if not new_papers:
        print("No new papers discovered this cycle. Living paper remains unchanged.")
        return

    print(f"Found {len(new_papers)} new paper(s).")
    
    with open(PAPER_FILE, "r", encoding="utf-8") as f:
        current_paper = f.read()
    with open(JOURNAL_FILE, "r", encoding="utf-8") as f:
        current_journal = f.read()
        
    result = generate_revision(current_paper, current_journal, new_papers)
    new_ids = [p["id"] for p in new_papers]
    
    commit_changes(result, new_ids)
    print("Run completed successfully.")


if __name__ == "__main__":
    main()