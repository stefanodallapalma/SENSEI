import datetime
import copy
import re
from flask import request, Response, json
from forex_python.converter import CurrencyRates
from forex_python.bitcoin import BtcConverter
import pandas as pd
import numpy as np

from database.anita.controller.ProductController import ProductController
from database.db.MySqlDB import MySqlDB

drugs_mapping = {
    'Benzodiazepines': ['benzodiazepines', 'klonopin', 'aprazolam', 'alprazolam', 'xanax', 'lorazepam', 'flunitrazolam',
                        'diazepam', 'valium'],
    'Cannabinoids': ['cannabis', 'weed', 'marijuana', 'hash', 'buds', 'bud', 'moonrocks','moonrock','vape','hashish',
                     'edibles', 'indica','concentrates', 'seeds', 'canned-buds'],
    'Stimulants': ['performance', 'cocaine', 'coke','stimulants', 'flakka', 'mdma', 'ecstacy', 'xtc', 'meth',
                   'crystalmeth', 'ice','yaba', 'adderall', 'adderal', 'ecstasy','n-formylamphetamine', 'amphetamine',
                   'iboga'],
    'Opiates/Opioids': ['opiates', 'opioid','heroin', 'herion', 'he-roin', 'he-roine','demerol', 'opana','codeine',
                        'oxycotin', 'oxy', 'oxycotine', 'oxycontin','fentanyl', 'fentany','hydrocodone','oxycodone',
                        'norco', 'methadone', 'roxicodone', 'tramadol', 'opiod', 'opium', 'subutex', 'morphine'],
    'Anabolic steroids': ['steroids', 'testosterone'],
    'Psychedelic/Dissociative Hallucinogens': ['psychedelics', 'dissociatives', 'molly', 'lsd', 'lsd-acid', 'ketamine',
                                               'mushrooms', 'mushroom', 'shrooms', '2cb', 'dmt'],
    'Pharmaceuticals': ['phamaceutical', 'novocain', 'ritalin', 'dexedrine', 'viagra', 'percocet', 'flunitrazepam',
                        'albendazole', 'lyrica', 'lexapro', 'zolpidem', 'temazepam','promethazine','pharmacy',
                        'sidenafil','nasal', 'modafinil', 'nembutal', 'corona', 'vaccine', 'actavis']
}


# ENDPOINT
def update_products():
    product_controller = ProductController()

    data = product_controller.get_product_no_fdb()
    data = ships_processing(data)
    data = convert_price_in_euro(data)

    df = pd.DataFrame(data, columns=['timestamp', 'market', 'name', 'vendor', 'ships_from', 'ships_to', 'category',
                                     'price'])

    # Duplicates are dropped
    df_filtered = df.drop_duplicates(['timestamp', 'name', 'vendor', 'ships_from', 'ships_to', 'category', 'price'],
                                     keep='first')

    df_filtered['macro_category'] = None
    df_filtered = fill_macro_category(df_filtered)

    final_data = [tuple(x) for x in df_filtered.to_numpy()]
    insert_data(final_data)

    return Response(json.dumps(True), status=200, mimetype="application/json")


def delete_all():
    mysql_db = MySqlDB("anita")

    query = "DELETE FROM anita.`products_cleaned`"
    mysql_db.delete(query)

    query = "DELETE FROM anita.`pseudonymized_vendors`"
    mysql_db.delete(query)

    query = "DELETE FROM anita.`reviews`"
    mysql_db.delete(query)

    query = "DELETE FROM anita.`vendor-analysis`"
    mysql_db.delete(query)

    return Response(json.dumps(True), status=200, mimetype="application/json")


