import requests
import pandas as pd
import mysql.connector
from mysql.connector import Error
from flask import Flask, render_template, jsonify

def fetch_bike_station_data(base_url, limit=10):
    stations = []  # Liste pour stocker toutes les stations
    offset = 0  # Démarrer à l'offset 0
    
    while True:  # Boucle infinie pour continuer jusqu'à ce qu'il n'y ait plus de résultats
        try:
            # Construire l'URL avec l'offset et la limite
            url = f"{base_url}?f=geojson&offset={offset}&limit={limit}"
            response = requests.get(url)
            response.raise_for_status()  # Vérifier si la requête a réussi
            
            # Analyser la réponse JSON
            data = response.json()
            
            # Extraire les informations des stations de vélos
            features = data.get("features", [])
            
            # Si aucune station n'est trouvée, sortir de la boucle
            if not features:
                break
            
            for feature in features:
                properties = feature.get("properties", {})
                geometry = feature.get("geometry", {}).get("coordinates", [])
                station_data = {
                     "id_station": properties.get("Code_insee"),
                    "commune": properties.get("commune"),
                    "nb_places_dispo": properties.get("nb_places_dispo"),
                    "longitude": geometry[0] if geometry else None,
                    "latitude": geometry[1] if geometry else None,
                }
                stations.append(station_data)

            # Incrémenter l'offset pour la prochaine requête
            offset += limit
            
        except requests.exceptions.RequestException as e:
            print(f"Erreur lors de la récupération des données : {e}")
            return None

    # Créer un DataFrame à partir des données des stations
    df = pd.DataFrame(stations)
    
    return df

# Exemple d'utilisation
base_url = "https://data.lillemetropole.fr/data/ogcapi/collections/vlille_temps_reel/items"
df_stations1 = fetch_bike_station_data(base_url, limit=10)

# Afficher le DataFrame
if df_stations1 is not None:
    print(df_stations1)


def fetch_bike_station_data(base_url, limit=10):
    stations = []  # Liste pour stocker toutes les stations
    offset = 0  # Démarrer à l'offset 0
    total_count = 0  # Compteur pour le nombre total de résultats

    # Récupérer le nombre total de stations
    initial_response = requests.get(base_url)
    initial_response.raise_for_status()  # Vérifier si la requête a réussi
    initial_data = initial_response.json()
    total_count = initial_data.get("total_count", 0)  # Récupérer le total_count
    print(f"Total de stations à récupérer : {total_count}")

    # Boucle pour récupérer toutes les stations
    while offset < total_count:
        try:
            # Construire l'URL avec l'offset et la limite
            url = f"{base_url}?offset={offset}&limit={limit}"
            response = requests.get(url)
            response.raise_for_status()  # Vérifier si la requête a réussi
            
            # Analyser la réponse JSON
            data = response.json()
            results = data.get("results", [])
            
            # Si aucune station n'est trouvée, sortir de la boucle
            if not results:
                break
            
            for station in results:
                station_data = {
                    "id_station": station.get("stationcode"),
                    "commune": station.get("nom_arrondissement_communes"),
                    "nb_places_dispo": station.get("numdocksavailable"),
                    "longitude": station["coordonnees_geo"]["lon"],
                    "latitude": station["coordonnees_geo"]["lat"],
                }
                stations.append(station_data)

            # Incrémenter l'offset pour la prochaine requête
            offset += limit
            
        except requests.exceptions.RequestException as e:
            print(f"Erreur lors de la récupération des données : {e}")
            return None

    # Créer un DataFrame à partir des données des stations
    df = pd.DataFrame(stations)
    
    return df

# Exemple d'utilisation
base_url = "https://opendata.paris.fr/api/explore/v2.1/catalog/datasets/velib-disponibilite-en-temps-reel/records?"  # Remplace cette URL par celle de l'API réelle
df_stations2 = fetch_bike_station_data(base_url, limit=10)

# Afficher le DataFrame
if df_stations2 is not None:
    print(df_stations2)


def fetch_bike_station_data(base_url, limit=10):
    stations = []  # Liste pour stocker toutes les stations
    offset = 0  # Démarrer à l'offset 0
    total_count = 0  # Compteur pour le nombre total de résultats

    # Récupérer le nombre total de stations
    initial_response = requests.get(base_url)
    initial_response.raise_for_status()  # Vérifier si la requête a réussi
    initial_data = initial_response.json()
    total_count = initial_data.get("total_count", 0)  # Récupérer le total_count
    print(f"Total de stations à récupérer : {total_count}")

    # Boucle pour récupérer toutes les stations
    while offset < total_count:
        try:
            # Construire l'URL avec l'offset et la limite
            url = f"{base_url}?offset={offset}&limit={limit}"
            response = requests.get(url)
            response.raise_for_status()  # Vérifier si la requête a réussi
            
            # Analyser la réponse JSON
            data = response.json()
            results = data.get("results", [])
            
            # Si aucune station n'est trouvée, sortir de la boucle
            if not results:
                break
            
            for station in results:
                # Extraire les informations requises
                station_data = {
                    "id_station": station.get("insee"),
                    "commune": station.get("commune"),
                    "nb_places_dispo": station.get("nb_places"),
                    "longitude": station["geo_point_2d"]["lon"],
                    "latitude": station["geo_point_2d"]["lat"],
                }
                stations.append(station_data)

            # Incrémenter l'offset pour la prochaine requête
            offset += limit
            
        except requests.exceptions.RequestException as e:
            print(f"Erreur lors de la récupération des données : {e}")
            return None

    # Créer un DataFrame à partir des données des stations
    df = pd.DataFrame(stations)
    
    return df

# Exemple d'utilisation
base_url = "https://data.toulouse-metropole.fr/api/explore/v2.1/catalog/datasets/stationnement-velo/records" # Remplace cette URL par celle de l'API réelle
df_stations3 = fetch_bike_station_data(base_url, limit=10)

# Afficher le DataFrame
if df_stations3 is not None:
    print(df_stations3)


# Fusionner les DataFrames
bd = pd.concat([df_stations1, df_stations2, df_stations3], ignore_index=True)

# Connexion à MySQL
connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="martine1",
    database="vélo_station"
)

cursor = connection.cursor()

# Requête SQL
insert_query = """
INSERT IGNORE INTO stations (id_station, commune, nb_places_dispo, longitude, latitude)
VALUES (%s, %s, %s, %s, %s)
"""


# Préparation des données
data_to_insert = bd[["id_station", "commune", "nb_places_dispo", "longitude", "latitude"]].values.tolist()

# Insertion dans la base de données
try:
    cursor.executemany(insert_query, data_to_insert)
    connection.commit()
    print(f"{cursor.rowcount} lignes insérées avec succès !")
except mysql.connector.Error as e:
    print(f"Erreur lors de l'insertion des données : {e}")
finally:
    cursor.close()
    connection.close()

app = Flask(__name__)

# Connexion à la base de données MySQL
def get_db_connection():
    connection = mysql.connector.connect(
        host='localhost',
        database='vélo_station',
        user='root',
        password='martine1'
    )
    return connection
@app.route('/')
def index():
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    
    cursor.execute("SELECT * FROM stations")
    stations = cursor.fetchall()
    
    # Debug : Afficher les stations pour vérifier
    print(stations)  # Affiche les données récupérées
    
    return render_template('index.html', stations=stations)


# Route pour récupérer les stations en JSON pour mise à jour en temps réel
@app.route('/get_stations')
def get_stations():
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM stations")
    stations = cursor.fetchall()
    return jsonify(stations)

if __name__ == "__main__":
    app.run(debug=True)
