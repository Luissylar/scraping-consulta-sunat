# scraping-consulta-sunat

Proyecto Python para consultar datos en SUNAT con una arquitectura orientada a objetos (POO), separada por capas y preparada para consultar por:

- RUC
- DNI
- Nombre o razon social

## Arquitectura del proyecto

El codigo esta distribuido en modulos para facilitar mantenimiento y crecimiento:

- `main.py`: punto de entrada de consola.
- `app/cli.py`: menu interactivo y lectura de datos por terminal.
- `app/service.py`: orquestador principal (flujo de consulta).
- `app/queries.py`: tipos de consulta y armado de payload por estrategia.
- `app/client.py`: cliente HTTP para enviar la peticion a SUNAT.
- `app/parser.py`: parser HTML para extraer informacion estructurada.
- `app/constants.py`: URL, cabeceras y token base.

## Requisitos

- Python 3.8+
- Dependencias en `requirements.txt`

Instalacion:

```bash
pip install -r requirements.txt
```

## Uso

Ejecuta:

```bash
python main.py
```

Luego en terminal:

1. Selecciona el tipo de consulta (RUC, DNI o NOMBRE).
2. Escribe el dato solicitado.
3. El resultado se guarda en `consulta.json`.

Nota: para consulta por RUC, el RUC se ingresa directamente en la terminal por el usuario.

## Configuracion importante

SUNAT usa cookies y token de sesion que pueden expirar. Si aparece error de sesion o no hay resultados:

1. Actualiza `DEFAULT_HEADERS["Cookie"]` en `app/constants.py`.
2. Actualiza `DEFAULT_TOKEN` en `app/constants.py`.

## Licencia y uso libre

Este proyecto es de uso libre bajo licencia MIT.

Cualquier persona puede usar, copiar, modificar, distribuir y vender este software, siempre que se mantenga el aviso de copyright y la licencia.

Consulta el detalle completo en `LICENSE`.

## Codigo Original ##
> Esta Es la peticion original obtenida debida a una investigacion que hice, ademas de encontrar el patron inicial para poder extraer los datos de una manera cretiva.

