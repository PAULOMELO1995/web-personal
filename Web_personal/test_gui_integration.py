"""
Teste de integração GUI: simula extração sem abrir a interface
"""
import sys
import threading
import time
from unittest.mock import Mock
from web_completo import WebScraperApp, WebScraper, SeleniumAutomaticaton
import tkinter as tk

def test_gui_integration():
    """Testa a integração da GUI com extração de dados"""
    print("\n📋 Teste de integração GUI...\n")
    
    # Criar root (sem exibir)
    root = tk.Tk()
    root.withdraw()  # Esconder a janela
    
    # Inicializar app
    app = WebScraperApp(root)
    
    # Verificar se os atributos existem
    assert hasattr(app, 'use_selenium'), "❌ Checkbox Selenium não encontrado"
    assert hasattr(app, 'text_html_editor'), "❌ Editor HTML não encontrado"
    assert hasattr(app, 'text_css_editor'), "❌ Editor CSS não encontrado"
    assert hasattr(app, 'text_js_editor'), "❌ Editor JS não encontrado"
    print("✅ Atributos da GUI validados")
    
    # Simular entrada de URL
    test_url = str(input(f"Qual site você deseja extrair? (Ex: https://example.com): "))
    
    app.entry_url.delete(0, tk.END)
    app.entry_url.insert(0, test_url)
    print(f"✅ URL definida: {test_url}")
    
    # Teste 1: Extração com requests (sem Selenium)
    print("\n--- Teste 1: Extração com requests (sem Selenium) ---")
    app.use_selenium.set(False)
    print("✅ Selenium desativado")
    
    # Simular extração
    app._extrair_thread(test_url)
    app.root.update()
    
    # Verificar se dados foram extraídos
    if app.dados_atuais:
        print(f"✅ Dados extraídos com requests")
        print(f"   - URL: {app.dados_atuais['url']}")
        print(f"   - Stats: {app.dados_atuais['stats']}")
    else:
        print("❌ Falha na extração com requests")
    
    # Teste 2: Extração com Selenium
    print("\n--- Teste 2: Extração com Selenium (headless) ---")
    app.use_selenium.set(True)
    app.dados_atuais = {}  # Limpar dados
    print("✅ Selenium ativado")
    
    # Simular extração com Selenium
    app._extrair_thread(test_url)
    app.root.update()
    
    # Verificar se dados foram extraídos com Selenium
    if app.dados_atuais:
        print(f"✅ Dados extraídos com Selenium")
        print(f"   - URL: {app.dados_atuais['url']}")
    else:
        print("❌ Falha na extração com Selenium")
    
    # Teste 3: Verificar se editores foram preenchidos
    print("\n--- Teste 3: Verificar preenchimento dos editores ---")
    html_content = app.text_html_editor.get(1.0, tk.END)
    css_content = app.text_css_editor.get(1.0, tk.END)
    js_content = app.text_js_editor.get(1.0, tk.END)
    
    if html_content.strip():
        print(f"✅ Editor HTML foi preenchido ({len(html_content)} chars)")
    else:
        print("⚠️  Editor HTML vazio")
    
    if css_content.strip():
        print(f"✅ Editor CSS foi preenchido ({len(css_content)} chars)")
    else:
        print("⚠️  Editor CSS vazio")
    
    if js_content.strip():
        print(f"✅ Editor JS foi preenchido ({len(js_content)} chars)")
    else:
        print("⚠️  Editor JS vazio")
    
    # Teste 4: Verificar se arquivos foram salvos em memória
    print("\n--- Teste 4: Verificar memória de arquivos ---")
    if app.arquivos_criados:
        print(f"✅ Arquivos em memória: {list(app.arquivos_criados.keys())}")
        for tipo, conteudo in app.arquivos_criados.items():
            print(f"   - {tipo.upper()}: {len(conteudo)} chars")
    else:
        print("⚠️  Nenhum arquivo em memória")
    
    # Fechar root
    root.destroy()
    
    print("\n✅ Testes da integração GUI concluídos com sucesso!")

if __name__ == '__main__':
    test_gui_integration()
