from asyncio import sleep
import time
import requests,openpyxl
from bs4 import BeautifulSoup

excel=openpyxl.Workbook()
sheet=excel.active
sheet.title="Hirestream"
sheet.append(["Company","Interview Questions(DSA)"])
print(excel.sheetnames)
# List of company URLs
company_urls = {
    "accenture": "https://www.geeksforgeeks.org/accenture-interview-questions/",
    "adobe": "https://www.geeksforgeeks.org/adobe-topics-interview-preparation/",
    "amazon": "https://www.geeksforgeeks.org/amazon-topics-interview-preparation/",
    "cisco": "https://www.geeksforgeeks.org/cisco-topics-interview-preparation/",
    "d-e-shaw": "https://www.geeksforgeeks.org/d-e-shaw-topics-interview-preparation/",
    "directi": "https://www.geeksforgeeks.org/directi-topics-interview-preparation/",
    "facebook": "https://www.geeksforgeeks.org/facebook-topics-interview-preparation/",
    "flipkart": "https://www.geeksforgeeks.org/flipkart-topics-interview-preparation/",
    "goldman-sachs": "https://www.geeksforgeeks.org/goldman-sachs-topics-interview-preparation/",
    "google": "https://www.geeksforgeeks.org/google-topics-interview-preparation/",
    "maq-software": "https://www.geeksforgeeks.org/maq-software-topics-interview-preparation/",
    "microsoft": "https://www.geeksforgeeks.org/microsoft-topics-interview-preparation/",
    "morgan-stanley": "https://www.geeksforgeeks.org/morgan-stanley-topics-interview-preparation/",
    "ola-cabs": "https://www.geeksforgeeks.org/ola-cabs-topics-interview-preparation/",
    "paytm": "https://www.geeksforgeeks.org/paytm-topics-interview-preparation/",
    "samsung": "https://www.geeksforgeeks.org/samsung-topics-interview-preparation/",
    "sap-labs": "https://www.geeksforgeeks.org/sap-labs-topics-interview-preparation/",
    "amdocs": "https://www.geeksforgeeks.org/amdocs-interview-questions-for-technical-profiles/",
    "apple": "https://www.geeksforgeeks.org/apple-sde-sheet-interview-questions-and-answers/",
    "atlassian": "https://www.geeksforgeeks.org/atlassian-interview-questions-for-technical-profiles/",
    "ey-ernst-young": "https://www.geeksforgeeks.org/ey-ernst-young-interview-questions-and-answers-for-technical-profiles/",
    "infosys": "https://www.geeksforgeeks.org/infosys-sde-sheet-interview-questions-and-answers/",
    "intuit": "https://www.geeksforgeeks.org/intuit-interview-questions-for-technical-profiles/",
    "juspay": "https://www.geeksforgeeks.org/juspay-interview-questions-for-technical-profiles/",
    "salesforce": "https://www.geeksforgeeks.org/salesforce-interview-questions-for-technical-profiles/",
    "wipro": "https://www.geeksforgeeks.org/wipro-sde-sheet-interview-questions-and-answers/",
    "zoho": "https://www.geeksforgeeks.org/zoho-interview-questions-and-answers-for-technical-profiles/",
    "bny-mellon": "https://www.geeksforgeeks.org/bny-mellon-interview-questions-and-answers-for-technical-profiles/",
    "deloitte": "https://www.geeksforgeeks.org/deloitte-interview-questions-and-answers-for-technical-profiles/",
    "ibm": "https://www.geeksforgeeks.org/ibm-interview-questions-and-answers-for-technical-profiles/",
    "ion-group": "https://www.geeksforgeeks.org/ion-group-interview-questions-and-answers-for-technical-profiles/",
    "jenkins": "https://www.geeksforgeeks.org/jenkins-interview-questions/",
    "jp-morgan": "https://www.geeksforgeeks.org/jp-morgan-interview-questions-and-answers-for-technical-profiles/",
    "kpmg": "https://www.geeksforgeeks.org/kpmg-interview-questions-and-answers-for-technical-profiles/?ref=ml_lbp",
    "nvidia": "https://www.geeksforgeeks.org/nvidia-interview-questions-and-answers-for-technical-profiles/",
    "pwc": "https://www.geeksforgeeks.org/pwc-interview-questions-and-answers-for-technical-profiles/",
    "qualcomm": "https://www.geeksforgeeks.org/qualcomm-interview-questions-and-answers-for-technical-profiles/",
    "synopsys": "https://www.geeksforgeeks.org/synopsys-interview-questions-for-technical-profiles/",
    "tcs": "https://www.geeksforgeeks.org/tcs-sde-sheet-interview-questions-and-answers/",
    "virtusa": "https://www.geeksforgeeks.org/virtusa-interview-questions/"
}


