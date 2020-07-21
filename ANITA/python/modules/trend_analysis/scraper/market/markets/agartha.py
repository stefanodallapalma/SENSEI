from .scraper import Scraper, ProductScraper, VendorScraper


class AgarthaScraper(Scraper):
    def __init__(self):
        self.product_scraper = AgarthaProductScraper()
        self.vendor_scraper = AgarthaVendorScraper()

    def pagetype(self, soup):
        """Define how to distinguish vendor pages from product pages"""
        try:
            if soup.find_all('a', {'class': 'btn btn-link btn-xs'})[1].text == 'Listings':
                return 'product'
        except:
            pass

        try:
            if soup.find('span', {'class': 'user-class-hint'}).find('strong').text == 'Vendor':
                return 'vendor'
        except:
            pass

        raise Exception("Unknown type")


class AgarthaProductScraper(ProductScraper):
    def product_name(self):
        return self.soup.find('h2').text

    def vendor(self):
        return self.soup.find('div', {'class' : 'panel-body'}).find('a').text

    def ships_from(self):
        for item in self.soup.find_all('p'):
            if 'Ships From: ' in item.text:
                ship_from = item
                for b in ship_from('b'):
                    b.decompose()
                return ' '.join(ship_from.text.split())

    def ships_to(self):
        for item in self.soup.find_all('p'):
            if 'Ships To: ' in item.text:
                ship_from = item
                for b in ship_from('b'):
                    b.decompose()
                return ship_from.text.split()[0]

    def price(self):
        return ' '.join(self.soup.find('span', {'style' : 'font-size:95%;'}).text.split()[1:3])

    def info(self):
        return self.soup.find('p', {'style' : 'max-width:74%; width:auto; overflow:auto; word-wrap: break-word; text-overflow: ellipsis;'}).text

    def feedback(self):
        """ NONE IN DATASET, THUS ALL NONE"""
        feedback_list = None
        return feedback_list


class AgarthaVendorScraper(VendorScraper):
    def vendor_name(self):
        return self.soup.find_all('a', {'class' : 'btn btn-link btn-xs'})[1].text

    def score(self):
        return (float(self.soup.find('div', {'style' : 'margin: 0px 20px;'}).find('span').text.split()[1]),100)

    def registration(self):
        time = self.soup.find_all('div', {'class': 'vendorbio-stats-online'})[0]
        for item in time('span'):
            item.decompose()
        return ' '.join(time.text.split()).split('.')[0]

    def last_login(self):
        time = self.soup.find_all('div', {'class': 'vendorbio-stats-online'})[0]
        for item in time('span'):
            item.decompose()
        return ' '.join(time.text.split()).split('.')[1]

    def sales(self):
        return ' '.join(self.soup.find_all('span', {'class' : 'gen-user-ratings'})[1].text.split()[2:3])

    def info(self):
        # example: return soup.find('div', {'class' : 'container container_large'}).text
        return self.soup.find('p', {'style': 'word-wrap: break-word; text-overflow: ellipsis;'}).text

    def feedback(self):
        feedback_list = []

        # loop to walk through the feedback
        for item in self.soup.find('div', {'class': 'embedded-feedback-list'}).find('tbody').find_all('tr'):
            # Find the score, can be numerical score: (score, scale), or 'positive', 'negative' or 'neutral' for pos/neg scores.
            score = (int(item('td')[0].text[0]), 5)

            # The message of the feedback in type str
            message = item('td')[1].text

            # The time in datetime object or time ago in type str
            date = item('td')[3].text

            # Name of the product that the feedback is about (if any) in type str
            product = ' '.join(item('td')[2].text.split())

            # User, name of the user or encrypted user name (if any) in type str
            user = item('td')[4].text.split()[0]

            # Deals by user (if any) in type int or str (if range)
            deals = ' '.join(item('td')[4].text.split()[-4:])

            # in json format
            feedback_json = {
                'score': score,
                'message': message,
                'date': date,
                'product': product,
                'user': user,
                'deals': deals
            }
            feedback_list.append(feedback_json)

        return feedback_list
