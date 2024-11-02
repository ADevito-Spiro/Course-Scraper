from bs4 import BeautifulSoup
import time
import requests

def course_scrap(url):
    courses = []
    next_page_url = url
    next_page = 2

    while next_page_url:
        response = requests.get(next_page_url)

        soup = BeautifulSoup(response.content, 'html.parser')

        page_courses = soup.find_all('td', class_='width')
        for course in page_courses:
            course_text = course.get_text(strip=True)
            courses.append(course_text)

        print(f"Scraped {len(page_courses)} courses from this page.")

        #Replace the element tag in soup.find with the element of the next page indicator.
        next_page_element = soup.find('a', {'aria-label': f'Page {next_page}'})

        #Combines the element from above with a static url to get the next page.
        #Note this is how it is achieved through my school but you will need to inspect element to find the proper way to get the next page.
        if next_page_element and 'href' in next_page_element.attrs:
            next_page_url = 'insert url here' + next_page_element['href']
            next_page += 1
        else:
            next_page_url = None

        # Wait for 1 second before going to the next page, to avoid sending too many requests at once.
        # Could be faster without this line.
        time.sleep(1)

    return courses

#Writes the list of courses to a file
def write_courses_to_file(courses, filename):
    with open(filename, 'w') as f:
        for course in courses:
            f.write(course + '\n')
    print(f"Courses have been written to {filename}")


#This line is where you will put the URL of the School's Course Catalog that you want to Scrape. 
url = "insert school url here"
output_file = "courses.txt"

all_courses = course_scrap(url)
write_courses_to_file(all_courses, output_file)