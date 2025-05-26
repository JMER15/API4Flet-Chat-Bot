from openai import OpenAI
import requests
from dotenv import load_dotenv
import os
import json

# cargar variables de entorno
load_dotenv()

# Variables de entorno
client = OpenAI(api_key=os.getenv("OPENROUTER_API_KEY"), base_url='https://openrouter.ai/api/v1')
WHEATHER_API_KEY = os.getenv("OPENWHEATHER_API_KEY")

def translate_text(description):
    match description:
        case "clear sky": description = "cielo despejado"
        case "few clouds": description = "pocas nubes"
        case "scattered clouds": description = "nubes dispersas"
        case "broken clouds": description = "nubes rotas"
        case "shower rain": description = "lluvia ligera"
        case "rain": description = "lluvia"
        case "thunderstorm": description = "tormenta eléctrica"
        case "snow": description = "nieve"
        case "mist": description = "neblina"
    return description

def get_weather(city):
    try:
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={WHEATHER_API_KEY}&units=metric"
        response = requests.get(url)

        if response.status_code == 200:
            data = response.json()
            temperature = data["main"]["temp"]
            description = data["weather"][0]["description"]
            translate_description = translate_text(description)
            return f"El clima en {city} es {translate_description} con una temperatura de {temperature}°C."
        else:
            return f"No se pudo obtener el clima para {city}. Código de estado: {response.status_code}"
    except requests.exceptions.RequestException as e:
        return f"Error de red al obtener información del tiempo: {str(e)}"
    except Exception as e:  
        return f"Error al obtener el clima: {str(e)}"
    
def get_response_ai(prompt):
    try:
        response = client.chat.completions.create(
            model="deepseek/deepseek-r1:free",
            messages=[
                {"role": "system", "content": "Eres un asistente amigable e útil."},
                {"role": "user", "content": prompt}
            ]
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error al consultar a OpenAi: {str(e)}"
    
def get_pokemon(pokemon_name):
    try:
        url = f"https://pokeapi.co/api/v2/pokemon/{pokemon_name.lower()}"
        response = requests.get(url)

        if response.status_code == 200:
            data = response.json()
            name = data["name"].capitalize() # poner la primera letra en mayúscula
            types = [type_info["type"]["name"] for type_info in data["types"]]
            height = data["height"]
            weight = data["weight"]
            return f"El pokemón {name} es de tipo {', '.join(types)}. Su altura es: {height / 10} m y su peso: {weight / 10} kg"
            # hay que dividirlo por 10 por que no representa la altura ni el peso directamente.
        else:
            return f"No se pudo obtener información sobre {pokemon_name}. Código de estado: {response.status_code}"
    except requests.exceptions.RequestException as e:
        return f"Error de red al obtener información del pokemon: {str(e)}"  
    except Exception as e:
        return f"Error al obtener información del Pokémon: {str(e)}"
    
def get_country_info(country):
    try:
        url = f"https://restcountries.com/v3.1/name/{country.lower()}"
        response = requests.get(url)
        
        if response.status_code == 200: # el data tiene que ir dentro del if, porque sino el else no salta
            data = response.json()
            # Imprimir data en formato json para que sea más legible
            # print(json.dumps(data, indent=4))
            name = data[0]["name"]["common"]
            capital = data[0]["capital"][0] if "capital" in data[0] else "No disponible"
            population = data[0]["population"]
            area = data[0]["area"]
            region = data[0]["region"]
            subregion = data[0]["subregion"] if "subregion" in data[0] else "No disponible"
            languages = ", ".join(data[0]["languages"].values()) if "languages" in data[0] else "No disponible"
            currencies = ", ".join([f"{v['name']} ({k})" for k, v in data[0]["currencies"].items()]) if "currencies" in data[0] else "No disponible"
            return f"Información sobre {name}:\n" \
                     f"Capital: {capital}\n" \
                     f"Población: {population}\n" \
                     f"Área: {area} km²\n" \
                     f"Región: {region}\n" \
                     f"Subregión: {subregion}\n" \
                     f"Idiomas: {languages}\n" \
                     f"Monedas: {currencies}"
        else:
            return f"No se pudo obtener información de {country}. Código de estado: {response.status_code}"
    except requests.exceptions.RequestException as e:
        return f"Error de red al obtener información del país: {str(e)}"  
    except Exception as e:
        return f"Error inesperado: {str(e)}"

## Pruebas
# print(get_weather("madrid"))
# print(get_weather("barcelona"))
# print(get_weather("pik"))
# print(get_country_info("francia"))
# print(get_country_info("australia"))