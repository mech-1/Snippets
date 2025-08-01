import pytest
from django.urls import reverse
from selenium.webdriver.common.by import By


@pytest.mark.django_db
def test_view_snippets_button_on_homepage(browser, live_server):
    """
    Тест проверяет, что на главной странице есть кнопка "Посмотреть сниппеты",
    которая ведет по url-name 'snippets-list'
    """
    # Открываем главную страницу
    browser.get(f"{live_server.url}/")

    # Ищем кнопку "Посмотреть сниппеты" в header
    view_snippets_button = browser.find_element(By.XPATH, "//a[contains(text(), 'Посмотреть сниппеты')]")

    # Проверяем, что кнопка найдена
    assert view_snippets_button is not None

    # Проверяем, что кнопка имеет правильный href (должен вести на snippets-list)
    expected_url = f"{live_server.url}{reverse('snippets-list')}"
    actual_href = view_snippets_button.get_attribute('href')

    assert actual_href == expected_url, f"Ожидался URL: {expected_url}, получен: {actual_href}"