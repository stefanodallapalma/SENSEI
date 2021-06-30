from flask import Flask, render_template, url_for, flash, redirect, session
from flask_caching import Cache
from flask_mysql_connector import MySQL
from flask_cors import CORS
import json
import logging
import sys
from collections import Counter
from flask import jsonify
import time
import pycountry
import pycountry_convert as pc
import datetime
import collections
import copy
import numpy as np
from flask import Response
import pandas as pd
import re

logging.basicConfig(level=logging.DEBUG)

cache = Cache(config={'CACHE_TYPE': 'simple'})

app = Flask(__name__)
app.secret_key = 'p85d4d1154eb513f4c45a021392dd1fb9ec23aed706a29ac745b3d090285a282b'
# auth = HTTPBasicAuth()
# app.config['SESSION_TYPE'] = 'redis'
# app.config['SESSION_REDIS'] = redis.from_url('redis://:p85d4d1154eb513f4c45a021392dd1fb9ec23aed706a29ac745b3d090285a282b@ec2-34-248-71-23.eu-west-1.compute.amazonaws.com:9620')
app.config['JSON_SORT_KEYS'] = False
cache.init_app(app)

CORS(app)
supports_credentials = True
# app.config['CACHE_TYPE'] = 'simple'
# app.config['MYSQL_HOST'] = 'localhost'
# app.config['MYSQL_USER'] =  'root'
# app.config['MYSQL_PASSWORD'] = 'gfT!-@sayUOO'
# app.config['MYSQL_DATABASE'] = 'anita'

# users = {
#     "john": generate_password_hash("hello"),
#     "susan": generate_password_hash("bye")
# }

app.config['CACHE_TYPE'] = 'simple'
app.config['MYSQL_HOST'] = '0.0.0.0'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'gfT!-@sayUOO'
app.config['MYSQL_DATABASE'] = 'anita'

mysql = MySQL(app)

database_name = "anita"
# conn = mysql.connector.connect(pool_name = "mypool",
#                   pool_size = 6, connection_timeout=3600,
#                   **dbconfig)

# @auth.verify_password
# def verify_password(username, password):
#     if username in users and \
#             check_password_hash(users.get(username), password):
#         return username


###########################################################################################################################


