#----------------------------------------NAVEGAÇÃO-------------------------------------------------#
def leiaInt():
    while True:
        try:
            n = int(input("Digite um número: "))
        except (ValueError, TypeError):
            print("[0;31mERRO! Digite um número inteiro válido.[m")
            continue
        except (KeyboardInterrupt):
            print("\n[0;31mUsuário preferiu não digitar.[m")
            return 0
        else:
            return n

def linha(tam=42):
    return "-" * tam

def cabeçalho(txt):
    print(linha())
    print(txt.center(42))
    print(linha())

def menu(lista):
    cabeçalho("MENU PRINCIPAL")
    c = 1
    for item in lista:
        print(f"{c} - {item}")
        c += 1
    print(linha())
    opcao = int(input("Digite a opção desejada: "))
    return opcao

def menu_usuario(lista):
    cabeçalho("MENU USUÁRIO")
    c = 1
    for item in lista:
        print(f"{c} - {item}")
        c += 1
    print(linha())
    opcao = int(input("Digite a opção desejada: "))
    return opcao

def menu_adm(lista):
    cabeçalho("MENU ADMINISTRADOR")
    c = 1
    for item in lista:
        print(f"{c} - {item}")
        c += 1
    print(linha())
    opcao = int(input("Digite a opção desejada: "))
    return opcao