```python
import requests
import json
from bs4 import BeautifulSoup

ruc = input('Inserte ruc') 

def standardize_key(key):
    key = key.lower()
    key = key.replace(' ', '_') 
    key = key.replace(':', '') 
    key = key.replace('(', '').replace(')', '')
    return key

def clear_text(text):
    if not text:
        return ""
    # 1. Reemplaza cualquier secuencia de \r, \n, \t o múltiples espacios por un solo espacio
    texto_limpio = " ".join(text.split())
    # 2. Si el resultado es algo como "DNI 73016189 - APELLIDOS", limpiamos espacios alrededor del guion
    if " - " in texto_limpio:
        partes = [p.strip() for p in texto_limpio.split("-", 1)]
        return " - ".join(partes)
    return texto_limpio

def extraer_datos_sunat(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    data = {}
    
   

    # 1. Extraer RUC y Razón Social (el H4 principal)
    try:
        # Buscamos TODOS los h4 con esa clase
        h4_headers = soup.find_all('h4', class_='list-group-item-heading')

         # Verificar si la respuesta es válida (si existe el contenedor principal)
        container = soup.find('div', class_='container')
        if not h4_headers or not container:
            return {"success": False, "message": "No se encontraron resultados o sesión expirada"}

        data["success"] = True
        
        header_ruc = None
        for h4 in h4_headers:
            texto = h4.get_text(strip=True)
            # El XPath original apunta al primer h4 importante que contiene el RUC
            if '-' in texto and ('RUC' in texto or texto.split(' - ')[0].isdigit()):
                header_ruc = h4
                break

        if header_ruc:
            text_ruc = header_ruc.get_text(strip=True)
            # Limpiamos el texto por si trae "RUC: " al inicio
            text_ruc = text_ruc.replace('RUC: ', '')
            
            # Dividimos por el guion
            parts = text_ruc.split(' - ', 1)
            if len(parts) == 2:
                data["ruc"] = parts[0].strip()
                data["razon_social"] = parts[1].strip()
            else:
                data["ruc"] = text_ruc
                data["razon_social"] = "No encontrada"
        else:
            # Si no encontró nada con el loop, intentamos el selector directo
            # que equivale al div.list-group-item h4 del XPath
            direct_h4 = soup.select_one('div.list-group-item h4.list-group-item-heading')
            if direct_h4:
                text_ruc = direct_h4.get_text(strip=True).replace('RUC: ', '')
                parts = text_ruc.split(' - ', 1)
                data["ruc"] = parts[0].strip() if len(parts) > 0 else None
                data["razon_social"] = parts[1].strip() if len(parts) > 1 else None
    
    except Exception as e:
        print(f"Error específico en RUC/Razón Social: {e}")
        data["ruc"] = None
        data["razon_social"] = None

    # 2. Extraer pares H4 y P (Datos generales)
    items = soup.find_all('div', class_='list-group-item')
    for item in items:
        h4_elements = item.find_all('h4', class_='list-group-item-heading')
        p_elements = item.find_all('p', class_='list-group-item-text')

        if len(h4_elements) == len(p_elements):
            for h4, p in zip(h4_elements, p_elements):
                key = standardize_key(h4.get_text(strip=True).rstrip(':'))
                raw_value = p.get_text() # Obtenemos el texto con todo y basura
                value = clear_text(raw_value)
                data[key] = value

    # 3. Extraer Tablas (tblResultado)
    for item in items:
        h4_element = item.find('h4', class_='list-group-item-heading')
        table_element = item.find('table', class_='tblResultado')
        
        if h4_element and table_element:
            table_key = standardize_key(h4_element.get_text(strip=True))
            rows = table_element.find_all('tr')
            table_data = []
            
            for row in rows:
                cells = row.find_all('td')
                for cell in cells:
                    value = cell.get_text(strip=True)
                    if value: table_data.append(value)
            
            data[table_key] = table_data

    return data



url = "https://e-consultaruc.sunat.gob.pe/cl-ti-itmrconsruc/jcrS00Alias"

headers = {
    "Host": "e-consultaruc.sunat.gob.pe",
    "Cookie": "ITMRCONSRUCSESSION=hTR2pSwSJLpNdg7JpZVGjmg9Qw1nTQk42pYbfvHhrCbLHBvGcFTGG2Rd0pqHN4ldCpjJh3VFlL213FMpQJwBqjg6yZpw32tZ2RvvhgVCZM1vcyn2R1S5VYsJ6mVDg2LJ6cCT9XhtTXSNST7PkyvWSCGpLYmwvlq5TCh17h5HtGLx3ndhJnknJpDJNBvvglcmQBKylQZxnQHMgYHGlGBl92ZRPpnJyn3T1GD1bWBtcmPyVR2Mn9b149Rp2zvJyvwz!-1537523843!-1747081720; TS01fda901=014dc399cb77c3e3a60e8c53106f1cacf0515a7318daf996c38006b27cfd69d0222d219665e5b1837dbf9dc13f8acc6b1a6aa8257362222fc1241e0a0b0ba88ce4a7a3b565; TSf3c1dbbd027=08fe7428c8ab2000fd359742df8c04fc6c4971367e4c28d76a57338b6ff483466f3780f76f52d35408c9a96eb51130002bd4e01cf9477f2bbafa194c14563286e79982a39cd941dd787a9ec6ac63950f6e1cdcb96d06e3775db5fad15887b186; site24x7rumID=478242528727210.1775415413504.1775415419770.0",
    "Cache-Control": "max-age=0",
    "Sec-Ch-Ua": '"Not-A.Brand";v="24", "Chromium";v="146"',
    "Sec-Ch-Ua-Mobile": "?0",
    "Sec-Ch-Ua-Platform": '"Windows"',
    "Accept-Language": "es-ES,es;q=0.9",
    "Origin": "https://e-consultaruc.sunat.gob.pe",
    "Content-Type": "application/x-www-form-urlencoded",
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "Sec-Fetch-Site": "same-origin",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-User": "?1",
    "Sec-Fetch-Dest": "document",
    "Referer": "https://e-consultaruc.sunat.gob.pe/cl-ti-itmrconsruc/FrameCriterioBusquedaWeb.jsp",
    "Accept-Encoding": "gzip, deflate, br",
    "Connection": "keep-alive"
}

payload = {
    "accion": "consPorRuc",
    "razSoc": "",
    "nroRuc": ruc,
    "nrodoc": "",
    "token": "j9r9v43x4y96c9efegzd5ndrzey2o4ojofrf6kaw5u7jw8cac36u", # Este token es temporal
    "contexto": "ti-it",
    "modo": "1",
    "rbtnTipo": "1",
    "search1": ruc,
    "tipdoc": "1",
    "search2": "",
    "search3": "",
    "codigo": ""
}

try:
    response = requests.post(url, headers=headers, data=payload)
    
    if response.status_code == 200:
        # Procesar el HTML con la lógica de Playwright
        resultado_final = extraer_datos_sunat(response.text)
        
        # Guardar en JSON
        with open('consulta.json', 'w', encoding='utf-8') as json_file:
            json.dump(resultado_final, json_file, ensure_ascii=False, indent=4)
        
        print("Datos extraídos y guardados en consulta.json")
    else:
        print(f"Error en servidor: {response.status_code}")

except Exception as e:
    print(f"Error: {e}")

```

