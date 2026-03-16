#Proyecto M4 - Buscador de Pokémon con PokéAPI

import requests
import json
import webbrowser
import os
from pathlib import Path


def obtener_datos_pokemon(nombre_pokemon):
    """
    Consulta la API de PokéAPI para obtener datos del Pokémon.

    Args:
        nombre_pokemon (str): Nombre del Pokémon a buscar

    Returns:
        dict: Datos del Pokémon o None si ocurre un error
    """
    try:
        url = f"https://pokeapi.co/api/v2/pokemon/{nombre_pokemon.lower()}"
        respuesta = requests.get(url, timeout=5)

        if respuesta.status_code == 404:
            print(f"[ERROR] El Pokémon '{nombre_pokemon}' no existe en la API.")
            return None

        if respuesta.status_code != 200:
            print(f"[ERROR] La API retornó el código {respuesta.status_code}")
            return None

        return respuesta.json()

    except requests.exceptions.Timeout:
        print("❌ Error: La solicitud tardó demasiado. Intenta de nuevo.")
        return None
    except requests.exceptions.ConnectionError:
        print("❌ Error: No se pudo conectar a la API. Verifica tu conexión a internet.")
        return None
    except Exception as e:
        print(f"❌ Error inesperado: {str(e)}")
        return None


def procesar_datos_pokemon(datos):
    """
    Extrae y procesa los datos relevantes del Pokémon.

    Args:
        datos (dict): Datos del Pokémon desde la API

    Returns:
        dict: Datos procesados
    """
    movimientos = []
    for movimiento in datos.get("moves", [])[:10]:  # Primeros 10 movimientos
        movimientos.append(movimiento["move"]["name"])

    habilidades = []
    for habilidad in datos.get("abilities", []):
        habilidades.append(habilidad["ability"]["name"])

    tipos = []
    for tipo in datos.get("types", []):
        tipos.append(tipo["type"]["name"])

    imagen_url = datos.get("sprites", {}).get("front_default")

    datos_procesados = {
        "nombre": datos.get("name", "").upper(),
        "imagen_url": imagen_url,
        "peso": datos.get("weight"),
        "tamaño": datos.get("height"),
        "movimientos": movimientos,
        "habilidades": habilidades,
        "tipos": tipos,
        "id": datos.get("id")
    }

    return datos_procesados


def mostrar_informacion(datos):
    """
    Muestra la información del Pokémon en la consola.

    Args:
        datos (dict): Datos procesados del Pokémon
    """
    print("\n" + "="*50)
    print(f"📊 INFORMACIÓN DEL POKÉMON: {datos['nombre']}")
    print("="*50)
    print(f"🔢 ID: {datos['id']}")
    print(f"⚖️  Peso: {datos['peso']} hectogramos")
    print(f"📏 Tamaño: {datos['tamaño']} decímetros")
    print(f"🎯 Tipos: {', '.join(datos['tipos'])}")
    print(f"💪 Habilidades: {', '.join(datos['habilidades'])}")
    print(f"🎮 Movimientos (primeros 10):")
    for i, movimiento in enumerate(datos['movimientos'], 1):
        print(f"   {i}. {movimiento}")
    print(f"🖼️  Imagen: {datos['imagen_url']}")
    print("="*50 + "\n")


def guardar_json(datos, nombre_pokemon):
    """
    Guarda los datos del Pokémon en un archivo JSON.

    Args:
        datos (dict): Datos del Pokémon a guardar
        nombre_pokemon (str): Nombre del Pokémon (para el nombre del archivo)

    Returns:
        bool: True si se guardó correctamente, False en caso contrario
    """
    try:
        carpeta_pokedex = Path("pokedex")

        if not carpeta_pokedex.exists():
            carpeta_pokedex.mkdir(parents=True, exist_ok=True)
            print(f"✅ Carpeta 'pokedex' creada.")

        archivo_json = carpeta_pokedex / f"{nombre_pokemon.lower()}.json"

        with open(archivo_json, "w", encoding="utf-8") as archivo:
            json.dump(datos, archivo, ensure_ascii=False, indent=4)

        print(f"✅ Datos guardados en: {archivo_json}")
        return True

    except Exception as e:
        print(f"❌ Error al guardar el archivo JSON: {str(e)}")
        return False


def abrir_imagen(url_imagen):
    """
    Abre la imagen frontal del Pokémon en el navegador.

    Args:
        url_imagen (str): URL de la imagen
    """
    if url_imagen:
        try:
            webbrowser.open(url_imagen)
            print(f"🌐 Abriendo imagen en el navegador...")
        except Exception as e:
            print(f"❌ No se pudo abrir la imagen: {str(e)}")
    else:
        print("❌ No se encontró imagen del Pokémon.")


def buscar_otro_pokemon():
    """
    Función para buscar otro Pokémon.
    """
    nombre_pokemon = input("\n¿Qué Pokémon deseas buscar? ").strip()

    if not nombre_pokemon:
        print("❌ Error: Debes ingresar un nombre de Pokémon.")
        return

    print(f"\n🔍 Buscando a {nombre_pokemon}...")

    # Obtener datos de la API
    datos_api = obtener_datos_pokemon(nombre_pokemon)

    if datos_api is None:
        return

    # Procesar datos
    datos_procesados = procesar_datos_pokemon(datos_api)

    # Mostrar información
    mostrar_informacion(datos_procesados)

    # Guardar en JSON
    guardar_json(datos_procesados, nombre_pokemon)

    # Abrir imagen en navegador
    if datos_procesados["imagen_url"]:
        abrir_imagen(datos_procesados["imagen_url"])


def cerrar_programa():
    """
    Función para cerrar el programa esperando Enter.
    """
    input("\nPresiona Enter para cerrar el programa...")


def main():
    """
    Función principal que coordina todo el flujo del programa.
    """
    print("\n" + "="*50)
    print("🎮 BUSCADOR DE POKÉMON - PokéAPI")
    print("="*50)

    while True:
        buscar_otro_pokemon()
        continuar = input("¿Quieres buscar otro Pokémon? (s/n): ").strip().lower()
        if continuar != 's':
            break

    cerrar_programa()


if __name__ == "__main__":
    main()
