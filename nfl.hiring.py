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

# Find the section with the "OC/DC INTERVIEWS" heading (looks for <h2> -> <strong>)
oc_dc_interviews_section = None
oc_dc_link = soup.find('h2', string='OC/DC INTERVIEWS')  # Find the h2 tag with the specific text

if oc_dc_link:
    # The <strong> tag is inside the <h2>, so find the section after this
    oc_dc_interviews_section = oc_dc_link.find_next('div')  # You can adjust the tag if needed

if oc_dc_interviews_section is None:
    raise ValueError("OC/DC INTERVIEWS section not found on the page.")

# Extract relevant information from the section
data = []

# Look for <ul> tags and extract information from <li> tags within them
for ul in oc_dc_interviews_section.find_all('ul'):
    for li in ul.find_all('li'):
        text = li.get_text(strip=True)
        print(f"Scraping: {text}")  # For debugging, to see the content of each <li> tag
        
        # Process the text to extract the relevant data (candidate, former employment, and status)
        parts = text.split(',')  # Split by commas to handle candidate name and former employment
        if len(parts) >= 2:
            candidate_name = parts[0].strip()
            former_employment = parts[1].strip() if len(parts) > 1 else 'N/A'

            # Check if the status (last part) exists
            status = text.split('(')[-1].split(')')[0].strip() if '(' in text else 'N/A'
            
            data.append({
                'Candidate Name': candidate_name,
                'Former Employment': former_employment,
                'Status': status
            })

# Print the extracted data to see if it's being collected correctly
if data:
    print(f"Total candidates extracted: {len(data)}")
else:
    print("No candidates found.")

# Save the data to an Excel file if you have valid extracted data
if data:
    df = pd.DataFrame(data)
    output_file = 'nfl_coaching_interviews_2025.xlsx'
    
    # Debugging step: print the DataFrame before saving
    print(df.head())  # Shows the first few rows of the DataFrame
    
    df.to_excel(output_file, index=False)
    print(f"Data successfully saved to {output_file}.")
else:
    print("No data extracted, nothing to save.")


