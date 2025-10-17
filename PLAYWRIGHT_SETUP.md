# Playwright Scraper Setup Guide

## Overview

This document explains how to use the Playwright scraper to extract case studies from JavaScript-rendered pages on the Shuru Tech website.

## Installation

### 1. Install Playwright

```bash
pip install 'playwright>=1.48.0'
```

### 2. Install Browser

```bash
playwright install chromium
```

## Usage

### Quick Start

1. **Add URLs to scrape** - Edit `case_study_urls.txt`:
```
https://shurutech.com/insights/case-study/your-case-study-url
```

2. **Run the scraper**:
```bash
python scrape_with_playwright.py
```

3. **Merge with knowledge base**:
```bash
python merge_case_studies.py
```

### Manual Steps

#### Step 1: Configure URLs

Edit `case_study_urls.txt` to add case study URLs (one per line):

```txt
# Comment lines start with #
https://shurutech.com/insights/case-study/case-study-1
https://shurutech.com/insights/case-study/case-study-2
```

#### Step 2: Run Scraper

```bash
python scrape_with_playwright.py
```

This will:
- Launch Chromium browser (headless mode)
- Navigate to each URL
- Wait for JavaScript to render
- Extract case study content
- Save to `case_studies_scraped.json`

#### Step 3: Review Scraped Data

Check `case_studies_scraped.json` to verify the extracted data quality.

#### Step 4: Merge with Knowledge Base

```bash
python merge_case_studies.py
```

This will:
- Load existing `knowledge_base.json`
- Check for duplicates (by URL)
- Add new case studies
- Create backup (`knowledge_base_backup.json`)
- Update `knowledge_base.json`

## Configuration

### Scraper Settings

Edit `scrape_with_playwright.py` to customize:

```python
scraper = PlaywrightScraper(
    headless=True,   # Set to False to see browser
    timeout=60000    # Timeout in milliseconds
)
```

### Extracted Fields

The scraper extracts:
- **Client Name** - Company/project name
- **Industry** - Auto-detected from content
- **Problem** - Challenge description
- **Solution** - Implementation approach
- **Technologies** - Tech stack used
- **Results** - Business impact & metrics
- **URL** - Original case study URL

## Troubleshooting

### Page Timeout Errors

If pages timeout, increase the timeout:

```python
scraper = PlaywrightScraper(timeout=120000)  # 2 minutes
```

### Missing Content

If content isn't extracted:
1. Set `headless=False` to see what's happening
2. Check browser console for JavaScript errors
3. Verify the page loads properly in a regular browser

### Browser Not Found

If you get "browser not found" errors:

```bash
playwright install chromium
```

## Maintenance

### Adding New Case Studies

1. Add URLs to `case_study_urls.txt`
2. Run `python scrape_with_playwright.py`
3. Run `python merge_case_studies.py`
4. Restart the Streamlit app to reload knowledge base

### Updating Existing Case Studies

The merge script skips duplicates by URL. To update:
1. Remove the old entry from `knowledge_base.json`
2. Rescrape and merge

## Files

- **`scrape_with_playwright.py`** - Main scraper module
- **`case_study_urls.txt`** - URLs to scrape
- **`merge_case_studies.py`** - Merge script
- **`case_studies_scraped.json`** - Scraper output
- **`knowledge_base.json`** - Main knowledge base
- **`knowledge_base_backup.json`** - Backup before merge

## Performance

- **Speed**: ~10-15 seconds per page
- **Headless vs Headed**: Headless is slightly faster
- **Parallel**: Not currently supported (sequential only)

## Known Limitations

1. **Slow pages**: Some pages take 30+ seconds to load
2. **Dynamic content**: Waits 5 seconds for JS rendering
3. **Technology detection**: May miss some technologies
4. **Industry classification**: Auto-detected, may need manual correction
5. **Sequential processing**: Scrapes one page at a time

## Future Improvements

- [ ] Parallel scraping support
- [ ] Better technology detection
- [ ] Improved section extraction (problem/solution/results)
- [ ] Support for more page layouts
- [ ] Automatic retry on failures
- [ ] Progress bar for large batches

