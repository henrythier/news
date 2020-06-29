import datetime

class opener:
    def __init__(self, headline, url, author, resort, subresort, keywords, outlet):
        self.headline = headline
        self.url = url
        self.author = author
        self.resort = resort
        self.subresort = subresort
        self.keywords = keywords
        self.outlet = outlet
        self.tmstmp = datetime.datetime.now()

    def __str__(self):
        return "Headline: {0},\n" \
               "Authors: {1},\n" \
               "Resort: {2},\n" \
               "Subresort: {3},\n" \
               "URL: {4},\n" \
               "Keywords: {5},\n" \
               "Outlet: {6},\n" \
               "Time: {7}".format(self.headline,
                                  self.author,
                                  self.resort,
                                  self.subresort,
                                  self.url,
                                  self.keywords,
                                  self.outlet,
                                  self.tmstmp)