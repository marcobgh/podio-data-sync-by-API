from bs4 import BeautifulSoup

class Empresa:
    def __init__(self, dados):
        self.razao_social = dados['nome']
        self.fantasia = dados['nome-fantasia']
        self.capital = dados['capital-social']
        self.email = dados['email-2']
        self.telefone = dados['telefone-2']
        self.cnae_principal = dados['cnae-principal']
        self.endereco = dados['endereco']
        self.cnaes_secundarios = dados['cnaes-secundarios']
        self.socios = dados['socios']

    def criar_objeto_webhook_podio(webhook):
        capital = next(field for field in webhook['fields'] if field['external_id'] == 'dinheiro')['values'][0]['value']
        capital2 = float(capital)
        dados = {
            # Utiliza o BeautifulSoup para remover as tags html e percorre o json procurando pelo valor
            'nome': BeautifulSoup(
                next(field for field in webhook['fields'] if field['external_id'] == 'nome')['values'][0]['value'],
                'html.parser').get_text(),
            'nome-fantasia': BeautifulSoup(
                next(field for field in webhook['fields'] if field['external_id'] == 'nome-fantasia')['values'][0][
                    'value'], 'html.parser').get_text(),
            'capital-social': f"{capital2:.2f}",
            'email-2': BeautifulSoup(
                next(field for field in webhook['fields'] if field['external_id'] == 'email-2')['values'][0]['value'],
                'html.parser').get_text(),
            'telefone-2': BeautifulSoup(
                next(field for field in webhook['fields'] if field['external_id'] == 'telefone-2')['values'][0][
                    'value'], 'html.parser').get_text(),
            'cnae-principal': BeautifulSoup(
                next(field for field in webhook['fields'] if field['external_id'] == 'cnae-principal')['values'][0][
                    'value'], 'html.parser').get_text(),
            'endereco': BeautifulSoup(
                next(field for field in webhook['fields'] if field['external_id'] == 'endereco')['values'][0]['value'],
                'html.parser').get_text(),
            'cnaes-secundarios': BeautifulSoup(
                next(field for field in webhook['fields'] if field['external_id'] == 'cnaes-secundarios')['values'][0]['value'],
                'html.parser').get_text(separator='\n').strip(),
            'socios': BeautifulSoup(
                next(field for field in webhook['fields'] if field['external_id'] == 'socios')['values'][0]['value'],
                'html.parser').get_text(separator='\n').strip()
        }
        return Empresa(dados)

    def comparar_objetos(item_podio, item_receita):
        diffs = []
        obj1 = Empresa.criar_objeto_webhook_podio(item_podio)
        obj2 = Empresa(item_receita)

        for campo in vars(obj1):
            valor1 = getattr(obj1, campo)
            valor2 = getattr(obj2, campo)
            if valor1 != valor2:
                nome_campo_formatado = campo.replace('_', ' ').capitalize()
                diffs.append(f'- {nome_campo_formatado}: de "{valor1}" para "{valor2}"')

        if diffs:
            return "Diferenças encontradas:\n" + "\n".join(diffs)
        else:
            return None
