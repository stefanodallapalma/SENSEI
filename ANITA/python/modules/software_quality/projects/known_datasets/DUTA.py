import re
from bs4 import BeautifulSoup
import numpy as np

from modules.software_quality.projects.known_datasets import load_csv

known_dataset_path = "../resources/known_datasets/"
folder_name = "Duta"
csv_name = "DUTA_10K.csv"


def get_extra_informations(pages_path):
    duta_dataframe = load_csv(folder_name, delimiter=",")

    print(duta_dataframe)

    duta_dataframe = __extra_features(duta_dataframe, pages_path)

    return duta_dataframe.to_json()


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
    a = ['btc','bitcoin','₿']
    return any(x in text.lower() for x in a)


def __deep_web(url):
    if '.onion' in url:
        return True
    else:
        return False


def __extra_features(dataframe,html_path):
    '''Returns new dataframe with added features. Needs original dataframe and location to html files as input'''
    number_links = []
    max_words = []
    min_words = []
    words = []
    bitcoin = []
    deepweb = []
    for index, row in dataframe.iterrows():
        try:
            onion_address = row['Onion_Address']
            soup = BeautifulSoup(open(r"{}\{}.html".format(html_path,onion_address),encoding='utf-8'), "html.parser")
            all_text = __get_all_text_simple(soup)
            number_links.append(all_text[2])
            site_text = all_text[1]
            max_words.append(__max_min_words_in_sentence(all_text[1])[0])
            min_words.append(__max_min_words_in_sentence(all_text[1])[1])
            words.append(__word_count(all_text[1]))
            bitcoin.append(__detect_bitcoin_transaction(all_text[1]))
            deepweb.append(__deep_web(onion_address))
        except:
            number_links.append(np.nan)
            max_words.append(np.nan)
            min_words.append(np.nan)
            words.append(np.nan)
            bitcoin.append(np.nan)
            deepweb.append(np.nan)
    dataframe['number_links'] = number_links
    dataframe['number_of_words'] = words
    dataframe['min_words_in_sentence'] = min_words
    dataframe['max_words_in_sentence'] = max_words
    dataframe['bitcoin'] = bitcoin
    dataframe['deep_web'] =deepweb
    return dataframe