"""
Prototype for a Qt list/dict editor

parameters: existing dict/list


TODO:
    add dynamic headers (e.g. 'age range' and 'file' for age-specific normal data)
    add option to use a file browser button instead of string editor (for dicts/lists of files)
    lists are ordered, so maybe should have numbers on left column
    use QListView instead of a grid layout?

"""

from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDialogButtonBox, QPushButton


class QCompoundEditor(QtWidgets.QDialog):

    def __init__(self, data, parent=None):
        super(QCompoundEditor, self).__init__(parent=parent)
        root_layout = QtWidgets.QVBoxLayout()
        self.datable = QtWidgets.QTableWidget()
        self.data = data
        self.list_mode = isinstance(data, list)
        # create the button box
        self.buttonbox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        insertbutton = QPushButton('Insert')
        deletebutton = QPushButton('Delete')
        self.buttonbox.addButton(insertbutton, QDialogButtonBox.ActionRole)
        self.buttonbox.addButton(deletebutton, QDialogButtonBox.ActionRole)
        insertbutton.clicked.connect(self._insert_item)
        deletebutton.clicked.connect(self._delete_item)
        self.buttonbox.accepted.connect(self.accept)
        self.buttonbox.rejected.connect(self.reject)
        self.datable = QtWidgets.QTableWidget()
        if self.list_mode:
            self._init_for_list()
        else:
            self._init_for_dict()
        root_layout.addWidget(self.datable)
        root_layout.addWidget(self.buttonbox)
        self.datable.resizeColumnsToContents()
        self.datable.setSelectionBehavior(QtWidgets.QTableView.SelectRows)
        self.setLayout(root_layout)

    def _init_for_dict(self):
        """Init table for dict data"""
        self.datable.setColumnCount(2)
        self.datable.setHorizontalHeaderLabels(['Key', 'Value'])
        #self.datable.setVerticalHeaderLabels()
        for k, (key, val) in enumerate(data.items()):
            key = str(key)
            self.datable.insertRow(k)
            self.datable.setItem(k, 0, QtWidgets.QTableWidgetItem(key))
            self.datable.setItem(k, 1, QtWidgets.QTableWidgetItem(val))

    def _init_for_list(self):
        """Init table for list data"""
        self.datable.setColumnCount(1)
        self.datable.setHorizontalHeaderLabels(['Value'])
        for k, val in enumerate(data):
            val = str(val)
            self.datable.insertRow(k)
            self.datable.setItem(k, 0, QtWidgets.QTableWidgetItem(val))

    def _insert_item(self):
        """Insert a new dict/list item at current position"""
        pos = self.datable.currentRow()
        self.datable.insertRow(pos)

    def _delete_item(self):
        """Delete dict/list item at current position"""
        pos = self.datable.currentRow()
        self.datable.removeRow(pos)

    def _collect_column(self, col):
        """Collect data from column col"""
        items = (self.datable.item(row, col) for row in range(self.datable.rowCount()))
        return (_item.text() for _item in items)

    def accept(self):
        """Do some sanity checks, close dialog if ok"""
        if self.list_mode:
            self.data = self._collect_column(0)
        else:
            keys, vals = self._collect_column(0), self._collect_column(1)
            self.data = {k: v for k, v in zip(keys, vals)}
        self.done(QtWidgets.QDialog.Accepted)


class QCompoundEditorList(QCompoundEditor):
    



if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    data = list('abcdef')
    data = {'a': 1, 'b': 2}
    #data = list(range(100))
    #data = ['Toe standing', 'Unipedal right', 'Unipedal left']
    data = {(7, 12): 'Z:\\PXD_files\\muscle_length_7_12.xlsx', (3, 6): 'Z:\\PXD_files\\muscle_length_3_6.xlsx', (13, 19): 'Z:\\PXD_files\\muscle_length_13_19.xlsx'}
    #data = [['AnkleAnglesX', 'AnkleAnglesY', 'AnkleAnglesZ'], ['ForeFootAnglesX', 'ForeFootAnglesZ', 'ForeFootAnglesY']]
    dlg = QCompoundEditor(data)
    dlg.show()
    if dlg.exec_():
        print(dlg.data)