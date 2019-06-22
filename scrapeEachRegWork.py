from bs4 import BeautifulSoup as BS
import requests
import time 


def connect(link, query = None):  
	while True:
		try: #requesting the page
			return requests.get(link, params = query, cookies = {'UserPref': 'ps=20'}).text
		except requests.exceptions.RequestException as connecting_error: #if there is an error, try reconnecting 
			time.sleep(5) 
			continue

def get_estimates(estimate_text):
	try: #if the 1st estimation is in $
		lo_est = estimate_text[1].split(' - ')[0].split('$')[1]
		hi_est = estimate_text[1].split(' - ')[1]
	except IndexError: 
		lo_est = estimate_text[3].split(' - ')[0].split('$')[1]
		hi_est = estimate_text[3].split(' - ')[1]

	return (lo_est, hi_est)

def get_winning_bid(winning_bid_text): 
	try: #if the 1st winning bid is in $
		winning_bid = winning_bid_text[0].split('$')[1]
	except IndexError:
		winning_bid = winning_bid_text[2].split('$')[1]

	return winning_bid

def get_details(details_list): 
	full_details = ''
	
	for detail in details_list[:-1]:
		detail = ' '.join(' '.join(detail.split('\n')).split())
		full_details += detail + ' | '

	return full_details

def scrape_each_reg_work(reg_work_link): #return each regular work's info 
	reg_work_soup = BS(connect(reg_work_link), 'lxml')

	try:
		auction_info = reg_work_soup.find('div', class_ = 'artworkDetails').p.strong.text 
		#auction info contains the auction's name & date
	except AttributeError:
		with open('invalid-reg-work-links.txt', 'a') as invalid_reg_work_file:
			invalid_reg_work_file.write(reg_work_link + '\n')
		return

	'''
	All works have information about auction name and auction date.
	Therefore, when BS can't find these info (AttributeError raised),
	it means the website has redirected us to an 'invalid' page. 
	To handle this exception, we put the 'bad' links into a file for later checks. 
	'''

	auction_name = auction_info.split('\n')[1].strip() #extract the auction's name from auction info 
	auction_date = auction_info.split('\n')[3].strip() #extract the auction's date from auction info 

	try: #if there are estimates
		estimate_text = reg_work_soup.find('label', id = 'ContentPlaceHolder1_lblEstimates').text.split('\n')
		lo_est, hi_est = get_estimates(estimate_text)
	except AttributeError:
		lo_est, hi_est = None, None

	try: #if there is info about winning bid
		winning_bid_text = reg_work_soup.find('b', class_ = 'wining-text').find_next('strong').text.split('\n')
		winning_bid = get_winning_bid(winning_bid_text)
	except IndexError:
		winning_bid = None

	artist_name = reg_work_soup.find('a', id = 'ContentPlaceHolder1_AboutWork1__ArtistName').text

	title = reg_work_soup.find('span', id = 'ContentPlaceHolder1_AboutWork1_sn_Workdetails').i.text

	details_soup = reg_work_soup.find('span', id = 'ContentPlaceHolder1_AboutWork1_sn_Workdetails').parent 
	#get the parent tag of all the details

	details_list = details_soup.find_all(text = True, recursive = False)

	details = get_details(details_list)

	try: #if there is info about provenance
		provenance = reg_work_soup.find('p', id = 'ContentPlaceHolder1_AboutWork1__Provenance').get_text(' | ')
	except AttributeError:
		provenance = None

	try: #if there is info about exhibition or publication
		exhibition = reg_work_soup.find('p', id = 'ContentPlaceHolder1_AboutWork1__PublishingDesc').get_text(' | ')
	except AttributeError:
		exhibition = None

	category_style = reg_work_soup.find('a', id = 'ContentPlaceHolder1_AboutWork1_TellAFriendLink').parent.find_previous_sibling('p').text

	try: #if there is info about category
		category = category_style.split('Category: ')[1].split('\n')[0].strip() #extract category from category_style
	except IndexError:
		category = None 

	try: #if there is info about style
		style = category_style.split('Style: ')[1].split('\n')[0].strip() #extract style from category_style
	except IndexError:
		style = None

	return (artist_name, title, winning_bid, lo_est, hi_est, auction_name, auction_date, category, style, provenance, exhibition, details)

if __name__ == '__main__':
	reg_work_link = 'https://www.saffronart.com/auctions/DefaultController.aspx?pt=1&l=25889&eid=4037&a=Sir Jacob  Epstein'
	scrape_each_reg_work(reg_work_link)
 	#https://www.saffronart.com/auctions/PostWork.aspx?l=23172
