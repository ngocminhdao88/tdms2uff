# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'view.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(1024, 768)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout(Dialog)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.openFilesButton = QtWidgets.QPushButton(Dialog)
        self.openFilesButton.setObjectName("openFilesButton")
        self.horizontalLayout.addWidget(self.openFilesButton)
        self.openFolderButton = QtWidgets.QPushButton(Dialog)
        self.openFolderButton.setObjectName("openFolderButton")
        self.horizontalLayout.addWidget(self.openFolderButton)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.inputFileLabel = QtWidgets.QLabel(Dialog)
        self.inputFileLabel.setObjectName("inputFileLabel")
        self.verticalLayout.addWidget(self.inputFileLabel)
        self.inputFilesListView = QtWidgets.QListView(Dialog)
        self.inputFilesListView.setObjectName("inputFilesListView")
        self.verticalLayout.addWidget(self.inputFilesListView)
        self.horizontalLayout_4.addLayout(self.verticalLayout)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.addToQueueButton = QtWidgets.QPushButton(Dialog)
        self.addToQueueButton.setObjectName("addToQueueButton")
        self.horizontalLayout_2.addWidget(self.addToQueueButton)
        self.sameSettingsCheckBox = QtWidgets.QCheckBox(Dialog)
        self.sameSettingsCheckBox.setObjectName("sameSettingsCheckBox")
        self.horizontalLayout_2.addWidget(self.sameSettingsCheckBox)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem1)
        self.verticalLayout_2.addLayout(self.horizontalLayout_2)
        self.channelsMappingLabel = QtWidgets.QLabel(Dialog)
        self.channelsMappingLabel.setObjectName("channelsMappingLabel")
        self.verticalLayout_2.addWidget(self.channelsMappingLabel)
        self.channelsTableView = QtWidgets.QTableView(Dialog)
        self.channelsTableView.setObjectName("channelsTableView")
        self.verticalLayout_2.addWidget(self.channelsTableView)
        self.horizontalLayout_4.addLayout(self.verticalLayout_2)
        self.verticalLayout_3 = QtWidgets.QVBoxLayout()
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.convertButton = QtWidgets.QPushButton(Dialog)
        self.convertButton.setObjectName("convertButton")
        self.horizontalLayout_3.addWidget(self.convertButton)
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem2)
        self.verticalLayout_3.addLayout(self.horizontalLayout_3)
        self.outputQueueLabel = QtWidgets.QLabel(Dialog)
        self.outputQueueLabel.setObjectName("outputQueueLabel")
        self.verticalLayout_3.addWidget(self.outputQueueLabel)
        self.outputQueueListView = QtWidgets.QListView(Dialog)
        self.outputQueueListView.setObjectName("outputQueueListView")
        self.verticalLayout_3.addWidget(self.outputQueueListView)
        self.horizontalLayout_4.addLayout(self.verticalLayout_3)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.openFilesButton.setText(_translate("Dialog", "Open files"))
        self.openFolderButton.setText(_translate("Dialog", "Open folder"))
        self.inputFileLabel.setText(_translate("Dialog", "Input files"))
        self.addToQueueButton.setText(_translate("Dialog", "Add to queue"))
        self.sameSettingsCheckBox.setText(_translate("Dialog", "Same settings for all files"))
        self.channelsMappingLabel.setText(_translate("Dialog", "Channels mapping"))
        self.convertButton.setText(_translate("Dialog", "Convert"))
        self.outputQueueLabel.setText(_translate("Dialog", "Output queue"))

