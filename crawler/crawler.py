# coding: utf-8
import os, sys, re, time, argparse
from collections import OrderedDict
from pprint import pprint

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import pandas as pd
import requests
import mojimoji


from common import timewatch


root_url = 'https://ruru-jinro.net'
page_url_template = os.path.join(root_url, "searchresult.jsp?st=%d&sort=NUMBER")
imported_urls_filename = 'imported_urls.txt'


def get_driver():
    options = Options()
    options.add_argument('--headless')
    driver = webdriver.Chrome(chrome_options=options)
    return driver

def fix_unicode_escape(text, to_space=True):
    if not text:
        return ''
    X = ' ' if to_space else ''

    text = text.replace('\u3000', X).replace('\xa0', X)
    text = text.replace('<br\/>', X)
    text = ' '.join([w for w in text.split() if w]).strip()
    return text

@timewatch()
def parse_page(page_url, vinfo, driver):
    driver.get(page_url)
    html_source = driver.page_source
    soup = BeautifulSoup(html_source, "html5lib")
    log_table = soup.find("table", {"id": "villageslog"})
    if log_table is None:
        print('None was detected')
        print(soup)
        exit(1)
    print('url', page_url)
    print('thead', log_table.find('thead'))
    print('thead.tr', log_table.find('thead').find('tr'))
    print('thead.tr.th', log_table.find('thead').find('tr').find_all('th'))
    # exit(1)
    
    header = [th.text for th in log_table.find('thead').find('tr').find_all('th')]
    # print(header)

    new_vinfo = []
    village_urls = {}
    for tr in log_table.find('tbody').find_all('tr'):
        values = [fix_unicode_escape(td.text) for td in tr.find_all('td')]
        # info = OrderedDict([(h, v) for h, v in zip(header, values)])
        urls = tr.find_all('a') # 全公開，霊界会話/役職表示なし，霊界会話のみ

        if len(values) < 3:
            continue
        village_id = values[0]
        winner = values[3]
        if winner == '廃 村':
            continue
        if int(village_id) in vinfo['No.'].values:
            continue
        assert len(values) == len(header)
        new_vinfo.append(values)
        village_url = os.path.join(root_url, urls[0].get('href'))
        village_urls[village_id] = village_url
    new_vinfo = pd.DataFrame(new_vinfo, columns=header)

    print('Page: ', page_url)
    print('# Known villages:', len(vinfo))
    print('# New villages:', len(new_vinfo))

    for village_id in new_vinfo['No.'].values:
        village_url = village_urls[village_id]
        target_path = args.target_dir + '/%s.html' % village_id
        if not os.path.exists(target_path):
            try:
                log = get_log(village_url, driver)
            # except requests.exceptions.ConnectionError:
            except:
                continue
            with open(target_path, 'w') as f:
                f.write(log)
        time.sleep(0.1)

    update_vinfo(new_vinfo, args.village_info)
    time.sleep(1)
    return new_vinfo


def update_vinfo(new_vinfo, info_path):
    with open(info_path, 'a') as f:
        f.write(new_vinfo.to_csv(header=False, index=False))


def get_log(village_url, driver):
    r = requests.get(village_url)
    driver.get(village_url)
    html_source = driver.page_source
    return html_source


def load_village_info(path):
    if os.path.exists(path):
        vinfo = pd.read_csv(path)
    else:
        header = ['No.', '終了時刻', '村名', '勝者', 'ＧＭ', '希職', '聴狂', '猫又', '身内', '１５', '強化', '配役']
        vinfo = pd.DataFrame(columns=header)
        with open(path, 'w') as f:
            f.write(vinfo.to_csv(header=True, index=False))
    return vinfo


def main(args):
    os.makedirs(args.target_dir, exist_ok=True)
    vinfo = load_village_info(args.village_info)

    page_id = args.start_page
    driver = get_driver()
    while not args.max_page or page_id < args.max_page:
        page_url = page_url_template % page_id
        new_vinfo = parse_page(page_url, vinfo, driver)
        # try: 
        #     new_vinfo = parse_page(page_url, vinfo, driver)
        # except KeyboardInterrupt:
        #     exit(1)
        # except Exception as e:
        #     print(e)
        #     continue
        vinfo = pd.concat([vinfo, new_vinfo])
        page_id += 1 




if __name__ == "__main__":
    desc = ""
    parser = argparse.ArgumentParser(description=desc)
    parser.add_argument('-sp', '--start_page', type=int, default=1, help=' ')
    parser.add_argument('-mp', '--max_page', type=int, default=1, help=' ')
    parser.add_argument('-t', '--target_dir', type=str, default='logs/rawfile')
    parser.add_argument('-vi', '--village_info', type=str, default='logs/villages.csv')
    args = parser.parse_args()
    main(args)

