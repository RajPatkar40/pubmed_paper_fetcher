import requests
import lxml.etree as ET
import re
import csv
import time  # 🛠 Add delay to avoid API rate limits
from typing import List, Dict, Optional
import argparse


PUBMED_API_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/"
HEADERS = {"User-Agent": "PubMedPaperFetcher/1.0 (email@example.com)"}

def fetch_paper_ids(query: str, max_results: int = 10) -> List[str]:
    """Fetch paper IDs from PubMed based on a search query."""
    params = {
        "db": "pubmed",
        "term": query,
        "retmode": "json",
        "retmax": max_results,  # Limit results to prevent overload
    }
    try:
        response = requests.get(f"{PUBMED_API_URL}esearch.fcgi", params=params, headers=HEADERS)
        response.raise_for_status()  # Raise exception for HTTP errors
        
        data = response.json()
        return data.get("esearchresult", {}).get("idlist", [])
    except requests.RequestException as e:
        print(f"⚠️ Error fetching paper IDs: {e}")
        return []

def fetch_paper_details(paper_id: str) -> Optional[Dict]:
    """Fetch detailed information for a given PubMed paper ID."""
    params = {
        "db": "pubmed",
        "id": paper_id,
        "retmode": "xml",
    }

    try:
        response = requests.get(f"{PUBMED_API_URL}efetch.fcgi", params=params, headers=HEADERS)
        response.raise_for_status()
        
        xml_tree = ET.fromstring(response.content)

        # Extract fields safely
        title = xml_tree.xpath("//ArticleTitle/text()")
        publication_date = xml_tree.xpath("//PubDate/Year/text()")
        authors = xml_tree.xpath("//AuthorList/Author")

        # Extract affiliations
        non_academic_authors = []
        company_affiliations = []
        corresponding_email = None

        for author in authors:
            last_name = author.xpath("LastName/text()")
            first_name = author.xpath("ForeName/text()")
            full_name = f"{first_name[0]} {last_name[0]}" if first_name and last_name else "Unknown"

            affiliation = author.xpath("AffiliationInfo/Affiliation/text()")
            if affiliation and any(kw in affiliation[0] for kw in ["Pharma", "Biotech", "Inc", "Ltd", "Laboratories"]):
                non_academic_authors.append(full_name)
                company_affiliations.append(affiliation[0])

            # Extract email (if available)
            email_match = re.search(r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+", affiliation[0] if affiliation else "")
            if email_match:
                corresponding_email = email_match.group(0)

        return {
            "PubmedID": paper_id,
            "Title": title[0] if title else "N/A",
            "Publication Date": publication_date[0] if publication_date else "N/A",
            "Non-academic Authors": ", ".join(non_academic_authors) if non_academic_authors else "None",
            "Company Affiliations": ", ".join(company_affiliations) if company_affiliations else "None",
            "Corresponding Email": corresponding_email if corresponding_email else "N/A",
        }
    
    except requests.RequestException as e:
        print(f"⚠️ Error fetching details for PubMed ID {paper_id}: {e}")
        return None
    except ET.XMLSyntaxError:
        print(f"⚠️ Warning: XML response could not be parsed for {paper_id}")
        return None

def save_to_csv(papers: List[Dict], filename: str = "papers.csv"):
    """Save the fetched data to a CSV file."""
    if not papers:
        print("No data to save.")
        return

    with open(filename, "w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=["PubmedID", "Title", "Publication Date", "Non-academic Authors", "Company Affiliations", "Corresponding Email"])
        writer.writeheader()
        writer.writerows(papers)
    print(f"✅ Results saved to {filename}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Fetch PubMed Papers.")
    parser.add_argument("--query", type=str, default="biotechnology AND pharmaceutical", help="Search query for PubMed")
    parser.add_argument("--max", type=int, default=5, help="Maximum results to fetch")
    args = parser.parse_args()

    paper_ids = fetch_paper_ids(args.query, max_results=args.max)
    print(f"🔍 Fetched Paper IDs: {paper_ids}")

    paper_data = []
    for paper_id in paper_ids:
        details = fetch_paper_details(paper_id)
        if details:
            paper_data.append(details)
        time.sleep(1)

    save_to_csv(paper_data)
