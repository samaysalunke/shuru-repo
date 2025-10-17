"""
Merge scraped case studies into knowledge_base.json
"""

import json
from pathlib import Path

def load_json(filepath):
    """Load JSON file"""
    with open(filepath, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_json(data, filepath):
    """Save JSON file"""
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def merge_case_studies():
    """Merge scraped case studies into knowledge base"""
    
    print("=" * 70)
    print("MERGING CASE STUDIES")
    print("=" * 70)
    
    # Load files
    kb_path = Path('knowledge_base.json')
    scraped_path = Path('case_studies_scraped.json')
    
    if not kb_path.exists():
        print("❌ knowledge_base.json not found")
        return
    
    if not scraped_path.exists():
        print("❌ case_studies_scraped.json not found")
        return
    
    knowledge_base = load_json(kb_path)
    scraped_cases = load_json(scraped_path)
    
    print(f"\n✓ Loaded existing knowledge base with {len(knowledge_base['case_studies'])} case studies")
    print(f"✓ Loaded {len(scraped_cases)} new case studies from scraper")
    
    # Check for duplicates by URL
    existing_urls = {cs.get('url', '') for cs in knowledge_base['case_studies']}
    
    added = 0
    skipped = 0
    
    for case_study in scraped_cases:
        url = case_study.get('url', '')
        client = case_study.get('client_name', 'Unknown')
        
        if url in existing_urls:
            print(f"\n⚠️  Skipping duplicate: {client}")
            print(f"   URL already exists: {url}")
            skipped += 1
        else:
            knowledge_base['case_studies'].append(case_study)
            print(f"\n✓ Added: {client}")
            print(f"   URL: {url}")
            added += 1
            existing_urls.add(url)
    
    if added > 0:
        # Create backup
        backup_path = Path('knowledge_base_backup.json')
        save_json(knowledge_base, backup_path)
        print(f"\n✓ Created backup: {backup_path}")
        
        # Save updated knowledge base
        save_json(knowledge_base, kb_path)
        print(f"✓ Updated knowledge_base.json")
    
    print("\n" + "=" * 70)
    print("MERGE SUMMARY")
    print("=" * 70)
    print(f"Total case studies in knowledge base: {len(knowledge_base['case_studies'])}")
    print(f"Added: {added}")
    print(f"Skipped (duplicates): {skipped}")
    print("=" * 70)

if __name__ == "__main__":
    merge_case_studies()

