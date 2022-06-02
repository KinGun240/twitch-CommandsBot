from twitchio.ext import commands
from obswebsocket import obsws, requests

from shutil import rmtree
import os
import glob
import importlib
import sys
import signal
import time
import numpy as np

isDebug = False

# バージョン
ver = '1.1.1'

# 各種初期設定 #####################################
# bot用コンフィグの読み込み
try:
    sys.path.append(os.path.join(os.path.dirname(__file__), '.'))
    configCommands = importlib.import_module('config')
    print("Read config.py")
    # remove "#" mark
    if configCommands.Twitch_Channel.startswith('#'):
        print(" - Find # mark at channel name! I remove '#' from 'config:Twitch_Channel'")
        configCommands.Twitch_Channel = configCommands.Twitch_Channel[1:]
    # remove "oauth:" mark
    if configCommands.Trans_OAUTH.startswith('oauth:'):
        print(" - Find 'oauth:' at OAUTH text! I remove 'oauth:' from 'config:Trans_OAUTH'")
        configCommands.Trans_OAUTH = configCommands.Trans_OAUTH[6:]
except Exception as e:
    print(e)
    print('Please make [config.py] and put it with Commandsbot')
    input()  # stop for error!!


# botの初期化
try:
    commandsBot = commands.Bot(
        irc_token="oauth:" + configCommands.Trans_OAUTH,
        client_id=configCommands.CLIENT_ID,
        nick=configCommands.Trans_Username,
        prefix=configCommands.BOT_PREFIX,
        initial_channels=[configCommands.Twitch_Channel]
    )
except Exception as e:
    print(e)
    print('Please check [config.py]')
    input()  # stop for error!!


# obs-websocket初期化
try:
    ws = obsws(
        host=configCommands.Host,
        port=configCommands.Port,
        password=configCommands.Password
    )
except Exception as e:
    print(e)
    print('Please check [config.py]')
    input()  # stop for error!!


# obsCommands用パラメーターの読み込み
try:
    obsCommands = importlib.import_module('param_commandsBot')
    print("Read param_obsCommands.py")
except Exception as e:
    print(e)
    print('Please make [param_commandsBot.py] and put it with Commandsbot')
    input()  # stop for error!!


# bot処理 #####################################
# bot起動時処理
@commandsBot.event
async def event_ready():
    print(f"{configCommands.Trans_Username}がオンラインになりました!")
    # this is only needed to send messages within event_ready
    botws = commandsBot._ws
    await botws.send_privmsg(configCommands.Twitch_Channel, f"/color {configCommands.TextColor}")
    await botws.send_privmsg(configCommands.Twitch_Channel, "/me accepts command!")


# helloコマンド処理 ----------
@commandsBot.command()
async def hello(ctx):
    await ctx.send(f'{ctx.author.name}さん こんにちは～ KonCha')
    time.sleep(1)


# botコマンド処理 ----------
@commandsBot.command()
async def bot(ctx):
    implemented = '''
    streamStart、
    streamStop、
    scene、
    vol、
    move、
    onoff
    '''
    await ctx.send('実装済のコマンドは以下のとおりです' + implemented)
    time.sleep(1)


# 配信Start/Stopコマンド処理 ----------
# 入力値エラーチェック
def errorCheck_start(ctx):
    if obsCommands.start_isModOnly:
        if not ctx.author.is_mod:
            return 'isMod'
    return 'True'


def errorCheck_stop(ctx):
    if obsCommands.stop_isModOnly:
        if not ctx.author.is_mod:
            return 'isMod'
    return 'True'


# コマンドstreamStart
@commandsBot.command()
async def streamStart(ctx):
    error = errorCheck_start(ctx)
    if error == 'isMod':
        print(f"streamStart:ユーザー({ctx.author.name})はモデレーター権限を持っていません")
        await ctx.send('すみません、モデレーター権限が無いと実行できません FBBlock')
    if error != 'True':
        return

    result = ws.call(requests.StartStreaming())
    if result.status:
        print("streamStart:Streamを開始しました")
    else:
        print("streamStart:Streamの開始に失敗しました")
        print('Please check [param_commandsBot.py]')
    time.sleep(5)


