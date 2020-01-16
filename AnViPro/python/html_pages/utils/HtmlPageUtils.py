from html_pages.bean.HtmlPage import HtmlPage
from html_pages.bean.Category import Category
from html_pages.bean.Marketplace import Marketplace
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
                
                pages_code = get_codes(pages)

                # For each code, extract all pages related
                for page_code in pages_code:
                    paths = []

                    for page in pages:
                        if page_code in page:
                            paths.append(join(market_folder_path, page))

                    profile_path = get_profile_path(paths)
                    term_and_condition_path = get_term_and_condition_path(paths)
                    pgp_path = get_pgp_path(paths)
                    feedback_paths = get_feedback_paths(paths)

                    html_page = HtmlPage()
                    html_page.category = category
                    html_page.timestamp = timestamp
                    html_page.marketplace = market
                    html_page.code = page_code
                    html_page.profile_path = profile_path
                    html_page.term_and_condition_path = term_and_condition_path
                    html_page.pgp_path = pgp_path
                    html_page.feedback_paths = feedback_paths

                    html_pages.append(html_page)
    
    return html_pages

def get_codes(pages):
    names = set()

    for page in pages:
        page_without_ext = splitext(page)[0]
        split = page_without_ext.split("&")
        for word in split:
            if "code" in word or "v_id" in word:
                names.add(word.split("=")[1])
    
    return names

def get_profile_path(paths):
    for path in paths:
        path_without_ext = splitext(path)[0]
        split = path_without_ext.split("&")

        # Profile tab: there is no tab in the name
        if len(split) == 3:
            return path

    return None


def get_term_and_condition_path(paths):
    for path in paths:
        path_without_ext = splitext(path)[0]
        split = path_without_ext.split("&")

        # Profile tab: there is no tab in the name
        if len(split) == 4 and split[3] == "tab=2":
            return path

    return None


def get_pgp_path(paths):
    for path in paths:
        path_without_ext = splitext(path)[0]
        split = path_without_ext.split("&")

        if split[1] == "a=vendor" and len(split) == 4 and split[3] == "tab=3":
            return path

    return None


def get_feedback_paths(paths):
    index_list = []
    tmp_feedback_paths = []
    feedback_paths = []

    for path in paths:
        path_without_ext = splitext(path)[0]
        split = path_without_ext.split("&")

        # In this case, for now, there is only one feedback page.
        # So, it's not necessary to handle the case with more pages
        if split[1] == "a=product":
            if len(split) == 4 and split[3] == "tab=3":
                index_list.append(1)
                tmp_feedback_paths.append(path)
        else:
            number_of_page = None

            if len(split) == 4:
                if split[3] == "tab=4":
                    number_of_page = 1
                elif split[3].startswith("tab=4"):
                    number_of_page = int(split[3].split("_")[1])

            elif len(split) == 5 and split[3] == "tab=4":
                number_of_page = int(split[4].split("=")[1])

            if number_of_page is not None:
                index_list.append(number_of_page)
                tmp_feedback_paths.append(path)

    if len(tmp_feedback_paths) == 0:
        return None
    else:
        for i in range(len(index_list)):
            for j in range(len(index_list)):
                if index_list[j] == i+1:
                    feedback_paths.append(tmp_feedback_paths[j])
                    break

    return feedback_paths


