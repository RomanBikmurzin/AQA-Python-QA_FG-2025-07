import pytest
from playwright.sync_api import Page, expect


@pytest.mark.parametrize("query", ["qa", "aqa", "cars"])
def test_google_search_results_count(page: Page, query):
    # Переходим на Google
    page.goto("https://www.google.ru/")

    ## Принимаем куки, если появилось окно
    # try:
    #    page.locator("button:has-text('Принять все')").click(timeout=3000)
    # except:
    #    pass  # Если окна с куками нет, продолжаем

    # Вводим поисковый запрос
    search_box = page.locator("[name='q']")
    search_box.fill(query)
    search_box.press("Enter")

    # Ждем появления результатов
    results_locator = page.locator("#search .g")  # Локатор для каждого результата
    results_locator.first.wait_for()

    # Получаем все результаты
    results = results_locator.all()
    results_count = len(results)

    # Проверяем что результатов больше 5
    assert (
        results_count > 5
    ), f"Для запроса '{query}' найдено только {results_count} результатов"

    # Дополнительная проверка через expect (для лучшего сообщения об ошибке)
    expect(results_locator).to_have_count(
        lambda count: count > 5,
        message=f"Ожидалось более 5 результатов для '{query}', найдено {results_count}",
    )
