from flask import Flask, request, jsonify
import yfinance as yf

app = Flask(__name__)

@app.route("/price", methods=["GET"])
def get_price():
    symbol = request.args.get("ticker", "UMAC").upper()
    interval = request.args.get("interval", "15m")
    try:
        df = yf.download(symbol, period="5d", interval=interval)
        df = df.reset_index()
        df["Datetime"] = df["Datetime"].astype(str)
        data = df.to_dict(orient="records")
        return jsonify(data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
