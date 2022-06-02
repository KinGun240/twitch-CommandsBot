# パラメーター項目 ###########################
# 配信Start/Stopコマンド(streamStart/streamStop) ----------
# モデレーター権限を持つユーザーだけに限定させたい場合は、start_isModOnly/stop_isModOnlyをTrueに設定してください
start_isModOnly = True
stop_isModOnly = True

# シーン変更コマンド(sceneXX) ----------
# モデレーター権限を持つユーザーだけに限定させたい場合は、scene_isModOnlyをTrueに設定してください
# sceneXXに変更対象のシーン名を入力してください
scene_isModOnly = True
scene01 = "----------"
scene02 = "----------"

# 音量変更コマンド(volXX) ----------
# モデレーター権限を持つユーザーだけに限定させたい場合は、vol_isModOnlyをTrueに設定してください
# vol_sourceXXに変更対象のソース名を入力してください
vol_isModOnly = True
vol_source01 = "----------"
vol_source02 = "----------"

# ソース移動・拡大縮小コマンド(moveXX) ----------
# モデレーター権限を持つユーザーだけに限定させたい場合は、move_isModOnlyをTrueに設定してください
# move_sourceXXに変更対象のソース名を入力してください
# move_sourceXX_xpos・move_sourceXX_yposに、必要であれば優先される(x,y)座標位置を入力してください
# 　本項目でxposとyposを入力した場合は、コマンドでの入力よりもこちらの値が優先されます
move_isModOnly = True
move_source01 = "----------"
move_source01_xpos = ""
move_source01_ypos = ""
move_source02 = "----------"
move_source02_xpos = ""
move_source02_ypos = ""

# ソースON/OFFコマンド(onoffXX) ----------
# モデレーター権限を持つユーザーだけに限定させたい場合は、onoff_isModOnlyをTrueに設定してください
# onoff_sourceXXに変更対象のソース名を入力してください
onoff_isModOnly = True
onoff_source01 = "----------"
onoff_source02 = "----------"
