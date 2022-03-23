from pprint import pprint
import re
from bs4 import BeautifulSoup
import requests
import pandas as pd

search_for_all = False      #Boolean to denote if we are searching for all or any "terms"
search_year_range = False   #Boolean to denote if we are searching for year range or single year
ourdate_text = []           #Stores dates in text form
links_array = []            #Array of links for each edition
result = {}
result_one = {}
input_keywords_list = []

def ask_choice_search_type():
    print("Please select :")
    print("     1. All terms are present in the title ")
    print("     2. Any term is present in the title")

    return int(input())

#funtion to set variable for choice of operation
def set_choice_search_type():

    choice = ask_choice_search_type()

    match choice:
        case 1:                                     # 1. All terms are present in the title
            return True
        case 2:
            return False                            # 2. Any term is present in the title
        case _:
            print("Please enter a valid choice!!")
            print("Exiting Now")
            exit()


def ask_choice_year_select():
    print("Please select :")
    print("     1. Year Range ")
    print("     2. Single Year")

    return int(input())

#funtion to set variable for choice of operation
def set_choice_year_select():

    choice = ask_choice_year_select()

    match choice:
        case 1:                                     # 1. All terms are present in the title
            return True
        case 2:
            return False                            # 2. Any term is present in the title
        case _:
            print("Please enter a valid choice!!")
            print("Exiting Now")
            exit()



def set_year_range():
    print("Please enter the year range you wish to search for (separated by space):")
    return str(input())
    
def set_year():
    print("Please enter the year you wish to search for:")
    return str(input())


def set_economist_data(year):

    archive_URL = "https://www.economist.com/weeklyedition/archive?year="

    archive_URL = archive_URL + str(year)

    page = requests.get(archive_URL)

    soup = BeautifulSoup(page.content, "html.parser")

    results = soup.find("div", {"class": "layout-edition-collection"})
    ourdate = results.find_all("time", {"class": "edition-teaser__subheadline"})
    ourdate_links = results.find_all("a", {"class": "headline-link"})

    global ourdate_text           #resetting as empty
    global links_array            #resetting as empty

    links_array = []
    ourdate_text = []

    for link in ourdate_links:
            temp_link = link['href']

            if temp_link[0]=="/":
                temp_link="https://www.economist.com"+temp_link
                links_array.append(temp_link)



    for x in ourdate:
        ourdate_text.append(x.text)
    #print(ourdate_text)


#search for multiple search terms : OR
def search_for_keywords(ifAll):    
    
    global input_keywords_list


    new_issue_dict = {}

    print("Please wait while we go through the editions over the years..")
    print("\n")
    print("\n")

    for index, new_url in enumerate(links_array):

        issue_page= requests.get(new_url)
        new_soup = BeautifulSoup(issue_page.content, "html.parser")
        results_new = new_soup.find("div", {"class": "layout-weekly-edition"})
        link_heads = results_new.find_all("a", {"class": "headline-link"})
        links= []

        for link in link_heads:

            temp_link = link['href']
            if temp_link[0]=="/":
                temp_link="https://www.economist.com"+temp_link

            temp_link_word_list = re.split(', |_|-|/|!', temp_link)
            
            if (ifAll):
                if all(word in temp_link_word_list for word in input_keywords_list):
                    links.append(temp_link)

            else:
                if any(word in temp_link_word_list for word in input_keywords_list):
                    links.append(temp_link)      
               
        #print(ourdate_text[index])   
        #print(links)
        if(links):
            new_issue_dict[ourdate_text[index]] = links

    return new_issue_dict
    

#Program Starts   

result_list = []

print("Welcome to the Economist __ program")
print("\n")
print("\n")

#gets and sets the choice for type of function - keyword searcg
search_for_all = set_choice_search_type()

 #input
input_string = input("Enter keywords to search for separated by space :")
print("\n")
input_keywords_list = input_string.split()

#gets and sets the choice for type of year search
search_year_range = set_choice_year_select()

if(search_year_range):
    input_year_range_string = set_year_range()
    start_year = input_year_range_string.split()[0]
    end_year = input_year_range_string.split()[1]

    year_counter = int(start_year)

    while(year_counter <= int(end_year)):

        set_economist_data(year_counter)
        partial_result = search_for_keywords(search_for_all)

        if(result):
            result.update(partial_result.copy())
            result_list.append(partial_result.copy())
        else:
            result = partial_result.copy()

        year_counter = year_counter + 1

        pprint(result)

else:
    year = set_year()
    set_economist_data(year)
    print("hello")
    #call the scrape function
    result = search_for_keywords(search_for_all)

pprint(result)

df = pd.DataFrame({ key:pd.Series(value) for key, value in result.items() })
print(df)
df_transposed = df.transpose()
df_transposed.to_csv("trial-econ-transposed.csv", encoding='utf-8', index=True)
    
print("Done!!")




