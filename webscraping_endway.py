import os
import re
import sys
import datetime
import time
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from openpyxl import Workbook
import threading
import json
from multiprocessing import Process

# scraping_url = "http://localhost:8012/test1.php"
scraping_url = "https://auth.salesgenie.com/account/mixed?ReturnUrl=%2fissue%2fwsfed%3fwa%3dwsignin1.0%26wtrealm%3dhttps%253a%252f%252fapp.salesgenie.com%26wctx%3drm%253d0%2526id%253dpassive%2526ru%253d%25252fhome%25252fhome%26wct%3d2020-02-06T15%253a43%253a33Z%26wreply%3dhttps%253a%252f%252fapp.salesgenie.com%252fHome%252fHome&wa=wsignin1.0&wtrealm=https%3a%2f%2fapp.salesgenie.com&wctx=rm%3d0%26id%3dpassive%26ru%3d%252fhome%252fhome&wct=2020-02-06T15%3a43%3a33Z&wreply=https%3a%2f%2fapp.salesgenie.com%2fHome%2fHome"
threadLock = threading.Lock()
start_page = 0
end_page = 29000
cur_page = 0

def save_thread_to_excel(r_cnt, row, sheet):
	excel_header = ['A', 'B', 'C', 'D', 'F', 'G', 'H', 'I', 'K']
	
	f_cnt = 0
	# fields = row.find_elements_by_css_selector('td .td-content .business-name-column .business-name-column__name,td .td-content .executive-column,td .td-content .phone-column,td .td-content .address-column,td .SICCode-data,td .SICDescription-data')
	fields = row.find_elements_by_css_selector('td')
	for field in fields:
		sheet[excel_header[f_cnt]+str(r_cnt)] = field.text
		f_cnt = f_cnt + 1


def scraping_90page(workbook_name, workbook_page_cnt):
	# filename = "scraped_data.xlsx"
	workbook = Workbook()
	workbook.security.workbookPassword = 'pythondeveloper!123@234#345$456'
	workbook.security.lockStructure = True
	workbook.security.revisionsPassword = 'pythondeveloper!123@234#345$456'
	sheet = workbook.active
	sheet.protection.sheet = True
	sheet.protection.disable()
	sheet.protection.set_password('pythondeveloper!123@234#345$456')

	sheet["A1"] = "IMAGE"
	sheet["B1"] = "BUSINESS_NAME!"
	sheet['C1'] = "EXECUTIVE_INFO"
	sheet['D1'] = "EXECUTIVE_INFO"
	sheet['E1'] = "PHONE"
	sheet['F1'] = "ADDRESS"
	sheet['G1'] = "SIC_DESCRIPTION"
	sheet['H1'] = "ETC_COLUMN"


	fieldnames = ['IMAGE', 'BUSINESS_NAME', 'EXECUTIVE_INFO', 'PHONE', 'ADDRESS', 'SIC_CODE', 'SIC_DESCRIPTION', 'ETC_COLUMN']

	book_cnt = workbook_page_cnt

	r_cnt = 2
	for page_cnt in range(0, book_cnt):

		driver.execute_script("if($(\"#scraping_tmp\").length == 0){$(\"body\").append(\"<div style='opacity: 0.1' id='scraping_tmp'></div>\");}var row_elements = $('#gridContainer table.grid__table.grid-scrolling-table tbody.column-rows tr');var arr = {};var row_cnt = "+str(r_cnt)+";var f_alias = [\"A\",\"B\",\"C\",\"D\",\"E\",\"F\",\"G\",\"H\",\"I\"];for (var i = 0; i < row_elements.length; i++) {var fields = $(row_elements[i]).find('td');for (var j = 0; j < fields.length; j++) {arr[f_alias[j]+row_cnt] = fields.eq(j).text();}row_cnt++;}var str = JSON.stringify(arr);$(\"#scraping_tmp\").text(str);")
		time.sleep(1)
		elements = driver.find_element_by_css_selector('#scraping_tmp')
		parsed_json = json.loads(elements.text)
		
		for key in parsed_json:
			sheet[key] = parsed_json[key]

		driver.execute_script("document.querySelector('#gridContainer .next').click()")
		time.sleep(0.2)
		driver.execute_script("if(document.querySelector('#gridContainer .grid-container__tables .grid > div > div[style ^= \"position: absolute;\"]')) document.querySelector('#gridContainer .grid-container__tables .grid > div > div[style ^= \"position: absolute;\"]').id='waiting_element'")
		time.sleep(0.2)
		driver.execute_script("if(document.querySelector('#gridContainer .grid-container__tables .grid > div > div[style ^= \"position: absolute;\"]')) document.querySelector('#gridContainer .grid-container__tables .grid > div > div[style ^= \"position: absolute;\"]').id='waiting_element'")
		time.sleep(0.2)
		driver.execute_script("if(document.querySelector('#gridContainer .grid-container__tables .grid > div > div[style ^= \"position: absolute;\"]')) document.querySelector('#gridContainer .grid-container__tables .grid > div > div[style ^= \"position: absolute;\"]').id='waiting_element'")
		time.sleep(0.2)
		driver.execute_script("if(document.querySelector('#gridContainer .grid-container__tables .grid > div > div[style ^= \"position: absolute;\"]')) document.querySelector('#gridContainer .grid-container__tables .grid > div > div[style ^= \"position: absolute;\"]').id='waiting_element'")

		wait = WebDriverWait(driver, 30)
		men_menu = wait.until(EC.invisibility_of_element_located((By.ID, "waiting_element")))
		print("geted page number =====> ", page_cnt, "/", book_cnt)
		r_cnt = r_cnt + 90

	
	workbook.save(filename=workbook_name)


