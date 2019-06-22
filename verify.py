from scrapeEachRegWork import connect
from bs4 import BeautifulSoup as BS
import time 


class VerificationError(Exception):
   pass

def verify(soup, page_type): #see explanation below
	try:
		page_address = ' '.join(soup.find('span', id = 'Header1_smp1').text.split())  
		if page_address != 'Home > ' + page_type:
			raise VerificationError
	except AttributeError:
		raise VerificationError

'''
The website sometimes redirects us to an unexpected page.
This makes our program misbehave and miss some artworks.
Therefore, we need to verify a page by looking at the 'page address'.
If the address doesn't exist or match our page_type, a VerificationError is raised.
'''

def double_verify(invalid_links_file_name, page_type): #see explantion below 
	invalid_links_file = open(invalid_links_file_name, 'r') 
	
	working_links_file_name = invalid_links_file_name.replace('invalid', 'working', 1) 
	
	for line in invalid_links_file: #each line is a link
		link = line.rstrip('\n')
		
		for i in range(3): #each link is verified three times before confirmed as broken
			try:
				soup = BS(connect(link), 'lxml')
				verify(soup, page_type)
				with open(working_links_file_name, 'a') as working_links_file:
					working_links_file.write(link + '\n')
				break
			except VerificationError:
				time.sleep(3)
				continue

	invalid_links_file.close()

'''
We double check the invalid links that have been put into files earlier 
to see that they're actually broken links 
or it's because of the website's inconsistent redirecting.
You may want to do this manually because there're often not many links in each file.  
'''
	

if __name__ == '__main__':
	soup = BS(connect('https://www.saffronart.com/artists/tiffany'), 'lxml')
	try:
		verify(soup, 'Artist')
		print('Verified')
	except VerificationError:
		print('Not Verified')

	#double_verify('invalid-all-works-links.txt', 'Search Results')
	#double_verify('invalid-artist-links.txt', 'Artist')
	
