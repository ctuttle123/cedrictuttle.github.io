---
layout: default
title: "NFL Coaching Data Scraper"
permalink: /projects/nfl-scraper/
---

# NFL Coaching Data Scraper (2025)

This project scrapes NFL websites to extract coaching and GM interview data for the 2025 hiring cycle and saves it to an Excel file. The scraper uses `requests` to fetch the page, `BeautifulSoup` to parse the HTML, and `pandas` to store the data.

---

## Python Script

```python```
import requests
from bs4 import BeautifulSoup
import pandas as pd

# URL of the NFL coaching and GM tracker for the 2025 hiring cycle
url = "https://www.nfl.com/news/nfl-coaching-gm-tracker-latest-news-interviews-developments-in-2025-hiring-cycle"

# Send a GET request to the URL
response = requests.get(url)
response.raise_for_status()  # Raise an error for bad status codes

# Parse the HTML content using BeautifulSoup
soup = BeautifulSoup(response.content, 'html.parser')

# Find the section with the "OC/DC INTERVIEWS" heading
oc_dc_interviews_section = None
oc_dc_link = soup.find('h2', string='OC/DC INTERVIEWS')

if oc_dc_link:
    oc_dc_interviews_section = oc_dc_link.find_next('div')

if oc_dc_interviews_section is None:
    raise ValueError("OC/DC INTERVIEWS section not found on the page.")

# Extract relevant information from the section
data = []

for ul in oc_dc_interviews_section.find_all('ul'):
    for li in ul.find_all('li'):
        text = li.get_text(strip=True)
        parts = text.split(',')
        if len(parts) >= 2:
            candidate_name = parts[0].strip()
            former_employment = parts[1].strip() if len(parts) > 1 else 'N/A'
            status = text.split('(')[-1].split(')')[0].strip() if '(' in text else 'N/A'
            data.append({
                'Candidate Name': candidate_name,
                'Former Employment': former_employment,
                'Status': status
            })

# Save the data to an Excel file
if data:
    df = pd.DataFrame(data)
    output_file = 'nfl_coaching_interviews_2025.xlsx'
    df.to_excel(output_file, index=False)
    print(f"Data successfully saved to {output_file}.")
else:
    print("No data extracted, nothing to save.")
    output_file = 'nfl_coaching_interviews_2025.xlsx'
    df.to_excel(output_file, index=False)
