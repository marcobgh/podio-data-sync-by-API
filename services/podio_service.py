from dotenv import load_dotenv
import os
import requests as requests
from flask import Flask, request, jsonify
import re


def get_access_token():
    load_dotenv()

    response = requests.post("https://podio.com/oauth/token", data={
        "grant_type": "password",
        "client_id": os.getenv('CLIENT_ID'),
        "client_secret": os.getenv('CLIENT_SECRET'),
        "username": os.getenv('PODIO_USERNAME'),
        "password": os.getenv('PASSWORD')
    })

    if response.status_code == 200:
        token = response.json()["access_token"]
        return token
    else:
        print("Erro ao obter token:", response.status_code, response.text)
        return None

def atualizar_item_podio(item_id, access_token, campos):
    url = f'https://api.podio.com/item/{item_id}'
    headers = {
        'Authorization': f'OAuth2 {access_token}',
        'Content-Type': 'application/json'
    }
    payload = {
        "fields": campos  # já espera um dicionário com os external_id dos campos
    }
    response = requests.put(url, json=payload, headers=headers)
    if response.status_code == 200:
        print("Item podio atualizado com sucesso!")
    else:
        print("Erro ao atualizar item podio:", response.status_code, response.text)

def validar_webhook(data, token):

    hook_id = data.get('hook_id')
    code = data.get('code')

    print(f"Recebido hook.verify - hook_id: {hook_id}, code: {code}")

    # Faz a validação com a API do Podio
    response = requests.post(
        f"https://api.podio.com/hook/{hook_id}/verify/validate",
        headers={
            "Authorization": f"OAuth2 {token}",
            "Content-Type": "application/json"
        },
        json={"code": code}
    )

    print("Resposta do Podio:", response.status_code, response.text)

    if response.status_code == 200:
        return jsonify({"message": "Webhook validado com sucesso!"}), 200
    else:
        return jsonify({"message": "Falha ao validar webhook"}), 500

def get_podio_item_by_id(item_id, token):
    response = requests.get(
        f'https://api.podio.com/item/{item_id}',
        headers={
            'Authorization': f'OAuth2 {token}'
        }
    )

    return response

def get_cnpj(item_data):
    global cnpj
    for campo in item_data["fields"]:
        if campo["external_id"] == "cnpj":
            cnpj_numero = campo["values"][0]["value"]
            cnpj = re.sub(r'\D', '', cnpj_numero)

    return cnpj

def usuario_solicitou_atualizacao(item_data):
    return next(
        field for field in item_data['fields'] if field['external_id'] == 'consulta-na-receita')['values'][0]['value'][
        'id']
