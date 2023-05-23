from google_patent_scraper import scraper_class
import json

# ~ Initialize scraper class ~ #
scraper=scraper_class()

# ~ Add patents to list ~ #
scraper.add_patents('US20190020496A1')
# scraper.add_patents('US20190020496A1')

# ~ Scrape all patents ~ #
scraper.scrape_all_patents()

# ~ Get results of scrape ~ #
patent_1_parsed = scraper.parsed_patents['US20190020496A1']
# patent_2_parsed = scraper.parsed_patents['US266827A']

print(patent_1_parsed)
# ~ Print inventors of patent US2668287A ~ #
# for inventor in json.loads(patent_1_parsed['inventor_name']):
#   print('Patent inventor : {0}'.format(inventor['inventor_name']))