"""
Scraper Validation Script
Tests and validates the web scraper and its output
- Runs the scraper
- Validates JSON structure
- Checks required fields
- Generates validation report
"""

import json
import subprocess
import sys
import logging
from pathlib import Path
from typing import Dict, List, Tuple, Any

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)


class ScraperValidator:
    """Validate scraper output and data quality"""

    # Required fields for case studies
    CASE_STUDY_REQUIRED_FIELDS = [
        'client_name',
        'industry',
        'challenge',
        'solution',
        'technologies_used',
        'business_impact'
    ]

    # Optional but recommended fields
    CASE_STUDY_OPTIONAL_FIELDS = [
        'project_duration',
        'source_url',
        'metadata'
    ]

    # Required top-level keys
    REQUIRED_KEYS = [
        'case_studies',
        'services',
        'technologies',
        'industries'
    ]

    def __init__(self, output_file='knowledge_base_auto.json', run_scraper=True):
        self.output_file = output_file
        self.run_scraper = run_scraper
        self.data = None
        self.errors = []
        self.warnings = []
        self.validation_results = {
            'json_valid': False,
            'structure_valid': False,
            'case_studies_valid': False,
            'technologies_valid': False,
            'industries_valid': False
        }

    def run_web_scraper(self) -> bool:
        """Execute the web scraper"""
        if not self.run_scraper:
            logger.info("⏭️  Skipping scraper execution (using existing file)")
            return True

        logger.info("\n" + "=" * 70)
        logger.info("🚀 Running Web Scraper")
        logger.info("=" * 70)

        try:
            # Check if scraper file exists
            scraper_path = Path('scrape_website.py')
            if not scraper_path.exists():
                self.errors.append("Scraper file 'scrape_website.py' not found")
                logger.error("❌ Scraper file not found")
                return False

            # Run the scraper
            logger.info("Executing scrape_website.py...")
            result = subprocess.run(
                [sys.executable, 'scrape_website.py'],
                capture_output=True,
                text=True,
                timeout=600  # 10 minute timeout
            )

            # Check if scraper ran successfully
            if result.returncode != 0:
                self.errors.append(f"Scraper failed with exit code {result.returncode}")
                logger.error(f"❌ Scraper failed with exit code {result.returncode}")
                if result.stderr:
                    logger.error(f"Error output: {result.stderr[:500]}")
                return False

            logger.info("✓ Scraper completed successfully")
            return True

        except subprocess.TimeoutExpired:
            self.errors.append("Scraper timed out (exceeded 10 minutes)")
            logger.error("❌ Scraper timed out")
            return False

        except Exception as e:
            self.errors.append(f"Error running scraper: {str(e)}")
            logger.error(f"❌ Error running scraper: {str(e)}")
            return False

    def load_output_file(self) -> bool:
        """Load and parse the output JSON file"""
        logger.info("\n📂 Loading output file...")

        try:
            file_path = Path(self.output_file)

            # Check if file exists
            if not file_path.exists():
                self.errors.append(f"Output file '{self.output_file}' not found")
                logger.error(f"❌ File not found: {self.output_file}")
                return False

            # Check if file is empty
            if file_path.stat().st_size == 0:
                self.errors.append(f"Output file '{self.output_file}' is empty")
                logger.error(f"❌ File is empty: {self.output_file}")
                return False

            # Load JSON
            with open(self.output_file, 'r', encoding='utf-8') as f:
                self.data = json.load(f)

            logger.info(f"✓ Successfully loaded {self.output_file}")
            self.validation_results['json_valid'] = True
            return True

        except json.JSONDecodeError as e:
            self.errors.append(f"Invalid JSON: {str(e)}")
            logger.error(f"❌ Invalid JSON: {str(e)}")
            return False

        except Exception as e:
            self.errors.append(f"Error loading file: {str(e)}")
            logger.error(f"❌ Error loading file: {str(e)}")
            return False

    def validate_structure(self) -> bool:
        """Validate top-level JSON structure"""
        logger.info("\n🔍 Validating JSON structure...")

        if not self.data:
            self.errors.append("No data to validate")
            return False

        valid = True

        # Check for required keys
        for key in self.REQUIRED_KEYS:
            if key not in self.data:
                self.errors.append(f"Missing required key: '{key}'")
                logger.error(f"❌ Missing key: '{key}'")
                valid = False
            else:
                # Check if value is a list
                if not isinstance(self.data[key], list):
                    self.errors.append(f"Key '{key}' should be a list, got {type(self.data[key]).__name__}")
                    logger.error(f"❌ '{key}' is not a list")
                    valid = False

        if valid:
            logger.info("✓ JSON structure is valid")
            self.validation_results['structure_valid'] = True

        return valid

    def validate_case_studies(self) -> Tuple[bool, int]:
        """Validate case studies have required fields"""
        logger.info("\n📚 Validating case studies...")

        if not self.data or 'case_studies' not in self.data:
            self.errors.append("No case studies to validate")
            return False, 0

        case_studies = self.data['case_studies']
        case_study_count = len(case_studies)

        if case_study_count == 0:
            self.warnings.append("No case studies found (this might be expected for some websites)")
            logger.warning("⚠️  No case studies found")
            self.validation_results['case_studies_valid'] = True  # Not an error, just a warning
            return True, 0

        valid = True
        issues_found = 0

        for i, case_study in enumerate(case_studies, 1):
            # Check required fields
            missing_fields = []
            for field in self.CASE_STUDY_REQUIRED_FIELDS:
                if field not in case_study:
                    missing_fields.append(field)

            if missing_fields:
                issues_found += 1
                self.warnings.append(
                    f"Case study #{i} missing fields: {', '.join(missing_fields)}"
                )
                logger.warning(f"⚠️  Case study #{i} missing: {', '.join(missing_fields)}")

            # Validate field content
            if 'client_name' in case_study:
                if not case_study['client_name'] or len(case_study['client_name']) < 2:
                    self.warnings.append(f"Case study #{i} has invalid client_name")
                    issues_found += 1

            if 'technologies_used' in case_study:
                if not isinstance(case_study['technologies_used'], list):
                    self.errors.append(f"Case study #{i}: 'technologies_used' should be a list")
                    valid = False
                elif len(case_study['technologies_used']) == 0:
                    self.warnings.append(f"Case study #{i} has no technologies listed")
                    issues_found += 1

            # Check for recommended fields
            missing_optional = []
            for field in self.CASE_STUDY_OPTIONAL_FIELDS:
                if field not in case_study:
                    missing_optional.append(field)

            if missing_optional and i <= 3:  # Only warn for first 3
                logger.debug(f"Case study #{i} missing optional fields: {', '.join(missing_optional)}")

        if issues_found > 0:
            logger.warning(f"⚠️  Found {issues_found} case study issues (see warnings)")
        else:
            logger.info(f"✓ All {case_study_count} case studies are valid")

        self.validation_results['case_studies_valid'] = valid
        return valid, case_study_count

    def validate_services(self) -> Tuple[bool, int]:
        """Validate services structure"""
        logger.info("\n🔧 Validating services...")

        if not self.data or 'services' not in self.data:
            self.errors.append("No services to validate")
            return False, 0

        services = self.data['services']
        service_count = len(services)

        if service_count == 0:
            self.warnings.append("No services found (this might be expected)")
            logger.warning("⚠️  No services found")
            return True, 0

        valid = True
        required_service_fields = ['name', 'description']

        for i, service in enumerate(services, 1):
            missing_fields = []
            for field in required_service_fields:
                if field not in service:
                    missing_fields.append(field)

            if missing_fields:
                self.warnings.append(
                    f"Service #{i} missing fields: {', '.join(missing_fields)}"
                )
                logger.warning(f"⚠️  Service #{i} missing: {', '.join(missing_fields)}")

        logger.info(f"✓ Validated {service_count} services")
        return valid, service_count

    def validate_technologies(self) -> Tuple[bool, int]:
        """Validate technologies list"""
        logger.info("\n💻 Validating technologies...")

        if not self.data or 'technologies' not in self.data:
            self.errors.append("No technologies to validate")
            return False, 0

        technologies = self.data['technologies']
        tech_count = len(technologies)

        if tech_count == 0:
            self.warnings.append("No technologies found - scraper may have failed to detect any")
            logger.warning("⚠️  No technologies found")
            self.validation_results['technologies_valid'] = False
            return False, 0

        # Check if all technologies are strings
        valid = True
        for i, tech in enumerate(technologies):
            if not isinstance(tech, str):
                self.errors.append(f"Technology #{i+1} is not a string: {type(tech).__name__}")
                valid = False
            elif len(tech.strip()) == 0:
                self.warnings.append(f"Technology #{i+1} is empty")

        if valid:
            logger.info(f"✓ Found {tech_count} technologies")
            self.validation_results['technologies_valid'] = True

        return valid, tech_count

    def validate_industries(self) -> Tuple[bool, int]:
        """Validate industries list"""
        logger.info("\n🏭 Validating industries...")

        if not self.data or 'industries' not in self.data:
            self.errors.append("No industries to validate")
            return False, 0

        industries = self.data['industries']
        industry_count = len(industries)

        if industry_count == 0:
            self.warnings.append("No industries found - scraper may have failed to detect any")
            logger.warning("⚠️  No industries found")
            self.validation_results['industries_valid'] = False
            return False, 0

        # Check if all industries are strings
        valid = True
        for i, industry in enumerate(industries):
            if not isinstance(industry, str):
                self.errors.append(f"Industry #{i+1} is not a string: {type(industry).__name__}")
                valid = False
            elif len(industry.strip()) == 0:
                self.warnings.append(f"Industry #{i+1} is empty")

        if valid:
            logger.info(f"✓ Found {industry_count} industries")
            self.validation_results['industries_valid'] = True

        return valid, industry_count

    def run_validation(self) -> bool:
        """Execute complete validation suite"""
        logger.info("\n" + "=" * 70)
        logger.info("🔍 Starting Validation Suite")
        logger.info("=" * 70)

        # Step 1: Run scraper (if requested)
        if self.run_scraper:
            if not self.run_web_scraper():
                return False

        # Step 2: Load output file
        if not self.load_output_file():
            return False

        # Step 3: Validate structure
        if not self.validate_structure():
            return False

        # Step 4: Validate individual components
        case_studies_valid, case_study_count = self.validate_case_studies()
        services_valid, service_count = self.validate_services()
        technologies_valid, tech_count = self.validate_technologies()
        industries_valid, industry_count = self.validate_industries()

        # Overall validation result
        all_valid = (
            self.validation_results['json_valid'] and
            self.validation_results['structure_valid'] and
            case_studies_valid and
            technologies_valid and
            industries_valid
        )

        return all_valid

    def print_report(self):
        """Print comprehensive validation report"""
        print("\n" + "=" * 70)
        print("📊 VALIDATION REPORT")
        print("=" * 70)

        # JSON validation
        if self.validation_results['json_valid']:
            print("\n✓ JSON structure valid")
        else:
            print("\n❌ JSON structure invalid")

        # Structure validation
        if self.validation_results['structure_valid']:
            print("✓ All required keys present")
        else:
            print("❌ Missing required keys")

        # Statistics
        if self.data:
            case_study_count = len(self.data.get('case_studies', []))
            service_count = len(self.data.get('services', []))
            tech_count = len(self.data.get('technologies', []))
            industry_count = len(self.data.get('industries', []))

            print(f"\n📚 Data Summary:")
            print(f"   ✓ {case_study_count} case studies extracted")
            print(f"   ✓ {service_count} services found")
            print(f"   ✓ {tech_count} technologies found")
            print(f"   ✓ {industry_count} industries identified")

        # Warnings
        if self.warnings:
            print(f"\n⚠️  Warnings ({len(self.warnings)}):")
            for warning in self.warnings[:10]:  # Show first 10
                print(f"   • {warning}")
            if len(self.warnings) > 10:
                print(f"   ... and {len(self.warnings) - 10} more warnings")

        # Errors
        if self.errors:
            print(f"\n❌ Errors ({len(self.errors)}):")
            for error in self.errors:
                print(f"   • {error}")

        # Overall result
        print("\n" + "=" * 70)
        if not self.errors and len(self.warnings) <= 5:
            print("✅ VALIDATION PASSED - All checks successful!")
        elif not self.errors:
            print("⚠️  VALIDATION PASSED WITH WARNINGS")
        else:
            print("❌ VALIDATION FAILED - Please fix errors above")
        print("=" * 70)


def main():
    """Main execution function"""
    import argparse

    parser = argparse.ArgumentParser(
        description='Validate web scraper output',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument(
        '--no-run',
        action='store_true',
        help='Skip running the scraper, only validate existing file'
    )
    parser.add_argument(
        '--file',
        default='knowledge_base_auto.json',
        help='Output file to validate (default: knowledge_base_auto.json)'
    )

    args = parser.parse_args()

    # Create validator
    validator = ScraperValidator(
        output_file=args.file,
        run_scraper=not args.no_run
    )

    try:
        # Run validation
        success = validator.run_validation()

        # Print report
        validator.print_report()

        # Return exit code
        return 0 if success and not validator.errors else 1

    except KeyboardInterrupt:
        logger.warning("\n⚠️  Validation interrupted by user")
        return 1

    except Exception as e:
        logger.error(f"❌ Unexpected error: {str(e)}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
