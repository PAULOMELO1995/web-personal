# 🌐 ANALISADOR WEB COMPLETO - Extração, IA, Simulador e Guia de Códigos
# Sistema para análise e desenvolvimento de websites

import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox, filedialog
import requests
from bs4 import BeautifulSoup
import pandas as pd
from typing import List, Dict, Optional
import logging
import threading
import json
from datetime import datetime
import re
import webbrowser
import tempfile
import os
import html
import zipfile
import self
from undetected_chromedriver import ChromeOptions
import webdriver_manager
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options



# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ==================== MÓDULO SCRAPER ====================

class WebScraper:
    """Classe para web scraping ético e análise de dados"""
    
    def __init__(self, timeout: int = 10):
        self.timeout = timeout
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
    
    def obter_pagina(self, url: str) -> Optional[BeautifulSoup]:
        """Obter conteúdo HTML de uma página"""
        try:
            logger.info(f"Acessando: {url}")
            response = self.session.get(url, timeout=self.timeout)
            response.raise_for_status()
            return BeautifulSoup(response.content, 'html.parser')
        except requests.RequestException as e:
            logger.error(f"Erro ao acessar {url}: {e}")
            return None
    
    def extrair_titulos(self, soup: BeautifulSoup, nivel: int = 1) -> List[str]:
        """Extrair títulos de uma página"""
        tag = f'h{nivel}'
        titulos = soup.find_all(tag)
        return [t.get_text(strip=True) for t in titulos]
    def extrair_paragrafos(self, soup: BeautifulSoup) -> List[str]:
        """Extrair parágrafos"""
        paragrafos = soup.find_all('p')
        return [p.get_text(strip=True) for p in paragrafos if p.get_text(strip=True)]
    
    def extrair_links(self, soup: BeautifulSoup) -> List[Dict]:
        """Extrair links"""
        links = soup.find_all('a', href=True)
        return [{'texto': l.get_text(strip=True), 'url': l['href']} for l in links]
    
    def extrair_tabelas(self, soup: BeautifulSoup) -> List[Dict]:
        """Extrair tabelas"""
        tabelas = soup.find_all('table')
        resultado = []
        for tabela in tabelas:
            linhas = tabela.find_all('tr')
            dados = []
            for linha in linhas:
                colunas = linha.find_all(['td', 'th'])
                dados.append([col.get_text(strip=True) for col in colunas])
            resultado.append(dados)
        return resultado
    
    def extrair_metadados(self, soup: BeautifulSoup) -> Dict:
        """Extrair metadados"""
        return {
            'titulo': soup.title.string if soup.title else 'N/A',
            'descricao': soup.find('meta', {'name': 'description'})['content'] if soup.find('meta', {'name': 'description'}) else 'N/A'
        }
        

# =============Selenium=====================
class SeleniumAutomaticaton:
    def __init__(self, headless=False):
        # Configurações do navegador
        options = Options()
        if headless:
            options.add_argument("--headless")
        options.add_argument("--disable-gpu")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        # Inicializa o WebDriver automaticamente
        service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service, options=options)
        self.driver.implicitly_wait(30)

    def navegar(self, url):
        self.driver.get(url)

    def fechar(self):
        self.driver.quit()




# ==================== MÓDULO IA ====================

class IAAnalisadora:
    """Análise inteligente de dados extraídos"""
    
    def __init__(self):
        self.padroes_email = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
        self.padroes_telefone = r'[\(\+]?[0-9]{2,}[\)\s]?[0-9]{4,}[\-\s]?[0-9]{4,}'
        self.padroes_preco = r'R\$\s*[\d.,]+|[\d.,]+\s*(reais|BRL)'
        self.padroes_data = r'\d{1,2}/\d{1,2}/\d{2,4}|\d{4}-\d{1,2}-\d{1,2}'
    
    def detectar_padroes(self, texto: str) -> Dict:
        """Detectar padrões comuns"""
        return {
            'emails': re.findall(self.padroes_email, texto),
            'telefones': re.findall(self.padroes_telefone, texto),
            'precos': re.findall(self.padroes_preco, texto),
            'datas': re.findall(self.padroes_data, texto)
        }

# ==================== GUI APPLICATION ====================

