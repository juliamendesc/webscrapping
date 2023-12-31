import csv
import requests
import os
import subprocess
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup

config = load_dotenv("creds.env")

DRIVER_PATH = './chromedriver/chromedriver-linux64/chromedriver'
USERNAME = os.environ.get('USERNAME')
PASSWORD = os.environ.get('PASSWORD')

service = Service(executable_path=DRIVER_PATH)
options = webdriver.ChromeOptions()
options.headless = True
options.binary_location = './chromedriver/chrome-linux64/chrome'
options.add_argument('--headless')
options.add_argument("--window-size=1920,1200")

image_array = []

webpage = "https://www.linkedin.com/jobs/search/?keywords=junior%20developer%20python&location=Lisbon%2C%20Portugal&position=1&pageNum=0&origin=JOB_SEARCH_PAGE_JOB_FILTER&sortBy=DD&start="
# webpage = "https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search?keywords=junior%20developer%20python&location=Lisbon%2C%20Portugal&trk=public_jobs_jobs-search-bar_search-submit&position=1&pageNum=0&origin=JOB_SEARCH_PAGE_JOB_FILTER&sortBy=DD&start="

file = open('linkedin-jobs.csv', 'a')
writer = csv.writer(file)
writer.writerow(['Title', 'Company', 'Location', 'Apply', 'Post Date'])

def get_url_login(driver):
	driver.get('https://www.linkedin.com/login?fromSignIn=true&trk=guest_homepage-basic_nav-header-signin')
	# Enter your email address and password
	driver.find_element(By.ID, value='username').send_keys(USERNAME)
	driver.find_element(By.ID, value='password').send_keys(PASSWORD)
	# Submit the login form
	driver.find_element(By.CLASS_NAME, value='login__form_action_container ').click()

def get_jobs_url(driver, webpage, page_number):
	next_page = webpage+str(page_number)
	response = requests.get(str(next_page))
	driver.implicitly_wait(15)
	driver.save_screenshot('hn_homepage.png')
	if response.status_code != 200:
		print("Error fetching page")
		exit()
	else:
		jobs_content = response.content
	driver.quit()
	parse_content(jobs_content)
	if page_number < 25:
		page_number = page_number + 25
		get_jobs_url(webpage, page_number)
	else:
		file.close()
		print('File closed')

def parse_content(jobs_content):
	soup = BeautifulSoup(jobs_content, 'html.parser')
	jobs = soup.find_all('div', class_='base-card relative w-full hover:no-underline focus:no-underline base-card--link base-search-card base-search-card--link job-search-card')
	for job in jobs:
		job_title = job.find('h3', class_='base-search-card__title').text.strip()
		job_company = job.find('h4', class_='base-search-card__subtitle').text.strip()
		job_location = job.find('span', class_='job-search-card__location').text.strip()
		job_link = job.find('a', class_='base-card__full-link')['href']
		if job.find('time', class_='job-search-card__listdate'):
			job_post_date = job.find('time', class_='job-search-card__listdate').text.strip()
		else:
			'No date'
		create_csv_file(job_title=job_title, job_company=job_company, job_location=job_location, job_link=job_link, job_post_date=job_post_date)

def create_csv_file(job_title, job_company, job_location, job_link, job_post_date):
	if job_title and job_company and job_location and job_link:
		writer.writerow([
			job_title.encode('utf-8'),
			job_company.encode('utf-8'),
			job_location.encode('utf-8'),
			job_link.encode('utf-8'),
			job_post_date.encode('utf-8')
			])
	else:
		print('Error adding to csv file')


def main():
	os.system("sh ./untar.sh")
	driver = webdriver.Chrome(service=service, options=options)

	get_url_login(driver=driver)
	get_jobs_url(driver=driver,webpage=webpage, page_number=25)


if __name__ == '__main__':
	main()
