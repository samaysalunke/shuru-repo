"""
Advanced Web Scraper for Shuru Tech Website
Features:
- Multi-strategy content extraction
- NLP pattern matching for case studies
- Smart crawling with depth control
- Intelligent technology and industry detection
"""

import requests
from bs4 import BeautifulSoup
import json
import time
import re
import logging
from urllib.parse import urljoin, urlparse
from urllib.robotparser import RobotFileParser
from collections import deque
from typing import List, Dict, Set, Tuple

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)


class AdvancedShuruTechScraper:
    """Advanced scraper with intelligent extraction capabilities"""

    # Comprehensive technology keywords for detection
    # Organized by category for better maintainability
    TECH_KEYWORDS = {
        'frontend': [
            # Core frameworks
            'React', 'React.js', 'Angular', 'Vue', 'Vue.js', 'Svelte', 'Ember.js',
            # Meta frameworks
            'Next.js', 'Nuxt.js', 'Gatsby', 'Remix',
            # Languages
            'JavaScript', 'TypeScript', 'HTML5', 'CSS3', 'SASS', 'SCSS', 'LESS',
            # UI Libraries & Tools
            'Tailwind', 'TailwindCSS', 'Bootstrap', 'Material-UI', 'Ant Design',
            'Chakra UI', 'Shadcn', 'Redux', 'MobX', 'Zustand', 'Webpack', 'Vite', 'Babel'
        ],
        'backend': [
            # Node.js ecosystem
            'Node.js', 'Express', 'Express.js', 'Nest.js', 'Fastify', 'Koa',
            # Python
            'Python', 'Django', 'Flask', 'FastAPI', 'Pyramid', 'Tornado',
            # Java
            'Java', 'Spring', 'Spring Boot', 'Spring Cloud', 'Hibernate', 'Quarkus',
            # Ruby
            'Ruby', 'Rails', 'Ruby on Rails', 'Sinatra',
            # Go
            'Go', 'Golang', 'Gin', 'Echo',
            # PHP
            'PHP', 'Laravel', 'Symfony', 'CodeIgniter', 'Yii',
            # .NET
            '.NET', 'ASP.NET', 'C#', '.NET Core',
            # Other
            'Rust', 'Elixir', 'Phoenix', 'Scala', 'Play Framework'
        ],
        'mobile': [
            # Cross-platform
            'React Native', 'Flutter', 'Ionic', 'Cordova', 'Xamarin', 'Capacitor',
            # iOS
            'iOS', 'Swift', 'SwiftUI', 'Objective-C', 'Xcode',
            # Android
            'Android', 'Kotlin', 'Java Android', 'Jetpack Compose', 'Android Studio'
        ],
        'database': [
            # SQL Databases
            'PostgreSQL', 'MySQL', 'MariaDB', 'SQL Server', 'Oracle', 'SQLite',
            # NoSQL Databases
            'MongoDB', 'Cassandra', 'CouchDB', 'Neo4j', 'ArangoDB',
            # In-Memory & Cache
            'Redis', 'Memcached', 'Hazelcast',
            # Search & Analytics
            'Elasticsearch', 'Solr', 'Algolia',
            # Cloud Databases
            'DynamoDB', 'Firebase', 'Firestore', 'Supabase', 'PlanetScale',
            # General
            'SQL', 'NoSQL'
        ],
        'cloud': [
            # Major Cloud Providers
            'AWS', 'Amazon Web Services', 'Azure', 'Microsoft Azure',
            'Google Cloud', 'GCP', 'Google Cloud Platform',
            # Cloud Services
            'AWS Lambda', 'AWS EC2', 'AWS S3', 'AWS RDS',
            'Azure Functions', 'Azure DevOps',
            'Google Cloud Functions', 'Google App Engine',
            # Platform as a Service
            'Heroku', 'DigitalOcean', 'Vercel', 'Netlify', 'Render',
            'Railway', 'Fly.io', 'CloudFlare', 'Cloudflare Workers'
        ],
        'devops': [
            # Containers
            'Docker', 'Podman', 'containerd',
            # Orchestration
            'Kubernetes', 'K8s', 'Docker Swarm', 'Nomad', 'OpenShift',
            # CI/CD Tools
            'Jenkins', 'GitLab CI', 'GitLab CI/CD', 'GitHub Actions',
            'CircleCI', 'Travis CI', 'Azure Pipelines', 'Bamboo',
            'TeamCity', 'ArgoCD', 'Flux',
            # Infrastructure as Code
            'Terraform', 'Ansible', 'Puppet', 'Chef', 'CloudFormation',
            'Pulumi', 'Vagrant',
            # Monitoring & Logging
            'Prometheus', 'Grafana', 'ELK Stack', 'Datadog', 'New Relic',
            'Splunk', 'Sentry'
        ],
        'cicd': [
            # CI/CD Concepts & Tools
            'CI/CD', 'Continuous Integration', 'Continuous Deployment',
            'Continuous Delivery', 'Jenkins', 'GitHub Actions', 'GitLab CI',
            'CircleCI', 'Travis CI', 'Bamboo', 'TeamCity', 'Azure DevOps',
            'Bitbucket Pipelines', 'Drone', 'Spinnaker'
        ],
        'ai_ml': [
            # Machine Learning
            'Machine Learning', 'ML', 'AI', 'Artificial Intelligence',
            'Deep Learning', 'Neural Network', 'Neural Networks',
            # Frameworks
            'TensorFlow', 'PyTorch', 'Keras', 'Scikit-learn', 'XGBoost',
            'LightGBM', 'Caffe', 'MXNet', 'ONNX',
            # NLP
            'NLP', 'Natural Language Processing', 'BERT', 'GPT', 'Transformer',
            'spaCy', 'NLTK', 'Hugging Face',
            # Computer Vision
            'Computer Vision', 'OpenCV', 'YOLO', 'CNN',
            # Other
            'Jupyter', 'Pandas', 'NumPy', 'SciPy'
        ],
        'architecture': [
            # API Architectures
            'REST', 'REST API', 'RESTful', 'GraphQL', 'gRPC', 'SOAP',
            # Architectural Patterns
            'Microservices', 'Monolith', 'Serverless', 'Event-Driven',
            'Service-Oriented Architecture', 'SOA',
            # Communication
            'WebSocket', 'Server-Sent Events', 'SSE', 'Message Queue',
            'Apache Kafka', 'RabbitMQ', 'ActiveMQ', 'MQTT', 'ZeroMQ',
            # Design Patterns
            'Event Sourcing', 'CQRS', 'Saga Pattern', 'API Gateway'
        ],
        'testing': [
            # Testing Frameworks
            'Jest', 'Mocha', 'Chai', 'Jasmine', 'Pytest', 'JUnit', 'TestNG',
            'RSpec', 'Cucumber', 'Selenium', 'Cypress', 'Playwright',
            'Puppeteer', 'Testing Library', 'Vitest'
        ],
        'other': [
            # Version Control
            'Git', 'GitHub', 'GitLab', 'Bitbucket', 'SVN',
            # Blockchain
            'Blockchain', 'Ethereum', 'Solidity', 'Web3',
            # CMS
            'WordPress', 'Drupal', 'Contentful', 'Strapi', 'Sanity',
            # Real-time
            'Socket.io', 'WebRTC',
            # API Tools
            'Postman', 'Swagger', 'OpenAPI'
        ]
    }

    # Comprehensive industry keywords for classification
    # Each industry mapped to relevant keywords for robust detection
    INDUSTRY_KEYWORDS = {
        'E-commerce': [
            'ecommerce', 'e-commerce', 'online store', 'online shop', 'retail', 'shopping',
            'cart', 'checkout', 'marketplace', 'b2c', 'online retail', 'webshop',
            'product catalog', 'storefront', 'shopify', 'woocommerce', 'magento'
        ],
        'FinTech': [
            'fintech', 'finance', 'financial', 'banking', 'payment', 'payments',
            'financial services', 'cryptocurrency', 'crypto', 'blockchain finance',
            'wealth management', 'trading', 'stock', 'investment', 'lending',
            'digital wallet', 'mobile banking', 'neobank', 'payment gateway',
            'remittance', 'forex', 'peer-to-peer lending', 'robo-advisor'
        ],
        'Healthcare': [
            'healthcare', 'health', 'medical', 'hospital', 'patient', 'clinic',
            'telemedicine', 'healthtech', 'pharmaceutical', 'clinical', 'doctor',
            'nurse', 'diagnosis', 'treatment', 'therapy', 'medicine', 'pharmacy',
            'electronic health record', 'ehr', 'emr', 'telehealth', 'wellness',
            'mental health', 'healthcare provider', 'medical device'
        ],
        'SaaS': [
            'saas', 'software as a service', 'cloud software', 'subscription',
            'b2b software', 'enterprise software', 'cloud-based', 'subscription model',
            'software platform', 'api service', 'hosted solution', 'paas',
            'platform as a service', 'multi-tenant'
        ],
        'AgriTech': [
            'agritech', 'agriculture', 'farming', 'agri', 'crop', 'crops',
            'agricultural', 'farm', 'precision agriculture', 'agtech',
            'livestock', 'harvest', 'irrigation', 'soil', 'farmer',
            'agricultural technology', 'farm management', 'vertical farming'
        ],
        'Logistics': [
            'logistics', 'supply chain', 'shipping', 'delivery', 'warehouse',
            'transportation', 'freight', 'fleet', 'distribution', 'courier',
            'last mile', 'fulfillment', 'logistics management', 'cargo',
            'dispatch', 'route optimization', 'inventory management',
            'supply chain management', 'third-party logistics', '3pl'
        ],
        'Real Estate': [
            'real estate', 'property', 'housing', 'proptech', 'realty',
            'real estate tech', 'rental', 'lease', 'landlord', 'tenant',
            'commercial property', 'residential property', 'real estate management',
            'property management', 'real estate platform', 'home buying', 'home selling'
        ],
        'Media & Entertainment': [
            'media', 'streaming', 'content', 'video', 'entertainment',
            'music', 'gaming', 'games', 'movie', 'film', 'television', 'tv',
            'broadcast', 'publishing', 'digital media', 'content creation',
            'video streaming', 'music streaming', 'ott', 'over-the-top',
            'social media', 'influencer', 'creator economy'
        ],
        'Insurance': [
            'insurance', 'insurtech', 'claims', 'policy', 'policies',
            'underwriting', 'insurer', 'insurance company', 'life insurance',
            'health insurance', 'auto insurance', 'property insurance',
            'insurance platform', 'insurance technology', 'reinsurance',
            'actuarial', 'risk assessment'
        ],
        'Retail': [
            'retail', 'store', 'stores', 'merchandise', 'pos', 'point of sale',
            'brick and mortar', 'retail chain', 'department store', 'boutique',
            'retail technology', 'retail management', 'retail analytics',
            'omnichannel', 'in-store', 'retail operations'
        ],
        'Education': [
            'education', 'edtech', 'learning', 'school', 'university', 'college',
            'e-learning', 'lms', 'learning management system', 'training',
            'online learning', 'online education', 'student', 'teacher',
            'educational technology', 'course', 'classroom', 'curriculum',
            'tutoring', 'mooc', 'educational platform'
        ],
        'Travel & Hospitality': [
            'travel', 'hospitality', 'hotel', 'tourism', 'booking', 'reservation',
            'restaurant', 'accommodation', 'vacation', 'trip', 'flight',
            'airline', 'travel booking', 'travel agency', 'hotel booking',
            'food service', 'hospitality industry', 'guest', 'lodging'
        ],
        'Manufacturing': [
            'manufacturing', 'industry 4.0', 'production', 'factory', 'factories',
            'supply chain', 'assembly', 'industrial', 'plant', 'manufacturing process',
            'quality control', 'automation', 'production line', 'manufacturer',
            'industrial automation', 'smart manufacturing'
        ],
        'Energy': [
            'energy', 'renewable', 'renewable energy', 'solar', 'wind', 'utilities',
            'power', 'electricity', 'oil', 'gas', 'petroleum', 'energy sector',
            'clean energy', 'green energy', 'energy management', 'power generation',
            'energy efficiency', 'grid', 'utility company'
        ],
        'Automotive': [
            'automotive', 'automobile', 'car', 'vehicle', 'auto', 'mobility',
            'electric vehicle', 'ev', 'autonomous vehicle', 'self-driving',
            'automotive industry', 'car manufacturer', 'ride-sharing',
            'car rental', 'automotive technology'
        ],
        'Telecommunications': [
            'telecommunications', 'telecom', 'telco', '5g', '4g', 'network',
            'mobile network', 'internet service provider', 'isp', 'connectivity',
            'broadband', 'fiber optic', 'wireless', 'cellular'
        ],
        'Food & Beverage': [
            'food', 'beverage', 'restaurant', 'food delivery', 'food service',
            'catering', 'dining', 'food tech', 'foodtech', 'meal',
            'food industry', 'culinary', 'recipe', 'cooking', 'food ordering'
        ],
        'Gaming': [
            'gaming', 'game', 'games', 'video game', 'esports', 'e-sports',
            'game development', 'game studio', 'mobile gaming', 'pc gaming',
            'console gaming', 'game publisher', 'indie game', 'multiplayer'
        ],
        'Fashion & Apparel': [
            'fashion', 'apparel', 'clothing', 'garment', 'textile', 'fashion tech',
            'fashion industry', 'fashion retail', 'fashion ecommerce', 'style',
            'wardrobe', 'fashion platform', 'online fashion'
        ],
        'Construction': [
            'construction', 'building', 'infrastructure', 'contractor', 'architecture',
            'construction industry', 'construction management', 'construction technology',
            'construction project', 'civil engineering', 'building materials'
        ],
        'Legal Tech': [
            'legal tech', 'legaltech', 'legal', 'law', 'lawyer', 'attorney',
            'legal services', 'legal technology', 'legal platform', 'litigation',
            'compliance', 'contract management', 'legal software'
        ],
        'HR Tech': [
            'hr tech', 'hrtech', 'human resources', 'hr', 'recruitment', 'hiring',
            'talent', 'talent management', 'employee', 'workforce', 'payroll',
            'hr management', 'hr platform', 'applicant tracking', 'onboarding'
        ],
        'Cybersecurity': [
            'cybersecurity', 'cyber security', 'security', 'infosec', 'information security',
            'data security', 'network security', 'threat detection', 'firewall',
            'encryption', 'security platform', 'vulnerability', 'penetration testing'
        ],
        'Government': [
            'government', 'public sector', 'civic tech', 'govtech', 'municipal',
            'federal', 'state government', 'public administration', 'civic',
            'government services', 'e-government'
        ],
        'Non-profit': [
            'non-profit', 'nonprofit', 'ngo', 'charity', 'charitable', 'foundation',
            'social impact', 'social good', 'philanthropic', 'humanitarian',
            'non-governmental organization'
        ]
    }

    # NLP patterns for case study extraction
    PROBLEM_PATTERNS = [
        r'(challenge|problem|issue|struggle|difficulty|pain point|needed to|required to)[\w\s:,-]{20,200}',
        r'(facing|faced with|dealing with|suffering from)[\w\s:,-]{20,200}',
        r'(couldn\'t|wasn\'t able to|failed to|lacked)[\w\s:,-]{20,200}'
    ]

    SOLUTION_PATTERNS = [
        r'(implemented|developed|built|created|designed|deployed|solution|approach)[\w\s:,-]{20,200}',
        r'(we developed|we built|we created|we implemented|we designed)[\w\s:,-]{20,200}',
        r'(using|leveraging|utilizing|by building|by creating)[\w\s:,-]{20,200}'
    ]

    RESULT_PATTERNS = [
        r'(increased by|improved by|reduced by|decreased by|achieved|grew by)\s+\d+%',
        r'(\d+%\s+(increase|improvement|reduction|growth|decrease))',
        r'(result|outcome|impact|achievement|success)[\w\s:,-]{20,200}',
        r'(saved|generated|earned|revenue|profit)\s+[\$€£¥]\d+'
    ]

    # Priority URL keywords
    PRIORITY_KEYWORDS = ['work', 'case', 'project', 'portfolio', 'client', 'about',
                         'service', 'solution', 'story', 'testimonial', 'insights', 
                         'blog', 'case-study']

    # Priority seed URLs to scrape first
    PRIORITY_SEED_URLS = [
        'https://www.shurutech.com/work',
        'https://www.shurutech.com/insights',
        'https://www.shurutech.com/insights?category=Case+Study'
    ]

    def __init__(self, base_url='https://www.shurutech.com/', max_pages=30, max_depth=3):
        self.base_url = base_url
        self.max_pages = max_pages
        self.max_depth = max_depth
        self.visited_urls = set()
        self.url_queue = deque([(base_url, 0)])  # (url, depth)

        self.knowledge_base = {
            "case_studies": [],
            "services": [],
            "technologies": [],
            "industries": []
        }

        self.robot_parser = RobotFileParser()
        self.case_study_id_counter = 1

        # Prepend priority seed URLs to queue (they'll be scraped first)
        for priority_url in reversed(self.PRIORITY_SEED_URLS):
            self.url_queue.appendleft((priority_url, 0))
        
        logger.info("=" * 70)
        logger.info("Advanced Shuru Tech Scraper Initialized")
        logger.info(f"Base URL: {base_url}")
        logger.info(f"Max Pages: {max_pages}")
        logger.info(f"Max Depth: {max_depth}")
        logger.info(f"Priority Seed URLs: {len(self.PRIORITY_SEED_URLS)}")
        for url in self.PRIORITY_SEED_URLS:
            logger.info(f"  - {url}")
        logger.info("=" * 70)

    def check_robots_txt(self):
        """Check and respect robots.txt"""
        try:
            robots_url = urljoin(self.base_url, '/robots.txt')
            logger.info(f"Checking robots.txt at {robots_url}")
            self.robot_parser.set_url(robots_url)
            self.robot_parser.read()
            logger.info("robots.txt loaded successfully")
            return True
        except Exception as e:
            logger.warning(f"Could not read robots.txt: {str(e)}")
            return False

    def can_fetch(self, url):
        """Check if we're allowed to fetch this URL"""
        try:
            return self.robot_parser.can_fetch("*", url)
        except:
            return True

    def fetch_page(self, url, timeout=10):
        """Fetch page content with robust error handling"""
        if not self.can_fetch(url):
            logger.warning(f"⚠️  Blocked by robots.txt: {url}")
            return None

        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (compatible; ShuruTechBot/2.0; +http://www.shurutech.com)'
            }
            logger.info(f"Fetching: {url}")
            response = requests.get(url, headers=headers, timeout=timeout)
            response.raise_for_status()

            # Validate content is meaningful (>100 chars)
            if len(response.text) < 100:
                logger.warning(f"⚠️  Skipping {url}: Content too short ({len(response.text)} chars)")
                return None

            logger.info(f"✓ Successfully fetched (Status: {response.status_code}, Size: {len(response.text)} bytes)")
            return response.text

        except requests.exceptions.Timeout:
            logger.error(f"❌ Timeout error fetching {url} (exceeded {timeout}s)")
            return None

        except requests.exceptions.HTTPError as e:
            status_code = e.response.status_code if e.response else 'unknown'
            logger.error(f"❌ HTTP error {status_code} fetching {url}: {str(e)}")
            return None

        except requests.exceptions.ConnectionError as e:
            logger.error(f"❌ Connection error fetching {url}: {str(e)}")
            return None

        except requests.exceptions.RequestException as e:
            logger.error(f"❌ Request error fetching {url}: {str(e)}")
            return None

        except Exception as e:
            logger.error(f"❌ Unexpected error fetching {url}: {type(e).__name__} - {str(e)}")
            return None

    def extract_with_nlp_patterns(self, text: str, patterns: List[str]) -> List[str]:
        """Extract text using NLP regex patterns"""
        results = []
        for pattern in patterns:
            matches = re.finditer(pattern, text, re.IGNORECASE)
            for match in matches:
                extracted = match.group(0).strip()
                if len(extracted) > 30:  # Filter out very short matches
                    results.append(extracted)
        return results

    def detect_technologies(self, text: str) -> List[str]:
        """Detect technologies mentioned in text"""
        detected = set()
        text_lower = text.lower()

        for category, techs in self.TECH_KEYWORDS.items():
            for tech in techs:
                # Use word boundaries for more accurate matching
                pattern = r'\b' + re.escape(tech.lower()) + r'\b'
                if re.search(pattern, text_lower):
                    detected.add(tech)

        return sorted(list(detected))

    def detect_industries(self, text: str) -> List[str]:
        """
        Detect industries mentioned in text using keyword matching.
        Scans page content for industry-specific keywords and assigns matching industries.
        """
        detected = set()
        detected_keywords = {}  # Track which keywords matched
        text_lower = text.lower()

        for industry, keywords in self.INDUSTRY_KEYWORDS.items():
            for keyword in keywords:
                if keyword in text_lower:
                    detected.add(industry)
                    detected_keywords[industry] = keyword
                    break  # Found this industry, move to next

        # Log detected industries with matching keywords for debugging
        if detected:
            for industry in sorted(detected):
                logger.debug(f"    Detected industry '{industry}' (matched: '{detected_keywords[industry]}')")

        return sorted(list(detected))

    def extract_semantic_content(self, soup: BeautifulSoup) -> List[Dict]:
        """Extract content using semantic HTML tags"""
        logger.info("  Extracting content from semantic HTML tags...")
        content_blocks = []

        # Look for semantic tags
        semantic_tags = soup.find_all(['article', 'section', 'div'], class_=True)

        for tag in semantic_tags:
            class_names = ' '.join(tag.get('class', [])).lower()

            # Check if classes contain relevant keywords
            relevant_keywords = ['case', 'project', 'portfolio', 'client', 'story',
                                'testimonial', 'work', 'study']

            if any(keyword in class_names for keyword in relevant_keywords):
                text = tag.get_text(separator=' ', strip=True)
                if len(text) > 100:  # Meaningful content threshold
                    content_blocks.append({
                        'tag': tag.name,
                        'classes': class_names,
                        'text': text,
                        'element': tag
                    })
                    logger.info(f"    Found semantic content block: {tag.name}.{class_names[:50]}")

        return content_blocks

    def extract_card_layouts(self, soup: BeautifulSoup) -> List[Dict]:
        """Extract content from card-based layouts"""
        logger.info("  Extracting content from card layouts...")
        cards = []

        # Common card class patterns
        card_patterns = ['card', 'item', 'box', 'tile', 'panel', 'block']

        for pattern in card_patterns:
            elements = soup.find_all(class_=lambda x: x and pattern in x.lower())

            for elem in elements:
                # Extract title
                title_elem = elem.find(['h1', 'h2', 'h3', 'h4', 'h5', 'h6'])
                title = title_elem.get_text(strip=True) if title_elem else ''

                # Extract description
                desc_elem = elem.find('p')
                description = desc_elem.get_text(strip=True) if desc_elem else ''

                # Get all text
                full_text = elem.get_text(separator=' ', strip=True)

                if title or (len(full_text) > 100):
                    cards.append({
                        'title': title,
                        'description': description,
                        'text': full_text,
                        'element': elem
                    })
                    logger.info(f"    Found card: {title[:50] if title else 'Untitled'}")

        return cards

    def extract_case_studies_advanced(self, soup: BeautifulSoup, url: str) -> List[Dict]:
        """Advanced case study extraction with multiple strategies"""
        logger.info("Extracting case studies using advanced methods...")
        case_studies = []

        # Check if this is an insights/case study detail page
        is_case_study_detail = '/insights/case-study/' in url.lower()
        if is_case_study_detail:
            logger.info("  Detected CASE STUDY DETAIL page - using enhanced extraction")

        # Strategy 1: Semantic HTML extraction
        semantic_blocks = self.extract_semantic_content(soup)

        # Strategy 2: Card layout extraction
        card_blocks = self.extract_card_layouts(soup)

        # Strategy 3: Article-based extraction for insights pages
        article_blocks = []
        if is_case_study_detail or '/insights' in url.lower():
            logger.info("  Extracting from article/blog post structure...")
            articles = soup.find_all(['article', 'main'])
            for article in articles:
                text = article.get_text(separator=' ', strip=True)
                if len(text) > 200:  # Meaningful article content
                    article_blocks.append({
                        'tag': 'article',
                        'classes': ' '.join(article.get('class', [])),
                        'text': text,
                        'element': article
                    })
                    logger.info(f"    Found article block with {len(text)} chars")

        # Combine all content blocks
        all_blocks = semantic_blocks + card_blocks + article_blocks

        for block in all_blocks:
            text = block.get('text', '')

            if len(text) < 100:  # Skip short content
                continue

            # Extract structured information using NLP patterns
            problems = self.extract_with_nlp_patterns(text, self.PROBLEM_PATTERNS)
            solutions = self.extract_with_nlp_patterns(text, self.SOLUTION_PATTERNS)
            results = self.extract_with_nlp_patterns(text, self.RESULT_PATTERNS)

            # Detect technologies and industries
            technologies = self.detect_technologies(text)
            industries = self.detect_industries(text)

            # Extract title/client name
            element = block.get('element')
            title = ''
            if element:
                title_elem = element.find(['h1', 'h2', 'h3', 'h4'])
                title = title_elem.get_text(strip=True) if title_elem else block.get('title', '')

            client_name = title.split('-')[0].strip() if '-' in title else (title or 'Unnamed Project')

            # Only create case study if we have meaningful content (>100 chars validation)
            if (problems or solutions or results) or len(technologies) > 2:
                # Validate content is meaningful
                problem_text = problems[0] if problems else "Problem description not found"
                solution_text = solutions[0] if solutions else "Solution description not found"

                # Skip if both problem and solution are too short
                if len(problem_text) < 100 and len(solution_text) < 100 and len(technologies) < 3:
                    logger.warning(f"    ⚠️  Skipping case study: Content too short")
                    continue

                case_study = {
                    "id": self.case_study_id_counter,
                    "client_name": client_name,
                    "industry": industries[0] if industries else "Not specified",
                    "problem": problem_text,
                    "solution": solution_text,
                    "technologies": technologies[:10],  # Limit to top 10
                    "results": results[0] if results else "Results not specified",
                    "duration": "Not specified",
                    "url": url,
                    "extracted_at": time.strftime('%Y-%m-%d %H:%M:%S')
                }

                case_studies.append(case_study)
                self.case_study_id_counter += 1
                logger.info(f"    ✓ Created case study #{case_study['id']}: {client_name}")

        if not case_studies:
            logger.info("    No case studies found on this page")

        return case_studies

    def extract_services_from_page(self, soup: BeautifulSoup, url: str) -> List[Dict]:
        """Extract services with improved detection including capabilities"""
        logger.info("Extracting services from page...")
        services = []
        seen_services = set()

        # Check if this is a service page
        is_service_page = 'service' in url.lower()
        if is_service_page:
            logger.info("  This is a SERVICE page - extracting with high priority")

        # Look for service containers with multiple strategies
        service_containers = []

        # Strategy 1: Find by specific class names (service, offering, solution)
        service_containers.extend(soup.find_all(class_=lambda x: x and any(
            term in x.lower() for term in ['service', 'offering', 'solution', 'what-we-do',
                                           'expertise', 'capability', 'what-we-offer']
        )))

        # Strategy 2: Find sections/divs with service-related headings
        for section in soup.find_all(['section', 'div', 'article']):
            heading = section.find(['h1', 'h2', 'h3'])
            if heading:
                heading_text = heading.get_text().lower()
                if any(term in heading_text for term in ['service', 'what we do', 'expertise',
                                                         'offering', 'solution', 'we offer']):
                    service_containers.append(section)

        logger.info(f"  Found {len(service_containers)} potential service containers")

        for container in service_containers:
            # Find individual service items
            service_items = container.find_all(['div', 'li', 'article', 'section'], recursive=True)

            for item in service_items:
                # Extract service name from h1-h4 headings
                title_elem = item.find(['h1', 'h2', 'h3', 'h4'])

                if not title_elem:
                    # Try strong/b tags as fallback
                    title_elem = item.find(['strong', 'b'])

                if title_elem:
                    service_name = title_elem.get_text(strip=True)

                    # Skip if too short or already seen (min 3 chars)
                    if not service_name or len(service_name) < 3 or service_name in seen_services:
                        continue

                    # Extract description from first paragraph
                    description = ''
                    first_p = item.find('p')
                    if first_p:
                        description = first_p.get_text(strip=True)

                    # Validate service has meaningful content (>50 chars)
                    if len(description) < 50 and len(service_name) < 10:
                        logger.warning(f"    ⚠️  Skipping service '{service_name}': Content too short")
                        continue

                    # Extract capabilities from bullet points (max 5)
                    capabilities = []

                    # Look for unordered/ordered lists
                    lists = item.find_all(['ul', 'ol'], limit=2)
                    for lst in lists:
                        list_items = lst.find_all('li', limit=5)
                        for li in list_items:
                            capability_text = li.get_text(strip=True)
                            if capability_text and len(capability_text) > 5:
                                capabilities.append(capability_text)
                                if len(capabilities) >= 5:
                                    break
                        if len(capabilities) >= 5:
                            break

                    # If no list items, try to find bullet-like patterns in text
                    if not capabilities:
                        # Look for text with bullet points or dashes
                        all_text = item.get_text(separator='\n', strip=True)
                        lines = all_text.split('\n')
                        for line in lines[:10]:  # Check first 10 lines
                            line = line.strip()
                            # Check if line starts with bullet-like characters
                            if line and any(line.startswith(char) for char in ['•', '-', '✓', '→', '*']):
                                clean_line = line.lstrip('•-✓→* ').strip()
                                if len(clean_line) > 5 and len(clean_line) < 200:
                                    capabilities.append(clean_line)
                                    if len(capabilities) >= 5:
                                        break

                    # Create service object
                    service = {
                        "name": service_name,
                        "description": description[:500] if description else "No description available",
                        "capabilities": capabilities[:5],  # Limit to max 5
                        "url": url
                    }

                    services.append(service)
                    seen_services.add(service_name)
                    logger.info(f"    ✓ Found service: {service_name}")
                    logger.info(f"      - Description length: {len(description)} chars")
                    logger.info(f"      - Capabilities: {len(capabilities)}")

        if not services:
            logger.info("    No services found on this page")
        else:
            logger.info(f"  Total services extracted: {len(services)}")

        return services

    def format_case_studies(self) -> List[Dict]:
        """Format and standardize case studies output"""
        logger.info("Formatting case studies...")

        formatted = []
        for cs in self.knowledge_base['case_studies']:
            formatted_cs = {
                "id": cs.get('id'),
                "client_name": cs.get('client_name', 'Unknown'),
                "industry": cs.get('industry', 'Not specified'),
                "challenge": cs.get('problem', 'Not specified'),
                "solution": cs.get('solution', 'Not specified'),
                "technologies_used": cs.get('technologies', []),
                "business_impact": cs.get('results', 'Not specified'),
                "project_duration": cs.get('duration', 'Not specified'),
                "source_url": cs.get('url', ''),
                "metadata": {
                    "extracted_at": cs.get('extracted_at', ''),
                    "confidence": "high" if len(cs.get('technologies', [])) > 2 else "medium"
                }
            }
            formatted.append(formatted_cs)

        return formatted

    def prioritize_url(self, url: str) -> int:
        """Calculate priority score for URL (higher is better)"""
        score = 0
        url_lower = url.lower()

        # Maximum priority for case study detail pages
        if '/insights/case-study/' in url_lower:
            score += 100
            logger.info(f"  MAXIMUM priority case study page: {url}")
        
        # Very high priority for insights pages
        elif '/insights' in url_lower:
            score += 50
            logger.info(f"  Very high priority insights page: {url}")

        # High priority for service pages
        elif 'service' in url_lower:
            score += 20
            logger.info(f"  High priority service page: {url}")

        # Standard priority keywords
        for keyword in self.PRIORITY_KEYWORDS:
            if keyword in url_lower:
                score += 10

        # Deprioritize certain patterns
        if any(skip in url_lower for skip in ['login', 'signup', 'cart', 'checkout', 'admin']):
            score -= 50

        return score

    def scrape_page(self, url: str, depth: int):
        """Scrape a single page and extract content with error handling"""
        if url in self.visited_urls or len(self.visited_urls) >= self.max_pages:
            return

        logger.info("=" * 70)
        logger.info(f"📄 Scraping: {url} (depth: {depth})")

        self.visited_urls.add(url)

        try:
            # Fetch page
            html_content = self.fetch_page(url)
            if not html_content:
                logger.warning(f"⚠️  Skipping {url}: No content returned")
                return

            # Parse with BeautifulSoup
            try:
                soup = BeautifulSoup(html_content, 'html.parser')
            except Exception as e:
                logger.error(f"❌ Failed to parse HTML for {url}: {str(e)}")
                return

            # Count text blocks
            all_blocks = soup.find_all(['article', 'section', 'div'], class_=True)
            logger.info(f"   Found {len(all_blocks)} text blocks")

            # Extract all data types with error handling
            case_studies = []
            services = []

            try:
                case_studies = self.extract_case_studies_advanced(soup, url)
            except Exception as e:
                logger.error(f"❌ Error extracting case studies from {url}: {str(e)}")

            try:
                services = self.extract_services_from_page(soup, url)
            except Exception as e:
                logger.error(f"❌ Error extracting services from {url}: {str(e)}")

            # Log extracted case studies with titles
            for cs in case_studies:
                logger.info(f"   ✓ Extracted case study: {cs.get('client_name', 'Unknown')}")

            # Log extracted services count
            if services:
                logger.info(f"   ✓ Extracted {len(services)} services")

            # Get page text for technology and industry detection
            try:
                page_text = soup.get_text(separator=' ', strip=True)
                technologies = self.detect_technologies(page_text)
                industries = self.detect_industries(page_text)
            except Exception as e:
                logger.error(f"❌ Error detecting technologies/industries from {url}: {str(e)}")
                technologies = []
                industries = []

            # Add to knowledge base
            self.knowledge_base["case_studies"].extend(case_studies)
            self.knowledge_base["services"].extend(services)

            # Add unique technologies and industries
            for tech in technologies:
                if tech not in self.knowledge_base["technologies"]:
                    self.knowledge_base["technologies"].append(tech)

            for industry in industries:
                if industry not in self.knowledge_base["industries"]:
                    self.knowledge_base["industries"].append(industry)

            logger.info(f"   📊 Page summary: {len(case_studies)} case studies, {len(services)} services, "
                       f"{len(technologies)} technologies, {len(industries)} industries")

            # Find and queue internal links (if not at max depth)
            if depth < self.max_depth and len(self.visited_urls) < self.max_pages:
                try:
                    self.discover_links(soup, url, depth)
                except Exception as e:
                    logger.error(f"❌ Error discovering links from {url}: {str(e)}")

        except Exception as e:
            logger.error(f"❌ Unexpected error scraping {url}: {type(e).__name__} - {str(e)}")

        finally:
            # Be respectful - delay between requests
            time.sleep(1)

    def is_valid_url(self, url: str) -> bool:
        """Validate URL before adding to queue"""
        try:
            parsed = urlparse(url)

            # Check if URL has valid scheme and netloc
            if not parsed.scheme or not parsed.netloc:
                return False

            # Check if URL is too long (>2000 chars is suspicious)
            if len(url) > 2000:
                logger.warning(f"⚠️  Skipping excessively long URL: {url[:100]}...")
                return False

            # Check for valid file extensions (skip media files, docs, etc.)
            invalid_extensions = ['.pdf', '.jpg', '.jpeg', '.png', '.gif', '.zip', '.exe', '.dmg',
                                  '.mp4', '.mp3', '.avi', '.mov', '.doc', '.docx', '.xls', '.xlsx']
            if any(url.lower().endswith(ext) for ext in invalid_extensions):
                return False

            return True

        except Exception as e:
            logger.warning(f"⚠️  Invalid URL format: {url}: {str(e)}")
            return False

    def discover_links(self, soup: BeautifulSoup, current_url: str, current_depth: int):
        """Discover and prioritize internal links with validation"""
        logger.info("Discovering internal links...")

        links = soup.find_all('a', href=True)
        link_scores = []

        for link in links:
            try:
                href = link['href']

                # Skip empty hrefs and javascript/mailto links
                if not href or href.startswith(('javascript:', 'mailto:', 'tel:', '#')):
                    continue

                full_url = urljoin(current_url, href)

                # Validate URL before processing
                if not self.is_valid_url(full_url):
                    continue

                # Only follow internal links
                if urlparse(full_url).netloc == urlparse(self.base_url).netloc:
                    if full_url not in self.visited_urls:
                        # Remove fragment but preserve query params for insights pages
                        clean_url = full_url.split('#')[0]
                        
                        # For non-insights pages, remove query params for deduplication
                        if '/insights' not in clean_url.lower():
                            clean_url = clean_url.split('?')[0]

                        if clean_url not in self.visited_urls:
                            score = self.prioritize_url(clean_url)
                            link_scores.append((score, clean_url, current_depth + 1))

            except Exception as e:
                logger.warning(f"⚠️  Error processing link: {str(e)}")
                continue

        # Sort by priority and add to queue
        link_scores.sort(reverse=True, key=lambda x: x[0])

        added = 0
        for score, url, depth in link_scores[:10]:  # Limit to top 10 per page
            if score > 0:  # Only add positively scored URLs
                self.url_queue.append((url, depth))
                added += 1
                logger.info(f"  Queued (priority {score}): {url}")

        logger.info(f"Added {added} URLs to queue")

    def scrape(self):
        """Main scraping function with smart crawling"""
        logger.info("\n" + "=" * 70)
        logger.info(f"🚀 Starting intelligent scrape of {self.base_url}")
        logger.info("=" * 70)

        # Check robots.txt
        self.check_robots_txt()

        # Process queue with BFS approach
        while self.url_queue and len(self.visited_urls) < self.max_pages:
            url, depth = self.url_queue.popleft()

            if depth <= self.max_depth:
                self.scrape_page(url, depth)

        # Format case studies
        formatted_case_studies = self.format_case_studies()
        self.knowledge_base['case_studies'] = formatted_case_studies

        # Print summary
        logger.info("\n" + "=" * 70)
        logger.info("✅ Scraping complete!")
        logger.info("=" * 70)
        logger.info(f"   Pages visited: {len(self.visited_urls)}")
        logger.info(f"   Case studies found: {len(self.knowledge_base['case_studies'])}")
        logger.info(f"   Services found: {len(self.knowledge_base['services'])}")
        logger.info(f"   Technologies found: {len(self.knowledge_base['technologies'])}")
        logger.info(f"   Industries found: {len(self.knowledge_base['industries'])}")
        logger.info("=" * 70)

        return self.knowledge_base

    def save_to_json(self, filename='knowledge_base_auto.json'):
        """Save scraped data to JSON file"""
        logger.info(f"Saving data to {filename}...")

        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(self.knowledge_base, f, indent=2, ensure_ascii=False)
            logger.info(f"Successfully saved to {filename}")
        except Exception as e:
            logger.error(f"Failed to save: {str(e)}")


