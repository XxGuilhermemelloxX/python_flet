import flet as ft
import hashlib
from Backend import *


class Gui:
    def __init__(self) -> None:
        pass

    def main(page: ft.Page):
        back = Backend()
        page.title = 'controle de acesso de pessoas'.title()
        page.vertical_alignment = ft.MainAxisAlignment.CENTER
        page.horizontal_alignment = ft.MainAxisAlignment.CENTER
        alinhamento = ft.MainAxisAlignment.CENTER
        #Criação dos campos
        field_nome = ft.TextField(label='Nome*', width=300)
        field_email = ft.TextField(label='Email*', width=300, keyboard_type=ft.KeyboardType.EMAIL)
        field_tel = ft.TextField(label='Telefone*', width=250, keyboard_type=ft.KeyboardType.PHONE)
        field_sexo = ft.Dropdown(
            width=100,
            options=[
                ft.dropdown.Option('Masculino'),
                ft.dropdown.Option('feminino')
            ]
            , label='SEXO'
        )
        field_senha = ft.TextField(label='Senha*', width=250, password=True)
        field_choise = ft.Dropdown(
            width=350,
            options=[
                ft.dropdown.Option('Nome'),
                ft.dropdown.Option('Email'),
                ft.dropdown.Option('Telefone'),
            ]
            , label='Escolha o campo para alterar'

        )
        field_new_choise = ft.TextField(label='Novo campo', width=500)
        field_ID = ft.TextField(label='Digite o ID', width=200, keyboard_type=ft.KeyboardType.NUMBER)

        # criando a ação dos botões
        def botao_cadastar(e):
            if not field_nome.value:
                field_nome.error_text = "digite seu nome!"
                page.update()
            elif not field_senha.value:
                field_senha.error_text = 'Digite uma senha!'
                page.update()
            elif 8 > len(field_senha.value) < 16:
                field_senha.error_text = 'Digite uma senha no minimo 8 digitos e maximo de 16'
                page.update()
            elif not field_tel.value:
                field_tel.error_text = 'Digite o seu telefone'
                page.update()
            elif not field_tel.value.isdigit():
                field_tel.error_text = 'o telefone só pode ser numeros'
            elif not field_email.value:
                field_email.error_text = 'Digite seu e-mail!'
                page.update()
            elif not field_sexo.value:
                field_sexo.error_text = 'escolha o seu sexo!'
                page.update()

            else:
                field_nome.error_text = ''
                field_senha.error_text = ''
                field_email.error_text = ''
                field_sexo.error_text = ''
                field_tel.error_text = ''
                senha_hash = hashlib.sha256(field_senha.value.encode())
                senha = senha_hash.hexdigest()
                back.inserir(field_nome.value, field_email.value, senha, field_tel.value, field_sexo.value)
                field_nome.value = ''
                field_email.value = ''
                field_sexo.value = ''
                field_tel.value = ''
                field_senha.value = ''
                

            page.update()

        def btn_registrar(e):
            if not field_choise.value:
                field_choise.error_text = 'Escolha uma opção'
                page.update()
            elif not field_new_choise.value:
                field_new_choise.error_text = 'o campo não pode estar vazio'
                page.update()
            elif not field_ID.value:
                field_ID.error_text = 'O Campo está vazio'
                page.update()
            elif not field_ID.value.isdigit():
                field_ID.error_text = 'O ID só pode ser numeros'
                page.update()
            elif field_choise.value == 'Telefone' and not field_new_choise.value.isdigit():
                field_new_choise.error_text = 'O telefone só pode ser numeros'
                page.update()

            else:
                field_choise.error_text = ''
                field_new_choise.error_text = ''
                field_ID.error_text = ''
                id = int(field_ID.value)
                back.editar_dado(id, field_choise.value, field_new_choise.value)
            page.update()

         # adicionado a pagina e as rotas
        def route_change(route):
            back_color = ft.colors.SURFACE_VARIANT
            page.views.clear()
            page.views.append(
                ft.View(
                    '/',
                    [
                        ft.AppBar(title=ft.Text('Cadastro de pessoas'), bgcolor= ft.colors.GREY,center_title=True),
                        ft.Row(
                            [
                                field_nome,
                                field_email
                            ],
                           alignment=alinhamento
                        ),
                        ft.Row(
                            [
                                field_tel,
                                field_senha
                            ],
                           alignment=alinhamento
                        ),

                        ft.Row(

                            [
                                field_sexo
                            ],
                            alignment=alinhamento
                        ),
                        ft.Row(
                            [
                                ft.ElevatedButton('Cadastrar', on_click=botao_cadastar),
                                ft.ElevatedButton('Visualizar', on_click=lambda _:page.go('/visualizar')),
                                ft.ElevatedButton('Editar', on_click=lambda _:page.go('/editar')),

                            ],
                            alignment=alinhamento
                        )
                    ],
                    bgcolor = ft.colors.WHITE,horizontal_alignment=alinhamento,vertical_alignment=alinhamento
                ),
                                                     
            )
            
            if page.route == '/editar':
                page.views.append(
                    ft.View(
                        '/editar',
                        [
                            ft.AppBar(title=ft.Text('Editar cadastro'), bgcolor='#141414',center_title=True),
                            ft.Row([field_choise, field_ID],alignment=alinhamento),
                            ft.Row([field_new_choise],alignment=alinhamento),
                            ft.Row([ft.ElevatedButton('Registrar', on_click=btn_registrar, width=250)],alignment=alinhamento)
                        ]
                    )
                )
            elif page.route == '/visualizar':
                data = back.visualizar()
                list_view = ft.ListView(spacing=8)
                
                if data is not None:
                    for row in data:
                        formated_row = ' - '.join(f'{key}:{value}' for key, value in row.items())
                        id = row['ID']
                        delete_btn = ft.ElevatedButton('Deletar',on_click=lambda event, id=id:delete_linha(id))
                        list_view.controls.append(
                            ft.Row(
                                [
                                    ft.Text(formated_row, text_align=ft.TextAlign.CENTER),
                                    delete_btn,  
                                ], 
                                    alignment=alinhamento
                                    )
                            
                            )      
                    
                page.views.append(
                    ft.View(
                        '/visualizar',
                        [
                                list_view
                            
                        ]
                    )
                )
            
            
            
            page.update()
        

        def delete_linha(index):
            back.excluir(index) 
       
            
           
            
        def pop_view(view):
            page.views.pop()
            top_view = page.views[-1]
            page.go(top_view.route)

        page.on_route_change = route_change
        page.on_view_pop = pop_view
        page.go(page.route)

    
        

      
        

    #ft.app(target=main)   rodar desktop
    ft.app(target=main,view=ft.AppView.WEB_BROWSER)#rodar no browser
