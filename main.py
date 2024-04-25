from typing import List
from datetime import datetime
import twstock
import time
import os


def get_real_time_stock_data(code: str | List[str]) -> dict:  # 盤中即時報價
    stock = twstock.realtime.get(code)

    def transform_data(stock: dict) -> dict:
        real_time = stock["realtime"]
        info = stock["info"]
        latest_trade_price = real_time["latest_trade_price"]  # 即時報價
        five_price = real_time["best_bid_price"]  # 五檔報價

        return {
            "code": info["code"],
            "name": info["name"],
            "time": info["time"],
            "timestamp": stock["timestamp"],
            "price": {
                "now": (
                    latest_trade_price if latest_trade_price != "-" else five_price[0]
                ),
                "open": real_time["open"],
                "high": real_time["high"],
                "low": real_time["low"],
            },
        }

    def multiple_data_to_list(stock: dict) -> dict:
        del stock["success"]
        return [stock[key] for i, key in enumerate(stock)]

    if type(code) == str:
        return [transform_data(stock)]
    else:
        return [transform_data(data) for data in multiple_data_to_list(stock)]


def display(data: str | List[dict], delay: int) -> None:
    while True:
        try:
            result = "====================================\n\n"
            result += f"""最後更新時間: {str(datetime.now())[:19]}\n\n"""
            stock_data = get_real_time_stock_data(data)
            for i in range(len(stock_data)):
                s = stock_data[i]
                result += f"""{s["code"]} {s["name"]} {s["price"]["now"]}"""
                result += "\n"
            result += "\n===================================="
            os.system("clear")
            print(result, end="\r")
            time.sleep(delay)
        except KeyboardInterrupt:
            break


if __name__ == "__main__":
    display(
        ["0050", "006208", "00631L", "00687B", "00937B", "00940", "2330", "2317"], 5
    )
