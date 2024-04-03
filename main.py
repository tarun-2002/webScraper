from flask import Flask, render_template, request
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/scrape', methods=['POST'])
def scrape():
    url = request.form['url']
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    form = soup.find('form')
    input_and_select_elements = form.find_all(['input', 'select'])
    elements_data = []

    for element in input_and_select_elements:
        element_data = {}
        element_data['id'] = element.get('id', '')
        if element.name == 'input':
            placeholder = element.get('placeholder')
            if placeholder:
                element_data['placeholder'] = placeholder
        elif element.name == 'select':
            first_option = element.find('option')
            if first_option:
                first_option_text = first_option.text.strip()
                element_data['first_option'] = first_option_text
        elements_data.append(element_data)

    return render_template('result.html', elements_data=elements_data)

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='0.0.0.0', port=5000)
