from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# Defina as informações de autenticação da RD Station
rdstation_client_id = 'bfb38759-80cc-41cf-95a6-a8db521ed0aa'
rdstation_client_secret = '7c1ea987f27f40f6b118dfec2da0fd00'
rdstation_token = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJpc3MiOiJodHRwczovL2FwaS5yZC5zZXJ2aWNlcyIsInN1YiI6Im50T3VJekdobWFlVkdJR1hxMUJ2YjdjYXRiMUR2QXM2bGx3blhYZzJLZ0FAY2xpZW50cyIsImF1ZCI6Imh0dHBzOi8vYXBwLnJkc3RhdGlvbi5jb20uYnIvYXBpL3YyLyIsImFwcF9uYW1lIjoiaW50ZWdyYcOnw6NvemVuZGVzayIsImV4cCI6MTY5NjA5NDc0NiwiaWF0IjoxNjk2MDA4MzQ2LCJzY29wZSI6IiJ9.MY8Be_DXVBvCReeD7z4M5NCY5-0fvn03dn7xqk1ChXwFNp70qjeTr4SlzEObVByviHB_GuNQt7PX-87lo7dpT0ljpToFGu_NwdSvGUpek4Mjk6kpxWWafP0u7-ALppv4ak92Q1C8JoGck3DRTgege7mJxdRBQKir44M-aIIlqXQCxf35cUPwW2Py9fHLYnFA__67Tvx2VT3tEXeRX4EMV5aciFebAsG3UlNfkU7_qIXMdgewaUE-OF47Kyzxe1_Y8eplzy8P6d7e6wtokvztKyUkzW26YlFn5I2ekr-_CO6aFwdOwhsTZv26uhCqYjZKByoXc14GSd45nZjJLGx4iw'
rdstation_base_url = 'https://api.rd.services/platform/contacts'

# Defina as informações de autenticação do Zendesk
zendesk_username = 'ola@laviesports.com.br'
zendesk_password = 'MariBetaFe192083'
zendesk_base_url = 'https://laviesportssupport.zendesk.com/admin/staff/14973530680987'

# Função para verificar se um cliente já está cadastrado na RD Station
def verificar_cadastro_rdstation(email):
    headers = {
        'Authorization': f'Bearer {rdstation_token}'
    }
    params = {
        'email': email
    }
    response = requests.get(f'{rdstation_base_url}/platform/contacts/email', headers=headers, params=params)
    if response.status_code == 200:
        data = response.json()
        return data
    else:
        return None

# Função para criar ou atualizar um contato na RD Station
def criar_ou_atualizar_contato_rdstation(email, canal, data_contato, motivo_contato):
    headers = {
        'Authorization': f'Bearer {rdstation_token}'
    }
    data = {
        'email': email,
        'lead_source': canal,
        'contact_status': 'OPEN',
        'last_conversion_date': data_contato,
        'funnel_stage': motivo_contato
    }
    response = requests.post(f'{rdstation_base_url}/platform/contacts', headers=headers, json=data)
    if response.status_code == 201:
        print('Contato criado com sucesso na RD Station')
    elif response.status_code == 200:
        print('Contato atualizado com sucesso na RD Station')
    else:
        print('Erro ao criar/atualizar contato na RD Station')

# Rota para verificar o cadastro do cliente e atualizar na RD Station
@app.route('/api/atualizar_cliente', methods=['POST'])
def atualizar_cliente():
    data = request.get_json()
    email_cliente = data.get('email')
    canal_contato = data.get('canal')
    data_contato = data.get('data_contato')
    motivo_contato = data.get('motivo_contato')

    info_cliente_rd = verificar_cadastro_rdstation(email_cliente)

    if info_cliente_rd:
        # Cliente já cadastrado na RD Station, atualizar informações
        criar_ou_atualizar_contato_rdstation(email_cliente, canal_contato, data_contato, motivo_contato)
    else:
        # Cliente não cadastrado na RD Station, criar um novo contato
        criar_ou_atualizar_contato_rdstation(email_cliente, canal_contato, data_contato, motivo_contato)

    return jsonify({'message': 'Operação concluída com sucesso'})

# Rota para trazer informações da RD Station para o Zendesk quando um ticket for aberto
@app.route('/api/trazer_informacoes', methods=['POST'])
def trazer_informacoes():
    data = request.get_json()
    # Aqui você deve implementar a lógica para trazer as informações da RD Station
    # e atualizar o ticket no Zendesk conforme necessário

    return jsonify({'message': 'Operação concluída com sucesso'})

if __name__ == '__main__':
    app.run(port=5000,host='localhost',debug=True)
#Neste exemplo, a API possui duas rotas:
#/api/atualizar_cliente: Essa rota é usada para verificar se o cliente já está cadastrado na RD Station e atualizar suas informações, se necessário.

##Você pode enviar requisições POST para essas rotas com os dados relevantes para realizar as operações desejadas. Certifique-se de que as URLs e as informações de autenticação estejam configuradas corretamente de acordo com a sua conta do Zendesk e da RD Station.

#Lembre-se de que este é um exemplo simplificado e que você precisará personalizar o código de acordo com os detalhes específicos da sua integração e implementar a lógica de atualização de tickets no Zendesk de acordo com suas necessidades.
#