class WebScraperApp:
    """Aplicação principal com interface Tkinter"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("🌐 Analisador Web Completo - Extração, Simulador e Guia de Códigos")
        self.root.geometry("1600x900")
        
        # Centralizar janela
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')
        
        self.scraper = WebScraper()
        self.ia = IAAnalisadora()
        self.dados_atuais = {}
        self.arquivos_criados = {}
        
        # Criar abas principais primeiro
        self._criar_abas_principais()
    
    def _criar_abas_principais(self):
        """Cria as abas principais da aplicação"""
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Criar frames para cada aba
        self.frame_extracao = ttk.Frame(self.notebook)
        self.frame_analise = ttk.Frame(self.notebook)
        self.frame_arquivos = ttk.Frame(self.notebook)
        
        # Adicionar abas ao notebook
        self.notebook.add(self.frame_extracao, text="📥 Extração")
        self.notebook.add(self.frame_analise, text="⚙️ Análise Completa")
        self.notebook.add(self.frame_arquivos, text="📂 Arquivos")
        
        # Criar conteúdo das abas
        self._criar_aba_extracao()
        self._criar_aba_analise_completa()
        self._criar_aba_arquivos()
    
    def _criar_aba_extracao(self):
        """Aba de extração de dados"""
        # Frame principal
        frame = ttk.Frame(self.frame_extracao)
        frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Painel de entrada de URL
        frame_url = ttk.LabelFrame(frame, text="🔗 URL para Extração", padding=10)
        frame_url.pack(fill=tk.X, pady=(0, 10))
        
        # Configuração de grid para alinhamento
        frame_url.grid_columnconfigure(1, weight=1)
        
        ttk.Label(frame_url, text="URL:", font=("Arial", 10)).grid(row=0, column=0, padx=5, pady=5, sticky="w")
        
        self.entry_url = ttk.Entry(frame_url, font=("Arial", 10))
        self.entry_url.grid(row=0, column=1, padx=5, pady=5, sticky="ew")
        self.entry_url.insert(0, "https://exemplo.com")
        # Opção: usar Selenium para renderizar JS
        self.use_selenium = tk.BooleanVar(value=False)
        chk_selenium = ttk.Checkbutton(frame_url, text="Renderizar com Selenium (executa JS)", variable=self.use_selenium)
        chk_selenium.grid(row=1, column=1, padx=5, pady=2, sticky="w")
        
        frame_botoes_url = ttk.Frame(frame_url)
        frame_botoes_url.grid(row=0, column=2, padx=5, pady=5)
        
        ttk.Button(frame_botoes_url, text="🔍 Extrair", 
                  command=self._extrair_dados, width=15).pack(side=tk.LEFT, padx=2)
        ttk.Button(frame_botoes_url, text="🗑️ Limpar", 
                  command=self._limpar, width=10).pack(side=tk.LEFT, padx=2)
        
        # Painel de botões rápidos
        frame_botoes = ttk.LabelFrame(frame, text="Extrações Rápidas", padding=10)
        frame_botoes.pack(fill=tk.X, pady=(0, 10))
        
        botoes_rapidos = [
            ("📝 Títulos H1", lambda: self._extrair_rapido('titulos_h1')),
            ("📋 Títulos H2", lambda: self._extrair_rapido('titulos_h2')),
            ("📄 Parágrafos", lambda: self._extrair_rapido('paragrafos')),
            ("🔗 Links", lambda: self._extrair_rapido('links')),
            ("📊 Tabelas", lambda: self._extrair_rapido('tabelas'))
        ]
        
        for texto, comando in botoes_rapidos:
            ttk.Button(frame_botoes, text=texto, command=comando).pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        
        # Painel de download
        frame_download = ttk.LabelFrame(frame, text="📥 Download dos Arquivos", padding=10)
        frame_download.pack(fill=tk.X, pady=(0, 10))
        
        botoes_download = [
            ("⬇️ HTML", self._download_html_site),
            ("⬇️ CSS", self._download_css_site),
            ("⬇️ JavaScript", self._download_js_site)
        ]
        
        for texto, comando in botoes_download:
            ttk.Button(frame_download, text=texto, command=comando).pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        
        # Área de resultados
        frame_resultado = ttk.LabelFrame(frame, text="📊 Resultados", padding=10)
        frame_resultado.pack(fill=tk.BOTH, expand=True)
        
        self.text_extracao = scrolledtext.ScrolledText(
            frame_resultado, 
            height=30, 
            font=("Consolas", 10),
            wrap=tk.WORD,
            bg="#f8f9fa",
            relief=tk.SUNKEN,
            borderwidth=1
        )
        self.text_extracao.pack(fill=tk.BOTH, expand=True, pady=(5, 0))
    
    def _criar_aba_analise_completa(self):
        """ABA PRINCIPAL: Análise Completa com Site Modelo + Editor de Código HTML/CSS/JavaScript"""
        
        # Frame principal da aba
        frame_main = ttk.Frame(self.frame_analise)
        frame_main.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Título
        ttk.Label(frame_main, 
                 text="📝 Criar Página: Site Modelo + Editor de Código HTML/CSS/JavaScript", 
                 font=("Arial", 12, "bold")).pack(anchor=tk.W, pady=(0, 10))
        
        # Container principal com 3 colunas
        main_paned = ttk.PanedWindow(frame_main, orient=tk.HORIZONTAL)
        main_paned.pack(fill=tk.BOTH, expand=True)
        
        # ========== COLUNA 1: SITE MODELO ==========
        self._criar_coluna_modelo(main_paned)
        
        # ========== COLUNA 2: EDITOR DE CÓDIGO COM MAIS EXEMPLOS JS ==========
        self._criar_coluna_editor_com_exemplos(main_paned)
        
        # ========== COLUNA 3: GUIA DE INTEGRAÇÃO + MONTAÇÃO ==========
        self._criar_coluna_integracao(main_paned)
        
        # Inserir conteúdo inicial nos editores
        self._inserir_conteudo_inicial_editores()
    
    def _criar_coluna_modelo(self, main_paned):
        """Cria a coluna do site modelo"""
        frame_modelo = ttk.LabelFrame(main_paned, text="📄 Site Modelo (Referência)", padding=10)
        main_paned.add(frame_modelo, weight=10)  # Alterado de 1 para 10
        
        # Título da seção
        ttk.Label(frame_modelo, 
                 text="Site analisado - use como guia:", 
                 font=("Arial", 9)).pack(anchor=tk.W, pady=(0, 5))
        
        # Área de texto para o modelo HTML
        self.text_html_modelo = scrolledtext.ScrolledText(
            frame_modelo, 
            font=("Consolas", 9),
            wrap=tk.WORD,
            bg="#f8f9fa",
            relief=tk.SUNKEN,
            borderwidth=1
        )
        self.text_html_modelo.pack(fill=tk.BOTH, expand=True)
        
        # Mensagem inicial
        self.text_html_modelo.insert(tk.END, 
            "⏳ Extraia dados de uma URL primeiro\n\n"
            "1. Vá para a aba '📥 Extração'\n"
            "2. Cole uma URL e clique em 'Extrair'\n"
            "3. O código HTML aparecerá aqui automaticamente\n\n"
            "Depois, use o código como referência para criar sua página personalizada."
        )
        self.text_html_modelo.config(state=tk.DISABLED)
        
        # Botões para interação com o modelo
        frame_botoes_modelo = ttk.Frame(frame_modelo)
        frame_botoes_modelo.pack(fill=tk.X, pady=(5, 0))
        
        ttk.Button(frame_botoes_modelo, 
                   text="📋 Copiar para Editor",
                   command=self._copiar_modelo_para_editor).pack(fill=tk.X, padx=2)
    
    def _criar_coluna_editor_com_exemplos(self, main_paned):
        """Cria a coluna do editor de código com muitos exemplos JS"""
        frame_editor = ttk.LabelFrame(main_paned, text="✏️ Editor de Código + Exemplos JS", padding=10)
        main_paned.add(frame_editor, weight=20)  # Alterado de 2 para 20
        
        # Notebook para as abas de código
        notebook_codigo = ttk.Notebook(frame_editor)
        notebook_codigo.pack(fill=tk.BOTH, expand=True)
        
        # Aba HTML
        self._criar_aba_html(notebook_codigo)
        
        # Aba CSS
        self._criar_aba_css(notebook_codigo)
        
        # Aba JavaScript com exemplos estendidos
        self._criar_aba_javascript_com_exemplos(notebook_codigo)
        
        # Aba Exemplos Práticos JS
        self._criar_aba_exemplos_praticos_js(notebook_codigo)
    
    def _criar_aba_html(self, notebook):
        """Cria a aba do editor HTML"""
        frame_html = ttk.Frame(notebook)
        notebook.add(frame_html, text="📄 HTML")
        
        # Frame para botões HTML
        frame_btns = ttk.Frame(frame_html)
        frame_btns.pack(fill=tk.X, pady=(0, 5))
        
        # Botões HTML
        botoes_html = [
            ("📥 Carregar Modelo", self._carregar_html_modelo),
            ("💾 Salvar", lambda: self._salvar_arquivo('html')),
            ("📥 Download", lambda: self._download_arquivo('html')),
            ("🗑️ Limpar", lambda: self._limpar_editor('html')),
            ("👁️ Preview", self._preview_html)
        ]
        
        for texto, comando in botoes_html:
            btn = ttk.Button(frame_btns, text=texto, command=comando)
            btn.pack(side=tk.LEFT, padx=2)
        
        # Editor HTML
        self.text_html_editor = scrolledtext.ScrolledText(
            frame_html, 
            font=("Consolas", 11),
            wrap=tk.WORD,
            bg="#f8f9fa",
            relief=tk.SUNKEN,
            borderwidth=1,
            undo=True
        )
        self.text_html_editor.pack(fill=tk.BOTH, expand=True)
    
    def _criar_aba_css(self, notebook):
        """Cria a aba do editor CSS"""
        frame_css = ttk.Frame(notebook)
        notebook.add(frame_css, text="🎨 CSS")
        
        # Frame para botões CSS
        frame_btns = ttk.Frame(frame_css)
        frame_btns.pack(fill=tk.X, pady=(0, 5))
        
        # Botões CSS
        botoes_css = [
            ("💾 Salvar", lambda: self._salvar_arquivo('css')),
            ("📥 Download", lambda: self._download_arquivo('css')),
            ("🗑️ Limpar", lambda: self._limpar_editor('css')),
            ("👁️ Preview", self._preview_html)
        ]
        
        for texto, comando in botoes_css:
            btn = ttk.Button(frame_btns, text=texto, command=comando)
            btn.pack(side=tk.LEFT, padx=2)
        
        # Editor CSS
        self.text_css_editor = scrolledtext.ScrolledText(
            frame_css, 
            font=("Consolas", 11),
            wrap=tk.WORD,
            bg="#f8f9fa",
            relief=tk.SUNKEN,
            borderwidth=1,
            undo=True
        )
        self.text_css_editor.pack(fill=tk.BOTH, expand=True)
    
    def _criar_aba_javascript_com_exemplos(self, notebook):
        """Cria a aba do editor JavaScript com muitos exemplos"""
        frame_js = ttk.Frame(notebook)
        notebook.add(frame_js, text="⚡ JavaScript + Exemplos")
        
        # Criar paned para dividir espaço entre editor e exemplos
        js_paned = ttk.PanedWindow(frame_js, orient=tk.VERTICAL)
        js_paned.pack(fill=tk.BOTH, expand=True)
        
        # Parte superior: Editor JavaScript
        frame_editor_js = ttk.Frame(js_paned)
        js_paned.add(frame_editor_js, weight=1)
        
        # Frame para botões JS
        frame_btns = ttk.Frame(frame_editor_js)
        frame_btns.pack(fill=tk.X, pady=(0, 5))
        
        # Botões JavaScript
        botoes_js = [
            ("💾 Salvar", lambda: self._salvar_arquivo('js')),
            ("📥 Download", lambda: self._download_arquivo('js')),
            ("🗑️ Limpar", lambda: self._limpar_editor('js')),
            ("👁️ Preview", self._preview_html)
        ]
        
        for texto, comando in botoes_js:
            btn = ttk.Button(frame_btns, text=texto, command=comando)
            btn.pack(side=tk.LEFT, padx=2)
        
        # Editor JavaScript
        self.text_js_editor = scrolledtext.ScrolledText(
            frame_editor_js, 
            font=("Consolas", 11),
            wrap=tk.WORD,
            bg="#f8f9fa",
            relief=tk.SUNKEN,
            borderwidth=1,
            undo=True
        )
        self.text_js_editor.pack(fill=tk.BOTH, expand=True)
        
        # Parte inferior: Exemplos JavaScript
        frame_exemplos = ttk.LabelFrame(js_paned, text="📚 Exemplos JavaScript", padding=10)
        js_paned.add(frame_exemplos, weight=1)
        
        # Notebook para os exemplos
        notebook_exemplos = ttk.Notebook(frame_exemplos)
        notebook_exemplos.pack(fill=tk.BOTH, expand=True)
        
        # Aba: Manipulação DOM
        frame_dom = ttk.Frame(notebook_exemplos)
        notebook_exemplos.add(frame_dom, text="DOM")
        
        exemplos_dom = scrolledtext.ScrolledText(
            frame_dom,
            font=("Consolas", 9),
            wrap=tk.WORD,
            bg="#f0f8ff",
            relief=tk.SUNKEN,
            borderwidth=1,
            height=10
        )
        exemplos_dom.pack(fill=tk.BOTH, expand=True)
        
        exemplos_dom.insert(tk.END, """// 1. Selecionar elementos
const elemento = document.getElementById('id');
const elementos = document.querySelectorAll('.classe');
const primeiro = document.querySelector('#id .classe');

// 2. Manipular conteúdo
elemento.textContent = 'Novo texto';
elemento.innerHTML = '<strong>HTML</strong>';
elemento.innerText = 'Texto puro';

// 3. Manipular atributos
elemento.setAttribute('data-id', '123');
const valor = elemento.getAttribute('data-id');
elemento.removeAttribute('data-id');

// 4. Manipular classes
elemento.classList.add('nova-classe');
elemento.classList.remove('classe-antiga');
elemento.classList.toggle('ativo');
const temClasse = elemento.classList.contains('ativo');

// 5. Criar e remover elementos
const novoElemento = document.createElement('div');
novoElemento.textContent = 'Novo elemento';
elemento.appendChild(novoElemento);
elemento.removeChild(novoElemento);

// 6. Estilos dinâmicos
elemento.style.backgroundColor = 'blue';
elemento.style.fontSize = '20px';
elemento.style.display = 'none';""")
        exemplos_dom.config(state=tk.DISABLED)
        
        # Aba: Eventos
        frame_eventos = ttk.Frame(notebook_exemplos)
        notebook_exemplos.add(frame_eventos, text="Eventos")
        
        exemplos_eventos = scrolledtext.ScrolledText(
            frame_eventos,
            font=("Consolas", 9),
            wrap=tk.WORD,
            bg="#f0f8ff",
            relief=tk.SUNKEN,
            borderwidth=1,
            height=10
        )
        exemplos_eventos.pack(fill=tk.BOTH, expand=True)
        
        exemplos_eventos.insert(tk.END, """// 1. Eventos de clique
elemento.addEventListener('click', function(event) {
    console.log('Clicado!', event.target);
});

// 2. Eventos de teclado
document.addEventListener('keydown', function(event) {
    console.log('Tecla pressionada:', event.key);
    if (event.key === 'Enter') {
        console.log('Enter pressionado!');
    }
});

// 3. Eventos de formulário
formulario.addEventListener('submit', function(event) {
    event.preventDefault();
    console.log('Formulário enviado');
});

// 4. Eventos de mouse
elemento.addEventListener('mouseenter', function() {
    this.style.backgroundColor = 'yellow';
});
elemento.addEventListener('mouseleave', function() {
    this.style.backgroundColor = '';
});

// 5. Eventos de input
input.addEventListener('input', function() {
    console.log('Valor alterado:', this.value);
});

// 6. Eventos de mudança
select.addEventListener('change', function() {
    console.log('Opção selecionada:', this.value);
});""")
        exemplos_eventos.config(state=tk.DISABLED)
        
        # Aba: APIs e Fetch
        frame_api = ttk.Frame(notebook_exemplos)
        notebook_exemplos.add(frame_api, text="APIs")
        
        exemplos_api = scrolledtext.ScrolledText(
            frame_api,
            font=("Consolas", 9),
            wrap=tk.WORD,
            bg="#f0f8ff",
            relief=tk.SUNKEN,
            borderwidth=1,
            height=10
        )
        exemplos_api.pack(fill=tk.BOTH, expand=True)
        
        exemplos_api.insert(tk.END, """// 1. Fetch básico (GET)
async function buscarDados(url) {
    try {
        const response = await fetch(url);
        if (!response.ok) {
            throw new Error('HTTP error! status: ${response.status}');
        }
        const data = await response.json();
        return data;
    } catch (error) {
        console.error('Erro ao buscar dados:', error);
        throw error;
    }
}

// 2. Fetch com POST
async function enviarDados(url, dados) {
    try {
        const response = await fetch(url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(dados)
        });
        
        const result = await response.json();
        return result;
    } catch (error) {
        console.error('Erro ao enviar dados:', error);
        throw error;
    }
}

