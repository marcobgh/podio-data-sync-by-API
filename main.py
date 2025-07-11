from flask import Flask, request, jsonify
from models.Empresa import Empresa
from services.podio_service import get_access_token, atualizar_item_podio, validar_webhook, get_podio_item_by_id, get_cnpj, usuario_solicitou_atualizacao
from services.receitaws_service import buscar_cnpj_ws


app = Flask(__name__)
PODIO_ACCESS_TOKEN = get_access_token()

@app.route('/create', methods=['POST'])
def webhook_create():
    global item_id
    data = request.form.to_dict()  # ou request.form se vier como formulário

    if data.get('type') == 'hook.verify':
        validar_webhook(data, PODIO_ACCESS_TOKEN)

    else: # Caso não seja verificação, trata como webhook comum
        print("Webhook comum recebido:", data)

        item_id = data.get('item_id')

    response = get_podio_item_by_id(item_id, PODIO_ACCESS_TOKEN)

    if response.status_code == 200:
        item_data = response.json()

        dados_receita = buscar_cnpj_ws(get_cnpj(item_data))

        atualizar_item_podio(item_id, PODIO_ACCESS_TOKEN, dados_receita)

    else:
        print("Erro ao buscar item:", response.status_code, response.text)

    return jsonify({"message": "Webhook processado"}), 200


@app.route('/update', methods=['POST'])
def webhook_update():
    global item_id
    data = request.form.to_dict() # ou request.form se vier como formulário

    if data.get('type') == 'hook.verify':
        validar_webhook(data, PODIO_ACCESS_TOKEN)

    else: # Caso não seja verificação, trata como webhook comum
        print("Webhook comum recebido:", data)

        item_id = data.get('item_id')

    response = get_podio_item_by_id(item_id, PODIO_ACCESS_TOKEN)

    if response.status_code == 200:
        item_data = response.json()

        if usuario_solicitou_atualizacao(item_data) == 1:

            # Captura e formata o cnpj da empresa e em seguida consulta ele na receita
            cnpj = get_cnpj(item_data)
            dados_receita = buscar_cnpj_ws(cnpj)

            # Compara o item do podio com o item da receita para apontar suas diferenças
            diferentes = Empresa.comparar_objetos(item_data, dados_receita)

            if diferentes:
                dados_receita.update({'cadastro': 'Desatualizado'})
                dados_receita.update({'observacoes': diferentes})
            else:
                dados_receita.update({'cadastro': 'Atualizado'})
                dados_receita.update({'observacoes': ' '})

            atualizar_item_podio(item_id, PODIO_ACCESS_TOKEN, dados_receita)
        else:
            print("Usuário não solicitou consulta")
    else:
        print("Erro ao buscar item:", response.status_code, response.text)

    return jsonify({"message": "Webhook processado"}), 200

if __name__ == '__main__':
    app.run(port=5000)


