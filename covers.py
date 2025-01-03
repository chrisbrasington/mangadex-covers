import os
import sys
import requests
from urllib.parse import urlparse
import json

# Function to extract manga ID from MangaDex URL
def extract_manga_id(url):
    parsed_url = urlparse(url)
    path_parts = parsed_url.path.split('/')
    manga_id = path_parts[2]  # Manga ID is the 3rd part of the URL
    return manga_id

# Function to fetch manga details (including title) from the MangaDex API
def fetch_manga_details(manga_id):
    api_url = f'https://api.mangadex.org/manga/{manga_id}'
    headers = {
        'accept': 'application/json'
    }
    response = requests.get(api_url, headers=headers)
    if response.status_code == 200:
        return response.json()['data']['attributes']
    else:
        print(f"Error fetching manga details: {response.status_code}")
        return None

# Function to fetch covers from the MangaDex API
def fetch_covers(manga_id):
    api_url = f'https://api.mangadex.org/cover?limit=100&manga%5B%5D={manga_id}&order%5BcreatedAt%5D=asc'
    headers = {
        'accept': 'application/json'
    }
    response = requests.get(api_url, headers=headers)
    if response.status_code == 200:
        return response.json()['data']
    else:
        print(f"Error fetching cover data: {response.status_code}")
        return []

# Function to generate HTML content
def generate_html(manga_title, covers):
    html_content = f"""
    <html>
    <head>
        <title>{manga_title} Covers</title>
        <style>
            body {{
                font-family: Arial, sans-serif;
                display: flex;
                flex-wrap: wrap;
                justify-content: center;
            }}
            img {{
                width: 200px;
                margin: 10px;
                border-radius: 8px;
            }}
            a {{
                display: inline-block;
                margin: 5px;
            }}
        </style>
    </head>
    <body>
        <h1>{manga_title} - Cover Images</h1>
        <div>
    """
    
    for cover in covers:
        image_filename = cover['attributes']['fileName']
        cover_id = cover['relationships'][0]['id']
        image_url = f"https://mangadex.org/covers/{cover_id}/{image_filename}"
        
        # Linking the image to its full-size version
        full_image_url = f"https://mangadex.org/covers/{cover_id}/{image_filename}"
        html_content += f'<a href="{full_image_url}" target="_blank"><img src="{image_url}" alt="Cover Image"/></a>\n'
    
    html_content += """
        </div>
    </body>
    </html>
    """
    
    return html_content

# Function to open the generated HTML file with suppressed errors/warnings
def open_html_file(html_file):
    os.system(f'xdg-open {html_file} > /dev/null 2>&1')

# Main function
def main():
    if len(sys.argv) != 2:
        print("Usage: python covers.py <MangaDex URL>")
        sys.exit(1)
    
    manga_url = sys.argv[1]
    manga_id = extract_manga_id(manga_url)
    
    # Fetch the manga title and cover data
    manga_details = fetch_manga_details(manga_id)
    if not manga_details:
        print(f"Unable to fetch details for manga ID {manga_id}.")
        sys.exit(1)
    
    manga_title = manga_details['title']['en'] if 'en' in manga_details['title'] else 'Untitled Manga'
    
    covers = fetch_covers(manga_id)
    
    if not covers:
        print(f"No covers found for manga ID {manga_id}.")
        sys.exit(1)
    
    # Generate HTML content
    html_content = generate_html(manga_title, covers)
    
    # Define the output HTML file name
    html_file = f"{manga_title.replace(' ', '_').lower()}.html"
    
    # Write the HTML content to the file
    with open(html_file, 'w') as file:
        file.write(html_content)
    
    print(f"HTML file '{html_file}' generated successfully.")
    
    # Open the HTML file using xdg-open
    open_html_file(html_file)

if __name__ == "__main__":
    main()
