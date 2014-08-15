
ログファイルの管理はlog_managerディレクトリで行う。

1.ログファイルの整型
python log_manager -parse [srcfilename] [destfilename]
とすることで./log_manager/logfiles内のわかめての村ログをパース可能。

2. 学習処理
python log_manager -learn で可能。
主な用語についてと、適当に選んだ形態素についての各役職のスコアが表示される。

3. 役職当てテスト
python log_manager -infer [rolename] で、学習に使用していない村ログの
各役職の発言データからの役職当てテストが出来る。

rolename はそれぞれ villager | seer | medium | freemason | hunter | wolf | lunatic | fox

 