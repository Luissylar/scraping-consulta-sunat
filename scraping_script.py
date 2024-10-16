from playwright.sync_api import sync_playwright
import json

def standardize_key(key):
    key = key.lower()
    key = key.replace(' ', '_') 
    key = key.replace(':', '') 
    key = key.replace('(', '').replace(')', '')
    return key

def run(playwright):
    browser = playwright.chromium.launch(headless=True)
    url = 'https://e-consultaruc.sunat.gob.pe/cl-ti-itmrconsruc/FrameCriterioBusquedaWeb.jsp'
    data = {}

    context = browser.new_context(
        user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36"
    )

    page = context.new_page()
    page.goto(url, wait_until='networkidle')

    search_data = "20501741079"

    # Validar si el RUC es válido
    if len(search_data) != 11:
        return {"success": False, "message": "El RUC debe tener 11 dígitos"}

    ruc_input = page.locator('#txtRuc')
    ruc_input.wait_for(state='visible')
    ruc_input.fill(search_data)

    search_button = page.locator('#btnAceptar')
    search_button.wait_for(state='visible') 
    search_button.click()

    page.wait_for_timeout(2000)
    page.wait_for_load_state('networkidle')

    if page.url != 'https://e-consultaruc.sunat.gob.pe/cl-ti-itmrconsruc/jcrS00Alias':
        return {"success": False, "message": "No se encontraron resultados"}
    
    data["success"] = True

    try:
        ruc_razon_social_xpath = 'xpath=/html/body/div/div[2]/div/div[3]/div[2]/div[1]/div/div[2]/h4'
        ruc_razon_social = page.locator(ruc_razon_social_xpath).inner_text()
        ruc, razon_social = ruc_razon_social.split(' - ', 1)
        data["ruc"] = ruc
        data["razon_social"] = razon_social
    except Exception as e:
        data["ruc"] = None
        data["razon_social"] = None

    list_group_items = page.locator('div.list-group-item')
    for item in list_group_items.element_handles():
        h4_elements = item.query_selector_all('h4.list-group-item-heading')
        p_elements = item.query_selector_all('p.list-group-item-text')

        if len(h4_elements) == len(p_elements):
            for h4, p in zip(h4_elements, p_elements):
                key = standardize_key(h4.inner_text().strip(':'))
                value = p.inner_text().strip()
                data[key] = value

    try:
        list_group_items = page.locator('div.list-group-item')
        for item in list_group_items.element_handles():
            h4_element = item.query_selector('h4.list-group-item-heading')
            if h4_element:
                table_element = item.query_selector('table.tblResultado')
                if table_element:
                    table_key = standardize_key(h4_element.inner_text().strip()) 
                    rows = table_element.query_selector_all('tbody tr')  
                    table_data = [] 

                    for row in rows:
                        cells = row.query_selector_all('td')
                        for cell in cells:
                            value = cell.inner_text().strip()
                            table_data.append(value) 

                    data[table_key] = table_data 

    except Exception as e:
        print(f"Error al capturar la tabla: {e}")

    page.screenshot(path='resultado.png', full_page=True)
    pdf_path = 'resultado.pdf'
    page.pdf(path=pdf_path, format='A4', print_background=True)
    browser.close()

    return data

with sync_playwright() as playwright:
    data = run(playwright)

    with open('consulta.json', 'w', encoding='utf-8') as json_file:
        json.dump(data, json_file, ensure_ascii=False, indent=4)