// 3. Upload de arquivo
async function uploadArquivo(url, arquivo) {
    const formData = new FormData();
    formData.append('file', arquivo);
    
    try {
        const response = await fetch(url, {
            method: 'POST',
            body: formData
        });
        
        return await response.json();
    } catch (error) {
        console.error('Erro no upload:', error);
        throw error;
    }
}""")
        exemplos_api.config(state=tk.DISABLED)
    
    def _criar_aba_exemplos_praticos_js(self, notebook):
        """Cria aba com exemplos práticos de JavaScript"""
        frame_praticos = ttk.Frame(notebook)
        notebook.add(frame_praticos, text="🛠️ Práticos JS")
        
        # Área de texto com exemplos
        exemplos_praticos = scrolledtext.ScrolledText(
            frame_praticos,
            font=("Consolas", 9),
            wrap=tk.WORD,
            bg="#f0f8ff",
            relief=tk.SUNKEN,
            borderwidth=1
        )
        exemplos_praticos.pack(fill=tk.BOTH, expand=True)
        
        exemplos_conteudo = """// ===== EXEMPLOS PRÁTICOS DE JAVASCRIPT =====

// 1. VALIDAÇÃO DE FORMULÁRIO
function validarFormulario(form) {
    const campos = form.querySelectorAll('[required]');
    let valido = true;
    
    campos.forEach(campo => {
        if (!campo.value.trim()) {
            campo.style.borderColor = 'red';
            valido = false;
        } else {
            campo.style.borderColor = 'green';
        }
    });
    
    return valido;
}

// 2. MÁSCARA DE TELEFONE
function mascaraTelefone(input) {
    let valor = input.value.replace(/\\D/g, '');
    
    if (valor.length <= 10) {
        valor = valor.replace(/(\\d{2})(\\d)/, '($1) $2');
        valor = valor.replace(/(\\d{4})(\\d)/, '$1-$2');
    } else {
        valor = valor.replace(/(\\d{2})(\\d)/, '($1) $2');
        valor = valor.replace(/(\\d{5})(\\d)/, '$1-$2');
    }
    
    input.value = valor;
}

// 3. DARK MODE TOGGLE
function toggleDarkMode() {
    const body = document.body;
    const isDark = body.classList.toggle('dark-mode');
    localStorage.setItem('darkMode', isDark);
    
    if (isDark) {
        body.style.backgroundColor = '#1a1a1a';
        body.style.color = '#ffffff';
    } else {
        body.style.backgroundColor = '#ffffff';
        body.style.color = '#000000';
    }
}

// 4. CARREGAMENTO LAZY DE IMAGENS
function lazyLoadImages() {
    const images = document.querySelectorAll('img[data-src]');
    
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const img = entry.target;
                img.src = img.dataset.src;
                img.removeAttribute('data-src');
                observer.unobserve(img);
            }
        });
    });
    
    images.forEach(img => observer.observe(img));
}

// 5. DEBOUNCE PARA PESQUISA
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

// 6. CONTADOR DE CARACTERES
function contadorCaracteres(textarea, contador) {
    textarea.addEventListener('input', function() {
        const max = this.maxLength || 500;
        const atual = this.value.length;
        contador.textContent = `${atual}/${max}`;
        
        if (atual > max * 0.8) {
            contador.style.color = 'orange';
        } else {
            contador.style.color = 'green';
        }
    });
}

// 7. MODAL DINÂMICO
function abrirModal(conteudo) {
    const modal = document.createElement('div');
    modal.style.cssText = `
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: rgba(0,0,0,0.5);
        display: flex;
        justify-content: center;
        align-items: center;
        z-index: 1000;
    `;
    
    modal.innerHTML = `
        <div style="background: white; padding: 30px; border-radius: 10px; max-width: 500px;">
            ${conteudo}
            <button onclick="this.parentElement.parentElement.remove()">Fechar</button>
        </div>
    `;
    
    document.body.appendChild(modal);
}

// 8. COPIAR PARA CLIPBOARD
function copiarParaClipboard(texto) {
    navigator.clipboard.writeText(texto)
        .then(() => alert('Copiado!'))
        .catch(err => console.error('Erro ao copiar:', err));
}

// 9. ANIMAÇÃO DE SCROLL SUAVE
function scrollSuave(alvo) {
    const elemento = document.querySelector(alvo);
    if (elemento) {
        elemento.scrollIntoView({ behavior: 'smooth' });
    }
}

// 10. FORMATAÇÃO DE MOEDA
function formatarMoeda(valor) {
    return new Intl.NumberFormat('pt-BR', {
        style: 'currency',
        currency: 'BRL'
    }).format(valor);
}"""
        
        exemplos_praticos.insert(tk.END, exemplos_conteudo)
        exemplos_praticos.config(state=tk.DISABLED)
    
    def _criar_coluna_integracao(self, main_paned):
        """Cria a coluna de guia e montação de página"""
        frame_integracao = ttk.LabelFrame(main_paned, 
                                         text="📚 Guia de Integração + Montação", 
                                         padding=10)
        main_paned.add(frame_integracao, weight=15)  # Alterado de 1.5 para 15
        
        # Notebook para as abas
        notebook_integracao = ttk.Notebook(frame_integracao)
        notebook_integracao.pack(fill=tk.BOTH, expand=True)
        
        # Aba 1: Guia de Integração
        self._criar_aba_guia_integracao(notebook_integracao)
        
        # Aba 2: Exemplo Prático Completo
        self._criar_aba_exemplo_pratico_completo(notebook_integracao)
        
        # Aba 3: Montação da Página
        self._criar_aba_montacao_pagina(notebook_integracao)
        
        # Aba 4: Teste Rápido
        self._criar_aba_teste_rapido(notebook_integracao)
    
    def _criar_aba_guia_integracao(self, notebook):
        """Cria aba com guia completa de integração"""
        frame_guia = ttk.Frame(notebook)
        notebook.add(frame_guia, text="📖 Guia Completa")
        
        # Área de texto da guia
        text_guia = scrolledtext.ScrolledText(
            frame_guia, 
            font=("Consolas", 10),
            wrap=tk.WORD,
            bg="#f8f9fa",
            relief=tk.SUNKEN,
            borderwidth=1
        )
        text_guia.pack(fill=tk.BOTH, expand=True)
        
        # Conteúdo da guia
        guia_conteudo = """📚 GUIA COMPLETA DE INTEGRAÇÃO HTML + CSS + JAVASCRIPT
═══════════════════════════════════════════════════════════

🏗️ 1. ESTRUTURA BÁSICA DE UMA PÁGINA WEB
─────────────────────────────────────────

HTML (Estrutura):
<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Título da Página</title>
    <link rel="stylesheet" href="estilo.css">
</head>
<body>
    <!-- Conteúdo visível -->
    <script src="script.js"></script>
</body>
</html>

CSS (Estilo - arquivo estilo.css):
/* Reset básico */
* { margin: 0; padding: 0; box-sizing: border-box; }

body {
    font-family: Arial, sans-serif;
    line-height: 1.6;
}

JavaScript (Interatividade - arquivo script.js):
document.addEventListener('DOMContentLoaded', function() {
    // Código executa quando DOM está pronto
});

🎯 2. COMO OS TRÊS TRABALHAM JUNTOS
──────────────────────────────────

1. HTML define a ESTRUTURA:
   - Tags semânticas (header, main, footer, section, article)
   - Atributos (id, class, data-*)
   - Formulários e inputs

2. CSS define a APARÊNCIA:
   - Cores, fontes, espaçamentos
   - Layout (Flexbox, Grid)
   - Animações e transições
   - Responsividade

3. JavaScript define o COMPORTAMENTO:
   - Manipulação do DOM
   - Eventos (cliques, teclas, formulários)
   - Comunicação com APIs
   - Validações e cálculos

🔗 3. PONTOS DE INTEGRAÇÃO
──────────────────────────

HTML -> CSS:
• Classes: <div class="container">
• IDs: <h1 id="titulo">
• Atributos: <input type="text" data-validate="email">

HTML -> JavaScript:
• IDs para seleção: document.getElementById('id')
• Classes para múltiplos: document.querySelectorAll('.classe')
• Atributos data-*: elemento.dataset.validacao

CSS -> JavaScript:
• Manipulação de classes: elemento.classList.toggle('ativo')
• Estilos dinâmicos: elemento.style.color = 'red'
• Animação via classes: .fade-in { animation: fade 1s; }

🔄 4. FLUXO DE TRABALHO TÍPICO
──────────────────────────────

1. HTML (Estrutura inicial):
   <button id="meuBotao">Clique aqui</button>
   <p id="mensagem"></p>

2. CSS (Estilização):
   #meuBotao {
       background: blue;
       color: white;
       padding: 10px;
   }

3. JavaScript (Interação):
   document.getElementById('meuBotao').addEventListener('click', function() {
       document.getElementById('mensagem').textContent = 'Botão clicado!';
   });

⚡ 5. BOAS PRÁTICAS DE INTEGRAÇÃO
─────────────────────────────────

1. Separação de Responsabilidades:
   • HTML = estrutura
   • CSS = apresentação
   • JS = comportamento

2. Semântica HTML:
   • Use tags semânticas (nav, section, article)
   • Não use div para tudo

3. CSS Modulável:
   • Use classes reutilizáveis
   • Seguindo BEM, SMACSS ou OOCSS

4. JavaScript Não Intrusivo:
   • Use addEventListener em vez de onclick=""
   • Mantenha JS separado do HTML

5. Performance:
   • CSS no <head>
   • JS no final do <body> ou com defer
   • Imagens otimizadas

🔧 6. FERRAMENTAS DE DESENVOLVIMENTO
────────────────────────────────────

• Chrome DevTools: F12 para inspecionar
• Console JavaScript: console.log(), .error(), .warn()
• Network tab: Monitorar requisições
• Sources: Debug de código
• Lighthouse: Auditoria de performance"""
        
        text_guia.insert(tk.END, guia_conteudo)
        text_guia.config(state=tk.DISABLED)
    
    def _criar_aba_exemplo_pratico_completo(self, notebook):
        """Cria aba com exemplo prático completo"""
        frame_exemplo = ttk.Frame(notebook)
        notebook.add(frame_exemplo, text="🛠️ Exemplo Prático")
        
        # Área de texto com exemplo
        text_exemplo = scrolledtext.ScrolledText(
            frame_exemplo, 
            font=("Consolas", 9),
            wrap=tk.WORD,
            bg="#f0f8ff",
            relief=tk.SUNKEN,
            borderwidth=1
        )
        text_exemplo.pack(fill=tk.BOTH, expand=True)
        
        exemplo_conteudo = """🛠️ EXEMPLO PRÁTICO: FORMULÁRIO INTELIGENTE
═══════════════════════════════════════════════════════════

