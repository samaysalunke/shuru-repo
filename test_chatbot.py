"""
Test script for Shuru Tech AI Solutions Finder
Validates core functionality, vector search, and system readiness
"""

import os
import json
import time
from datetime import datetime
from dotenv import load_dotenv
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.schema import Document

# Suppress tokenizer warnings
os.environ["TOKENIZERS_PARALLELISM"] = "false"

# Load environment variables
load_dotenv()


class ChatbotTester:
    """Comprehensive testing for the RAG chatbot"""

    def __init__(self):
        self.knowledge_base_path = 'knowledge_base.json'
        self.documents = []
        self.vectorstore = None
        self.test_results = []
        self.performance_metrics = {}

    def print_header(self, text):
        """Print a formatted section header"""
        print(f"\n{'=' * 70}")
        print(f"  {text}")
        print(f"{'=' * 70}\n")

    def print_test(self, test_name, passed, details=""):
        """Print test result with status"""
        status = "[PASS]" if passed else "[FAIL]"
        color = "\033[92m" if passed else "\033[91m"
        reset = "\033[0m"
        print(f"{color}{status}{reset} Test {test_name}: {details}")
        self.test_results.append({"name": test_name, "passed": passed, "details": details})

    def test_1_load_knowledge_base(self):
        """Test 1: Load and validate knowledge base"""
        self.print_header("TEST 1: Knowledge Base Loading")

        start_time = time.time()

        try:
            # Check file exists
            if not os.path.exists(self.knowledge_base_path):
                self.print_test("1", False, "knowledge_base.json not found")
                return False

            # Load JSON
            with open(self.knowledge_base_path, 'r', encoding='utf-8') as f:
                data = json.load(f)

            # Validate structure
            if 'case_studies' not in data:
                self.print_test("1", False, "No 'case_studies' key in JSON")
                return False

            case_studies = data.get('case_studies', [])
            if not case_studies:
                self.print_test("1", False, "case_studies array is empty")
                return False

            # Process documents
            for case_study in case_studies:
                page_content = f"""Case Study: {case_study.get('client_name', 'Unknown Client')}
Industry: {case_study.get('industry', 'N/A')}

Problem:
{case_study.get('problem', 'N/A')}

Solution:
{case_study.get('solution', 'N/A')}

Technologies Used: {', '.join(case_study.get('technologies', []))}

Results:
{case_study.get('results', 'N/A')}

Duration: {case_study.get('duration', 'N/A')}"""

                doc = Document(
                    page_content=page_content,
                    metadata={
                        "source": "case_study",
                        "type": "case_study",
                        "client_name": case_study.get('client_name', 'Unknown'),
                        "industry": case_study.get('industry', 'N/A'),
                        "technologies": ', '.join(case_study.get('technologies', []))
                    }
                )
                self.documents.append(doc)

            load_time = time.time() - start_time
            self.performance_metrics['load_time'] = load_time

            self.print_test(
                "1",
                True,
                f"Knowledge base loaded ({len(case_studies)} case studies) in {load_time:.2f}s"
            )
            print(f"   >> Case studies found: {len(case_studies)}")

            # Show case study names
            print("   >> Case studies:")
            for cs in case_studies:
                client = cs.get('client_name', 'Unknown')
                industry = cs.get('industry', 'N/A')
                print(f"      - {client} ({industry})")

            return True

        except json.JSONDecodeError as e:
            self.print_test("1", False, f"Invalid JSON: {str(e)}")
            return False
        except Exception as e:
            self.print_test("1", False, f"Error: {str(e)}")
            return False

    def test_2_create_embeddings(self):
        """Test 2: Create embeddings model"""
        self.print_header("TEST 2: Embeddings Model")

        start_time = time.time()

        try:
            print("   >> Initializing HuggingFace embeddings...")
            embeddings = HuggingFaceEmbeddings(
                model_name="sentence-transformers/all-MiniLM-L6-v2"
            )

            # Test embedding
            test_text = "This is a test sentence."
            test_embedding = embeddings.embed_query(test_text)

            embed_time = time.time() - start_time
            self.performance_metrics['embed_time'] = embed_time

            if len(test_embedding) > 0:
                self.print_test(
                    "2",
                    True,
                    f"Embeddings created (dimension: {len(test_embedding)}) in {embed_time:.2f}s"
                )
                return embeddings
            else:
                self.print_test("2", False, "Embedding dimension is 0")
                return None

        except Exception as e:
            self.print_test("2", False, f"Error: {str(e)}")
            return None

    def test_3_build_vector_store(self, embeddings):
        """Test 3: Build FAISS vector store"""
        self.print_header("TEST 3: Vector Store Creation")

        if not self.documents:
            self.print_test("3", False, "No documents to process")
            return False

        start_time = time.time()

        try:
            # Split documents
            print("   >> Splitting documents into chunks...")
            text_splitter = RecursiveCharacterTextSplitter(
                chunk_size=1000,
                chunk_overlap=200,
                length_function=len
            )
            splits = text_splitter.split_documents(self.documents)
            print(f"      Created {len(splits)} chunks from {len(self.documents)} documents")

            # Create vector store
            print("   >> Building FAISS vector store...")
            self.vectorstore = FAISS.from_documents(
                documents=splits,
                embedding=embeddings
            )

            vector_time = time.time() - start_time
            self.performance_metrics['vector_time'] = vector_time

            self.print_test(
                "3",
                True,
                f"Vector store built ({len(splits)} chunks) in {vector_time:.2f}s"
            )
            return True

        except Exception as e:
            self.print_test("3", False, f"Error: {str(e)}")
            return False

    def test_4_similarity_search(self):
        """Test 4: Similarity search with sample queries"""
        self.print_header("TEST 4: Similarity Search")

        if not self.vectorstore:
            self.print_test("4", False, "Vector store not initialized")
            return False

        # Sample test queries
        test_queries = [
            {
                "query": "cart abandonment e-commerce",
                "expected_industries": ["E-commerce", "Retail", "Online Shopping"],
                "keywords": ["cart", "shopping", "conversion", "checkout"]
            },
            {
                "query": "slow payment processing fintech",
                "expected_industries": ["FinTech", "Finance", "Banking", "Payment"],
                "keywords": ["payment", "transaction", "processing", "speed"]
            },
            {
                "query": "patient data healthcare consolidation",
                "expected_industries": ["Healthcare", "Medical", "Hospital"],
                "keywords": ["patient", "medical", "data", "health", "consolidat"]
            },
            {
                "query": "iot agriculture monitoring",
                "expected_industries": ["Agriculture", "Farming", "AgriTech"],
                "keywords": ["iot", "sensor", "monitor", "farm", "crop"]
            },
            {
                "query": "real-time analytics dashboard",
                "expected_industries": ["Analytics", "Data", "Business Intelligence"],
                "keywords": ["analytics", "dashboard", "real-time", "data", "visual"]
            }
        ]

        query_times = []
        passed_tests = 0

        for idx, test_case in enumerate(test_queries, 1):
            query = test_case["query"]
            print(f"\n   Query {idx}: \"{query}\"")

            start_time = time.time()

            try:
                # Perform similarity search
                results = self.vectorstore.similarity_search(query, k=3)
                query_time = time.time() - start_time
                query_times.append(query_time)

                if not results:
                    print(f"      [X] No results returned")
                    continue

                # Check first result
                top_result = results[0]
                metadata = top_result.metadata
                content = top_result.page_content.lower()

                client_name = metadata.get('client_name', 'Unknown')
                industry = metadata.get('industry', 'N/A')

                # Validate relevance
                is_relevant = False

                # Check industry match
                for expected_industry in test_case["expected_industries"]:
                    if expected_industry.lower() in industry.lower():
                        is_relevant = True
                        break

                # Check keyword match in content
                if not is_relevant:
                    keyword_matches = sum(1 for kw in test_case["keywords"] if kw.lower() in content)
                    if keyword_matches >= 2:
                        is_relevant = True

                if is_relevant:
                    print(f"      [OK] {client_name} ({industry}) - {query_time:.3f}s")
                    passed_tests += 1
                else:
                    print(f"      [?] {client_name} ({industry}) - relevance unclear")

            except Exception as e:
                print(f"      [X] Error: {str(e)}")

        # Calculate average query time
        avg_query_time = sum(query_times) / len(query_times) if query_times else 0
        self.performance_metrics['avg_query_time'] = avg_query_time

        success_rate = (passed_tests / len(test_queries)) * 100
        self.print_test(
            "4",
            passed_tests >= len(test_queries) * 0.6,  # At least 60% should pass
            f"Similarity search ({passed_tests}/{len(test_queries)} relevant, avg {avg_query_time:.3f}s/query)"
        )

        return passed_tests >= len(test_queries) * 0.6

    def test_5_api_key_check(self):
        """Test 5: Check API key configuration"""
        self.print_header("TEST 5: API Key Configuration")

        api_key = os.getenv('ANTHROPIC_API_KEY')

        if api_key:
            # Mask the key for security
            masked_key = api_key[:8] + "*" * (len(api_key) - 12) + api_key[-4:] if len(api_key) > 12 else "***"
            self.print_test("5", True, f"API key found ({masked_key})")
            return True
        else:
            self.print_test("5", False, "ANTHROPIC_API_KEY not set in .env")
            return False

    def print_performance_summary(self):
        """Print performance metrics summary"""
        self.print_header("PERFORMANCE METRICS")

        print(f"   >> Knowledge base load time: {self.performance_metrics.get('load_time', 0):.2f}s")
        print(f"   >> Embeddings creation time: {self.performance_metrics.get('embed_time', 0):.2f}s")
        print(f"   >> Vector store build time: {self.performance_metrics.get('vector_time', 0):.2f}s")
        print(f"   >> Average query time: {self.performance_metrics.get('avg_query_time', 0):.3f}s")

        total_time = sum([
            self.performance_metrics.get('load_time', 0),
            self.performance_metrics.get('embed_time', 0),
            self.performance_metrics.get('vector_time', 0)
        ])
        print(f"\n   >> Total initialization time: {total_time:.2f}s")

    def print_final_summary(self):
        """Print final test summary"""
        self.print_header("TEST SUMMARY")

        passed = sum(1 for result in self.test_results if result["passed"])
        total = len(self.test_results)
        success_rate = (passed / total * 100) if total > 0 else 0

        print(f"   Tests Passed: {passed}/{total} ({success_rate:.1f}%)")
        print()

        # List all tests
        for result in self.test_results:
            status = "[OK]" if result["passed"] else "[FAIL]"
            print(f"   {status} {result['name']}: {result['details']}")

        print()

        if passed == total:
            print("   " + "=" * 66)
            print("   " + " " * 15 + "ALL SYSTEMS OPERATIONAL!")
            print("   " + " " * 18 + "Ready for demo.")
            print("   " + "=" * 66)
            return True
        else:
            print("   " + "=" * 66)
            print("   " + " " * 12 + "SOME TESTS FAILED")
            print("   " + " " * 10 + "Please fix issues before demo")
            print("   " + "=" * 66)
            return False

    def run_all_tests(self):
        """Run complete test suite"""
        print("\n")
        print("=" * 70)
        print(" " * 10 + "SHURU TECH AI SOLUTIONS FINDER - TEST SUITE")
        print(" " * 20 + f"Run at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("=" * 70)

        # Run tests
        kb_loaded = self.test_1_load_knowledge_base()

        if not kb_loaded:
            print("\n[X] Critical failure: Cannot proceed without knowledge base")
            self.print_final_summary()
            return False

        embeddings = self.test_2_create_embeddings()

        if not embeddings:
            print("\n[X] Critical failure: Cannot proceed without embeddings")
            self.print_final_summary()
            return False

        vector_built = self.test_3_build_vector_store(embeddings)

        if not vector_built:
            print("\n[X] Critical failure: Cannot proceed without vector store")
            self.print_final_summary()
            return False

        self.test_4_similarity_search()
        self.test_5_api_key_check()

        # Print summaries
        self.print_performance_summary()
        success = self.print_final_summary()

        return success


def main():
    """Main test execution"""
    tester = ChatbotTester()
    success = tester.run_all_tests()

    # Exit with appropriate code
    exit(0 if success else 1)


if __name__ == "__main__":
    main()