# Set headers to avoid 403 errors
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
}


def scrape_type_1(soup, url):
    # Scraping header (Company name)
    print("Scraping using Type 1 pattern")
    header = soup.find("div", class_="article-title").find("h1")
    company_name = header.text.split()[0] if header else "Unknown Company"
    # Print the company name at the beginning
    print(f"Company: {company_name}")

    # For Accenture, extract only interview questions (ignore descriptions)
    if "accenture" in url.lower():
        print(f"Interview Questions for {company_name}:")

        # Locate the section containing the questions
        question_div = soup.find("div", class_="text")

        if question_div:
            # Extract all <h3> tags that typically contain questions
            questions = question_div.find_all("h3")
            if questions:
                for question in questions:
                    # Only extract the question text without description
                    question_text=question.get_text(strip=True)[3:]
                    print(f"\t- {question_text}")
                    sheet.append([company_name, question_text])

            else:
                print("ALERT: No questions found for this URL!")

    else:
        # For other companies, extract questions from tables without descriptions
        print(f"Questions for {company_name} (DSA Interview Questions):")
        tables = soup.find_all('table')
        if tables:
            for table in tables:
                rows = table.find_all('tr')
                for row in rows[1:]:  # Skip the header row if any
                    cells = row.find_all('td')
                    if cells:
                        # Extract only the first column which contains the question
                        question_text = cells[0].get_text(strip=True)
                        # Skip unwanted rows like "Problems" and "Try It"
                        if "Problems" not in question_text and "Try It" not in question_text:
                            print(f"\t- {question_text}")
                            sheet.append([company_name,question_text])
                print()  # Separation between tables


    print("\n")


# Function for Pattern 2 with flexibility for different structures
def scrape_type_2(soup):
    print("Scraping using Type 2 pattern")

    # Try to find the main header
    company_name = soup.find("div", class_="article-title").find("h1")
    if company_name:
        company_name=company_name.text.split()[0]
        print(f"Company: {company_name}")
    else:
        print("ALERT: No header found for this URL!")
        return

    # List of potential subheader IDs
    subheader_ids = ["easy-level", "medium-level", "hard-level"]

    for subheader_id in subheader_ids:
        subheader = soup.find("div", class_="text").find("h3", id=subheader_id)

        if subheader and subheader.has_attr('id'):
            print(f"{subheader.text} Interview Questions")
            questions = subheader.find_next('ol').find_all("li")
            if questions:
                for question in questions:
                    question_text=question.text
                    print(f"\t- {question_text}")
                    sheet.append([company_name, question_text])


    # Optionally check for other types of subheaders (h4, etc.)
    additional_subheaders = soup.find("div", class_="text").find_all("h4")
    for subheader in additional_subheaders:
        print(f"{subheader.text} Interview Questions")
        questions = subheader.find_next('ol').find_all("li")
        if questions:
            for question in questions:
                question_text=question.text
                print(f"\t- {question.text}")
                sheet.append([company_name, question_text])

    print("\n")


