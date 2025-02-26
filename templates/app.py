import __init__
from views.view import SubscriptionService
from models.database import engine
from models.model import Subscription, Payments
from datetime import datetime, date
from decimal import Decimal

class UI:
    def __init__(self):
        self.subscription_service = SubscriptionService(engine)

    def start(self):
        while True:
            print('''
            [1] -> Adicionar assinatura
            [2] -> Remover assinatura
            [3] -> Valor total
            [4] -> Gastos últimos 12 meses
            [5] -> Pagar assinatura
            [6] -> Sair
            ''')
    
            choice = int(input('Escolha uma opção: '))
            if choice == 1:
                self.add_subscription()
            elif choice == 2:
                self.delete_subscription()
            elif choice == 3:
                self.total_value()
            elif choice == 4:
                self.subscription_service.gen_chart()
            elif choice == 5:
                self.add_pay()
            # chamar metodo pay na interface
            else:
                break

    def add_subscription(self):
        empresa = input('Empresa: ')
        site = input('Site: ')
        data_assinatura = datetime.strptime(input('Data da Assinatura: '), '%d/%m/%Y')
        valor = Decimal(input('Insira o valor: '))

        subscription = Subscription(empresa = empresa, site = site, data_assinatura = data_assinatura, valor = valor)
        self.subscription_service.create(subscription)
        print('Assinatura cadastrada com sucesso')

    # Excluir assinatura e deixar os pagamentos da empresa diferente
    def delete_subscription(self):
        subscriptions = self.subscription_service.list_all()
        print('Qual assinatura deseja excluir? ')

        for i in subscriptions:
            print(f'[{i.id}] -> [{i.empresa}]')

            choice = input('Escolha uma assinatura: ')
            if choice != i.id:
                return
            
            self.subscription_service.delete(choice)
            
            if self.subscription_service.delete(choice):
                question = input('Dejesa excluir os históricos de pagamentos? Y ou N: ')
                if not question.upper() == 'Y':
                    return
            
                self.subscription_service.delete_payment(choice)

            if question == 'Y':
                print('Sua assinatura e historico de pagamento foram deletados com sucesso.')
            else:
                print('Sua assinatura foi excluida com sucesso.')

    def total_value(self):
        print(f'O valor total gasto por mês é de: {self.subscription_service.total_value()}')

    def add_pay(self):
        empresa = input('Pagamento é de qual empresa? ')
        site = input('Site da empresa: ')
        data_assinatura = date.today()
        valor = Decimal(input('Qual valor foi pago? '))

        subscription = Subscription(empresa = empresa, site = site, data_assinatura = data_assinatura, valor = valor)

        self.subscription_service.pay(subscription)
        print(f'Seu pagamento foi cadastrado')

UI().start()