HTML:
<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Formulário Inteligente</title>
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <div class="container">
        <h1>📝 Formulário de Contato</h1>
        <form id="formContato">
            <div class="form-group">
                <label for="nome">Nome:</label>
                <input type="text" id="nome" required>
                <div class="feedback" id="feedbackNome"></div>
            </div>
            
            <div class="form-group">
                <label for="email">E-mail:</label>
                <input type="email" id="email" required>
                <div class="feedback" id="feedbackEmail"></div>
            </div>
            
            <div class="form-group">
                <label for="mensagem">Mensagem:</label>
                <textarea id="mensagem" rows="4" required></textarea>
                <div class="contador">Caracteres: <span id="contador">0</span>/500</div>
            </div>
            
            <button type="submit" class="btn-enviar">Enviar</button>
            <div id="resultado"></div>
        </form>
    </div>
    
    <script src="script.js"></script>
</body>
</html>

CSS (style.css):
.container {
    max-width: 600px;
    margin: 0 auto;
    padding: 20px;
}

.form-group {
    margin-bottom: 20px;
}

label {
    display: block;
    margin-bottom: 5px;
    font-weight: bold;
}

input, textarea {
    width: 100%;
    padding: 10px;
    border: 2px solid #ddd;
    border-radius: 5px;
    font-size: 16px;
}

input:focus, textarea:focus {
    border-color: #4CAF50;
    outline: none;
}

.btn-enviar {
    background: #4CAF50;
    color: white;
    padding: 12px 24px;
    border: none;
    border-radius: 5px;
    cursor: pointer;
    font-size: 16px;
}

.btn-enviar:hover {
    background: #45a049;
}

.feedback {
    font-size: 14px;
    margin-top: 5px;
}

.contador {
    font-size: 14px;
    color: #666;
    text-align: right;
}

#resultado {
    margin-top: 20px;
    padding: 15px;
    border-radius: 5px;
    display: none;
}

JavaScript (script.js):
document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('formContato');
    const nomeInput = document.getElementById('nome');
    const emailInput = document.getElementById('email');
    const mensagemTextarea = document.getElementById('mensagem');
    const contador = document.getElementById('contador');
    const resultadoDiv = document.getElementById('resultado');
    
    // Validação em tempo real do nome
    nomeInput.addEventListener('input', function() {
        const nome = this.value.trim();
        const feedback = document.getElementById('feedbackNome');
        
        if (nome.length < 3) {
            feedback.textContent = 'Nome muito curto (mínimo 3 caracteres)';
            feedback.style.color = 'red';
            this.style.borderColor = 'red';
        } else {
            feedback.textContent = '✓ Nome válido';
            feedback.style.color = 'green';
            this.style.borderColor = 'green';
        }
    });
    
    // Validação de email
    emailInput.addEventListener('input', function() {
        const email = this.value.trim();
        const feedback = document.getElementById('feedbackEmail');
        const emailRegex = /^[^\\s@]+@[^\\s@]+\\.[^\\s@]+$/;
        
        if (!emailRegex.test(email)) {
            feedback.textContent = 'Email inválido';
            feedback.style.color = 'red';
            this.style.borderColor = 'red';
        } else {
            feedback.textContent = '✓ Email válido';
            feedback.style.color = 'green';
            this.style.borderColor = 'green';
        }
    });
    
    // Contador de caracteres
    mensagemTextarea.addEventListener('input', function() {
        const caracteres = this.value.length;
        contador.textContent = caracteres;
        
        if (caracteres > 450) {
            contador.style.color = 'orange';
        } else if (caracteres > 480) {
            contador.style.color = 'red';
        } else {
            contador.style.color = 'green';
        }
    });
    
    // Submissão do formulário
    form.addEventListener('submit', function(event) {
        event.preventDefault();
        
        // Validar todos os campos
        const nomeValido = nomeInput.value.trim().length >= 3;
        const emailValido = /^[^\\s@]+@[^\\s@]+\\.[^\\s@]+$/.test(emailInput.value.trim());
        const mensagemValida = mensagemTextarea.value.trim().length > 0;
        
        if (nomeValido && emailValido && mensagemValida) {
            // Simular envio
            resultadoDiv.textContent = 'Enviando...';
            resultadoDiv.style.backgroundColor = '#fff3cd';
            resultadoDiv.style.color = '#856404';
            resultadoDiv.style.display = 'block';
            
            setTimeout(() => {
                resultadoDiv.textContent = '✅ Mensagem enviada com sucesso!';
                resultadoDiv.style.backgroundColor = '#d4edda';
                resultadoDiv.style.color = '#155724';
                
                // Limpar formulário
                form.reset();
                contador.textContent = '0';
                contador.style.color = 'green';
                
                document.querySelectorAll('.feedback').forEach(fb => {
                    fb.textContent = '';
                });
                
                document.querySelectorAll('input, textarea').forEach(input => {
                    input.style.borderColor = '#ddd';
                });
                
            }, 1500);
        } else {
            resultadoDiv.textContent = '❌ Corrija os erros antes de enviar.';
            resultadoDiv.style.backgroundColor = '#f8d7da';
            resultadoDiv.style.color = '#721c24';
            resultadoDiv.style.display = 'block';
        }
    });
});

📋 RESUMO DA INTEGRAÇÃO:
1. HTML: Define estrutura do formulário
2. CSS: Estiliza os elementos para melhor UX
3. JavaScript: Adiciona validação, contagem e interação"""
        
        text_exemplo.insert(tk.END, exemplo_conteudo)
        text_exemplo.config(state=tk.DISABLED)
    
    def _criar_aba_montacao_pagina(self, notebook):
        """Cria aba com ferramenta de montação de página"""
        frame_montacao = ttk.Frame(notebook)
        notebook.add(frame_montacao, text="🧩 Montar Página")
        
        # Título
        ttk.Label(frame_montacao, 
                 text="Monte sua página passo a passo:", 
                 font=("Arial", 10, "bold")).pack(anchor=tk.W, pady=(0, 10))
        
        # Notebook para etapas
        notebook_etapas = ttk.Notebook(frame_montacao)
        notebook_etapas.pack(fill=tk.BOTH, expand=True)
        
        # Etapa 1: Estrutura HTML
        frame_etapa1 = ttk.Frame(notebook_etapas)
        notebook_etapas.add(frame_etapa1, text="1️⃣ HTML")
        
        ttk.Label(frame_etapa1, text="Escolha a estrutura base:", 
                 font=("Arial", 9, "bold")).pack(anchor=tk.W, pady=(0, 5))
        
        # Opções de estrutura
        estruturas = [
            ("Página Simples", "simples"),
            ("Blog/Artigo", "blog"),
            ("Portfólio", "portfolio"),
            ("Loja/E-commerce", "ecommerce"),
            ("Dashboard", "dashboard")
        ]
        
        self.var_estrutura = tk.StringVar(value="simples")
        
        for texto, valor in estruturas:
            rb = ttk.Radiobutton(frame_etapa1, text=texto, variable=self.var_estrutura, value=valor)
            rb.pack(anchor=tk.W, padx=20, pady=2)
        
        # Botão para gerar estrutura
        ttk.Button(frame_etapa1, text="🧱 Gerar Estrutura HTML", 
                  command=self._gerar_estrutura_html).pack(pady=10)
        
        # Etapa 2: Estilos CSS
        frame_etapa2 = ttk.Frame(notebook_etapas)
        notebook_etapas.add(frame_etapa2, text="2️⃣ CSS")
        
        ttk.Label(frame_etapa2, text="Escolha o tema de cores:", 
                 font=("Arial", 9, "bold")).pack(anchor=tk.W, pady=(0, 5))
        
        # Temas de cores
        temas = [
            ("Claro Padrão", "claro"),
            ("Escuro Moderno", "escuro"),
            ("Azul Corporativo", "azul"),
            ("Verde Natureza", "verde"),
            ("Rosa Vibrante", "rosa")
        ]
        
        self.var_tema = tk.StringVar(value="claro")
        
        for texto, valor in temas:
            rb = ttk.Radiobutton(frame_etapa2, text=texto, variable=self.var_tema, value=valor)
            rb.pack(anchor=tk.W, padx=20, pady=2)
        
        # Slider para tamanho da fonte
        ttk.Label(frame_etapa2, text="Tamanho da fonte base:", 
                 font=("Arial", 9)).pack(anchor=tk.W, pady=(10, 0))
        
        self.var_tamanho_fonte = tk.IntVar(value=16)
        slider_fonte = ttk.Scale(frame_etapa2, from_=12, to=24, variable=self.var_tamanho_fonte, 
                               orient=tk.HORIZONTAL, length=200)
        slider_fonte.pack(anchor=tk.W, padx=20, pady=5)
        
        ttk.Label(frame_etapa2, text=f"Tamanho atual: {self.var_tamanho_fonte.get()}px").pack(anchor=tk.W, padx=20)
        
        # Botão para gerar CSS
        ttk.Button(frame_etapa2, text="🎨 Gerar Estilos CSS", 
                  command=self._gerar_estilos_css).pack(pady=10)
        
        # Etapa 3: Funcionalidades JS
        frame_etapa3 = ttk.Frame(notebook_etapas)
        notebook_etapas.add(frame_etapa3, text="3️⃣ JavaScript")
        
        ttk.Label(frame_etapa3, text="Adicione funcionalidades:", 
                 font=("Arial", 9, "bold")).pack(anchor=tk.W, pady=(0, 5))
        
        # Checkboxes de funcionalidades
        self.var_funcionalidades = {
            'menu_responsivo': tk.BooleanVar(value=True),
            'validacao_formulario': tk.BooleanVar(value=True),
            'carrossel_imagens': tk.BooleanVar(value=False),
            'modal_popup': tk.BooleanVar(value=False),
            'dark_mode': tk.BooleanVar(value=False),
            'animacoes': tk.BooleanVar(value=True)
        }
        
        funcionalidades = [
            ("Menu Responsivo", 'menu_responsivo'),
            ("Validação de Formulário", 'validacao_formulario'),
            ("Carrossel de Imagens", 'carrossel_imagens'),
            ("Modal/Popup", 'modal_popup'),
            ("Modo Escuro", 'dark_mode'),
            ("Animações Suaves", 'animacoes')
        ]
        
        for texto, chave in funcionalidades:
            cb = ttk.Checkbutton(frame_etapa3, text=texto, 
                               variable=self.var_funcionalidades[chave])
            cb.pack(anchor=tk.W, padx=20, pady=2)
        
        # Botão para gerar JavaScript
        ttk.Button(frame_etapa3, text="⚡ Gerar Funcionalidades JS", 
                  command=self._gerar_funcionalidades_js).pack(pady=10)
        
        # Etapa 4: Integração e Exportação
        frame_etapa4 = ttk.Frame(notebook_etapas)
        notebook_etapas.add(frame_etapa4, text="4️⃣ Exportar")
        
        ttk.Label(frame_etapa4, text="Integre e exporte sua página:", 
                 font=("Arial", 9, "bold")).pack(anchor=tk.W, pady=(0, 10))
        
        # Botões de exportação
        botoes_exportacao = [
            ("🧩 Integrar Componentes", self._integrar_componentes),
            ("👁️ Preview Completo", self._preview_completo),
            ("📦 Exportar como ZIP", self._exportar_zip),
            ("🚀 Publicar Online", self._publicar_online)
        ]
        
        for texto, comando in botoes_exportacao:
            btn = ttk.Button(frame_etapa4, text=texto, command=comando)
            btn.pack(fill=tk.X, padx=20, pady=5)
    
    def _criar_aba_teste_rapido(self, notebook):
        """Cria aba para teste rápido de código"""
        frame_teste = ttk.Frame(notebook)
        notebook.add(frame_teste, text="⚡ Teste Rápido")
        
        # Área para código de teste
        ttk.Label(frame_teste, text="Teste seu código HTML/CSS/JS aqui:", 
                 font=("Arial", 9, "bold")).pack(anchor=tk.W, pady=(0, 5))
        
        self.text_teste_rapido = scrolledtext.ScrolledText(
            frame_teste, 
            font=("Consolas", 10),
            wrap=tk.WORD,
            bg="#f8f9fa",
            relief=tk.SUNKEN,
            borderwidth=1,
            height=15
        )
        self.text_teste_rapido.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        # Conteúdo inicial de teste
        codigo_teste = """<!-- Teste rápido de integração -->
