from flask import Flask, render_template, request
import json
import requests

app = Flask(__name__)
@app.route('/', methods=['GET','POST'])
def main():
    
    if request.method=='POST':
        
        title=str(request.form['title'])
        description=str(request.form['description'])
        candidate_http_request_json = json.dumps({'Title':title,'Description':description})
        PARAMS = json.dumps({'jobOrder':candidate_http_request_json}, indent=2)
        headers={'Content-type':'application/json', 'Accept':'application/json'}
        inbound_http_request = requests.post(url = 'https://outboundparser.azurewebsites.net/api/outboundparser', data = PARAMS,headers = headers)
        candidates=[i for i in str(inbound_http_request.text).split()]
        if len(candidates)<10:
            for i in range(len(candidates),10):
                candidates.append('Nil')
        a1=candidates[0]
        a2=candidates[1]
        b1=candidates[2]
        b2=candidates[3]
        c1=candidates[4]
        c2=candidates[5]
        d1=candidates[6]
        d2=candidates[7]
        e1=candidates[8]
        e2=candidates[9]
        return render_template('result.html', a1=a1, a2=a2, b1=b1, b2=b2, c1=c1, c2=c2, d1=d1, d2=d2, e1=e1, e2=e2)
    
    return render_template('index.html')

if __name__=='__main__':
	app.run(debug=True)