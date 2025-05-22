import sys
from PyQt5 import QtWidgets
from Ui_sorubankasıgiriş import Ui_MainWindow
from Ui_YeniSoruEkleEkranı import Ui_YeniSoruEkle
from Ui_SoruSeçEkranı import Ui_soru_bankasindan_soru_secimi
from database import DatabaseManager
import pandas as pd
from PyQt5.QtWidgets import QFileDialog, QMessageBox

class window(QtWidgets.QMainWindow):
    def __init__(self):
        super(window,self).__init__()

        self.db = DatabaseManager()



        self.ui=Ui_MainWindow()
        self.ui.setupUi(self)

        self.ui.yenisoruekle.triggered.connect(self.soruEkle)
        self.ui.sorusec.triggered.connect(self.soruSec)

    def soruEkle(self):
        self.ai = QtWidgets.QWidget()  # QWidget oluşturuyoruz
        self.ui_soruekle_1 = Ui_YeniSoruEkle()  # Ui_Form1'i oluşturuyoruz
        self.ui_soruekle_1.setupUi(self.ai)  # Form1'i QWidget'e yerleştiriyoruz

        self.ai.show()

        self.ui_soruekle_1.pushButton_1.clicked.connect(self.ekle) #giriş ekranı table ekleme.
        self.ui_soruekle_1.pushButton.clicked.connect(self.excelkaydet)


    def soruSec(self):
        # Yeni pencereyi oluştur ve referansını sınıf içinde tut
        self.pencere_sorusec = QtWidgets.QWidget()
        self.ui_sorusecimi_1 = Ui_soru_bankasindan_soru_secimi()
        self.ui_sorusecimi_1.setupUi(self.pencere_sorusec)

        # Pencereyi göster
        self.pencere_sorusec.show()

        # Verileri veritabanından çek
        try:
            data = self.db.connection.execute(
                "SELECT id, soru, secenekA, secenekB, secenekC, secenekD, secenekE FROM sorular"
            ).fetchall()
        except Exception as e:
            QtWidgets.QMessageBox.critical(self, "Hata", f"Veritabanı hatası:\n{e}")
            return

        # Tabloya verileri yerleştir
        table = self.ui_sorusecimi_1.tableWidget
        table.setRowCount(0)
        table.setColumnCount(7)
        table.setHorizontalHeaderLabels(["ID", "Soru", "A", "B", "C", "D", "E"])

        for row_data in data:
            row_position = table.rowCount()
            table.insertRow(row_position)
            for col, item in enumerate(row_data):
                table.setItem(row_position, col, QtWidgets.QTableWidgetItem(str(item)))

        self.ui_sorusecimi_1.pushButton_2.clicked.connect(self.baziexcelkaydet)
         

    def ekle(self):
        soru = self.ui_soruekle_1.textEdit.toPlainText()
        secenekA = self.ui_soruekle_1.lineEdit_1.text()
        secenekB = self.ui_soruekle_1.lineEdit_2.text()
        secenekC = self.ui_soruekle_1.lineEdit_3.text()
        secenekD = self.ui_soruekle_1.lineEdit_4.text()
        secenekE = self.ui_soruekle_1.lineEdit_5.text()

        # Doğru cevabı radio button'lardan al
        if self.ui_soruekle_1.radioButton_1.isChecked():
            dogru_cevap = "A"
        elif self.ui_soruekle_1.radioButton_2.isChecked():
            dogru_cevap = "B"
        elif self.ui_soruekle_1.radioButton_4.isChecked():
            dogru_cevap = "C"
        elif self.ui_soruekle_1.radioButton_5.isChecked():
            dogru_cevap = "D"
        elif self.ui_soruekle_1.radioButton_6.isChecked():
            dogru_cevap = "E"
        else:
            dogru_cevap = "Belirtilmedi"

        # Tabloya ekleme
        table = self.ui_soruekle_1.tableWidget
        row_position = table.rowCount()
        table.insertRow(row_position)

        table.setItem(row_position, 0, QtWidgets.QTableWidgetItem(soru))
        table.setItem(row_position, 1, QtWidgets.QTableWidgetItem(secenekA))
        table.setItem(row_position, 2, QtWidgets.QTableWidgetItem(secenekB))
        table.setItem(row_position, 3, QtWidgets.QTableWidgetItem(secenekC))
        table.setItem(row_position, 4, QtWidgets.QTableWidgetItem(secenekD))
        table.setItem(row_position, 5, QtWidgets.QTableWidgetItem(secenekE))
        table.setItem(row_position, 6, QtWidgets.QTableWidgetItem(dogru_cevap))

        self.db.soru_ekle(soru, secenekA, secenekB, secenekC, secenekD, secenekE, dogru_cevap)

        # Alanları temizle
        self.ui_soruekle_1.textEdit.clear()
        self.ui_soruekle_1.lineEdit_1.clear()
        self.ui_soruekle_1.lineEdit_2.clear()
        self.ui_soruekle_1.lineEdit_3.clear()
        self.ui_soruekle_1.lineEdit_4.clear()
        self.ui_soruekle_1.lineEdit_5.clear()
        self.ui_soruekle_1.radioButton_1.setChecked(False)
        self.ui_soruekle_1.radioButton_2.setChecked(False)
        self.ui_soruekle_1.radioButton_4.setChecked(False)
        self.ui_soruekle_1.radioButton_5.setChecked(False)
        self.ui_soruekle_1.radioButton_6.setChecked(False)
            
    def excelkaydet(self):

        # Veritabanından verileri çek
        df = self.db.dataframe_olarak_getir()

        # Kaydedilecek yeri kullanıcıdan seçmesini iste
        dosya_yolu, _ = QFileDialog.getSaveFileName(None, "Excel Dosyası Kaydet", "", "Excel Dosyası (*.xlsx)")

        if dosya_yolu:
            try:
                df.to_excel(dosya_yolu, index=False)
                QMessageBox.information(None, "Başarılı", "Veriler başarıyla Excel dosyasına kaydedildi.")
            except Exception as e:
                QMessageBox.critical(None, "Hata", f"Kaydetme sırasında bir hata oluştu:\n{e}")

    def baziexcelkaydet(self):
        table = self.ui_sorusecimi_1.tableWidget
        selected_rows = table.selectionModel().selectedRows()

        if not selected_rows:
            QMessageBox.warning(None, "Uyarı", "Lütfen en az bir soru seçin.")
            return

        sorular_listesi = []
        for row_index in selected_rows:
            row = row_index.row()
            soru = table.item(row, 1).text()
            secenekA = table.item(row, 2).text()
            secenekB = table.item(row, 3).text()
            secenekC = table.item(row, 4).text()
            secenekD = table.item(row, 5).text()
            secenekE = table.item(row, 6).text()
            sorular_listesi.append({
                "Soru": soru,
                "A": secenekA,
                "B": secenekB,
                "C": secenekC,
                "D": secenekD,
                "E": secenekE
            })

        # Excel'e kaydetme
        dosya_yolu, _ = QFileDialog.getSaveFileName(None, "Excel Dosyası Kaydet", "", "Excel Dosyası (*.xlsx)")

        if dosya_yolu:
            try:
                df = pd.DataFrame(sorular_listesi)
                df.to_excel(dosya_yolu, index=False)
                QMessageBox.information(None, "Başarılı", "Seçilen sorular başarıyla Excel'e aktarıldı.")
            except Exception as e:
                QMessageBox.critical(None, "Hata", f"Excel kaydı başarısız: {e}")


def app():
    app = QtWidgets.QApplication(sys.argv)
    screen = window()
    screen.show()
    sys.exit(app.exec_())
app()