from bs4 import BeautifulSoup
import requests
from pprint import pprint
import csv

def scrap_listing(page, brand, year_max, year_min, km_min, km_max, energy, price_max, price_min):
    url=f"https://www.lacentrale.fr/listing?energies={energy}&makesModelsCommercialNames={brand}&mileageMax={km_max}&mileageMin={km_min}&page={page}&priceMax={price_max}&priceMin={price_min}&yearMax={year_max}&yearMin={year_min}"
    reponse = requests.get(url)
    print(url) 
    return reponse.text

def lancement():
    brand = "PEUGEOT"
    year_max = 2023
    year_min = 2000
    km_min = 0
    km_max = 100000
    energy = "dies"
    price_min = 11600
    price_max = 81800
    page = 0
    fd = open("liste_voiture.csv", "w")
    csv_writer = csv.writer(fd)
    csv_writer.writerow(['brand', 'model', 'year', 'price', 'fuel', 'mileage', 'motor'])
    while page != 3:
        html_page = scrap_listing(page, brand, year_max, year_min, km_min, km_max, energy, price_max, price_min)
        soup = BeautifulSoup(html_page, 'html.parser')
        for result in soup.find_all('div', 'Vehiculecard_Vehiculecard_cardBody'):
            name_vehicle = result.find('h3').get_text()
            print("nom du véhicule : ", name_vehicle)
            cost = soup.find('span', "Text_Text_text Vehiculecard_Vehiculecard_price Text_Text_subtitle2")
            print("Coût de la voiture : ", cost.get_text())
            final_cost = cost.get_text()
            #années
            data = soup.find_all('div', class_= "Text_Text_text Vehiculecard_Vehiculecard_characteristicsItems Text_Text_body2")[0]
            #kilometrage
            data1 = soup.find_all('div', class_= "Text_Text_text Vehiculecard_Vehiculecard_characteristicsItems Text_Text_body2")[1]
            #carburant
            data2 = soup.find_all('div', class_= "Text_Text_text Vehiculecard_Vehiculecard_characteristicsItems Text_Text_body2")[3]
            data3 = soup.find('div', class_= 'Text_Text_text Vehiculecard_Vehiculecard_subTitle Text_Text_body2')                
            kilometrage = data1.get_text()
            print("années : ", data.get_text())
            print("mileage : ", data1.get_text())
            csv_writer.writerow([brand, name_vehicle.lstrip(brand), data.get_text(), final_cost.rstrip("€"), data2.get_text(), kilometrage.rstrip("km"), data3.get_text()])
        page += 1
    fd.close()

if __name__ == "__main__":
    lancement()
    print("la fonction a bien été lancée")