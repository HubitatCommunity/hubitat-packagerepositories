import json
import requests
import concurrent.futures
from rich.console import Console
from rich.text import Text
from tqdm.contrib.concurrent import thread_map

"""
Author: WalksOnAir
Date: 2025-02-22
Revision: 1.0
Purpose: 
    This script checks the accessibility of each repository URL listed in 
    the 'repositories.json' file. It attempts to fetch each URL and reports 
    whether it is accessible or not.

Dependencies:
    - requests: For making HTTP requests
    - rich: For colorized console output
    - tqdm: For displaying a progress bar

Installation Commands:
    pip install requests rich tqdm

Usage:
    1. Run this script in the same directory as the `repositories.json` file.
    2. The script will:
       - Show a progress bar while checking repositories.
       - Display a color-coded list of accessible and failed repositories.

Expected Output Example:
    Checking Repositories: 100%|███████████████████| 100/100 [00:10<00:00, 10.15it/s]
    [✓] dman2306: Accessible
    [✓] Victor Santana (Welasco): Accessible
    [⚠] WalksOnAir: Missing 'location' or 'url' key

Notes:
    - Press `Ctrl + C` to stop execution midway.
    - If running inside a virtual environment, activate it first:

        source ~/global_py312/bin/activate  # Example virtual environment
        python checkRepos.py

"""

console = Console()

with open('repositories.json', 'r', encoding='utf-8') as file:
    data = json.load(file)

repositories = data.get("repositories", [])

def check_repository(repo):
    """Check if a repository URL is accessible and return a formatted Rich message."""
    name = repo.get("name", "Unknown Repository")
    url = repo.get("location")

    if not url:
        return Text(f"[⚠] {name}: Missing 'location' key", style="yellow")

    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"
    }

    try:
        response = requests.get(url, headers=headers, timeout=5)
        if response.status_code == 200:
            return Text(f"[✓] {name}: Accessible", style="green")
        else:
            return Text(f"[✗] {name}: Failed with status {response.status_code}", style="red")
    except requests.RequestException as e:
        return Text(f"[✗] {name}: Error - {e}", style="red")

results = thread_map(check_repository, repositories, max_workers=10, desc="Checking Repositories")

for result in results:
    console.print(result)