@app.route('/reviews')
@cache.cached(timeout=0)
def reviews():
    # Firstly, retrieve pseudonyms
    conn = mysql.connection
    mycursor = conn.cursor()
    mycursor.execute(f'SELECT * FROM {database_name}.pseudonymized_vendors;')
    row_headers = [x[0] for x in mycursor.description]
    data = mycursor.fetchall()
    mycursor.close()
    data_append = []
    for line in data:
        data_append.append(dict(zip(row_headers, line)))
    vendor_pseudonym = {}
    for record in data_append:
        vendor_pseudonym[record['alias']] = record['pseudonym']

    # Import the actual data
    conn = mysql.connection
    mycursor = conn.cursor()
    mycursor.execute(f'SELECT * FROM {database_name}.reviews;')
    row_headers = [x[0] for x in mycursor.description]
    data = mycursor.fetchall()
    mycursor.close()
    json_data_temp = []
    for line in data:
        json_data_temp.append(dict(zip(row_headers, line)))



    # Pseudonymize the aliases by means of the pseudonyms
    json_data = []
    for to_be_anonymized in json_data_temp:
        for real_name, fake_name in vendor_pseudonym.items():
            if to_be_anonymized['name'] == real_name:
                to_be_anonymized['name'] = fake_name
                json_data.append(to_be_anonymized)

    return {"list": json_data}
    # Perform this second query to retrieve all timestamps of moments that data was collected
    conn = mysql.connection
    mycursor = conn.cursor()
    mycursor.execute(f'SELECT distinct timestamp FROM {database_name}.products_cleaned;')
    row_headers = [x[0] for x in mycursor.description]
    data_timestamps = mycursor.fetchall()
    mycursor.close()
    unique_timestamps = []
    unique_weeks = []
    # These timestamps are transformed into their corresponding week as sales are aggregated per week in the graphs
    for line in data_timestamps:
        unique_timestamps.append(line[0])
        ts = float(line[0])
        year = datetime.datetime.utcfromtimestamp(ts).strftime('%Y')
        weekday = datetime.datetime.fromtimestamp(ts).isocalendar()[1]
        year_week = year + '- week ' + str(weekday)
        if year_week not in unique_weeks:
            unique_weeks.append(year_week)

    # Create lists for all unique vendors, the market the vendors belong to and all unique markets
    unique_vendors = []
    unique_vendors_markets = {}
    unique_markets = []
    for x in json_data:
        if x['name'] not in unique_vendors:
            unique_vendors.append(x['name'])
            unique_vendors_markets[x['name']] = x['market']
        if x['market'] not in unique_markets:
            unique_markets.append(x['market'])

    # For the market agartha, calculate for every week the drugs/non-drugs ratio, which will be used to correct for the
    # review amount above (not all reviews on the agartha market are drugs related)
    markets_ratio = {
        market: {week: {product: 0 for product in ['Drugs', 'No drugs', 'Unknown']} for week in unique_weeks} for market
        in unique_markets}
    for review in json_data:
        if review['market'] != 'cannazon':
            for market, weeks in markets_ratio.items():
                for week, product_types in weeks.items():
                    if review['market'] == market and review['macro_category'] != 'No drugs' and review[
                        'macro_category'] != 'Unknown' and week == datetime.datetime.utcfromtimestamp(
                            float(review['timestamp'])).strftime('%Y') + '- week ' + str(
                            datetime.datetime.fromtimestamp(float(review['timestamp'])).isocalendar()[1]):
                        product_types['Drugs'] += 1
                    if review['market'] == market and review[
                        'macro_category'] == 'No drugs' and week == datetime.datetime.utcfromtimestamp(
                            float(review['timestamp'])).strftime('%Y') + '- week ' + str(
                            datetime.datetime.fromtimestamp(float(review['timestamp'])).isocalendar()[1]):
                        product_types['No drugs'] += 1
                    if review['market'] == market and review[
                        'macro_category'] == 'Unknown' and week == datetime.datetime.utcfromtimestamp(
                            float(review['timestamp'])).strftime('%Y') + '- week ' + str(
                            datetime.datetime.fromtimestamp(float(review['timestamp'])).isocalendar()[1]):
                        product_types['Unknown'] += 1
    for market, weeks in markets_ratio.items():
        if market != 'cannazon':
            for week, product_types in weeks.items():
                drug_nondrug_ratio = product_types['Drugs'] / (product_types['Drugs'] + product_types['No drugs'])
                markets_ratio[market][week] = drug_nondrug_ratio

    # If the market is not cannazon, each vendor will get the amount of reviews attached to his name
    # Thereafter, these will be multiplied by the drug/nondrug ration calculated above
    # The reviews for cannazon include a price, so the price is immediately calculated
    unique_vendors_dict = {vendor: {week: 0 for week in unique_weeks[:-1]} for vendor in unique_vendors}
    for review in json_data:
        if review['market'] != 'cannazon':
            for vendor, weeks in unique_vendors_dict.items():
                for week, amount in weeks.items():
                    if review['name'] == vendor and review['market'] == unique_vendors_markets[
                        vendor] and week == datetime.datetime.utcfromtimestamp(float(review['timestamp'])).strftime(
                            '%Y') + '- week ' + str(
                            datetime.datetime.fromtimestamp(float(review['timestamp'])).isocalendar()[1]):
                        unique_vendors_dict[vendor][week] += 1
        if review['market'] == 'cannazon':
            for vendor, weeks in unique_vendors_dict.items():
                for week, amount in weeks.items():
                    if review['name'] == vendor and review['market'] == unique_vendors_markets[
                        vendor] and week == datetime.datetime.utcfromtimestamp(float(review['timestamp'])).strftime(
                            '%Y') + '- week ' + str(
                            datetime.datetime.fromtimestamp(float(review['timestamp'])).isocalendar()[1]):
                        unique_vendors_dict[vendor][week] += float(review['deals'].strip('€'))
    for vendor, weeks in unique_vendors_dict.items():
        if unique_vendors_markets[vendor] != 'cannazon':
            for week, amount in weeks.items():
                corrected_amount = amount * markets_ratio[unique_vendors_markets[vendor]][week]
                unique_vendors_dict[vendor][week] = corrected_amount

    # This third query is done to determine the average price of the products a vendor offers.
    mycursor = conn.cursor()
    mycursor.execute(f'SELECT * FROM {database_name}.products_cleaned;')
    row_headers = [x[0] for x in mycursor.description]
    data = mycursor.fetchall()
    mycursor.close()
    product_price_data_temp = []
    for line in data:
        product_price_data_temp.append(dict(zip(row_headers, line)))

    # Pseudonymize the aliases by means of the pseudonyms
    product_price_data = []
    for to_be_anonymized in product_price_data_temp:
        for real_name, fake_name in vendor_pseudonym.items():
            if to_be_anonymized['vendor'] == real_name:
                to_be_anonymized['vendor'] = fake_name
                product_price_data.append(to_be_anonymized)

    unique_countries = []

    # For every vendor and a specific week, the average price of the products will be calculated
    vendor_country_week_drugs = {vendor: [] for vendor in unique_vendors}
    for vendor, to_be_replaced in vendor_country_week_drugs.items():
        all_products_vendor = []
        # Collect all products for the vendor
        for product in product_price_data:
            if product['vendor'] == vendor:
                all_products_vendor.append(product)
            if product['ships_from'] not in unique_countries:
                unique_countries.append(product['ships_from'])
        # Determine all unique countries for the vendor
        all_countries_vendor = list(set([product['ships_from'] for product in all_products_vendor]))
        countries_weeks = {country: {week: [] for week in unique_weeks} for country in all_countries_vendor}
        # Place all products under the right country, week combination
        for country, weeks in countries_weeks.items():
            for week, storage in weeks.items():
                for y in all_products_vendor:
                    if y['ships_from'] == country and week == datetime.datetime.utcfromtimestamp(
                            float(y['timestamp'])).strftime('%Y') + '- week ' + str(
                            datetime.datetime.fromtimestamp(float(y['timestamp'])).isocalendar()[1]):
                        countries_weeks[country][week].append(y)
                # For all products that fall within a specific country and week, determine to what category they belong
                new_storage = {}
                for product in storage:
                    if product['macro_category'] == None:
                        del product
                        continue
                    if product['macro_category'] not in new_storage:
                        new_storage[product['macro_category']] = {'quantity': 1, 'all_prices': [product['price']],
                                                                  'average_price': product['price']}
                    else:
                        new_storage[product['macro_category']]['quantity'] += 1
                        new_storage[product['macro_category']]['all_prices'].append(product['price'])
                        new_storage[product['macro_category']]['average_price'] = sum(
                            new_storage[product['macro_category']]['all_prices']) / new_storage[
                                                                                      product['macro_category']][
                                                                                      'quantity']
                countries_weeks[country][week] = new_storage
        vendor_country_week_drugs[vendor] = countries_weeks

    product_page_function_1 = copy.deepcopy(vendor_country_week_drugs)
    # For vendors that ship from multiple countries:
    # the overall sales/reviews will be evenly distributed over the countries and weeks
    for vendor, storing_place in vendor_country_week_drugs.items():
        # For vendors from cannazon, distribute the sales over the countries dependent on the amount of products from each country
        all_sales_vendor = unique_vendors_dict[vendor]
        # Check whether the vendor has sales at all. If he does not, skip him
        if sum(all_sales_vendor.values()) == 0:
            continue
        else:
            storage_to_alter = copy.deepcopy(storing_place)
            for week_sales, sales in all_sales_vendor.items():
                products_sold_week = 0
                # The sales of a week get connected to the products of the week after it.
                next_week = (' ').join(week_sales.split(' ')[:-1]) + ' ' + str(int(week_sales.split(' ')[-1]) + 1)
                for country, weeks in storing_place.items():
                    for week_products, product_categories in weeks.items():
                        if next_week == week_products and product_categories != {}:
                            for product_category, data in product_categories.items():
                                products_sold_week += data['quantity']
                if unique_vendors_markets[vendor] == "cannazon":
                    for country, weeks in storing_place.items():
                        for week_products, product_categories in weeks.items():
                            if week_products == next_week and product_categories != {}:
                                for product_category, data in product_categories.items():
                                    storage_to_alter[country][week_products][product_category]['drug category sales'] = \
                                    data['quantity'] * unique_vendors_dict[vendor][week_sales] / products_sold_week
                else:
                    for country, weeks in storing_place.items():
                        for week_products, product_categories in weeks.items():
                            if week_products == next_week and product_categories != {}:
                                for product_category, data in product_categories.items():
                                    storage_to_alter[country][week_products][product_category]['drug category sales'] = \
                                    data['quantity'] * data['average_price'] * (
                                                unique_vendors_dict[vendor][week_sales] / products_sold_week)

        vendor_country_week_drugs[vendor] = storage_to_alter

    # Remove all vendors, countries, categories and timestamps that do not have sales
    vendor_country_week_drugs_copy = copy.deepcopy(vendor_country_week_drugs)
    for vendor, countries in vendor_country_week_drugs_copy.items():
        if countries == {}:
            del vendor_country_week_drugs[vendor]
            continue
        for country, weeks in countries.items():
            for week, categories in weeks.items():
                for category, data in categories.items():
                    if data == {}:
                        del vendor_country_week_drugs[vendor][country][week][category]
                    elif 'drug category sales' not in data.keys():
                        del vendor_country_week_drugs[vendor][country][week][category]
                    else:
                        vendor_country_week_drugs[vendor][country][week][category] = \
                        vendor_country_week_drugs[vendor][country][week][category]['drug category sales']
                if vendor_country_week_drugs[vendor][country][week] == {}:
                    del vendor_country_week_drugs[vendor][country][week]

    # Since products were mapped to the sales of the previous week, the current week indication is one week off
    # This is corrected here.
    vendor_country_week_drugs_copy = copy.deepcopy(vendor_country_week_drugs)
    for vendor, countries in vendor_country_week_drugs_copy.items():
        for country, weeks in countries.items():
            for week, categories in weeks.items():
                correct_week = (' ').join(week.split(' ')[:-1]) + ' ' + str(int(week.split(' ')[-1]) - 1)
                vendor_country_week_drugs[vendor][country][correct_week] = vendor_country_week_drugs[vendor][
                    country].pop(week)
        if all(p == {} for p in countries.values()) == True:
            del vendor_country_week_drugs[vendor]

    product_page_function_2 = copy.deepcopy(vendor_country_week_drugs)
    # Now the sales per market and the sales per country can be calculated. Above this was done on vendor level.
    # First, calculate the sales per market
    # In case a vendor has reviews, but no products are found, the average product price will be taken for that market
    # Therefore, the average product price for a market for a week is calculated.
    market_week_average_price = {market: {week: [] for week in unique_weeks} for market in unique_markets}
    for product in product_price_data:
        for market, weeks in market_week_average_price.items():
            for week, average_price in weeks.items():
                if product['market'] == market and week == datetime.datetime.utcfromtimestamp(
                        float(product['timestamp'])).strftime('%Y') + '- week ' + str(
                        datetime.datetime.fromtimestamp(float(product['timestamp'])).isocalendar()[1]):
                    market_week_average_price[market][week].append(product['price'])
    for market, weeks in market_week_average_price.items():
        for week, all_prices in weeks.items():
            if all_prices != []:
                average_price = sum(all_prices) / len(all_prices)
                market_week_average_price[market][week] = average_price

    # This average price will be multiplied by the amount of reviews for vendors that have no products linked to them
    # So this is only done for vendors that are not from cannazon and do not have any products found
    for vendor, weeks_reviews in unique_vendors_dict.items():
        if vendor not in vendor_country_week_drugs.keys() and unique_vendors_markets[vendor] != 'cannazon':
            for week, review in weeks_reviews.items():
                for market, weeks_markets in market_week_average_price.items():
                    for week_market, average_price in weeks.items():
                        if market == unique_vendors_markets[vendor] and week_market == week:
                            total_sales = review * average_price
                            unique_vendors_dict[vendor][week] = total_sales

    # In case a vendor is not from the cannazon market but his products are found, replace the reviews amount
    # with the sales from a specific week. In case the vendor has made sales in a specific week, but
    # no product were found that week, this review amount is multiplied by the average price for that week
    for vendor, weeks_reviews in unique_vendors_dict.items():
        if vendor in vendor_country_week_drugs.keys() and unique_vendors_markets[vendor] != 'cannazon':
            weeks_sales = {}
            for countries, weeks in vendor_country_week_drugs[vendor].items():
                for week, drugs in weeks.items():
                    total_sales_week = sum(drugs.values())
                    if week not in weeks_sales.keys():
                        weeks_sales[week] = total_sales_week
                    else:
                        weeks_sales[week] += total_sales_week
            # Now that we have all the sales per week for a vendor, compare it to the review dictionary
            for vendor_vendor, weeks_vendor in unique_vendors_dict.items():
                if vendor_vendor == vendor:
                    for week_vendor, reviews_vendor in weeks_vendor.items():
                        if reviews_vendor == 0:
                            continue
                        # If a vendor does have reviews and products have been found, replace the reviews by the sales
                        if reviews_vendor != 0 and week_vendor in weeks_sales.keys():
                            unique_vendors_dict[vendor][week_vendor] = weeks_sales[week_vendor]
                        # If there are reviews but no products found, multiply the reviews by the average price for the market
                        if reviews_vendor != 0 and week_vendor not in weeks_sales.keys():
                            unique_vendors_dict[vendor][week_vendor] = reviews_vendor * \
                                                                       market_week_average_price[market][week]

    # Calculate the average sales per market throughout the weeks
    markets_total_sales = {market: {week: 0 for week in unique_weeks[:-1]} for market in unique_markets}
    for vendor, weeks_reviews in unique_vendors_dict.items():
        for week, review in weeks_reviews.items():
            for market, weeks_markets in markets_total_sales.items():
                for week_market, review_market in weeks_markets.items():
                    if week == week_market and market == unique_vendors_markets[vendor]:
                        markets_total_sales[unique_vendors_markets[vendor]][week] += review

    final_dict = {country: {week: 0 for week in unique_weeks[:-1]} for country in unique_countries + ['Unknown']}
    final_dict_copy = {country: {week: 0 for week in unique_weeks[:-1]} for country in unique_countries + ['Unknown']}
    # Calculate the average sales per country throughout the weeks
    for vendor, countries_vendor in vendor_country_week_drugs.items():
        for country_vendor, weeks_vendor in countries_vendor.items():
            for week_vendor, drugs_amounts in weeks_vendor.items():
                for drug_type, amount_vendor in drugs_amounts.items():
                    for country, weeks in final_dict.items():
                        for week, amount in weeks.items():
                            if week_vendor == week and country_vendor == country:
                                final_dict[country][week] += amount_vendor
    vendors_unknown = []
    for vendor in unique_vendors:
        if vendor not in vendor_country_week_drugs.keys():
            vendors_unknown.append(vendor)
    for vendor, weeks_vendor in unique_vendors_dict.items():
        if vendor in vendors_unknown:
            for week_vendor, sales_vendor in weeks_vendor.items():
                for week, amount in final_dict['Unknown'].items():
                    if week_vendor == week:
                        final_dict['Unknown'][week] += sales_vendor

    # Now the MAP SVG has to be made. Doing so requires removing "Unknown"
    dates_country_final = {week: {country: 0 for country in unique_countries} for week in unique_weeks[:-1]}
    dates_country_final_copy = {week: {country: 0 for country in unique_countries} for week in unique_weeks[:-1]}
    for country, weeks in final_dict.items():
        for week, sales in weeks.items():
            for week_country, countries in dates_country_final_copy.items():
                for country_country, amount in countries.items():
                    if week == week_country and country == country_country:
                        dates_country_final[week_country][country_country] += sales
    # Delete tags that cannot be converted to their alpha_2 (no actual countries)
    for week, countries in dates_country_final_copy.items():
        for country, sales in countries.items():
            if country == 'EU (exact location unknown)' or country == 'Unknown':
                del dates_country_final[week][country]
    for week, countries in dates_country_final.items():
        new_value = []
        for country, sales in countries.items():
            to_add = {"country": pycountry.countries.get(name=country).alpha_2,
                      "value": sales}
            new_value.append(to_add)
        dates_country_final[week] = new_value

        # Treemap calculations start!
    treemap_sales = {market: {} for market in unique_markets}
    treemap_growth = {market: {} for market in unique_markets}
    for vendor, market in unique_vendors_markets.items():
        for treemap_market, treemap_data in treemap_sales.items():
            if treemap_market == market:
                total_sales_vendor = sum(unique_vendors_dict[vendor].values())
                treemap_data[vendor] = total_sales_vendor

    # Now store the data in the right format for the treemap
    treemap_data = {'name': 'Dark markets',
                    'color': '"hsl(0°, 0%, 100%)"',
                    'children': [
                        {
                            'name': 'agartha',
                            'color': "hsl(0°, 0%, 100%)",
                            'children': []
                        }]}
    treemap_data_cannazon = {

        'name': 'cannazon',
        'color': 'hsl(0°, 0%, 100%)',
        'children': []
    }

    for market, vendors in treemap_sales.items():
        if market == 'agartha':
            for vendor, total_sales in vendors.items():
                data_to_append = {'name': vendor, 'loc': total_sales}
                treemap_data['children'][0]['children'].append(data_to_append)
    for market, vendors in treemap_sales.items():
        if market == 'cannazon':
            for vendor, total_sales in vendors.items():
                data_to_append = {'name': vendor, 'loc': total_sales}
                treemap_data_cannazon['children'].append(data_to_append)
    treemap_data['children'].append(treemap_data_cannazon)

    # Now the growth trajectory for the vendors will be determined. This is done by dividing all the weeks in half
    # and calculating the average weekly sales for each of the two halves. Lastly, these halves will be compared
    # to each other to get a growth rate
    for vendor, market in unique_vendors_markets.items():
        for treemap_market, treemap_d in treemap_growth.items():
            if treemap_market == market:
                all_weeks = list(unique_vendors_dict[vendor].keys())
                weeks_first_half = all_weeks[:len(all_weeks) // 2]
                weeks_second_half = all_weeks[len(all_weeks) // 2:]
                average_sales_first_half = sum(
                    [v for k, v in unique_vendors_dict[vendor].items() if k in weeks_first_half]) / len(
                    weeks_first_half)
                average_sales_second_half = sum(
                    [v for k, v in unique_vendors_dict[vendor].items() if k in weeks_second_half]) / len(
                    weeks_second_half)
                if average_sales_first_half == 0:
                    treemap_d[vendor] = 100
                    continue
                if average_sales_second_half == 0:
                    treemap_d[vendor] = -100
                    continue
                else:
                    growth_rate = ((
                                               average_sales_second_half - average_sales_first_half) / average_sales_first_half) * 100
                    if growth_rate > 200:
                        treemap_d[vendor] = 200
                        continue
                    else:
                        treemap_d[vendor] = growth_rate

                        # Based on the growth percentage, each vendor gets assigned a color
    # The different colours
    colour_palette = {'#ff0000': [50, 99999],
                      '#ff5252': [25, 50],
                      '#ff7b7b': [0, 25],
                      '#FFFFFF': [-0.5, 0.5],
                      '#71c7ec': [-25, -0.5],
                      '#189ad3': [-50, -25],
                      '#005073': [-99999, -50]}
    treemap_growth_copy = copy.deepcopy(treemap_growth)
    for market, vendors in treemap_growth_copy.items():
        for vendor, percentage in vendors.items():
            for colour, range_perc in colour_palette.items():
                if range_perc[0] <= percentage <= range_perc[1]:
                    treemap_growth[market][vendor] = colour
    # This is done to set the background colour of the treemap
    treemap_growth['agartha']['agartha'] = '#FFFFFF'
    treemap_growth['agartha']['Dark markets'] = '#FFFFFF'

    # Lastly, give dict with market, vendor, weeks sales
    market_vendor_weeks_sales = {market: {} for market in unique_markets}
    for vendor, market in unique_vendors_markets.items():
        market_vendor_weeks_sales[market][vendor] = unique_vendors_dict[vendor]

    # Create scatterplot data format, uses the same data as the treemap
    scatterplot_final = []
    colours = {'cannazon': 'rgb(24,154,211)', 'agartha': 'rgb(255,175,122)'}
    # This is the skeleton for the data storage
    general_structure = {
        'label': 'ExampleName',
        'data': [
            {
                'x': -3,
                'y': 7,
                'r': 7
            }
        ],
        'backgroundColor': "",
        'hoverBackgroundColor': ""
    }

    for market, vendors in treemap_sales.items():
        for vendor, total_amount in vendors.items():
            structure_to_add = copy.deepcopy(general_structure)
            structure_to_add['label'] = vendor
            structure_to_add['data'][0]['x'] = total_amount
            structure_to_add['data'][0]['y'] = round(treemap_growth_copy[market][vendor], 2)
            structure_to_add['backgroundColor'] = colours[market]
            structure_to_add['hoverBackgroundColor'] = colours[market]
            scatterplot_final.append(structure_to_add)

    # Structure of the output:
    # 0. Weekly sales vendors
    # 1. Weekly sales markets
    # 2. World map data
    # 3. Weekly sales countries
    # 4. All unique weeks (used to set graph labels)
    # 5. Treemap data
    # 6. Total amount of sales per vendor, on marketplace level
    # 7. Colour code for each vendor (treemap)
    # 8. Weekly sales vendors (per marketplace)
    # 9. Scatterplot data
    # 10. Average product price per vendor
    # 11. Estimated revenue per vendor per drug category
    # 11. Growth rate per vendor (per marketplace)

    return jsonify(unique_vendors_dict, markets_total_sales, dates_country_final, final_dict, unique_weeks[:-1],
                   treemap_data, treemap_sales, treemap_growth, market_vendor_weeks_sales, scatterplot_final,
                   product_page_function_1, product_page_function_2, treemap_growth_copy)


########################################################################################################################################

@app.route('/productpage')
@cache.cached(timeout=0)
def product_page():
    # Firstly, this is the dictionary used to map all products to the same categories. This is based on a mapping made by ANITA:
    # Pills are not known and depend on the type of specific drug mentioned in the title
    drugs_mapping = {'Benzodiazepines': ['benzodiazepines', 'klonopin', 'aprazolam', 'alprazolam', 'xanax', 'lorazepam',
                                         'flunitrazolam', 'diazepam', 'valium'],
                     'Cannabinoids': ['cannabis', 'weed', 'marijuana', 'hash', 'buds', 'bud', 'moonrocks', 'moonrock',
                                      'vape', 'hashish', 'edibles', 'indica', 'concentrates', 'seeds', 'canned-buds'],
                     'Stimulants': ['performance', 'cocaine', 'coke', 'stimulants', 'flakka', 'mdma', 'ecstacy', 'xtc',
                                    'meth', 'crystalmeth', 'ice', 'yaba', 'adderall', 'adderal', 'ecstasy',
                                    'n-formylamphetamine', 'amphetamine', 'iboga'],
                     'Opiates/Opioids': ['opiates', 'opioid', 'heroin', 'herion', 'he-roin', 'he-roine', 'demerol',
                                         'opana', 'codeine', 'oxycotin', 'oxy', 'oxycotine', 'oxycontin', 'fentanyl',
                                         'fentany', 'hydrocodone', 'oxycodone', 'norco', 'methadone', 'roxicodone',
                                         'tramadol', 'opiod', 'opium', 'subutex', 'morphine'],
                     'Anabolic steroids': ['steroids', 'testosterone'],
                     'Psychedelic/Dissociative Hallucinogens': ['psychedelics', 'dissociatives', 'molly', 'lsd',
                                                                'lsd-acid', 'ketamine', 'mushrooms', 'mushroom',
                                                                'shrooms', '2cb', 'dmt'],
                     'Pharmaceuticals': ['phamaceutical', 'novocain', 'ritalin', 'dexedrine', 'viagra', 'percocet',
                                         'flunitrazepam', 'albendazole', 'lyrica', 'lexapro', 'zolpidem', 'temazepam',
                                         'promethazine', 'pharmacy', 'sidenafil', 'nasal', 'modafinil', 'nembutal',
                                         'corona', 'vaccine', 'actavis']}

    # Firstly, retrieve pseudonyms
    mycursor = mysql.new_cursor()
    mycursor.execute(f'SELECT * FROM {database_name}.pseudonymized_vendors;')
    row_headers = [x[0] for x in mycursor.description]
    data = mycursor.fetchall()
    mycursor.close()
    data_append = []
    for line in data:
        data_append.append(dict(zip(row_headers, line)))
    vendor_pseudonym = {}
    for record in data_append:
        vendor_pseudonym[record['alias']] = record['pseudonym']

    # Retrieve all required product data
    mycursor = mysql.new_cursor()
    mycursor.execute(f'SELECT * FROM {database_name}.products_cleaned;')
    row_headers = [x[0] for x in mycursor.description]
    data = mycursor.fetchall()
    mycursor.close()
    json_data_temp = []
    for line in data:
        json_data_temp.append(dict(zip(row_headers, line)))

    # Pseudonymize the aliases by means of the pseudonyms
    json_data = []
    for to_be_anonymized in json_data_temp:
        for real_name, fake_name in vendor_pseudonym.items():
            if to_be_anonymized['vendor'] == real_name:
                to_be_anonymized['vendor'] = fake_name
                json_data.append(to_be_anonymized)

    # Take all unique values for certain attributes. These attributes can be deduced from names below
    unique_weeks = []
    unique_exact_timestamp = []
    unique_dates = []
    unique_countries = []
    unique_vendors = []
    unique_vendors_markets = {}
    unique_markets = []
    for record in json_data:
        if record['vendor'] not in unique_vendors:
            unique_vendors.append(record['vendor'])
            unique_vendors_markets[record['vendor']] = record['market']
        if record['market'] not in unique_markets:
            unique_markets.append(record['market'])
        if record['ships_from'] not in unique_countries:
            unique_countries.append(record['ships_from'])
        if record['timestamp'] not in unique_exact_timestamp:
            unique_exact_timestamp.append(record['timestamp'])
        if datetime.datetime.utcfromtimestamp(float(record['timestamp'])).strftime('%d-%m-%Y') not in unique_dates:
            unique_dates.append(datetime.datetime.utcfromtimestamp(float(record['timestamp'])).strftime('%d-%m-%Y'))
        ts = float(record['timestamp'])
        year = datetime.datetime.utcfromtimestamp(ts).strftime('%Y')
        weekday = datetime.datetime.fromtimestamp(ts).isocalendar()[1]
        year_week = year + '- week ' + str(weekday)
        record['timestamp'] = year_week
        if year_week not in unique_weeks:
            unique_weeks.append(year_week)

    # To ensure similar calculations are not done twice, the results from the 'review' function are importered here!
    # Retrieve the estimated revenue per drug category per vendor + the average product price per vendor
    reviews_data = reviews()
    json_data_reviews = reviews_data.get_json(reviews_data)
    vendor_countries_products_intermediate = json_data_reviews[10]
    vendor_countries_products_intermediate2 = json_data_reviews[10]
    vendor_countries_products = json_data_reviews[11]

    # Create the right skeleton for the final dict and then fill it
    # Structure --> country, drug type, week
    final_dict = {country: {drug: {week: 0 for week in unique_weeks[:-1]} for drug in drugs_mapping.keys()} for country
                  in unique_countries + ['All']}
    final_dict_markets = {
        market: {country: {drug: {week: 0 for week in unique_weeks[:-1]} for drug in drugs_mapping.keys()} for country
                 in unique_countries + ['All']} for market in unique_markets + ['All markets']}
    for vendor, countries in vendor_countries_products.items():
        for country, weeks in countries.items():
            for week, categories in weeks.items():
                for category, amount in categories.items():
                    # final_dict[country][category][week] += amount
                    # Now loop through to the final_dict
                    for country_final, categories_final in final_dict.items():
                        for category_final, weeks_final in categories_final.items():
                            for week_final, amount_final in weeks_final.items():
                                if (
                                        country == country_final or country_final == 'All') and week == week_final and category == category_final:
                                    final_dict[country_final][category_final][week_final] += amount
                    # Do the same for the final_dict_market that is based on marketplaces
                    for market_final_markets, countries_final_markets in final_dict_markets.items():
                        for country_final_markets, categories_final_markets in final_dict.items():
                            for category_final_markets, weeks_final_markets in categories_final_markets.items():
                                for week_final_markets, amount_final_markets in weeks_final_markets.items():
                                    if (
                                            country == country_final_markets or country_final_markets == 'All') and week == week_final_markets and category == category_final_markets and (
                                            unique_vendors_markets[
                                                vendor] == market_final_markets or market_final_markets == 'All markets'):
                                        final_dict_markets[market_final_markets][country_final_markets][
                                            category_final_markets][week_final_markets] += amount
                    # Check if country has no sales at all. In that case, remove it
                    countries_to_remove = []
                    for country_final, categories_final in final_dict.items():
                        country_total = 0
                        for category_final, weeks_final in categories_final.items():
                            for week_final, amount_final in weeks_final.items():
                                country_total += amount_final
                        if country_total == 0:
                            countries_to_remove.append(country_final)
                    # Check if country has no sales at all for final_dict_market. In that case, remove it
                    countries_to_remove_markets = []
                    for market_final_markets, countries_final_markets in final_dict_markets.items():
                        for country_final_markets, categories_final_markets in countries_final_markets.items():
                            country_total = 0
                            for category_final_markets, weeks_final_markets in categories_final_markets.items():
                                for week_final_markets, amount_final_markets in weeks_final_markets.items():
                                    country_total += amount_final_markets
                            if country_total == 0:
                                countries_to_remove_markets.append([market_final_markets, country_final_markets])
    # Remove the countries
    for country in countries_to_remove:
        del final_dict[country]
    # # Remove the countries
    # for country in countries_to_remove_markets:
    #     del final_dict_markets[country[0]][country[1]]

    all_categories = [x for x in drugs_mapping.keys()]
    # For every country, determine the total amount of sales for a week. This is used to determine the height
    # of the graphs.
    vendor_weekly_sales = {country: {week: 0 for week in unique_weeks[:-1]} for country in unique_countries + ['All']}
    for country, categories in final_dict.items():
        for category, weeks in categories.items():
            for week, amount in weeks.items():
                for country2, weeks2 in vendor_weekly_sales.items():
                    for week2, amount2 in weeks2.items():
                        if country == country2 and week == week2:
                            vendor_weekly_sales[country][week] += amount

    vendor_weekly_sales_2 = {vendor: {week: [] for week in unique_dates} for vendor in unique_vendors}
    for vendor, countries in vendor_countries_products_intermediate.items():
        for country, weeks in countries.items():
            for week, categories in weeks.items():
                for category, quantities in categories.items():
                    if quantities != {}:
                        for vendor2, timestamps in vendor_weekly_sales_2.items():
                            for timestamp, data in timestamps.items():
                                if category not in vendor_weekly_sales_2[vendor][
                                    timestamp] and vendor == vendor2 and week == datetime.datetime.utcfromtimestamp(
                                        float(datetime.datetime.strptime(timestamp, '%d-%m-%Y').strftime(
                                                "%s"))).strftime('%Y') + '- week ' + str(
                                        datetime.datetime.fromtimestamp(
                                                float(datetime.datetime.strptime(timestamp, '%d-%m-%Y').strftime(
                                                        "%s"))).isocalendar()[1]):
                                    vendor_weekly_sales_2[vendor][timestamp].append(category)

    # Create the special/generalist dictionary and fill it with data based on the specialist_generalist_data
    specialist_generalist = {
        country: {specialist: {week: {market: [] for market in unique_markets} for week in unique_dates} for specialist
                  in ['Specialist', 'Generalist']} for country in unique_countries + ['All']}
    for vendor, countries in vendor_countries_products_intermediate2.items():
        for country, weeks in countries.items():
            if weeks != {}:
                for week, categories in weeks.items():
                    if categories != {}:
                        all_categories_list = list(categories.keys())
                        # Now add it to the dictionary
                        for country2, specialist_types in specialist_generalist.items():
                            for specialist_type, timestamps in specialist_types.items():
                                for timestamp, markets in timestamps.items():
                                    for market, data_storage in markets.items():
                                        # If a vendor only sells products in 1 category --> specialist
                                        if len(all_categories_list) == 1:
                                            if (country == country2 or country2 == 'All') and market == \
                                                    unique_vendors_markets[
                                                        vendor] and week == datetime.datetime.utcfromtimestamp(
                                                    float(datetime.datetime.strptime(timestamp, '%d-%m-%Y').strftime(
                                                            "%s"))).strftime('%Y') + '- week ' + str(
                                                    datetime.datetime.fromtimestamp(
                                                            float(datetime.datetime.strptime(timestamp,
                                                                                             '%d-%m-%Y').strftime(
                                                                    "%s"))).isocalendar()[1]):
                                                if vendor not in \
                                                        specialist_generalist[country2]['Specialist'][timestamp][
                                                            market]:
                                                    specialist_generalist[country2]['Specialist'][timestamp][
                                                        market].append(vendor)
                                        # If a vendor sells products in multiple categories --> generalist
                                        if len(all_categories_list) > 1:
                                            if (country == country2 or country2 == 'All') and market == \
                                                    unique_vendors_markets[
                                                        vendor] and week == datetime.datetime.utcfromtimestamp(
                                                    float(datetime.datetime.strptime(timestamp, '%d-%m-%Y').strftime(
                                                            "%s"))).strftime('%Y') + '- week ' + str(
                                                    datetime.datetime.fromtimestamp(
                                                            float(datetime.datetime.strptime(timestamp,
                                                                                             '%d-%m-%Y').strftime(
                                                                    "%s"))).isocalendar()[1]):
                                                if vendor not in \
                                                        specialist_generalist[country2]['Generalist'][timestamp][
                                                            market]:
                                                    specialist_generalist[country2]['Generalist'][timestamp][
                                                        market].append(vendor)
    # Structure of the output:
    # 0. Weekly sales per drug category
    # 1. Weekly sales countries (to set height of y-axis)
    # 2. All macro-categories
    # 3. All drug types a vendor sells in a certain week
    # 4. Dictionary with the macro-category - category mapping
    # 5. Specialist/generalist dictionary

    return jsonify(final_dict_markets, vendor_weekly_sales, all_categories, vendor_weekly_sales_2, drugs_mapping,
                   specialist_generalist)


########################################################################################################################################


@app.route('/product')
@cache.cached(timeout=0)
def product_data():
    # Firstly, pseunomize the data
    mycursor = mysql.new_cursor()
    mycursor.execute(f'SELECT * FROM {database_name}.pseudonymized_vendors;')
    row_headers = [x[0] for x in mycursor.description]
    data = mycursor.fetchall()
    data_append = []
    for line in data:
        data_append.append(dict(zip(row_headers, line)))
    vendor_pseudonym = {}
    for record in data_append:
        vendor_pseudonym[record['alias']] = record['pseudonym']

    # Import actual data
    mycursor = mysql.new_cursor()
    mycursor.execute(f"SELECT * FROM {database_name}.products_cleaned;")
    row_headers = [x[0] for x in mycursor.description]
    data = mycursor.fetchall()
    json_data_temp = []
    for line in data:
        json_data_temp.append(dict(zip(row_headers, line)))

    # Pseudonymize the aliases by means of the pseudonyms
    json_data_timestamps = []
    for to_be_anonymized in json_data_temp:
        for real_name, fake_name in vendor_pseudonym.items():
            if to_be_anonymized['vendor'] == real_name:
                to_be_anonymized['vendor'] = fake_name
                json_data_timestamps.append(to_be_anonymized)

    # Timestamps are converted into dates
    json_data = []
    for x in json_data_timestamps:
        date = datetime.datetime.utcfromtimestamp(float(x['timestamp'])).strftime('%d-%m-%Y')
        x['timestamp'] = date
        json_data.append(x)

    # Take all unique countries
    unique_countries_list = []
    for product in json_data:
        if product['ships_from'] not in unique_countries_list:
            unique_countries_list.append(product['ships_from'])
    unique_countries_list.append('All')

    # Take all unique timestamps
    unique_dates_list = []
    for product in json_data:
        if product['timestamp'] not in unique_dates_list:
            unique_dates_list.append(product['timestamp'])

    # Take all unique markets
    unique_markets_list = []
    for product in json_data:
        if product['market'] not in unique_markets_list:
            unique_markets_list.append(product['market'])

    # Create a dictionary with country, timestamp, market and then all the products within that.
    country_timestamp_market = {
        country: {timestamp: {market: [] for market in unique_markets_list} for timestamp in unique_dates_list} for
        country in unique_countries_list}
    temp = {country: {timestamp: {market: [] for market in unique_markets_list} for timestamp in unique_dates_list} for
            country in unique_countries_list}
    for country, timestamps in temp.items():
        for timestamp, markets in timestamps.items():
            for market, storing_place in markets.items():
                # Now loop over original data and insert in the dictionary
                for product in json_data:
                    if product['ships_from'] == country and product['timestamp'] == timestamp and product[
                        'market'] == market:
                        country_timestamp_market[country][timestamp][market].append(product)
                    if product['timestamp'] == timestamp and product['market'] == market:
                        country_timestamp_market['All'][timestamp][market].append(product)

    # Now go through the dictionary and analyze whether vendors target the end consumer, serves as distributor or both
    country_timestap_market_type = {
        country: {timestamp: {market: [] for market in unique_markets_list} for timestamp in unique_dates_list} for
        country in unique_countries_list}
    for country, timestamps in country_timestamp_market.items():
        for timestamp, markets in timestamps.items():
            for market, storing_place in markets.items():
                # Analyse the prices for the various vendors to determine their class
                all_vendors = []
                for product in storing_place:
                    if product['vendor'] not in all_vendors:
                        all_vendors.append(product['vendor'])
                vendor_types = []
                for vendor in all_vendors:
                    all_prices = [x['price'] for x in storing_place if x['vendor'] == vendor]
                    # Distributor class
                    if all(x > 1000 for x in all_prices):
                        vendor_type = [vendor, 'Distributor']
                        vendor_types.append(vendor_type)
                    # End user class
                    elif all(x <= 1000 for x in all_prices):
                        vendor_type = [vendor, 'End user']
                        vendor_types.append(vendor_type)
                    else:
                        # Both class
                        vendor_type = [vendor, 'Both']
                        vendor_types.append(vendor_type)
                country_timestap_market_type[country][timestamp][market] = vendor_types

    # Finally, as we have all the required data, the final data structure can be made and filled
    final_dict = {
        country: {vendor_type: {date: {market: [] for market in unique_markets_list} for date in unique_dates_list} for
                  vendor_type in ['Distributor', 'Both', 'End user']} for country in unique_countries_list}
    for country, timestamps in country_timestap_market_type.items():
        for timestamp, markets in timestamps.items():
            for market, storing_place in markets.items():
                # Now store the vendors on the right place in the final_dict
                for vendor_type in storing_place:
                    if vendor_type[1] == "Distributor":
                        final_dict[country]["Distributor"][timestamp][market].append(vendor_type[0])
                    if vendor_type[1] == "End user":
                        final_dict[country]["End user"][timestamp][market].append(vendor_type[0])
                    if vendor_type[1] == "Both":
                        final_dict[country]["Both"][timestamp][market].append(vendor_type[0])

    # Create dictionary to count max value of chart size for every country.
    # This is done to align the y-axes of the charts
    y_axis_height = {country: {market: {date: 0 for date in unique_dates_list} for market in unique_markets_list} for
                     country in unique_countries_list}
    for country, distributor_endusers in final_dict.items():
        for distributor_enduser, timestamps in distributor_endusers.items():
            for timestamp, markets in timestamps.items():
                for market, vendors in markets.items():
                    for country2, markets2 in y_axis_height.items():
                        for market2, timestamps2 in markets2.items():
                            for timestamp2, count in timestamps2.items():
                                if country == country2 and market == market2 and timestamp == timestamp2:
                                    y_axis_height[country][market][timestamp] += len(vendors)

    # Structure of the output:
    # 0. All unique weeks (to label charts)
    # 1. Dictionary distributor/ end user class
    # 2. Products found per week
    # 3. All unique markets

    return jsonify(unique_dates_list, final_dict, y_axis_height, unique_markets_list)


########################################################################################################################################


@app.route('/nlp')
@cache.cached(timeout=0)
def nlp():
    # Firstly, pseunomize the data
    mycursor = mysql.new_cursor()
    mycursor.execute(f'SELECT * FROM {database_name}.pseudonymized_vendors;')
    row_headers = [x[0] for x in mycursor.description]
    data = mycursor.fetchall()
    data_append = []
    for line in data:
        data_append.append(dict(zip(row_headers, line)))
    vendor_pseudonym = {}
    for record in data_append:
        vendor_pseudonym[record['alias']] = record['pseudonym']

    # 2. Second query is done to retrieve all vendor data
    mycursor = mysql.new_cursor()
    mycursor.execute(
        f"SELECT timestamp,market,name,`group/individual`, ships_from FROM {database_name}.`vendor-analysis`;")
    row_headers = [x[0] for x in mycursor.description]
    data = mycursor.fetchall()
    json_data_temp = []
    for line in data:
        json_data_temp.append(dict(zip(row_headers, line)))

    # Pseudonymize the aliases by means of the pseudonyms
    json_data_timestamps = []
    for to_be_anonymized in json_data_temp:
        for real_name, fake_name in vendor_pseudonym.items():
            if to_be_anonymized['name'] == real_name:
                to_be_anonymized['name'] = fake_name
                json_data_timestamps.append(to_be_anonymized)

    # Timestamps are converted into dates
    json_data = []
    for x in json_data_timestamps:
        date = datetime.datetime.utcfromtimestamp(float(x['timestamp'])).strftime('%d-%m-%Y')
        x['timestamp'] = date
        json_data.append(x)

    # If it turns out a product is shipped from two countries it is broken up into 2 seperate records.
    # In this fashion it can be taken into consideration for both countries
    vendor_country_clean_seperated = []
    for x in json_data:
        if x['ships_from'] == None:
            continue
        elif ',' in x['ships_from']:
            list_countries = x['ships_from'].split(',')
            for country in list_countries:
                temp = copy.deepcopy(x)
                temp['ships_from'] = country
                vendor_country_clean_seperated.append(temp)
        else:
            vendor_country_clean_seperated.append(x)

    # If not containing an empty string, add the label 'unknown' to the data
    good_labelled_data = []
    for vendor in vendor_country_clean_seperated:
        if vendor['group/individual'] != '':
            good_labelled_data.append(vendor)
        else:
            vendor['group/individual'] = 'Unknown'
            good_labelled_data.append(vendor)

    # Take all unique countries
    unique_countries_list = []
    for product in good_labelled_data:
        if product['ships_from'] not in unique_countries_list:
            unique_countries_list.append(product['ships_from'])
    unique_countries_list.append('All')

    # Take all unique timestamps
    unique_dates_list = []
    for product in good_labelled_data:
        if product['timestamp'] not in unique_dates_list:
            unique_dates_list.append(product['timestamp'])

    # Take all unique markets
    unique_markets_list = []
    for product in good_labelled_data:
        if product['market'] not in unique_markets_list:
            unique_markets_list.append(product['market'])

    # Finally, create the empty structure and fill in all the data
    final_dictionary = {
        country: {group: {date: {market: [] for market in unique_markets_list} for date in unique_dates_list} for group
                  in ['Group', 'Individual', 'Unknown']} for country in unique_countries_list}
    for record in good_labelled_data:
        final_dictionary[record['ships_from']][record['group/individual']][record['timestamp']][
            record['market']].append(record['name'])
        if record['name'] not in final_dictionary['All'][record['group/individual']][record['timestamp']][
            record['market']]:
            final_dictionary['All'][record['group/individual']][record['timestamp']][record['market']].append(
                record['name'])

    # Structure of the output:
    # 0. Dictionary group/individual
    # 1. All unique dates

    return jsonify(final_dictionary, unique_dates_list)


########################################################################################################################################

@app.route('/operational')
@cache.cached(timeout=0)
def operational():
    # Firstly, pseunomize the data
    conn = mysql.connection
    mycursor = conn.cursor()
    mycursor.execute(f'SELECT * FROM {database_name}.pseudonymized_vendors;')
    row_headers = [x[0] for x in mycursor.description]
    data = mycursor.fetchall()
    mycursor.close()
    data_append = []
    for line in data:
        data_append.append(dict(zip(row_headers, line)))
    vendor_pseudonym = {}
    for record in data_append:
        vendor_pseudonym[record['alias']] = record['pseudonym']

    # First query is done to retrieve all vendor information
    conn = mysql.connection
    mycursor = conn.cursor()
    mycursor.execute(
        f'SELECT {database_name}.`vendor-analysis`.timestamp, {database_name}.`vendor-analysis`.market, {database_name}.`vendor-analysis`.name, {database_name}.`vendor-analysis`.email, {database_name}.`vendor-analysis`.`phone number`, {database_name}.`vendor-analysis`.wickr, {database_name}.`vendor-analysis`.`group/individual`, {database_name}.`vendor-analysis`.`other markets`,{database_name}.`vendor-analysis`.ships_from,{database_name}.`vendor-analysis`.ships_to, {database_name}.`vendor-analysis`.normalized_score, {database_name}.`vendor-analysis`.registration_date FROM {database_name}.`vendor-analysis`;')
    row_headers = [x[0] for x in mycursor.description]
    data = mycursor.fetchall()
    mycursor.close()
    json_data_start_temp = []
    for line in data:
        json_data_start_temp.append(dict(zip(row_headers, line)))

    # Pseudonymize the aliases by means of the pseudonyms
    json_data_start = []
    for to_be_anonymized in json_data_start_temp:
        for real_name, fake_name in vendor_pseudonym.items():
            if to_be_anonymized['name'] == real_name:
                to_be_anonymized['name'] = fake_name
                json_data_start.append(to_be_anonymized)

    # Any potential duplicates are removed
    df_duplicates = pd.DataFrame(json_data_start,
                                 columns=['timestamp', 'market', 'name', 'email', 'phone number', 'wickr',
                                          'group/individual', 'other markets', 'ships_from', 'ships_to',
                                          'score_normalized', 'registration'])
    df = df_duplicates.drop_duplicates(subset=['timestamp', 'market', 'name'])
    df_none = df.where(pd.notnull(df), "")
    json_data_filtered_timestamps = df_none.to_dict('records')
    # Timestamps are converted into dates
    json_data_filtered = []
    for x in json_data_filtered_timestamps:
        date = datetime.datetime.utcfromtimestamp(float(x['timestamp'])).strftime('%d-%m-%Y')
        x['timestamp'] = date
        json_data_filtered.append(x)

    # Import all import data from the 'review' function!
    # Percentual change is retrieved to determine whether the vendor has increased, decreased or remained the same
    json_data = reviews()
    json_data_final_reviews = json_data.get_json(json_data)
    sales_change = json_data_final_reviews[12]
    temporary_sales = copy.deepcopy(sales_change)
    for market, vendors in temporary_sales.items():
        for vendor, percentage in vendors.items():
            if percentage > 0:
                sales_change[market][vendor] = 'Increased'
            if percentage == 0:
                sales_change[market][vendor] = 'Same/unknown'
            if percentage < 0:
                sales_change[market][vendor] = 'Decreased'
    # Extract all vendors that grow
    all_growing_vendors = []
    for market, vendors in sales_change.items():
        for vendor, percentage in vendors.items():
            if percentage == 'Increased':
                all_growing_vendors.append(vendor)

    # Total size is retrieved to determine whether the vendor is large, medium or small
    # This is done based on percentiles; the biggest 25% are 'big', the smallest 25% are 'small'
    total_sales_categorized = json_data_final_reviews[6]
    total = []
    for x in list(total_sales_categorized.values()):
        total.append(list(x.values()))
    total = [x for y in total for x in y]
    q75, q25 = np.percentile(total, [75, 25])
    temporary = copy.deepcopy(total_sales_categorized)
    for market, vendors in temporary.items():
        for vendor, size in vendors.items():
            if size > q75:
                total_sales_categorized[market][vendor] = 'Large'
            if size >= q25 and size <= q75:
                total_sales_categorized[market][vendor] = 'Medium'
            if size < q25:
                total_sales_categorized[market][vendor] = 'Small'
    # Extract all vendors that are large
    all_large_vendors = []
    for market, vendors in total_sales_categorized.items():
        for vendor, size in vendors.items():
            if size == 'Large':
                all_large_vendors.append(vendor)

    # Append these values to the original data
    final_data = []
    for record in json_data_filtered:
        for vendor, percentage in sales_change[record['market']].items():
            if vendor == record['name']:
                record['percentual_change'] = percentage
        for vendor2, amount in total_sales_categorized[record['market']].items():
            if vendor2 == record['name']:
                record['size'] = amount
        final_data.append(record)
    # Add sales data of past 6 months to final data
    for record in final_data:
        record['Estimated sales since 2021 - week 1'] = 0
        for vendor, amount in temporary[record['market']].items():
            if vendor == record['name']:
                record['Estimated sales since 2021 - week 1'] = round(amount, 2)

    # Return lists with all unique options (used in the front-end)
    sizes = ['Large', 'Medium', 'Small']
    sales = ['Increased', 'Same/unknown', 'Decreased']
    markets = ['agartha', 'cannazon']
    # Get all unique timestamps
    timestamps = []
    vendors = []
    for x in final_data:
        if x['timestamp'] not in timestamps:
            timestamps.append(x['timestamp'])
        if x['name'] not in vendors:
            vendors.append(x['name'])

    # Take all unique countries
    unique_countries = []
    for x in final_data:
        if x['ships_from'] == None or x['ships_from'] == "":
            continue
        if ',' in x['ships_from']:
            list_countries = x['ships_from'].split(',')
            for country in list_countries:
                if country not in unique_countries:
                    unique_countries.append(country)
        else:
            if x['ships_from'] not in unique_countries:
                unique_countries.append(x['ships_from'])

    # Replace personal data with "*"
    final_json_data_vendor_final = []
    for record in final_data:
        record['info'] = '*'
        if record['email'] != "":
            record['email'] = '*'
        if record['phone number'] != '':
            record['phone number'] = '*'
        if record['wickr'] != '':
            record['wickr'] = '*'
        final_json_data_vendor_final.append(record)

    unique_markets = []
    unique_dates = []
    for vendor in final_json_data_vendor_final:
        if vendor['timestamp'] not in unique_dates:
            unique_dates.append(vendor['timestamp'])
        # Get unique markets
        if vendor['market'] not in unique_markets:
            unique_markets.append(vendor['market'])

    ## Create the "shipping point" dictionary for the 'how' page
    shipping_locations = {
        market: {country: {x: {week: [] for week in unique_dates} for x in ['One country', 'Multiple countries']} for
                 country in unique_countries + ['All']} for market in unique_markets + ["All markets"]}
    shipping_locations_copy = {market: {
        country: {x: {week: [] for week in unique_dates} for x in ['One country', 'Multiple countries', 'Unknown']} for
        country in unique_countries + ['All']} for market in unique_markets + ["All markets"]}
    for record in final_json_data_vendor_final:
        if record['ships_from'] != "":
            for market, countries in shipping_locations_copy.items():
                for country, multiples in countries.items():
                    for multiple, weeks in multiples.items():
                        for week, vendors in weeks.items():
                            multiple_single_country = len(record['ships_from'].split(','))
                            if multiple_single_country > 1:
                                # If multiple countries
                                if (country in record['ships_from'].split(',') or country == "All") and (
                                        market == record['market'] or market == "All markets") and week == record[
                                    'timestamp'] and record['name'] not in \
                                        shipping_locations[market][country]['Multiple countries'][week]:
                                    shipping_locations[market][country]['Multiple countries'][week].append(
                                        record['name'])
                                    continue
                            if multiple_single_country == 1:
                                if (country == record['ships_from'] or country == "All") and (
                                        market == record['market'] or market == "All markets") and week == record[
                                    'timestamp'] and record['name'] not in \
                                        shipping_locations[market][country]['One country'][week]:
                                    shipping_locations[market][country]['One country'][week].append(record['name'])
                                    continue

    # To determine the height of the 2 charts in the dashboard, the max values for each country for every date is calculated
    country_values = {country: {week: [] for week in unique_dates} for country in unique_countries + ["All"]}
    for market, countries in shipping_locations.items():
        for country, multiples in countries.items():
            for multiple, weeks in multiples.items():
                for week, vendors in weeks.items():
                    for vendor in vendors:
                        # Now loop through the new dict and append the records
                        for country2, weeks2 in country_values.items():
                            for week2, vendors2 in weeks2.items():
                                if country == country2 and week == week2 and vendor not in vendors2:
                                    country_values[country][week].append(vendor)
    for country, weeks in country_values.items():
        for week, vendors in weeks.items():
            number_of_vendors = len(vendors)
            country_values[country][week] = number_of_vendors

    # Structure of the output:
    # 0. All available weekly data for every vendor. Used in the 'who' page
    # 1. Country values (to set height of y-axis)
    # 2. All unique countries
    # 3. All unique markets
    # 4. All unique dates
    # 5. All large vendors
    # 6. All growing vendors
    # 7. Dictionary shipping from single/multiple countries

    return jsonify(final_json_data_vendor_final, country_values, unique_countries, markets, timestamps,
                   all_large_vendors, all_growing_vendors, shipping_locations)


########################################################################################################################################


@app.route('/rawdata')
@cache.cached(timeout=0)
def raw_data():
    # Firstly  pseunomize the data
    mycursor = mysql.new_cursor()
    mycursor.execute(f'SELECT * FROM {database_name}.pseudonymized_vendors;')
    row_headers = [x[0] for x in mycursor.description]
    data = mycursor.fetchall()
    data_append = []
    for line in data:
        data_append.append(dict(zip(row_headers, line)))
    vendor_pseudonym = {}
    for record in data_append:
        vendor_pseudonym[record['alias']] = record['pseudonym']

    # Import data for the product table
    mycursor = mysql.new_cursor()
    mycursor.execute(f"SELECT * FROM {database_name}.products_cleaned;")
    row_headers = [x[0] for x in mycursor.description]
    data = mycursor.fetchall()
    json_data_product_temp = []
    for line in data:
        json_data_product_temp.append(dict(zip(row_headers, line)))

    # Pseudonymize the aliases by means of the pseudonyms
    json_data_product_timestamps = []
    for to_be_anonymized in json_data_product_temp:
        for real_name, fake_name in vendor_pseudonym.items():
            if to_be_anonymized['vendor'] == real_name:
                to_be_anonymized['vendor'] = fake_name
                json_data_product_timestamps.append(to_be_anonymized)
    # Timestamps are converted into dates
    json_data_product = []
    for x in json_data_product_timestamps:
        date = datetime.datetime.utcfromtimestamp(float(x['timestamp'])).strftime('%d-%m-%Y')
        x['timestamp'] = date
        json_data_product.append(x)

    # This next query is done for the 'review' table
    mycursor = mysql.new_cursor()
    mycursor.execute(f"SELECT message, name, market, product, timestamp FROM {database_name}.reviews;")
    row_headers = [x[0] for x in mycursor.description]
    data = mycursor.fetchall()
    json_data_reviews_temp = []
    for line in data:
        json_data_reviews_temp.append(dict(zip(row_headers, line)))

    # Pseudonymize
    json_data_reviews_timestamps = []
    for to_be_anonymized in json_data_reviews_temp:
        for real_name, fake_name in vendor_pseudonym.items():
            if to_be_anonymized['name'] == real_name:
                to_be_anonymized['name'] = fake_name
                json_data_reviews_timestamps.append(to_be_anonymized)
    # Timestamps are converted into dates
    json_data_reviews = []
    for x in json_data_reviews_timestamps:
        date = datetime.datetime.utcfromtimestamp(float(x['timestamp'])).strftime('%d-%m-%Y')
        x['timestamp'] = date
        json_data_reviews.append(x)

    # Structure of the output:
    # 0. input for the product table
    # 1. Input for review table

    return jsonify(json_data_product, json_data_reviews)


########################################################################################################################################

@app.route('/network')
@cache.cached(timeout=0)
def network_data():
    # Firstly, pseunomize the data
    conn = mysql.connection
    mycursor = conn.cursor()
    mycursor.execute(f'SELECT * FROM {database_name}.pseudonymized_vendors;')
    row_headers = [x[0] for x in mycursor.description]
    data = mycursor.fetchall()
    data_append = []
    for line in data:
        data_append.append(dict(zip(row_headers, line)))
    vendor_pseudonym = {}
    for record in data_append:
        vendor_pseudonym[record['alias']] = record['pseudonym']

    # Import actual data
    mycursor = mysql.new_cursor()
    mycursor.execute(f"SELECT timestamp, market, name, `other markets` FROM {database_name}.`vendor-analysis`")
    row_headers = [x[0] for x in mycursor.description]
    data = mycursor.fetchall()
    json_data_temp = []
    for line in data:
        json_data_temp.append(dict(zip(row_headers, line)))

    # Pseudonymize the aliases by means of the pseudonyms
    json_data_timestamps = []
    for to_be_anonymized in json_data_temp:
        for real_name, fake_name in vendor_pseudonym.items():
            if to_be_anonymized['name'] == real_name:
                to_be_anonymized['name'] = fake_name
                json_data_timestamps.append(to_be_anonymized)


    # Timestamps are converted into dates
    json_data = []
    for x in json_data_timestamps:
        date = datetime.datetime.utcfromtimestamp(float(x['timestamp'])).strftime('%d-%m-%Y')
        x['timestamp'] = date
        json_data.append(x)

    # Take all unique dates and store them in an empty dict
    unique_dates = []
    for x in json_data:
        if x['timestamp'] not in unique_dates:
            unique_dates.append(x['timestamp'])
    timestamp_dict = dict.fromkeys(unique_dates, [])
    # Create copy of empty dict to append all results to
    final_dict = {key: value[:] for key, value in timestamp_dict.items()}

    # Add all records according to their date
    for key, value in timestamp_dict.items():
        for record in json_data:
            if record['timestamp'] == key:
                final_dict[record['timestamp']].append(record)

    # Loop through all the timestamps and add the correct data format to a new dictionary
    timestamp_dict_final = dict.fromkeys(unique_dates, {})
    which_market_final = dict.fromkeys(unique_dates, {})
    which_market_operational_table = dict.fromkeys(unique_dates, {})
    which_market_operational_table_temp = dict.fromkeys(unique_dates, {})

    for timestamp, network_data_input in timestamp_dict_final.items():

        # Create empty JSON with right structure
        right_format = {"nodes": [],
                        "edges": []}

        # All names of the 'other markets' column are taken
        all_markets = []
        for x in final_dict[timestamp]:
            all_markets.append(x['market'])
            if x['other markets'] != '':
                other_markets = x['other markets'].strip('[]')
                other_markets_split = other_markets.split("'")
                for market in other_markets_split:
                    if market != '' and market != ', ':
                        all_markets.append(market)

        market_occurence = Counter(all_markets)
        market_occurence_iterable = market_occurence.most_common()

        # Fill right_format with data from the final dictionary. Only nodes are added at this point, markets are added starting with an index of 9999
        for index, record in enumerate(final_dict[timestamp]):
            node = {'id': index, 'value': 1, 'label': record['name'], 'title': record['name']}
            edge = {'from': index, 'to': record['market']}
            right_format["nodes"].append(node)
            right_format["edges"].append(edge)
        # Add the markets as nodes
        counter = 9999
        for market in market_occurence_iterable:
            right_format["nodes"].append(
                {'id': counter, 'value': market[1], 'label': market[0], 'title': '{} active vendors'.format(market[1]),
                 'color': '#FFFFFF'})
            counter += 1

        # Find out who is present on what market in order to make the 'edge' attribute
        which_market = {}
        for x in final_dict[timestamp]:
            other_markets = x['other markets'].strip('"[]').split(', ')
            clean_other_markets = [x.strip("'") for x in other_markets]
            which_market[x['name']] = [x['market']]
            if clean_other_markets != ['']:
                for market in clean_other_markets:
                    which_market[x['name']].append(market)

        # To be able to make fill the 'edge' object, all names have to be converted to their corresponding id
        name_id_dict = {}
        for row in right_format["nodes"]:
            name_id_dict[row['label']] = row['id']
            # Fill new empty dict with id keys instead of names
        filled_name_id_dict = {}
        for x in which_market:
            for key, value in name_id_dict.items():
                if x == key:
                    filled_name_id_dict[value] = ''
        # Fill the dict values with id's instead of names
        counter = 0
        for x, y in which_market.items():
            id_list = []
            for market in y:
                for key, value in name_id_dict.items():
                    if market == key:
                        id_list.append(value)
            filled_name_id_dict[counter] = id_list
            counter += 1

        # Finally, create a list with edges that can be appended to the old edge list
        edge_list = []
        for key, value in filled_name_id_dict.items():
            for market_id in value:
                edge_list.append({'from': key, 'to': market_id})
        right_format["edges"] = edge_list

        json_right_format = json.dumps(right_format)
        market_right_format = json.dumps(which_market)

        timestamp_dict_final[timestamp] = json_right_format
        which_market_final[timestamp] = market_right_format
        which_market_operational_table[timestamp] = which_market
        which_market_operational_table_temp[timestamp] = which_market

    # Format the 'final_dict' so that it can be used for the network table
    # First create a list with all unique markets that are encountered
    operational_table_data = []
    for timestamp, vendor_info in final_dict.items():
        for vendor in vendor_info:
            if vendor['market'] not in operational_table_data:
                operational_table_data.append(vendor['market'])
            if vendor['other markets'] != '':
                right_format_list = vendor['other markets'].strip('[]')
                right_format_list = right_format_list.split("'")
                right_format_list = [x for x in right_format_list if x != '' and x != ', ']
                for possible_new_market in right_format_list:
                    if possible_new_market not in operational_table_data:
                        operational_table_data.append(possible_new_market)
    # Secondly, create a dictionary structure where all of these markets are named as keys and the values are whether the vendor is present on this market
    operational_table_structure = {key: '' for key in operational_table_data}
    operational_table_structure['name'] = ''
    operational_table_structure_keys = list(operational_table_structure.keys())
    operational_table_structure_keys.insert(0, operational_table_structure_keys.pop())
    # operational_table_structure_keys.insert(0, operational_table_structure_keys.pop(-1))

    for operational_timestamps, operational_vendors in which_market_operational_table_temp.items():
        for operational_vendor, operational_data in operational_vendors.items():
            structure_to_add = copy.deepcopy(operational_table_structure)
            structure_to_add['name'] = operational_vendor
            for present_market in operational_data:
                for k, v in structure_to_add.items():
                    if k == present_market:
                        structure_to_add[k] = 'yes'
            which_market_operational_table[operational_timestamps][operational_vendor] = structure_to_add

    # Transform the data into the right format
    for timestamps, data in which_market_operational_table.items():
        all_data_for_timestamp = []
        for vendor, markets in data.items():
            all_data_for_timestamp.append(markets)
        which_market_operational_table[timestamps] = all_data_for_timestamp

    # Create the dataframe for the multiple/one market graph
    multiple_one_market = {x: {timestamp: 0 for timestamp in unique_dates} for x in ['One market', 'Multiple markets']}
    for timestamp, vendors in which_market_operational_table.items():
        for vendor in vendors:
            amount_of_markets = 0
            for market, presence in vendor.items():
                if presence == "yes":
                    amount_of_markets += 1
            if amount_of_markets == 1:
                multiple_one_market['One market'][timestamp] += 1
            else:
                multiple_one_market['Multiple markets'][timestamp] += 1

    # Structure of the output:
    # 0. All edges
    # 1. All nodes
    # 2. Network table data
    # 3. Network table columns
    # 4. Values for network area graph

    return jsonify(timestamp_dict_final, which_market_final, which_market_operational_table,
                   operational_table_structure_keys, multiple_one_market)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=4000, debug=True, use_reloader=False)

