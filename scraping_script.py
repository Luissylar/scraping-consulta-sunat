from playwright.sync_api import sync_playwright
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

    # Validar si el RUC es válido
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

    # Procesar datos de la página
    try:
        # Obtener RUC y Razón Social
        ruc_razon_social_xpath = 'xpath=/html/body/div/div[2]/div/div[3]/div[2]/div[1]/div/div[2]/h4'
        ruc_razon_social = page.locator(ruc_razon_social_xpath).inner_text()
        ruc, razon_social = ruc_razon_social.split(' - ', 1)
        data["ruc"] = ruc
        data["razon_social"] = razon_social
    except Exception as e:
        print(f"Error al obtener RUC y Razón Social: {e}")
        data["ruc"] = None
        data["razon_social"] = None

    # Obtener información de etiquetas h4 y p
    sections = page.locator('xpath=//div[contains(@class, "list-group-item")]')
    for section in sections.element_handles():
        h4_element = section.query_selector('h4.list-group-item-heading')  # Cambiado a query_selector
        if h4_element:
            key = h4_element.inner_text().strip(':')
            # Tratar de obtener el texto del siguiente elemento p (si existe)
            p_element = section.query_selector('p.list-group-item-text')  # Cambiado a query_selector
            if p_element:
                value = p_element.inner_text().strip()
                data[key] = value
            else:
                # Si no hay p_element, tratar de obtener una tabla
                table_element = section.query_selector('table.tblResultado')  # Buscando la tabla
                if table_element:
                    # Obtener los valores de la tabla
                    rows = table_element.query_selector_all('tbody tr')  # Cambiado a query_selector_all
                    values = []
                    for row in rows:
                        cells = row.query_selector_all('td')  # Obtener las celdas de cada fila
                        values.append([cell.inner_text() for cell in cells])  # Obtener el texto de cada celda
                    data[key] = values  # Almacenar como lista de filas

    page.screenshot(path='resultado.png', full_page=True)
    pdf_path = 'resultado.pdf'
    page.pdf(path=pdf_path, format='A4', print_background=True)
    browser.close()

    return data

with sync_playwright() as playwright:
    data = run(playwright)

    with open('consulta.json', 'w', encoding='utf-8') as json_file:
        json.dump(data, json_file, ensure_ascii=False, indent=4)