<div id="testeContainer" style="padding: 20px; border: 2px dashed #ccc; border-radius: 10px;">
    <h2 style="color: #667eea;">Teste Rápido</h2>
    <p>Edite este código e clique em "Executar Teste"</p>
    <button onclick="testarFuncao()" style="background: #667eea; color: white; padding: 10px; border: none; border-radius: 5px; cursor: pointer;">
        Clique para testar
    </button>
    <div id="resultadoTeste" style="margin-top: 10px;"></div>
</div>

<style>
    #testeContainer {
        font-family: Arial, sans-serif;
        transition: all 0.3s;
    }
    #testeContainer:hover {
        border-color: #667eea;
        box-shadow: 0 0 10px rgba(102, 126, 234, 0.3);
    }
</style>

<script>
    function testarFuncao() {
        const resultado = document.getElementById('resultadoTeste');
        resultado.innerHTML = '<p style="color: green;">✅ Teste executado com sucesso!</p>';
        resultado.innerHTML += '<p>Data/hora: ' + new Date().toLocaleString() + '</p>';
    }
</script>"""
        
        self.text_teste_rapido.insert(tk.END, codigo_teste)
        
        # Botões de teste
        frame_botoes_teste = ttk.Frame(frame_teste)
        frame_botoes_teste.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Button(frame_botoes_teste, text="▶️ Executar Teste", 
                  command=self._executar_teste_rapido).pack(side=tk.LEFT, padx=5)
        ttk.Button(frame_botoes_teste, text="🗑️ Limpar Teste", 
                  command=self._limpar_teste_rapido).pack(side=tk.LEFT, padx=5)
        ttk.Button(frame_botoes_teste, text="💾 Salvar Teste", 
                  command=self._salvar_teste_rapido).pack(side=tk.LEFT, padx=5)
    
    def _criar_aba_arquivos(self):
        """Aba para visualizar arquivos baixados"""
        frame_principal = ttk.Frame(self.frame_arquivos)
        frame_principal.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Painel Superior: Botões
        frame_botoes = ttk.Frame(frame_principal)
        frame_botoes.pack(fill=tk.X, pady=10)
        
        ttk.Button(frame_botoes, text="🔄 Atualizar Lista", 
                  command=self._atualizar_lista_arquivos).pack(side=tk.LEFT, padx=5)
        ttk.Button(frame_botoes, text="🗑️ Limpar Todos", 
                  command=self._limpar_todos_arquivos).pack(side=tk.LEFT, padx=5)
        
        # Painel esquerdo: Lista de arquivos
        frame_esquerdo = ttk.Frame(frame_principal)
        frame_esquerdo.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 5))
        
        ttk.Label(frame_esquerdo, text="📂 Arquivos Salvos:", 
                 font=("Arial", 10, "bold")).pack(anchor=tk.W, pady=(0, 5))
        
        # Treeview para listar arquivos
        self.tree_arquivos = ttk.Treeview(frame_esquerdo, columns=("Tipo", "Tamanho"), height=15)
        self.tree_arquivos.column("#0", width=200)
        self.tree_arquivos.column("Tipo", width=80)
        self.tree_arquivos.column("Tamanho", width=100)
        
        self.tree_arquivos.heading("#0", text="Nome do Arquivo")
        self.tree_arquivos.heading("Tipo", text="Tipo")
        self.tree_arquivos.heading("Tamanho", text="Tamanho")
        
        scrollbar = ttk.Scrollbar(frame_esquerdo, orient=tk.VERTICAL, command=self.tree_arquivos.yview)
        self.tree_arquivos.config(yscroll=scrollbar.set)
        
        self.tree_arquivos.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Bind para seleção
        self.tree_arquivos.bind('<<TreeviewSelect>>', self._ao_selecionar_arquivo)
        
        # Painel direito: Visualização
        frame_direito = ttk.Frame(frame_principal)
        frame_direito.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(5, 0))
        
        ttk.Label(frame_direito, text="👁️ Visualização:", 
                 font=("Arial", 10, "bold")).pack(anchor=tk.W, pady=(0, 5))
        
        self.text_preview = scrolledtext.ScrolledText(
            frame_direito, 
            font=("Consolas", 10),
            wrap=tk.WORD,
            bg="#f8f9fa",
            relief=tk.SUNKEN,
            borderwidth=1
        )
        self.text_preview.pack(fill=tk.BOTH, expand=True)
        
        # Atualizar lista inicial
        self._atualizar_lista_arquivos()
    
    # ========== MÉTODOS DE FUNCIONALIDADE ==========
    
    def _inserir_conteudo_inicial_editores(self):
        """Insere conteúdo inicial nos editores de código"""
        # Conteúdo HTML inicial
        html_content = """<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Minha Página</title>
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <header>
        <h1>Bem-vindo ao Meu Site</h1>
        <nav>
            <ul>
                <li><a href="#">Home</a></li>
                <li><a href="#">Sobre</a></li>
                <li><a href="#">Contato</a></li>
            </ul>
        </nav>
    </header>
    
    <main>
        <section class="hero">
            <h2>Título Principal</h2>
            <p>Conteúdo da seção principal aqui.</p>
            <button id="meuBotao">Clique Aqui</button>
        </section>
    </main>
    
    <footer>
        <p>&copy; 2024 Meu Site</p>
    </footer>
    
    <script src="script.js"></script>
</body>
</html>"""
        
        # Conteúdo CSS inicial
        css_content = """/* Seu código CSS aqui */
* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

body {
    font-family: 'Arial', sans-serif;
    line-height: 1.6;
    background-color: #f4f4f4;
    color: #333;
}

header {
    background-color: #2c3e50;
    color: white;
    padding: 20px 0;
    text-align: center;
}

nav ul {
    list-style: none;
    display: flex;
    justify-content: center;
    gap: 20px;
    margin-top: 15px;
}

nav a {
    color: white;
    text-decoration: none;
}

.hero {
    background-color: white;
    padding: 40px;
    border-radius: 8px;
    margin: 20px;
}

footer {
    background-color: #34495e;
    color: white;
    text-align: center;
    padding: 20px;
}"""
        
        # Conteúdo JavaScript inicial
        js_content = """// Seu código JavaScript aqui
