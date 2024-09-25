from abc import ABC, abstractclassmethod, abstractproperty
from datetime  import datetime

class Conta:

    def __init__(self, numero, cliente):
        self._saldo = 0
        self._numero = numero
        self._agencia = "00001"
        self._cliente = cliente
        self._historico = Historico()

    @classmethod
    def nova_conta(cls, cliente, numero):
        return cls(cliente, numero)
    @property
    def saldo(self):
        return self._saldo
    @property
    def numero(self):
        return self._numero
    @property
    def agencia(self):
        return self._agencia
    @property
    def cliente(self):
        return self._cliente
    @property
    def historico(self):
        return self._historico

    def sacar(self, valor):
        saldo = self._saldo
        saldo_excedido = valor > saldo
        
        if saldo_excedido:
            print("\nVocê não tem saldo suficiente.")
        elif valor > 0:
            self._saldo -= valor
            print("\n>>>\t\t\tSaque realizado com sucesso!\t\t\t<<<")
        else:
            print("\nValor informado inválido.")
        
        return False
    def depositar(self, valor):
        if valor > 0:
            self._saldo += valor
            print("\n>>>\t\t\tDepósito realizado com sucesso!\t\t\t<<<")
        else:
            print("\nvalor informado inválido.")
            return False
        return True

    
class Historico:
    def __init__(self):
        self._transacoes = []

    @property
    def transacoes(self):
        return self._transacoes
    def adicionar_transacao(self, transacao):
        self._transacoes.append({
            "Tipo": transacao.__class__.__name__,
            "Valor": transacao.valor,
            "Data": datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        })

class ContaCorrente(Conta):
    def __init__(self, cliente, numero, limite=500, limite_saques=3):
        super().__init__(numero, cliente)
        self._limite = limite
        self._limite_saques = limite_saques

    def sacar(self, valor):
        numero_saques = len([transacao for transacao in self.historico.transacoes if transacao["Tipo"] == Saque.__name__])
        
        limite_excedido = valor > self._limite
        saques_excedido = numero_saques >= self._limite_saques

        if limite_excedido:
            print("\nVocê não tem saldo suficiente.")
        elif saques_excedido:
            print("\nNúmero máximo de saques atingido.")
        else:
            return super().sacar(valor)
        return False

    def __str__(self):
        return f"""
            Agência:\t\t\t\t{self.agencia}        
            Conta:\t\t\t\t{self.numero}        
            Titular:\t\t\t\t{self.cliente.nome} 
        """


class Cliente:
    def __init__(self, endereco):
        self.endereco = endereco
        self.contas = []
    
    def realizar_transacao(self, conta, transacao):
        transacao.registrar(conta)

    def adiciona_conta(self, conta):
        self.contas.append(conta)

class PessoaFisica(Cliente):
    def __init__(self, nome, data_nascimento, cpf, endereco):
        super().__init__(endereco)
        self.nome = nome
        self.data_nascimento = data_nascimento
        self.cpf = cpf

class Transacao(ABC):
    @property
    @abstractproperty
    def valor(self):
        pass
    
    @abstractclassmethod
    def registrar(self, conta):
        pass


class Depositar(Transacao):
    def __init__(self, valor):
        self._valor = valor
    @property
    def valor(self):
        return self._valor
    def registrar(self, conta):
        sucesso_na_transacao = conta.depositar(self.valor)
        if sucesso_na_transacao:
            conta.historico.adicionar_transacao(self)

class Saque(Transacao):
    def __init__(self, valor):
        self._valor = valor
    @property
    def valor(self):
        return self._valor
    def registrar(self, conta):
        sucesso_na_transacao = conta.sacar(self.valor)
        if sucesso_na_transacao:
            conta.historico.adicionar_transacao(self)

def menu():
    menu = """

        =============    MENU    =============
        [1] - Novo usuário
        [2] - Nova conta
        [3] - Lista de contas
        [4] - Depositar
        [5] - Sacar
        [6] - Extrato
        [0] - Sair
        =============------------=============

    => """
    return input(menu)

def criar_usuario(clientes):
    cpf = input("Informe o CPF: ")
    usuario = filtrar_usuarios(cpf, clientes)
    if usuario:
        print("\n Já existe um usuário com esse CPF!")
        return
    nome = input("Informe o nome e sobrenome do usuário: ")
    data_nascimento = input("Informe a data de nascimento (dd-mm-aaaa): ")
    endereco = input("Informe o endereço da seguinte forma: [rua, número: bairro - cidade/sigla estado]: ")

    usuario = PessoaFisica(nome=nome, data_nascimento=data_nascimento, cpf=cpf, endereco=endereco)
    clientes.append(usuario)
    print(">>>\n\t\t\tUsuário criado com sucesso\t\t\t<<<")

def filtrar_usuarios(cpf, clientes):
    filtra_usuarios = [cliente for cliente in clientes if cliente.cpf == cpf]
    return filtra_usuarios[0] if filtra_usuarios else None

def recuperar_conta_cliente(cliente):
    if not cliente.contas:
        print("Cliente não possuí conta!")
        return
    return cliente.contas[0]

def criar_conta(numero_conta, clientes, contas):
    cpf = input("Informe o CFP do usuário: ")
    usuario = filtrar_usuarios(cpf, clientes)
    
    if not usuario:
        print("\n Usuário não encontrado!")
        return
    conta = ContaCorrente.nova_conta(cliente=usuario, numero=numero_conta)
    contas.append(conta)
    usuario.contas.append(conta)
    print("\n>>>\t\t\tConta criada com sucesso\t\t\t<<<")

def listar_contas(contas):
    for conta in contas:
        print("=" * 100)
        print(str(conta))

def depositar(clientes):
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrar_usuarios(cpf, clientes)

    if not cliente:
        print("Cliente não existe!")
        return
    valor = float(input("Informe o valor do depósito: "))
    transacao = Depositar(valor)
    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return
    cliente.realizar_transacao(conta, transacao)

def sacar(clientes):
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrar_usuarios(cpf, clientes)

    if not cliente:
        print("\nCliente não encontrado")
        return
    valor = float(input("Informe o valor de saque: "))
    transacao = Saque(valor)
    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return
    cliente.realizar_transacao(conta, transacao)

def exibir_extrato(clientes):
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrar_usuarios(cpf, clientes)
    if not cliente:
        print("\nCliente não encontrado!")
        return

    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return
    print("=============    EXTRTATO    =============")
    transacoes = conta.historico.transacoes

    extrato = ""
    if not transacoes:
        extrato = "Não foram realizadas transações."
    else:
        for transacao in transacoes:
            extrato += f"\n{transacao['Tipo']}:\t\t\tR$ {transacao['Valor']:.2f}"

    print(extrato)
    print(f"\nSaldo:\t\t\t\tR$ {conta.saldo:.2f}")
    print("=============----------------=============")

def main():
    clientes = []
    contas = []

    while True:
        opcao = menu()

        if opcao == "1":
            criar_usuario(clientes)
        elif opcao == "2":
            numero_conta = len(contas) + 1
            criar_conta(numero_conta, clientes, contas)
        elif opcao == "3":
            listar_contas(contas)
        elif opcao == "4":
            depositar(clientes)
        elif opcao == "5":
            sacar(clientes)
        elif opcao == "6":
            exibir_extrato(clientes)
        elif opcao == "0":
            break
        else:
            print("Digite uma valor válido!")

main()
