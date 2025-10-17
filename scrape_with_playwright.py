"""
Playwright-based Web Scraper for JavaScript-Rendered Content
Handles case studies from Shuru Tech insights pages
"""

import asyncio
import json
import re
import time
from typing import List, Dict, Optional
from pathlib import Path

from playwright.async_api import async_playwright, Page, Browser
from bs4 import BeautifulSoup


class PlaywrightScraper:
    """Async scraper using Playwright for JavaScript-rendered content"""
    
    # Technology keywords for detection
    TECH_KEYWORDS = [
        'React', 'Angular', 'Vue', 'Next.js', 'Node.js', 'Express', 'Python', 'Django',
        'Flask', 'FastAPI', 'Java', 'Spring', 'Go', 'Rust', 'TypeScript', 'JavaScript',
        'PostgreSQL', 'MySQL', 'MongoDB', 'Redis', 'AWS', 'Azure', 'GCP', 'Docker',
        'Kubernetes', 'Terraform', 'GraphQL', 'REST', 'gRPC', 'Kafka', 'RabbitMQ',
        'TensorFlow', 'PyTorch', 'Machine Learning', 'AI', 'Microservices', 'Serverless'
    ]
    
    def __init__(self, headless: bool = True, timeout: int = 60000):
        """
        Initialize scraper
        
        Args:
            headless: Run browser in headless mode
            timeout: Page load timeout in milliseconds
        """
        self.headless = headless
        self.timeout = timeout
        self.case_study_counter = 11  # Start from 11 (after existing manual entries)
    
    async def scrape_case_study_url(self, url: str, browser: Browser) -> Optional[Dict]:
        """
        Scrape a single case study URL
        
        Args:
            url: Case study URL
            browser: Playwright browser instance
            
        Returns:
            Case study dict or None if failed
        """
        print(f"\n{'='*70}")
        print(f"Scraping: {url}")
        print('='*70)
        
        try:
            # Create new page
            page = await browser.new_page()
            
            # Set longer timeout for slow pages
            page.set_default_timeout(self.timeout)
            
            # Navigate to URL
            print("Loading page...")
            await page.goto(url, wait_until='load')  # Changed from networkidle to load
            
            # Wait for article content to load
            print("Waiting for content to render...")
            await page.wait_for_timeout(5000)  # Wait 5 seconds for JS to render
            
            # Try to wait for article tag
            try:
                await page.wait_for_selector('article', timeout=5000)
            except:
                print("⚠️  Article tag not found, proceeding anyway...")
            
            # Get page content
            content = await page.content()
            
            # Extract data
            case_study = await self.extract_article_content(page, content, url)
            
            await page.close()
            
            if case_study:
                print(f"✓ Successfully extracted: {case_study.get('client_name', 'Unknown')}")
                return case_study
            else:
                print("❌ Failed to extract case study data")
                return None
                
        except Exception as e:
            print(f"❌ Error scraping {url}: {str(e)}")
            return None
    
    async def extract_article_content(self, page: Page, html_content: str, url: str) -> Optional[Dict]:
        """
        Extract case study content from rendered page
        
        Args:
            page: Playwright page instance
            html_content: HTML content
            url: Page URL
            
        Returns:
            Case study dict or None
        """
        soup = BeautifulSoup(html_content, 'html.parser')
        
        # Extract title
        title = None
        h1 = await page.query_selector('h1')
        if h1:
            title = await h1.inner_text()
        
        if not title:
            title_tag = soup.find('title')
            if title_tag:
                title = title_tag.get_text(strip=True)
        
        if not title:
            title_meta = soup.find('meta', {'property': 'og:title'})
            if title_meta:
                title = title_meta.get('content')
        
        print(f"Title: {title}")
        
        # Extract metadata
        description = None
        desc_meta = soup.find('meta', {'name': 'description'})
        if desc_meta:
            description = desc_meta.get('content')
        
        # Try to extract article body
        article_text = ""
        
        # Method 1: Try article tag
        article = await page.query_selector('article')
        if article:
            article_text = await article.inner_text()
            print(f"✓ Extracted from <article>: {len(article_text)} chars")
        
        # Method 2: Try main tag
        if not article_text or len(article_text) < 500:
            main = await page.query_selector('main')
            if main:
                main_text = await main.inner_text()
                if len(main_text) > len(article_text):
                    article_text = main_text
                    print(f"✓ Extracted from <main>: {len(article_text)} chars")
        
        # Method 3: Try common content selectors
        if not article_text or len(article_text) < 500:
            selectors = ['.post-content', '.article-content', '.content', '.entry-content']
            for selector in selectors:
                elem = await page.query_selector(selector)
                if elem:
                    text = await elem.inner_text()
                    if len(text) > len(article_text):
                        article_text = text
                        print(f"✓ Extracted from {selector}: {len(article_text)} chars")
                        break
        
        # Fall back to description if no article text
        if not article_text or len(article_text) < 200:
            if description:
                article_text = description
                print(f"⚠️  Using description as fallback: {len(article_text)} chars")
        
        if not article_text:
            print("❌ No article content found")
            return None
        
        # Parse content to extract structured data
        case_study_data = self.parse_case_study_content(
            title=title,
            content=article_text,
            url=url,
            description=description
        )
        
        return case_study_data
    
    def parse_case_study_content(self, title: str, content: str, url: str, description: str = None) -> Dict:
        """
        Parse case study content into structured format
        
        Args:
            title: Article title
            content: Article content text
            url: Page URL
            description: Meta description
            
        Returns:
            Structured case study dict
        """
        # Extract client name from title or URL
        client_name = self.extract_client_name(title, url)
        
        # Detect industry
        industry = self.detect_industry(content)
        
        # Detect technologies
        technologies = self.detect_technologies(content)
        
        # Extract problem/challenge
        problem = self.extract_section(content, [
            'challenge', 'problem', 'issue', 'pain point', 'struggle', 
            'difficulty', 'before', 'situation'
        ])
        
        # Extract solution
        solution = self.extract_section(content, [
            'solution', 'approach', 'implemented', 'built', 'developed',
            'created', 'how we', 'what we did'
        ])
        
        # Extract results
        results = self.extract_section(content, [
            'result', 'outcome', 'impact', 'achievement', 'success',
            'improvement', 'growth', 'increase', 'reduction'
        ])
        
        # Extract metrics if available
        metrics = self.extract_metrics(content)
        if metrics:
            if results and 'Not specified' not in results:
                results = f"{results} {metrics}"
            else:
                results = metrics
        
        # Create case study object
        case_study = {
            "id": self.case_study_counter,
            "client_name": client_name,
            "industry": industry,
            "problem": problem if problem else (description or "Not specified"),
            "solution": solution or "Not specified",
            "technologies": technologies[:15],  # Limit to 15
            "results": results or "Not specified",
            "duration": "Not specified",
            "url": url,
            "metadata": {
                "extracted_at": time.strftime('%Y-%m-%d %H:%M:%S'),
                "confidence": "high" if len(technologies) > 3 else "medium",
                "source": "playwright_scraper"
            }
        }
        
        self.case_study_counter += 1
        return case_study
    
    def extract_client_name(self, title: str, url: str) -> str:
        """Extract client/company name from title or URL"""
        if not title:
            return "Unknown Client"
        
        # Common patterns in titles
        # "How Shuru Scaled Paper.id's Fintech Platform"
        # "The Engineering Behind Pickup Coffee's Record-Breaking Growth"
        # "How HaloDoc Reduced 40% Support Burden..."
        # "How Shuru Helped GFP Achieve..."
        
        # Look for possessive patterns (more flexible)
        possessive_match = re.search(r"([A-Z][a-zA-Z]+(?:[.\s]+[A-Z][a-zA-Z]+)*)'s", title)
        if possessive_match:
            return possessive_match.group(1)
        
        # Look for common company name patterns
        company_patterns = [
            (r"pickup coffee", "Pickup Coffee"),
            (r"paper\.?id", "Paper.id"),
            (r"halodoc", "HaloDoc"),
            (r"happy skin", "Happy Skin"),
            (r"rural net", "Rural Net"),
            (r"equiti", "Equiti"),
            (r"mosaic", "Mosaic"),
            (r"louise", "Louise"),
            (r"ontic", "Ontic"),
            (r"green future project|gfp", "Green Future Project (GFP)"),
            (r"blk cosmetics|blk", "BLK Cosmetics"),
        ]
        
        title_lower = title.lower()
        for pattern, name in company_patterns:
            if re.search(pattern, title_lower):
                return name
        
        # Look for "How [Company] Verb" or "How Shuru Helped [Company]"
        helped_match = re.search(r"How Shuru (?:Helped|Took|Delivered|Scaled)\s+([A-Z][a-zA-Z]+(?:\s+[A-Z][a-zA-Z]+)?)", title)
        if helped_match:
            name = helped_match.group(1)
            if name not in ['Ideas', 'Idea', 'A', 'The', 'From']:
                return name
        
        # Look for "How [Company] Verb"
        how_match = re.search(r"How\s+([A-Z][a-zA-Z]+(?:\s+[A-Z][a-zA-Z]+)?)\s+(?:Reduced|Cut|Achieved|Transformed|Scaled)", title)
        if how_match:
            return how_match.group(1)
        
        # Look for "for X" or "with X" or "behind X"
        for_match = re.search(r"(?:for|with|behind)\s+([A-Z][a-zA-Z]+(?:\s+[A-Z][a-zA-Z]+)*)", title)
        if for_match:
            name = for_match.group(1)
            # Clean up common words
            if name not in ['The', 'This', 'That', 'Record', 'Breaking', 'Just', 'Higher']:
                return name
        
        # Extract from URL slug - try to get the main subject
        url_parts = url.split('/')[-1].split('-')
        # Look for capitalized words that might be company names
        for part in url_parts:
            if len(part) > 2 and part[0].isupper():
                return part.title()
        
        # Use first few words of title
        words = title.split()[:3]
        return ' '.join(words)
    
    def detect_industry(self, content: str) -> str:
        """Detect industry from content"""
        content_lower = content.lower()
        
        industries = {
            'FinTech': ['fintech', 'finance', 'financial', 'banking', 'payment'],
            'E-commerce': ['ecommerce', 'e-commerce', 'retail', 'shopping', 'marketplace'],
            'Food & Beverage': ['coffee', 'food', 'restaurant', 'beverage', 'dining', 'meal'],
            'Healthcare': ['healthcare', 'health', 'medical', 'hospital', 'patient'],
            'Technology': ['software', 'platform', 'saas', 'technology', 'tech'],
            'AgriTech': ['agriculture', 'farming', 'agritech', 'crop', 'farm'],
            'Logistics': ['logistics', 'delivery', 'shipping', 'supply chain'],
        }
        
        for industry, keywords in industries.items():
            if any(keyword in content_lower for keyword in keywords):
                return industry
        
        return "Technology"
    
    def detect_technologies(self, content: str) -> List[str]:
        """Detect technologies mentioned in content"""
        detected = set()
        content_lower = content.lower()
        
        for tech in self.TECH_KEYWORDS:
            pattern = r'\b' + re.escape(tech.lower()) + r'\b'
            if re.search(pattern, content_lower):
                detected.add(tech)
        
        return sorted(list(detected))
    
    def extract_section(self, content: str, keywords: List[str]) -> Optional[str]:
        """
        Extract text section based on keywords
        
        Args:
            content: Full content text
            keywords: Keywords to look for
            
        Returns:
            Extracted section or None
        """
        content_lower = content.lower()
        lines = content.split('\n')
        
        # Find lines containing keywords
        for i, line in enumerate(lines):
            line_lower = line.lower()
            if any(keyword in line_lower for keyword in keywords):
                # Extract next few lines (paragraph)
                start = i
                end = min(i + 10, len(lines))
                section_lines = []
                
                for j in range(start, end):
                    text = lines[j].strip()
                    if text and len(text) > 20:
                        section_lines.append(text)
                    if len(' '.join(section_lines)) > 300:
                        break
                
                if section_lines:
                    section = ' '.join(section_lines)
                    # Clean up
                    section = re.sub(r'\s+', ' ', section)
                    return section[:500]  # Limit length
        
        return None
    
    def extract_metrics(self, content: str) -> Optional[str]:
        """Extract numerical metrics from content"""
        metrics = []
        
        # Look for percentages
        percent_matches = re.findall(r'\d+%\s+(?:increase|improvement|growth|reduction|decrease)', content, re.IGNORECASE)
        metrics.extend(percent_matches[:3])
        
        # Look for X times/x growth
        times_matches = re.findall(r'\d+x\s+(?:growth|increase|faster)', content, re.IGNORECASE)
        metrics.extend(times_matches[:2])
        
        # Look for revenue/cost figures
        money_matches = re.findall(r'[\$€£]\d+(?:K|M|B)?', content)
        metrics.extend(money_matches[:2])
        
        if metrics:
            return ', '.join(metrics)
        
        return None
    
    async def discover_case_study_urls(self, browser: Browser) -> List[str]:
        """
        Discover all case study URLs from insights and work pages
        
        Args:
            browser: Playwright browser instance
            
        Returns:
            List of discovered case study URLs
        """
        discovery_urls = [
            "https://www.shurutech.com/work",
            "https://www.shurutech.com/insights",
            "https://www.shurutech.com/insights?category=Case+Study"
        ]
        
        discovered_urls = set()
        
        for url in discovery_urls:
            print(f"\n{'='*70}")
            print(f"Discovering case studies from: {url}")
            print('='*70)
            
            try:
                page = await browser.new_page()
                await page.goto(url, wait_until='load')
                
                # Wait longer for dynamic content to load
                print("Waiting for content to render...")
                await page.wait_for_timeout(8000)  # 8 seconds for portfolio to load
                
                # Try multiple selectors for case study links
                selectors = [
                    'a[href*="/insights/case-study/"]',
                    'a[href*="/case-study/"]',
                    'a[href*="/work/"]',
                ]
                
                for selector in selectors:
                    links = await page.query_selector_all(selector)
                    print(f"  Found {len(links)} links matching '{selector}'")
                    
                    for link in links:
                        href = await link.get_attribute('href')
                        if href and '/case-study/' in href:
                            # Make absolute URL
                            if href.startswith('/'):
                                href = f"https://www.shurutech.com{href}"
                            discovered_urls.add(href)
                
                # Also check for all links that might contain case study references
                all_links = await page.query_selector_all('a[href]')
                for link in all_links:
                    href = await link.get_attribute('href')
                    if href and 'case-study' in href.lower():
                        if href.startswith('/'):
                            href = f"https://www.shurutech.com{href}"
                        discovered_urls.add(href)
                
                await page.close()
                print(f"✓ Total unique URLs discovered so far: {len(discovered_urls)}")
                
            except Exception as e:
                print(f"❌ Error discovering from {url}: {e}")
        
        # Filter out any non-case-study URLs
        case_study_urls = [
            url for url in discovered_urls 
            if '/insights/case-study/' in url or '/work/case-study/' in url
        ]
        
        print(f"\n{'='*70}")
        print(f"✅ Discovery complete! Found {len(case_study_urls)} case study URLs")
        print('='*70)
        
        # Print all discovered URLs
        if case_study_urls:
            print("\nDiscovered URLs:")
            for i, url in enumerate(sorted(case_study_urls), 1):
                print(f"  {i}. {url}")
        
        return case_study_urls
    
    async def scrape_multiple_case_studies(self, urls: List[str]) -> List[Dict]:
        """
        Scrape multiple case study URLs
        
        Args:
            urls: List of case study URLs
            
        Returns:
            List of case study dicts
        """
        case_studies = []
        
        async with async_playwright() as p:
            print(f"\nLaunching Chromium browser (headless={self.headless})...")
            browser = await p.chromium.launch(headless=self.headless)
            
            for url in urls:
                case_study = await self.scrape_case_study_url(url, browser)
                if case_study:
                    case_studies.append(case_study)
                
                # Brief pause between requests
                await asyncio.sleep(2)
            
            await browser.close()
            print(f"\n{'='*70}")
            print(f"Scraping complete! Extracted {len(case_studies)} case studies")
            print('='*70)
        
        return case_studies
    
    async def auto_discover_and_scrape(self) -> List[Dict]:
        """
        Automatically discover and scrape all case studies
        
        Returns:
            List of case study dicts
        """
        case_studies = []
        
        async with async_playwright() as p:
            print(f"\nLaunching Chromium browser (headless={self.headless})...")
            browser = await p.chromium.launch(headless=self.headless)
            
            # Phase 1: Discover URLs
            discovered_urls = await self.discover_case_study_urls(browser)
            
            if not discovered_urls:
                print("⚠️  No case study URLs discovered. Check if pages loaded correctly.")
                await browser.close()
                return []
            
            # Phase 2: Scrape each URL
            print(f"\n{'='*70}")
            print(f"Starting scraping phase ({len(discovered_urls)} URLs)")
            print('='*70)
            
            for i, url in enumerate(discovered_urls, 1):
                print(f"\n[{i}/{len(discovered_urls)}]")
                case_study = await self.scrape_case_study_url(url, browser)
                if case_study:
                    case_studies.append(case_study)
                
                # Be respectful - wait between requests
                await asyncio.sleep(2)
            
            await browser.close()
            
            print(f"\n{'='*70}")
            print(f"✅ Auto-scraping complete! Extracted {len(case_studies)}/{len(discovered_urls)} case studies")
            print('='*70)
        
        return case_studies
    
    def load_urls_from_file(self, filepath: str) -> List[str]:
        """Load URLs from text file (one per line, # for comments)"""
        urls = []
        path = Path(filepath)
        
        if not path.exists():
            print(f"❌ File not found: {filepath}")
            return urls
        
        with open(path, 'r') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#'):
                    urls.append(line)
        
        print(f"✓ Loaded {len(urls)} URLs from {filepath}")
        return urls
    
    def save_case_studies(self, case_studies: List[Dict], output_file: str = 'case_studies_scraped.json'):
        """Save case studies to JSON file"""
        output_path = Path(output_file)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(case_studies, f, indent=2, ensure_ascii=False)
        
        print(f"\n✓ Saved {len(case_studies)} case studies to {output_file}")


