from flask import Flask, Response, jsonify, request
import pymongo
import json
from yahoodata import*
import backtrader as bt
import backtrader.feeds as btfeeds


app = Flask(__name__)

try:
    mongo = pymongo.MongoClient(
        host='localhost',
        port=27017,
        serverSelectionTimeoutMS= 1000
    )
    db = mongo.BackTest
    mongo.server_info()
except:
    print("Cannot connect to db")


@app.route('/api/save_stratgy', methods=['POST'])
def hi():
    from strategys import res
    res.clear()
    data = request.get_json()
    dbResponse = db.strategy.insert_one(data)
    #response = get_data(data['fromdate'], data['todate'])
    print(f"------------{len(data['rules'])}-----------")
    if len(data['rules']) == 2:
        resp = back(data['fromdate'], data['todate'], data['balance'], 'both')
    else:
        resp = back(data['fromdate'], data['todate'], data['balance'],data['rules'][0]['indicator'])
    return jsonify({'message': resp})





if __name__ == "__main__":
    app.run(debug=True)