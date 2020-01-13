# ocr-snip 
A very simple screen caputer -> OCR script. 

# Platforms 
Debian 8 but any linux machine should be able to run it with all dependencies. Could support this on windows but I don't feel like writing a google OCR isntaller and other custom windows code for a one nighter projct. 

# Dependencies 
* Python 
* tkinter
* pytesseract 
* Googles tesseract OCR engine 
* Python Image Library (PIL)
* pyqt 

# install 
```sh
git clone https://www.github.com/wamadahama/ocr-snip
cd ocr-snip
sudo ./install.sh
python snip.py
```

# Moving forward 
* My own OCR algorithm 
* More than QT bindings
* Draw an actual box during selection 
