# News scraping
The code in this repo is used to scrape the headlines of major German media outlets and write them to a database 
in a given frequency. The data points collected are as follows:
* Headline: string that was displayed on top of the article
* URL: link to the article
* Keywords: the keywords found in the article's metadata
* Ressort: section of the newspaper
* Subressort: subsection of the newspaper
* Author(s): people/organisation that has written the article
* Outlet: name of the outlet that published the article
* Timestamp: time the data was collected

## Structure 
Each outlet corresponds to a class with the name *outlet*.py which
initialises an Opener object when its *getopener* method is called.