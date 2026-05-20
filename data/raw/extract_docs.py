import json
import requests
from bs4 import BeautifulSoup
from tqdm import tqdm
import time

INPUT_FILE = "data/raw/urls.txt"
OUTPUT_FILE = "data/processed/documents.json"

def clean_text(html):
    soup = BeautifulSoup(html, "lxml")

    # Remove noisy elements
    for tag in soup(["script", "style", "nav", "footer", "header", "aside"]):
        tag.decompose()

    text = soup.get_text(separator=" ", strip=True)

    # Normalize whitespace
    text = " ".join(text.split())

    return text

def extract_title(html):
    soup = BeautifulSoup(html, "lxml")
    if soup.title:
        return soup.title.text.strip()
    return "Untitled"

def main():
    with open(INPUT_FILE, "r", encoding="utf-8") as f:
        urls = [u.strip() for u in f if u.strip()]

    documents = []

    for i, url in enumerate(tqdm(urls)):

        try:
            headers = {"User-Agent": "Mozilla/5.0"}
            response = requests.get(url, headers=headers, timeout=10)

            if response.status_code != 200:
                print(f"Skipping {url} | status {response.status_code}")
                continue

            html = response.text

            doc = {
                "doc_id": f"doc_{i:04d}",
                "url": url,
                "title": extract_title(html),
                "text": clean_text(html)
            }

            # filter tiny/noisy pages
            if len(doc["text"]) < 200:
                continue

            documents.append(doc)

            time.sleep(0.2)  # polite crawling

        except Exception as e:
            print(f"Failed: {url}")
            print(str(e))

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(documents, f, indent=2)

    print(f"\nSaved {len(documents)} documents to {OUTPUT_FILE}")

if __name__ == "__main__":
    main()