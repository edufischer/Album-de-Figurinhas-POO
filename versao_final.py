import csv
import random
import os


class Figurinha:
    def __init__(self, id, nome, conteudo):
        self.id = id
        self.nome = nome
        self.conteudo = conteudo
        self.status = 0  # 0 - na coleção, 1 - colada no álbum, 2 - disponível para troca

class Troca:
    def __init__(self, proponente, destinatario, requerida, disponivel, status=0):
        self.proponente = proponente
        self.destinatario = destinatario
        self.requerida = requerida
        self.disponivel = disponivel
        # Status da troca pode ser 0 (aguardando análise), 1 (aceita), 2 (recusada) ou 3 (finalizada).
        self.status = status

class Usuario:
    def __init__(self, nome, senha):
        self.nome = nome
        self.senha = senha
        self.colecao = []
        self.album = []
        self.figurinhas_para_troca = []

    def adicionar_figurinha_a_colecao(self, figurinha):
        self.colecao.append(figurinha)

    def adicionar_figurinha_ao_album(self, figurinha):
        self.album.append(figurinha)

    def disponibilizar_figurinha_para_troca(self, figurinha):
        figurinha.status = 2
        self.figurinhas_para_troca.append(figurinha)
        self.colecao.remove(figurinha)

    # Pega a figurinha na lista de figurinhas na coleção por meio do id passado por parâmetro
    def verificar_figurinha_na_colecao(self, id):
        for figurinha in self.colecao:
            if figurinha.id == int(id):
                return figurinha
        return None

    # Pega a figurinha na lista de figurinhas no album por meio do id passado por parâmetro
    def verificar_figurinha_no_album(self, id):
        for figurinha in self.album:
            if figurinha.id == int(id):
                return figurinha
        return None

    # Pega a figurinha na lista de figurinhas para troca por meio do id passado por parâmetro
    def get_figurinha_by_id(self, id):
        for figurinha in self.figurinhas_para_troca:
            if figurinha.id == int(id):
                return figurinha
        return None

    def propor_troca(self, usuarios, trocas, figurinha_do_solicitante, figurinha_do_destinatario):
        contador = 0
        usuario_destinatario = None

        # Procurar figurinha do solicitante na coleção
        for figurinha in self.figurinhas_para_troca:
            if figurinha.id == figurinha_do_solicitante:
                figurinha_do_solicitante = figurinha
                contador = contador + 1
                break

        # Procurar figurinha do destinatário na coleção
        for usuario in usuarios:
            for figurinha in usuario.figurinhas_para_troca:
                if figurinha.id == figurinha_do_destinatario:
                    usuario_destinatario = usuario
                    figurinha_do_destinatario = figurinha
                    contador = contador + 1
                    break

        # Verificar se as figurinhas estão disponíveis para troca
        if contador == 0:
            print('\nAs figurinhas não estão disponíveis para troca.')
            return

        # Confirmar a troca e add troca na lista de trocas
        aceitar = input(
            f'\nDeseja propor uma troca para o usuário {usuario_destinatario.nome}? (S/N): ').strip().lower()
        if aceitar == 's':
            figurinha_do_solicitante.status = 2
            # self.figurinhas_para_troca.remove(figurinha_do_solicitante)
            solicitante = self.nome
            destinatario = usuario_destinatario.nome
            solicitacao = Troca(proponente=solicitante, destinatario=destinatario,
                                requerida=figurinha_do_destinatario.id, disponivel=figurinha_do_solicitante.id)
            trocas = trocas.append(solicitacao)
            print('\nSolicitação de troca concluída com sucesso!')
            print('\nAguarde o aceite do outro usuário!')
            return trocas

    def revisar_solicitacoes_de_troca(self, trocas, figurinhas):
        print('Suas solicitações de troca:')

        for troca in trocas:
            if troca.destinatario == self.nome and troca.status == 0:
                print(f'\nO usuário {troca.proponente.upper()} gerou esta solicitação de troca abaixo:\n'
                      f'\nSua figurinha de número {troca.requerida}.\n'
                      f'\nEm troca da figurinha de número {troca.disponivel}.')

                escolha = int(input(
                    '\nO que deseja fazer com esta solicitação acima? Aceitar(1), Recusar(2) ou 0 para sair: '))

                if escolha == 0:
                    return
                elif escolha == 1:
                    for figurinha in figurinhas:
                        if figurinha.id == int(troca.disponivel):
                            self.colecao.append(figurinha)
                            figurinha_requerida = self.get_figurinha_by_id(
                                troca.requerida)
                            self.figurinhas_para_troca.remove(
                                figurinha_requerida)
                            troca.status = 1
                    print('\nTroca concluída com sucesso!')
                    return
                elif escolha == 2:
                    troca.status = 2
                    print('\nTroca recusada!')
                    return
            else:
                print('\nNenhuma solicitação de troca pendente para você.')
            return


