import flet as ft
from controllers.Strings import stringsHome

def home(page: ft.Page, width: int, height: int):
    
    rolagem = ft.ListView(expand=1, spacing=10, padding=20, auto_scroll=False,)
    
    #elementos de rolagem da pagina de aviso
    rolagem.controls.append(ft.Column(
                            controls=[
                                # titulo
                                ft.Text(
                                    value='Bem vindo'.upper(),
                                    size=20,
                                    weight='bold',
                                    color=ft.colors.with_opacity(0.5, 'black')
                                ),

                                ft.Divider(
                                    height=1,
                                    thickness=2
                                ),
                                # texto vindo das strings.py
                                ft.Text(
                                    value=stringsHome['Bem vindo'],
                                    size=15,
                                    weight='bold',
                                    color=ft.colors.with_opacity(0.5, 'black'),
                                    text_align='center'
                                ),
                                # botao de icone que quando clicado leva para proxima pagina
                                ft.IconButton(
                                    icon=ft.icons.LOGIN,
                                    icon_size=30,
                                    icon_color=ft.colors.BLACK,
                                    tooltip='Login',
                                    on_click= lambda e: page.go('/sfa')
                                )
                            ],
                            # alinhamento da pagina no centro
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER
                        ))

    view = ft.View(
        route='/',
        bgcolor=ft.colors.SURFACE_CONTAINER_HIGHEST,
        controls=[
            
            ft.ResponsiveRow(
                width=width, 
                height=height,

                controls=[
                    ft.Container(
                        col={'sm':10, 'md':6, 'xl':6},
                        height = 300,
                        bgcolor = ft.colors.GREY_400,
                        border_radius = ft.border_radius.all(12),
                        padding=ft.padding.all(12),
                        content=rolagem
                    )
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,    
            )
        ]
    )

    return view