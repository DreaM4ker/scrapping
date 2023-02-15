from bs4 import BeautifulSoup
import requests
import csv

def scrap_listing(page, brand, year_max, year_min, km_min, km_max, energy, price_max, price_min, nombre_de_page):
    url=f"https://www.lacentrale.fr/listing?energies={energy}&makesModelsCommercialNames={brand}&mileageMax={km_max}&mileageMin={km_min}&page={page}&priceMax={price_max}&priceMin={price_min}&yearMax={year_max}&yearMin={year_min}"
    reponse = requests.get(url)
    print(url) 
    return reponse.text
'''fonction qui lancera tout le programme'''
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
    nombre_de_page = int(input("rentrez le nombre de page : "))
    """on crée un fichier csv nommé liste_voiture"""
    fd = open("liste_voiture.csv", "w")
    csv_writer = csv.writer(fd)
    '''on écrit nos catégories'''
    csv_writer.writerow(['brand', 'model', 'year', 'price', 'fuel', 'mileage', 'motor'])
    '''On choisit le nombre de page'''
    while page != nombre_de_page:
        html_page = scrap_listing(page, brand, year_max, year_min, km_min, km_max, energy, price_max, price_min, nombre_de_page)
        soup = BeautifulSoup(html_page, 'html.parser')
        for result in soup.find_all('div', 'Vehiculecard_Vehiculecard_cardBody'):
            name_vehicle = result.find('h3').get_text().lstrip(brand)
            cost = soup.find('span', "Text_Text_text Vehiculecard_Vehiculecard_price Text_Text_subtitle2")
            final_cost2 = cost.get_text()
            '''années'''
            year = soup.find_all('div', class_= "Text_Text_text Vehiculecard_Vehiculecard_characteristicsItems Text_Text_body2")[0]
            '''type de carburant'''
            type_fuel = soup.find_all('div', class_= "Text_Text_text Vehiculecard_Vehiculecard_characteristicsItems Text_Text_body2")[3]
            '''moteur du véhicule'''
            motor_name = soup.find('div', class_= 'Text_Text_text Vehiculecard_Vehiculecard_subTitle Text_Text_body2').get_text()             
            '''kilometrage'''
            mileage_car_brut = soup.find_all('div', class_= "Text_Text_text Vehiculecard_Vehiculecard_characteristicsItems Text_Text_body2")[1]
            mileage_car_text = mileage_car_brut.get_text()
            '''permet de transfomer le prix en int en enlevant le symbole euros et les espaces'''
            final_cost = final_cost2.rstrip("€").replace(" ","")
            
            '''permet de transfomer le kilometrage en int en retirant le km et les espaces'''
            mileage_car= mileage_car_text.rstrip("km").replace(" ","")

            csv_writer.writerow([brand, name_vehicle, int(year.get_text()), int(final_cost), type_fuel.get_text(), int(mileage_car), motor_name])
            print("nom du véhicule : ", name_vehicle)
            print("années : ", (year.get_text()))
            print("Coût de la voiture : ", cost.get_text())
            print("kilometrage : ", mileage_car_brut.get_text())
        page += 1
    fd.close()

if __name__ == "__main__":
    lancement()
    print("la fonction a bien été lancée")