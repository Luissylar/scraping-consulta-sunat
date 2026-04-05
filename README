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
