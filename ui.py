import os
import time
from pathlib import Path

from PySide2.QtWidgets import (
    QApplication,
    QMainWindow,
    QPushButton,
    QWidget,
    QFileDialog,
    QLineEdit,
    QLabel,
    QComboBox,
    QProgressBar,
    QFrame,
    QSpacerItem,
    QSizePolicy,
    QListWidget,
    QListWidgetItem,
    QHBoxLayout,
    QVBoxLayout,
    QGridLayout,
)

from PySide2.QtCore import QSize, Qt
from PySide2.QtGui import QIcon, QFont

from get_metadata import video_metadata

from converter import convert_video, Codecs,Containers,Resolutions,Bitrates

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setIcon()

        self.setWindowTitle("Video Converter")
        self.setMinimumSize(QSize(1200, 700))

        #____________________________________#
        #            Layouts                 #
        #____________________________________#

        self.pagelayout = QVBoxLayout()

        self.top_button_layout = QHBoxLayout()
        self.save_button_layout = QHBoxLayout()
        self.convert_button_layout = QHBoxLayout()

        self.main_layout = QHBoxLayout()

        self.convert_options = QGridLayout()
        self.options_layout = QVBoxLayout()

        self.options_layout.addLayout(self.convert_options)

        vertical_spacer1 = QSpacerItem( QSizePolicy.Expanding, QSizePolicy.Maximum)
        #horizontal_spacer = QSpacerItem(20,40,  QSizePolicy.Expanding, QSizePolicy.Minimum)   

        self.pagelayout.addLayout(self.top_button_layout)
        self.pagelayout.addLayout(self.main_layout)
        self.pagelayout.addLayout(self.save_button_layout)
        self.pagelayout.addLayout(self.convert_button_layout)

        # _____________ Fonts  _____________ #

    
        font10 = self.font()
        font10.setPointSize(10)
        font12 = self.font()
        font12.setPointSize(12)
        
        vertical_spacer1 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        #horizontal_spacer = QSpacerItem(20,40,  QSizePolicy.Expanding, QSizePolicy.Minimum)

        # ___ bottom layout Log __#
        self.save_location = QLineEdit()
        self.save_location.setText(str(Path.cwd()))


        self.progress_bar = QProgressBar()
        self.progress_bar.setMinimum(0)
        self.progress_bar.setMaximum(100)

        self.progress_label = QLabel("No Files Selected for Conversion")
        self.progress_label.setStyleSheet('''QLabel{font-size: 10pt;}''' )
        self.progress_label.setFixedWidth(300)
        self.progress_label.setAlignment(Qt.AlignRight)

        #____________________________________#
        #            Buttons                 #
        #____________________________________#

        # Add Files button.
        self.add_file_button = QPushButton(" Add Files ")
        self.add_file_button.setStyleSheet(
            """
            QPushButton{
                background-color: #00bfff; 
            }
            QPushButton::hover{
                background-color:#0099cc;
            }
            """
        )
        self.add_file_button.setIcon(QIcon("icons\_add.png"))
        self.add_file_button.clicked.connect(self.openFileDialog)

        # Remove Button.
        self.remove_button = QPushButton(" Remove ")
        self.remove_button.setStyleSheet(
            """
            QPushButton{
                background-color: #e60000; 
            }
            QPushButton::hover{
                background-color:#b30000;
            }
            """
        )
        self.remove_button.setIcon(QIcon("icons\_remove.png"))
        self.remove_button.setEnabled(False)
        self.remove_button.clicked.connect(self.removeSelectedItems)


        # Select all Button
        self.select_all_button = QPushButton(" Select All ")
        self.select_all_button.setStyleSheet(
            """
            QPushButton{
                background-color: #59d22d; 
            }
            QPushButton::hover{
                background-color:#52a824;
            }
            """
        )
        self.select_all_button.setIcon(QIcon("icons\_select.png"))
        self.select_all_button.setEnabled(False)
        self.select_all_button.clicked.connect(self.selectAll)

        # Convert Button.
        self.convert_button = QPushButton(" Convert ")
        self.convert_button.setStyleSheet(
            """
            QPushButton{
                background-color: #00bfff; 
            }
            QPushButton::hover{
                background-color: #0099cc;
            }
            """
        )
        self.convert_button.setIcon(QIcon("icons\_convert.png"))
        self.convert_button.setEnabled(False)
        self.convert_button.setFixedWidth(190)
        self.convert_button.clicked.connect(self.convert)
        


        # Save Button.
        self.save_button = QPushButton(" Save Directory ")
        self.save_button.setStyleSheet(
            """
            QPushButton{
                background-color: #59d22d; 
            }
            QPushButton::hover{
                background-color: #52a824;
            }
            """
        )
        self.save_button.setIcon(QIcon("icons\_save.png"))
        self.save_button.setFixedWidth(190)
        self.save_button.clicked.connect(self.getSaveLocation)


        # __________ List Widget __________#

        self.files_list = QListWidget()
        self.files_list.setSelectionMode(QListWidget.MultiSelection)
        self.files_list.itemSelectionChanged.connect(self.getSelectedFiles)
        
        self.createFileList

        #___________________________________________#
        #              Convert Options              #
        #___________________________________________#

        self.title_label = QLabel("Convert Options")
        self.title_label.setStyleSheet('''QLabel{font-size: 12pt;}''' )
 

        # ____________ Output Properties ____________ #

        
        self.output_label = QLabel("Output Properties: ")
        self.output_label.setFrameStyle(QFrame.Panel | QFrame.Raised)
        


        # ____________ Format ____________ #

        self.format_label = QLabel("Format: ")


        self.format_combobox = QComboBox()
        self.format_combobox.addItem('MP4', ['H264','H265','MPEG4','PRORES','DNxHD','DNxHR'])
        self.format_combobox.addItem('MOV', ['H264', 'H265', 'MPEG4', 'PRORES', 'DNxHD', 'DNxHR'])
        self.format_combobox.addItem('AVI', ['H264', 'MPEG4', 'THEORA', 'WMV'])
        self.format_combobox.addItem('MKV', ['H264', 'H265', 'VP8', 'VP9', 'AV1', 'MPEG2', 'MPEG4', 'THEORA', 'WMV', 'PRORES', 'DNxHD', 'DNxHR'])
        self.format_combobox.addItem('FLV', ['H264', 'MPEG4', 'VP8', 'VP9'])
        self.format_combobox.addItem('WEBM', ['VP8', 'VP9', 'AV1'])
        self.format_combobox.addItem('OGG', ['THEORA'])
        self.format_combobox.addItem('MPEG', ['MPEG2', 'MPEG4'])

        self.format_combobox.setFont(font10)
        self.format_combobox.currentIndexChanged.connect(self.outputProperties)


        # ____________ Encoder ____________ #

        self.codec_label = QLabel("Codecs: ")

        self.codec_combobox = QComboBox()
        self.format_combobox.currentIndexChanged.connect(self.updateCodecs)
        self.updateCodecs(self.format_combobox.currentIndex())
        self.codec_combobox.setFont(font10)



        # ____________ FPS ____________ #

        self.fps_label = QLabel("FPS: ")


        self.fps_combobox = QComboBox()
        self.fps_combobox.addItems(['5','10','12','15','20', '23.976' , '24','25','29.97','30', '48','50','59.94','60','72','75','90','100'])
        self.fps_combobox.currentIndexChanged.connect(self.outputProperties)
        self.fps_combobox.setFont(font10)


        # ____________ Bitrate ____________ #

        self.bitrate_label = QLabel("Bitrate: ")

        self.bitrate_combobox = QComboBox()
        self.bitrate_combobox.addItems(['ORIGINAL','LOW','MEDIUM','HIGH','HD','FULLHD','UHD_4K'])
        self.bitrate_combobox.currentIndexChanged.connect(self.outputProperties)
        self.bitrate_combobox.setFont(font10)


        # ____________ Resolution ____________ #

        self.resolution_label = QLabel("Resolution: ")

        self.resolution_combobox = QComboBox()
        self.resolution_combobox.addItems(['Original','SD','HD','FULLHD','UHD_4K','UHD_8K'])

        self.resolution_combobox.currentIndexChanged.connect(self.outputProperties) 
        self.resolution_combobox.setFont(font10)


        # __________ Grid layout __________#

        self.convert_options.setColumnMinimumWidth(0, 60)

        self.convert_options.setColumnMinimumWidth(1, 200)
        self.convert_options.setVerticalSpacing(30)

        self.convert_options.addWidget(self.title_label, 0, 0)

        self.convert_options.addWidget(self.format_label, 1, 0)
        self.convert_options.addWidget(self.format_combobox, 1, 1)

        self.convert_options.addWidget(self.codec_label, 2, 0)
        self.convert_options.addWidget(self.codec_combobox, 2, 1)

        self.convert_options.addWidget(self.fps_label, 3, 0)
        self.convert_options.addWidget(self.fps_combobox, 3, 1)

        self.convert_options.addWidget(self.bitrate_label, 4, 0)
        self.convert_options.addWidget(self.bitrate_combobox, 4, 1)

        self.convert_options.addWidget(self.resolution_label, 5, 0)
        self.convert_options.addWidget(self.resolution_combobox, 5, 1)
        self.convert_options.setAlignment(Qt.AlignTop)
        self.options_layout.addItem(vertical_spacer1)
        self.options_layout.addWidget(self.output_label)

        


        # __________ Layout Setup __________#

        self.top_button_layout.addWidget(self.add_file_button)
        #self.top_button_layout.addWidget(self.add_folder_button)
        self.top_button_layout.addWidget(self.select_all_button)
        self.top_button_layout.addWidget(self.remove_button)
        self.top_button_layout.setAlignment(Qt.AlignLeft)

        
        self.save_button_layout.addWidget(self.save_button)
        self.save_button_layout.addWidget(self.save_location)
       # self.bottom_button_layout.addItem(horizontal_spacer)
        self.convert_button_layout.addWidget(self.convert_button)
        self.convert_button_layout.addWidget(self.progress_bar)
        self.convert_button_layout.addWidget(self.progress_label)


        self.main_layout.addWidget(self.files_list)
        self.main_layout.addLayout(self.options_layout)

        #Set layout

        self.widget = QWidget()
        self.widget.setLayout(self.pagelayout)

        self.setCentralWidget(self.widget)
        self.checked = QIcon('icons\_checked.png')
        self.uncheck= QIcon('icons\_unchecked.png')

        
    #____________________________________________#
    #              Utility Functions             #
    #____________________________________________#

    def setIcon(self):
        appIcon = QIcon("icons\_icon.png")
        self.setWindowIcon(appIcon)

    def updateButtonState(self):
        
        if self.files_list.count() > 0:
            self.select_all_button.setEnabled(True)
            self.remove_button.setEnabled(True)
        
        else:
            self.select_all_button.setEnabled(False)
            self.remove_button.setEnabled(False)
            self.convert_button.setEnabled(False)
    
    def selectAll(self):
        self.files_list.selectAll()

    def removeSelectedItems(self):
        selected_items = self.files_list.selectedItems()
        for item in selected_items:
            row = self.files_list.row(item)
            self.files_list.takeItem(row)    
    
    def updateCodecs(self,index):
        self.codec_combobox.clear()
        codecs = self.format_combobox.itemData(index)
        if codecs:
            self.codec_combobox.addItems(codecs)

    def outputProperties(self):
        
        formats = self.format_combobox.currentText()
        fps = self.fps_combobox.currentText()
        bitrate = self.bitrate_combobox.currentText()
        resolution = self.resolution_combobox.currentText()

        self.output_label.setText(f"Output Properties:\n Format: {getattr(Containers, formats)} \n FPS: {int(fps)} \n Bitrate: {getattr(Bitrates, bitrate)} \n Resolution: {getattr(Resolutions, resolution)} ")       

    def createFileList(self, files: list): 
        for i in files:
            
            video_name = os.path.basename(i)
            metadata = video_metadata(i)

            listWidgetItem = QListWidgetItem("\n {} \nVideo Metadata: {}".format(video_name , metadata) )
            listWidgetItem.setData(Qt.UserRole,Path(i))
            listWidgetItem.setIcon(self.uncheck)
            self.files_list.addItem(listWidgetItem)

            self.updateButtonState()

    def getSelectedFiles(self):
        
        selected_items = self.files_list.selectedItems()
        for row in range(self.files_list.count()):
            item = self.files_list.item(row)
            if item in selected_items:
                item.setIcon(self.checked)
                self.convert_button.setEnabled(True)
            else:
                item.setIcon(self.uncheck)
        
    

    def openFileDialog(self) -> None:
        option = QFileDialog.Options()
        files = QFileDialog.getOpenFileNames(
            parent=self.widget,
            caption="Open File",
            directory="No File Selected",
            filter="Video Files (*.mp4 *.mov *.avi *.mkv *.mpeg *.webm *.ogg *.flv)",
            options=option,
        )
        
        self.createFileList(files[0])  
    
    def getSaveLocation(self):
        option=QFileDialog.Options()
        file=QFileDialog.getExistingDirectory(parent = self.widget, caption="Select Save Location",directory = "No Folder Selected")
        file_str=str(file)
        self.save_location.setText(file)
           
    def progress(self,s):
        progress=self.progress_bar.value()
        if progress == 100:
            start=0
        else:
            start=progress
           
        for i in range(start,int(s)):
            time.sleep(0.01)
            self.progress_bar.setValue(i+1)

        
        self.progress_label.setText("Conversion started")

        if s == 100:
            selected_items=self.files_list.selectedItems()
            total_files = len( selected_items)
            for item in range(total_files):
                self.progress_label.setText("{} out of {} files converted succussfully".format(item+1,total_files))
                  

    def convert(self):
        formats = self.format_combobox.currentText()
        codec = self.codec_combobox.currentText()
        fps = self.fps_combobox.currentText()
        bitrate = self.bitrate_combobox.currentText()
        resolution = self.resolution_combobox.currentText()

        selected_items = self.files_list.selectedItems()
        for items in selected_items:
            convert_this= items.data(Qt.UserRole)
            
            convert_video(
            Path('"{}"'.format(convert_this)),
            new_fps=int(fps),
            new_bitrate=getattr(Bitrates,bitrate),
            new_resolution=getattr(Resolutions,resolution),
            new_codec=getattr(Codecs,codec),
            new_container=getattr(Containers,formats),
            folder=Path('"{}"'.format(self.save_location.text())),
            callback=self.progress

        )
   
# ------------------------------------------


app = QApplication()

app.setStyleSheet(Path('style.qss').read_text())

window = MainWindow()
window.show()

app.exec_()
