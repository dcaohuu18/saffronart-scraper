from scrapeEachArtist import scrape_each_artist
from selenium import webdriver


driver = webdriver.Firefox()

driver.get('https://www.saffronart.com/Artist/ArtistList.aspx/')

num_of_pages = int(driver.find_element_by_id('ContentPlaceHolder1_PagingLinks1_rptPagingLinks_lbPagingFooter').text) 
#get the number of pages 

for page in range(num_of_pages): #go through every page 
	profile_list = driver.find_elements_by_link_text('Profile') 
	
	for profile in profile_list: #go through every artist profile in the page
		profile_link = profile.get_attribute('href')
		scrape_each_artist(profile_link)

	driver.execute_script("scroll(0, 1050)") #scroll down to the 'Next' button
		
	next_page = driver.find_element_by_id('ContentPlaceHolder1_lnkNext')

	next_page.click()

driver.close()
driver.quit()