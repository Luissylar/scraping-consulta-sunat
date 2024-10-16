from playwright.sync_api import sync_playwright
import time
import json

def run(playwright):
    browser = playwright.chromium.launch(headless=True)

    url = 'https://e-consultaruc.sunat.gob.pe/cl-ti-itmrconsruc/FrameCriterioBusquedaWeb.jsp'
    data = {}
    
    context = browser.new_context(
        user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36"
    )
    
    page = context.new_page()

    page.goto(url, wait_until='networkidle')
    search_data = "10730161897"

    #validar si el ruc es valido
    if len(search_data) != 11:
        data["success"] = False
        data["message"] = "El RUC debe tener 11 dígitos"
        return data

    ruc_input = page.locator('#txtRuc')
    ruc_input.wait_for(state='visible')
    ruc_input.fill(search_data)

    search_button = page.locator('#btnAceptar')
    search_button.wait_for(state='visible') 
    search_button.click()

    page.wait_for_timeout(2000)
    page.wait_for_load_state('networkidle')

    if page.url != 'https://e-consultaruc.sunat.gob.pe/cl-ti-itmrconsruc/jcrS00Alias':
        data["success"] = False
        data["message"] = "No se encontraron resultados"
        return data
    else:
        data["success"] = True

    actividades_economicas_xpath = 'xpath=/html/body/div/div[2]/div/div[3]/div[2]/div[10]/div/div[2]/table/tbody/tr'
    comprobantes_de_pago_xpath = 'xpath=/html/body/div/div[2]/div/div[3]/div[2]/div[11]/div/div[2]/table/tbody/tr'
    sistema_emision_electronica_xpath = 'xpath=/html/body/div/div[2]/div/div[3]/div[2]/div[12]/div/div[2]/table/tbody/tr'
    padrones_xpath = 'xpath=/html/body/div/div[2]/div/div[3]/div[2]/div[16]/div/div[2]/table/tbody/tr'
    ruc_razon_social_xpath = 'xpath=/html/body/div/div[2]/div/div[3]/div[2]/div[1]/div/div[2]/h4'
    
    xpaths = {
        "tipo_contribuyente": 'xpath=/html/body/div/div[2]/div/div[3]/div[2]/div[2]/div/div[2]/p',
        "tipo_documento": 'xpath=/html/body/div/div[2]/div/div[3]/div[2]/div[3]/div/div[2]/p',
        "nombre_comercial": 'xpath=/html/body/div/div[2]/div/div[3]/div[2]/div[4]/div/div[2]/p',
        "fecha_inscripcion": 'xpath=/html/body/div/div[2]/div/div[3]/div[2]/div[4]/div/div[2]/p',
        "fecha_inicio_actividades": 'xpath=/html/body/div/div[2]/div/div[3]/div[2]/div[4]/div/div[4]/p',
        "estado_contribuyente": 'xpath=/html/body/div/div[2]/div/div[3]/div[2]/div[5]/div/div[2]/p',
        "condicion_contribuyente": 'xpath=/html/body/div/div[2]/div/div[3]/div[2]/div[6]/div/div[2]/p',
        "direccion_domicilio_fiscal": 'xpath=/html/body/div/div[2]/div/div[3]/div[2]/div[7]/div/div[2]/p',
        "sistema_emision_comprobante": 'xpath=/html/body/div/div[2]/div/div[3]/div[2]/div[8]/div/div[2]/p',
        "actividad_comercio_exterior": 'xpath=/html/body/div/div[2]/div/div[3]/div[2]/div[8]/div/div[4]/p',
        "sistema_contabilidad": 'xpath=/html/body/div/div[2]/div/div[3]/div[2]/div[9]/div/div[2]/p',
        "emisor_electronico": 'xpath=/html/body/div/div[2]/div/div[3]/div[2]/div[13]/div/div[2]/p',
        "comprobantes_electronicos": 'xpath=/html/body/div/div[2]/div/div[3]/div[2]/div[14]/div/div[2]/p',
        "afiliado_a_ple": 'xpath=/html/body/div/div[2]/div/div[3]/div[2]/div[15]/div/div[2]/p',
    }


    try:
        ruc_razon_social = page.locator(ruc_razon_social_xpath).inner_text()
        
        ruc, razon_social = ruc_razon_social.split(' - ', 1)
        data["ruc"] = ruc
        data["razon_social"] = razon_social
    except Exception as e:
        print(f"Error al obtener RUC y Razón Social: {e}")
        data["ruc"] = None
        data["razon_social"] = None

    for key, xpath in xpaths.items():
        try:
            element = page.locator(xpath)
            if element.count() > 0:
                data[key] = element.inner_text()
            else:
                data[key] = None
        except Exception as e:
            print(f"Error al obtener {key}: {e}")
            data[key] = None

    actividades_economicas = []
    comprobantes_de_pago = []
    emisiones_electronicas = []
    padrones = []

    # Procesamiento de actividades económicas
    try:
        rows = page.locator(actividades_economicas_xpath)
        for i in range(rows.count()):
            actividades_economicas.append(rows.nth(i).inner_text())
    except Exception as e:
        print(f"Error al obtener actividades económicas: {e}")

    # Procesamiento de comprobantes de pago
    try:
        rows = page.locator(comprobantes_de_pago_xpath)
        for i in range(rows.count()):
            comprobantes_de_pago.append(rows.nth(i).inner_text())
    except Exception as e:
        print(f"Error al obtener comprobantes de pago: {e}")

    # Procesamiento de sistema de emisión electrónica
    try:
        rows = page.locator(sistema_emision_electronica_xpath)
        for i in range(rows.count()):
            emisiones_electronicas.append(rows.nth(i).inner_text())
    except Exception as e:
        print(f"Error al obtener sistema de emisión electrónica: {e}")

    # Procesamiento de padrones
    try:
        rows = page.locator(padrones_xpath)
        for i in range(rows.count()):
            padrones.append(rows.nth(i).inner_text())
    except Exception as e:
        print(f"Error al obtener padrones: {e}")
    
    data["actividades_economicas"] = actividades_economicas
    data["comprobantes_de_pago"] = comprobantes_de_pago
    data["sistema_emision_electronica"] = emisiones_electronicas
    data["padrones"] = padrones

    page.screenshot(path='resultado.png', full_page=True)
    pdf_path = 'resultado.pdf'
    page.pdf(path=pdf_path, format='A4', print_background=True)
    browser.close()

    return data

with sync_playwright() as playwright:
    data = run(playwright)

    with open('consulta.json', 'w', encoding='utf-8') as json_file:
        json.dump(data, json_file, ensure_ascii=False, indent=4)
