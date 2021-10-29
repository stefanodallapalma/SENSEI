from flask import request, Response, json
import re
import pandas as pd

from database.anita.controller.VendorController import VendorController
from database.db.MySqlDB import MySqlDB


# ENDPOINT
def update_vendors():
    vendor_controller = VendorController()
    data = vendor_controller.get_vendor_filtered()
    data = textual_analysis(data)

    df = pd.DataFrame(data, columns=['timestamp', 'market', 'vendor', 'registration', 'average_review_score', 'email',
                                     'phone number', 'Wickr', 'group/individual', 'other markets'])

    vendor_countries = get_data_countries()

    if not vendor_countries:
        return Response(json.dumps(False), status=200, mimetype="application/json")

    df_countries = pd.DataFrame(vendor_countries, columns=['vendor', 'market', 'ships_from', 'ships_to'])

    df_merged = pd.merge(df, df_countries, how='left', on=['vendor', 'market'])
    df_final = df_merged.where(pd.notnull(df_merged), None)

    final_data = [tuple(x) for x in df_final.to_numpy()]
    insert_data(final_data)

    return Response(json.dumps(True), status=200, mimetype="application/json")


def textual_analysis(sql_output):
    """
    Regular expressions were used to extract the following
    -Email
    -Wickr
    -Phonenumber
    -Active on other markets
    -singular/group
    """
    vendor_plus_re = []
    # The regular expressions
    email = re.compile(r'[a-zA-Z][a-zA-Z0-9_.+-]+@[a-zA-Z0-9.-]+\.[a-z]{3}')
    phonenumber = re.compile(r'(.\d.\d{3}.\d{3}.\d{4})|(..\d{2}.\d{5}[\d]+)')
    wickr = re.compile(r'((wickr|WICKR|Wickr|w.i.c.k.r)(\.|\s|\:|\*)+(\.|\s|\:|\*)+([a-z0-9]+|[A-Z0-9]+)|((wickr|WICKR|'
                       r'Wickr|w.i.c.k.r)\s\w+)(\.|\:|\*)+[a-zA-Z0-9]+|(wickr|WICKR|Wickr|w.i.c.k.r)(\s|\:|\-|\>|\;)(\s'
                       r'|\:|\-|\>|\;)+)[a-z0-9]+|(wickr|WICKR|Wickr|w.i.c.k.r)(\:|\;)[a-zA-Z0-9]+')
    wickr_present = re.compile(r'(wickr|w.i.c.k.r|w1ckr)', re.IGNORECASE)
    sin_group = re.compile(r'( we | our )', re.IGNORECASE)
    other_markets = re.compile(r'(dream market|dreammarket|wall street|silkroad|silk road|empire|dream alt market|'
                               r'dreamaltmarket|samsara|nightmare|appolon|agora|cannazon|pandora|evolution|alpha bay|'
                               r'alphabay|deepbay|dark market|darkmarket|sheep|white house market|whitehousemarket|'
                               r'monopoly|russian market|russianmarket|tochka|berlusconi|big blue|bigblue|vicecity|'
                               r'vice city)', re.IGNORECASE)

    for vendor in sql_output:
        vendor_text = vendor[3]
        # Look for the different identifiers
        email_match = email.search(vendor_text)
        phonenumber_match = phonenumber.search(vendor_text)
        wickr_match = wickr.search(vendor_text)
        sin_group_match = sin_group.search(vendor_text)
        other_markets_match = other_markets.findall(vendor_text)

        # If/else statements to assign the right value to the object
        if email_match != None:
            return_mail = email_match[0]
        else:
            return_mail = ''

        if phonenumber_match != None:
            return_phonenumber = phonenumber_match[0]
        else:
            return_phonenumber = ''

        if sin_group_match != None:
            return_sin_group = 'Group'
        elif vendor_text == '':
            return_sin_group = ''
        else:
            return_sin_group = 'Individual'

        if other_markets_match != []:
            return_other_markets = other_markets_match
            return_other_markets = [x.lower() for x in return_other_markets]
            other_markets_final = []
            for x in return_other_markets:
                # Remove the spaces from all marketnames. As such every marketplace will only appear once
                # e.g 'white house market' and 'whitehousemarket' are the same marketplace, they will now only appear as whitehousemarket
                if ' ' in x:
                    x = x.replace(" ", "")
                if x not in other_markets_final:
                    other_markets_final.append(x)
        else:
            other_markets_final = ''

        if wickr_match != None:
            return_wickr = wickr_match[0]
        else:
            wicker_match_present = wickr_present.search(vendor_text)
            if wicker_match_present != None:
                return_wickr = 'Uses Wickr, check text for username'
            else:
                return_wickr = ''

        # Make sure markets are only returned once
        return_mail = return_mail.split('..')[-1]
        if return_mail.startswith('.') == True:
            return_mail = return_mail[1:]
        if return_wickr == 'Uses Wickr, check text for username' or return_wickr == '':
            pass
        else:
            return_wickr = re.split(' |\*|\.|\:', return_wickr)[-1]
        vendor_plus_re.append(
            vendor[:3] + vendor[4:] + (return_mail,) + (return_phonenumber,) + (return_wickr,) + (return_sin_group,) + (
            str(other_markets_final),) + ())

    return vendor_plus_re


def get_data_countries():
    """
    Import product data to extract where vendors are shipping from/to
    """
    vendor_controller = VendorController()
    vendor_country = vendor_controller.get_vendor_country()

    print(vendor_country)

    if not vendor_country:
        return None

    # Some vendors ships from multiple countries. Therefore, this step is performed to append all countries
    # that are found for a vendor in 1 string.
    vendor_country_clean_temp2 = []
    vendor_country_clean_temp = []
    for record in vendor_country:
        if (record['name']) not in vendor_country_clean_temp2 and record['ships_from'] != None:
            vendor_country_clean_temp2.append((record['name']))
            vendor_country_clean_temp.append(record)
        else:
            for x in vendor_country_clean_temp:
                if x['name'] == record['name']:
                    if record['ships_from'] != None:
                        if record['ships_from'] not in x['ships_from']:
                            x['ships_from'] = x['ships_from'] + ',' + record['ships_from']

    # The 'ships_from' and 'ships_to' fields for vendors are not properly organized. This is fixed here
    vendor_country_clean = []
    for record in vendor_country_clean_temp:
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

    output = [tuple(x.values()) for x in vendor_country_clean]

    return output


def insert_data(data):
    mysql_db = MySqlDB("anita")
    query = "INSERT INTO anita.`vendor-analysis` (`timestamp`, `market`, `name`, `registration_date`, " \
            "`normalized_score`, `email`, `phone number`, `wickr`, `group/individual`, `other markets`, `ships_from`," \
            " `ships_to`) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"

    mysql_db.insert(query, data)