# コマンドstreamStop
@commandsBot.command()
async def streamStop(ctx):
    error = errorCheck_stop(ctx)
    if error == 'isMod':
        print(f"streamStop:ユーザー({ctx.author.name})はモデレーター権限を持っていません")
        await ctx.send('すみません、モデレーター権限が無いと実行できません FBBlock')
    if error != 'True':
        return

    result = ws.call(requests.StopStreaming())
    if result.status:
        print("streamStop:Streamを停止しました")
    else:
        print("streamStop:Streamの停止に失敗しました")
        print('Please check [param_commandsBot.py]')
    time.sleep(5)


# シーン変更コマンド処理 ----------
# 入力値エラーチェック
def errorCheck_scene(ctx):
    if obsCommands.scene_isModOnly:
        if not ctx.author.is_mod:
            return 'isMod'
    return 'True'


# シーン変更実行
def changeScene(scene):
    return ws.call(requests.SetCurrentScene(scene))


# コマンドscene01
@commandsBot.command()
async def scene01(ctx):
    error = errorCheck_scene(ctx)
    if error == 'isMod':
        print(f"scene01:ユーザー({ctx.author.name})はモデレーター権限を持っていません")
        await ctx.send('すみません、モデレーター権限が無いと実行できません FBBlock')
    if error != 'True':
        return

    scene = obsCommands.scene01
    result = changeScene(scene)
    if result.status:
        print(f"scene01:シーンを({scene})に変更しました")
    else:
        print(f"scene01:シーン({scene})の変更に失敗しました")
        print('Please check [param_commandsBot.py]')
    time.sleep(5)


# コマンドscene02
@commandsBot.command()
async def scene02(ctx):
    error = errorCheck_scene(ctx)
    if error == 'isMod':
        print(f"scene02:ユーザー({ctx.author.name})はモデレーター権限を持っていません")
        await ctx.send('すみません、モデレーター権限が無いと実行できません FBBlock')
    if error != 'True':
        return

    scene = obsCommands.scene02
    result = changeScene(scene)
    if result.status:
        print(f"scene02:シーンを({scene})に変更しました")
    else:
        print(f"scene02:シーン({scene})の変更に失敗しました")
        print('Please check [param_commandsBot.py]')
    time.sleep(5)


# ソース音量変更コマンド処理 ----------
# 入力値エラーチェック
def errorCheck_vol(ctx, args, volume):
    if len(args) < 1:
        return 'shortInputs'
    if obsCommands.vol_isModOnly:
        if not ctx.author.is_mod:
            return 'isMod'
    if not volume.isdecimal():
        return 'isDecimal'
    if int(volume) < 0 or int(volume) > 1000:
        return 'isRange'
    return 'True'


# ソース音量変更実行
def changeVolume(source, volume):
    if volume == 0:
        dB = -99.9
    else:
        dB = db(volume / 100, 1)

    return ws.call(requests.SetVolume(source, dB, True))


# コマンドvol01
@commandsBot.command()
async def vol01(ctx, *args):
    volume = 'None'
    count = 0
    for inputs in args:
        count += 1
        if count == 1:
            volume = inputs
            continue
    print(f"入力volume({type(volume)}, {volume})")
    error = errorCheck_vol(ctx, args, volume)
    if error == 'shortInputs':
        print(f"vol01:入力args({args})が少なすぎます")
        await ctx.send('volumeが入力されていません FBBlock')
    elif error == 'isMod':
        print(f"vol01:ユーザー({ctx.author.name})はモデレーター権限を持っていません")
        await ctx.send('すみません、モデレーター権限が無いと実行できません FBBlock')
    elif error == 'isDecimal':
        print("vol01:入力volumeは正の十進数字ではありません")
        await ctx.send('volumeが数値でありません FBBlock')
    elif error == 'isRange':
        print("vol01:入力volumeが0以上1000以下の値ではありません")
        await ctx.send('volumeの値が範囲を超えています FBBlock')
    if error != 'True':
        return

    source = obsCommands.vol_source01
    result = changeVolume(source, int(volume))
    if result.status:
        print(f"vol01:ソース({source})の音量を{volume}[%]に変更しました")
    else:
        print(f"vol01:ソース({source})の音量{volume}[%]への変更に失敗しました")
        print('Please check [param_commandsBot.py]')
    time.sleep(3)


