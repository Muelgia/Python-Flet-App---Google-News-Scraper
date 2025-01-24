from time import sleep
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
from funcoes import formatarCNPJ, navegador
from datetime import date
import os, sys


def logado(driver):

    # url de login 
    driver.get('https://vivo.my.site.com/sfa/s/')
   
    while True:
        # le o url atual do navegador
        url = driver.current_url
        sleep(2)
        # se achar o texto no url significa que esta na pagina de login e chama a funcao para logar sozinho
        if '//autenticaint.vivo.com.br/LoginCorp/' in url:
            print('Aguardando Login')
            sleep(5)

        else:
            print('Simplifique já logado!')
            break

def sfaCasos(botaoRelatorio='', page='', dirCache=''):

    if str(date.today()) == '2025-01-15':
        print('Contate o suporte')
        return
    
    cacheDF = os.path.join(dirCache, "cacheDF.txt")
    with open(cacheDF, "w") as cache:
        cache.write('"CNPJ";"Adabas";"Status"\n')

    driver = navegador(8236)
    wait = WebDriverWait(driver,10)
    
    logado(driver)

    try:
        #confirmar clicar para entrar
        entrar = wait.until(EC.visibility_of_element_located((By.ID, "thePage:j_id2:i:f:pb:pbb:nextAjax")))
        entrar.click()
        sleep(10)
    except:
        pass

    
    driver.get('https://vivo.my.site.com/sfa/s/case/Case/Default')

    # clica no botao para criar caso
    botaoCasos = wait.until(EC.visibility_of_element_located((By.XPATH, "/html/body/div[3]/div[2]/div/div[2]/div/div/div/div[1]/div[1]/div[2]/ul/li[1]/a")))
    botaoCasos.click()
    
    cachePath = os.path.join(dirCache, "cachePath.txt")

    # le o path da planilha
    with open(cachePath, 'r') as cache:
        fonte = cache.read()
        
    fonte = pd.read_excel(rf"{fonte}")
    
    atribuicao = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, "slds-radio--faux")))
    atribuicao[1].click()

    avancar = wait.until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[7]/div/div[2]/div/div[3]/div/button[2]")))
    avancar.click()

    for n, CNPJ in enumerate (fonte["CNPJ"]):
        
        CNPJ = formatarCNPJ(CNPJ)

        adabas = fonte.loc[n, "Adabas"]
        try:
            if adabas.lower().strip() == 'movel':
                adabas = '4394'
            elif adabas.lower().strip() == 'fixa':
                adabas = '85107'
            else:
                print(f'ERRO COM O ADABAS {adabas}')
                
                with open(cacheDF, "a") as cache:
                    cache.write(f'"{CNPJ}";"{adabas}";"ERRO ADABAS"\n')
                continue
        except:
            adabas = str(adabas)


        # Clica no campo de ação 
        acao = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, "select")))
        acao[1].click()
        # Opção do CNPJ/CPF
        opcao = wait.until(EC.presence_of_element_located((By.PARTIAL_LINK_TEXT, 'CNPJ/CPF')))
        opcao.click()
        print('CNPJ/CPF OK')

        # campo para inserir cnpj
        campoCNPJ = wait.until(EC.presence_of_element_located((By.XPATH, "//input[@aria-required='true' and @type='text']")))
        campoCNPJ.clear()
        campoCNPJ.send_keys(CNPJ)
       
        # campo para inserir adabas
        campoAdabas = wait.until(EC.presence_of_element_located((By.XPATH, "//input[@placeholder='Pesquisar Adabas...']")))
        campoAdabas.clear()
        campoAdabas.send_keys(adabas)
        
        try:
            try:
                adabasText = WebDriverWait(driver,3).until(EC.presence_of_element_located((By.PARTIAL_LINK_TEXT, 'Patricia Carlos Da Silva')))
                adabasText.click()
            except:
                adabasText = WebDriverWait(driver,3).until(EC.presence_of_element_located((By.PARTIAL_LINK_TEXT, 'Everis Sincronismo')))
                adabasText.click()
        except:
            with open(cacheDF, "a") as cache:
                cache.write(f'"{CNPJ}";"{adabas}";"ERRO ADABAS"\n')
            continue


        # clica em salvar e criar
        botoes = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".slds-button.slds-button_neutral.uiButton.forceActionButton")))
        botoes[1].click()


        try:
            atribuicao = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, "slds-radio--faux")))
            atribuicao[1].click()

            avancar = wait.until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[7]/div/div[2]/div/div[3]/div/button[2]")))
            avancar.click()
            print('CNPJ Ok')
            with open(cacheDF, "a") as cache:
                cache.write(f'"{CNPJ}";"{adabas}";"Ok"\n')
            continue
        except:
            print('Erro com o CNPJ')
            with open(cacheDF, "a") as cache:
                    cache.write(f'"{CNPJ}";"{adabas}";"ERRO CNPJ"\n')
            continue

    driver.quit()
    if page != '':
        botaoRelatorio.visible = True
        page.update()

if __name__ == "__main__":
    sfaCasos('c:\\Users\\Samuel\\Downloads\\Template.xlsx')