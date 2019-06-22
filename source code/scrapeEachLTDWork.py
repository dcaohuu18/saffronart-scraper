from scrapeEachRegWork import connect
from bs4 import BeautifulSoup as BS
import requests 


def scrape_each_LTD_work(LTD_work_link): #return each LTD work's info
	LTD_work_soup = BS(connect(LTD_work_link), 'lxml')

	try:
		auction_info = LTD_work_soup.find('input', id = 'hdnAuctionTitle')['value'] 
		#auction info contains the auction's name & date
	except TypeError:
		with open('invalid-LTD-work-links.txt', 'a') as invalid_LTD_work_file:
			invalid_LTD_work_file.write(LTD_work_link + '\n')
		return

	'''
	All works have information about auction name and auction date.
	Therefore, when BS can't find these info (TypeError raised),
	it means the website has redirected us to an 'invalid' page. 
	To handle this exception, we put the 'bad' links into a file for later checks. 
	'''

	auction_name = auction_info.split('(')[0].strip() #extract the auction's name from auction info
	auction_date = auction_info.split('(')[1].strip(')').strip() #extract the auction's date from auction info

	artist_info = LTD_work_soup.find('h2', id = 'head1').text
	artist_name = artist_info.split('(')[0].strip() #extract the artist's name from artist_info

	title = LTD_work_soup.find('h4', id = 'head2').text.strip()
	
	try:#if there is info about winning bid
		winning_bid = LTD_work_soup.find('span', id = 'lblCurrentBid').text.split('|')[0].strip() #get the winning bid in $
	except IndexError:
		winning_bid = None

	try: #if there are estimates
		estimate_text = LTD_work_soup.find('span', id = 'lblEstimate').text
		lo_est = estimate_text.split('(')[1].split('-')[0].strip()
		hi_est = estimate_text.split('(')[1].split('-')[1].strip(' )').strip()
	except AttributeError:
		lo_est, hi_est = None, None

	details_soup = LTD_work_soup.find('div', id = 'details')
	details_soup_str = str(details_soup)
	
	try: #extracting provenance from details
		provenance = ' | '.join(details_soup_str.split('PROVENANCE:', 1)[1].split('</p>')[0].split('<br/>')).strip(' | ')
	except IndexError:
		provenance = None
	
	try: #extracting publication or exhibition info from details 
		exhibition = ' | '.join(details_soup_str.split('PUBLISHED:', 1)[1].split('</p>')[0].split('<br/>')).strip(' | ')
	except IndexError:
		try:
			exhibition = ' | '.join(details_soup_str.split('EXHIBITED:', 1)[1].split('</p>')[0].split('<br/>')).strip(' | ')
		except IndexError:
			exhibition = None

	details = details_soup.get_text(' | ').split('|', 1)[1].strip() #reformat details 

	category = None
	style = None

	return (artist_name, title, winning_bid, lo_est, hi_est, auction_name, auction_date, category, style, provenance, exhibition, details)

if __name__ == '__main__':
	LTD_work_link = 'https://www.storyltd.com/auction/item.aspx?eid=3971&lotno=1'
	scrape_each_LTD_work(LTD_work_link)
