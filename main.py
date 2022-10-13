from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager 
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service

import time, bs4, sys, requests, io, os
from pyfiglet import figlet_format
from colorama import Fore, Back, Style
from PIL import Image
import PIL


##-----------------------------##
##      DEFINING FUNCTIONS     ##
##-----------------------------##

#creating progress bar
def progress(count, total, status='', bar_len=60):
        filled_len = int(round(bar_len * count / float(total)))

        percents = round(100.0 * count / float(total), 1)
        bar = chr(9608) * filled_len + '-' * (bar_len - filled_len)

        fmt = '[%s] %s%s ...%s' % (bar, percents, '%', status)
        print(Fore.BLUE + '\b' * len(fmt), end='')  # clears the line
        sys.stdout.write(fmt)
        sys.stdout.flush()


#taking userinput - images to scrape
def userinput():
    while True:
        try:
            images_to_scrape = int(input("How many images to scrape: "))
        #if the user doesn't type int
        except ValueError:
            print(Fore.BLUE + "Error: Please enter a valid number")
            continue
        #if the user types correct input
        else:
            return images_to_scrape

#scrolling the google results page
def scroll(i):
    for _ in range(5):
        driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
        time.sleep(i)

##-----------------------------##
##-----------------------------##



##-----------------------------##
##   CHROME BROWSER SETTINGS   ##
##-----------------------------##
options = Options()
options.add_argument('--headless')
options.add_argument('--disable-gpu')
options.add_argument('--log-level=3')
options.add_argument('--disable-software-rasterizer')
options.add_argument('--ignore-certificate-errors-spki-list')
options.add_argument('--ignore-ssl-errors')
options.add_argument('--ignore-certificate-errors')
options.add_experimental_option('excludeSwitches', ['enable-logging'])

##-----------------------------##
##-----------------------------##


##-----------------------------##
##          SCRAPER            ##
##-----------------------------##

print(Fore.RED + '''
 ██████╗  ██████╗  ██████╗  ██████╗ ██╗     ███████╗    ███████╗ ██████╗██████╗  █████╗ ██████╗ ███████╗██████╗ 
██╔════╝ ██╔═══██╗██╔═══██╗██╔════╝ ██║     ██╔════╝    ██╔════╝██╔════╝██╔══██╗██╔══██╗██╔══██╗██╔════╝██╔══██╗
██║  ███╗██║   ██║██║   ██║██║  ███╗██║     █████╗      ███████╗██║     ██████╔╝███████║██████╔╝█████╗  ██████╔╝
██║   ██║██║   ██║██║   ██║██║   ██║██║     ██╔══╝      ╚════██║██║     ██╔══██╗██╔══██║██╔═══╝ ██╔══╝  ██╔══██╗
╚██████╔╝╚██████╔╝╚██████╔╝╚██████╔╝███████╗███████╗    ███████║╚██████╗██║  ██║██║  ██║██║     ███████╗██║  ██║
 ╚═════╝  ╚═════╝  ╚═════╝  ╚═════╝ ╚══════╝╚══════╝    ╚══════╝ ╚═════╝╚═╝  ╚═╝╚═╝  ╚═╝╚═╝     ╚══════╝╚═╝  ╚═╝
''')

#enter the search term
search_term = input(Fore.MAGENTA + "Enter your search term: ")
#number of images to scrape
images_to_scrape = userinput()

#1s delay
time.sleep(1)

print(Fore.GREEN + "Launching Scraper... Will start in 10 seconds....")

time.sleep(1)

print("Scrolling Results....")

#Chome Drive Initialization
chrome_executable = Service(executable_path="C:\\Users\\Volted User\\Desktop\\Google-Image-Scraper\\chromedriver.exe")
driver = webdriver.Chrome(service=chrome_executable, options=options)

#google images url
driver.get("https://www.google.co.in/imghp")

driver.find_element(By.XPATH, "//input[@title='Search']").send_keys(search_term)

driver.find_element(By.XPATH, "//button[@aria-label='Google Search']").send_keys(Keys.ENTER)

#if we are scraping less than 30 images, we don't have to scroll
if images_to_scrape > 30:
    scroll(3)

    try:
        button_check = driver.find_element(By.XPATH, '//*[@id="islmp"]/div/div/div/div[1]/div[2]/div[2]/input')
        if button_check.get_attribute('type') == 'button':
            button_check.click()
            scroll(5)
    except:
        pass

#initializing the image counter, collecting all the image urls in a list
count = 1
urls = []
#
'''
Every 25th element, there is a suggesting bar, we'll ignore that 
'''
#
unwanted = [not_image for not_image in range(25,700,25)]

#starting the scraper
scraper_start = time.time()

#for all the results in the page
for i in range(1,500):
    #try to process the image
    try:
        #checking if we've already scraped enough images and if the element is not a suggestion bar
        if i not in unwanted and count <= images_to_scrape:
            #low-res image url
            preview_image = driver.find_element(By.XPATH, f'//*[@id="islrg"]/div[1]/div[{i}]/a[1]/div[1]/img').get_attribute('src')
            driver.find_element(By.XPATH, f'//*[@id="islrg"]/div[1]/div[{i}]/a[1]').send_keys(Keys.ENTER)

            #waiting for high-res image url
            start_time = time.time()

            while True:
                #high-res image url
                actual_image = driver.find_element(By.XPATH, '//*[@id="Sva75c"]/div/div/div[3]/div[2]/c-wiz/div/div[1]/div[1]/div[3]/div/a/img').get_attribute("src")
                current_time = time.time()

                #if the low res and high res images have diff urls, we proceed else we wait for 3 seconds
                try:
                    if preview_image != actual_image and not actual_image.startswith("data"):
                        #path to save the file
                        #os.chdir(r'C:\Users\Volted User\Desktop\Google-Image-Scraper\images')

                        #resizing the image
                        r = requests.get(actual_image, stream = True).content
                        img = Image.open(io.BytesIO(r))
                        #img = img.resize((400,400), Image.Resampling.LANCZOS)
                        img.save('image-{}.png'.format(count))
                        #urls.append(actual_image)
                        progress(count,images_to_scrape)
                        count +=1
                        break
                except PIL.UnidentifiedImageError:
                    break

                #if we dont get a high res image url within 3 secs, we move on to the next image
                else:
                    if (current_time - start_time) > 3:
                        break
                    continue
    # if we're unable to process the current image, we move on to the next image
    except:
        continue

#scraping completed
scraper_end = time.time()



# print(Fore.GREEN + "Images Saved.")
print("\n")
print("Printing Statistics")
print(f"Time Taken to Scrape: {round((scraper_end - scraper_start), 2)}")
print(f"Images successfully scraped: {count-1}")
