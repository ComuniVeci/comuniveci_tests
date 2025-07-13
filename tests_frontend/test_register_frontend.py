from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import uuid
import pytest

@pytest.mark.frontend
def test_frontend_register(browser, track_created_user_frontend):
    # Generar correo y usuario aleatorio
    random_username = f"testuser_{uuid.uuid4().hex[:6]}"
    random_email = f"{random_username}@example.com"
    password = "Password123"

    track_created_user_frontend(random_email)  # Registrar para limpieza

    # Ir al formulario de registro
    browser.get("http://localhost:8080/register.html")

    browser.find_element(By.ID, "username").send_keys(random_username)
    browser.find_element(By.ID, "email").send_keys(random_email)
    browser.find_element(By.ID, "password").send_keys(password)
    browser.find_element(By.CSS_SELECTOR, "button[type='submit']").click()

    # Esperar redirección al index (después del registro exitoso)
    try:
        WebDriverWait(browser, 10).until(
            lambda d: d.current_url in ["http://localhost:8080/", "http://localhost:8080/index.html"]
        )
    except TimeoutException:
        print("❌ No se redirigió al index después del registro.")
        assert False

    # Confirmar que aparece el saludo y botón de perfil
    nav = browser.find_element(By.ID, "nav-links")
    assert f"Hola, {random_username}" in nav.text
    assert "Perfil" in nav.text
    assert "Cerrar sesión" in nav.text

    # Hacer logout
    logout_btn = nav.find_element(By.XPATH, ".//button[contains(text(),'Cerrar sesión')]")
    logout_btn.click()

    WebDriverWait(browser, 5).until(
        EC.text_to_be_present_in_element((By.ID, "nav-links"), "Iniciar sesión")
    )

    nav_text_after_logout = browser.find_element(By.ID, "nav-links").text
    assert "Iniciar sesión" in nav_text_after_logout
    assert "Registrarse" in nav_text_after_logout
    assert f"Hola, {random_username}" not in nav_text_after_logout