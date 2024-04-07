import os
import PySimpleGUI as sg
import pyperclip
import numpy as np
from PIL import Image
import pyocr
import pyocr.builders
import io

sg.theme('SystemDefault1')

path_tesseract = './Tesseract-OCR' #Tesseractの呼び出し
if path_tesseract not in os.environ["PATH"].split(os.pathsep):
    os.environ["PATH"] += os.pathsep + path_tesseract
tools = pyocr.get_available_tools() #PyOCRで使えるエンジンを取得する
tool = tools[0] #最初のエンジンを使用

supported_file = ('.png', '.jpg', '.jpeg', '.tiff', '.bmp') #サポートする拡張子

layout = [[sg.InputText(key=('path')), sg.FolderBrowse(key="file1"), sg.Button('Load'), sg.Text(key='filepath')],
        [sg.Image('./blank.png', key='image'), sg.Multiline(key='notepad', enable_events=True, default_text='', pad=((0,0),(0,0)), size=(40,40))],
        [sg.Button('<-'), sg.Text('0 / 0', key='number'), sg.Button('->'), sg.Button('OCR'),sg.Button('Copy'), sg.Button('Save'), 
         sg.Radio('日本語(横書き)', group_id='languages', default=True, key='jpn'), sg.Radio('日本語(縦書き)', group_id='languages', key='jpn_vert'), 
         sg.Radio('简体中文(横写)', group_id='languages', key='chi_sim'), sg.Radio('简体中文(竖写)', group_id='languages', key='chi_sim_vert'),
         sg.Radio('繁體中文(橫寫)', group_id='languages', key='chi_tra'), sg.Radio('繁體中文(豎寫)', group_id='languages', key='chi_tra_vert'), 
        sg.Radio('English', group_id='languages', key='eng')]
]

window = sg.Window('OCREditor Powered by Tesseract', layout, location=(0, 0), use_default_focus=False)

