from flask import render_template
import connexion
import os
from scraper.scrape.BerlusconiScrape import BerlusconiScrape
import json
from api.scraper import berlusconi_vendor_list as vendor_list

# Create the application instance
app = connexion.App(__name__, specification_dir='./')

# Read the swagger.yml file to configure the endpoints
app.add_api('swagger.yml')


@app.route('/')
def home():
    return "D"

def get_html_pages ():
    path = "../resources/Data/DATA_RAW/2019_09_18/BERLUSCONI/Vendor_pages/"
    
    children = os.listdir(path)

    html_pages = []

    for child in children:
        if (child.endswith("htm" or "html") and child.find("&tab") == -1):
            html_pages.append(os.path.join(os.path.abspath(path), child))
    
    return html_pages

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)

    """html_pages = get_html_pages()
    html_page = html_pages[0]

    print(html_page, "\n")

    name = os.path.splitext(html_page)[0]
    html_tabs = []
    html_tabs.append(html_page)
    html_tabs.append(name + "&tab=2.htm")
    html_tabs.append(name + "&tab=3.htm")
    html_tabs.append(name + "&tab=4.htm")
    
    vendor = vendor_list(html_tabs)

    print(vendor)"""
    
