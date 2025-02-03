import requests
from bs4 import BeautifulSoup
import pandas as pd

# Step 1: Set the URL of the DSI faculty page
url = 'https://dsi.udel.edu/faculty/'

# Step 2: Send a GET request to the webpage
response = requests.get(url)

# Check if the request was successful
if response.status_code == 200:
    # Step 3: Parse the page content using BeautifulSoup
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Step 4: Find all the faculty entries (adjust based on actual structure)
    faculty_list = []
    
    # This assumes each faculty has a div with the class "listing_list"
    faculty_entries = soup.find_all('div', class_='listing_list')
    # Iterate through the faculty entries
    current_faculty = {}
    for entry in faculty_entries:
        print(entry.text.split('\n'))
        # Extract name if present in this entry (it resets for a new faculty)
        name_tag = entry.find('strong')
        if name_tag:
            # If a new name is found, save the current faculty data and reset
            if current_faculty:
                faculty_list.append(current_faculty)

            current_faculty = {
                'Name': name_tag.text.strip(),
                'College' : 'N/A',
                'Department': 'N/A',
                'Email': 'N/A',
                'Website': 'N/A'
            }
        
        # Extract department or title (from span with specific style)
        department_tag = entry.find('span', style="color: #0070c0;")

        if department_tag:
            current_faculty['Department'] = department_tag.text.strip()
        
        # Extract email if present
        email_tag = entry.find('a', href=lambda href: href and 'mailto:' in href)
        if email_tag:
            current_faculty['Email'] = email_tag.text.strip()
        
        # Extract website if present
        website_tag = entry.find('a', href=lambda href: href and 'http' in href)
        if website_tag:
            current_faculty['Website'] = website_tag['href']
            
        if  len(entry.text.split('\n')) >= 2:
            current_faculty['College'] = entry.text.split('\n')[1]
    
    # Append the last faculty member after the loop ends
    if current_faculty:
        faculty_list.append(current_faculty)
    
    # Step 5: Store the data in a DataFrame or save as CSV/JSON
    df = pd.DataFrame(faculty_list)
    df.to_csv('ud_dsi_faculty.csv', index=False)  # Save as CSV

    print('Faculty data saved to ud_dsi_faculty.csv')

else:
    print('Failed to retrieve the webpage. Status code:', response.status_code)
