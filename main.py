import json
from typing import List
from datetime import datetime, timezone, timedelta
from stock.real_time import stock, index
import threading
import requests
import warnings
import twstock
import time
import os

warnings.filterwarnings("ignore")


def loading(keep: int, speed: int = 0.2):
    loading = ["|", "/", "-", "\\"]

    while keep > 0:
        for i in range(len(loading)):
            print(
                f"""現在時間: {str(datetime.now(
                timezone(timedelta(hours=+8))).strftime("%Y/%m/%d %H:%M:%S"))} {loading[i]}""",
                end="\r",
            )
            time.sleep(0.2)
            keep -= speed


def display(data: str | List[dict], delay: int) -> None:
    while True:
        try:
            th = threading.Thread(target=loading, args=(delay,))
            th.start()

            # 更新主要資料
            stock_data = stock(data)
            index_data = index()

            result_time = f"""最後更新時間: {str(datetime.now(
                timezone(timedelta(hours=+8))).strftime("%Y/%m/%d %H:%M:%S"))}\n\n"""
            result_data = ""

            # 加權數據
            index_info = index_data["index"]["infoArray"][0]
            result_data += f"""台股加權\n現價: {index_info["z"]}\n昨收: {index_info["y"]}\n盤中最高:{index_info["h"]}\n盤中最低:{index_info["l"]}\n\n"""
            futures_index_info = index_data["futures_index"]["msgArray"][0]
            result_data += f"""{futures_index_info["n"]}\n現價: {futures_index_info["z"]}\n昨收: {futures_index_info["y"]}\n盤中最高: {futures_index_info["h"]}\n盤中最低: {futures_index_info["l"]}\n\n"""  # 台指期

            result_data += f"""期現價差: {round(float(futures_index_info["z"]) - float(index_info["z"]),2)}\n\n"""

            for s in stock_data:
                result_data += (
                    f"""{s["code"]} {s["name"]} {round(float(s["price"]["now"]),2)}"""
                )
                result_data += "\n"
            result_data += "\n"

            th.join()  # loading done

            # 刷新頁面
            os.system("clear")
            print(result_time, end="\r")
            print(result_data, end="\r")

            loading(0.2)
        except KeyboardInterrupt:
            break


if __name__ == "__main__":
    display(
        [
            "0050",
            "006208",
            "00631L",
            "00753L",
            "00647L",
            "00632R",
            "0056",
            "00878",
            "00713",
            "00919",
            "00940",
            "00687B",
            "00679B",
            "00937B",
            "2330",
            "2412",
            "2317",
        ],
        5,
    )
