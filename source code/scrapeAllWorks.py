from scrapeEachRegWork import scrape_each_reg_work, connect
from scrapeEachLTDWork import scrape_each_LTD_work
from verify import VerificationError, verify
from bs4 import BeautifulSoup as BS 
import requests
import csv


def scrape_all_works(birth_date, birth_place, death_date, death_place, education, past_auctions_link, work_type): #append to the csv file 
	all_works_page = connect(past_auctions_link) #go to the page of all the works from past auctions
	all_works_soup = BS(all_works_page, 'lxml')

	try:
		verify(all_works_soup, 'Search Results')
	except VerificationError:
		with open('invalid-all-works-links.txt', 'a') as invalid_all_works_file:
			invalid_all_works_file.write(past_auctions_link + '\n')
		raise VerificationError

	'''
	If the page fails the verification test,
	we put the link into a file for later checks and raise a VerificationError.
	This error is handled by scrape_past_reg_auctions() or scrape_past_LTD_auctions() (see scrapeEachArtist.py).
	This means the first four works from past auctions have already been scraped >>> Beware of duplicates! 
	'''

	try: #finding number of pages
		num_of_pages = int(all_works_soup.find_all('dd')[-1].text.strip('…'))
	except ValueError: #if there is only 1 page
		num_of_pages = 1

	csv_file = open('saffronart.csv', 'a')  	
	csv_writer = csv.writer(csv_file)

	scrape_each_work_mappings = { 
	'scrape_each_reg_work': scrape_each_reg_work,
	'scrape_each_LTD_work': scrape_each_LTD_work
	}

	scrape_each_work = scrape_each_work_mappings['scrape_each_' + work_type + '_work'] 
	#get the correct scrape_each_work function from work_type  

	for page in range(1, num_of_pages + 1):
		page_content = connect(past_auctions_link, {'pu': page})
		page_soup = BS(page_content, 'lxml')
		
		works_list = page_soup.find_all('a', text = 'Details') #list of all the works in the page
		
		for work in works_list:
			work_link = work['onclick'].split("'")[1]

			try:
				(artist_name, title, winning_bid, lo_est, hi_est, 
				auction_name, auction_date, category, style, provenance, exhibition, details) = scrape_each_work(work_link)
				
				csv_writer.writerow([artist_name, birth_date, birth_place, death_date, death_place, education,
				title, winning_bid, lo_est, hi_est, auction_name, auction_date, category, style, provenance, exhibition, details])

			except TypeError:
				continue

	csv_file.close()


if __name__ == '__main__':
	'''
	scrape_all_works('September 17, 1913', 'Pandharpur, Maharashtra', 'June 9, 2011', None, 'Self-taught', 
	'https://www.saffronart.com/search/SearchResult.aspx?all=3&exh=1&past=1&pastsl=1&sq=M%20F%20Husain&artistid=114', 'reg')
	'''
	#https://www.saffronart.com/search/SearchResult.aspx?all=3&amp;past=1&amp;pastsl=1&amp;artistid=790
	print()
