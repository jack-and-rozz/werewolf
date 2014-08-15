
##### ログファイルの管理(./werewolf/log_manager)
* ログファイルの整型
`python log_manager -parse [srcfilename] [destfilename]`
./log_manager/logfiles内のわかめての村ログをパース可能。

* 学習処理
`python log_manager -learn`
主な用語についてと、適当に選んだ形態素についての各役職のスコアが表示される。

* 役職当てテスト
`python log_manager -infer [rolename]`
学習に使用していない村ログの各役職の発言データからの役職当てテストが出来る。rolename はそれぞれ villager | seer | medium | freemason | hunter | wolf | lunatic | fox

 