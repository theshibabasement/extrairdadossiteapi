from flask import Flask, request, jsonify
import re
import requests
import ssl

app = Flask(__name__)

def extract_domain(url):
    domain_pattern = r'(?:https?://)?(?:www\.)?([^/]+)'
    domain_match = re.search(domain_pattern, url)
    return domain_match.group(1) if domain_match else None

def extract_data(url):
    # Faz um request GET para a página inicial do site
    response = requests.get(url)
    
    # Verifica se o request foi bem-sucedido
    if response.status_code == 200:
        # Obtém o conteúdo da página
        content = response.text
        
        # Extrai o domínio da URL
        domain = extract_domain(url)
        
        # Extrai o email
        email_pattern = r'\b[A-Za-z0-9._%+-]+@' + re.escape(domain) + r'\b'
        email_match = re.search(email_pattern, content)
        email = email_match.group() if email_match else None
        
        # Extrai o CNPJ
        cnpj_pattern = r'\d{2}\.\d{3}\.\d{3}/\d{4}-\d{2}'
        cnpj_match = re.search(cnpj_pattern, content)
        cnpj = cnpj_match.group() if cnpj_match else None
        
        # Extrai o WhatsApp
        whatsapp_pattern = r'(?:https?://)?(?:api\.whatsapp\.com/send\?l=pt_br&phone=|wa\.me/)(\d+)'
        whatsapp_match = re.search(whatsapp_pattern, content)
        whatsapp = whatsapp_match.group(1) if whatsapp_match else None
        
        # Extrai o Instagram
        instagram_pattern = r'(?:https?://)?(?:www\.)?instagram\.com/([A-Za-z0-9_\.]+)'
        instagram_match = re.search(instagram_pattern, content)
        instagram = instagram_match.group(1) if instagram_match else None
        
        # Extrai o Facebook
        facebook_pattern = r'(?:https?://)?(?:www\.)?facebook\.com/(?!tr\?)[A-Za-z0-9_\.]+(?!/\?)'
        facebook_match = re.search(facebook_pattern, content)
        facebook = facebook_match.group() if facebook_match else None
        
        return {
            'email': email,
            'cnpj': cnpj,
            'whatsapp': whatsapp,
            'instagram': instagram,
            'facebook': facebook
        }
    else:
        return None

@app.route('/extract', methods=['POST'])
def extract_endpoint():
    data = request.get_json()
    url = data.get('url')
    
    if url:
        result = extract_data(url)
        if result:
            return jsonify(result), 200
        else:
            return jsonify({'error': 'Failed to extract data'}), 500
    else:
        return jsonify({'error': 'URL not provided'}), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000)



