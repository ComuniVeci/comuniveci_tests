import json, os, sys, pdfkit
from datetime import datetime
from jinja2 import Environment, FileSystemLoader

# Verificar si el archivo report.json existe
if not os.path.exists("report.json"):
    print("❌ El archivo report.json no existe. Ejecuta primero pytest para generar el reporte:")
    print("   poetry run pytest -v --json-report --json-report-file=report.json")
    sys.exit(1)

# Cargar datos
with open("report.json", "r") as f:
    report_data = json.load(f)

# Preparar datos para plantilla
summary = report_data["summary"]
tests = report_data["tests"]

context = {
    "date": datetime.now().strftime("%d/%m/%Y %H:%M"),
    "summary": summary,
    "tests": tests,
    "logo_path": "logo_universidad.png"  # si quieres incluir un logo
}

# Renderizar HTML
env = Environment(loader=FileSystemLoader("."))
template = env.get_template("template.html")
html_out = template.render(context)

# Exportar a PDF
pdfkit.from_string(html_out, "TestReport.pdf", options={"enable-local-file-access": ""})
print("✅ Reporte generado como TestReport.pdf")
