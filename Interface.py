from  customtkinter import *
# import ttkbootstrap as ttk
# from ttkbootstrap.constants import *
from tkinter import ttk
from tkinter import messagebox
import customtkinter as ctk
import databaset
import hashlib
import binascii
from email_validator import validate_email, EmailNotValidError

home = CTk()

class Sistema():

    def __init__(self):
        self.home = home
        self.tela_padrao()
        self.tela_home()
        home.mainloop()

    def tela_padrao(self):
        self.home.geometry("700x400")
        self.home.title("SMS - Home")
        self.home.resizable(False, False)

    def tela_home(self):
        # definir tamanho de quadro
        frame_home = CTkFrame(master = home, width = 650, height = 350)
        frame_home.pack(pady= 20, padx = 20)

        # widgets login
        login_label = CTkLabel(master = frame_home, text = "Faça seu Login", font= ("Roboto", 20)).place(x= ((650-150)/2), y=20)

        # digite seu cpf
        cpf_entry_str = ctk.StringVar()
        cpf_entry = CTkEntry(master = frame_home, placeholder_text="Digite o CPF", width = 300, textvariable=cpf_entry_str).place(x= ((650-150)/2), y=70)
        cpf_label = CTkLabel(master = frame_home, text = "*O campo CPF é obrigatório.", text_color = "red", font = ("Roboto", 10)).place(x= ((650-150)/2), y=100)

        # digite sua senha
        senha_entry_str = ctk.StringVar()
        senha_entry = CTkEntry(master = frame_home, placeholder_text="Digite a senha", width = 300, show = "*", textvariable=senha_entry_str).place(x= ((650-150)/2), y=145)
        senha_label = CTkLabel(master = frame_home, text = "*O campo senha é obrigatório.", text_color = "red", font = ("Roboto", 10)).place(x= ((650-150)/2), y=175)

        # não sou um robo
        not_robot = ctk.StringVar(value="off")
        nao_robo_check = CTkCheckBox(master = frame_home, text= "Não sou um robo",variable=not_robot, onvalue="on", offvalue="off").place(x= ((650 - 150)/2), y = 205)

        def cpf_save():
            cpf_salvo = vcpf
            return cpf_salvo
        # def auth():
        #     auth_check = vauth
        #     vauth = 0
        #     return auth_check

        def user_log():
            global vcpf
            check_in = not_robot.get()
            # global vauth
            def user_login(vcpf, vsenha):
                # vauth = vauth
                databaset.cursor.execute("SELECT SENHA, AUTORIZAÇÃO FROM user WHERE CPF = ?", (vcpf,))
                rs = databaset.cursor.fetchone()

                if rs is None:
                    return False
            #cirptografia armazenada no cadastro
                vs_crip_arm = rs[0]
                Uauth = rs[1]

            #criptografia atual
                hasher = hashlib.sha256()
                hasher.update(vsenha.encode('utf-8'))
                vs_crip_forn = hasher.hexdigest()

                return str(vs_crip_arm.decode('utf-8')) == vs_crip_forn and Uauth ==2

            def adm_login(vcpf, vsenha):

                databaset.cursor.execute("SELECT SENHA, AUTORIZAÇÃO FROM user WHERE CPF = ?", (vcpf,))
                rs = databaset.cursor.fetchone()

                if rs is None:
                    return False
            #cirptografia armazenada no cadastro
                vs_crip_arm = rs[0]
                vauth = rs[1]

            #criptografia atual
                hasher = hashlib.sha256()
                hasher.update(vsenha.encode('utf-8'))
                vs_crip_forn = hasher.hexdigest()

                return str(vs_crip_arm.decode('utf-8')) == vs_crip_forn and vauth == 1

            t = 3 # number of tries to login
            while t > 0 :
                vcpf = cpf_entry_str.get()
                vsenha = senha_entry_str.get()


                if user_login(vcpf, vsenha) and check_in == "on":
                    print("Login bem-sucedido!")
                    span = messagebox.showinfo(title="LOGIN", message= "LOGIN EFETUADO! BEM-VINDO!")
                    menu_user()

                elif adm_login(vcpf, vsenha) and check_in == "on":
                    print("Login bem-sucedido!")
                    span = messagebox.showinfo(title="LOGIN", message= "LOGIN EFETUADO! BEM-VINDO!")
                    menu_admin()

                elif check_in == "off":
                    print("Você é um robô?")
                    span = messagebox.showinfo(title="ALERTA", message= "Você é um robô? Confirme os dados e tente novamente.")

                else:
                    t -= 1
                    print(f"CPF ou senha incorretos. Tente novamente. Restam {t} tentativas")
                    span = messagebox.showinfo(title="ALERTA", message= f"Confirme os dados e tente novamente. Você tem {t} tentativas.")
                break
            if t == 0:
                print("Você excedeu o número de tentativas permitidas. Tente novamente mais tarde.")
                span = messagebox.showwarning(title="!!!!ALERTA!!!!", message= "ACESSO NEGADO!")
                quit()

        def menu_user():
            # remover frame de cad
            frame_home.pack_forget()

            # tela de cadastro de usuários
            frame_uMenu = CTkFrame(master = home, width = 650, height = 370)
            frame_uMenu.pack(pady= 20, padx = 20)

            vcpf = cpf_save()
            databaset.cursor.execute("SELECT * FROM user WHERE CPF = ?", (vcpf,))
            dados_user = databaset.cursor.fetchone()
            menu_user_Label = CTkLabel(master = frame_uMenu, text = f"Bem-Vindo, {dados_user[2]}.\nEste é o menu do usuário", font= ("Roboto", 20)).place(x= ((650-150)/2), y=20)

            def comprar():
                global carrinho
                carrinho = []

                # remover frame de cad
                frame_uMenu.pack_forget()

                frame_comprar = CTkFrame(master = home, width = 650, height = 370)
                frame_comprar.pack(pady= 20, padx = 20)

                compras_tree = ttk.Treeview(frame_comprar)
                compras_tree['columns'] = ("ID", "CATEGORIA", "SABOR", "PREÇO", "QUANTIDADE")

                compras_tree.column("ID", width=50, anchor=CENTER)
                compras_tree.heading("ID", text="ID")

                compras_tree.column("CATEGORIA", width=70, anchor=W)
                compras_tree.heading("CATEGORIA", text="CATEGORIA")

                compras_tree.column("SABOR", width=100, anchor=W)
                compras_tree.heading("SABOR", text="SABOR")

                compras_tree.column("PREÇO", width=70, anchor=CENTER)
                compras_tree.heading("PREÇO", text="PREÇO")

                compras_tree.column("QUANTIDADE", width=100, anchor=CENTER)
                compras_tree.heading("QUANTIDADE", text="QUANTIDADE")

                databaset.cursor.execute("SELECT * FROM products")
                produtos = databaset.cursor.fetchall()

                compras_tree.place(x=250, y=20, width = 380, height = 150)

                for produto in produtos:
                    compras_tree.insert("", "end", values=(produto[0], produto[1], produto[2], produto[3], produto[4]))


                # comprar_label = CTkLabel(master = frame_comprar, text = "Hora de comprar", font= ("Roboto", 20)).place(x= 10, y=20)
                id_entry_str = ctk.StringVar()
                id_label = CTkLabel(master = frame_comprar, text="ID:", font = ("Robot", 12)).place(x=250, y =190)
                id_entry = CTkEntry(master = frame_comprar, placeholder_text="ID", width= 100, textvariable=id_entry_str).place(x= 250, y= 215)

                categoria_entry_str = ctk.StringVar()
                categoria_entry = CTkEntry(master = frame_comprar, placeholder_text="Categoria", width=152.5, textvariable=categoria_entry_str).place(x= 250, y =250)

                sabor_entry_str = ctk.StringVar()
                sabor_entry = CTkEntry(master = frame_comprar, placeholder_text="Sabor", width=152.5,textvariable=sabor_entry_str).place(x= 420, y = 250)

                preco_entry_str = ctk.StringVar()
                preco_entry = CTkEntry(master = frame_comprar, placeholder_text="Preco",width=152.5, textvariable=preco_entry_str).place(x= 250, y = 285)

                quantidade_entry_str = ctk.StringVar()
                quantidade_entry = CTkEntry(master = frame_comprar, placeholder_text="Quantidade",width=152.5, textvariable=quantidade_entry_str).place(x= 420, y = 285)

                def id_save():
                    id_prod = id_save
                    return id_prod

                def clicar_buscar():
                    global id_prod

                    id_prod = id_entry_str.get()
                    databaset.cursor.execute("SELECT * FROM products WHERE ID = ?", (id_prod,))
                    dados_prod = databaset.cursor.fetchone()

                    if dados_prod is not None:
                        categoria_entry_str.set(dados_prod[1])
                        sabor_entry_str.set(dados_prod[2])
                        preco_entry_str.set(dados_prod[3])
                        quantidade_entry_str.set(dados_prod[4])

                    else:
                        span = messagebox.showerror(title="Error!", message= "Produto não encontrado")
                # procurar produtos
                procurar_button = CTkButton(master = frame_comprar, text="Buscar ID", width=198, command= clicar_buscar,font = ("Roboto", 12, "bold"), text_color= "white")
                procurar_button.pack(padx=10,pady=10)
                procurar_button.place(x= 375, y= 215)

                def add():# função adicionar carrinho de compras
                    global carrinho

                    id_prod = id_entry_str.get()
                    quantity = int(quantidade_entry_str.get())

                    databaset.cursor.execute("SELECT * FROM products WHERE ID=?", (id_prod,))
                    product = databaset.cursor.fetchone()

                    if product and product[4] >= quantity:
                        carrinho.append((id_prod, quantity))
                        span = messagebox.showinfo(title = "ADICIONANDO ITENS NO CARRINHO!", message=f"Seu carrrihno está com {quantity} {product[1]} {product[2]}")
                        print(f"Adicionado {quantity} {product[1]} no carrinho.")
                        new_quantity = product[4] - quantity
                        databaset.cursor.execute("UPDATE products SET QUANTIDADE=? WHERE ID=?", (new_quantity, id_prod))
                        databaset.conn.commit()

                    else:
                        span = messagebox.showerror(title="Error!", message="Produto não encontrado ou quantidade insuficiente.")
                        print("Produto não encontrado ou quantidade insuficiente.")
                        return False

                # adicionar produtos ao carrinho
                adicionar_button = CTkButton(master = frame_comprar, text= "Adicionar", width = 100, command= add, fg_color="green",font = ("Roboto", 12, "bold"), text_color= "white")
                adicionar_button.pack(padx=10,pady=10)
                adicionar_button.place(x= 250, y= 320)

                def remove():# função remover do carrinho
                    global carrinho

                    id_prod = id_entry_str.get()
                    quantity = int(quantidade_entry_str.get())

                    databaset.cursor.execute("SELECT * FROM products WHERE ID=?", (id_prod,))
                    product = databaset.cursor.fetchone()

                    if product and product[4] >= quantity:
                        for item in carrinho:
                            if item[0] == id_prod:
                                if item[1]>= quantity:
                                    carrinho.remove(item)
                                    span = messagebox.showinfo(title = "REMOVENDO ITENS DO CARRINHO!", message=f"Removido {quantity} {product[1]} de {product[2]}")
                                    print(f"Removido {quantity} {product[1]} de {product[2]} do carrinho.")
                                    new_quantity = product[4] + quantity
                                    databaset.cursor.execute("UPDATE products SET QUANTIDADE=? WHERE ID=?", (new_quantity, id_prod))
                                    databaset.conn.commit()
                                    break

                #   remover produtos do carrinho
                remove_button = CTkButton(master = frame_comprar, text="Remover", width=100, command = remove, fg_color="red", font = ("Roboto", 12, "bold"), text_color= "white")
                remove_button.pack(padx=10,pady=10)
                remove_button.place(x= 365, y= 320)

                def finalizar():# finalizar produtos do carrinho
                    global carrinho
                    total_cost = 0

                    for item in carrinho:
                        databaset.cursor.execute("SELECT PRECO FROM products WHERE ID=?", (item[0],))
                        price = databaset.cursor.fetchone()

                        total_cost += price[0] * item[1]

                    span = messagebox.showinfo(title="Compra finalizada!", message=f"Custo da compra: R${total_cost} ")
                    print(f"Custo da compra: R${total_cost}")
                    carrinho.clear()

                # Finalizar compras
                finalizar_button = CTkButton(master = frame_comprar, text="Finalizar", width=100, command=finalizar,font = ("Roboto", 12, "bold"), text_color= "white")
                finalizar_button.pack(padx=10,pady=10)
                finalizar_button.place(x= 475, y= 320)

                def voltar():
                # remover frame de cadastro
                    frame_comprar.pack_forget()

                # tela de home
                    frame_uMenu.pack(pady= 20, padx = 20)

                # voltar ao menu
                voltar_button = CTkButton(master = frame_comprar, text="Voltar", width=30, height = 135, command = voltar,font = ("Roboto", 12, "bold"), text_color= "white")
                voltar_button.pack(padx=10,pady=10)
                voltar_button.place(x= 580, y= 215)

            comprar_button = CTkButton(master = frame_uMenu, text = "Comprar", width= 180, command=comprar,font = ("Roboto", 12, "bold"), text_color= "white")
            comprar_button.pack(pady = 10, padx = 10)
            comprar_button.place(x=250, y=80)

            def alterar_dados():
                # remover frame de cad
                frame_uMenu.pack_forget()

                frame_alterar = CTkFrame(master = home, width = 650, height = 370)
                frame_alterar.pack(pady= 20, padx = 20)

                alter_label = CTkLabel(master = frame_alterar, text = "Alterar Dados de usuário", font= ("Roboto", 20)).place(x= ((650-150)/2), y=20)
                campos_label = CTkLabel(master = frame_alterar, text = "*Digite apenas onde quer alterar.", text_color = "red", font = ("Roboto", 12)).place(x= ((650-150)/2), y= 50)

                alternome_str = ctk.StringVar()
                alter_nome = CTkEntry(master = frame_alterar, placeholder_text="Nome completo", width = 300, textvariable=alternome_str).place(x= 290, y=120)
                alter_nome_label = CTkLabel(master = frame_alterar, text="Nome", font = ("Roboto", 12), text_color="black").place(x= 250,y = 120)

                alteremail_str = ctk.StringVar()
                alter_email = CTkEntry(master = frame_alterar, placeholder_text="E-mail", width = 300, textvariable=alteremail_str).place(x= 290, y=160)
                alter_email_label = CTkLabel(master = frame_alterar, text="Email", font = ("Roboto", 12), text_color="black").place(x= 250,y = 160)

                altersenha_str = ctk.StringVar()
                alter_senha = CTkEntry(master = frame_alterar, placeholder_text="Senha", width = 300, show = "*", textvariable=altersenha_str).place(x= 290, y=200)
                alter_senha_label = CTkLabel(master = frame_alterar, text="Senha", font = ("Roboto", 12), text_color="black").place(x= 250,y = 200)

                altersenha_conf_str = ctk.StringVar()
                alter_senha_confirma = CTkEntry(master = frame_alterar, placeholder_text="Repita sua senha", width = 300, show= "*", textvariable=altersenha_conf_str).place(x= 290, y=240)
                alter_senha1_label = CTkLabel(master = frame_alterar, text="Senha", font = ("Roboto", 12), text_color="black").place(x= 250,y = 240)

                vcpf = cpf_save()
                databaset.cursor.execute("SELECT * FROM user WHERE CPF = ?", (vcpf,))
                dados_user = databaset.cursor.fetchone()

                alternome_str.set(dados_user[2])
                alteremail_str.set(dados_user[1])
                altersenha_str.set(dados_user[4])
                altersenha_conf_str.set(dados_user[4])

                def conf_alteracao():
                    alter_nome = alternome_str.get()
                    alter_email = alteremail_str.get()
                    alter_senha = altersenha_str.get()
                    alter_senha1 = altersenha_conf_str.get()

                    vcpf = cpf_save()

                    def criptar_novasenha(alter_senha):
                        #verifica se a senha contém pelo menos 1 caracter de cada
                        letter = any(c.isalpha() for c in alter_senha)
                        number = any(c.isdigit() for c in alter_senha)
                        spchar = any(c in "!@#$%&*?" for c in alter_senha)
                        lenght = len(alter_senha) <= 18

                        return letter and number and spchar and lenght

                    def cript_pass(alter_senha):

                        if criptar_novasenha(alter_senha):
                            hasher1 = hashlib.sha256()
                            hasher1.update(alter_senha.encode('utf-8'))
                            senha_hash = hasher1.digest()
                            vsenhacrip = binascii.hexlify(senha_hash)
                            return vsenhacrip

                    def verificar_email(alter_email):
                        try:
                            # Valida o email usando a função validate_email
                            valid = validate_email(alter_email)
                            return True
                        except EmailNotValidError as e:
                            # Captura a exceção EmailNotValidError caso o email não seja válido
                            print(str(e))
                            return False

                    def verificar_nome(alter_nome):
                        if all((c.isalpha() or c.isspace()) for c in alter_nome) and  len(alter_nome) > 0:
                            return True
                        else:
                            return False

                    if alter_senha == alter_senha1 and criptar_novasenha(alter_senha) and verificar_email(alter_email) and verificar_nome(alter_nome):
                        vsenhacrip = cript_pass(alter_senha)

                        databaset.cursor.execute("UPDATE user SET NOME = ?, EMAIL = ?, SENHA = ? WHERE CPF = ?", (alter_nome, alter_email, vsenhacrip, vcpf,))
                        databaset.conn.commit()
                        span = messagebox.showinfo(title="Alteração Realizada!", message="Os dados foram, alterados com sucesso!, faça login novamente...")
                        databaset.conn.close()
                        home.destroy()
                    else:
                        span = messagebox.showinfo(title="Erro!", message="As senhas não coincidem ou não atendem aos requisitos de segurança, tente novamente!")

                confirmar_alteracao = CTkButton(master = frame_alterar, text="Enviar", width=150, command = conf_alteracao,font = ("Roboto", 12, "bold"), text_color= "white")
                confirmar_alteracao.pack(padx = 10, pady = 10)
                confirmar_alteracao.place(x=((650-150)/2), y =280)

                def voltar():
                # remover frame de cadastro
                    frame_alterar.pack_forget()

                # tela de home
                    frame_uMenu.pack(pady= 20, padx = 20)

                voltar_button = CTkButton(master = frame_alterar, text = "Voltar", width = 110,fg_color="green", command= voltar,font = ("Roboto", 12, "bold"), text_color= "white")
                voltar_button.pack(padx = 10, pady = 10)
                voltar_button.place(x= 480, y = 280)

            alter_button = CTkButton(master = frame_uMenu, text = "Alterar dados", width = 180, command= alterar_dados,font = ("Roboto", 12, "bold"), text_color= "white")
            alter_button.pack(padx = 10, pady = 10)
            alter_button.place(x=450, y=80)

            def excluir_usuário():
                frame_uMenu.pack_forget()

                frame_excluir = CTkFrame(master = home, width = 650, height = 370)
                frame_excluir.pack(pady= 20, padx = 20)

                excl_label = CTkLabel(master = frame_excluir, text = "Confirme a senha para excluir este usuário", font= ("Roboto", 20)).place(x= ((650-150)/2), y=20)

                exclsenha_str = ctk.StringVar()
                excl_senha = CTkEntry(master = frame_excluir, placeholder_text="Senha", width = 270, textvariable=exclsenha_str, show = "*").place(x= 350, y=120)
                excl_label = CTkLabel(master = frame_excluir, text="senha", font = ("Roboto", 12), text_color="black").place(x= 250,y = 120)

                exclsenha1_str = ctk.StringVar()
                excl_senha1 = CTkEntry(master = frame_excluir, placeholder_text="Repita a senha", width = 270, textvariable=exclsenha1_str, show = "*").place(x= 350, y=160)
                excl_label = CTkLabel(master = frame_excluir, text="Repita a senha", font = ("Roboto", 12), text_color="black").place(x= 250,y = 160)

                def excluir_user():

                    vcpf = cpf_save()

                    def confirmar_excl(vcpf, vsenha):

                        databaset.cursor.execute("SELECT SENHA FROM user WHERE CPF = ?", (vcpf,))
                        rs = databaset.cursor.fetchone()

                        excl_senha = exclsenha_str.get()
                        excl_senha1 = exclsenha1_str.get()

                        if rs is None:
                            return False
                        #cirptografia armazenada no cadastro
                        vs_crip_arm = rs[0]

                        #criptografia atual
                        hasher = hashlib.sha256()
                        hasher.update(vsenha.encode('utf-8'))
                        vs_crip_forn = hasher.hexdigest()

                        if str(vs_crip_arm.decode('utf-8')) == vs_crip_forn:
                            return True
                        else:
                            return False

                    vcpf = cpf_save()
                    databaset.cursor.execute("SELECT count(*), EMAIL, NOME, AUTORIZAÇÃO FROM user WHERE CPF = ?", (vcpf,))
                    rs = databaset.cursor.fetchone()

                    if rs[0] > 0:
                        print ("Usuário localizado")
                        print ("Email: ", rs[1])
                        print ("Nome: ", rs[2])

                        print("QUAL A SENHA DO USUÁRIO QUE DESEJA EXCLUIR?")

                        vsenha = exclsenha1_str.get()


                        if excl_senha == excl_senha1 and confirmar_excl(vcpf, vsenha):
                            confirmation = messagebox.askyesno(title = "Confirmar ação", message = "Tem certeza que quer excluir seu usuário? A ação NÃO PODE ser desfeita!")
                        # Enviar instrução SQL para ser executada
                            if confirmation:
                                span = messagebox.showwarning(title="SEU USUÁRIO SERÁ EXCLUÍDO", message = "ADEUS, ;(")
                                databaset.conn.execute("DELETE FROM user WHERE CPF = " + vcpf)
                                databaset.conn.commit()
                                print("USUÁRIO EXCLUÍDO COM SUCESSO!")
                                home.destroy()
                            else:
                                print("Obrigado por ficar! :)")
                    else:
                        span = messagebox.showerror(title ="!!ALERTA!!", message = "VOCÊ NÃO TEM PERMISSÃO PARA EXCLUIR!")
                        print("VOCÊ NÃO PODE EXCLUIR ESTE USUÀRIO!")


                excl_button = CTkButton(master = frame_excluir, text = "EXCLUIR", width = 200, command = excluir_user,fg_color="red", font = ("Roboto", 12, "bold"), text_color= "white")
                excl_button.pack(padx = 10, pady = 10)
                excl_button.place(x=((650-150)/2), y =200)

                def voltar():
                # remover frame de cadastro
                    frame_excluir.pack_forget()

                # tela de home
                    frame_uMenu.pack(pady= 20, padx = 20)

                exclsair_button = CTkButton(master = frame_excluir, text = "Sair", width= 100, fg_color="green", command = voltar, font = ("Roboto", 12, "bold"), text_color= "white")
                exclsair_button.pack(padx = 10, pady = 10)
                exclsair_button.place(x=520, y = 200)

            excluir_button = CTkButton(master = frame_uMenu, text = "Excluir minha conta", width = 180, command = excluir_usuário,font = ("Roboto", 12, "bold"), text_color= "white")
            excluir_button.pack(padx = 10, pady = 10)
            excluir_button.place(x=250, y= 120)

            def voltar():
                # remover frame de cadastro
                frame_uMenu.pack_forget()

                # tela de home
                frame_home.pack(pady= 20, padx = 20)

            sair_button = CTkButton(master = frame_uMenu, text = "Sair", width= 180, fg_color="green",font = ("Roboto", 12, "bold"), text_color= "white", command = voltar)
            sair_button.pack(padx = 10, pady = 10)
            sair_button.place(x=450, y = 120)

            vcpf = cpf_save()
            databaset.cursor.execute("SELECT * FROM user WHERE CPF = ?", (vcpf,))
            dados_user = databaset.cursor.fetchone()

            meus_dados = CTkLabel(master=frame_uMenu, text="Meus Dados: ", font=("Roboto", 14)).place(x=((650-150)/2), y=180)
            cpf_label = CTkLabel(master = frame_uMenu, text=f"CPF: {dados_user[0]}", font=("Roboto", 18)).place(x= ((650-150)/2), y= 200)
            nome_label = CTkLabel(master = frame_uMenu, text=f"Email: {dados_user[1]}", font=("Roboto", 18)).place(x= ((650-150)/2), y= 230)
            email_label = CTkLabel(master = frame_uMenu, text=f"Nome: {dados_user[2]}", font=("Roboto", 18)).place(x= ((650-150)/2), y= 260)

        def menu_admin():
            # remover frame de login
            frame_home.pack_forget()

            # tela de cadastro de usuários
            frame_menu_adm = CTkFrame(master = home, width = 650, height = 370)
            frame_menu_adm.pack(pady= 20, padx = 20)

            area_administrador = CTkLabel(master = frame_menu_adm, text ="Olá, administrador.", font= ("Roboto", 20)).place(x= 250, y=20)
            dados_entry = CTkLabel(master = frame_menu_adm, text= "Digite o que gostaria de consultar que gostaria de pesquisar!", font= ("Roboto", 14)).place(x= 250, y=50)

            def id_cpf_save():
                id_cpf = id_cpf_save
                return id_cpf
            # seleciona qual tabela vai ser usada
            def Select():

                global id_cpf

                id_cpf = id_cpf_procurar_str.get()
                dado1 = dado1_entry_str.get()
                dado2 = dado2_entry_str.get()
                dado3 = dado3_entry_str.get()
                dado4 = dado4_entry_str.get()
                procurar = procurar_entry_str.get().upper()
                
                if procurar == "PRODUTOS":
                    databaset.cursor.execute("SELECT * FROM products WHERE ID = ?", (id_cpf,))
                    dados_prod = databaset.cursor.fetchone()

                    if dados_prod is not None:
                        dado1_entry_str.set(dados_prod[1])
                        dado2_entry_str.set(dados_prod[2])
                        dado3_entry_str.set(dados_prod[3])
                        dado4_entry_str.set(dados_prod[4])
                
                elif procurar == "USUÁRIOS":
                    databaset.cursor.execute("SELECT * FROM user WHERE CPF = ?", (id_cpf,))
                    dados_user = databaset.cursor.fetchone()

                    if dados_user is not None:
                        dado1_entry_str.set(dados_user[1])
                        dado2_entry_str.set(dados_user[2])
                        dado3_entry_str.set(dados_user[3])
                        dado4_entry_str.set(dados_user[4])

                else:
                    span = messagebox.showerror(title="Error!", message= "Produto não encontrado")

                if procurar == "PRODUTOS":
                        # tabelas do banco de dados
                        consulta_produto_tree = ttk.Treeview(frame_menu_adm)
                        consulta_produto_tree['columns'] = ("ID", "CATEGORIA", "SABOR", "PREÇO", "QUANTIDADE")

                        consulta_produto_tree.column("ID", width=50, anchor=CENTER)
                        consulta_produto_tree.heading("ID", text="ID")

                        consulta_produto_tree.column("CATEGORIA", width=70, anchor=W)
                        consulta_produto_tree.heading("CATEGORIA", text="CATEGORIA")

                        consulta_produto_tree.column("SABOR", width=100, anchor=W)
                        consulta_produto_tree.heading("SABOR", text="SABOR")

                        consulta_produto_tree.column("PREÇO", width=70, anchor=CENTER)
                        consulta_produto_tree.heading("PREÇO", text="PREÇO")

                        consulta_produto_tree.column("QUANTIDADE", width=100, anchor=CENTER)
                        consulta_produto_tree.heading("QUANTIDADE", text="QUANTIDADE")

                        databaset.cursor.execute("SELECT * FROM products")
                        produtos = databaset.cursor.fetchall()

                        consulta_produto_tree.place(x=20, y=20, width = 200, height = 300)

                        for produto in produtos:
                            consulta_produto_tree.insert("", "end", values=(produto[0], produto[1], produto[2], produto[3], produto[4]))

                elif procurar == "USUÁRIOS":
                    consulta_usuario_tree = ttk.Treeview(frame_menu_adm)
                    consulta_usuario_tree['columns'] = ("CPF", "EMAIL", "NOME", "SENHA", "AUTH")

                    consulta_usuario_tree.column("CPF", width=50, anchor=CENTER)
                    consulta_usuario_tree.heading("CPF", text="CPF")

                    consulta_usuario_tree.column("EMAIL", width=70, anchor=W)
                    consulta_usuario_tree.heading("EMAIL", text="EMAIL")

                    consulta_usuario_tree.column("NOME", width=100, anchor=W)
                    consulta_usuario_tree.heading("NOME", text="NOME")

                    consulta_usuario_tree.column("SENHA", width=70, anchor=CENTER)
                    consulta_usuario_tree.heading("SENHA", text="SENHA")

                    consulta_usuario_tree.column("AUTH", width=100, anchor=CENTER)
                    consulta_usuario_tree.heading("AUTH", text="AUTH")

                    databaset.cursor.execute("SELECT * FROM user")
                    users = databaset.cursor.fetchall()

                    consulta_usuario_tree.place(x=20, y=20, width = 200, height = 300)

                    for user in users:
                        consulta_usuario_tree.insert("", "end", values=(user[0], user[1], user[2], user[3], user[4]))

            procurar_button = CTkButton(master = frame_menu_adm, text="Procurar", font=("Roboto", 15, "bold"), width = 75, command = Select)
            procurar_button.pack(padx=20, pady=20)
            procurar_button.place(x= 395, y= 115)
            
            # tabelas = ["Produtos", "Usuários"]
            # procurar = CTkComboBox(master = frame_menu_adm, values=tabelas, command=Select).place(x= 250, y= 125)
            procurar_label = CTkLabel(master = frame_menu_adm, text= "Produtos ou usuários? ", font=("Roboto", 12)).place(x=255, y= 90)
            procurar_entry_str = ctk.StringVar()
            procurar_entry = CTkEntry(master= frame_menu_adm, placeholder_text="Escolha uma tabela.", textvariable= procurar_entry_str).place(x=250, y = 115)
            #   dados de entrada para pesquisar usuários ou CPF
            id_cpf_label= CTkLabel(master = frame_menu_adm, text= "CPF ou ID: ", font=("Roboto", 12)).place(x=255 ,y= 145)
            id_cpf_procurar_str = ctk.StringVar()
            id_cpf_procurar = CTkEntry(master = frame_menu_adm, placeholder_text="Procure pra mim: ", textvariable=id_cpf_procurar_str).place(x=250, y=170)
            
            dado1_label = CTkLabel(master = frame_menu_adm, text= "Email ou Categoria: ", font=("Roboto", 12)).place(x=405 ,y= 145)
            dado1_entry_str = ctk.StringVar()
            dado1_entry = CTkEntry(master = frame_menu_adm, textvariable=dado1_entry_str).place(x =400, y= 170)
            
            dado2_label = CTkLabel(master = frame_menu_adm, text= "Nome ou Sabor: ", font=("Roboto", 12)).place(x=255 ,y= 200)
            dado2_entry_str = ctk.StringVar()
            dado2_entry = CTkEntry(master = frame_menu_adm, textvariable=dado2_entry_str).place(x =250, y= 225)
            
            dado3_label = CTkLabel(master = frame_menu_adm, text= "Senha ou Preço: ", font=("Roboto", 12)).place(x=405 ,y= 200)
            dado3_entry_str = ctk.StringVar()
            dado3_entry = CTkEntry(master = frame_menu_adm, textvariable=dado3_entry_str).place(x =400, y= 225)
           
            dado4_label =CTkLabel(master = frame_menu_adm, text= "Auth ou Quantidade: ", font=("Roboto", 12)).place(x=255 ,y= 255)           
            dado4_entry_str = ctk.StringVar()
            dado4_entry = CTkEntry(master = frame_menu_adm, textvariable=dado4_entry_str).place(x =250, y= 280)
            
            check_var = ctk.StringVar(value="off")
            check_confirmation = CTkCheckBox(master = frame_menu_adm, text= "Concordo.", variable=check_var, onvalue="on", offvalue="off").place(x=400, y = 280)

            def alterar_dados():
                
                id_cpf = id_cpf_procurar_str.get()
                procurar = procurar_entry_str.get().upper()
                check_in = check_var.get()
                dado1 = dado1_entry_str.get()
                dado2 = dado2_entry_str.get()
                dado3 = dado3_entry_str.get()
                dado4 = dado4_entry_str.get()

                # alterar usuários
                def criptar_novasenha(alter_senha):
                    #verifica se a senha contém pelo menos 1 caracter de cada
                    letter = any(c.isalpha() for c in alter_senha)
                    number = any(c.isdigit() for c in alter_senha)
                    spchar = any(c in "!@#$%&*?" for c in alter_senha)
                    lenght = len(alter_senha) <= 18

                    return letter and number and spchar and lenght

                def cript_pass(alter_senha):

                    if criptar_novasenha(alter_senha):
                        hasher1 = hashlib.sha256()
                        hasher1.update(alter_senha.encode('utf-8'))
                        senha_hash = hasher1.digest()
                        vsenhacrip = binascii.hexlify(senha_hash)
                        return vsenhacrip

                def verificar_email(alter_email):
                    try:
                        # Valida o email usando a função validate_email
                        valid = validate_email(alter_email)
                        return True
                    except EmailNotValidError as e:
                        # Captura a exceção EmailNotValidError caso o email não seja válido
                        print(str(e))
                        return False

                def verificar_nome(alter_nome):
                    if all((c.isalpha() or c.isspace()) for c in alter_nome) and  len(alter_nome) > 0:
                        return True
                    else:
                        return False

                # alterar produtos
                def nova_categoria(alter_categoria):
                    if all((c.isalpha() or c.isspace()) for c in alter_categoria) and  len(alter_categoria) > 0:
                        return True
                    else:
                        return False
                
                def novo_sabor(alter_sabor):
                    if all((c.isalpha() or c.isspace()) for c in alter_sabor) and  len(alter_sabor) > 0:
                        return True
                    else:
                        return False
        
                if procurar == "USUÁRIOS" and verificar_email(dado1) and verificar_nome(dado2) and criptar_novasenha(dado3) and dado4 and check_in == "on":

                    vsenhacrip = cript_pass(dado3)
                    databaset.cursor.execute("UPDATE user SET EMAIL = ?, NOME = ?, SENHA = ?, AUTORIZAÇÃO = ? WHERE CPF = ?", (dado1, dado2, vsenhacrip, dado4, id_cpf,))
                    databaset.conn.commit()
                    span = messagebox.showinfo(title="Alteração Realizada!", message="Os dados foram, alterados com sucesso! Para atualizar a tabela, clique em 'PROCURAR'!")
                    print("Confirmado")

                    # consulta_usuario_tree = ttk.Treeview(frame_menu_adm)
                    # consulta_usuario_tree['columns'] = ("CPF", "EMAIL", "NOME", "SENHA", "AUTH")

                    # consulta_usuario_tree.column("CPF", width=50, anchor=CENTER)
                    # consulta_usuario_tree.heading("CPF", text="CPF")

                    # consulta_usuario_tree.column("EMAIL", width=70, anchor=W)
                    # consulta_usuario_tree.heading("EMAIL", text="EMAIL")

                    # consulta_usuario_tree.column("NOME", width=100, anchor=W)
                    # consulta_usuario_tree.heading("NOME", text="NOME")

                    # consulta_usuario_tree.column("SENHA", width=70, anchor=CENTER)
                    # consulta_usuario_tree.heading("SENHA", text="SENHA")

                    # consulta_usuario_tree.column("AUTH", width=100, anchor=CENTER)
                    # consulta_usuario_tree.heading("AUTH", text="AUTH")

                    # databaset.cursor.execute("SELECT * FROM user")
                    # users = databaset.cursor.fetchall()

                    # consulta_usuario_tree.place(x=20, y=20, width = 200, height = 300)

                    # for user in users:
                    #     consulta_usuario_tree.insert("", "end", values=(user[0], user[1], user[2], user[3], user[4]))
                
                elif procurar == "PRODUTOS" and nova_categoria(dado1) and novo_sabor(dado2) and dado3 and dado4 and check_in == "on":
                
                    databaset.cursor.execute("UPDATE products SET PRODUTO = ?, SABOR = ?, PRECO = ?, QUANTIDADE = ? WHERE ID = ?", (dado1, dado2, dado3, dado4, id_cpf,))
                    databaset.conn.commit()
                    span = messagebox.showinfo(title="Alteração Realizada!", message="Os dados foram, alterados com sucesso! Para atualizar a tabela clique em 'PROCURAR!'")
                    print("Confirmado")

                    #  # tabelas do banco de dados
                    # consulta_produto_tree = ttk.Treeview(frame_menu_adm)
                    # consulta_produto_tree['columns'] = ("ID", "CATEGORIA", "SABOR", "PREÇO", "QUANTIDADE")

                    # consulta_produto_tree.column("ID", width=50, anchor=CENTER)
                    # consulta_produto_tree.heading("ID", text="ID")

                    # consulta_produto_tree.column("CATEGORIA", width=70, anchor=W)
                    # consulta_produto_tree.heading("CATEGORIA", text="CATEGORIA")

                    # consulta_produto_tree.column("SABOR", width=100, anchor=W)
                    # consulta_produto_tree.heading("SABOR", text="SABOR")

                    # consulta_produto_tree.column("PREÇO", width=70, anchor=CENTER)
                    # consulta_produto_tree.heading("PREÇO", text="PREÇO")

                    # consulta_produto_tree.column("QUANTIDADE", width=100, anchor=CENTER)
                    # consulta_produto_tree.heading("QUANTIDADE", text="QUANTIDADE")

                    # databaset.cursor.execute("SELECT * FROM products")
                    # produtos = databaset.cursor.fetchall()

                    # consulta_produto_tree.place(x=20, y=20, width = 200, height = 300)

                    # for produto in produtos:
                    #     consulta_produto_tree.insert("", "end", values=(produto[0], produto[1], produto[2], produto[3], produto[4]))
                
                elif check_in == "off":
                    span = messagebox.showinfo(title="Erro!", message="Preencha o checkbox !")
                        
                else:
                    span = messagebox.showinfo(title="Erro!", message="Verifique se as informações estão preenchidas de acordo com os padrões estabelecidos!")
        
            alter_button = CTkButton(master = frame_menu_adm, text="Alterar",text_color="white", font=("Roboto", 12,"bold"), width= 100, command = alterar_dados)
            alter_button.pack(padx = 20, pady = 20)
            alter_button.place(x= 250, y= 325)
            
            def excluir_dados():
                id_cpf = id_cpf_procurar_str.get()
                procurar = procurar_entry_str.get().upper()
                check_in = check_var.get()
               
                confimation = span = messagebox.askyesno(title="CONFIRMAR!", message="Podemos concluir esta operação? Após confirmação, atualize a tabela clicando em 'PROCURAR'! ")
                if confimation:
                    if procurar =="USUÁRIOS" and check_in == "on":
                        span = messagebox.showinfo(tilte="AÇÃO CONCLUÍDA!", message="Usuário apagado do nosso sistema! Atualize a tabela clicando em 'PROCURAR'.")
                        databaset.cursor.execute("DELETE FROM user WHERE CPF =?", (id_cpf,))
                        databaset.conn.commit()
                        print("Confirmado")

                    elif procurar == "PRODUTOS" and check_in == "on":
                        span = messagebox.showinfo(title="AÇÃO CONCLUÍDA!", message="Produto apagado do nosso sistema! Atualize a tabela clicando em 'PROCURAR'.")
                        databaset.cursor.execute("DELETE FROM products WHERE ID =?", (id_cpf,))
                        databaset.conn.commit()
                        print("Confirmado")
                    
                    elif check_in == "off":
                        span = messagebox.showerror(title="ERRO!", message="Preencha o checkbox !")
                
                    else: 
                        span = messagebox.showerror(title="ERRO!", message="Verifique se as informações estão preenchidas de acordo com os padrões estabelecidos!")

                else:
                    span = messagebox.showinfo(title="CANCELANDO OPERAÇÃO!", message="OPERAÇÃO FOI CANCELADA !")
            
            remove_button = CTkButton(master = frame_menu_adm, text="Excluir",text_color="white", font=("Roboto", 12, "bold"), width= 100, fg_color="red", command=excluir_dados)
            remove_button.pack(padx = 20, pady = 20)
            remove_button.place(x= 355, y= 325)

            def cadastrar_dados():

                def  verificar_cpf(vcpf):
                    if vcpf.isdigit() and len(vcpf) == 11:
                        return True
                    else:
                        return False
            # Verifica se o email é válido
                def verificar_email(vemail):
                    try:
                        #Valida o email usando a função validate_email
                        valid = validate_email(vemail)
                        return True
                    except EmailNotValidError as e:
                        #Captura a exceção EmailNotValidError caso o email não seja válido
                        print(str(e))
                        return False
            # Verificar se o nome contém apenas letras
                def verificar_nome(vnome):
                    if all((c.isalpha() or c.isspace()) for c in vnome) and  len(vnome) > 0:
                        return True
                    else:
                        return False
            # Verificar senha e criptografa
                def verificar_senha(vsenha):
                    #verifica se a senha contém pelo menos 1 caracter de cada
                    letter = any(c.isalpha() for c in vsenha)
                    number = any(c.isdigit() for c in vsenha)
                    spchar = any(c in "!@#$%&*?" for c in vsenha)
                    lenght = len(vsenha) <= 18

                    return letter and number and spchar and lenght
            # Criptografar senha    
                def cript_pass(vsenha):

                    if verificar_senha(vsenha):
                        hasher = hashlib.sha256()
                        hasher.update(vsenha.encode('utf-8'))
                        senha_hash = hasher.digest()
                        vsenhacrip = binascii.hexlify(senha_hash)
                        return vsenhacrip
                
                def gerador_de_id():

                    counter = 1
                    generated_ids = set()
                    
                    formatted_ID = f"{counter:04d}"
                    counter += 1

                    while formatted_ID in generated_ids:
                        formatted_ID = f"{counter:04d}"
                        counter += 1

                        generated_ids.add(formatted_ID)
                        return int(formatted_ID)
            # Verifica se o categoria contém apenas letras
                def verificar_produto(vprod):
                    if all((c.isalpha() or c.isspace()) for c in vprod) and  len(vprod) > 0:
                        return vprod
                    else:
                        return False
            # Verificar se o sabor contém apenas letras
                def verificar_sabor(vsabor):
                    if all((c.isalpha() or c.isspace()) for c in vsabor) and  len(vsabor) > 0:
                        return vsabor
                    else:
                        return None
            # Verificar se o preço contém apenas números
                def verificar_preco(vpreco):
                    try:
                        preco = float(vpreco)
                        return preco
                    except ValueError:
                        return None
            # Verificar se a quantidade contém apenas números         
                def verificar_quantidade(vqtd):
                    try:
                        qtd = int(vqtd)
                        return qtd
                    except ValueError:
                        return None
                
                procurar = procurar_entry_str.get().upper()
                check_in = check_var.get()
                id_cpf = id_cpf_procurar_str.get()
                dado1 = dado1_entry_str.get()
                dado2 = dado2_entry_str.get()
                dado3 = dado3_entry_str.get()
                dado4 = dado4_entry_str.get()
                
                if procurar == "USUÁRIOS" and check_in == "on":
                    if verificar_cpf(id_cpf) and verificar_email(dado1) and verificar_nome(dado2) and verificar_senha(dado3) and dado4:
                        vsenhacrip = cript_pass(dado3)
                        databaset.cursor.execute("INSERT INTO user VALUES (?, ?, ?, ?, ?)",(id_cpf, dado1, dado2, vsenhacrip, dado4 ))
                        databaset.conn.commit()
                        span = messagebox.showinfo(title="AÇÃO CONCLUÍDA!", message="Usuário cadastrado no nosso sistema! Atualize a tabela clicando em 'PROCURAR'.")

                    else:
                        span = messagebox.showerror(title="ERRO!",message= "Algo inesperado ocorreu, verifique as informações e tente novamente!\nA senha deve conter números, letras e caracteres especiais '!@#$'\nCPF deve conter apenas números e 11 digitos apenas\nNome deve conter apenas letras\nEmail precisa ser válido, exemplo@kmail.com")

                elif procurar == "PRODUTOS" and check_in =="on":    
                    if verificar_produto(dado1) and verificar_sabor(dado2) and verificar_preco(dado3) and verificar_quantidade(dado4):
                        id = gerador_de_id()
                        databaset.cursor.execute("INSERT INTO products VALUES (?, ?, ?, ?, ?)",(id, dado1, dado2, dado3, dado4 ))
                        databaset.conn.commit()
                        span = messagebox.showinfo(title="AÇÃO CONCLUÍDA!", message="Produto cadastrado no nosso sistema! Atualize a tabela clicando em 'PROCURAR'.")

                    else:
                        span = messagebox.showerror(title="ERRO!",message= "Algo inesperado ocorreu, verifique as informações e tente novamente!")

                elif check_in == "off":
                    span = messagebox.showerror(title="ERRO!", message="Preencha o checkbox !")

            cadastre_button = CTkButton(master = frame_menu_adm, text="Cadastrar",text_color="white", font=("Roboto", 12,"bold"), width= 100, fg_color="green", command= cadastrar_dados)
            cadastre_button.pack(padx = 20, pady = 20)
            cadastre_button.place(x= 460, y= 325)

        # login realizado
        login_button = CTkButton(master = frame_home, text= "Entrar", width=300, command = user_log, font = ("Roboto", 12, "bold"), text_color= "white")
        login_button.pack(padx = 20, pady = 20)
        login_button.place(x= ((650 - 150)/2), y = 250)

        def tela_cadastro():
            # remover frame de login
            frame_home.pack_forget()

            # tela de cadastro de usuários
            frame_cad = CTkFrame(master = home, width = 650, height = 370)
            frame_cad.pack(pady= 20, padx = 20)

            cad_label = CTkLabel(master = frame_cad, text = "Faça seu cadastro", font= ("Roboto", 20)).place(x= ((650-150)/2), y=20)
            campos_label = CTkLabel(master = frame_cad, text = "*todos os campos são obrigátorios.", text_color = "red", font = ("Roboto", 12)).place(x= ((650-150)/2), y= 50)

            cpf_str = ctk.StringVar()
            cad_cpf = CTkEntry(master = frame_cad, placeholder_text="CPF", width = 300, textvariable = cpf_str).place(x= 290, y=80)
            cad_cpf_label = CTkLabel(master = frame_cad, text="CPF", font = ("Roboto", 12), text_color= "black").place(x= 250,y = 80)

            email_str = ctk.StringVar()
            cad_email = CTkEntry(master = frame_cad, placeholder_text="E-mail", width = 300, textvariable=email_str).place(x= 290, y=160)
            cad_email_label = CTkLabel(master = frame_cad, text="Email", font = ("Roboto", 12), text_color="black").place(x= 250,y = 160)

            nome_str = ctk.StringVar()
            cad_nome = CTkEntry(master = frame_cad, placeholder_text="Nome completo", width = 300, textvariable=nome_str).place(x= 290, y=120)
            cad_nome_label = CTkLabel(master = frame_cad, text="Nome", font = ("Roboto", 12), text_color="black").place(x= 250,y = 120)

            senha_str = ctk.StringVar()
            cad_senha = CTkEntry(master = frame_cad, placeholder_text="Senha", width = 300, show = "*", textvariable=senha_str).place(x= 290, y=200)
            cad_senha_label = CTkLabel(master = frame_cad, text="Senha", font = ("Roboto", 12), text_color="black").place(x= 250,y = 200)

            senha_conf_str = ctk.StringVar()
            cad_senha_confirma = CTkEntry(master = frame_cad, placeholder_text="Repita sua senha", width = 300, show= "*", textvariable=senha_conf_str).place(x= 290, y=240)
            cad_senha1_label = CTkLabel(master = frame_cad, text="Senha", font = ("Roboto", 12), text_color="black").place(x= 250,y = 240)

            aceitar = ctk.StringVar(value = "off")
            cad_check = CTkCheckBox(master = frame_cad, text= "Aceito vender minha alma", variable=aceitar, onvalue="on", offvalue="off").place(x= ((650 - 150)/2), y = 280)

            # Realizar cadastro
            def cadastrar_realizado():
                check_in = aceitar.get()
                # global vname
                # global vcpf
                #verifica se o CPF é válido
                def  verificar_cpf(vcpf):
                    if vcpf.isdigit() and len(vcpf) == 11:
                        return True
                    else:
                        return False

            #verifica se o email é válido
                def verificar_email(vemail):
                    try:
                        #Valida o email usando a função validate_email
                        valid = validate_email(vemail)
                        return True
                    except EmailNotValidError as e:
                        #Captura a exceção EmailNotValidError caso o email não seja válido
                        print(str(e))
                        return False

            #verificar se o nome contém apenas letras
                def verificar_nome(vnome):
                    if all((c.isalpha() or c.isspace()) for c in vnome) and  len(vnome) > 0:
                        return True
                    else:
                        return False

            #verificar senha e criptografa
                def verificar_senha(vsenha):
                    #verifica se a senha contém pelo menos 1 caracter de cada
                    letter = any(c.isalpha() for c in vsenha)
                    number = any(c.isdigit() for c in vsenha)
                    spchar = any(c in "!@#$%&*?" for c in vsenha)
                    lenght = len(vsenha) <= 18

                    return letter and number and spchar and lenght

                def cript_pass(vsenha):

                    if verificar_senha(vsenha):
                        hasher = hashlib.sha256()
                        hasher.update(vsenha.encode('utf-8'))
                        senha_hash = hasher.digest()
                        vsenhacrip = binascii.hexlify(senha_hash)
                        return vsenhacrip

                while True:
                    vcpf = cpf_str.get()
                    if verificar_cpf(vcpf):
                        print("CPF Válido")
                        break
                    else:
                        span = messagebox.showinfo(title="CPF Inválido.", message= "CPF deve conter apenas números e no máximo 11 digitos!")
                        print("CPF Inválido")
                        break

                while True:
                    vemail = email_str.get()
                    if verificar_email(vemail):
                        print("Email válido")
                        break
                    else:
                        span = messagebox.showinfo(title="Email Inválido.", message= "Email inválido! Faça como o exemplo: pedro@kmail.com")
                        print("Email Inválido")
                        break


                while True:
                    vname = nome_str.get()
                    if verificar_nome(vname):
                        print("Nome válido")
                        break
                    else:
                        span = messagebox.showinfo(title="Nome Inválido.", message= "Nome deve conter apenas letras e no mínimo 3 caracteres!")
                        print("Nome Inválido")
                        break

                while True:
                    authentication = 2
                    vsenha = senha_str.get()
                    vsenha_confirma = senha_conf_str.get()
                    if vsenha == vsenha_confirma and verificar_senha(vsenha) and check_in == "on":
                        vsenhacrip = cript_pass(vsenha)
                        print("Senha criptografada")
                        span = messagebox.showinfo(title="Cadastro Realizado", message= "Parabéns usuário cadastrado com sucesso!")
                        databaset.cursor.execute("INSERT INTO user VALUES (?, ?, ?, ?, ?)", (vcpf, vemail, vname, vsenhacrip, authentication ))
                        databaset.conn.commit()
                        break

                    else:
                        span = messagebox.showinfo(title="Cadastro não realizado", message= "Verifique se todos os campos estão preenchidos corretamente!")
                        break

            cad_button_confirma = CTkButton(master = frame_cad, text = "Confirmar", width = 220, fg_color="green", command = cadastrar_realizado,font = ("Roboto", 12, "bold"), text_color= "white")
            cad_button_confirma.pack(padx = 10, pady = 10)
            cad_button_confirma.place(x= ((650 - 150)/2), y = 320)

            # Voltar para pagina de home
            def voltar():
                # remover frame de cadastro
                frame_cad.pack_forget()

                # tela de home
                frame_home.pack(pady= 20, padx = 20)

            voltar_button = CTkButton(master = frame_cad, text = "Voltar", width = 110, command= voltar,font = ("Roboto", 12, "bold"), text_color= "white")
            voltar_button.pack(padx = 10, pady = 10)
            voltar_button.place(x= 480, y = 320)

        cadastro_span = CTkLabel(master = frame_home, text = "Sou novo aqui, quero me")
        cadastro_span.place(x= ((650 - 150)/2), y = 300)
        cadastro_button = CTkButton(master = frame_home, text= "Cadastrar",  width = 150, fg_color="green", hover_color="#2d9334", command = tela_cadastro, font = ("Roboto", 12, "bold"), text_color= "white")
        cadastro_button.pack(padx = 20, pady = 20)
        cadastro_button.place(x= 400, y = 300)



Sistema()