document.addEventListener('DOMContentLoaded', function() {
    console.log('Página carregada!');
    
    const botao = document.getElementById('meuBotao');
    
    if (botao) {
        botao.addEventListener('click', function() {
            alert('Botão clicado!');
            this.textContent = 'Clicado!';
        });
    }
});"""
        
        # Inserir nos editores
        self.text_html_editor.delete(1.0, tk.END)
        self.text_html_editor.insert(tk.END, html_content)
        
        self.text_css_editor.delete(1.0, tk.END)
        self.text_css_editor.insert(tk.END, css_content)
        
        self.text_js_editor.delete(1.0, tk.END)
        self.text_js_editor.insert(tk.END, js_content)
    
    def _atualizar_lista_arquivos(self):
        """Atualizar lista de arquivos salvos"""
        # Limpar árvore
        for item in self.tree_arquivos.get_children():
            self.tree_arquivos.delete(item)
        
        # Adicionar arquivos salvos
        if not self.arquivos_criados:
            self.tree_arquivos.insert("", "end", text="Nenhum arquivo salvo", values=("", ""))
            return
        
        for tipo, conteudo in self.arquivos_criados.items():
            nome = f"{tipo.upper()}.{tipo}"
            tamanho = f"{len(conteudo)} bytes"
            self.tree_arquivos.insert("", "end", text=nome, values=(tipo, tamanho))
    
    def _ao_selecionar_arquivo(self, event):
        """Ação ao selecionar um arquivo da lista"""
        selecionados = self.tree_arquivos.selection()
        if selecionados:
            item = selecionados[0]
            nome_arquivo = self.tree_arquivos.item(item, "text")
            tipo = nome_arquivo.split(".")[0].lower()
            
            if tipo in self.arquivos_criados:
                conteudo = self.arquivos_criados[tipo]
                self.text_preview.config(state=tk.NORMAL)
                self.text_preview.delete(1.0, tk.END)
                self.text_preview.insert(tk.END, conteudo[:5000])
                self.text_preview.config(state=tk.DISABLED)
    
    def _copiar_modelo_para_editor(self):
        """Copiar conteúdo do modelo para o editor HTML"""
        if 'soup' not in self.dados_atuais:
            messagebox.showwarning("Aviso", "Primeiro extraia dados de uma URL")
            return
        
        soup = self.dados_atuais['soup']
        html_completo = soup.prettify()
        self.text_html_editor.delete(1.0, tk.END)
        self.text_html_editor.insert(tk.END, html_completo[:10000])
        messagebox.showinfo("Sucesso", "HTML do modelo copiado para o editor!")
    
    def _preview_html(self):
        """Atualizar visualização de HTML"""
        if 'soup' in self.dados_atuais:
            soup = self.dados_atuais['soup']
            html_content = soup.prettify()[:5000]
            self.text_html_modelo.config(state=tk.NORMAL)
            self.text_html_modelo.delete(1.0, tk.END)
            self.text_html_modelo.insert(tk.END, html_content)
            self.text_html_modelo.config(state=tk.DISABLED)
    
    def _extrair_rapido(self, tipo: str):
        """Extração rápida"""
        if 'soup' not in self.dados_atuais:
            messagebox.showwarning("Aviso", "Primeiro extraia de uma URL")
            return
        
        soup = self.dados_atuais['soup']
        resultado = ""
        
        if tipo == 'titulos_h1':
            titulos = self.scraper.extrair_titulos(soup, 1)
            resultado = "Títulos H1 encontrados:\n" + "\n".join([f"- {t}" for t in titulos]) if titulos else "Nenhum H1 encontrado"
        elif tipo == 'titulos_h2':
            titulos = self.scraper.extrair_titulos(soup, 2)
            resultado = "Títulos H2 encontrados:\n" + "\n".join([f"- {t}" for t in titulos]) if titulos else "Nenhum H2 encontrado"
        elif tipo == 'paragrafos':
            paragrafos = self.scraper.extrair_paragrafos(soup)
            resultado = "Parágrafos encontrados (primeiros 10):\n" + "\n".join([f"- {p}" for p in paragrafos[:10]]) if paragrafos else "Nenhum parágrafo encontrado"
        elif tipo == 'links':
            links = self.scraper.extrair_links(soup)
            resultado = "Links encontrados (primeiros 10):\n" + "\n".join([f"- {l['texto']}: {l['url']}" for l in links[:10]]) if links else "Nenhum link encontrado"
        elif tipo == 'tabelas':
            tabelas = self.scraper.extrair_tabelas(soup)
            resultado = f"Tabelas encontradas: {len(tabelas)}" if tabelas else "Nenhuma tabela encontrada"
        
        self.text_extracao.config(state=tk.NORMAL)
        self.text_extracao.delete(1.0, tk.END)
        self.text_extracao.insert(tk.END, resultado)
        self.text_extracao.config(state=tk.DISABLED)
    
    def _extrair_dados(self):
        """Extrair dados"""
        url = self.entry_url.get().strip()
        if not url or url == "https://exemplo.com":
            messagebox.showerror("Erro", "Digite uma URL válida")
            return
        
        if not url.startswith(('http://', 'https://')):
            url = 'https://' + url
        
        thread = threading.Thread(target=self._extrair_thread, args=(url,))
        thread.start()
    
    def _extrair_thread(self, url: str):
        """Executar extração em thread"""
        try:
            self.text_extracao.config(state=tk.NORMAL)
            self.text_extracao.delete(1.0, tk.END)
            self.text_extracao.insert(tk.END, "⏳ Acessando URL...\n")
            self.root.update()
            
            # Se o usuário optou por usar Selenium, carregar página renderizada
            if getattr(self, 'use_selenium', None) and self.use_selenium.get():
                try:
                    self.text_extracao.insert(tk.END, "Usando Selenium para renderizar a página (executando JS)...\n")
                    self.root.update()
                    bot = SeleniumAutomaticaton(headless=True)
                    bot.navegar(url)
                    page_source = bot.driver.page_source
                    bot.fechar()
                    soup = BeautifulSoup(page_source, 'html.parser')
                except Exception as e:
                    raise Exception(f"Selenium erro: {e}")
            else:
                soup = self.scraper.obter_pagina(url)
                if not soup:
                    raise Exception("Erro ao acessar URL")

            # Montar estatísticas e dados
            self.dados_atuais = {
                'url': url,
                'soup': soup,
                'stats': self.ia.detectar_padroes(str(soup))
            }

            # Extrair HTML, CSS e JS para popular editores
            try:
                html_completo = soup.prettify()

                # Extrair CSS: <style> e arquivos vinculados
                css_content = "/* CSS extraído do site */\n\n"
                styles = soup.find_all('style')
                for i, style in enumerate(styles):
                    if style.string:
                        css_content += f"/* Estilo {i+1} */\n" + style.string + "\n\n"

                links = soup.find_all('link', rel=lambda x: x and 'stylesheet' in x, href=True)
                for i, link in enumerate(links):
                    href = link.get('href')
                    full = requests.compat.urljoin(url, href)
                    try:
                        r = requests.get(full, timeout=10)
                        if r.ok:
                            css_content += f"/* Arquivo externo: {href} */\n" + r.text + "\n\n"
                    except Exception:
                        css_content += f"/* Falha ao baixar {href} */\n\n"

                # Extrair JS: inline e externos
                js_content = "// JavaScript extraído do site\n\n"
                scripts = soup.find_all('script')
                for i, script in enumerate(scripts):
                    src = script.get('src')
                    if script.string:
                        js_content += f"// Script inline {i+1}\n" + script.string + "\n\n"
                    elif src:
                        full = requests.compat.urljoin(url, src)
                        try:
                            r = requests.get(full, timeout=10)
                            if r.ok:
                                js_content += f"// Arquivo externo: {src}\n" + r.text + "\n\n"
                        except Exception:
                            js_content += f"// Falha ao baixar {src}\n\n"

                # Atualizar editores e memória do programa
                self.text_html_editor.delete(1.0, tk.END)
                self.text_html_editor.insert(tk.END, html_completo)

                self.text_css_editor.delete(1.0, tk.END)
                self.text_css_editor.insert(tk.END, css_content)

                self.text_js_editor.delete(1.0, tk.END)
                self.text_js_editor.insert(tk.END, js_content)

                # Guardar em memória
                self.arquivos_criados['html'] = html_completo
                self.arquivos_criados['css'] = css_content
                self.arquivos_criados['js'] = js_content
                self._atualizar_lista_arquivos()
            except Exception:
                # Não falhar a extração se a extração de recursos falhar
                pass
            
            # Limpar e mostrar resultados
            self.text_extracao.delete(1.0, tk.END)
            self.text_extracao.insert(tk.END, f"✅ URL: {url}\n\n")
            
            # Mostrar estatísticas básicas
            titulos_h1 = self.scraper.extrair_titulos(soup, 1)
            titulos_h2 = self.scraper.extrair_titulos(soup, 2)
            paragrafos = self.scraper.extrair_paragrafos(soup)
            links = self.scraper.extrair_links(soup)
            
            self.text_extracao.insert(tk.END, f"📊 Estatísticas:\n")
            self.text_extracao.insert(tk.END, f"- Títulos H1: {len(titulos_h1)}\n")
            self.text_extracao.insert(tk.END, f"- Títulos H2: {len(titulos_h2)}\n")
            self.text_extracao.insert(tk.END, f"- Parágrafos: {len(paragrafos)}\n")
            self.text_extracao.insert(tk.END, f"- Links: {len(links)}\n")
            
            # Mostrar padrões detectados
            self.text_extracao.insert(tk.END, f"\n🔍 Padrões detectados:\n")
            self.text_extracao.insert(tk.END, f"- Emails: {len(self.dados_atuais['stats']['emails'])}\n")
            self.text_extracao.insert(tk.END, f"- Telefones: {len(self.dados_atuais['stats']['telefones'])}\n")
            self.text_extracao.insert(tk.END, f"- Preços: {len(self.dados_atuais['stats']['precos'])}\n")
            self.text_extracao.insert(tk.END, f"- Datas: {len(self.dados_atuais['stats']['datas'])}\n")
            
            # Atualizar aba de análise
            self._preview_html()
            
            messagebox.showinfo("Sucesso", f"Dados extraídos com sucesso!\n\nURL: {url}")
            
        except Exception as e:
            self.text_extracao.insert(tk.END, f"\n❌ Erro: {e}")
        finally:
            self.text_extracao.config(state=tk.DISABLED)
    
    def _carregar_html_modelo(self):
        """Carregar HTML do site modelo para o editor"""
        self._copiar_modelo_para_editor()
    
    def _salvar_arquivo(self, tipo: str):
        """Salvar arquivo no programa"""
        if tipo == 'html':
            conteudo = self.text_html_editor.get(1.0, tk.END)
            self.arquivos_criados['html'] = conteudo
            messagebox.showinfo("Sucesso", "✅ HTML salvo no programa!")
        elif tipo == 'css':
            conteudo = self.text_css_editor.get(1.0, tk.END)
            self.arquivos_criados['css'] = conteudo
            messagebox.showinfo("Sucesso", "✅ CSS salvo no programa!")
        elif tipo == 'js':
            conteudo = self.text_js_editor.get(1.0, tk.END)
            self.arquivos_criados['js'] = conteudo
            messagebox.showinfo("Sucesso", "✅ JavaScript salvo no programa!")
        
        # Atualizar lista de arquivos
        self._atualizar_lista_arquivos()
    
    def _download_arquivo(self, tipo: str):
        """Download do arquivo"""
        if tipo == 'html':
            conteudo = self.text_html_editor.get(1.0, tk.END)
            extensao = '.html'
            nome_padrao = 'index.html'
        elif tipo == 'css':
            conteudo = self.text_css_editor.get(1.0, tk.END)
            extensao = '.css'
            nome_padrao = 'style.css'
        else:  # js
            conteudo = self.text_js_editor.get(1.0, tk.END)
            extensao = '.js'
            nome_padrao = 'script.js'
        
        # Abrir diálogo de save
        arquivo = filedialog.asksaveasfilename(
            defaultextension=extensao,
            initialfile=nome_padrao,
            filetypes=[(f"{tipo.upper()} files", f"*{extensao}"), ("All files", "*.*")]
        )
        
        if arquivo:
            try:
                with open(arquivo, 'w', encoding='utf-8') as f:
                    f.write(conteudo)
                messagebox.showinfo("Sucesso", f"✅ Arquivo salvo em:\n{arquivo}")
            except Exception as e:
                messagebox.showerror("Erro", f"❌ Erro ao salvar: {e}")
    
    def _limpar_editor(self, tipo: str):
        """Limpar editor de código"""
        if tipo == 'html':
            self.text_html_editor.delete(1.0, tk.END)
        elif tipo == 'css':
            self.text_css_editor.delete(1.0, tk.END)
        else:  # js
            self.text_js_editor.delete(1.0, tk.END)
    
    def _gerar_pagina_completa(self):
        """Gerar página completa com HTML, CSS e JS"""
        html = self.text_html_editor.get(1.0, tk.END).strip()
        css = self.text_css_editor.get(1.0, tk.END)
        js = self.text_js_editor.get(1.0, tk.END)
        
        if not html:
            messagebox.showwarning("Aviso", "O editor HTML está vazio!")
            return
        
        # Criar arquivo HTML completo
        arquivo_completo = f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Site Gerado</title>
    <style>
{css if css else "        body {{ font-family: Arial, sans-serif; margin: 20px; }}"}
    </style>
</head>
<body>
{html}
    <script>
{js if js else "        console.log('Site gerado');"}
    </script>
</body>
</html>"""
        
        # Salvar arquivo
        arquivo = filedialog.asksaveasfilename(
            defaultextension=".html",
            initialfile="site_gerado.html",
            filetypes=[("HTML files", "*.html"), ("All files", "*.*")]
        )
        
        if arquivo:
            try:
                with open(arquivo, 'w', encoding='utf-8') as f:
                    f.write(arquivo_completo)
                messagebox.showinfo("Sucesso", f"✅ Site gerado e salvo em:\n{arquivo}")
                
                # Armazenar em memória
                self.arquivos_criados['html'] = arquivo_completo
                self._atualizar_lista_arquivos()
                
            except Exception as e:
                messagebox.showerror("Erro", f"❌ Erro ao salvar: {e}")
    
    def _abrir_preview_local(self):
        """Abrir preview local do HTML atual"""
        html = self.text_html_editor.get(1.0, tk.END).strip()
        css = self.text_css_editor.get(1.0, tk.END)
        
        if not html:
            messagebox.showwarning("Aviso", "Editor HTML vazio!")
            return
        
        # Criar arquivo temporário
        temp_file = tempfile.NamedTemporaryFile(mode='w', suffix='.html', delete=False, encoding='utf-8')
        
        # Criar HTML completo
        html_completo = f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Preview</title>
    <style>
{css if css else ''}
    </style>
