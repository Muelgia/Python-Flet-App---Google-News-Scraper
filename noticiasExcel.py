from noticiasFunc import noticiasFunc
from resumeText import resumirTexto
from datetime import datetime
from funcoesFlet import mostrar_notificacao
import flet as ft

import ntplib
from datetime import datetime, timezone

def obter_data_ntp(data_limite):
    try:
        # Cliente NTP para obter a data/hora atual
        cliente = ntplib.NTPClient()
        resposta = cliente.request('pool.ntp.org')

        # Obtendo a data atual do servidor NTP
        data_atual = datetime.fromtimestamp(resposta.tx_time, tz=timezone.utc).date()

        # Convertendo a data limite para um objeto date
        data_limite_obj = datetime.strptime(data_limite, "%Y-%m-%d").date()

        # Comparação entre as datas
        if data_atual > data_limite_obj:
            print("Fim da DEMO")
            return False
        else:
            print("Demo válida até 31/01")
            return True

    except Exception as e:
        return f"Erro: {e}"

# Chamando a função
data_atual = obter_data_ntp("2025-02-01")
print(data_atual)

def startarApp(page, navegadorEscondido, tema, inputPesquisa, botaoRelatorio, botoesFiltro, botaoPlay):

    botaoRelatorio.disabled = True
    botaoRelatorio.update()

    if data_atual:
        
        try:
            botaoPlay.disabled=True
            botaoPlay.update()

            if botoesFiltro['24 horas']:
                filtroData = 'tbs=qdr:d'
            elif botoesFiltro['1 semana']:
                filtroData = '&tbs=qdr:w'
            elif botoesFiltro['Todas']:
                filtroData = ''
            
            noticias = noticiasFunc(page=page, esconderNavegador=navegadorEscondido, fieldInput=inputPesquisa, filtroData=filtroData)

            print(noticias)

            dicionarioNoticias = []

            for textoNoticia in noticias:

                try:
                    if textoNoticia["texto"] == '':
                        continue
                    
                    noticiaResumida = resumirTexto(texto = textoNoticia["texto"])

                    noticiaLink = textoNoticia['url']

                    tituloNoticia = textoNoticia['titulo']

                    texto = f'"{tituloNoticia}";"{noticiaLink}";"{noticiaResumida}"'
                    texto = texto.replace('\n', ';')
                    texto = texto +'\n'

                    # Caminho e nome do arquivo
                    nome_arquivo = tema

                    dicionarioNoticias.append({
                    "titulo": tituloNoticia,
                    "url": noticiaLink,
                    "Texto": noticiaResumida
                    })

                    print(f"Texto salvo em {nome_arquivo}")
                
                except:
                    print('ERRO')
                    continue

            if not dicionarioNoticias:
                mostrar_notificacao(page=page, texto='Nenhuma notícia encontrada!', icon=ft.icons.WARNING, cor='red', titulo='Atenção')
            else:
                botaoRelatorio.disabled = False
                botaoRelatorio.update()
                mostrar_notificacao(page=page, texto='Busca de notícias finalizada, salve antes de proseguir!', icon=ft.icons.CHECK_CIRCLE_SHARP, cor='green', titulo='FINALIZADO')
            return dicionarioNoticias

        finally:
            botaoPlay.disabled=False
            botaoPlay.update()