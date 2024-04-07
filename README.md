# 【習作】OCREditor Powered by Tesseract
システムにPySimpleGUIとPyOCRを使用し、画像認識エンジンにTesseractを使用したOCRソフトウェアです。  
OCR技術への好奇心と、osライブラリに習熟するため作成しました。
<img width="995" alt="スクリーンショット 2024-04-07 193724" src="https://github.com/Flying-Fishcan/OCREditor-Powered-by-Tesseract/assets/147997884/eb465f8f-3375-4715-9918-737cef9640f7">
<img width="929" alt="スクリーンショット 2024-04-07 193811" src="https://github.com/Flying-Fishcan/OCREditor-Powered-by-Tesseract/assets/147997884/04ce10b1-f761-4f87-866e-48fefea7b6d2">
<img width="851" alt="スクリーンショット 2024-04-07 193855" src="https://github.com/Flying-Fishcan/OCREditor-Powered-by-Tesseract/assets/147997884/83eb7a1a-5803-43f9-a272-b04b0b1e05b5">
## 機能
画像データの文字列からテキストを生成（グレースケール化→二値科→白黒反転処理）  
日本語・英語・簡体字中国語・繁体字中国語の認識に対応
生成されたテキストをクリップボードにコピー    
生成されたテキストをtxtファイル形式で保存  
## 既知の不具合
言語を問わず、縦書きの文字列では低い認識精度である  
