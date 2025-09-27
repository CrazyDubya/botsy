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
        
        # Save data
        if all_papers:
            self.save_data(all_papers, f"research_papers_{datetime.now().strftime('%Y%m%d_%H%M%S')}")
        
        return all_papers
    
    def get_available_tools(self) -> Dict[str, str]:
        """Return available tools for research scraping."""
        return {
            'arXiv API': 'Free access to 2M+ research papers',
            'PubMed API': 'Free access to biomedical literature',
            'bioRxiv API': 'Free access to biological preprints',
            'medRxiv API': 'Free access to medical preprints',
            'Semantic Scholar API': 'Free tier: 100 requests/minute',
            'CrossRef API': 'Free access to scholarly metadata',
            'DOAJ API': 'Free access to open access journals',
            'SSRN': 'Social Science Research Network (limited free access)',
            'Google Scholar': 'Web scraping (no official API)',
            'ResearchGate': 'Web scraping (no official API)'
        }

if __name__ == "__main__":
    scraper = ResearchScraper()
    papers = scraper.scrape()
    print(f"Scraped {len(papers)} research papers")
    
    # Print available tools
    print("\nAvailable Tools:")
    for tool, description in scraper.get_available_tools().items():
        print(f"- {tool}: {description}")