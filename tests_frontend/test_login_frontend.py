import time
import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

@pytest.mark.frontend
def test_frontend_login_and_logout(browser):
    browser.get("http://localhost:8080/login.html")

    # Completar formulario de login
    email_input = browser.find_element(By.ID, "email")
    password_input = browser.find_element(By.ID, "password")
    submit_button = browser.find_element(By.CSS_SELECTOR, "button[type='submit']")

    email_input.send_keys("admin@admin.com")
    password_input.send_keys("12345678")
    submit_button.click()

    # Esperar redirección
    WebDriverWait(browser, 5).until(
        EC.url_contains("localhost:8080")
    )

    assert browser.current_url.startswith("http://localhost:8080")

    # Esperar a que se cargue el header dinámico
    nav = WebDriverWait(browser, 5).until(
        EC.presence_of_element_located((By.ID, "nav-links"))
    )

    nav_text = nav.text
    assert "Hola, admin1" in nav_text
    assert "Administrar" in nav_text
    assert "Cerrar sesión" in nav_text

    # Hacer clic en "Cerrar sesión"
    logout_btn = nav.find_element(By.XPATH, ".//button[contains(text(),'Cerrar sesión')]")
    logout_btn.click()

    # Esperar a que cambie el contenido del header
    WebDriverWait(browser, 5).until(
        EC.text_to_be_present_in_element((By.ID, "nav-links"), "Iniciar sesión")
    )

    nav_text_after_logout = browser.find_element(By.ID, "nav-links").text
    assert "Iniciar sesión" in nav_text_after_logout
    assert "Registrarse" in nav_text_after_logout
    assert "Hola, admin1" not in nav_text_after_logout