def main():
    """Main execution function"""
    scraper = AdvancedShuruTechScraper(
        base_url='https://www.shurutech.com/',
        max_pages=30,
        max_depth=3
    )

    try:
        knowledge_base = scraper.scrape()

        output_file = 'knowledge_base_auto.json'
        scraper.save_to_json(output_file)

        # Detailed final summary with case study preview
        print("\n" + "=" * 70)
        print("📋 FINAL DETAILED SUMMARY")
        print("=" * 70)
        print(f"\n📊 Total pages visited: {len(scraper.visited_urls)}")
        print(f"\n🔍 What was found:")
        print(f"   • Case studies: {len(knowledge_base['case_studies'])}")
        print(f"   • Services: {len(knowledge_base['services'])}")
        print(f"   • Technologies: {len(knowledge_base['technologies'])}")
        print(f"   • Industries: {len(knowledge_base['industries'])}")

        # Sample case study preview (show first case study if available)
        if knowledge_base['case_studies']:
            first_case_study = knowledge_base['case_studies'][0]
            print(f"\n📄 Sample Case Study Preview:")
            print(f"   Client: {first_case_study.get('client_name', 'N/A')}")
            print(f"   Industry: {first_case_study.get('industry', 'N/A')}")
            print(f"   Challenge: {first_case_study.get('challenge', 'N/A')[:100]}...")
            print(f"   Technologies: {', '.join(first_case_study.get('technologies_used', [])[:5])}")

        print(f"\n💾 Output saved to: {output_file}")
        print("=" * 70)

    except KeyboardInterrupt:
        logger.warning("\nScraping interrupted by user")
        logger.info("Saving partial data...")
        scraper.save_to_json('knowledge_base_auto.json')
    except Exception as e:
        logger.error(f"An error occurred: {str(e)}")
        logger.info("Saving partial data...")
        scraper.save_to_json('knowledge_base_auto.json')


if __name__ == "__main__":
    main()
