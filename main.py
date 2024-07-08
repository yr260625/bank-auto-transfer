from selenium import webdriver
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.chrome import service
from selenium.webdriver.chrome.options import Options
from dotenv import load_dotenv
import os
import random
import json
import traceback

from bank_transfer_automation import BankTransferAutomation


def create_driver(driver_pass: str) -> WebDriver:
    """
    Chromeドライバー作成

    Returns:
        WebDriver: Chromeドライバー
    """

    ua_list = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36",
    ]
    options = Options()
    user_agent = ua_list[random.randrange(0, len(ua_list), 1)]
    options.add_argument("--user-agent=" + user_agent)
    options.add_experimental_option("excludeSwitches", ["enable-logging"])
    # テスト用に開きっぱなしにする
    options.add_experimental_option("detach", True)

    chrome_service = service.Service(executable_path=driver_pass)
    return webdriver.Chrome(service=chrome_service, options=options)


def get_bta() -> BankTransferAutomation:
    """環境変数取得

    Args:
        name (str): 環境変数名称
    Raises:
        ValueError: 未定義時に発生
    Returns:
        str: 環境変数値
    """

    load_dotenv()
    env_var = {
        "wait_time": str(os.getenv("WAIT_TIME")),
        "kaiin_no": str(os.getenv("KAIIN_NO")),
        "password": str(os.getenv("PASSWORD")),
        "hurikomi_money": str(os.getenv("HURIKOMI_MONEY")),
        "key_map": json.loads(str(os.getenv("KEY_MAP_STR"))),
        "login_url": str(os.getenv("LOGIN_URL")),
    }

    driver = create_driver(str(os.getenv("CHROMEDRIVER")))
    bta = BankTransferAutomation(env_var, driver)
    return bta


if __name__ == "__main__":

    try:
        print("-------------------------------------------")
        print("bank auto hurikomi start")
        bta = get_bta()

        # ログイン後、取引ページに遷移
        bta.login()
        bta.move_to_torihiki()

        # 銀行１
        bta.move_to_hurikomi()
        bta.execute_hurikomi(0)
        bta.execute_ninsyo()
        bta.back_to_torihiki()

        # 銀行２
        bta.move_to_hurikomi()
        bta.execute_hurikomi(1)
        bta.execute_ninsyo()
        bta.back_to_torihiki()

        # 結果参照
        bta.move_to_meisai()

        print("bank auto hurikomi end")
        print("-------------------------------------------")
    except Exception as e:
        tb = traceback.format_exc()
        print(
            f"Exception occurred in function: {traceback.extract_tb(e.__traceback__)[-1].name}"
        )
        print(f"Exception details: {str(e)}")
        print("Full traceback:")
        print(tb)