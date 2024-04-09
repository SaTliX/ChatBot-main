import requests
import json

# Définir les paramètres de recherche
api_key = "API KEY"
headers = {
  'Authorization': 'Bearer %s' % api_key,
}

# Demander au client de saisir les préférences
location = input("Entrez la localisation : ")
cuisine = input("Entrez le type de cuisine : ")
budget = input("Entrez le budget (1 = $, 2 = $$, 3 = $$$, 4 = $$$$) : ")

params = {
  'term': 'restaurant',
  'location': location,
  'category': cuisine,
  'price': budget,
  'limit': 5
}

# Envoyer la requête à l'API Yelp
response = requests.get('https://api.yelp.com/v3/businesses/search', headers=headers, params=params)

# Traiter la réponse JSON
data = response.json()
businesses = data['businesses']

# Afficher les résultats
for business in businesses:
  print(business['name'])
  print(business['location']['address1'])
  print(business['location']['city'])
  print(business['location']['zip_code'])
  print(business['phone'])
  print(business['rating'])
  print(business['price'])
  print()
