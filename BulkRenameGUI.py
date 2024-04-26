import os
import re
import PyQt5

from PyQt5.QtGui import QStandardItemModel, QStandardItem
from PyQt5.QtWidgets import *
from PyQt5 import uic

os.environ['QT_AUTO_SCREEN_SCALE_FACTOR'] = '1'

class MyGUI(QMainWindow):

    def __init__(self):
        super(MyGUI, self).__init__()
        uic.loadUi('BulkRename.ui', self)
        self.show()


        self.directory = "."
        self.ListModel = QStandardItemModel()
        self.selectModel = QStandardItemModel()

        self.SelectView.setModel(self.selectModel)
        self.selected = []

        self.ActionOpen.triggered.connect(self.load_directory)
        self.FilterButton.clicked.connect(self.filter_list)
        self.SelectButton.clicked.connect(self.choose_selection)
        self.RemoveButton.clicked.connect(self.remove_selection)
        self.ApplyButton.clicked.connect(self.rename_files)



    def load_directory(self):
        self.directory = QFileDialog.getExistingDirectory(self, "Select Directory")
        for file in os.listdir(self.directory):
            if os.path.isfile(os.path.join(self.directory, file)):
                self.ListModel.appendRow(QStandardItem(file))

        self.ListView.setModel(self.ListModel)

    def rename_files(self):
        counter = 1
        for filename in self.selected:
            if self.AddPrefixRadio.isChecked():
                os.rename(os.path.join(self.directory, filename), os.path.join(self.directory, self.NameEdit.text() + filename))
                #os.rename(os.path.join(self.directory, filename), os.path.join(self.directory, self.NameEdit.text() + filename))
            elif self.RemovePrefixRadio.isChecked():
                if filename.startswith(self.NameEdit.text()):
                    os.rename(os.path.join(self.directory, filename), os.path.join(self.directory, self.filename[len(self.NameEdit.text()):]))
            elif self.AddSuffixRadio.isChecked():
                filetype = filename.split('.')[-1]
                os.rename(os.path.join(self.directory, filename), os.path.join(self.directory, filename[:(len(filetype) + 1)] + self.NameEdit.text()  + "." + filetype))
                #os.rename(os.path.join(self.directory, filename), os.path.join(self.directory, filename + self.NameEdit.text() + "." + filetype))
            elif self.RemoveSuffixRadio.isChecked():
                filetype = filename.split('.')[-1]
                if filename.endswith(self.NameEdit.text() + "." + filetype):
                    os.rename(os.path.join(self.directory, filename), os.path.join(self.directory, filename[:-len(self.NameEdit.text() + '.' + filetype)] + "." + filetype))
                    #os.rename(os.path.join(self.directory, filename), os.path.join(self.directory, filename[:-len(self.NameEdit.text() + '.' + filetype)] + "." + filetype))
            elif self.NewNameRadio.isChecked():
                filetype = filename.split('.')[-1]
                os.rename(os.path.join(self.directory, filename), os.path.join(self.directory, self.NameEdit.text() + str(counter) + "." + filetype))
                counter += 1
            else:
                print("Select a Radio Button!")

            self.selected = []
            self.selectModel.clear()
            self.ListModel.clear()


            for file in os.listdir(self.directory):
                if os.path.isfile(os.path.join(self.directory, file)):
                    self.ListModel.appendRow(QStandardItem(file))
            self.ListView.setModel(self.ListModel)





    def choose_selection(self):
        if len(self.ListView.selectedIndexes()) != 0:
            for index in self.ListView.selectedIndexes():
                if index.data() not in self.selected:
                    self.selected.append(index.data())
                    self.selectModel.appendRow(QStandardItem(index.data()))

    def remove_selection(self):
        if len(self.SelectView.selectedIndexes()) != 0:
            for index in reversed(sorted(self.SelectView.selectedIndexes())):
                self.selected.remove(index.data())
                self.selectModel.removeRow(index.row())




    def filter_list(self):
        self.selectModel.clear()
        self.selected = []
        for index in range(self.ListModel.rowCount()):
            item = self.ListModel.item(index)
            if re.match(self.FilterEdit.text(), item.text()):
                self.selectModel.appendRow(QStandardItem(item.text()))
                self.selected.append(item.text())





app = QApplication([])
window = MyGUI()
app.exec_()