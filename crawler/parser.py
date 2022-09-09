# coding: utf-8
import os, sys, re, time, argparse
from collections import OrderedDict
from pprint import pprint
import glob
# from selenium import webdriver
# from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import requests
import mojimoji

from crawler import fix_unicode_escape

def parse_players_log(tds):
    assert len(tds) == 2
    cn, cc = tds
    parsed = []
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
        parsed.append((ctype, fix_unicode_escape(text)))

    for content in cc.contents:
        if content.name == 'span':
            ctype = content.get('class')[0]
            text = content.text
        elif not content.name:
            ctype = 'text'
            text = content
        else:
            continue

        parsed.append((ctype, fix_unicode_escape(text)))

    return parsed

def parse_vote_log(tds):
    parsed = []
    return parsed

def parse_system_log(tds):
    assert len(tds) == 1
    parsed = []

    # for content in tds[0].contents:
    content = tds[0].contents[0]
    if content.name == 'span':
        ctype = content.get('class')[0]
        # parsed.append((ctype, content.text))
        # if ctype == 'death':
        #     print('cont', content)
        #     print(content.find('span'))
        #     print(content.find('span').text)
        #     exit(1)
        parsed.append((ctype, fix_unicode_escape(content.find('span').text)))
        text = fix_unicode_escape(content.text)
        parsed.append(('text', text))
    elif len(tds[0].contents) >= 2:
        ## ['「', '$user_name', '」さんが…しました'] の形
        player_name = tds[0].contents[1].text
        parsed = [('name', player_name)]
        text = fix_unicode_escape(''.join([c.text for c in tds[0].contents]))
        parsed += [('text', text )]
    else:
        # タグなしテキストのみ
        text = fix_unicode_escape(content.text)
        parsed.append(('text', text))

    return parsed

def parse_action_log(tds):
    assert len(tds) == 1
    parsed = []
    for content in tds[0].contents:
        if content.name == 'span':
            ctype = content.get('class')[0] # アクション実行者の役職
            parsed.append(('role', ctype))
            action_log = [fix_unicode_escape(c.text) for c in content.find_all('span')]
        parsed.append(('source', action_log[0]))
        parsed.append(('target', action_log[1]))
        if len(action_log) >= 3:
            parsed.append(('result', action_log[2]))
        # parsed.append((ctype, fix_unicode_escape(text)))

    return parsed

def parse_watchers_log(tds):
    cn, cc = tds
    parsed = [('name', cn.text)]
    for content in cc.contents:
        if content.name == 'span':
            ctype = content.get('class')[0]
            text = content.text
        elif not content.name:
            ctype = 'text'
            text = content
        else:
            continue
        parsed.append((ctype, fix_unicode_escape(text)))
    return parsed

def parse_deadmens_log(tds):
    cnd, ccd = tds
    parsed = [('name', cnd.text)]
    for content in ccd.contents:
        if content.name == 'span':
            ctype = content.get('class')[0]
            text = content.text
        elif not content.name:
            ctype = 'text'
            text = content
        else:
            continue
        parsed.append((ctype, fix_unicode_escape(text)))
    return parsed

def parse_gamemasters_log(tds):
    # parsed = []
    parsed = parse_players_log(tds)
    return parsed


def parse_log(path):
    soup = BeautifulSoup(open(path), "html5lib")
    chatlogs = soup.find_all("div", {"class": "d12151"})
    for i, day_div in enumerate(chatlogs):
        lines = day_div.find(
            "table", recursive=False).find(
                'tbody', recursive=False).find_all(
                    'tr', recursive=False)
        for line in lines:

            tds = [x for x in line.children]
            ltype = tds[0].get('class')[0]

            print('line:', line)
            # if ltype == 'cs':
            #     print('line:', line)
            #     print('tds:', tds, len(tds))
            #     parsed = parse_system_log(tds)
            #     print(parsed)
            #     print()
            #     continue
            # else:
            #     continue

            # 左側のカラムで判断
            if ltype == 'cn': # プレイヤーの発言
                parsed = parse_players_log(tds)
            elif ltype == 'cnw': # 観戦者の発言
                parsed = parse_watchers_log(tds)
            elif ltype == 'cnd': # 死亡者の発言
                parsed = parse_deadmens_log(tds)
            elif ltype == 'cng': # GMの発言
                parsed = parse_gamemasters_log(tds)
            elif ltype == 'ca': # アクション結果
                parsed = parse_action_log(tds)
            elif ltype == 'cv': # 投票結果
                parsed = parse_vote_log(tds)
            elif ltype == 'cs': # システムメッセージ
                parsed = parse_system_log(tds)
            else:
                continue
            parsed = [('type', ltype)] + parsed
            print("parsed:", parsed)
            print()
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
    os.makedirs(args.target_dir, exist_ok=True)
    for source_path in glob.glob(args.source_dir + '/*'):
        bname = os.path.basename(source_path)
        target_path = args.target_dir + '/' + bname
        if os.path.exists(target_path):
            continue
        source_path = 'logs/rawfile/499680.html'
        parsed_log = parse_log(source_path)

if __name__ == "__main__":
    desc = ""
    parser = argparse.ArgumentParser(description=desc)
    parser.add_argument('-s', '--source_dir', type=str, default='logs/rawfile')
    parser.add_argument('-t', '--target_dir', type=str, default='logs/processed')
    args = parser.parse_args()
    main(args)
