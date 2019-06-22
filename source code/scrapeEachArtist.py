from scrapeAllWorks import scrape_all_works
from scrapeEachRegWork import scrape_each_reg_work, connect 
from scrapeEachLTDWork import scrape_each_LTD_work
from verify import VerificationError, verify
from bs4 import BeautifulSoup as BS
import requests
import csv


def scrape_past_reg_auctions(birth_date, birth_place, death_date, death_place, education, artist_soup):
	try: 
	#if there is a "Show All" button, go to the the page that shows all the works and scrape that page 
		past_reg_auctions_link = artist_soup.find('a', id = 'ContentPlaceHolder1_SearchResults_showAllPreviousAuctions')['href'] #sublink
		past_reg_auctions_link = 'https://www.saffronart.com' + past_reg_auctions_link[2:] #full link to the page that shows all the works 
		scrape_all_works(birth_date, birth_place, death_date, death_place, education, past_reg_auctions_link, work_type = 'reg')
	
	except (TypeError, VerificationError) as e:  		
		#if there is no "Show All" button but there're still some works available, we scrape each available work 
		reg_works_list = artist_soup.find('table', id = 'ContentPlaceHolder1_SearchResults_previousAuctionItemsList')  
		reg_works_list = reg_works_list.find_all('a', text = 'Details') #list of all the works available

		csv_file = open('saffronart.csv', 'a')  	
		csv_writer = csv.writer(csv_file)
			
		for reg_work in reg_works_list: #go through each work and scrape it
			reg_work_link = reg_work['onclick'].split("'")[1]

			try:
				(artist_name, title, winning_bid, lo_est, hi_est, 
				auction_name, auction_date, category, style, provenance, exhibition, details) = scrape_each_reg_work(reg_work_link)
				
				csv_writer.writerow([artist_name, birth_date, birth_place, death_date, death_place, education,
				title, winning_bid, lo_est, hi_est, auction_name, auction_date, category, style, provenance, exhibition, details])

			except TypeError:
				continue

		csv_file.close()


def scrape_past_LTD_auctions(birth_date, birth_place, death_date, death_place, education, artist_soup):
	try:
		past_LTD_auctions_link = artist_soup.find('a', id = 'ContentPlaceHolder1_SearchResults_showAllSLPreviousAuctions')['href'] #sublink
		past_LTD_auctions_link = 'https://www.saffronart.com' + past_LTD_auctions_link[2:] #full link
		scrape_all_works(birth_date, birth_place, death_date, death_place, education, past_LTD_auctions_link, work_type = 'LTD') 
	
	except (TypeError, VerificationError) as e:
		LTD_works_list = artist_soup.find('table', id = 'ContentPlaceHolder1_SearchResults_previousSLAuctionItemsList')
		LTD_works_list = LTD_works_list.find_all('a', text = 'Details')

		csv_file = open('saffronart.csv', 'a')  	
		csv_writer = csv.writer(csv_file)
			
		for LTD_work in LTD_works_list:
			LTD_work_link = LTD_work['onclick'].split("'")[1]

			try:
				(artist_name, title, winning_bid, lo_est, hi_est, 
				auction_name, auction_date, category, style, provenance, exhibition, details) = scrape_each_LTD_work(LTD_work_link)

				csv_writer.writerow([artist_name, birth_date, birth_place, death_date, death_place, education,
				title, winning_bid, lo_est, hi_est, auction_name, auction_date, category, style, provenance, exhibition, details])

			except TypeError:
				continue 

		csv_file.close()


def scrape_each_artist(profile_link):
	artist_page = connect(profile_link)
	artist_soup = BS(artist_page, 'lxml')

	try: #verifying the artist page
		verify(artist_soup, 'Artist')
	except VerificationError: #put the link into a file for later checks 
		with open('invalid-artist-links.txt', 'a') as invalid_artist_file:
			invalid_artist_file.write(profile_link + '\n')
		return 

	try: #if there is info about the artist's birthdate 
		birth_date = ' '.join(artist_soup.find('span', id = 'ContentPlaceHolder1_lblBirthInfo').text.split())
	except AttributeError:
		birth_date = None
	
	try: #if there is info about the artist's birthplace 
		birth_place = ' '.join(artist_soup.find('span', id = 'ContentPlaceHolder1_lblBirthPlace').text.split())
	except AttributeError:
		birth_place = None

	try: #if there is info about the artist's death date 
		death_date = ' '.join(artist_soup.find('span', id = 'ContentPlaceHolder1_lblDeathInfo').text.split())
	except AttributeError:
		death_date = None

	try: #if there is info about the artist's death place 
		death_place = ' '.join(artist_soup.find('span', id = 'ContentPlaceHolder1_lblDeathPlace').text.split())
	except AttributeError:
		death_place = None

	try: #if there is info about the artist's education 
		education = artist_soup.find('span', id = 'ContentPlaceHolder1_lblEducation').text 
	except AttributeError:
		education = None

	try:
		scrape_past_reg_auctions(birth_date, birth_place, death_date, death_place, education, artist_soup)
	except AttributeError as no_work_error: #if there is no work at past auctions 
		pass 

	try:
		scrape_past_LTD_auctions(birth_date, birth_place, death_date, death_place, education, artist_soup)	
	except AttributeError as no_work_error:
		pass  


if __name__ == '__main__':
	#scrape_each_artist('https://www.saffronart.com/artists/jamini-roy')
	#scrape_each_artist('https://www.saffronart.com/artists/b-prabha')
	#scrape_each_artist('https://www.saffronart.com/artists/pooja')
	#scrape_each_artist('https://www.saffronart.com/artists/kriti-arora')
	#scrape_each_artist('https://www.saffronart.com/artists/m-f-husain') 
	#scrape_each_artist('https://www.saffronart.com/artists/van%20cleef-&%20arpels')
	#scrape_each_artist('https://www.saffronart.com/artists/a-a-almelkar') 
	print()
