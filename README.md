# 🧪 ComuniVeci - Pruebas de Integración

Este repositorio contiene las pruebas automáticas para el sistema ComuniVeci, incluyendo:

    - 🔐 Servicio de autenticación (auth-service)

    - 🌐 Interfaz web (frontend)

Se utilizan herramientas como Pytest, Selenium y Faker para validar tanto el backend como flujos de usuario en el navegador.

## 📁 Estructura del proyecto

```bash
comuniveci_tests/
├── conftest.py                # Configuración global y fixtures (incluye navegador y seguimiento de usuarios)
├── tests_backend/
│   ├── test_auth_login.py     # Pruebas de login
│   ├── test_auth_me.py        # Pruebas del endpoint /me
│   └── test_auth_register.py  # Pruebas de registro
├── tests_frontend/
│   ├── test_login_frontend.py     # Pruebas E2E del login
│   ├── test_register_frontend.py  # Pruebas E2E del registro
│   └── test_admin_frontend.py     # Pruebas del panel de administración
├── generate_report.py         # Script para generar reporte en PDF
├── template.html              # Plantilla HTML para reporte PDF
├── .env                       # Variables de entorno
├── report.json                # Reporte en JSON generado por pytest
└── TestReport.pdf             # Reporte PDF final
```


## ⚙️ Requisitos

- Python ≥ 3.10
- MongoDB en ejecución local
- Google Chrome (para Selenium)
- ChromeDriver compatible
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
DB_NAME=nombre_base_de_datos
```

ℹ️ Ahora las pruebas se ejecutan sobre la base de datos principal communiveci pero eliminan automáticamente los usuarios creados durante las pruebas.

## ✅ Ejecutar pruebas

Ejecuta todas las pruebas:

```bash
poetry run pytest --json-report --json-report-file=report.json
```

También puedes ejecutar pruebas por grupo:

- Solo backend:

```bash
poetry run pytest -m backend
```

- Solo frontend:

```bash
poetry run pytest -m frontend
```

## 🧼 Limpieza de datos

Los usuarios creados por las pruebas se rastrean dinámicamente y se eliminan automáticamente al finalizar cada prueba, incluso en la base de datos principal.

## 🧾 Generar reporte PDF

Una vez generadas las pruebas, ejecuta el siguiente comando para construir el reporte PDF con los resultados:

```bash
poetry run python generate_report.py
```

Esto creará un archivo llamado TestReport.pdf en la raíz del proyecto.

📌 El archivo TestReport.pdf incluirá:

- Resultados por prueba

- Estado de éxito o fallo

- Porcentaje de cobertura

- Fecha y hora de ejecución

- Agrupación por tipo de prueba

## ✅ Funcionalidades cubiertas

✔️ Registro, login y validación de sesión
✔️ Pruebas visuales del flujo de autenticación
✔️ Acceso al panel de administración y sus secciones
✔️ Verificación de usuarios, estadísticas, métricas y cierre de sesión