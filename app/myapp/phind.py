from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException, TimeoutException

def phind(points):
    # Configuración para trabajar en segundo plano (headless mode)
    service = Service(executable_path='/bin/chromedriver')
    options = webdriver.ChromeOptions()
    options.binary_location = "/bin/google-chrome"
    # options.add_argument('--headless')  # Ejecutar en segundo plano
    options.add_argument("--window-size=1920,1080")  # Simular tamaño de ventana normal
    options.add_argument("--disable-gpu")  # Desactivar GPU en modo headless
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3")

    answer = ""
    # Inicializar el navegador en modo headless
    driver = webdriver.Chrome(service=service, options=options)

    # Abrir la página de Phind
    driver.get("https://www.phind.com")

    # Aumentar el tiempo de espera
    wait = WebDriverWait(driver, 30)

    # Intentar encontrar el textarea y tomar una captura para depuración
    try:
        search_box = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "textarea")))
        # # Tomar una captura de pantalla para verificar el estado de la página en headless mode
        # driver.save_screenshot('headless_screenshot.png')
        # print("Captura de pantalla guardada como headless_screenshot.png")

    except TimeoutException:
        print("No se pudo encontrar el textarea. Revisa la captura de pantalla para más detalles.")

    # Si se encuentra el textarea, continuar con el envío del prompt
    if search_box:
        # Construir el prompt basado en los puntos de interés
        

        prompt = (
            "Imagina que estás creando un comercial emocionante para una excursión en un hermoso paisaje natural. "
            "Los visitantes recorrerán diversos puntos, cada uno con sus propios encantos. "
            "Debes describir estos lugares de manera atractiva y destacar las experiencias únicas que pueden ofrecer. "
            "Haz que los turistas se sientan emocionados por la fauna, los sitios históricos, y las vistas espectaculares. "
            "Aquí están los puntos del recorrido:"
        )

        # Generar respuestas para cada punto
        for point in points:
            Id = point["id"]
            location = point["location"]
            altitude = point["altitude"]
            char1 = point["characteristics"][0]
            char2 = point["characteristics"][1]
            char3 = point["characteristics"][2]
            char4 = point["characteristics"][3]

            fauna_desc = f"con un índice de diversidad de fauna de {char1}"
            flora_desc = f"con un índice de variedad de flora de {char2}"
            rivers_desc = f"con un índice de ríos de {char3}"
            historic_desc = f"con un índice de historia de {char4}"

            prompt += (
                f"\nPunto {Id}: Ubicado en {location}, es un lugar a {altitude} altitud. "
                f"Este lugar es {fauna_desc}, {flora_desc}, {rivers_desc}, y {historic_desc}. "
                "Un lugar que promete una experiencia enriquecedora."
            )

        prompt += "\nElabora un mini-comercial sobre esta excursión."

        try:
            # Enviar la pregunta al campo de búsqueda en Phind
            search_box.send_keys(prompt)
            search_box.send_keys(Keys.ENTER)
        except StaleElementReferenceException:
            pass
            # print("El elemento textarea fue reemplazado o actualizado, no se pudo enviar el mensaje nuevamente.")

        # Esperar a que el texto "Suggestions" aparezca, lo que indica que la respuesta se ha generado completamente
        wait.until(EC.presence_of_element_located((By.XPATH, "//h6[contains(text(), 'Suggestions')]")))

        # Obtener el contenido de la página
        page_source = driver.page_source

        # Parsear el HTML con BeautifulSoup
        soup = BeautifulSoup(page_source, "html.parser")

        # Encontrar la respuesta usando las clases mencionadas
        answer_section = soup.find("h6", string="Answer | Phind Instant Model")
        if answer_section:
            answer_divs = answer_section.find_next_siblings("div", class_="fs-5")
            for div in answer_divs:
                answer = div.get_text(strip=True)
        else:
            print("No se encontró la respuesta.")

    # Cerrar el navegador
    driver.quit()

    return answer
