from html_pages.bean.HtmlPage import HtmlPage
from os import listdir
from os.path import isfile, join, splitext

ext_allowed = ["htm", "html"]

def get_html_pages(folder_path):
    html_pages = []

    # First level: expected 2 subfloders: Product and vendor
    for category in listdir(folder_path):
        category_folder_path = join(folder_path, category)

        # Second level: timestamps
        for timestamp in listdir(category_folder_path):
            timestamp_folder_path = join(category_folder_path, timestamp)

            # Third level: marketplaces
            for market in listdir(timestamp_folder_path):
                pages = []
                market_folder_path = join(timestamp_folder_path, market)

                for page in listdir(market_folder_path):
                    #if splitext(join(market_folder_path, page))[1] in ext_allowed
                    if isfile(join(market_folder_path, page)):
                        # Take the name of this page
                        pages.append(page)
                
                pages_code = extract_pages_name(pages)

                # For each code, extract all pages related
                for page_code in pages_code:
                    for page in pages:
                        if page_code in page:
                            html_path = join(market_folder_path, page)
                            html_page = HtmlPage(category, timestamp, market, page_code, html_path)
                            html_pages.append(html_page)
    
    return html_pages

def extract_pages_name(pages):
    names = set()

    for page in pages:
        page_without_ext = splitext(page)[0]
        split = page_without_ext.split("&")
        for word in split:
            if "code" in word:
                names.add(word.split("=")[1])
    
    return names