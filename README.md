# 🧪 ComuniVeci - Pruebas de Integración

Este repositorio contiene las pruebas de integración para el sistema ComuniVeci, específicamente para el servicio de autenticación de usuarios (`auth-service`).

## 📁 Estructura del proyecto

```bash
comuniveci_tests/
├── conftest.py # Configuración global de pruebas (fixtures)
├── tests/
│ └── test_auth_register.py # Pruebas para el registro de usuarios
├── template.html # Plantilla HTML para el reporte en PDF
├── generate_report.py # Script para generar reporte en PDF
├── .env # Variables de entorno para pruebas (local)
└── report.json # Archivo JSON generado por pytest con resultados
```


## ⚙️ Requisitos

- Python ≥ 3.10
- MongoDB en ejecución local
- Poetry instalado: `pip install poetry`
- Dependencias instaladas con Poetry

## 📦 Instalación

1. Clona este repositorio:

```bash
git clone https://github.com/tu_usuario/comuniveci_tests.git
cd comuniveci_tests
```

2. Instala las dependencias:

```bash
poetry install
```

3. Crea un archivo .env en la raíz del proyecto con el siguiente contenido (ajusta según sea necesario):

```bash
MONGO_URI=mongodb://localhost:27017/
DB_NAME_TEST=communiveci_test
```

Asegúrate de que MongoDB esté en ejecución local y que la base de datos communiveci_test esté vacía o sea temporal.

## ✅ Ejecutar pruebas

Puedes ejecutar todas las pruebas de integración usando:

```bash
poetry run pytest -v --json-report --json-report-file=report.json
```

Esto ejecutará las pruebas y generará un reporte en formato JSON.

## 🧾 Generar reporte PDF

Una vez generadas las pruebas, ejecuta el siguiente comando para construir el reporte PDF con los resultados:

```bash
poetry run python generate_report.py
```

Esto creará un archivo llamado TestReport.pdf en la raíz del proyecto.

📌 El PDF incluye:

- Resultados por prueba

- Estado de éxito o fallo

- Porcentaje de cobertura

- Logo de la universidad

- Fecha de generación

## 🏁 Ejemplo de prueba

Archivo de prueba incluido:

- test_auth_register.py: contiene tres casos de prueba:

    - Registro exitoso

    - Registro con correo duplicado

    - Registro con email inválido

## 🧼 Limpieza de datos
Durante las pruebas, los usuarios creados se almacenan temporalmente en la base de datos communiveci_test. Se eliminan automáticamente antes de cada prueba para evitar interferencias.