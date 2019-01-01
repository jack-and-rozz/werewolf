# coding: utf-8
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from pprint import pprint
from collections import OrderedDict
import os, sys, re, time, argparse
import bs4
from bs4 import BeautifulSoup
import requests
from utils.common import dotDict
root_url = 'https://ruru-jinro.net'
page_url_template = os.path.join(root_url, "searchresult.jsp?st=%d&sort=NUMBER")
imported_urls_filename = 'imported_urls.txt'

def get_driver():
  options = Options()
  options.set_headless(True) # headlessモードを有効に
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


def parse_players_log(tds):
  assert len(tds) == 2
  cn, cc = tds
  line = []
  #print(cn.contents)
  for content in cn.contents:
    if content.name == 'span':
      if 'name' in content.get('class'):
        ctype = 'name'
      else:
        ctype = content.get('class')[0]
      text = content.text
    else:
      ctype = 'id'
      text = content
    line.append((ctype, fix_unicode_escape(text)))

  for content in cc.contents:
    if content.name == 'span':
      ctype = content.get('class')[0]
      text = content.text
    elif not content.name:
      ctype = 'text'
      text = content
    line.append((ctype, fix_unicode_escape(text)))

  print(line)

def parse_vote_log(tds):
  pass

def parse_system_log(tds):
  pass

def parse_action_log(tds):
  pass

def parse_logs(village_url, driver):
  r = requests.get(village_url)
  driver.get(village_url)
  html_source = driver.page_source
  #html_source = requests.get(village_url).content
  #print(html_source)
  soup = BeautifulSoup(html_source, "html5lib")
  #print(soup)
  #days = soup.find_all("div", {"class": "d12150"})
  chatlogs = soup.find_all("div", {"class": "d12151"})
  #sys.stdout = sys.stderr
  for i, day_div in enumerate(chatlogs):
    lines = day_div.find(
      "table", recursive=False).find(
        'tbody', recursive=False).find_all(
          'tr', recursive=False)
    for line in lines:
      tds = [x for x in line.children]
      print(line)
      ltype = tds[0].get('class')[0]
      # 左側のカラムで判断
      if ltype == 'cn': # プレイヤーの発言
        parse_players_log(tds)
      elif ltype == 'ca': # アクション結果
        parse_action_log(tds[0])
      elif ltype == 'cv': # 投票結果
        parse_vote_log(tds[0])
      elif ltype == 'cs': # システムメッセージ
        parse_system_log(tds[0])
      else: # 霊界会話(cnd), GM会話(cng)など
        continue
      print()
      #syslog = line.find('td', {'class': 'ca'})
      #vote = line.find('td', {'class': 'cv'})
      #name = line.find('td', {'class': 'cn'})
      #message = line.find('td', {'class': 'cc'})
  #print (soup)
  exit(1)

  # Profiles of the players.
  profile_table = soup.find("div", {"class": "d1221"}).find("table")
  names = profile_table.find_all("a", {"class": "report"})
  roles = profile_table.find_all("span", {"class": re.compile('oc[0-9]+')})
  tmp_names = [x.find('span').text for x in names]
  fixed_names = [re.match('%s【(.+)】' % tn, x.text).group(1) 
                 for x, tn in zip(names, tmp_names)]
  roles = [fix_unicode_escape(x.text, to_space=False) for x in roles]


def main(args):
  imported_urls_filepath = os.path.join(args.target_dir, imported_urls_filename)
  imported_urls = set()
  if os.path.exists(imported_urls_filepath):
    for l in open(imported_urls_filepath):
      imported_url.add(l.replace('\n', ''))

  page_id = 1
  while True:
    page_url = page_url_template % page_id
    driver = get_driver()
    driver.get(page_url)
    html_source = driver.page_source
    soup = BeautifulSoup(html_source, "html5lib")
    log_table = soup.find("table", {"id": "villageslog"})
    header = [th.text for th in log_table.find('thead').find('tr').find_all('th')]
    print(header)
    for tr in log_table.find('tbody').find_all('tr'):
      values = [fix_unicode_escape(td.text) for td in tr.find_all('td')]
      info = OrderedDict([(h, v) for h, v in zip(header, values)])
      urls = tr.find_all('a') # 全公開，霊界会話/役職表示なし，霊界会話のみ
      if info['勝者'] == '廃 村':
        continue
      assert len(values) == len(header)
      assert len(urls) == 3
      village_url = os.path.join(root_url, urls[0].get('href'))
      sys.stderr.write("Parsing \'%s\' ...\n" % village_url)
      village_url = 'https://ruru-jinro.net/log5/log459430.html'
      log = parse_logs(village_url, driver)
      time.sleep(1)

    r = requests.get(page_url)
    soup = BeautifulSoup(r.text, "html.parser")
    time.sleep(1)
    page_id += 1

if __name__ == "__main__":
  desc = ""
  parser = argparse.ArgumentParser(description=desc)
  parser.add_argument('-m', '--max_pages', type=int, default=1)
  parser.add_argument('-t', '--target_dir', type=str, default='logfiles')
  args = parser.parse_args()
  main(args)