async def main():
    """Main execution function"""
    import sys
    
    scraper = PlaywrightScraper(headless=True, timeout=60000)
    
    # Check command line arguments
    mode = sys.argv[1] if len(sys.argv) > 1 else "auto"
    
    if mode == "auto":
        # Auto-discover and scrape all case studies
        print("🔍 AUTO-DISCOVERY MODE: Finding all case studies...")
        print("="*70)
        case_studies = await scraper.auto_discover_and_scrape()
    
    elif mode == "manual":
        # Use manual URL list from file
        print("📝 MANUAL MODE: Using case_study_urls.txt...")
        print("="*70)
        urls = scraper.load_urls_from_file('case_study_urls.txt')
        if not urls:
            print("No URLs to scrape. Add URLs to case_study_urls.txt")
            return
        case_studies = await scraper.scrape_multiple_case_studies(urls)
    
    else:
        print(f"❌ Unknown mode: {mode}")
        print("Usage: python scrape_with_playwright.py [auto|manual]")
        print("  auto   - Auto-discover all case studies (default)")
        print("  manual - Use case_study_urls.txt")
        return
    
    # Save to file
    if case_studies:
        scraper.save_case_studies(case_studies, 'case_studies_scraped.json')
        
        # Print summary
        print("\n" + "=" * 70)
        print("CASE STUDIES SUMMARY")
        print("=" * 70)
        for cs in case_studies:
            print(f"\nID: {cs['id']}")
            print(f"Client: {cs['client_name']}")
            print(f"Industry: {cs['industry']}")
            print(f"Technologies: {', '.join(cs['technologies'][:5]) if cs['technologies'] else 'None detected'}")
            print(f"Problem: {cs['problem'][:100]}...")
            print(f"Solution: {cs['solution'][:100]}...")
            print(f"Results: {cs['results'][:100]}...")
            print(f"URL: {cs['url']}")
    else:
        print("\n❌ No case studies were successfully scraped")


if __name__ == "__main__":
    asyncio.run(main())

