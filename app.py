from flask import Flask, render_template, request, jsonify, session
import os
import requests

# Crée l'objet Flask
app = Flask(__name__)

# Lit la clé secrète à partir de la variable d'environnement SECRET_KEY
app.secret_key = os.environ.get('SECRET_KEY')

# Clé API Yelp (remplacez par votre propre clé)
YELP_API_KEY = 'API KEY'

# Endpoint pour la page d'accueil
@app.route("/")
def index():
    return render_template('chat.html')  # Rend le fichier chat.html

# Endpoint pour gérer les requêtes de l'utilisateur
@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    user_message = data["message"]

    # Logique de traitement du message de l'utilisateur
    response = process_message(user_message)

    return jsonify({"message": response})

def process_message(message):
    if "ville" in message.lower() and "restaurant" in message.lower():
        # Extrait le nom de la ville de la phrase
        ville = message.split(" ")[message.lower().index("ville") + 1]
        session['ville'] = ville  # Stocke la ville dans la session
        return "Je vais rechercher des restaurants dans cette ville pour vous. Patientez un instant..."
    elif "restaurant" in message.lower():
        return "Désolé, je ne comprends pas. Veuillez préciser votre demande."

    # Requête à l'API Yelp pour obtenir des restaurants dans la ville spécifiée par l'utilisateur
    headers = {
        'Authorization': f'Bearer {YELP_API_KEY}'
    }
    params = {
        'term': 'restaurant',
        'location': session.get('ville', message)  # Utilise la ville stockée dans la session, ou la ville spécifiée dans le message si aucune ville n'est stockée
    }


    try:
        response = requests.get('https://api.yelp.com/v3/businesses/search', headers=headers, params=params)
        data = response.json()

        if response.status_code == 200 and 'businesses' in data:
            # Récupérer les noms des restaurants ou d'autres informations selon vos besoins
            restaurant_names = [restaurant['name'] for restaurant in data['businesses']]
            return f"Voici quelques restaurants à {message}: {', '.join(restaurant_names)}"
        else:
            return "Désolé, je n'ai pas trouvé de restaurants dans cette ville."

    except Exception as e:
        return f"Une erreur s'est produite lors de la recherche des restaurants: {e}"

    return "Désolé, je n'ai pas compris. Pouvez-vous reformuler votre question ?"

if __name__ == '__main__':
    app.run(debug=True)
