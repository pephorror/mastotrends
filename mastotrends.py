### SACA UNA LISTA DE SERVIDORES DE MASTODON Y AGRUPA LOS TAGS POR POPULARIDAD

import requests
from bs4 import BeautifulSoup
import json

# variables
servidores = [] #para guardar la lista de servidores
lista_total = [] #lista total de tags encontrados
result_dict = {} #diccionario de tags agrupados

#########EXTRACT A LIST OF MASTODON SERVERS
# URL where im taking the urls from
url = "https://instances.social/list/old"

# get the html with requests
response = requests.get(url)
html_content = response.text

# BeautifulSoup
soup = BeautifulSoup(html_content, "html.parser")

# Find the html table with the class "table table-sm sortable"
table = soup.find("table", class_="table table-sm sortable")

# Extract table headers
headers = [header.get_text(strip=True) for header in table.find_all("th")]

# save data in list of dictionaries
table_data = []
for row in table.find_all("tr")[1:]:
    row_data = [cell.get_text(strip=True) for cell in row.find_all("td")]
    row_dict = dict(zip(headers, row_data))
    table_data.append(row_dict)

# aux function to get the int value of users or 0 if is not a digit
def get_users(row_dict):
    users_value = row_dict.get('Users', '0')
    return int(users_value) if users_value.isdigit() else 0

# Sort
sorted_data = sorted(table_data, key=get_users, reverse=True)

# Save 50 servers with more users in a list
for row in sorted_data[:80]:
    print(row)
    servidores.append("https://" + row['Instance'])

#########GET THE TRENDS
for serv in servidores:
    try:
        response = requests.get(serv + "/api/v1/trends/tags?limit=20").text
        try:
            objeto = json.loads(response)
            for o in objeto:
                try:
                    lista_total.append([o['name'], o['history'][0]['accounts'], o['history'][0]['uses']])
                except:
                    print("ERROR")
        except:
            print("ErrOR")

    except:
        print("server error")
        
# Group by values (put together same trends from different servers)
for item in lista_total:
    key = item[0].lower()
    value1 = int(item[1])
    value2 = int(item[2])
    if key in result_dict:
        result_dict[key][0] += value1
        result_dict[key][1] += value2
    else:
        result_dict[key] = [value1, value2]
sorted_dict = dict(sorted(result_dict.items(), key=lambda item: item[1][0], reverse=True))

# Convert dictionary to list of lists to print easily
lista_depurada = [[key, value[0], value[1]] for key, value in sorted_dict.items()]
print(lista_depurada)
lista_toot = []
contador_tags = 0
for tag in lista_depurada:
    if contador_tags < 20:
        lista_toot.append(tag)
    contador_tags += 1
for t in lista_toot:
    print("#" + t[0] + " Accounts: " + str(t[1]))# + " Toots: " + str(t[2]))



