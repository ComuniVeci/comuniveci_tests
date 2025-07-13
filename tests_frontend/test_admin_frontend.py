import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

@pytest.mark.frontend
def test_admin_panel_sections(browser):
    admin_email = "admin@admin.com"
    admin_password = "12345678"

    # 1. Ir a login y logearse
    browser.get("http://localhost:8080/login.html")
    browser.find_element(By.ID, "email").send_keys(admin_email)
    browser.find_element(By.ID, "password").send_keys(admin_password)
    browser.find_element(By.CSS_SELECTOR, "button[type='submit']").click()

    # 2. Esperar redirección al index y hacer clic en el botón "Administrar"
    WebDriverWait(browser, 10).until(
        EC.presence_of_element_located((By.XPATH, "//a[contains(text(), 'Administrar')]"))
    )
    browser.find_element(By.XPATH, "//a[contains(text(), 'Administrar')]").click()

    # 3. Esperar carga del panel
    WebDriverWait(browser, 10).until(
        EC.visibility_of_element_located((By.ID, "admin-content"))
    )

    WebDriverWait(browser, 10).until(
        lambda d: d.find_element(By.ID, "postList").text.strip() != ""
    )

    WebDriverWait(browser, 10).until(
        lambda d: d.find_element(By.ID, "statistics").text.strip() != ""
    )

    WebDriverWait(browser, 10).until(
        lambda d: d.find_element(By.ID, "users").text.strip() != ""
    )

    WebDriverWait(browser, 10).until(
        lambda d: d.find_element(By.ID, "metrics").text.strip() != ""
    )

    # 4. Verificar que existen las 4 secciones
    assert browser.find_element(By.ID, "postList").is_displayed()
    assert browser.find_element(By.ID, "statistics").is_displayed()
    assert browser.find_element(By.ID, "users").is_displayed()
    assert browser.find_element(By.ID, "metrics").is_displayed()

    # 5. Verificar algún elemento de alguna sección
    approved_li = WebDriverWait(browser, 10).until(
        EC.presence_of_element_located((By.XPATH, "//li[strong[contains(text(), '🟢 Aprobadas:')]]"))
    )
    assert "🟢 Aprobadas:" in approved_li.text

    # 6. Volver al inicio y cerrar sesión
    browser.find_element(By.XPATH, "//a[contains(text(), '← Volver al mapa')]").click()
    WebDriverWait(browser, 5).until(
        EC.presence_of_element_located((By.XPATH, "//button[contains(text(), 'Cerrar sesión')]"))
    )
    browser.find_element(By.XPATH, "//button[contains(text(), 'Cerrar sesión')]").click()
