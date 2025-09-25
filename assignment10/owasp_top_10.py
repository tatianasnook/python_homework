import csv
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By


driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))

# Task 6: Scraping Structured Data

# 1. Use your browser developer tools to view this page: [https://owasp.org/www-project-top-ten/].  
# You are going to extract the top 10 security risks reported there.  Figure out how you will find them.

# 2. Within your python_homework/assignment10 directory, write a script called owasp_top_10.py. 
# Use selenium to read this page.

# 3. Find each of the top 10 vulnerabilities.  Hint: You will need XPath.  
# For each of the top 10 vulnerabilites, keep the vulnerability title and the href link in a dict.  
# Accumulate these dict objects in a list.

# 4.Print out the list to make sure you have the right data.  
# Then, add code to the program to write it to a file called owasp_top_10.csv.  Verify that this file appears correct.

# 5. Create a file, challenges.txt, also within your lesson9 directory.  
# In this file, describe any challenges you faced in completing this assignment and how you resolved them.

try:
    driver.get("https://owasp.org/www-project-top-ten/")

    vulnerabilities = []

    h2_element = driver.find_element(By.CSS_SELECTOR, '[id="top-10-web-application-security-risks"]')
    ul_element = h2_element.find_element(By.XPATH, 'following-sibling::p/following-sibling::ul')
    li_elements = ul_element.find_elements(By.TAG_NAME, 'li')

    print(f"Found {len(li_elements)} li_elements")

    for li in li_elements:
        a_tag = li.find_element(By.TAG_NAME, 'a')
        strong_tag = a_tag.find_element(By.TAG_NAME, 'strong')
        title = strong_tag.text
        link = a_tag.get_attribute('href')
        vulnerabilities.append({'title': title, 'link': link})

except Exception as e:
    print("couldn't get the web page")
    print(f"Exception: {type(e).__name__} {e}")
finally:
    driver.quit()

print(vulnerabilities)

with open('owasp_top_10.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["title", "link"])
    for vulnerability in vulnerabilities:
        writer.writerow([vulnerability["title"], vulnerability["link"]])
