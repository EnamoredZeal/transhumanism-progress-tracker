import xml.etree.ElementTree as ET
import requests


def search_transhuman_tech(query: str, max_results: int = 5):
    """Searches PubMed for recent scientific papers matching a metric pillar."""
    base_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
    params = {
        "db": "pubmed",
        "term": query,
        "retmode": "json",
        "retmax": max_results
    }
    
    # 1. Get the list of IDs matching our query
    response = requests.get(base_url, params=params).json()
    id_list = response.get("esearchresult", {}).get("idlist", [])
    
    if not id_list:
        print(f"No recent papers found for query: '{query}'")
        return []

    # 2. Fetch the details for those IDs
    fetch_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi"
    fetch_params = {
        "db": "pubmed",
        "id": ",".join(id_list),
        "retmode": "xml"
    }
    
    fetch_response = requests.get(fetch_url, params=fetch_params)
    root = ET.fromstring(fetch_response.content)
    
    articles = []
    for article in root.findall(".//PubmedArticle"):
        title = article.find(".//ArticleTitle").text
        # Extract DOI if available
        doi = "No DOI found"
        for id_elem in article.findall(".//ArticleId"):
            if id_elem.attrib.get("IdType") == "doi":
                doi = id_elem.text
        
        articles.append({
            "title": title,
            "doi": f"https://doi.org/{doi}" if "No" not in doi else doi,
        })
        
    return articles

if __name__ == "__main__":
    # Test our scraper with a core cognitive science query
    print("Scanning PubMed for Integrated Information Theory / Phi updates...")
    results = search_transhuman_tech('"Integrated Information Theory" OR "Perturbational Complexity Index"')
    
    for idx, paper in enumerate(results, 1):
        print(f"\n[{idx}] {paper['title']}")
        print(f"    Source/DOI: {paper['doi']}")
