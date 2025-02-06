import flet as ft

# abre notificacao pro usuario
def mostrar_notificacao(texto, page, icon, cor, titulo='Atenção'):
    # abre uma pagina de dialogo
    page.dialog = ft.AlertDialog(
        # declara o titulo como uma Row para poder inserir um icon de alerta
        title=ft.Row([ 
            ft.Icon(icon, color=cor), 
            ft.Text(titulo),
        ]), 
        # mostra o texto de acordo com o que for passado para funcao
        content=ft.Text(texto), 
        # cria o botao de fechar e chama a funcao fechar notificao ao ser clicado
        actions=[ 
            ft.TextButton("Fechar", on_click=lambda e: fechar_notificacao(e=e, page=page))
        ], 
        open=True 
    )
    # atualiza a pagina para refletir as mudancas
    page.update()

# fecha notificacoes
def fechar_notificacao(e, page):
    # declara o valor da notificao para False para fecha-la
    page.dialog.open = False
    # atualiza a pagina para refletir as mudancas
    page.update()

