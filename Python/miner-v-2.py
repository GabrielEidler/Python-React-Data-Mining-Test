import requests # for making standard html requests
from bs4 import BeautifulSoup # magical tool for parsing html data
import json # for parsing data
from pandas import DataFrame as df # premier library for data organization

# Syntax: 
""" 
 BeautifulSoup — parsed content
 Tag — standard HTML tag
 NavigableString — string of text within a tag
 Comment — a special type of NavigableString

"""

# Type Of Data retrievals:

""" 
 page.text() for text (most common)
 page.content() for byte-by-byte output
 page.json() for JSON objects
 page.raw() for the raw socket response (extremely complex)
"""

page = requests.get("https://locations.familydollar.com/id/")
soup = BeautifulSoup(page.text, 'html.parser')

# If I want to go beyond english-written websites: 
""" 
 page = requests.get(URL)
 page.encoding = 'ISO-885901'
 soup = BeautifulSoup(page.text, 'html.parser')
"""
# to access a tag saved by bs4, use tag['some_attribute']
# tags children: tag.contents
# access full contents with string: re.compile("my_string"), 
# this way I can avoid navigating the HTML tree


dollar_tree_list = soup.find_all(class_ = 'itemlist')
""" for i in dollar_tree_list[:2]:
  print(i) """

# Analyse type and length

type(dollar_tree_list)
len(dollar_tree_list)

city_hrefs = [] # initialise empty list

for i in dollar_tree_list:
    cont = i.contents[0]
    href = cont['href']
    city_hrefs.append(href)

print("Web addresses")
#  check to be sure all went well
for i in city_hrefs[:2]:
  print(i)

# restart the extraction process on a specific example:

page2 = requests.get(city_hrefs[2]) # again establish a representative example
soup2 = BeautifulSoup(page2.text, 'html.parser')

# after geolocating, use soup.find_all, because it enables type search

arco = soup2.find_all(type="application/ld+json")
print("Json content: ")
print(arco[1])

# indexing list: 

arco_contents = arco[1].contents[0]
arco_contents

# since the format is json, I won't be needing extensive RegEx commands

# officially converting from bs4 to json:

arco_json =  json.loads(arco_contents)
print('Converting bs4 to json: ')
type(arco_json)
print(arco_json)

# getting the nested desired address information: 

arco_address = arco_json['address']
arco_address

# iterating over the parsed content

locs_dict = [] # initialise empty list

for link in city_hrefs:
  locpage = requests.get(link)   # request page info
  locsoup = BeautifulSoup(locpage.text, 'html.parser')
      # parse the page's content
  locinfo = locsoup.find_all(type="application/ld+json")
      # extract specific element
  loccont = locinfo[1].contents[0]  
      # get contents from the bs4 element set
  locjson = json.loads(loccont)  # convert to json
  locaddr = locjson['address'] # get address
  locs_dict.append(locaddr) # add address to list
  


  # cleaning results with pandas
  # basically we convert the data to a "pandas data frame"
  # removing the "@type

locs_df = df.from_records(locs_dict)
locs_df.drop(['@type', 'addressCountry'], axis = 1, inplace = True)
locs_df.head(n = 5)

# saving the results

#df.to_csv(locs_df, "family_dollar_ID_locations.csv", sep = ",", index = False)

result = locs_df.to_json(orient="table")
parsed = json.loads(result)
json.dumps(parsed, indent=4)