from bs4 import BeautifulSoup
from os.path import join
import re

from sonarqube.local.SonarqubeLocalProject import SonarqubeLocalProject
from utils.FileUtils import getfiles


def extra_features(project_name):
    sq_local = SonarqubeLocalProject(project_name)
    parent_path = sq_local.raw_path
    html_files = getfiles(sq_local.raw_path, abs_path=False, ext_filter=("html", "htm"))

    addicts = []

    index = 0
    print("Pages analyzed: 0 of " + str(len(html_files)))
    for html_file in html_files:
        addict = {}
        addict["project_name"] = project_name
        addict["page"] = html_file
        try:
            soup = BeautifulSoup(open(join(parent_path, html_file),encoding='utf-8'), "html.parser")
            all_text = __get_all_text_simple(soup)

            addict["number_links"] = all_text[2]
            addict["number_of_words"] = __word_count(all_text[1])
            addict["min_words_in_sentence"] = __max_min_words_in_sentence(all_text[1])[1]
            addict["max_words_in_sentence"] = __max_min_words_in_sentence(all_text[1])[0]
            addict["bitcoin"] = __detect_bitcoin_transaction(all_text[1])
            addict["deep_web"] = __deep_web(html_file)
        except Exception as e:
            addict["number_links"] = None
            addict["number_of_words"] = None
            addict["min_words_in_sentence"] = None
            addict["max_words_in_sentence"] = None
            addict["bitcoin"] = None
            addict["deep_web"] = None

        addicts.append(addict)
        index += 1
        print("\rPages analyzed: " + str(index) + " of " + str(len(html_files)))

    return addicts


def __get_all_text_simple(soup):
    '''Retrieve all the text from a soup object'''
    number_found_links = 0
    potential_urls = []
    # Find all reference links on webpage and count them
    for link in soup.find_all('a'):
        number_found_links += 1

    # kill all script and style elements
    for script in soup(["script", "style"]):
        script.decompose()  # rip it out

    # get text
    text = re.sub('\s+', ' ', soup.get_text())

    # break into lines and remove leading and trailing space on each
    lines = (line.strip() for line in text.splitlines())
    # break multi-headlines into a line each
    chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
    # drop blank lines
    text = '\n'.join(chunk for chunk in chunks if chunk)
    try:
        header = soup.title.string
        return [header, text, number_found_links]
    except:
        return ['No title', text, number_found_links]


def __max_min_words_in_sentence(paragraph):
    '''Returns maximum and minimun sentence length of a provided text'''
    numWords = [len(sentence.split()) for sentence in paragraph.split('.')]
    return max(numWords), min(numWords)


def __word_count(paragraph):
    '''Returns the ammount of words in a paragraph of text'''
    num_words = sum([len(sentence.split()) for sentence in paragraph.split('.')])
    return num_words


def __detect_bitcoin_transaction(text):
    '''Returns boolean if there are bitcoins in a paragraph of text'''
    a = ['btc', 'bitcoin', '₿']
    return any(x in text.lower() for x in a)


def __deep_web(url):
    if '.onion' in url:
        return True
    else:
        return False