# コマンドvol02
@commandsBot.command()
async def vol02(ctx, *args):
    volume = 'None'
    count = 0
    for inputs in args:
        count += 1
        if count == 1:
            volume = inputs
            continue
    print(f"入力:volume({type(volume)}, {volume})")
    error = errorCheck_vol(ctx, args, volume)
    if error == 'shortInputs':
        print(f"vol02:入力args({args})が少なすぎます")
        await ctx.send('volumeが入力されていません FBBlock')
    elif error == 'isMod':
        print(f"vol02:ユーザー({ctx.author.name})はモデレーター権限を持っていません")
        await ctx.send('すみません、モデレーター権限が無いと実行できません FBBlock')
    elif error == 'isDecimal':
        print(f"vol02:入力volume({volume})は正の十進数字ではありません")
        await ctx.send('volumeが数値でありません FBBlock')
    elif error == 'isRange':
        print(f"vol02:入力volume({volume})が0以上1000以下の値ではありません")
        await ctx.send('volumeの値が範囲を超えています FBBlock')
    if error != 'True':
        return

    source = obsCommands.vol_source02
    result = changeVolume(source, volume)
    if result.status:
        print(f"vol02:ソース({source})の音量を({volume})[%]に変更しました")
    else:
        print(f"vol02:ソース({source})の音量({volume})[%]への変更に失敗しました")
        print('Please check [param_commandsBot.py]')
    time.sleep(3)


# ソース移動・縮小拡大コマンド処理 ----------
# 入力値エラーチェック
def errorCheck_move(ctx, args, xpos, ypos, xscale, yscale, rot):
    if len(args) < 2:
        return 'shortInputs'
    if obsCommands.move_isModOnly:
        if not ctx.author.is_mod:
            return 'isMod'
    if not xpos.isdecimal() or not ypos.isdecimal():
        return 'isDecimal'
    if not is_num(xscale) or not is_num(yscale) or not is_num(rot):
        return 'isNum'
    return 'True'


# ソース移動実行
def moveSource(source, xpos, ypos):
    return ws.call(requests.SetSceneItemPosition(source, int(xpos), int(ypos)))


# ソース縮小拡大実行
def scaleSource(source, xscale, yscale, rot):
    srouceInfo = ws.call(requests.GetSceneItemProperties(source))
    scale = srouceInfo.getScale()
    if xscale == 0.0:
        xscale = scale['x']
    if yscale == 0.0:
        yscale = scale['y']

    return ws.call(requests.SetSceneItemTransform(source, float(xscale), float(yscale), int(rot)))


# コマンドmove01
@commandsBot.command()
async def move01(ctx, *args):
    xpos = 'None'
    ypos = 'None'
    xscale = '0.0'
    yscale = '0.0'
    rot = '0.0'
    count = 0
    for inputs in args:
        count += 1
        if count == 1:
            xpos = inputs
            continue
        if count == 2:
            ypos = inputs
            continue
        if count == 3:
            xscale = inputs
            continue
        if count == 4:
            yscale = inputs
            continue
        if count == 5:
            rot = inputs
            continue
    print(f"入力:xpos({type(xpos)}, {xpos}), ypos({type(ypos)}, {ypos})")
    print(
        f"入力:xscale({type(xscale)}, {xscale}), yscale({type(yscale)}, {yscale}), rot({type(rot)}, {rot})")
    error = errorCheck_move(ctx, args, xpos, ypos, xscale, yscale, rot)
    if error == 'shortInputs':
        print(f"move01:入力args({args})が少なすぎます")
        await ctx.send('xposまたはyposが入力されていません FBBlock')
    elif error == 'isMod':
        print(f"move01:ユーザー({ctx.author.name})はモデレーター権限を持っていません")
        await ctx.send('すみません、モデレーター権限が無いと実行できません FBBlock')
    elif error == 'isDecimal':
        print(f"move01:入力xpos,ypos({xpos}or{ypos})は正の十進数字ではありません")
        await ctx.send('xposまたはyposが数値ではありません FBBlock')
    elif error == 'isNum':
        print(
            f"move01:入力xscale,yscale,rot({xscale}or{yscale}or{rot})が数値ではありません")
        await ctx.send('xscaleまたはyscaleまたはrotが数値ではありません FBBlock')
    if error != 'True':
        return

    source = obsCommands.move_source01
    if obsCommands.move_source01_xpos:
        xpos = obsCommands.move_source01_xpos
    if obsCommands.move_source01_ypos:
        ypos = obsCommands.move_source01_ypos
    result = moveSource(source, xpos, ypos)
    if result.status:
        print(f"move01:ソース({source})を({xpos},{ypos})に移動しました")
    else:
        print(f"move01:ソース({source})の({xpos},{ypos})への移動に失敗しました")
        print('Please check [param_commandsBot.py]')
    if xscale != '0.0' or yscale != '0.0' or rot != '0.0':
        result = scaleSource(source, float(xscale), float(yscale), float(rot))
        if result.status:
            print(
                f"move01:ソース({source})を({xscale},{yscale})に拡大縮小、({rot})度に角度変更しました")
        else:
            print(
                f"move01:ソース({source})の({xscale},{yscale})への拡大縮小・({rot})度への角度変更に失敗しました")
            print('Please check [param_commandsBot.py]')
    time.sleep(3)


