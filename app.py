from flask import Flask, request, jsonify
import yfinance as yf

app = Flask(__name__)

@app.route("/<symbol>")
def get_stock_data(symbol):
    interval = request.args.get("interval", "15m")
    range_ = request.args.get("range", "5d")
    
    try:
        df = yf.download(symbol, interval=interval, period=range_)
        if df.empty:
            return jsonify({"error": "No data returned from yfinance"}), 404

        df.reset_index(inplace=True)
        df = df[["Datetime", "Open", "High", "Low", "Close", "Volume"]]
        df["Datetime"] = df["Datetime"].astype(str)
        return df.to_dict(orient="records")
    except Exception as e:
        return jsonify({"error": str(e)}), 500