i = 0 #iの値をリセット
while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED: #xボタンを押すとプログラムを終了する
        break

    if event == 'Load':
        folder = values['path'] #フォルダパスを取得する
        if folder == '':
            continue #フォルダパスが取得されなかった場合は最初の画面に戻す
        try:
            folder
        except NameError:
            continue #フォルダパスを取得していない場合の例外処理
        else:
            get_directory = os.listdir(folder) #ファイルのディレクトリを取得する
            file_list = [f for f in get_directory if os.path.isfile(os.path.join(folder, f)) and f.lower().endswith(supported_file)] #supported_fileの拡張子と合致したファイルのみでリストを作成する
            num_files = len(file_list) #フォルダに含まれるファイルの数を取得する
            if num_files == 0:
                sg.popup_error('File does not exist in folder!')
                continue #ファイル数が0の場合は最初の画面に戻す
            del get_directory  #必要ないため関数を消去
            file_name = os.path.join(folder, file_list[i])
            img = Image.open(file_name)
            thumbnail_size = (1000, 650)
            img.thumbnail(thumbnail_size) #サムネイル画像のサイズを1000*650に制限する
            binary = io.BytesIO() #画像をバイナリデータに変換する
            img.save(binary, format="PNG") #バイナリデータをPNG画像に変換
            del img #メモリ上から画像データを削除
            thumbnail_data = binary.getvalue()
            window['image'].update(data=thumbnail_data) #サムネイルを更新
            window['number'].update('{} / {}'.format(i+1, num_files)) #フォルダの中で画像ファイルが何枚目か更新する
            window['filepath'].update(file_name) #ファイル名を更新する

    if event in ('<-'):
        try:
            num_files
        except NameError:
            continue #フォルダパスを取得していない場合の例外処理
        else:
            i = i + 1
            if i >= num_files:
                i = i - num_files #先頭の数値を代入
            file_name = os.path.join(folder, file_list[i])
            img = Image.open(file_name)
            thumbnail_size = (1000, 650)
            img.thumbnail(thumbnail_size) #サムネイル画像のサイズを1000*650に制限する
            binary = io.BytesIO() #画像をバイナリデータに変換する
            img.save(binary, format="PNG") #バイナリデータをPNG画像に変換
            del img #メモリ上から画像データを削除
            thumbnail_data = binary.getvalue()
            window['image'].update(data=thumbnail_data) #サムネイルを更新
            window['number'].update('{} / {}'.format(i+1, num_files)) #フォルダの中で画像ファイルが何枚目か更新する
            window['filepath'].update(file_name) #ファイル名を更新する
    elif event in ('->'):
        try:
            num_files
        except NameError:
            continue #フォルダパスを取得していない場合の例外処理
        else:
            i = i - 1
            if i < 0:
                i = num_files + i #最後尾の数値を代入
            file_name = os.path.join(folder, file_list[i])
            img = Image.open(file_name)
            thumbnail_size = (1000, 650)
            img.thumbnail(thumbnail_size) #サムネイル画像のサイズを1000*650に制限する
            binary = io.BytesIO() #画像をバイナリデータに変換する
            img.save(binary, format="PNG") #バイナリデータをPNG画像に変換
            del img #メモリ上から画像データを削除
            thumbnail_data = binary.getvalue()
            window['image'].update(data=thumbnail_data) #サムネイルを更新
            window['number'].update('{} / {}'.format(i+1, num_files)) #フォルダの中で画像ファイルが何枚目か更新する
            window['filepath'].update(file_name) #ファイル名を更新する
    else:
        pass

    if event == 'OCR':
        try:
            file_name
        except NameError:
            continue
        else:
            ocr_img = np.array(Image.open(file_name).convert('L'), 'f') #画像をグレースケール、かつfloat型にして呼び出す
            ocr_img = (ocr_img > 128) * 255 #二値化処理を行う（閾値は128）
            ocr_img = 255 - ocr_img #白黒反転処理を行う
            ocr_img = Image.fromarray(ocr_img) #PyOCRが読み込める形式に変換する
        
            #Tesseractのレイアウト指定→画像データからテキストを生成→テキストから空白を消去→テキストボックスに結果を出力
            if values['jpn'] == True:
                builder = pyocr.builders.TextBuilder(tesseract_layout=6) #日本語（横書き）のOCR
                result = tool.image_to_string(ocr_img, lang='jpn', builder=builder)
                result = result.replace(' ', '')
                window['notepad'].print(result)
            elif values['jpn_vert'] == True:
                builder = pyocr.builders.TextBuilder(tesseract_layout=5) #日本語（縦書き）のOCR
                result = tool.image_to_string(ocr_img, lang='jpn_vert', builder=builder)
                result = result.replace(' ', '')
                window['notepad'].print(result)
            elif values['chi_sim'] == True:
                builder = pyocr.builders.TextBuilder(tesseract_layout=6) #簡体字中国語（横書き）のOCR
                result = tool.image_to_string(ocr_img, lang='chi_sim', builder=builder)
                result = result.replace(' ', '')
                window['notepad'].print(result)
            elif values['chi_sim_vert'] == True:
                builder = pyocr.builders.TextBuilder(tesseract_layout=5) #簡体字中国語（縦書き）のOCR
                result = tool.image_to_string(ocr_img, lang='chi_sim_vert', builder=builder)
                result = result.replace(' ', '')
                window['notepad'].print(result)
            elif values['chi_tra'] == True:
                builder = pyocr.builders.TextBuilder(tesseract_layout=6) #繁体字中国語（横書き）のOCR
                result = tool.image_to_string(ocr_img, lang='chi_tra', builder=builder)
                result = result.replace(' ', '')
                window['notepad'].print(result)
            elif values['chi_tra_vert'] == True:
                builder = pyocr.builders.TextBuilder(tesseract_layout=5) #繁体字中国語（縦書き）のOCR
                result = tool.image_to_string(ocr_img, lang='chi_tra_vert', builder=builder)
                result = result.replace(' ', '')
                window['notepad'].print(result)
            else:
                builder = pyocr.builders.TextBuilder(tesseract_layout=6) #英語のOCR
                result = tool.image_to_string(ocr_img, lang='eng', builder=builder)
                result = result.replace(' ', '')
                window['notepad'].print(result)

    if event == 'Copy':
        copy_text = values['notepad']
        pyperclip.copy(copy_text) #テキストボックスのデータをクリップボードにコピー

    if event == 'Save':
        directory: str = sg.popup_get_folder('Select folder') #フォルダーを選択
        save_file_name: str = sg.popup_get_text('Enter file name') #ファイル名を入力
        if directory == '':
            continue
        elif save_file_name == '':
            continue
        else:
            file_path: str = directory + '/' + save_file_name + '.txt' #ディレクトリとファイル名を結合
            try:
                save_file = open(file_path, mode='w', encoding='UTF-8')
            except FileNotFoundError:
                continue #存在しないディレクトリを入力された際の例外処理
            else:
                save_file = open(file_path, mode='w', encoding='UTF-8') #簡体字・繁体字を出力するため文字コードにUTF-8を指定
                save_file.write(values['notepad']) #テキストボックスのデータをtxtファイルに出力
                save_file.close()

window.close()