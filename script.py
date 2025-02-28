"""
Scrapes multiple headlines from The Daily Pennsylvanian website and saves them to a 
JSON file that tracks headlines over time.
"""

import os
import sys

import daily_event_monitor

import bs4
import requests
import loguru


def scrape_data_point(num_headlines=3):
    """
    Scrapes multiple headlines from The Daily Pennsylvanian home page.

    Args:
        num_headlines (int): Number of headlines to scrape. Defaults to 3.

    Returns:
        list: A list of headline texts. Empty list if none are found.
    """
    headers = {
        "User-Agent": "cis3500-scraper"
    }
    req = requests.get("https://www.thedp.com", headers=headers)
    loguru.logger.info(f"Request URL: {req.url}")
    loguru.logger.info(f"Request status code: {req.status_code}")

    if req.ok:
        soup = bs4.BeautifulSoup(req.text, "html.parser")
        target_elements = soup.find_all("a", class_="frontpage-link", limit=num_headlines)
        
        headlines = []
        for element in target_elements:
            if element is not None:
                headlines.append(element.text.strip())
        
        loguru.logger.info(f"Found {len(headlines)} headlines")
        for i, headline in enumerate(headlines):
            loguru.logger.info(f"Headline {i+1}: {headline}")
        
        return headlines
    
    return []


if __name__ == "__main__":
    # Number of headlines to scrape
    NUM_HEADLINES = 3

    # Setup logger to track runtime
    loguru.logger.add("scrape.log", rotation="1 day")

    # Create data dir if needed
    loguru.logger.info("Creating data directory if it does not exist")
    try:
        os.makedirs("data", exist_ok=True)
    except Exception as e:
        loguru.logger.error(f"Failed to create data directory: {e}")
        sys.exit(1)

    # Load daily event monitor
    loguru.logger.info("Loading daily event monitor")
    dem = daily_event_monitor.DailyEventMonitor(
        "data/daily_pennsylvanian_headlines.json"
    )

    # Run scrape
    loguru.logger.info(f"Starting scrape for {NUM_HEADLINES} headlines")
    try:
        headlines = scrape_data_point(NUM_HEADLINES)
        data_point = headlines  # Store all headlines as the data point
    except Exception as e:
        loguru.logger.error(f"Failed to scrape data points: {e}")
        data_point = None

    # Save data
    if data_point is not None and len(data_point) > 0:
        dem.add_today(data_point)
        dem.save()
        loguru.logger.info("Saved daily event monitor")
    else:
        loguru.logger.warning("No headlines found to save")

    def print_tree(directory, ignore_dirs=[".git", "__pycache__"]):
        loguru.logger.info(f"Printing tree of files/dirs at {directory}")
        for root, dirs, files in os.walk(directory):
            dirs[:] = [d for d in dirs if d not in ignore_dirs]
            level = root.replace(directory, "").count(os.sep)
            indent = " " * 4 * (level)
            loguru.logger.info(f"{indent}+--{os.path.basename(root)}/")
            sub_indent = " " * 4 * (level + 1)
            for file in files:
                loguru.logger.info(f"{sub_indent}+--{file}")

    print_tree(os.getcwd())

    loguru.logger.info("Printing contents of data file {}".format(dem.file_path))
    with open(dem.file_path, "r") as f:
        loguru.logger.info(f.read())

    # Finish
    loguru.logger.info("Scrape complete")
    loguru.logger.info("Exiting")