</head>
<body>
{html}
</body>
</html>"""
        
        temp_file.write(html_completo)
        temp_file.close()
        
        # Abrir no navegador
        webbrowser.open(f'file://{temp_file.name}')
    
    def _abrir_no_navegador(self):
        """Abrir no navegador web"""
        if 'url' in self.dados_atuais:
            webbrowser.open(self.dados_atuais['url'])
        else:
            messagebox.showwarning("Aviso", "Nenhuma URL extraída!")
    
    def _copiar_codigo_completo(self):
        """Copiar código completo para a área de transferência"""
        html = self.text_html_editor.get(1.0, tk.END)
        css = self.text_css_editor.get(1.0, tk.END)
        js = self.text_js_editor.get(1.0, tk.END)
        
        codigo_completo = f"""<!-- HTML -->
{html}

<!-- CSS -->
{css}

<!-- JavaScript -->
{js}"""
        
        self.root.clipboard_clear()
        self.root.clipboard_append(codigo_completo)
        messagebox.showinfo("Sucesso", "Código copiado para a área de transferência!")
    
    def _salvar_todos_arquivos(self):
        """Salvar todos os arquivos"""
        if not self.arquivos_criados:
            messagebox.showwarning("Aviso", "Nenhum arquivo para salvar!")
            return
        
        # Criar diretório
        diretorio = filedialog.askdirectory(title="Selecione onde salvar os arquivos")
        if not diretorio:
            return
        
        try:
            for tipo, conteudo in self.arquivos_criados.items():
                if tipo == 'html':
                    arquivo = os.path.join(diretorio, 'index.html')
                elif tipo == 'css':
                    arquivo = os.path.join(diretorio, 'style.css')
                else:  # js
                    arquivo = os.path.join(diretorio, 'script.js')
                
                with open(arquivo, 'w', encoding='utf-8') as f:
                    f.write(conteudo)
            
            messagebox.showinfo("Sucesso", f"✅ Todos os arquivos salvos em:\n{diretorio}")
        except Exception as e:
            messagebox.showerror("Erro", f"❌ Erro ao salvar: {e}")
    
    def _download_html_site(self):
        """Download HTML do site"""
        if 'soup' not in self.dados_atuais:
            messagebox.showwarning("Aviso", "Extraia um site primeiro")
            return
        
        soup = self.dados_atuais['soup']
        html_completo = soup.prettify()
        
        arquivo = filedialog.asksaveasfilename(
            defaultextension=".html",
            initialfile="site_analisado.html",
            filetypes=[("HTML files", "*.html"), ("All files", "*.*")]
        )
        
        if arquivo:
            try:
                with open(arquivo, 'w', encoding='utf-8') as f:
                    f.write(html_completo)
                messagebox.showinfo("Sucesso", f"✅ HTML salvo em:\n{arquivo}")
                
                # Armazenar em memória
                self.arquivos_criados['html'] = html_completo
                self._atualizar_lista_arquivos()
                
            except Exception as e:
                messagebox.showerror("Erro", f"❌ Erro ao salvar: {e}")
    
    def _download_css_site(self):
        """Download CSS do site"""
        if 'soup' not in self.dados_atuais:
            messagebox.showwarning("Aviso", "Extraia um site primeiro")
            return
        
        soup = self.dados_atuais['soup']
        css_content = "/* CSS Extraído do Site */\n\n"
        
        # Extrair CSS inline
        styles = soup.find_all('style')
        for i, style in enumerate(styles):
            if style.string:
                css_content += f"/* Estilo {i+1} */\n"
                css_content += style.string
                css_content += "\n\n"
        
        if css_content.strip() == "/* CSS Extraído do Site */":
            css_content += "/* Nenhum CSS encontrado */\n"
        
        arquivo = filedialog.asksaveasfilename(
            defaultextension=".css",
            initialfile="estilos_site.css",
            filetypes=[("CSS files", "*.css"), ("All files", "*.*")]
        )
        
        if arquivo:
            try:
                with open(arquivo, 'w', encoding='utf-8') as f:
                    f.write(css_content)
                messagebox.showinfo("Sucesso", f"✅ CSS salvo em:\n{arquivo}")
                
                # Armazenar em memória
                self.arquivos_criados['css'] = css_content
                self._atualizar_lista_arquivos()
                
            except Exception as e:
                messagebox.showerror("Erro", f"❌ Erro ao salvar: {e}")
    
    def _download_js_site(self):
        """Download JavaScript do site"""
        if 'soup' not in self.dados_atuais:
            messagebox.showwarning("Aviso", "Extraia um site primeiro")
            return
        
        soup = self.dados_atuais['soup']
        js_content = "// JavaScript Extraído do Site\n\n"
        
        # Extrair JavaScript inline
        scripts = soup.find_all('script')
        for i, script in enumerate(scripts):
            if script.string:
                js_content += f"// Script {i+1}\n"
                js_content += script.string
                js_content += "\n\n"
        
        if js_content.strip() == "// JavaScript Extraído do Site":
            js_content += "// Nenhum JavaScript encontrado\n"
        
        arquivo = filedialog.asksaveasfilename(
            defaultextension=".js",
            initialfile="scripts_site.js",
            filetypes=[("JavaScript files", "*.js"), ("All files", "*.*")]
        )
        
        if arquivo:
            try:
                with open(arquivo, 'w', encoding='utf-8') as f:
                    f.write(js_content)
                messagebox.showinfo("Sucesso", f"✅ JavaScript salvo em:\n{arquivo}")
                
                # Armazenar em memória
                self.arquivos_criados['js'] = js_content
                self._atualizar_lista_arquivos()
                
            except Exception as e:
                messagebox.showerror("Erro", f"❌ Erro ao salvar: {e}")
    
    def _limpar_todos_arquivos(self):
        """Limpar todos os arquivos salvos"""
        if not self.arquivos_criados:
            messagebox.showinfo("Aviso", "Nenhum arquivo para limpar")
            return
        
        if messagebox.askyesno("Confirmar", "Deletar TODOS os arquivos salvos?"):
            self.arquivos_criados.clear()
            self._atualizar_lista_arquivos()
            self.text_preview.config(state=tk.NORMAL)
            self.text_preview.delete(1.0, tk.END)
            self.text_preview.config(state=tk.DISABLED)
            messagebox.showinfo("Sucesso", "Todos os arquivos foram deletados")
    
    def _limpar(self):
        """Limpar todos os dados"""
        self.dados_atuais = {}
        self.text_extracao.config(state=tk.NORMAL)
        self.text_extracao.delete(1.0, tk.END)
        self.text_extracao.config(state=tk.DISABLED)
        self.text_html_modelo.config(state=tk.NORMAL)
        self.text_html_modelo.delete(1.0, tk.END)
        self.text_html_modelo.insert(tk.END, 
            "⏳ Extraia dados de uma URL primeiro\n\n"
            "1. Vá para a aba '📥 Extração'\n"
            "2. Cole uma URL e clique em 'Extrair'\n"
            "3. O código HTML aparecerá aqui automaticamente"
        )
        self.text_html_modelo.config(state=tk.DISABLED)
        messagebox.showinfo("Sucesso", "Dados limpos!")
    
    # ========== NOVOS MÉTODOS PARA MONTAGEM DE PÁGINA ==========
    
    def _gerar_estrutura_html(self):
        """Gera estrutura HTML base conforme seleção"""
        estrutura = self.var_estrutura.get()
        
        estruturas = {
            'simples': """<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Minha Página Simples</title>
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <header>
        <h1>Bem-vindo</h1>
        <nav>
            <ul>
                <li><a href="#inicio">Início</a></li>
                <li><a href="#sobre">Sobre</a></li>
                <li><a href="#contato">Contato</a></li>
            </ul>
        </nav>
    </header>
    
    <main>
        <section id="inicio">
            <h2>Seção Principal</h2>
            <p>Conteúdo da sua página aqui.</p>
        </section>
    </main>
    
    <footer>
        <p>&copy; 2024 Minha Página</p>
    </footer>
    
    <script src="script.js"></script>
</body>
</html>""",
            
            'blog': """<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Meu Blog</title>
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <header class="blog-header">
        <div class="container">
            <h1>📝 Meu Blog</h1>
            <p>Compartilhando conhecimento e experiências</p>
        </div>
    </header>
    
    <main class="container">
        <article class="post">
            <header class="post-header">
                <h2>Título do Artigo</h2>
                <time datetime="2024-01-01">01 de Janeiro, 2024</time>
            </header>
            <div class="post-content">
                <p>Conteúdo do seu artigo aqui...</p>
            </div>
        </article>
    </main>
    
    <footer class="blog-footer">
        <p>Blog criado com ❤️</p>
    </footer>
    
    <script src="script.js"></script>
</body>
</html>""",
            
            'portfolio': """<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Meu Portfólio</title>
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <header class="portfolio-header">
        <div class="hero">
            <h1>👨‍💻 Desenvolvedor Web</h1>
            <p>Transformando ideias em código</p>
        </div>
    </header>
    
    <main>
        <section class="projects">
            <h2>Meus Projetos</h2>
            <div class="project-grid">
                <div class="project-card">
                    <h3>Projeto 1</h3>
                    <p>Descrição do projeto</p>
                </div>
            </div>
        </section>
    </main>
    
    <script src="script.js"></script>
</body>
</html>"""
        }
        
        html_gerado = estruturas.get(estrutura, estruturas['simples'])
        self.text_html_editor.delete(1.0, tk.END)
        self.text_html_editor.insert(tk.END, html_gerado)
        messagebox.showinfo("Sucesso", "Estrutura HTML gerada com sucesso!")
    
    def _gerar_estilos_css(self):
        """Gera estilos CSS conforme seleção"""
        tema = self.var_tema.get()
        tamanho_fonte = self.var_tamanho_fonte.get()
        
        temas = {
            'claro': {
                'cor_primaria': '#667eea',
                'cor_secundaria': '#764ba2',
                'cor_fundo': '#ffffff',
                'cor_texto': '#333333',
                'cor_borda': '#dddddd'
            },
            'escuro': {
                'cor_primaria': '#8a2be2',
                'cor_secundaria': '#4b0082',
                'cor_fundo': '#1a1a1a',
                'cor_texto': '#f0f0f0',
                'cor_borda': '#444444'
            },
            'azul': {
                'cor_primaria': '#2196F3',
                'cor_secundaria': '#1976D2',
                'cor_fundo': '#f5f9ff',
                'cor_texto': '#263238',
                'cor_borda': '#bbdefb'
            }
        }
        
        cores = temas.get(tema, temas['claro'])
        
        css_gerado = f"""/* Estilos gerados automaticamente */
