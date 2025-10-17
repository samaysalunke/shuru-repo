"""
Knowledge Base Merger Script
Intelligently merges manual and auto-scraped knowledge bases
- Combines case studies from both sources
- Deduplicates services by name
- Merges and sorts technologies and industries
"""

import json
import logging
from typing import Dict, List, Any
from pathlib import Path

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)


class KnowledgeBaseMerger:
    """Intelligently merge manual and auto-scraped knowledge bases"""

    def __init__(self,
                 manual_file='knowledge_base.json',
                 auto_file='knowledge_base_auto.json',
                 output_file='knowledge_base_merged.json'):
        self.manual_file = manual_file
        self.auto_file = auto_file
        self.output_file = output_file

        self.manual_data = None
        self.auto_data = None
        self.merged_data = {
            "case_studies": [],
            "services": [],
            "technologies": [],
            "industries": []
        }

    def load_json_file(self, filepath: str) -> Dict[str, Any]:
        """Load JSON file with error handling"""
        try:
            file_path = Path(filepath)

            if not file_path.exists():
                logger.warning(f"⚠️  File not found: {filepath}")
                return None

            if file_path.stat().st_size == 0:
                logger.warning(f"⚠️  File is empty: {filepath}")
                return None

            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)

            logger.info(f"✓ Successfully loaded: {filepath}")
            return data

        except json.JSONDecodeError as e:
            logger.error(f"❌ Invalid JSON in {filepath}: {str(e)}")
            return None

        except Exception as e:
            logger.error(f"❌ Error loading {filepath}: {str(e)}")
            return None

    def validate_structure(self, data: Dict, source_name: str) -> bool:
        """Validate that the data has the expected structure"""
        if not data:
            return False

        required_keys = ['case_studies', 'services', 'technologies', 'industries']

        for key in required_keys:
            if key not in data:
                logger.warning(f"⚠️  Missing key '{key}' in {source_name}, adding empty list")
                data[key] = []

        return True

    def merge_case_studies(self) -> List[Dict]:
        """Combine all case studies from both sources"""
        logger.info("\n📚 Merging case studies...")

        manual_studies = self.manual_data.get('case_studies', []) if self.manual_data else []
        auto_studies = self.auto_data.get('case_studies', []) if self.auto_data else []

        logger.info(f"   Manual case studies: {len(manual_studies)}")
        logger.info(f"   Auto case studies: {len(auto_studies)}")

        # Combine all case studies
        all_studies = []

        # Add manual studies with source tag
        for study in manual_studies:
            study_copy = study.copy()
            if 'metadata' not in study_copy:
                study_copy['metadata'] = {}
            study_copy['metadata']['source'] = 'manual'
            all_studies.append(study_copy)

        # Add auto studies with source tag
        for study in auto_studies:
            study_copy = study.copy()
            if 'metadata' not in study_copy:
                study_copy['metadata'] = {}
            study_copy['metadata']['source'] = 'auto'
            all_studies.append(study_copy)

        logger.info(f"✓ Total case studies after merge: {len(all_studies)}")
        return all_studies

    def merge_services(self) -> List[Dict]:
        """Deduplicate services by name (case-insensitive)"""
        logger.info("\n🔧 Merging services...")

        manual_services = self.manual_data.get('services', []) if self.manual_data else []
        auto_services = self.auto_data.get('services', []) if self.auto_data else []

        logger.info(f"   Manual services: {len(manual_services)}")
        logger.info(f"   Auto services: {len(auto_services)}")

        # Use dict to deduplicate by lowercase name
        services_dict = {}

        # Add manual services first (they take priority)
        for service in manual_services:
            name = service.get('name', '').strip()
            if name:
                name_lower = name.lower()
                if name_lower not in services_dict:
                    service_copy = service.copy()
                    service_copy['source'] = 'manual'
                    services_dict[name_lower] = service_copy
                    logger.debug(f"   Added manual service: {name}")

        # Add auto services (skip if already exists)
        duplicates = 0
        for service in auto_services:
            name = service.get('name', '').strip()
            if name:
                name_lower = name.lower()
                if name_lower not in services_dict:
                    service_copy = service.copy()
                    service_copy['source'] = 'auto'
                    services_dict[name_lower] = service_copy
                    logger.debug(f"   Added auto service: {name}")
                else:
                    duplicates += 1
                    logger.debug(f"   Skipped duplicate: {name}")

        merged_services = list(services_dict.values())

        logger.info(f"✓ Total unique services: {len(merged_services)} (removed {duplicates} duplicates)")
        return merged_services

    def merge_technologies(self) -> List[str]:
        """Combine and deduplicate technologies, return sorted list"""
        logger.info("\n💻 Merging technologies...")

        manual_techs = self.manual_data.get('technologies', []) if self.manual_data else []
        auto_techs = self.auto_data.get('technologies', []) if self.auto_data else []

        logger.info(f"   Manual technologies: {len(manual_techs)}")
        logger.info(f"   Auto technologies: {len(auto_techs)}")

        # Combine and deduplicate (case-sensitive to preserve proper casing)
        all_techs = set()

        for tech in manual_techs:
            if tech and isinstance(tech, str):
                all_techs.add(tech.strip())

        for tech in auto_techs:
            if tech and isinstance(tech, str):
                all_techs.add(tech.strip())

        # Sort alphabetically
        sorted_techs = sorted(list(all_techs))

        duplicates = (len(manual_techs) + len(auto_techs)) - len(sorted_techs)
        logger.info(f"✓ Total unique technologies: {len(sorted_techs)} (removed {duplicates} duplicates)")

        return sorted_techs

    def merge_industries(self) -> List[str]:
        """Combine and deduplicate industries, return sorted list"""
        logger.info("\n🏭 Merging industries...")

        manual_industries = self.manual_data.get('industries', []) if self.manual_data else []
        auto_industries = self.auto_data.get('industries', []) if self.auto_data else []

        logger.info(f"   Manual industries: {len(manual_industries)}")
        logger.info(f"   Auto industries: {len(auto_industries)}")

        # Combine and deduplicate (case-sensitive to preserve proper casing)
        all_industries = set()

        for industry in manual_industries:
            if industry and isinstance(industry, str):
                all_industries.add(industry.strip())

        for industry in auto_industries:
            if industry and isinstance(industry, str):
                all_industries.add(industry.strip())

        # Sort alphabetically
        sorted_industries = sorted(list(all_industries))

        duplicates = (len(manual_industries) + len(auto_industries)) - len(sorted_industries)
        logger.info(f"✓ Total unique industries: {len(sorted_industries)} (removed {duplicates} duplicates)")

        return sorted_industries

    def merge(self) -> bool:
        """Execute the complete merge process"""
        logger.info("\n" + "=" * 70)
        logger.info("🔄 Starting Knowledge Base Merge")
        logger.info("=" * 70)

        # Load both files
        logger.info("\n📂 Loading knowledge bases...")
        self.manual_data = self.load_json_file(self.manual_file)
        self.auto_data = self.load_json_file(self.auto_file)

        # Check if at least one file was loaded successfully
        if not self.manual_data and not self.auto_data:
            logger.error("❌ Both files failed to load or don't exist. Cannot merge.")
            return False

        # Validate structures
        if self.manual_data:
            self.validate_structure(self.manual_data, self.manual_file)

        if self.auto_data:
            self.validate_structure(self.auto_data, self.auto_file)

        # Perform merges
        try:
            self.merged_data['case_studies'] = self.merge_case_studies()
            self.merged_data['services'] = self.merge_services()
            self.merged_data['technologies'] = self.merge_technologies()
            self.merged_data['industries'] = self.merge_industries()

            logger.info("\n✅ Merge completed successfully!")
            return True

        except Exception as e:
            logger.error(f"❌ Error during merge: {str(e)}")
            return False

    def save_merged_data(self) -> bool:
        """Save merged data to output file"""
        try:
            logger.info(f"\n💾 Saving merged data to {self.output_file}...")

            with open(self.output_file, 'w', encoding='utf-8') as f:
                json.dump(self.merged_data, f, indent=2, ensure_ascii=False)

            logger.info(f"✓ Successfully saved to {self.output_file}")
            return True

        except Exception as e:
            logger.error(f"❌ Failed to save merged data: {str(e)}")
            return False

    def print_summary(self):
        """Print comprehensive merge summary"""
        manual_studies = len(self.manual_data.get('case_studies', [])) if self.manual_data else 0
        auto_studies = len(self.auto_data.get('case_studies', [])) if self.auto_data else 0
        total_studies = len(self.merged_data.get('case_studies', []))

        print("\n" + "=" * 70)
        print("📊 MERGE SUMMARY")
        print("=" * 70)
        print(f"\n📚 Case Studies:")
        print(f"   • Manual: {manual_studies} case studies")
        print(f"   • Auto: {auto_studies} case studies")
        print(f"   • Merged: {total_studies} total case studies")

        print(f"\n🔧 Services:")
        print(f"   • Total services: {len(self.merged_data.get('services', []))}")

        print(f"\n💻 Technologies:")
        print(f"   • Total technologies: {len(self.merged_data.get('technologies', []))}")

        print(f"\n🏭 Industries:")
        print(f"   • Total industries: {len(self.merged_data.get('industries', []))}")

        print(f"\n💾 Output:")
        print(f"   • Saved to: {self.output_file}")

        print("=" * 70)


def main():
    """Main execution function"""
    merger = KnowledgeBaseMerger(
        manual_file='knowledge_base.json',
        auto_file='knowledge_base_auto.json',
        output_file='knowledge_base_merged.json'
    )

    try:
        # Execute merge
        success = merger.merge()

        if success:
            # Save merged data
            if merger.save_merged_data():
                # Print summary
                merger.print_summary()
            else:
                logger.error("❌ Failed to save merged data")
                return 1
        else:
            logger.error("❌ Merge failed")
            return 1

        return 0

    except KeyboardInterrupt:
        logger.warning("\n⚠️  Merge interrupted by user")
        return 1

    except Exception as e:
        logger.error(f"❌ Unexpected error: {str(e)}")
        return 1


if __name__ == "__main__":
    exit(main())
