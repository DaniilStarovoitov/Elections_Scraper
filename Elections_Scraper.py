"""
projekt_3.py: třetí projekt do Engeto Online Python Akademie
author: Daniil Starovoitov
email: daniil.s@seznam.cz
discord: Scorched_Earth#6256
"""
import sys
import csv
import requests
from bs4 import BeautifulSoup


def check_num_of_args():
    if len(sys.argv) != 3:
        print(f'only 2 args')
        quit()


def check_first_arg():
    district_url = []
    html = get_soup('https://www.volby.cz/pls/ps2017nss/ps3?xjazyk=CZ')
    for i in range(15):
        district_url_soup = html.find_all('td', headers= f't{i}sa3')
        for dis in district_url_soup:
            dis = dis.a['href']
            district_url.append(f'https://www.volby.cz/pls/ps2017nss/{dis}')

    if link not in district_url:
        print(f'Wrong town link')
        print(f'Choose from here: https://www.volby.cz/pls/ps2017nss/ps3?xjazyk=CZ')
        quit()


def check_second_arg():
    if file_name() != file:
        print(f'Wronge CSV file name')
        print(f'Must be in format: "results_<district_name>.csv"')
        quit()


def file_name():
    region_name = get_soup(link).find('div', {'class': 'topline'}).find_all('h3')[1].text.strip().lstrip('Okres: ')
    return(f'results_{region_name}.csv')


def get_soup(l):
    while True:
        try:
            response = requests.get(l)
            soup = BeautifulSoup(response.text, 'html.parser')
            print(f'Link "{l}": success')
            return soup
        except requests.exceptions.ConnectionError:
            print(f'Link "{l}": lost connection, new attempt')


def get_code():
    code = []
    html = get_soup(link)
    code_soup = html.find_all('td', 'cislo')
    for c in code_soup:
        code.append(c.text)
    return code


def get_location():
    location = []
    html = get_soup(link)
    code_soup = html.find_all('td', {'class': 'overflow_name'})
    for c in code_soup:
        location.append(c.text)
    return location


def get_location_url():
    location_url = []
    html = get_soup(link)
    location_soup = html.find_all('td', 'cislo')
    for loc in location_soup:
        loc = loc.a['href']
        location_url.append(f'https://volby.cz/pls/ps2017nss/{loc}')
    return location_url


def get_registered_voters():
    voters = []
    url = get_location_url()
    for u in url:
        numbers = get_soup(u).find_all('td', headers='sa2')
        for n in numbers:
            n = n.text
            voters.append(n.replace('\xa0', ' '))
    return(voters)


def get_envelopes():
    envelopes = []
    url = get_location_url()
    for u in url:
        numbers = get_soup(u).find_all('td', headers='sa3')
        for n in numbers:
            n = n.text
            envelopes.append(n.replace('\xa0', ' '))
    return(envelopes)


def get_valid_votes():
    valid_votes = []
    url = get_location_url()
    for u in url:
        numbers = get_soup(u).find_all('td', headers='sa6')
        for n in numbers:
            n = n.text
            valid_votes.append(n.replace('\xa0', ' '))
    return(valid_votes)


def get_parties():
    parties = []
    url = get_location_url()
    party_names = get_soup(url[0]).find_all("td", "overflow_name")
    for party_name in party_names:
        parties.append(party_name.text)
    return parties


def get_party_votes():
    party_votes = []
    url = get_location_url()
    for u in url:
        numbers = get_soup(u).find_all('td', headers=['t1sb3', 't2sb3'])
        lol = []
        for n in numbers:
            n = n.text
            lol.append(n.replace('\xa0', ' '))
        try:
            lol.remove('-')
        except:
            ValueError
        party_votes.append(lol)
    return party_votes


def get_csv():
    code = get_code()
    location = get_location()
    registered_voters = get_registered_voters()
    envelopes = get_envelopes()
    valid_votes = get_valid_votes()
    party_votes = get_party_votes()
    table_rows = []

    zip_one = list(zip(code, location, registered_voters, envelopes, valid_votes))

    zip_two = zip(zip_one, party_votes)
    for z, p in zip_two:
        table_rows.append(list(z) + p)

    header = ['code', 'location', 'registered', 'envelopes', 'valid']
    parties = get_parties()
    for p in parties:
        header.append(p)

    with open(file_name(), 'w', newline='', encoding='utf-8') as f:
        f_writer = csv.writer(f)
        f_writer.writerow(header)
        for kek in table_rows:
            f_writer.writerow(kek)
    print(80 * '-')
    print(f'Data from "{link}" has been downloaded and written to "{file}"')
       

if __name__ == '__main__':
    link = sys.argv[1]
    file = sys.argv[2]

    check_first_arg()
    check_num_of_args()
    check_second_arg()
    get_csv()