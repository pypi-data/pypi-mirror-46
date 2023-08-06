#  -*- coding: utf-8 -*-
"""
CalcS
errorcalcs Gui
"""

import os

from PyQt5.QtWidgets import (QMainWindow, QApplication, QDialog, QGridLayout,
                             QGroupBox, QHBoxLayout, QLabel, QLineEdit,

                             QPushButton, QVBoxLayout, QWidget, QScrollArea,
                             QMessageBox, QAction, QFileDialog)
from PyQt5.QtGui import (QDoubleValidator, QIcon)

import errorcalcsbeta.ecfuncs
import errorcalcsbeta.menu_bar


class main_Window(QMainWindow):
    def __init__(self, parent=None):
        super(main_Window, self).__init__(parent)

        title = 'CalcS - errorcalcs-beta'
        self.setWindowTitle(title)

        mainMenu = self.menuBar()
        fileMenu = mainMenu.addMenu('File')
        viewMenu = mainMenu.addMenu('View')
        helpMenu = mainMenu.addMenu('Help')
        ecMenu = mainMenu.addMenu('ErroRCalcS')

        # fileMenu
        FNew = QAction(QIcon('./pictures/icon/actions/new.png'), 'New', self)
        FNew.triggered.connect(menu_bar.File.new)
        
        FOpen = QAction(QIcon('./pictures/icon/actions/open.png'), 'Open', self)
        FOpen.triggered.connect(menu_bar.File._open_)

        FSave = QAction(QIcon('./pictures/icon/actions/save.png'), 'Save', self)
        FSave.setShortcut('Ctrl+S')
        FSave.triggered.connect(menu_bar.File.save)

        FExport_here = QAction(QIcon('./pictures/icon/actions/export.png'),
                              'Export Formula in new File',
                              self)
        FExport_here.setShortcut('Crtl+Shift+E')
        FExport_here.triggered.connect(menu_bar.File.exportFormulaNew)

        FExport = QAction(QIcon('./pictures/icon/actions/export.png'),
                         'Export Formula',
                         self)
        FExport.setShortcut('Ctrl+E')
        FExport.triggered.connect(menu_bar.File.exportFormulaAppend)

        file_menu = [FNew, FSave, FExport_here, FExport]

        for i in file_menu:
            fileMenu.addAction(i)
        # end fileMenu

        # viewMenu
        VFull = QAction(QIcon('./pictures/icon/actions/fullcreen.png'), 'Fullscreen', self)
        VFull.setShortcut('F11')
        VFull.triggered.connect(menu_bar.View.fullScreen)

        view_menu = [VFull]

        for i in view_menu:
            viewMenu.addAction(i)
        # end viewMenu

        # helpMenu
        HUse = QAction('Usage', self)
        HUse.setShortcut('F1')
        HUse.triggered.connect(menu_bar.Help.usage)

        HShortCuts = QAction('Shortcut Summary')
        HShortCuts.triggered.connect(menu_bar.Help.shortcut)

        HUpdate = QAction('Check for updates')
        HUpdate.triggered.connect(menu_bar.Help.update)

        help_menu = [HUse, HShortCuts, HUpdate]

        for i in help_menu:
            helpMenu.addAction(i)
        # end helpMenu

        # ecMenu
        EDonate = QAction(QIcon('./pictures/icon/actions/paypal.png'), 'Donate for ErroRCalcS', self)
        EDonate.triggered.connect(menu_bar.Ec.donate)
        
        EGit = QAction(QIcon('./pictures/icon/actions/git.png'), 'ErroRCalcS on GitHub', self)
        EGit.triggered.connect(menu_bar.Ec.git)
        
        EWeb = QAction(QIcon('./pictures/icon/actions/ec.png'), 'ErroRCalcS Webpage', self)
        EWeb.triggered.connect(menu_bar.Ec.web)
        
        EPypi = QAction(QIcon('./pictures/icon/actions/pypi.png'), 'ErroRCalcS on PyPi', self)
        EPypi.triggered.connect(menu_bar.Ec.pypi)

        ec_menu = [EDonate, EGit, EWeb, EPypi]

        for i in ec_menu:
            ecMenu.addAction(i)
        # end helpMenu
        # end ecMenu

        self.setCentralWidget(main_Widget(self))


