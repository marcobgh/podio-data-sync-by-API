import requests as requests
from datetime import datetime

def buscar_cnpj_ws(cnpj):
    global dados_receita
    response = requests.get(f'https://receitaws.com.br/v1/cnpj/{cnpj}')
    if response.status_code == 200:
        cnpj_ws = response.json()


        cnaes_sec = "\n".join([f"{cnaesec['code']} - {cnaesec['text']}" for cnaesec in cnpj_ws["atividades_secundarias"]])
        socios = "\n".join(f"{socio['nome']} - {socio['qual']}" for socio in cnpj_ws['qsa'])
        cnae_prim = "\n".join(f"{cnae['code']} - {cnae['text']}" for cnae in cnpj_ws["atividade_principal"])

        if cnpj_ws['complemento'] == '':
            endereco = f"{cnpj_ws['logradouro']}, n° {cnpj_ws['numero']}, {cnpj_ws['bairro']}, {cnpj_ws['municipio']}/{cnpj_ws['uf']}, {cnpj_ws['cep']}"
        else:
            endereco = f"{cnpj_ws['logradouro']}, n° {cnpj_ws['numero']}, {cnpj_ws['complemento']}, {cnpj_ws['bairro']}, {cnpj_ws['municipio']}/{cnpj_ws['uf']}, {cnpj_ws['cep']}"

        dados_receita = {
            'nome': cnpj_ws['nome'],
            'capital-social': cnpj_ws['capital_social'],
            'socios': socios,
            'email-2': cnpj_ws['email'],
            'telefone-2': cnpj_ws['telefone'],
            'tipo': cnpj_ws['tipo'],
            'cnaes-secundarios': cnaes_sec,
            'cnae-principal': str(cnae_prim),
            'endereco': endereco,
            'dinheiro': {"value": cnpj_ws['capital_social'], "currency": "BRL"},
            'data-da-ultima-consulta': {"start": datetime.now().strftime("%Y-%m-%d %H:%M:%S")},
            'consulta-na-receita': 2,
            'cadastro': 'Atualizado'
        }

        if cnpj_ws["fantasia"] != '':
            dados_receita.update({'nome-fantasia': cnpj_ws['fantasia']})

        return dados_receita

    else:
        dados_receita = {
            'consulta-na-receita': 3
        }

    return dados_receita
