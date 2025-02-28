# Robots Analysis for the Daily Pennsylvanian

The Daily Pennsylvanian's `robots.txt` file is available at
[https://www.thedp.com/robots.txt](https://www.thedp.com/robots.txt).

## Contents of the `robots.txt` file on February 28, 2025

```
User-agent: *
Crawl-delay: 10
Allow: /

User-agent: SemrushBot
Disallow: /
```

## Explanation

This robots.txt indicates:
- All bots except SemrushBot are allowed to crawl the entire website
- A 10-second delay between requests is required
- SemrushBot is completely blocked

For daily headline scraper:
- I have permission to access the front page
- The once-per-day frequency is within the crawl-delay requirement
- This project complies with both ethical and legal guidelines for web scraping
