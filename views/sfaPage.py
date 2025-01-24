import flet as ft
from controllers.Strings import stringsHome
from controllers.planilha import ExcelFunc, criarPlanilha, salvarPlanilha
import pandas as pd
from sfa import sfaCasos


def sfa(page: ft.Page, width: int, height: int):
    
    excelOptions = ExcelFunc()
    corContainer = ft.colors.GREY_400
    subContainer = ft.colors.GREY_300

    #abre notificacao pro usuario
    def mostrar_notificacao(texto):
        #abre uma pagina de dialogo
        page.dialog = ft.AlertDialog(
            #declara o titulo como uma Row para poder inserir um icon de alerta
            title=ft.Row([ 
                ft.Icon(ft.icons.WARNING, color="red"), 
                ft.Text("Atenção"),
            ]), 
            #mostra o texto de acordo com o que for passado para funcao
            content=ft.Text(texto), 
            #cria o botao de fechar e chama a funcao fechar notificao ao ser clicado
            actions=[ 
                ft.TextButton("Fechar", on_click=fechar_notificacao)
            ], 
            open=True 
        )
        #atualiza a pagina para refletir as mudancas
        page.update()

    #fecha notificacoes
    def fechar_notificacao(e):
        #declara o valor da notificao para False para fecha-la
        page.dialog.open = False
        #atualiza a pagina para refletir as mudancas
        page.update()

        
    #-------------------------------------------------------------------------------------------------------------------------------
    #borda arredondada dos containers
    borderContainers = 15

    #barra de rolagem
    rolagem = ft.ListView(expand=1, spacing=5, padding=5, auto_scroll=False,)

# ----------------------------------------------------------------------------------------------------------------------------

    def salvarTemplate(e: ft.FilePickerResultEvent):
        if e.path:
            # Chama a função para criar a planilha
            mensagem = criarPlanilha(e.path)
            # Exibe uma mensagem ao usuário
            page.snack_bar = ft.SnackBar(
                content=ft.Text(mensagem),
                open=True  # Define o estado do SnackBar como "aberto"
            )
            page.update()  # Atualiza a interface para refletir a mudança

    # Criação do FilePicker no modo de salvar arquivo
    save_file_picker = ft.FilePicker(on_result=salvarTemplate)
    page.overlay.append(save_file_picker)


    tituloTemplate = ft.Text("Buscar", text_align="center", size="20", weight=ft.FontWeight.BOLD)
 
    # Botão para abrir o FilePicker no modo de salvar
    inputPesquisa = ft.TextField(hint_text='Desejo notícias sobre: ')

    TemplateColumn = ft.Column(
        controls=[
            tituloTemplate, inputPesquisa
            ],
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
    )

    ContainerTemplate = ft.Container(
                #cadastro emails
                content=ft.Column(
                    [   
                        TemplateColumn,
                    ],
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=10,
                ),
                #padding do container
                padding=10,
                #cor do container
                bgcolor=subContainer,
                #altura da pagina total
                height=135, 
                #tamanho em colunas MAX12 de acordo com os tamanhos de dispositivos
                col={'sm':12, 'md':6, 'xl':6},  
                #borda arredondada 
                border_radius=ft.border_radius.all(borderContainers),
            )
# ----------------------------------------------------------------------------------------------------------------
 
    # Botão para abrir o FilePicker no modo de salvar
    botaoPlay = ft.ElevatedButton(
        text="Play", disabled=True,
        on_click=lambda e: sfaCasos(botaoRelatorio=relatorio, page=page),
    )

    tituloPlayGrid = ft.Row(
        alignment=ft.MainAxisAlignment.CENTER,
        controls=[ 
            ft.Text("Iniciar Busca", text_align="center", size="20", weight=ft.FontWeight.BOLD),
        ]
    )

    ContainerPlay = ft.Container(
                #cadastro emails
                content=ft.Column(
                    [   
                        tituloPlayGrid, botaoPlay
                    ],
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=10,
                ),
                #padding do container
                padding=10,
                #cor do container
                bgcolor=subContainer,
                #altura da pagina total
                height=135, 
                #tamanho em colunas MAX12 de acordo com os tamanhos de dispositivos
                col={'sm':12, 'md':6, 'xl':6},  
                #borda arredondada 
                border_radius=ft.border_radius.all(borderContainers),
            )


