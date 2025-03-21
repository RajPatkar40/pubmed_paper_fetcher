# PubMed Paper Fetcher
# Fetch PubMed Papers

This Python script fetches research papers from PubMed based on a user-specified query. It identifies papers with at least one author affiliated with a pharmaceutical or biotech company and returns the results as a CSV file.

## Features
- Fetches paper IDs from PubMed using the Entrez API.
- Retrieves paper details such as title, publication date, and authors.
- Identifies non-academic authors affiliated with pharmaceutical/biotech companies.
- Saves the results as a CSV file or prints them to the console.
- Supports command-line options for flexible execution.# PubMed Paper Fetcher
# Fetch PubMed Papers

This Python script fetches research papers from PubMed based on a user-specified query. It identifies papers with at least one author affiliated with a pharmaceutical or biotech company and returns the results as a CSV file.

## Features
- Fetches paper IDs from PubMed using the Entrez API.
- Retrieves paper details such as title, publication date, and authors.
- Identifies non-academic authors affiliated with pharmaceutical/biotech companies.
- Saves the results as a CSV file or prints them to the console.
- Supports command-line options for flexible execution.

## Installation
### Prerequisites
- Python 3.9+
- Poetry (for dependency management)

### Steps
1. Clone the repository:
   ```sh
   git clone https://github.com/yourusern/fetch-pubmed-papers.git
   cd fetch-pubmed-papers
   ```
2. Install dependencies using Poetry:
   ```sh
   poetry install
   ```

## Usage
### Running the script
To fetch papers based on a search query:
```sh
poetry run python fetch_papers.py "cancer research"
```

### Command-line options:
- `-f, --file <filename>`: Specify a filename to save the results as CSV.
- `-h, --help` : Display usage instructions.

Example:
```sh
poetry run python fetch_papers.py "gene therapy" -f results.csv
```

## Project Structure
```python
import argparse
import csv
import os
from Bio import Entrez, Medline

def fetch_paper_ids(query):
    """Fetch paper IDs from PubMed using the Entrez API."""
    Entrez.email = "your_email@example.com"
    handle = Entrez.esearch(db="pubmed", term=query, usehistory="y")
    record = Entrez.read(handle)
    handle.close()
    return record["IdList"]

def fetch_paper_details(id_list):
    """Retrieve paper details such as title, publication date, and authors."""
    handle = Entrez.efetch(db="pubmed", id=id_list, rettype="medline", retmode="text")
    records = Medline.parse(handle)
    handle.close()
    return list(records)

def identify_non_academic_authors(records):
    """Identify non-academic authors affiliated with pharmaceutical/biotech companies."""
    non_academic_authors = []
    for record in records:
        for author in record.get("AU", []):
            affiliation = record.get("AD", [""])[0]
            if "pharmaceutical" in affiliation.lower() or "biotech" in affiliation.lower():
                non_academic_authors.append((author, affiliation))
    return non_academic_authors

def save_results(filename, results):
    """Save the results as a CSV file."""
    with open(filename, "w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Author", "Affiliation"])
        writer.writerows(results)

def main():
    parser = argparse.ArgumentParser(description="Fetch PubMed Papers")
    parser.add_argument("query", help="Search query")
    parser.add_argument("-f", "--file", help="Filename to save the results as CSV")
    args = parser.parse_args()

    paper_ids = fetch_paper_ids(args.query)
    records = fetch_paper_details(paper_ids)
    non_academic_authors = identify_non_academic_authors(records)

    if args.file:
        save_results(args.file, non_academic_authors)
    else:
        for author, affiliation in non_academic_authors:
            print(f"{author}: {affiliation}")

if __name__ == "__main__":
    main()
```

## API Details
This script uses the PubMed Entrez API:
- `esearch.fcgi` to fetch paper IDs.
- `esummary.fcgi` to retrieve paper details.

## Contribution
1. Fork the repository.
2. Create a new branch (`feature-branch`).
3. Commit changes and push.
4. Open a pull request.

## License
MIT License

## Installation
### Prerequisites
- Python 3.9+
- Poetry (for dependency management)

### Steps
1. Clone the repository:
   ```sh
   git clone https://github.com/yourusern/fetch-pubmed-papers.git
   cd fetch-pubmed-papers
   ```
2. Install dependencies using Poetry:
   ```sh
   poetry install
   ```

## Usage
### Running the script
To fetch papers based on a search query:
```sh
poetry run python fetch_papers.py "cancer research"
```

### Command-line options:
- `-f, --file <filename>`: Specify a filename to save the results as CSV.
- `-h, --help` : Display usage instructions.

Example:
```sh
poetry run python fetch_papers.py "gene therapy" -f results.csv
```

## Project Structure
```
pubmed_papers/
│── fetch_papers.py  # Main script
│── pyproject.toml   # Poetry configuration
│── README.md        # Documentation
│── papers.csv       # Output file (if specified)
```

## API Details
This script uses the PubMed Entrez API:
- `esearch.fcgi` to fetch paper IDs.
- `esummary.fcgi` to retrieve paper details.

## Contribution
1. Fork the repository.
2. Create a new branch (`feature-branch`).
3. Commit changes and push.
4. Open a pull request.

## License
MIT License

---
**Fetched Paper IDs:** ['40094454', '40094145', '40093551', '40093334', '40093330']
**Results saved to papers.csv**
