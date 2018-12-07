from bs4 import BeautifulSoup
from multiprocessing import Pool, Process
import requests
import pandas as pd
import numpy as np
def _create_dataframe(citylist):
 return  pd.DataFrame(columns=citylist)

def getDistanceBetweenTwoCities(citylist,df):
  city_distance_dict = {}
  for c in range(len(citylist)):
    from_city = citylist[c]
    to_ct_str = '|'.join(map(str,citylist))
    url = "https://maps.googleapis.com/maps/api/distancematrix/json?units=metrics&origins=" + from_city + "&destinations=" + to_ct_str +"&key=AIzaSyBIU_Fr0S5WghNCCOT_7rrBo3NXGHi_MvQ"
    r = requests.get(url)
    for i in range(len(r.json()["destination_addresses"]) -1):
      if r.json()["rows"][0]["elements"][i]["status"] == 'OK':
        city_distance_dict[r.json()["destination_addresses"][i]]= r.json()["rows"][0]["elements"][i]["distance"]["value"]
      else:
      	city_distance_dict[r.json()["destination_addresses"][i]] = np.nan
    df = df.append(city_distance_dict, ignore_index=True)


  df = df.set_index(citylist)
  return df

def getTopCities(number):
  r = requests.get("https://www.insee.fr/fr/statistiques/1906659?sommaire=1906743")
  citiesList = []
  soup = BeautifulSoup(r.text,'html.parser')
  for i in range(1,number):
    citiesList.append(soup.table.findAll('tr')[i].findAll('th')[1].text)
  return citiesList
def main():
  ct_lst = getTopCities(10)
  ct_df = _create_dataframe(ct_lst)
  print(getDistanceBetweenTwoCities(ct_lst,ct_df))
if __name__ == '__main__':
  main()