/* Tema: {tema.capitalize()} | Tamanho da fonte: {tamanho_fonte}px */

/* ===== RESET E CONFIGURAÇÕES GERAIS ===== */
* {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

html {{
    font-size: {tamanho_fonte}px;
    scroll-behavior: smooth;
}}

body {{
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, sans-serif;
    line-height: 1.6;
    color: {cores['cor_texto']};
    background-color: {cores['cor_fundo']};
    transition: all 0.3s ease;
}}

/* ===== TIPOGRAFIA ===== */
h1, h2, h3, h4, h5, h6 {{
    font-weight: 700;
    line-height: 1.2;
    margin-bottom: 1rem;
    color: {cores['cor_primaria']};
}}

h1 {{ font-size: 2.5rem; }}
h2 {{ font-size: 2rem; }}
h3 {{ font-size: 1.75rem; }}
h4 {{ font-size: 1.5rem; }}
h5 {{ font-size: 1.25rem; }}
h6 {{ font-size: 1rem; }}

p {{
    margin-bottom: 1rem;
}}

a {{
    color: {cores['cor_primaria']};
    text-decoration: none;
    transition: color 0.3s ease;
}}

a:hover {{
    color: {cores['cor_secundaria']};
    text-decoration: underline;
}}

/* ===== BOTÕES ===== */
.btn {{
    display: inline-block;
    padding: 0.75rem 1.5rem;
    background: linear-gradient(to right, {cores['cor_primaria']}, {cores['cor_secundaria']});
    color: white;
    border: none;
    border-radius: 0.5rem;
    font-size: 1rem;
    font-weight: 600;
    cursor: pointer;
    transition: all 0.3s ease;
}}

.btn:hover {{
    transform: translateY(-2px);
    box-shadow: 0 10px 20px rgba(0,0,0,0.2);
}}

/* ===== CARDS ===== */
.card {{
    background: white;
    border: 1px solid {cores['cor_borda']};
    border-radius: 1rem;
    padding: 1.5rem;
    box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    transition: all 0.3s ease;
}}

.card:hover {{
    transform: translateY(-5px);
    box-shadow: 0 10px 20px rgba(0,0,0,0.15);
}}

/* ===== RESPONSIVIDADE ===== */
@media (max-width: 768px) {{
    .container {{
        padding: 0 15px;
    }}
    
    h1 {{ font-size: 2rem; }}
    h2 {{ font-size: 1.75rem; }}
    h3 {{ font-size: 1.5rem; }}
    
    .btn {{
        padding: 0.5rem 1rem;
        font-size: 0.9rem;
    }}
}}"""
        
        self.text_css_editor.delete(1.0, tk.END)
        self.text_css_editor.insert(tk.END, css_gerado)
        messagebox.showinfo("Sucesso", "Estilos CSS gerados com sucesso!")
    
    def _gerar_funcionalidades_js(self):
        """Gera funcionalidades JavaScript conforme seleção"""
        funcionalidades = []
        
        if self.var_funcionalidades['menu_responsivo'].get():
            funcionalidades.append("""
// ===== MENU RESPONSIVO =====
function initResponsiveMenu() {
    const menuToggle = document.createElement('button');
    menuToggle.innerHTML = '☰';
    menuToggle.className = 'menu-toggle';
    
    const nav = document.querySelector('nav');
    if (nav) {
        nav.parentNode.insertBefore(menuToggle, nav);
        
        const mediaQuery = window.matchMedia('(max-width: 768px)');
        
        function handleMobileChange(e) {
            if (e.matches) {
                menuToggle.style.display = 'block';
                nav.style.display = 'none';
            } else {
                menuToggle.style.display = 'none';
                nav.style.display = '';
            }
        }
        
        mediaQuery.addListener(handleMobileChange);
        handleMobileChange(mediaQuery);
        
        menuToggle.addEventListener('click', function() {
            if (nav.style.display === 'none' || nav.style.display === '') {
                nav.style.display = 'block';
            } else {
                nav.style.display = 'none';
            }
        });
    }
}""")
        
        if self.var_funcionalidades['validacao_formulario'].get():
            funcionalidades.append("""
// ===== VALIDAÇÃO DE FORMULÁRIO =====
function initFormValidation() {
    const forms = document.querySelectorAll('form');
    
    forms.forEach(form => {
        form.addEventListener('submit', function(event) {
            let isValid = true;
            const requiredFields = this.querySelectorAll('[required]');
            
            requiredFields.forEach(field => {
                if (!field.value.trim()) {
                    isValid = false;
                    field.style.borderColor = '#f44336';
                } else {
                    field.style.borderColor = '#4CAF50';
                }
            });
            
            if (!isValid) {
                event.preventDefault();
                alert('Por favor, preencha todos os campos obrigatórios.');
            }
        });
    });
}""")
        
        # Montar o JS completo
        js_gerado = """// ===== INICIALIZAÇÃO DO SISTEMA =====
document.addEventListener('DOMContentLoaded', function() {
    console.log('Sistema inicializando...');\n"""
        
        # Adicionar chamadas para as funcionalidades selecionadas
        if self.var_funcionalidades['menu_responsivo'].get():
            js_gerado += "    initResponsiveMenu();\n"
        if self.var_funcionalidades['validacao_formulario'].get():
            js_gerado += "    initFormValidation();\n"
        
        js_gerado += """    
    console.log('Sistema inicializado com sucesso!');
});

// ===== FUNCIONALIDADES =====\n"""
        
        # Adicionar as funções
        for func in funcionalidades:
            js_gerado += func + "\n"
        
        self.text_js_editor.delete(1.0, tk.END)
        self.text_js_editor.insert(tk.END, js_gerado)
        messagebox.showinfo("Sucesso", "Funcionalidades JavaScript geradas com sucesso!")
    
    def _integrar_componentes(self):
        """Integra todos os componentes gerados"""
        messagebox.showinfo("Integração", "Componentes integrados com sucesso!\n\nPronto para visualização.")
    
    def _preview_completo(self):
        """Mostra preview completo da página"""
        html = self.text_html_editor.get(1.0, tk.END)
        css = self.text_css_editor.get(1.0, tk.END)
        js = self.text_js_editor.get(1.0, tk.END)
        
        if not html.strip():
            messagebox.showwarning("Aviso", "Gere uma estrutura HTML primeiro!")
            return
        
        # Criar arquivo temporário
        temp_file = tempfile.NamedTemporaryFile(mode='w', suffix='.html', delete=False, encoding='utf-8')
        
        html_completo = f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Preview - Página Montada</title>
    <style>
{css if css else ''}
    </style>
</head>
<body>
{html}
    <script>
{js if js else ''}
    </script>
</body>
</html>"""
        
        temp_file.write(html_completo)
        temp_file.close()
        
        # Abrir no navegador
        webbrowser.open(f'file://{temp_file.name}')
    
    def _exportar_zip(self):
        """Exporta a página como arquivo ZIP"""
        html = self.text_html_editor.get(1.0, tk.END).strip()
        css = self.text_css_editor.get(1.0, tk.END)
        js = self.text_js_editor.get(1.0, tk.END)
        
        if not html:
            messagebox.showwarning("Aviso", "O editor HTML está vazio!")
            return
        
        # Abrir diálogo para salvar ZIP
        arquivo = filedialog.asksaveasfilename(
            defaultextension=".zip",
            initialfile="site_completo.zip",
            filetypes=[("ZIP files", "*.zip"), ("All files", "*.*")]
        )
        
        if arquivo:
            try:
                with zipfile.ZipFile(arquivo, 'w', zipfile.ZIP_DEFLATED) as zipf:
                    # Adicionar index.html
                    html_completo = f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Site Completo</title>
    <link rel="stylesheet" href="style.css">
</head>
<body>
{html}
    <script src="script.js"></script>
</body>
</html>"""
                    
                    zipf.writestr("index.html", html_completo)
                    
                    # Adicionar style.css
                    if css.strip():
                        zipf.writestr("style.css", css)
                    else:
                        zipf.writestr("style.css", "/* Estilos CSS */")
                    
                    # Adicionar script.js
                    if js.strip():
                        zipf.writestr("script.js", js)
                    else:
                        zipf.writestr("script.js", "// JavaScript")
                
                messagebox.showinfo("Sucesso", f"✅ Site exportado como ZIP em:\n{arquivo}")
            except Exception as e:
                messagebox.showerror("Erro", f"❌ Erro ao exportar: {e}")
    
    def _publicar_online(self):
        """Publica a página online"""
        messagebox.showinfo("Publicar", "Funcionalidade de publicação online em desenvolvimento.\n\nSugestão: Use serviços como Netlify, Vercel ou GitHub Pages.")
    
    def _executar_teste_rapido(self):
        """Executa teste rápido do código"""
        codigo_teste = self.text_teste_rapido.get(1.0, tk.END)
        
        # Criar arquivo temporário para teste
        temp_file = tempfile.NamedTemporaryFile(mode='w', suffix='.html', delete=False, encoding='utf-8')
        
        html_teste = f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Teste Rápido</title>
</head>
<body>
    <div style="padding: 20px; font-family: Arial;">
        <h2>Teste Rápido - Resultado</h2>
        <div id="testeContainer">
            {codigo_teste}
        </div>
    </div>
</body>
</html>"""
        
        temp_file.write(html_teste)
        temp_file.close()
        
        # Abrir no navegador
        webbrowser.open(f'file://{temp_file.name}')
        messagebox.showinfo("Teste", "Teste aberto no navegador!")
    
    def _limpar_teste_rapido(self):
        """Limpa a área de teste rápido"""
        self.text_teste_rapido.delete(1.0, tk.END)
        messagebox.showinfo("Limpar", "Área de teste limpa!")
    
    def _salvar_teste_rapido(self):
        """Salva o código de teste"""
        codigo_teste = self.text_teste_rapido.get(1.0, tk.END)
        
        arquivo = filedialog.asksaveasfilename(
            defaultextension=".html",
            initialfile="teste_rapido.html",
            filetypes=[("HTML files", "*.html"), ("All files", "*.*")]
        )
        
        if arquivo:
            try:
                with open(arquivo, 'w', encoding='utf-8') as f:
                    f.write(codigo_teste)
                messagebox.showinfo("Sucesso", f"Teste salvo em:\n{arquivo}")
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao salvar: {e}")

          
# ==================== MAIN ====================
if __name__ == '__main__':
    root = tk.Tk()
    app = WebScraperApp(root)
    root.mainloop()