def scrape_type_3(soup):
    print("Scraping using Type 3 pattern")

    # Find the main header (Company)
    company_name = soup.find("div", class_="article-title").find("h1")
    if company_name:
        company_name=company_name.text.split()[0]
        print(f"Company: {company_name}")
    else:
        print("ALERT: No header found for this URL!")
        return
    print(f"Interview Questions for {company_name}:")
    # Find all subheaders (h3) and the associated questions (ol)
    subheaders = soup.find("div", class_="text").find_all("h3")

    for subheader in subheaders:
        # Print the subheader (Difficulty Level)
        level = subheader.find("span").text.strip() if subheader.find("span") else subheader.text.strip()
        if not level=="Why this sheet?":
            print(f"{level} Interview Questions")

        # Find the next <ol> after each subheader and extract the questions
        ol_tag = subheader.find_next("ol")
        if ol_tag:
            questions = ol_tag.find_all("li")
            for question in questions:
                # Extract the question text and print it
                question_text = question.text.strip()
                print(f"\t- {question_text}")
                sheet.append([company_name, question_text])
        else:
            if not level=="Why this sheet?":
                print(f"ALERT: No questions found under {level}!")

    # Scrape tabular data if present

    tables = soup.find_all('table')
    if tables:
        for table in tables:
            rows = table.find_all('tr')
            for row in rows[1:]:  # Skip the header row if any
                cells = row.find_all('td')
                if cells:
                    # Only print the first column data, without any links or other unwanted text
                    problem_title = cells[0].get_text(strip=True)
                    # Skip unwanted text like "Try It", "Problems", etc.
                    if "Problems" not in problem_title and "Try It" not in problem_title:
                        question_text=problem_title
                        print(f"\t- {question_text}")
                        sheet.append([company_name, question_text])

    print("\n")  # Separate sections for readability



import string
def scrape_type_4(soup):
    print("Scraping using Type 4 pattern")

    # Find the main header (Company)
    header = soup.find("div", class_="article-title").find("h1")
    if header:
        company_name = header.text.strip()
        print(f"Company: {company_name.split()[0]}")
    else:
        print("ALERT: No header found for this URL!")
        return

    print(f"Interview questions for {company_name.split()[0]}")

    questions = []

    # Extract questions from <a> tags
    for a in soup.find_all("a"):
        # Check if the <a> tag contains a <strong> or <b> tag
        if a.find("strong") or a.find("b"):
            question_text = a.get_text(strip=True)
            # Filter out unwanted text and clean up the question
            if question_text and not any(keyword in question_text for keyword in ["interested", "Explore", "ALERT"]):
                # Remove leading punctuation (like ".") if present
                question_text = question_text.lstrip(string.punctuation).strip()
                questions.append(question_text)

    # Print the extracted questions
    if questions:
        for question in questions:
            question_text=question
            print(f"\t- {question_text}")
            sheet.append([company_name, question_text])

    # Check if there is a table with problem data
    table = soup.find("figure", class_="table")
    if table:
        problems = []
        rows = table.find_all("tr")[1:]  # Skip the header row
        for row in rows:
            cols = row.find_all("td")
            if len(cols) >= 2:
                problem_name = cols[0].text.strip()  # Problem link text
                problems.append({
                    "problem_name": problem_name
                })

        # Print the extracted problem details
        if problems:
            for problem in problems:
                question_text=problem['problem_name']
                print(f"\t- {question_text}")
                sheet.append([company_name, question_text])
        else:
            print("ALERT: No valid problem entries found in the table.")


