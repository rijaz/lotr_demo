from bs4 import BeautifulSoup
import requests, sys, os
import json
import pandas as pd
from collection import Counter

full_dict = {}

base_url = "http://lotr.wikia.com"
char_page_url = "/wiki/Category:Characters"

#Gets the number of characters in the wiki overall
def numberOfCharacters(url):
    url = base_url + url
    print(url)
    response = requests.get(url)
    html = response.text.encode('utf-8')

    soup = BeautifulSoup(html, "html5lib")

    count_section = soup.find('p', {"class": "category-page__total-number"}).text
    total = ''.join([i for i in count_section if i.isdigit()])

    return(total)

#print(numberOfCharacters(char_oage_url))


def getCharacterInfo(name, char_url):
    char_info = {}
    char_info["Name"] = name
    response = requests.get(base_url + char_url)
    html = response.text.encode("utf-8")
    soup = BeautifulSoup(html, "html5lib")
    char_info_section = soup.findAll('div', {"class":"pi-item pi-data pi-item-spacing pi-border-color"})
    for i in char_info_section:
        h3_val = i.find('h3').text
        if h3_val == "Birth" or h3_val == "Death":
            try:
                div_val = i.find('a').text
            except:
                div_val = i.find('div').text
        elif h3_val == "Other Names":
            continue
        else:
            div_val = i.find('div').text

        char_info[h3_val] = div_val
    return(char_info)


def compileCharacters():
    outfile = ('Characters.csv', 'w')
    count = 0
    next_url = base_url + char_page_url

    while(next_url):
        response = requests.get(next_url)
        html = response.text.encode('utf-8')
        soup = BeautifulSoup(html, "html5lib")

        #Get all the "boxes" in the list of characters
        char_sections = soup.findAll('a', {"class":"category-page__member-link"})

        #Extract the character's information
        for char in char_sections:
            count += 1
            print(count)
            char_url = char["href"]
            char_name = char.text
            c_dict = getCharacterInfo(char_name, char_url)
            full_dict[char_url] = c_dict

        #Update the next_ulr to the URL of the next page of characters. Will be None if the current page is the last page.
        try:
            next_url = soup.find('a', {"class":"category-page__pagination-next wds-button wds-is-secondary"})['href']
        except:
            next_url = ""
        print(next_url)

    return(full_dict)

def getRaceCount():
    races = char_df['Race'].tolist()
    race_count = Counter(races)

    return(race_count)


def getAllCharacters():
    dict = compileCharacters()
    char_df = pd.DataFrame.from_dict(full_dict, orient='index')
    #If you want a csv, uncomment line below
    #char_df.to_csv('all_characters')
    return(char_df)

def getElves():
    elves_pd = char_df.loc[char_df['Race'] == 'Elves'].append(char_df.loc[char_df['Race'] =='Elf'])
    #If you want a csv, uncomment line below
    #elves_pd.to_csv('Elves.csv')
    return(elves_pd)

def getDwarves():
    dwarves_pd = char_df.loc[char_df['Race'] == 'Dwarves'].append(char_df.loc[char_df['Race'] =='Dwarf'])
    #If you want a csv, uncomment line below
    #dwarves_pd.to_csv('Dwarves.csv')
    return(dwarf_pd)
