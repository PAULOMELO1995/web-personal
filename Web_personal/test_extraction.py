from web_completo import WebScraper, SeleniumAutomaticaton
from bs4 import BeautifulSoup
import requests

TEST_URL = 'https://example.com'

print('=== Teste de extração usando requests (WebScraper) ===')
ws = WebScraper(timeout=10)
soup = ws.obter_pagina(TEST_URL)
if soup:
    html = soup.prettify()
    styles = soup.find_all('style')
    scripts = soup.find_all('script')
    print(f'HTML length: {len(html)}')
    print(f'styles found: {len(styles)}')
    print(f'scripts found: {len(scripts)}')
else:
    print('Falha na extração via requests')

print('\n=== Teste de extração usando SeleniumAutomaticaton (headless) ===')
try:
    bot = SeleniumAutomaticaton(headless=True)
    bot.navegar(TEST_URL)
    page = bot.driver.page_source
    bot.fechar()
    soup2 = BeautifulSoup(page, 'html.parser')
    html2 = soup2.prettify()
    styles2 = soup2.find_all('style')
    scripts2 = soup2.find_all('script')
    print(f'HTML length (selenium): {len(html2)}')
    print(f'styles found (selenium): {len(styles2)}')
    print(f'scripts found (selenium): {len(scripts2)}')
except Exception as e:
    print('Erro ao executar Selenium test:', e)