# コマンドmove02
@commandsBot.command()
async def move02(ctx, *args):
    xpos = 'None'
    ypos = 'None'
    xscale = '0.0'
    yscale = '0.0'
    rot = '0.0'
    count = 0
    for inputs in args:
        count += 1
        if count == 1:
            xpos = inputs
            continue
        if count == 2:
            ypos = inputs
            continue
        if count == 3:
            xscale = inputs
            continue
        if count == 4:
            yscale = inputs
            continue
        if count == 5:
            rot = inputs
            continue
    print(f"入力:xpos({type(xpos)}, {xpos}), ypos({type(ypos)}, {ypos})")
    print(
        f"入力:xscale({type(xscale)}, {xscale}), yscale({type(yscale)}, {yscale}), rot({type(rot)}, {rot})")
    error = errorCheck_move(ctx, args, xpos, ypos, xscale, yscale, rot)
    if error == 'shortInputs':
        print(f"move02:入力args({args})が少なすぎます")
        await ctx.send('xposまたはyposが入力されていません FBBlock')
    elif error == 'isMod':
        print(f"move02:ユーザー({ctx.author.name})はモデレーター権限を持っていません")
        await ctx.send('すみません、モデレーター権限が無いと実行できません FBBlock')
    elif error == 'isDecimal':
        print(f"move02:入力xpos,ypos({xpos}or{ypos})は正の十進数字ではありません")
        await ctx.send('xposまたはyposが数値ではありません FBBlock')
    elif error == 'isNum':
        print(
            f"move02:入力xscale,yscale,rot({xscale}or{yscale}or{rot})が数値ではありません")
        await ctx.send('xscaleまたはyscaleまたはrotが数値ではありません FBBlock')
    if error != 'True':
        return

    source = obsCommands.move_source02
    if obsCommands.move_source02_xpos:
        xpos = obsCommands.move_source02_xpos
    if obsCommands.move_source02_ypos:
        ypos = obsCommands.move_source02_ypos
    result = moveSource(source, xpos, ypos)
    if result.status:
        print(f"move02:ソース({source})を({xpos},{ypos})に移動しました")
    else:
        print(f"move02:ソース({source})の({xpos},{ypos})への移動に失敗しました")
        print('Please check [param_commandsBot.py]')
    if xscale != '0.0' or yscale != '0.0' or rot != '0.0':
        result = scaleSource(source, float(xscale), float(yscale), float(rot))
        if result.status:
            print(
                f"move02:ソース({source})を({xscale},{yscale})に拡大縮小、({rot})度に角度変更しました")
        else:
            print(
                f"move02:ソース({source})の({xscale},{yscale})への拡大縮小・({rot})度への角度変更に失敗しました")
            print('Please check [param_commandsBot.py]')
    time.sleep(3)


# ソースON/OFFコマンド処理 ----------
# 入力値エラーチェック
def errorCheck_onoff(ctx, args, set):
    if len(args) < 1:
        return 'shortInputs'
    if obsCommands.onoff_isModOnly:
        if not ctx.author.is_mod:
            return 'isMod'
    if not (set == 'ON' or set == 'OFF'):
        return 'isONOFF'
    return 'True'


# 表示変更実行
def changeVisible(item, set):
    if set == 'ON':
        visible = True
    elif set == 'OFF':
        visible = False
    else:
        return
    return ws.call(requests.SetSceneItemProperties(item, visible=visible))


