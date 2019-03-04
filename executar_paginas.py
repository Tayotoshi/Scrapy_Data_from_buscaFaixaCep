from selenium import webdriver
from bs4 import BeautifulSoup as bs
from pegar_registros import *
class Page:
    #Variaveis que possam ser utilizadas no programa

    def __init__(self, driver):
        self.driver = driver
        self.url = 'http://www.buscacep.correios.com.br/sistemas/buscacep/buscaFaixaCEP.cfm'
        self.search_bar = 'f1col'
        self.btn_search = 'btn2'
        self.table = 'tmptabela'


    # Inicia a navegação até o URL requisitado
    def navegar(self):
        self.driver.get(self.url)
        Page.estado(self)

    def estado(self):
        escolha=0
        while escolha != 1:
            print (20*'-=')
            print('O que deseja fazer?\n[0] Para pesquisar por uma UF\n[1] Para encerrar o programa')
            escolha = int(input('Escolha [0] ou [1]: '))
            if escolha == 0:
                uf=input(str('Insira a sigla da UF (Unidade da Federação), por exemplo: SC,SP,RS... : ')).upper()
                Page.pesquisar(self, uf)
            elif escolha == 1:
                print (20*'-=')
                print ('FINALIZANDO PROGRAMA!')
                gc.quit()
            else:
                print('OPÇÃO INVÁLIDA! DIGITE UM NÚMERO VALIDO POR FAVOR [0] ou [1]')


    # Pesquisa pelo estado e clica em buscar.
    def pesquisar(self, word='None'):
        self.driver.find_element_by_class_name(
            self.search_bar).send_keys(word)
        self.driver.find_element_by_class_name(
            self.btn_search).click()
        Page.pegar_tabelas(self,t=1)

    @staticmethod
    def inicia_nova_consulta(driver):
        escolha = 0
        while escolha != 1:
            print(20 * '-=')
            print('Deseja fazer uma nova consulta a uma UF?\n[0] SIM\n[1] NÃO')
            escolha = int(input('Escolha [0] ou [1]: '))
            if escolha == 0:
                driver.find_element_by_link_text("[ Nova Consulta ]").click()
                g.navegar()
            elif escolha == 1:
                print(20 * '-=')
                print('FINALIZANDO PROGRAMA!')
                gc.quit()
            else:
                print ('OPÇÃO INVÁLIDA! DIGITE UM NÚMERO VALIDO POR FAVOR [0] ou [1]')

    @staticmethod
    # Pega a tabela onde estão os registros
    def pegar_tabelas(self, t=1):
        tabelas = (self.driver.find_elements_by_class_name(
            self.table))
        tabela = tabelas[t]
        pagina_HTML()

    @staticmethod
    # Muda a pagina para a proxima
    def mudar_pagina(driver):
        driver.find_element_by_link_text("[ Próxima ]").click()


# Pega o documento HTML da pagina e disseca ele até as td
def pagina_HTML(qual_tabela=1):
    qual_tabela=qual_tabela
    html=gc.page_source
    correio_pagina = bs(html, 'html.parser')
    tabela = correio_pagina.find_all('table')
    tbody = tabela[qual_tabela].find('tbody')
    td = tbody.find_all('td')
    limpa_registros(td)
    return td

#Pega os registros cidade e CEP de dentro da tabela, retira as tags HTML os armazena em uma lista, e logo após armazena em um arquivo.txt.
def limpa_registros(td):
    cep_inicial = 1
    cidade_inicial = 0
    lista_registros = []
    for cada_registro in range(0, len(td), 4):
        lista_registros.append(td[cidade_inicial].text)
        lista_registros.append(td[cep_inicial].text)
        cidade_inicial += 4
        cep_inicial += 4
    cria_e_salva_arquivo(lista_registros)
    continua_procurando(lista_registros)


#Se registros.txt ainda não tiver 100 registros, essa função ira ser ativa e registrará mais 50 registros.
def continua_procurando (lista_registros):
    texto = lista_registros
    if len(texto)<100:
        Page.mudar_pagina(gc)
        pagina_HTML(0)
    else:
        if len(texto)>=100:
            Page.inicia_nova_consulta(gc)


gc = webdriver.Chrome()
g = Page(gc)
g.navegar()
