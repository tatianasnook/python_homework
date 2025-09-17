import json
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import pandas as pd


driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))

# Task 3: Write a Program to Extract this Data

# 1. get_books.py. The program should import from selenium and webdriver_manager, as shown in your lesson. 
# You also need pandas and json.

# 2. Add code to load the web page given in task 2.

# 3. Find all the li elements in that page for the search list results.  You use the class values you stored in task 2 step 3. 
# Also use the tag name when you do the find, to make sure you get the right elements.

# 4. Within your program, create an empty list called results. 
# You are going to add dict values to this list, one for each search result.

#5. Main loop: You iterate through the list of li entries.  For each, you find the entry that contains title of the book,
# and get the text for that entry.  Then you find the entries that contain the authors of the book, and get the text for each. 
# If you find more than one author, you want to join the author names with a semicolonbetween each.
# Then you find the div that contains the format and the year, and then you find the span entry within it that contains this information.
# You get that text too.  You now have three pieces of text.  
# Create a dict that stores these values, with the keys being Title, Author, and Format-Year.  
# Then append that dict to your results list.

# 6. Create a DataFrame from this list of dicts.  Print the DataFrame.

results = []

try:
    driver.get("https://durhamcounty.bibliocommons.com/v2/search?query=learning%20spanish&searchType=smart")

    list_elements = driver.find_elements(By.CLASS_NAME, "cp-search-result-item")
    print(f"Found {len(list_elements)} search results")
    
    for list_element in list_elements:
        title_elem = list_element.find_element(By.CLASS_NAME, "title-content")
        title = title_elem.text.strip()

        author_elems = list_element.find_elements(By.CLASS_NAME, "author-link")
        authors = "; ".join([a.text.strip() for a in author_elems]) if author_elems else ""

        format_year_elem = list_element.find_element(By.CLASS_NAME, "display-info-primary")
        format_year_text = format_year_elem.text.strip()
        format_year = format_year_text.split("—")[0].strip()
        
        results.append({
            "Title": title,
            "Author": authors,
            "Format-Year": format_year
        })

except Exception as e:
    print("couldn't get the web page")
    print(f"Exception: {type(e).__name__} {e}")
finally:
    driver.quit()

df = pd.DataFrame(results)
print(df)

# Task 4: Write out the Data

# 1. Write the DataFrame to a file called get_books.csv, within the assignment10 folder.
# Examine the file to see if it looks right.

df.to_csv("assignment10/get_books.csv", index=False)

# 2. Write the results list out to a file called get_books.json, also within the assignment10 folder.  
# You should write it out in JSON format.  Examine the file to see if it looks right.

data = {"books_data": results}
with open('assignment10/get_books.json', 'w') as json_file:
    json.dump(data, json_file, indent=4)
    