def scrape_type_5(soup,url):
    print("Scraping using Type 5 pattern")

    # Find the main header (Company)
    header = soup.find("div", class_="article-title").find("h1")
    if header:
        company_name = header.text.strip().split()[0]
        print(f"Company: {company_name}")
    else:
        print("ALERT: No header found for this URL!")
        return

    # Check for subheaders in <h2>
    subheaders = soup.find("div", class_="text").find("h2")
    if subheaders and "Inorder" not in subheaders.text:
        print(f"{subheaders.text.split()[1]} Interview Questions")

    # Check for <h3> tags for Jenkins-like structure
    questions = soup.find('div', class_="text").find_all("h3")
    for question in questions:
        scraped_question = question.find("span").text.strip() if question.find("span") else question.text.strip()

        if scraped_question and scraped_question[0].isdigit():
            question_text=scraped_question[3:]
            print(f"\t- {question_text}")
            sheet.append([company_name, question_text])


    nvidia_questions = soup.find_all("b")
    if nvidia_questions:
        if "nvidia" in url:
            print("Nvidia Interview Qustions")
        for nvidia_question in nvidia_questions:
            bold_text = nvidia_question.text.strip()
            if bold_text and bold_text[0].isdigit():
                question_text = nvidia_question.find_next("a").text.strip() if nvidia_question.find_next(
                    "a") else nvidia_question.find_next("span").text.strip()
                question_text=question_text
                print(f"\t- {question_text}")
                sheet.append([company_name, question_text])

    print("\n")


def scrape_type_6(soup):
    # Find the main header (Company)
    print("Scraping using Type 6 pattern")
    header = soup.find("div", class_="article-title").find("h1")
    if header:
        company_name = header.text.strip().split()[0]
        print(f"Company: {company_name}")
    else:
        print("ALERT: No header found for this URL!")
        return

    print(f"{header.text.strip()}")

    # Find all <strong> tags which may contain the numbered questions
    questions = soup.find_all("strong")

    if not questions:
        print("No <strong> tags found.")
        return

    # List to store the questions
    extracted_questions = []

    for question in questions:
        question_text = question.text.strip()

        # Check if the <strong> tag contains a question number, e.g., "Q1."
        if question_text.startswith("Q") and question_text[1:].strip(".").isdigit():
            # Find the next <a> tag which contains the actual question text
            associated_link = question.find_next("a")
            if associated_link:
                full_question = associated_link.text.strip()
                extracted_questions.append(f"{question_text} {full_question}")

    # Print only the extracted questions
    if extracted_questions:
        for q in extracted_questions:
            question_text=q[4:]
            print(f"\t- {question_text}")
            sheet.append([company_name, question_text])
    else:
        print("No valid questions found.")

    print("\n")



# Function to detect the HTML pattern and call the appropriate scraper
def scrape_interview_questions(url):
    try:
        source = requests.get(url, headers=headers)
        source.raise_for_status()
        soup = BeautifulSoup(source.text, 'html.parser')

        div_text = soup.find("div", class_="text")

        if div_text and div_text.find("h2"):
            if not ("jenkins" in url or "nvidia" in url):
                scrape_type_1(soup, url)
            else:
                scrape_type_5(soup, url)


        elif div_text and div_text.find("h3"):
            h3_tag = div_text.find("h3")
            if h3_tag and h3_tag.get("id"):
                scrape_type_2(soup)
            elif "virtusa" in url:
                scrape_type_6(soup)
            else:
                scrape_type_3(soup)  # Use pattern 3 if there's an h3 but no id
        else:
            scrape_type_4(soup)
        # else:
        #     print(f"Unable to detect the HTML pattern for URL: {url}")

    except Exception as e:
        print(f"Error scraping {url}: {e}")

continue1="y"
while continue1=="y":
    print("The List of Companies!!")
    for ind,(key,val) in enumerate(company_urls.items()):
        print(f"{ind+1}) {key}")
    user_input=input("Enter the company name to get the Interview Questions (Eg. microsoft,amazonetc):").lower()
    if not user_input in company_urls:
        print("Please enter the valid input with respect to the Companies list!!")
        time.sleep(5)
    else:
        scrape_interview_questions(company_urls[user_input])
        continue1=input("Do you want to continue (Y/N)?:").lower() 

excel.save("Hirestreem.xlsx")