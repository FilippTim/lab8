import cv2
import sys
from window import ImageWindow
from PyQt6.QtWidgets import QApplication, QFileDialog

save_process_path = 'stuff/saved/save_proc.jpg'
class Mywindow(ImageWindow):
    def __init__(self):
        super().__init__()
        self.initial_path = ''
        self.scale=1.8
        self.minNeighbors=3
    def on_button1_clicked(self):
        self.download_img(1)
        self.faces_recognition()
    def on_button_find_clicked(self):
        if self.inputScale.text():
            if float(self.inputScale.text())>1 and float(self.inputScale.text())<5:
                self.scale = float(self.inputScale.text())
        if self.inputNeigh.text():
            if int(self.inputNeigh.text())>1 and int(self.inputNeigh.text())<15:
                self.minNeighbors=int(self.inputNeigh.text())
        print(self.scale, '   ', self.minNeighbors)
        self.faces_recognition()
    def download_img(self, i):
        try:
            self.initial_path, _ = QFileDialog.getOpenFileName(self, "Выберите изображение", "", "Изображения (*.png *.jpg *.jpeg)")
            if not self.initial_path:
                raise FileNotFoundError("Путь к изображению не был выбран.")
            if i == 1:
                self.update_images1(self.initial_path)
            else:
                raise FileNotFoundError("Куда ты хочешь картинку?")
        except Exception as e:
            print("Ошибка при загрузке изображения", e)
            return None
    def faces_recognition(self):
        try:
            img = cv2.imread(self.initial_path)
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            faces = cv2.CascadeClassifier('faces.xml')
            results = faces.detectMultiScale(gray, scaleFactor=self.scale, minNeighbors=self.minNeighbors)
            for(x, y, w, h) in results:
                cv2.rectangle(img, (x,y),(w+x, y+h),(0,255,0), thickness=2)

            cv2.imwrite(save_process_path, img)
            self.update_images2(save_process_path)
        except Exception as e:
            print('Ошибка при попытке распознать лица: ')
            return None
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Mywindow()
    sys.exit(app.exec())
