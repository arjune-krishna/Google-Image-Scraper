# Google Image Scraper
Scrape Images off Google Search Results.

## Pre-requisites:
1. Google Chrome
1. Selenium (pip install Selenium)
2. Pillow (pip install Pillow)

## Setup:
1. Open command prompt
2. Clone this repository (or [download](https://github.com/arjune-krishna/Google-Image-Scraper.git))
    ```
    gh repo clone arjune-krishna/Google-Image-Scraper
    ```
3. Install Dependencies
    ```
    pip install -r requirements.txt
    ```
4. Edit your desired parameters in main.py
    ```
    search_keyword      = Keyword for the search query
    images_to_scrape    = Number of Images to Scrape
    height              = Height of the Image
    width               = Width of the Image
    ```
5. Run the program
    ```
    python main.py
    ```
    
## Usage:
This project was created to bypass Google Chrome's new restrictions on web scraping from Google Images. 
To use it, define your desired parameters in main.py and run through the command line:
```
python main.py
```
Note: The max number of images that can be scraped at once is 200-300. You might faces errors if you try to scrape more than this. 
In order to scrape more than 200-300 images, use multiple similar keywords.


## Important:
- This program will not run through VSCode. It must be run in the command line. 
- This program will install an updated webdriver automatically. There is no need to install your own.
- V2 version will be launched soon...

### Please like, subscribe, and share if you found my project helpful! 
