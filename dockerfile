# Usa la imagen base oficial de Python
FROM python:3.9-slim

# Instala las dependencias necesarias para Chrome
RUN apt-get update && apt-get install -y \
    wget \
    curl \
    unzip \
    gnupg2 \
    ca-certificates \
    fonts-liberation \
    libappindicator3-1 \
    libasound2 \
    libatk-bridge2.0-0 \
    libatk1.0-0 \
    libcups2 \
    libdbus-glib-1-2 \
    libgbm-dev \
    libgtk-3-0 \
    libnspr4 \
    libnss3 \
    libx11-xcb1 \
    libxcomposite1 \
    libxrandr2 \
    xdg-utils \
    --no-install-recommends && \
    rm -rf /var/lib/apt/lists/*

# Agrega el repositorio de Google Chrome e instala la última versión de Chrome
RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - && \
    echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" > /etc/apt/sources.list.d/google-chrome.list && \
    apt-get update && \
    apt-get install -y google-chrome-stable

# Establece el directorio de trabajo
WORKDIR /app

# Verificar la versión de Chrome
RUN google-chrome --version

# Instalar ChromeDriver manualmente
RUN CHROME_DRIVER_VERSION=latest && \
    DRIVER_VERSION=$(curl -sS https://chromedriver.storage.googleapis.com/LATEST_RELEASE) && \
    echo "Using ChromeDriver version: $DRIVER_VERSION" && \
    wget -q https://chromedriver.storage.googleapis.com/$DRIVER_VERSION/chromedriver_linux64.zip && \
    unzip chromedriver_linux64.zip -d /usr/local/bin/ && \
    rm chromedriver_linux64.zip

# Copia el archivo de dependencias
COPY requirements.txt .

# Instala las dependencias de Python
RUN pip install --no-cache-dir -r requirements.txt

# Instala las librerías de Playwright y descarga los navegadores
RUN pip install playwright && \
    playwright install

# Copia el código de la aplicación
COPY . .

# Establece el ChromeDriver en la variable PATH
ENV PATH="/usr/local/bin:$PATH"

# Define el comando por defecto para ejecutar el script de scraping
CMD ["python", "scraping_script.py"]
