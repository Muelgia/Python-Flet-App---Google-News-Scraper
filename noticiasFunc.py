import requests, re
import bs4
from time import sleep
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import flet as ft
from funcoesFlet import mostrar_notificacao

# funcao principal que roda o app
def noticiasFunc(page, fieldInput, filtroData, esconderNavegador : bool = True):

    # pega as noticias de cada pagina
    def pegarNoticias(driver, tag, classe, noticias : list ):
        
        try:
            # pega o url atual da pagina
            urlAtual = driver.current_url
            print(urlAtual)
            # transforma o codigo fonte no html 
            paginaHtml = bs4.BeautifulSoup(driver.page_source, "html.parser")
            # pega o elemento que vai ser uma "lista"
            listaNoticias = paginaHtml.find_all(tag, class_=classe)
            # adiciona cada elemento da lista em outra lista, que é a principal
            for noticia in listaNoticias:
                print('ok')

                #adiciona o url da noticia no dicionario
                linkNoticia = noticia.get("href")
                #adiciona o titulo da noticia no dicionario
                noticia =  noticia.text

                # adiciona a noticia e o link a lista
                noticias.append((noticia, linkNoticia))

        # printa o erro 
        except Exception as e:
            print(e)
            print('Erro na função pegar notícias')


    # entra até o side do google noticias com filtro de cripto a menos de um dia
    pesquisa = ''

    # se o campo de input do tema da noticia não estivar vazio
    if fieldInput.value != '':
        pesquisa = fieldInput.value
    # mostra uma notificação caso o campo esteja vazio 
    else:
        mostrar_notificacao(page=page, texto='Campo "BUSCAR" está vazio. Digite a notícia que deseja pesquisar!', icon=ft.icons.WARNING, cor='red')
        return
    
    # url de acordo com a pesquisa e a data escolhida
    url = f'https://www.google.com/search?q={pesquisa}&tbm=nws{filtroData}'
    
    # declara a classe do chrome options
    chrome_options = Options()

    # esconde o navegador de o botão for clicado
    if esconderNavegador == True:      
        chrome_options.add_argument("--headless")  # Executar no modo headless

    # chrome service
    service = Service(ChromeDriverManager().install())

    # declara o driver
    driver = webdriver.Chrome(service=service, options=chrome_options)

    # entra no url já filtrado de acordo 
    driver.get(url)
    # wait declarado
    wait = WebDriverWait(driver, 3)

    noticias = []

    while True:
        # chama a função de pegar notícia 
        pegarNoticias(driver=driver, tag='a', classe='WlydOe', noticias=noticias)

        print(noticias)

        # tenta clicar para avançar pagina
        try:
            
            avancaPagina = wait.until(EC.presence_of_element_located((By.ID, 'pnnext')))
            avancaPagina.click()
            continue
        # caso não consiga encontrar a pagina finaliza o loop
        except:
            print('Fim das páginas')
            break

    # evita algumas detecções de bot
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }

    # fecha o navegador
    driver.close()

    resultados = []

    # para cada noticia que foi adicionada na lista, entra no site e pega todos os <p>
    for link in noticias:
        try:

            textoNoticia = ''   

            # entra no site, que é o segundo elemento da lista, passa o headers com dados de navegador e aguarda 10seg na requisição
            responseLink = requests.get(link[1], headers=headers, timeout=10)
            # 
            paginaLink = bs4.BeautifulSoup(responseLink.text, "html.parser")
            # pega a tag que vai ser uma "lista"
            noticiaLink = paginaLink.find_all("p")
            
            # para cada tag de paragrafo no html, concatena o texto e uma quebra de linha
            for p in noticiaLink:
                textoNoticia += p.text + "\n"

            # titulo e url de acordo com seus indices 
            tituloR = link[0]
            urlR = link[1]

            # adiciona os resultados ao dicionario resultados e remove todos os ;
            resultados.append({
                "titulo": tituloR.replace(';', ''),
                "url": urlR.replace(';', ''),
                "texto": textoNoticia
            })

            print(f'Noticia do site {link[1]} pega com sucesso!')
        except Exception as e:
            print(e)
            print(f'Erro ao pegar noticia do site {link[1]}')
            pass
    
    # retorna os resultados 
    return resultados
    
# chama a funcao para teste 
if __name__ == '__main__':

    noticiasFunc()