def start_scraping(url):
	if sys.argv[1] != "pythondeveloper!123@234#345$456" :
		print("Password incorrect")
		driver.quit()
		return
	
	driver.get(url)
	print("running scraping")

	driver.execute_script("document.querySelector('#UserName').value='affilitate@nationalstudentloans.org'")#oceaniccapital@gmail.com, bola@nationalstudentloans.org
	driver.execute_script("document.querySelector('#Password').value='soul1624'")#Nostrand991
	time.sleep(0.3)
	driver.execute_script("document.querySelector('#formSignIn').click()")
	time.sleep(8)
	driver.execute_script("document.querySelector('#submit').click()")
	time.sleep(8)
	driver.execute_script("document.querySelector('.post-auth-section .fluid-grid a').click()")
	time.sleep(15)

	print("starting scraping")
	total_page_cnt = driver.find_element_by_css_selector('#gridContainer .page-input').text
	# page-input__input-control
	if total_page_cnt == "":
		print("Your net speed is too slow or data does not exist")
		driver.quit()

	# total_page_cnt = 270
	total_page_cnt = int(total_page_cnt[total_page_cnt.rfind(" "):].replace(",",""))
	
	start_page = 1200
	end_page = total_page_cnt
	
	end_page = start_page + 1500
	try:
		if sys.argv[2] :
			start_page = int(sys.argv[2])
		
		
		if sys.argv[3] :
			end_page = int(sys.argv[3])
	except:
		print("start, end is not seted")
	

	time.sleep(30)


	for i in range(start_page, end_page, 150):
		work_book_name = "C:/ProgramData/Adobe/ARM/scrapped_data" + str(i) + ".xlsx"

		workbook_page_cnt = 150
		if i + 150 > total_page_cnt :
			workbook_page_cnt = total_page_cnt - i + 1
		cur_page = i
		scraping_90page(work_book_name, workbook_page_cnt)
	
	work_book_name = "scrapped_data_xxxx_.xlsx"
	workbook_page_cnt = 2
	scraping_90page(work_book_name, workbook_page_cnt)
	
	print("scraping end")
	time.sleep(1000)

	driver.quit()



driver = webdriver.Chrome()
threads = list()


if __name__=='__main__' :
	start_scraping(scraping_url);
