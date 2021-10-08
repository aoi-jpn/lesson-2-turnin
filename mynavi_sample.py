import os
from selenium.webdriver import Chrome, ChromeOptions
from selenium.webdriver import Firefox
from selenium.webdriver.firefox.options import Options
import time
import pandas as pd

# Chromeを起動する関数


def set_driver(driver_path, headless_flg):
    if "chrome" in driver_path:
          options = ChromeOptions()
    else:
      options = Options()

    # ヘッドレスモード（画面非表示モード）をの設定
    if headless_flg == True:
        options.add_argument('--headless')

    # 起動オプションの設定
    options.add_argument(
        '--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36')
    # options.add_argument('log-level=3')
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--ignore-ssl-errors')
    options.add_argument('--incognito')          # シークレットモードの設定を付与

    # ChromeのWebDriverオブジェクトを作成する。
    if "chrome" in driver_path:
        return Chrome(executable_path=os.getcwd() + "/" + driver_path,options=options)
    else:
        return Firefox(executable_path=os.getcwd()  + "/" + driver_path,options=options)

# main処理


def main():
    print('検索ワードを入力してください')
    search_keyword = input('>> ')
    # driverを起動
    if os.name == 'nt': #Windows
        driver = set_driver("chromedriver.exe", False)
    elif os.name == 'posix': #Mac
        driver = set_driver("chromedriver", False)
    # Webサイトを開く
    driver.get("https://tenshoku.mynavi.jp/")
    time.sleep(5)
    # ポップアップを閉じる
    driver.execute_script('document.querySelector(".karte-close").click()')
    time.sleep(5)
    # ポップアップを閉じる
    driver.execute_script('document.querySelector(".karte-close").click()')

    # 検索窓に入力
    driver.find_element_by_class_name(
        "topSearch__text").send_keys(search_keyword)
    # 検索ボタンクリック
    driver.find_element_by_class_name("topSearch__button").click()


    # ページ終了まで繰り返し取得
    while True:
        # 検索結果の一番上の会社名を取得
        name_list = driver.find_elements_by_class_name("cassetteRecruit__name")
        status_list = driver.find_elements_by_class_name("labelEmploymentStatus")
        copy_list = driver.find_elements_by_class_name("cassetteRecruit__copy")

        # 空のDataFrame作成
        df = pd.DataFrame()

        # 1ページ分繰り返し
        for name,status,copy in zip (name_list,status_list,copy_list):
            try:
                print(name.text)
                print(status.text)
                print(copy.text)
                # DataFrameに対して辞書形式でデータを追加する
                df = df.append(
                    {"会社名": name.text, 
                     "仕事内容": status.text,
                     "勤務地": copy.text}, 
                    ignore_index=True)
            except Exception as e:
                print(e)
            else:
                print('finish (no error)')

        next_page = driver.find_elements_by_class_name("iconFont--arrowLeft")
        if len(next_page) >= 1:
            next_page_link = next_page[0].get_attribute("href")
            driver.get(next_page_link)
        else:
            print("最終ページです。終了します。")
            break
            
        
        


# 直接起動された場合はmain()を起動(モジュールとして呼び出された場合は起動しないようにするため)
if __name__ == "__main__":
    main()