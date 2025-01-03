# MangaDex Covers Downloader

This script allows you to generate an HTML file displaying all cover images of a manga from MangaDex based on a provided manga URL.

![](.img/tsubasa.png)

## Requirements
- Python 3.x
- `requests` library

Install the required library using:
```
pip install requests
```

## Usage
Run the script with the following command:
```
python covers.py <MangaDex URL>
```

### Example:
```
python covers.py https://mangadex.org/title/f830514d-f3e1-4b11-b18b-e5f7b6d9b861/tsubasa-reservoir-chronicle
```

This will generate an HTML file displaying all cover images for the manga and open it using the default web browser.

## License
This project is licensed under the MIT License.
