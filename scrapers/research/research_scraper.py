"""
Research & Academia scraper using arXiv and other academic sources.
"""
import arxiv
import requests
from typing import Dict, List, Any
from datetime import datetime, timedelta
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from utils.scraper_base import BaseScraper
from config.config import CATEGORIES

class ResearchScraper(BaseScraper):
    """Scraper for research and academic content."""
    
    def __init__(self):
        super().__init__('research')
        self.subjects = CATEGORIES['research']['subjects']
        self.max_papers = CATEGORIES['research']['max_papers']
    
    def scrape_arxiv(self, subject: str) -> List[Dict]:
        """Scrape recent papers from arXiv for a specific subject."""
        try:
            self.logger.info(f"Scraping arXiv for subject: {subject}")
            
            # Search for recent papers in the subject
            search = arxiv.Search(
                query=f"cat:{subject}",
                max_results=self.max_papers,
                sort_by=arxiv.SortCriterion.SubmittedDate
            )
            
            papers = []
            for paper in search.results():
                paper_data = {
                    'title': paper.title,
                    'authors': [author.name for author in paper.authors],
                    'summary': paper.summary,
                    'published': paper.published.isoformat(),
                    'updated': paper.updated.isoformat() if paper.updated else None,
                    'categories': paper.categories,
                    'pdf_url': paper.pdf_url,
                    'entry_id': paper.entry_id,
                    'subject': subject,
                    'scraped_at': datetime.now().isoformat()
                }
                papers.append(paper_data)
            
            self.logger.info(f"Scraped {len(papers)} papers from arXiv for {subject}")
            return papers
            
        except Exception as e:
            self.logger.error(f"Error scraping arXiv for {subject}: {e}")
            return []
    
    def scrape_pubmed(self, query: str = "machine learning", max_results: int = 10) -> List[Dict]:
        """Scrape medical research from PubMed (free API)."""
        try:
            self.logger.info(f"Scraping PubMed for query: {query}")
            
            # Search PubMed
            search_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
            search_params = {
                'db': 'pubmed',
                'term': query,
                'retmax': max_results,
                'retmode': 'json',
                'sort': 'pub_date'
            }
            
            search_response = self.make_request(search_url, search_params)
            search_data = search_response.json()
            
            paper_ids = search_data.get('esearchresult', {}).get('idlist', [])
            
            if not paper_ids:
                return []
            
            # Fetch paper details
            fetch_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi"
            fetch_params = {
                'db': 'pubmed',
                'id': ','.join(paper_ids),
                'retmode': 'xml'
            }
            
            fetch_response = self.make_request(fetch_url, fetch_params)
            
            # Parse XML response (simplified)
            papers = []
            # Note: In a real implementation, you'd parse the XML properly
            papers.append({
                'query': query,
                'paper_ids': paper_ids,
                'count': len(paper_ids),
                'scraped_at': datetime.now().isoformat(),
                'note': 'XML parsing needed for full paper details'
            })
            
            self.logger.info(f"Found {len(paper_ids)} papers on PubMed for {query}")
            return papers
            
        except Exception as e:
            self.logger.error(f"Error scraping PubMed: {e}")
            return []
    
    def scrape_biorxiv(self) -> List[Dict]:
        """Scrape preprints from bioRxiv."""
        try:
            self.logger.info("Scraping bioRxiv preprints")
            
            # bioRxiv API endpoint for recent papers
            url = "https://api.biorxiv.org/details/biorxiv"
            
            # Get papers from the last 7 days
            end_date = datetime.now().strftime('%Y-%m-%d')
            start_date = (datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d')
            
            full_url = f"{url}/{start_date}/{end_date}"
            response = self.make_request(full_url)
            data = response.json()
            
            papers = []
            for paper in data.get('collection', [])[:10]:  # Limit to 10 papers
                paper_data = {
                    'title': paper.get('title', ''),
                    'authors': paper.get('authors', ''),
                    'abstract': paper.get('abstract', ''),
                    'doi': paper.get('doi', ''),
                    'date': paper.get('date', ''),
                    'category': paper.get('category', ''),
                    'server': 'bioRxiv',
                    'scraped_at': datetime.now().isoformat()
                }
                papers.append(paper_data)
            
            self.logger.info(f"Scraped {len(papers)} papers from bioRxiv")
            return papers
            
        except Exception as e:
            self.logger.error(f"Error scraping bioRxiv: {e}")
            return []
    
    def scrape(self) -> List[Dict[str, Any]]:
        """Main scraping method."""
        all_papers = []
        
        # Scrape arXiv for each subject
        for subject in self.subjects:
            arxiv_papers = self.scrape_arxiv(subject)
            all_papers.extend(arxiv_papers)
        
        # Scrape PubMed for medical research
        pubmed_papers = self.scrape_pubmed("artificial intelligence")
        all_papers.extend(pubmed_papers)
        
        # Scrape bioRxiv for biological preprints
        biorxiv_papers = self.scrape_biorxiv()
        all_papers.extend(biorxiv_papers)
        
        # Scrape Semantic Scholar for AI research
        semantic_papers = self.scrape_semantic_scholar("machine learning")
        all_papers.extend(semantic_papers)
        
        # Scrape CrossRef for general research
        crossref_papers = self.scrape_crossref("computer science")
        all_papers.extend(crossref_papers)
        
        # Save data
        if all_papers:
            self.save_data(all_papers, f"research_papers_{datetime.now().strftime('%Y%m%d_%H%M%S')}")
        
        return all_papers
    
    def scrape_semantic_scholar(self, query: str = "machine learning") -> List[Dict]:
        """Scrape research papers using Semantic Scholar API."""
        try:
            self.logger.info(f"Scraping Semantic Scholar for: {query}")
            
            # Semantic Scholar API endpoint
            url = "https://api.semanticscholar.org/graph/v1/paper/search"
            params = {
                'query': query,
                'limit': 10,
                'fields': 'title,authors,abstract,year,citationCount,url'
            }
            
            response = self.make_request(url, params)
            data = response.json()
            
            papers = []
            for paper in data.get('data', []):
                paper_data = {
                    'title': paper.get('title', ''),
                    'authors': [author.get('name', '') for author in paper.get('authors', [])],
                    'abstract': paper.get('abstract', ''),
                    'year': paper.get('year', 0),
                    'citation_count': paper.get('citationCount', 0),
                    'url': paper.get('url', ''),
                    'source': 'Semantic Scholar',
                    'scraped_at': datetime.now().isoformat()
                }
                papers.append(paper_data)
            
            self.logger.info(f"Scraped {len(papers)} papers from Semantic Scholar")
            return papers
            
        except Exception as e:
            self.logger.error(f"Error scraping Semantic Scholar: {e}")
            return []
    
    def scrape_crossref(self, query: str = "artificial intelligence") -> List[Dict]:
        """Scrape academic papers using CrossRef API (completely free)."""
        try:
            self.logger.info(f"Scraping CrossRef for: {query}")
            
            # CrossRef API endpoint
            url = "https://api.crossref.org/works"
            params = {
                'query': query,
                'rows': 10,
                'sort': 'relevance',
                'order': 'desc'
            }
            
            response = self.make_request(url, params)
            data = response.json()
            
            papers = []
            for item in data.get('message', {}).get('items', []):
                paper_data = {
                    'title': ' '.join(item.get('title', [''])),
                    'authors': [f"{author.get('given', '')} {author.get('family', '')}" 
                              for author in item.get('author', [])],
                    'doi': item.get('DOI', ''),
                    'published_date': item.get('published-print', {}).get('date-parts', [[]])[0],
                    'publisher': item.get('publisher', ''),
                    'citation_count': item.get('is-referenced-by-count', 0),
                    'source': 'CrossRef',
                    'scraped_at': datetime.now().isoformat()
                }
                papers.append(paper_data)
            
            self.logger.info(f"Scraped {len(papers)} papers from CrossRef")
            return papers
            
        except Exception as e:
            self.logger.error(f"Error scraping CrossRef: {e}")
            return []

    def get_available_tools(self) -> Dict[str, str]:
        """Return available tools for research scraping."""
        return {
            # Completely free APIs - No authentication
            'arXiv API': 'Unlimited access to 2M+ preprint papers',
            'PubMed API': 'Free access to biomedical literature (rate limited)',
            'bioRxiv API': 'Free access to biology preprints',
            'medRxiv API': 'Free access to medical preprints',
            'CrossRef API': 'Unlimited DOI and citation metadata',
            'DOAJ API': 'Unlimited access to open access journals',
            'OpenAlex API': 'Free access to 200M+ scholarly works',
            
            # Free APIs - Key required
            'Semantic Scholar API': 'Free tier: 100 requests/minute for paper search',
            'Europe PMC API': 'Free access to life science literature',
            'CORE API': 'Free tier: 1000 requests/day for open access research',
            
            # Specialized Python libraries
            'arxiv': 'arXiv API client (github: lukasschwab/arxiv.py)',
            'scholarly': 'Google Scholar scraper (github: scholarly-python-package/scholarly)',
            'biopython': 'Bioinformatics tools (github: biopython/biopython)',
            'pubmed-parser': 'PubMed XML parser (github: titipata/pubmed_parser)',
            'crossref-commons': 'CrossRef API wrapper',
            'semanticscholar': 'Semantic Scholar API wrapper',
            'academic-scraper': 'Multi-source scraper (github: VincentStimper/academic-scraper)',
            
            # Premium/Institutional APIs
            'Web of Science API': 'Institutional access required for citation indexing',
            'Scopus API': 'Institutional access required for abstract database',
            'Dimensions API': 'Custom pricing for research analytics',
            'IEEE Xplore API': 'Free tier available for IEEE publications',
            'ACM Digital Library': 'Free access to abstracts, paid for full text',
            
            # Web scraping targets
            'Google Scholar': 'Web scraping (no official API, use scholarly library)',
            'ResearchGate': 'Web scraping for researcher profiles and papers',
            'Academia.edu': 'Web scraping for academic papers',
            'SSRN': 'Social Science Research Network (limited free access)',
            'PhilPapers': 'Philosophy research database',
            'NBER': 'National Bureau of Economic Research papers',
            
            # Specialized academic databases
            'JSTOR': 'Limited free access, institutional subscriptions',
            'SpringerLink': 'Some open access content available',
            'ScienceDirect': 'Elsevier papers (limited free access)',
            'Wiley Online Library': 'Some open access content',
            'PLOS ONE': 'Open access scientific journal',
            'Nature Open Access': 'Free Nature research articles',
            
            # Citation and metrics
            'OpenCitations': 'Free citation data',
            'Microsoft Academic Graph': 'Academic knowledge graph (deprecated)',
            'Altmetric API': 'Alternative metrics for research impact',
            'PlumX Metrics': 'Research metrics and analytics',
            
            # Research data repositories
            'Zenodo API': 'Free research data repository',
            'Figshare API': 'Free research data sharing',
            'Dryad API': 'Research data repository',
            'Harvard Dataverse': 'Research data repository',
            
            # Preprint servers
            'ChemRxiv': 'Chemistry preprints',
            'PsyArXiv': 'Psychology preprints',
            'SocArXiv': 'Social science preprints',
            'EconArXiv': 'Economics preprints',
            'engrXiv': 'Engineering preprints'
        }

if __name__ == "__main__":
    scraper = ResearchScraper()
    papers = scraper.scrape()
    print(f"Scraped {len(papers)} research papers")
    
    # Print available tools
    print("\nAvailable Tools:")
    for tool, description in scraper.get_available_tools().items():
        print(f"- {tool}: {description}")