# コマンドonoff01
@commandsBot.command()
async def onoff01(ctx, *args):
    set = 'None'
    count = 0
    for inputs in args:
        count += 1
        if count == 1:
            set = inputs
            continue
    print(f"入力:set({type(set)}, {set})")
    error = errorCheck_onoff(ctx, args, set)
    if error == 'shortInputs':
        print(f"onoff01:入力args({args})が少なすぎます")
        await ctx.send('setが入力されていません FBBlock')
    elif error == 'isMod':
        print(f"onoff01:ユーザー({ctx.author.name})はモデレーター権限を持っていません")
        await ctx.send('すみません、モデレーター権限が無いと実行できません FBBlock')
    elif error == 'isONOFF':
        print(f"onoff01:入力({set})は'ON'または'OFF'ではありません")
        await ctx.send('setが既定の値ではありません FBBlock')
    if error != 'True':
        return

    source = obsCommands.onoff_source01
    result = changeVisible(source, set)
    if result.status:
        print(f"onoff01:ソース({source})を({set})にしました")
    else:
        print(f"onoff01:ソース({source})の({set})への表示変更に失敗しました")
        print('Please check [param_commandsBot.py]')
    time.sleep(3)


# コマンドonoff02
@commandsBot.command()
async def onoff02(ctx, *args):
    set = 'None'
    count = 0
    for inputs in args:
        count += 1
        if count == 1:
            set = inputs
            continue
    print(f"入力:set({type(set)}, {set})")
    error = errorCheck_onoff(ctx, args, set)
    if error == 'shortInputs':
        print(f"onoff02:入力args({args})が少なすぎます")
        await ctx.send('setが入力されていません FBBlock')
    elif error == 'isMod':
        print(f"onoff02:ユーザー({ctx.author.name})はモデレーター権限を持っていません")
        await ctx.send('すみません、モデレーター権限が無いと実行できません FBBlock')
    elif error == 'isONOFF':
        print(f"onoff02:入力({set})は'ON'または'OFF'ではありません")
        await ctx.send('setが既定の値ではありません FBBlock')
    if error != 'True':
        return

    source = obsCommands.onoff_source02
    result = changeVisible(source, set)
    if result.status:
        print(f"onoff02:ソース({source})を({set})にしました")
    else:
        print(f"onoff02:ソース({source})の({set})への表示変更に失敗しました")
        print('Please check [param_commandsBot.py]')
    time.sleep(3)


# 汎用関数 #####################################
# 数値か否かを判定する
def is_num(s):
    try:
        float(s)
    except ValueError:
        return False
    else:
        return True


# リニア値からdBへ変換
def db(x, dBref):
    y = 20 * np.log10(x / dBref)  # 変換式
    return y  # dB値を返す


# dB値からリニア値へ変換
def idb(x, dBref):
    y = dBref * np.power(10, x / 20)  # 変換式
    return y


#####################################
# sig handler  -------------
def sig_handler(signum, frame) -> None:
    sys.exit(1)


#####################################
# _MEI cleaner  -------------
# Thanks to Sadra Heydari
# @ https://stackoverflow.com/questions/57261199/python-handling-the-meipass-folder-in-temporary-folder
def CLEANMEIFOLDERS():
    try:
        base_path = sys._MEIPASS

    except Exception:
        base_path = os.path.abspath(".")

    if isDebug:
        print(f'_MEI base path: {base_path}')
    base_path = base_path.split("\\")
    base_path.pop(-1)
    temp_path = ""
    for item in base_path:
        temp_path = temp_path + item + "\\"

    mei_folders = [f for f in glob.glob(temp_path + "**/", recursive=False)]
    for item in mei_folders:
        if item.find('_MEI') != -1 and item != sys._MEIPASS + "\\":
            rmtree(item)


#####################################
# 最後のクリーンアップ処理 -------------
def cleanup():
    print("!!!Clean up!!!")

    # Cleanup処理いろいろ

    # time.sleep(1)
    print("!!!Clean up Done!!!")


# メイン処理 ###########################
def main():
    signal.signal(signal.SIGTERM, sig_handler)

    try:
        # 以前に生成された _MEI フォルダを削除する
        CLEANMEIFOLDERS()

        # obsws
        ws.connect()
        print("Connected obs-websocket")

        # commandsBot(obswsの起動後に実行)
        commandsBot.run()

    except Exception as e:
        if isDebug:
            print(e)
        input()  # stop for error!!

    finally:
        ws.disconnect()
        print("Disconnected obs-websocket")
        signal.signal(signal.SIGTERM, signal.SIG_IGN)
        signal.signal(signal.SIGINT, signal.SIG_IGN)
        cleanup()
        signal.signal(signal.SIGTERM, signal.SIG_DFL)
        signal.signal(signal.SIGINT, signal.SIG_DFL)


if __name__ == "__main__":
    sys.exit(main())