# ----------------------------------------------------------------------------------------------------------------

    def salvarRelatorio(e: ft.FilePickerResultEvent):
        if e.path:
            # Chama a função para salvar a planilha
            mensagem = salvarPlanilha(e.path, )
            # Exibe uma mensagem ao usuário
            page.snack_bar = ft.SnackBar(
                content=ft.Text(mensagem),
                open=True  # Define o estado do SnackBar como "aberto"
            )
            page.update()  # Atualiza a interface para refletir a mudança

    # Criação do FilePicker no modo de salvar arquivo
    save_file_relatorio = ft.FilePicker(on_result=salvarRelatorio)
    page.overlay.append(save_file_relatorio)
    
    # Botão para abrir o FilePicker no modo de salvar
    relatorio = ft.ElevatedButton(
        text="Salvar Relatório", visible=False,
        on_click=lambda e: save_file_relatorio.get_directory_path()
    )

    tituloRelatorioGrid = ft.Row(
        alignment=ft.MainAxisAlignment.CENTER,
        controls=[ 
            ft.Text("Salvar Relatório", text_align="center", size="20", weight=ft.FontWeight.BOLD),
            relatorio
        ]
    )

    relatorioColumn = ft.Column(
        controls=[
            tituloRelatorioGrid
            ],
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
    )

    ContainerRelatorio = ft.Container(
                #cadastro emails
                content=ft.Column(
                    [   
                        relatorioColumn,
                    ],
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=10,
                ),
                #padding do container
                padding=10,
                #cor do container
                bgcolor=subContainer,
                #altura da pagina total
                height=135, 
                #tamanho em colunas MAX12 de acordo com os tamanhos de dispositivos
                col={'sm':12, 'md':6, 'xl':6},  
                #borda arredondada 
                border_radius=ft.border_radius.all(borderContainers),
            )
    
# ----------------------------------------------------------------------------------------------------------------

    #imagem do boneco morto
    img_local = ft.Image(src="bonecoMorto.png", width=280, height=280)

    imagemColumn = ft.Column(
        controls=[
            img_local
            ],
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
    )

#------------------------------------------------------------------------------------------------------------------

   
#------------------------------------------------------------------------------------------------------------------
    #responsive row adiciona a barra de rolagem
    rolagem.controls.append(ft.ResponsiveRow(
        #chaves do responsive row
        [   
            #container como parametro do responsive row
            ft.Container(
                #cadastro emails
                content=ft.Column(
                    [  
                        ContainerTemplate, ContainerPlay,ContainerRelatorio
                    ],
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=10,
                ),
                #padding do container
                padding=10,
                #cor do container
                bgcolor=corContainer,
                #altura da pagina total
                height=445, 
                #tamanho em colunas MAX12 de acordo com os tamanhos de dispositivos
                col={'sm':12, 'md':6, 'xl':6},  
                #borda arredondada 
                border_radius=ft.border_radius.all(borderContainers) 
            ),

            ft.Container(
                #cadastro emails
                content=ft.Column(
                    [   
                        imagemColumn
                    ],
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=10,
                ),
                #padding do container
                padding=10,
                #cor do container
                bgcolor=corContainer,
                #altura da pagina total
                height=445, 
                #tamanho em colunas MAX12 de acordo com os tamanhos de dispositivos
                col={'sm':12, 'md':6, 'xl':6},  
                #borda arredondada 
                border_radius=ft.border_radius.all(borderContainers) 
            ),

            
        ],
    ))

    view = ft.View(
        route='/disparador',
        bgcolor=ft.colors.SURFACE_CONTAINER_HIGHEST,
        controls=[
            ft.ResponsiveRow(
                [
                    rolagem, 
                ]
            )
        ]
    )

    return view