def ships_processing(data):
    # The data on shipping countries is not properely formated. That is fixed here
    vendor_country_clean = []
    for record in data:
        if record['ships_from'] == None:
            continue
        if record['ships_to'] == None:
            record['ships_to'] = "Worldwide"
        if record['market'] == 'agartha':
            if record['ships_to'] == "Europe":
                record['ships_to'] = "EU"
            vendor_country_clean.append(record)
        if record['market'] == 'cannazon':
            if 'Worldwide (except US)' in record['ships_to']:
                record['ships_to'] = 'Worldwide (except US)'
            if 'Europe (EU)' in record['ships_to']:
                record['ships_to'] = 'EU (exact location unknown)'
            if record['ships_from'] == 'Europe (EU)':
                record['ships_from'] = 'EU (exact location unknown)'
            if 'Europe (EU)' in record['ships_from'] and 'Europe (EU)' != record['ships_from']:
                record['ships_from'] = record['ships_from'].replace('Europe (EU)', '').replace('|', ',')
                record['ships_from'] = re.sub('\s+', '', record['ships_from'])
                if record['ships_from'].startswith(','):
                    record['ships_from'] = record['ships_from'][1:]
            if '\t' in record['ships_from']:
                record['ships_from'] = re.sub('\s+', '', record['ships_from'])
                record['ships_from'] = record['ships_from'].replace('|', ',')
            if "UnitedKingdom" in record['ships_from']:
                record['ships_from'] = record['ships_from'].replace('UnitedKingdom', 'United Kingdom')
            if ',' in record['ships_from']:
                record['ships_from'] = record['ships_from'].replace(', ', ',')
            if ',' in record['ships_to']:
                record['ships_to'] = record['ships_to'].replace(', ', ',')

        vendor_country_clean.append(record)

    # If a product can be shipped from multiple places, the product record is split up in 2 seperate records.
    # In this fashion this product can be taken in consideration when an analyst filters on a specific country
    vendor_country_clean_seperated = []
    for x in vendor_country_clean:
        if ',' in x['ships_from']:
            list_countries = x['ships_from'].split(',')
            for country in list_countries:
                temp = copy.deepcopy(x)
                temp['ships_from'] = country
                vendor_country_clean_seperated.append(temp)
        else:
            vendor_country_clean_seperated.append(x)

    return vendor_country_clean_seperated


def convert_price_in_euro(data):
    vendor_country_euros = []
    c = CurrencyRates()
    b = BtcConverter()
    for x in data:
        if '€' in x['price'] or 'EUR' in x['price']:
            price = x['price'].strip('EUR').strip('€')
            x_copy = copy.deepcopy(x)
            x_copy['price'] = float(price)
            vendor_country_euros.append(x_copy)
            continue
        if 'USD' in x['price']:
            price_stripped = x['price'].strip('USD')
            convert_date = datetime.datetime.fromtimestamp(int(x['timestamp']))
            price = c.convert('USD', 'EUR', float(price_stripped), convert_date)
            x_copy = copy.deepcopy(x)
            x_copy['price'] = float(price)
            vendor_country_euros.append(x_copy)
            continue
        if 'GBP' in x['price']:
            price_stripped = x['price'].strip('GBP')
            convert_date = datetime.datetime.fromtimestamp(int(x['timestamp']))
            price = c.convert('GBP', 'EUR', float(price_stripped), convert_date)
            x_copy = copy.deepcopy(x)
            x_copy['price'] = float(price)
            vendor_country_euros.append(x_copy)
            continue
        if 'BTC' in x['price']:
            convert_date = datetime.datetime.fromtimestamp(int(x['timestamp']))
            price_stripped = float(x['price'].strip('BTC'))
            if price_stripped > 1:
                price = c.convert('USD', 'EUR', float(price_stripped), convert_date)
                x_copy = copy.deepcopy(x)
                x_copy['price'] = float(price)
                vendor_country_euros.append(x_copy)
                continue
            else:
                price = b.convert_btc_to_cur_on(round(price_stripped, 2), 'EUR', convert_date)
                x_copy = copy.deepcopy(x)
                x_copy['price'] = float(price)
                vendor_country_euros.append(x_copy)

    return vendor_country_euros


def fill_macro_category(df_filtered):
    for i, row in df_filtered.iterrows():
        macro_category_assigned = False
        if row[6]:
            drug_category = row[6].lower()
            for category, drug_list in drugs_mapping.items():
                if drug_category in drug_list:
                    drug_category = category
                    macro_category_assigned = True
            if row[6].lower() == 'pills':
                drug_title_lower = row[2].lower().split(' ')
                drug_title_stripped = [x.strip(',') for x in drug_title_lower]
                drug_title_split = [x.split(',') for x in drug_title_stripped]
                drug_title_split = [x for y in drug_title_split for x in y]
                for key, value in drugs_mapping.items():
                    for word in drug_title_split:
                        if word in value:
                            drug_category = key
                            macro_category_assigned = True
            if macro_category_assigned == True:
                df_filtered.at[i, 'macro_category'] = drug_category

    return df_filtered


def insert_data(data):
    mysql_db = MySqlDB("anita")
    query = "INSERT INTO anita.`products_cleaned` (`timestamp`, `market`, `name`, `vendor`, `ships_from`, `ships_to`," \
            " `category`, `price`, `macro_category`) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)"

    mysql_db.insert(query, data)