class AlbumDeFigurinhas:
    def __init__(self):
        self.usuarios = []
        self.figurinhas = []
        self.trocas = []

    def carregar_dados(self):
        with open('figurinhas.csv', 'r') as arquivo:
            reader = csv.reader(arquivo)
            next(reader)  # Ignora o cabeçalho
            for row in reader:
                id, nome, conteudo = row
                figurinha = Figurinha(int(id), nome, conteudo)
                self.figurinhas.append(figurinha)

        with open('trocas.csv', 'r') as arquivo:
            reader = csv.reader(arquivo)
            next(reader)
            for row in reader:
                if len(row) == 5:
                    proponente, destinatario, requerida, disponivel, status = row
                    status = int(status)
                    troca = Troca(proponente, destinatario,
                                  requerida, disponivel, status)
                    self.trocas.append(troca)

        with open('usuarios.csv', 'r') as arquivo:
            reader = csv.reader(arquivo)
            next(reader)
            for row in reader:
                # Só lê o arquivo caso tenha infos suficientes escritas
                if len(row) == 5:
                    nome, senha, colecao, album, troca = row
                    usuario = Usuario(nome, senha)
                    if colecao != '':
                        # Map() -> aplica a funcao int() para cada item da lista
                        # split(',') -> transforma a String para uma lista. O delimitador é a vírgula
                        colecao = list(map(int, colecao.split(',')))
                    if album != '':
                        album = list(map(int, album.split(',')))
                    if troca != '':
                        troca = list(map(int, troca.split(',')))
                    # Atribui ao usuário a lista de figurinhas com os IDs especificados na lista colecao
                    usuario.colecao = [
                        self.get_figurinha_by_id(id) for id in colecao]
                    usuario.album = [
                        self.get_figurinha_by_id(id) for id in album]
                    usuario.figurinhas_para_troca = [
                        self.get_figurinha_by_id(id) for id in troca]
                    self.usuarios.append(usuario)

    def get_figurinha_by_id(self, id):
        for figurinha in self.figurinhas:
            if figurinha.id == id:
                return figurinha
        return None

    def criar_usuario(self, nome, senha):
        novo_usuario = Usuario(nome, senha)
        self.usuarios.append(novo_usuario)
        return novo_usuario

    # Efetua o loading de pendencias de trocas já aceitas pelo outro usuário automática
    def verificar_pendencias(self, usuarios, nome, senha):
        for usuario in usuarios:
            if usuario.nome == nome and senha == senha:
                for troca in self.trocas:
                    if troca and troca.status == 1:
                        print(
                            '\nO seu pedido de troca foi aprovado. Efetuando a inclusao da figurinha nova em sua coleção...')

                        for figurinha in self.figurinhas:
                            if figurinha.id == int(troca.requerida):
                                usuario.colecao.append(figurinha)
                                figurinha_disponivel = usuario.get_figurinha_by_id(
                                    troca.disponivel)
                                usuario.figurinhas_para_troca.remove(
                                    figurinha_disponivel)
                                troca.status = 3

    def acessar_album(self, nome_usuario, senha):
        for usuario in self.usuarios:

            mensagem_erro = None
            
            if usuario.nome == nome_usuario and usuario.senha == senha:

                
                while True:
                    os.system('cls' if os.name == 'nt' else 'clear')

                    album.salvar_dados()
                    print(f'\n=== BEM VINDO {usuario.nome.upper()} ===')

                    if mensagem_erro: 
                        print(mensagem_erro)
                        mensagem_erro = None

                    opcao = input(
                        '\nOpções:\n\n1 - Ver Álbum\n2 - Gerenciar a coleção\n3 - Abrir pacote de Figurinhas\n4 - Voltar ao menu Anterior\n\nEscolha uma opção: ')
                    

                    if opcao == '1':
                        self.ver_album(usuario)
                        album.salvar_dados()
                    elif opcao == '2':
                        self.gerenciar_colecao(usuario)
                        album.salvar_dados()
                    elif opcao == '3':
                        self.abrir_pacote(usuario)
                        album.salvar_dados()
                    elif opcao == '4':
                        return
                    else:
                        mensagem_erro = '\nOpção inválida. Tente novamente.\n'

    def ver_album(self, usuario):
        print('=== Álbum ===')
        # Determinei 10 figurinhas por página no album como default
        figurinhas_por_pagina = 10

        # Slicing em paginas
        # Lista paginas contem sublistas de paginas que contem 10 figurinhas cada
        paginas = [self.figurinhas[numero_da_pagina : (numero_da_pagina + figurinhas_por_pagina)]
                   # for intera pelo range (start, comprimento, incremento)
                   for numero_da_pagina in range(0, len(self.figurinhas), figurinhas_por_pagina)]

        pagina_atual = 0
        mensagem_erro = None

        while True:
            os.system('cls' if os.name == 'nt' else 'clear')

            if pagina_atual < 0:
                pagina_atual = 0
            if pagina_atual >= len(paginas):
                pagina_atual = len(paginas) - 1

            pagina = paginas[pagina_atual]

            print(
                f'\n=== ÁLBUM DE {usuario.nome.upper()} - PÁGINA {pagina_atual + 1} ===')

            for figurinha in pagina:
                numero = figurinha.id
                tem_figurinha_colecao = usuario.verificar_figurinha_na_colecao(
                    numero)
                tem_figurinha_album = usuario.verificar_figurinha_no_album(
                    numero)

                if tem_figurinha_album:
                    print(
                        f'{tem_figurinha_album.id}: {figurinha.nome} - {figurinha.conteudo}')

                elif tem_figurinha_colecao:
                    print(f'{tem_figurinha_colecao.id}: DISPONÍVEL PARA COLAR')
                else:
                    print(f'{figurinha.id}: X')

            if mensagem_erro: 
                print(mensagem_erro)
                mensagem_erro = None

            print('\nOpções:')
            print('1. Avançar Página')
            print('2. Recuar Página')
            print('3. Voltar ao Menu Anterior')
            opcao = input('\nEscolha uma opção: ')

            if opcao == '1':
                pagina_atual += 1
            elif opcao == '2':
                pagina_atual -= 1
            elif opcao == '3':
                break
            else:
                mensagem_erro = ('\nOpção inválida. Tente novamente.')


    def gerenciar_colecao(self, usuario):
        print('\n=== Coleção ===')
            
        mensagem_erro = None

        while True:

            print('\n###################################################################') 
            print('\nFigurinhas que estão na coleção (disponíveis para colar): \n')

            if not usuario.colecao: print('Você não tem figurinha na coleção ainda.\n')
            else: 
                for figurinha in usuario.colecao: 
                    print(f'Figurinha {figurinha.id}: {figurinha.nome}, {figurinha.conteudo}.')
            print('\n###################################################################\n') 

            print('\nFigurinhas que estão disponíveis para troca:\n')
            if not usuario.figurinhas_para_troca: print('Nenhuma figurinha foi adicionada para troca ainda por você.\n')
            else:
                for figurinha in usuario.figurinhas_para_troca:
                    print(f'Figurinha {figurinha.id}: {figurinha.nome}, {figurinha.conteudo}.')
            print('\n###################################################################\n') 
                

            if mensagem_erro: 
                print(mensagem_erro)
                mensagem_erro = None

            opcao = input(
                'Opções:\n1 - Colar Figurinha\n2 - Disponibilizar para Troca\n3 - Propor Troca\n4 - Revisar Solicitações de Troca\n5 - Voltar ao menu Anterior\nEscolha uma opção: ')
            
            if opcao == '1':
                numero_figurinha = int(
                    input('\nDigite o número da figurinha que deseja colar: '))
                figurinha = self.get_figurinha_by_id(numero_figurinha)
                if figurinha and figurinha.status == 0:
                    usuario.adicionar_figurinha_ao_album(figurinha)
                    usuario.colecao.remove(figurinha)
                    figurinha.status = 1
                    print('\nFigurinha colada com sucesso!')
                else:
                    print('\nFigurinha não encontrada na coleção ou já colada no álbum.')
                album.salvar_dados()
            elif opcao == '2':
                numero_figurinha = int(
                    input('\nDigite o número da figurinha que deseja disponibilizar para troca: '))
                figurinha = self.get_figurinha_by_id(numero_figurinha)
                if figurinha and figurinha.status == 0:
                    usuario.disponibilizar_figurinha_para_troca(figurinha)
                    print('\nFigurinha disponibilizada para troca com sucesso!')
                else:
                    print(
                        '\nFigurinha não encontrada na coleção ou já disponibilizada para troca.')
                album.salvar_dados()

            elif opcao == '3':
                figurinha_do_solicitante = int(
                    input('\nDigite o número da sua figurinha que deseja trocar: '))
                figurinha_do_destinatario = int(
                    input('\nDigite o número da figurinha que deseja obter: '))
                solicitacao = usuario.propor_troca(
                    self.usuarios, self.trocas, figurinha_do_solicitante, figurinha_do_destinatario)
                self.trocas.append(solicitacao)
                album.salvar_dados()

            elif opcao == '4':
                usuario.revisar_solicitacoes_de_troca(
                    self.trocas, self.figurinhas)
                album.salvar_dados()

            elif opcao == '5':
                album.salvar_dados()
                return
            else:
                mensagem_erro = ('\nOpção inválida. Tente novamente.')

    def abrir_pacote(self, usuario):
        pacote = []
        for _ in range(3):
            figurinha = random.choice(self.figurinhas)
            figurinha.status = 0  # Figurinha disponível para colar
            usuario.adicionar_figurinha_a_colecao(figurinha)
            pacote.append(figurinha)

        print('\nVocê abriu um pacote de figurinhas e ganhou as seguintes figurinhas:\n')
        for figurinha in pacote:
            print(f' {figurinha.id} - {figurinha.nome}')

        input('\nPressione Enter para continuar...')
        album.salvar_dados()

    def salvar_dados(self):
        with open('figurinhas.csv', 'w', newline='') as arquivo:
            writer = csv.writer(arquivo)
            writer.writerow(['ID', 'Nome do Jogador', 'Conteudo', 'Status'])
            for figurinha in self.figurinhas:
                writer.writerow(
                    [figurinha.id, figurinha.nome, figurinha.conteudo])

        with open('trocas.csv', 'w', newline='') as arquivo:
            writer = csv.writer(arquivo)
            writer.writerow(['Proponente', 'Destinatario',
                            'Requerida', 'Disponivel', 'Status'])

            for troca in self.trocas:
                if troca:
                    writer.writerow([troca.proponente, troca.destinatario,
                                    troca.requerida, troca.disponivel, troca.status])

        with open('usuarios.csv', 'w', newline='') as arquivo:
            writer = csv.writer(arquivo)
            writer.writerow(['Nome', 'Senha', 'Colecao', 'Album', 'Troca'])
            for usuario in self.usuarios:
                colecao = ",".join(
                    map(str, [figurinha.id for figurinha in usuario.colecao]))
                album = ",".join(
                    map(str, [figurinha.id for figurinha in usuario.album]))
                troca = ",".join(
                    map(str, [figurinha.id for figurinha in usuario.figurinhas_para_troca]))
                writer.writerow(
                    [usuario.nome, usuario.senha, colecao, album, troca])


if __name__ == '__main__':
    album = AlbumDeFigurinhas()
    album.carregar_dados()

    mensagem_erro = None

    while True:

        os.system('cls' if os.name == 'nt' else 'clear')

        print('\n=== Tela Inicial ===\n')
        if mensagem_erro: 
            print(mensagem_erro)
            mensagem_erro = None

        opcao = input(
            '\nOpções:\n\n1 - Novo Álbum\n2 - Acessar Álbum\n3 - Sair do Aplicativo\n\nEscolha uma opção: ')
    

        if opcao == '1':
            nome = input('\nDigite seu nome de usuário: ')
            senha = input('\nDigite sua senha: ')
            album.criar_usuario(nome, senha)

        elif opcao == '2':
            nome = input('\nDigite seu nome de usuário: ')
            senha = input('\nDigite sua senha: ')
            usuarios = album.usuarios
            album.verificar_pendencias(usuarios, nome, senha)
            album.acessar_album(nome, senha)

        elif opcao == '3':
            album.salvar_dados()
            break

        else:
            mensagem_erro = '\nOpção inválida. Tente novamente.' 
        