class main_Widget(QWidget):
    def __init__(self, parent=None):
        super(main_Widget, self).__init__(parent)

        # ----------------create GroupBoxes----------------
        self.createTLGB()
        self.createBLGB()
        self.createTRGB()
        self.createBRGB()
        # ----------------end GroupBoxes----------------

        # ----------------main Layout----------------
        mainLayout = QHBoxLayout()
        
        leftArea = QVBoxLayout()
        rightArea = QVBoxLayout()
        leftArea.addWidget(self.TLGB)
        leftArea.addWidget(self.BLGB)
        rightArea.addWidget(self.TRGB)
        rightArea.addWidget(self.BRGB)
        
        mainLayout.addLayout(leftArea)
        mainLayout.addLayout(rightArea)
        
        self.setLayout(mainLayout)
        # ----------------end main Layout----------------
        
    def createTLGB(self):
        """
        places GroupBox to top-left
        inputs for calculations
        """
        
        self.TLGB = QGroupBox('add variable')
        
        # ----------------inputs----------------
        self.var_in = QLineEdit('')
        self.value_in = QLineEdit('')
        self.value_in.setValidator(QDoubleValidator())
        self.error_in = QLineEdit('')
        self.error_in.setValidator(QDoubleValidator())
        # ----------------end inputs----------------
        
        # ----------------labels----------------
        var_label = QLabel('variable:')
        value_label = QLabel('value:')
        error_label = QLabel('error:')
        # ----------------end labels----------------
        
        # ----------------buttons----------------
        add_button = QPushButton('add variable')
        # ----------------end buttons----------------
        
        # ----------------Layout----------------
        layout = QGridLayout()
        
        layout.addLayout(layout, 0, 0, 1, 3)
        layout.addWidget(var_label, 0, 0)
        layout.addWidget(self.var_in, 0, 1)
        layout.addWidget(value_label, 1, 0)
        layout.addWidget(self.value_in, 1, 1)
        layout.addWidget(error_label, 2, 0)
        layout.addWidget(self.error_in, 2, 1)
        layout.addWidget(add_button, 3, 0)
        layout.setRowStretch(1, 1)
        layout.setColumnStretch(1, 1)
        
        self.TLGB.setLayout(layout)
        
        self.TLGB.setMaximumHeight(170)
        # ----------------end Layout----------------
            
        # ----------------button functions----------------
        add_button.clicked.connect(self.addVar)
        add_button.clicked.connect(self.variableFunc)
        # ----------------end button functions----------------
        
    def createBLGB(self):
        """
        places GroupBox to bottom-left
        list of inputs
        """
        
        self.BLGB = QGroupBox('added variables')
        
        # ----------------scrollbar----------------
        list_of_inputs = QScrollArea(self)
        list_of_inputs.setWidgetResizable(True)
        # ----------------end scrollbar----------------
        
        # ----------------Layout----------------
        layout = QVBoxLayout()
        layout.addWidget(list_of_inputs)
        
        self.BLGB.setLayout(layout)
        
        # set scrollbar Layout                
        contentI = QWidget(list_of_inputs)
        self.contentILayout = QVBoxLayout(contentI)
        contentI.setLayout(self.contentILayout)
        
        list_of_inputs.setWidget(contentI)
        # ----------------end Layout----------------
        
    def createTRGB(self):
        """
        places GroupBox to top-left
        inputs for calculations
        """
        
        self.TRGB = QGroupBox('calculation')
        
        # ----------------inputs----------------
        self.calc_in = QLineEdit('')
        # ----------------end inputs----------------
        
        # ----------------labels----------------
        calc_label = QLabel('formula:')
        self.result_label = QLabel('...')
        # ----------------end labels----------------
        
        # ----------------buttons----------------
        calc_button = QPushButton('calculate')
        # ----------------end buttons----------------
        
        # ----------------Layout----------------
        layout = QGridLayout()
        
        layout.addLayout(layout, 0, 0, 1, 1)
        layout.addWidget(calc_label, 0, 0)
        layout.addWidget(self.calc_in, 0, 1)
        layout.addWidget(calc_button, 1, 0)
        layout.addWidget(self.result_label, 1, 1)
        layout.setRowStretch(1, 1)
        layout.setColumnStretch(1, 1)
        
        self.TRGB.setLayout(layout)
        
        self.TRGB.setMaximumHeight(170)
        # ----------------end Layout----------------
            
        # ----------------button functions----------------
        calc_button.clicked.connect(self.calculate)
        # ----------------end button functions----------------
        
    def createBRGB(self):
        """
        places GroupBox to bottom-right
        history
        """
        
        self.BRGB = QGroupBox('history')
        
        # ----------------scrollbar----------------
        history = QScrollArea(self)
        history.setWidgetResizable(True)
        # ----------------end scrollbar----------------
        
        # ----------------Layout----------------
        layout = QVBoxLayout()
        layout.addWidget(history)
        
        self.BRGB.setLayout(layout)
        
        # set scrollbar Layout                
        contentH = QWidget(history)
        self.contentHLayout = QVBoxLayout(contentH)
        contentH.setLayout(self.contentHLayout)
        
        history.setWidget(contentH)
        # ----------------end Layout----------------
        
    # ===================functions==============================================
    def addVar(self):
        ecfuncs.button_Funcs.addVar(self.var_in.text(),
                                    self.value_in.text(),
                                    self.error_in.text())
    
    def variableFunc(self):
        i = ecfuncs.button_Funcs.variableFunc()
        self.contentILayout.addWidget(QLabel(i))

    def calculate(self):
        way, result = ecfuncs.button_Funcs.calculate(self.calc_in.text())
        self.contentHLayout.addWidget(QLabel(way[-1]))
        self.result_label.setText(result)
    # ===================fend unctions==========================================    

    def file_Dialog(self):
        here = QFileDialog.getSaveFileName(self, 'Export Formula to LaTeX')
        return here[0]


def run_gui():
    """
    run_e_c() is the mainfunction od errorcalcs. It starts the errorcalcs-GUI
    so the user can use the GUI to calculate error propagation.
    This functon does not take any arguments. Use it as follows to run the GUI:
        from errorcalcs.errorcalcs import run_GUI
        run_GUI()
    """
    import sys
    
    try:
        os.mkdir('~/errorcalcsbeta')
    except FileExistsError:
        pass
    
    app = QApplication(sys.argv)
    gallery = main_Window()
    gallery.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    run_gui()
