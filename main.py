from PySide6 import QtCore, QtWidgets, QtGui
import sys
import random
import os
import pickle
import datetime
os.chdir(os.path.dirname(sys.argv[0]))

class MainMenu(QtWidgets.QWidget):
    def __init__(self, parent=None, plant_list=None):
        super(MainMenu, self).__init__(parent)
        self.setWindowTitle("PLANT ENCYCLOPEDIA by Dan")

        choice = random.choice(plant_list)
        random_plant = choice[1]
        self.label = choice[0]

        self.button1 = QtWidgets.QPushButton("BROWSE PLANTS")
        self.button1.setSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding)
        self.button1.setStyleSheet("""font-size:36px;""")

        self.button2 = QtWidgets.QPushButton("RANDOM PLANT")
        self.button2.setSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding)
        self.button2.setStyleSheet("""font-size:36px;""")

        self.button3 = QtWidgets.QPushButton("WATERING")
        self.button3.setSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding)
        self.button3.setStyleSheet("""font-size:36px;""")

        self.button4 = QtWidgets.QPushButton("EXIT")
        self.button4.setSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding)
        self.button4.setStyleSheet(f"""font-size:36px;""")

        size = QtCore.QSize(600,600)
        self.picture = QtWidgets.QLabel(self, alignment=QtCore.Qt.AlignCenter)
        self.picture.setPixmap(QtGui.QPixmap(f"./flowers/pics/{random_plant}.png").scaled(size))
        self.picture.setSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)

        self.button5 = QtWidgets.QPushButton(f"{self.label}")
        self.button7 = QtWidgets.QPushButton("HELP")
        self.button7.setStyleSheet("""font-size:36px;""")

        self.text = QtWidgets.QLabel("PLANT ENCYCLOPEDIA VERSION 0.3",
                                    alignment=QtCore.Qt.AlignTop | QtCore.Qt.AlignHCenter)
        self.text.setStyleSheet("""font-size:56px; background-color:{QtGui.QColor(255,0,0).name}; color:white;""")
        self.bg = QtWidgets.QLabel(self)
        
        self.rand_pic = QtWidgets.QVBoxLayout(self)
        self.rand_pic.addWidget(self.picture, 5)
        self.rand_pic.addWidget(self.button5)
        pic_layout = QtWidgets.QWidget()
        pic_layout.setLayout(self.rand_pic)

        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.addWidget(self.button1)
        self.layout.addWidget(self.button2)
        self.layout.addWidget(self.button3)
        self.layout.addWidget(self.button7)
        self.layout.addWidget(self.button4)
        main_widget = QtWidgets.QWidget()
        main_widget.setLayout(self.layout)

        menu_layout = QtWidgets.QHBoxLayout(self)
        menu_layout.addWidget(pic_layout, 2)
        menu_layout.addWidget(main_widget, 2)
        to_add = QtWidgets.QWidget()
        to_add.setLayout(menu_layout)

        full_layout = QtWidgets.QVBoxLayout(self)
        full_layout.addWidget(self.text)
        # full_layout.addWidget(search_bar)
        full_layout.addWidget(to_add)

        self.setStyleSheet("""
            QPushButton
            {
                color: white;
                background-color: rgba(130, 98, 66, 200);
            }
            QPushButton::hover
            {
                background-color: rgba(130, 98, 66, 230);
            }
        """)


class BrowseMenu(QtWidgets.QWidget):
    def __init__(self, parent=None, selected=None, plant_list=None, plants=None):
        super(BrowseMenu, self).__init__(parent)
        
        self.plants = plants
        self.plant_list = plant_list

        self.text_widget = QtWidgets.QTextBrowser(self)
        self.menu_widget = QtWidgets.QListWidget()
        index = None
        if selected != None:
            for i in range(len(self.plant_list)):
                if self.plant_list[i][0] == selected:
                    index = i
        counter = 0
        for i in self.plant_list:
            counter += 1
            item = QtWidgets.QListWidgetItem(f"{i[0]}")
            item.setTextAlignment(QtCore.Qt.AlignCenter)
            self.menu_widget.addItem(item)

        self.menu_widget.itemSelectionChanged.connect(self.selectionChanged)

        if index != None:
            self.menu_widget.setCurrentRow(index)

        self.add_button = QtWidgets.QPushButton("Add to Watering")
        remove_button = QtWidgets.QPushButton("Remove from Watering")
        self.back_button = QtWidgets.QPushButton("Back")

        two_buttons = QtWidgets.QHBoxLayout()
        two_buttons.addWidget(self.add_button)
        two_buttons.addWidget(remove_button)

        content_layout = QtWidgets.QVBoxLayout()
        content_layout.addWidget(self.text_widget)
        content_layout.addLayout(two_buttons)
        content_layout.addWidget(self.back_button)
        main_widget = QtWidgets.QWidget()
        main_widget.setLayout(content_layout)

        layout = QtWidgets.QHBoxLayout()
        layout.addWidget(self.menu_widget, 1)
        layout.addWidget(main_widget, 4)
        self.setLayout(layout)

        
        remove_button.clicked.connect(self.remove_from_watering)

        self.setStyleSheet("""
        QLabel {
            background-color: gray;
        }
        QTextBrowser {
            background-color: black;
            color: white;
        }
        QListWidget {
            color: #FFFFFF;
            background-color: #33373B;
        }

        QListWidget::item {
            height: 50px;
        }

        QListWidget::item:selected {
            background-color: #FFA500;
            color: black;
        }

        QLabel {
            background-color: #FFFFFF;
            qproperty-alignment: AlignCenter;
        }

        QPushButton {
            background-color: #FFA500;
            padding: 20px;
            font-size: 18px;
        }
        """)

    def selectionChanged(self):
        selected = self.menu_widget.selectedItems()[0].text()
        index = None
        for i in range(len(self.plant_list)):
            if self.plant_list[i][0] == selected:
                index = i
                self.name = self.plant_list[i][1]
        if index != None:
            self.text_widget.setSource(QtCore.QUrl.fromLocalFile(f"flowers\{self.name}.html"))
   
    
    def remove_from_watering(self):
        selected = self.menu_widget.selectedItems()[0].text()
        for plant in self.plants:
            if plant[0] == selected:
                plant[0], plant[1], plant[2], plant[3] = None, None, None, None


class Watering(QtWidgets.QWidget):
    def __init__(self, parent=None, plants=None):
        super(Watering, self).__init__(parent)
        self.plants = plants
        status_text = "No flower selected."
        empty_flower = "No flower selected."

        # set all the texts for flowers regardless if they were added to list
        size = QtCore.QSize(315,258)
        if plants[0][0] != None:
            text1 = QtWidgets.QLabel(f"{plants[0][0]}")
            text1.setAlignment(QtCore.Qt.AlignCenter)
            rt1 = QtWidgets.QLabel(f"{plants[0][0]}")
            rt1.setAlignment(QtCore.Qt.AlignCenter)
            rt1.setStyleSheet("font-size:36px")
            self.status1 = QtWidgets.QLabel(f"Water next on: {plants[0][1]}.")
            self.status1.setAlignment(QtCore.Qt.AlignCenter)   
            pic1 = QtWidgets.QLabel(self)
            pic1.setPixmap(QtGui.QPixmap(f"./flowers/pics/{plants[0][2]}.png").scaled(size))
        else:
            text1 = QtWidgets.QLabel(empty_flower)
            text1.setAlignment(QtCore.Qt.AlignCenter)
            rt1 = QtWidgets.QLabel(empty_flower)
            rt1.setAlignment(QtCore.Qt.AlignCenter)
            rt1.setStyleSheet("font-size:36px")
            self.status1 = QtWidgets.QLabel(status_text)
            self.status1.setAlignment(QtCore.Qt.AlignCenter) 
            pic1 = QtWidgets.QLabel()
        if plants[1][0] != None:
            text2 = QtWidgets.QLabel(f"{plants[1][0]}")
            text2.setAlignment(QtCore.Qt.AlignCenter)
            rt2 = QtWidgets.QLabel(f"{plants[1][0]}")
            rt2.setAlignment(QtCore.Qt.AlignCenter)
            rt2.setStyleSheet("font-size:36px")
            self.status2 = QtWidgets.QLabel(f"Water next on: {plants[1][1]}.")
            self.status2.setAlignment(QtCore.Qt.AlignCenter) 
            pic2 = QtWidgets.QLabel(self)
            pic2.setPixmap(QtGui.QPixmap(f"./flowers/pics/{plants[1][2]}.png").scaled(size))
        else:
            text2 = QtWidgets.QLabel(empty_flower)
            text2.setAlignment(QtCore.Qt.AlignCenter)
            rt2 = QtWidgets.QLabel(empty_flower)
            rt2.setAlignment(QtCore.Qt.AlignCenter)
            rt2.setStyleSheet("font-size:36px")
            self.status2 = QtWidgets.QLabel(status_text)
            self.status2.setAlignment(QtCore.Qt.AlignCenter) 
            pic2 = QtWidgets.QLabel()
        if plants[2][0] != None:
            text3 = QtWidgets.QLabel(f"{plants[2][0]}")
            text3.setAlignment(QtCore.Qt.AlignCenter)
            rt3 = QtWidgets.QLabel(f"{plants[2][0]}")
            rt3.setAlignment(QtCore.Qt.AlignCenter)
            rt3.setStyleSheet("font-size:36px")
            self.status3 = QtWidgets.QLabel(f"Water next on: {plants[2][1]}.")
            self.status3.setAlignment(QtCore.Qt.AlignCenter) 
            pic3 = QtWidgets.QLabel(self)
            pic3.setPixmap(QtGui.QPixmap(f"./flowers/pics/{plants[2][2]}.png").scaled(size))
        else:
            text3 = QtWidgets.QLabel(empty_flower)
            text3.setAlignment(QtCore.Qt.AlignCenter)
            rt3 = QtWidgets.QLabel(empty_flower)
            rt3.setAlignment(QtCore.Qt.AlignCenter)
            rt3.setStyleSheet("font-size:36px")
            self.status3 = QtWidgets.QLabel(status_text)
            self.status3.setAlignment(QtCore.Qt.AlignCenter) 
            pic3 = QtWidgets.QLabel()
        if plants[3][0] != None:
            text4 = QtWidgets.QLabel(f"{plants[3][0]}")
            text4.setAlignment(QtCore.Qt.AlignCenter)
            rt4 = QtWidgets.QLabel(f"{plants[3][0]}")
            rt4.setAlignment(QtCore.Qt.AlignCenter)
            rt4.setStyleSheet("font-size:36px")
            self.status4 = QtWidgets.QLabel(f"Water next on: {plants[3][1]}.")
            self.status4.setAlignment(QtCore.Qt.AlignCenter) 
            pic4 = QtWidgets.QLabel(self)
            pic4.setPixmap(QtGui.QPixmap(f"./flowers/pics/{plants[3][2]}.png").scaled(size))
        else:
            text4 = QtWidgets.QLabel(empty_flower)
            text4.setAlignment(QtCore.Qt.AlignCenter)
            rt4 = QtWidgets.QLabel(empty_flower)
            rt4.setAlignment(QtCore.Qt.AlignCenter)
            rt4.setStyleSheet("font-size:36px")
            self.status4 = QtWidgets.QLabel(status_text)
            self.status4.setAlignment(QtCore.Qt.AlignCenter) 
            pic4 = QtWidgets.QLabel()

        layout1 = QtWidgets.QVBoxLayout()
        layout1.addWidget(pic1, 3)
        layout1.addWidget(text1, 1)
        layout1.addWidget(pic3, 3)
        layout1.addWidget(text3, 1)

        layout2 = QtWidgets.QVBoxLayout()
        layout2.addWidget(pic2, 3)
        layout2.addWidget(text2, 1)
        layout2.addWidget(pic4, 3)
        layout2.addWidget(text4, 1)

        if self.plants[0][1] == datetime.date.today():
            self.water1 = QtWidgets.QPushButton("Water Now")
        elif self.plants[0][1] == datetime.date.today() + datetime.timedelta(days=1):
            self.water1 = QtWidgets.QPushButton("Water Tomorrow")
            self.water1.setEnabled(False)
        else:
            self.water1 = QtWidgets.QPushButton("No Plant")
            self.water1.setEnabled(False)
        if self.plants[1][1] == datetime.date.today():
            self.water2 = QtWidgets.QPushButton("Water Now")
        elif self.plants[1][1] == datetime.date.today() + datetime.timedelta(days=1):
            self.water2 = QtWidgets.QPushButton("Water Tomorrow")
            self.water2.setEnabled(False)
        else:
            self.water2 = QtWidgets.QPushButton("No Plant")
            self.water2.setEnabled(False)
        if self.plants[2][1] == datetime.date.today():
            self.water3 = QtWidgets.QPushButton("Water Now")
        elif self.plants[2][1] == datetime.date.today() + datetime.timedelta(days=1):
            self.water3 = QtWidgets.QPushButton("Water Tomorrow")
            self.water3.setEnabled(False)
        else:
            self.water3 = QtWidgets.QPushButton("No Plant")
            self.water3.setEnabled(False)
        if self.plants[3][1] == datetime.date.today():
            self.water4 = QtWidgets.QPushButton("Water Now")
        elif self.plants[3][1] == datetime.date.today() + datetime.timedelta(days=1):
            self.water4 = QtWidgets.QPushButton("Water Tomorrow")
            self.water4.setEnabled(False)
        else:
            self.water4 = QtWidgets.QPushButton("No Plant")
            self.water4.setEnabled(False)
        self.back_button = QtWidgets.QPushButton("Back")
        self.back_button.setStyleSheet(f"""font-size:36px;""")

        butstat1 = QtWidgets.QHBoxLayout()
        butstat1.addWidget(self.status1)
        butstat1.addWidget(self.water1)
        butstat2 = QtWidgets.QHBoxLayout()
        butstat2.addWidget(self.status2)
        butstat2.addWidget(self.water2)
        butstat3 = QtWidgets.QHBoxLayout()
        butstat3.addWidget(self.status3)
        butstat3.addWidget(self.water3)
        butstat4 = QtWidgets.QHBoxLayout()
        butstat4.addWidget(self.status4)
        butstat4.addWidget(self.water4)

        watering_list = QtWidgets.QVBoxLayout()
        watering_list.addWidget(rt1)
        watering_list.addLayout(butstat1)
        watering_list.addWidget(rt2)
        watering_list.addLayout(butstat2)
        watering_list.addWidget(rt3)
        watering_list.addLayout(butstat3)
        watering_list.addWidget(rt4)
        watering_list.addLayout(butstat4)
        watering_list.addWidget(self.back_button)

        layout3 = QtWidgets.QHBoxLayout()
        layout3.addLayout(layout1, 2)
        layout3.addLayout(layout2, 2)
        layout3.addLayout(watering_list, 4)

        main_layout = QtWidgets.QWidget()
        main_layout.setLayout(layout3)
        self.setLayout(layout3)

        self.water1.clicked.connect(self.water_1)
        self.water2.clicked.connect(self.water_2)
        self.water3.clicked.connect(self.water_3)
        self.water4.clicked.connect(self.water_4)

        self.setStyleSheet("""
            QLabel {
                background-color: rgba(0,0,0,200);
                color: white;
                font-size: 16px;
                text-align: center;
                border-width: 10px;
            }
            QPushButton
            {
                color: white;
                background-color: rgba(130, 98, 66, 200);
            }
            QPushButton::hover
            {
                background-color: rgba(130, 98, 66, 230);
            }
        """)

    def water_1(self):
        self.water1.setText("Water Tomorrow")
        self.water1.setEnabled(False)
        self.plants[0][1] = datetime.date.today() + datetime.timedelta(days=1)
        self.status1.setText(f"Water next on: {self.plants[0][1]}.")
    def water_2(self):
        self.water2.setText("Water Tomorrow")
        self.water2.setEnabled(False)
        self.plants[1][1] = datetime.date.today() + datetime.timedelta(days=1)
        self.status2.setText(f"Water next on: {self.plants[1][1]}.")
        with open('savefile.txt', 'wb') as save:
            pickle.dump(self.plants, save)
    def water_3(self):
        self.water3.setText("Water Tomorrow")
        self.water3.setEnabled(False)
        self.plants[2][1] = datetime.date.today() + datetime.timedelta(days=1)
        self.status3.setText(f"Water next on: {self.plants[2][1]}.")
        with open('savefile.txt', 'wb') as save:
            pickle.dump(self.plants, save)
    def water_4(self):
        self.water4.setText("Water Tomorrow")
        self.water4.setEnabled(False)
        self.plants[3][1] = datetime.date.today() + datetime.timedelta(days=1)
        self.status4.setText(f"Water next on: {self.plants[3][1]}.")
        with open('savefile.txt', 'wb') as save:
            pickle.dump(self.plants, save)


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.passed = 0
        self.plant_list = [
            ["Columbine", "c"],
            ["Wild Ginger", "wg"],
            ["Butterfly Weed", "bw"],
            ["White Wood Aster", "wwa"],
            ["New England Aster", "nea"],
            ["Aromatic Aster", "aa"],
            ["Blue Wild Indigo", "bwi"],
            ["Turtlehead", "t"],
            ["Green-and-Gold", "gag"],
            ["Bugbane", "bb"],
            ["Tall Coreopsis", "tc"],
            ["Wild Bleeding Heart", "wbh"],
            ["Joe-pye Weed", "jpw"],
            ["Cranesbill", "cr"],
            ["Common Sneezeweed", "cs"],
            ["Swamp Sunflower", "ss"],
            ["False Sunflower", "fs"],
            ["Alumroot", "al"],
            ["Dwarf Crested Iris", "dci"],
            ["Gayfeather", "g"],
            ["Michigan Lily", "ml"],
            ["Great Blue Lobelia", "gbl"],
            ["Virginia Bluebells", "vb"],
            ["Beebalm", "beebalm"],
            ["Wild Bergamot", "wb"],
            ["Beardtongue", "b"],
            ["Summer Phlox", "sp"],
            ["Jacob's Ladder", "jl"],
            ["Solomon's Seal", "sos"],
            ["Slender Mountain Mint", "smm"],
            ["Black-Eye Susan", "bes"],
            ["Golden Ragwort", "gr"],
            ["Narrow-leaved Blue-Eyed Grass", "nlbeg"],
            ["False Solomon's Seal", "fss"],
            ["Showy Goldenrod", "sg"],
            ["Foam Flower", "ff"],
            ["New York Ironweed", "nyi"],
            ["Culver's Root", "cur"],
        ]
        if self.passed == 1:
            with open('savefile.txt', 'wb') as save:
                pickle.dump(self.plants_selected, save)
        else:    
            try:
                with open('savefile.txt', 'rb') as f:
                    data = pickle.load(f)
                    print("Data loaded.")
                    self.plants_selected = data
            except IOError:
                print("New session. Creating plants_selected")
                self.plants_selected = [[None, None, None, None], [None, None, None, None], [None, None, None, None], [None, None, None, None]]
        self.setGeometry(50, 50, 400, 450)
        oImage = QtGui.QImage("./grass.jpg")
        sImage = oImage.scaled(QtCore.QSize(1280, 720))
        palette = QtGui.QPalette()
        palette.setBrush(QtGui.QPalette.Window, QtGui.QBrush(sImage))                        
        self.setPalette(palette)
        self.setFixedSize(1280, 720)
        self.setWindowTitle("PLANT ENCYCLOPEDIA by Dan")
        self.startMainMenu()



    def startMainMenu(self):
        self.Window = MainMenu(self, self.plant_list)
        self.setCentralWidget(self.Window)
        self.Window.button1.clicked.connect(self.startBrowseMenu)
        self.Window.button2.clicked.connect(self.startBrowseMenuRandom)
        self.Window.button3.clicked.connect(self.startWatering)
        self.Window.button5.clicked.connect(self.startBrowseMenuDisplayed)
        self.Window.button4.clicked.connect(self.exit)
        self.Window.button7.clicked.connect(self.help)
        self.show()

    def startBrowseMenu(self):
        self.Window = BrowseMenu(self, None, self.plant_list, self.plants_selected)
        self.setCentralWidget(self.Window)
        self.Window.back_button.clicked.connect(self.startMainMenu)
        self.Window.add_button.clicked.connect(self.add_to_watering)
        self.passed = 1
        self.show()

    def startBrowseMenuRandom(self):
        num = random.randint(0, len(self.plant_list)-1)
        ran = self.plant_list[num][0]
        self.Window = BrowseMenu(self, ran, self.plant_list, self.plants_selected)
        self.setCentralWidget(self.Window)
        self.passed = 1
        self.Window.back_button.clicked.connect(self.startMainMenu)
        self.show()

    def startBrowseMenuDisplayed(self):
        self.Window = BrowseMenu(self, self.Window.label, self.plant_list, self.plants_selected)
        self.setCentralWidget(self.Window)
        self.Window.back_button.clicked.connect(self.startMainMenu)
        self.passed = 1
        self.show()

    def startWatering(self):
        self.Window = Watering(self, self.plants_selected)
        self.setCentralWidget(self.Window)
        self.Window.back_button.clicked.connect(self.startMainMenu)
        self.passed = 1
        self.show()

    def help(self):
        self.warning = QtWidgets.QMessageBox()
        self.warning.setWindowTitle("How to Use Watering")
        self.warning.setIcon(QtWidgets.QMessageBox.Warning)
        self.warning.setText("""
To add a plant to the watering tracker:
1) Find the plant you wish to add in the "Browse Plants" menu.
2) Click on the "Add to Watering" button.
3) Return to the main menu using the back button.
4) Click on the "Watering" button.
You will now see the plants you have added to the watering tracker.
Press "Water" when you water them, and the app will notify you when to water them next.

To remove a plant from the watering tracker:
1) Navigate to the flower you have added via the "Browse Plants" menu.
2) Click on the "Remove from Watering" button.
The plant you have chosen will be removed from the Watering list.
        """)
        self.warning.setStandardButtons(QtWidgets.QMessageBox.Ok)
        self.warning.show()

    def exit(self):
        with open('savefile.txt', 'wb') as save:
            pickle.dump(self.plants_selected, save)
        exit()

    def show_warning(self):
        self.warning = QtWidgets.QMessageBox()
        self.warning.setWindowTitle("Warning")
        self.warning.setIcon(QtWidgets.QMessageBox.Warning)
        self.warning.setText("You can only add 4 plants.")
        self.warning.setStandardButtons(QtWidgets.QMessageBox.Ok)
        self.warning.show()

    def add_to_watering(self):
        selected = self.Window.menu_widget.selectedItems()[0].text()
        print(f"Adding {selected} to watering")
        for plant in self.plants_selected:
            if plant[0] == None:
                plant[0] = selected
                plant[1] = datetime.date.today()
                plant[2] = self.Window.name
                return
        self.show_warning()
        return

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)

    widget = MainWindow()
    widget.resize(1280, 720)
    widget.show()

    sys.exit(app.exec())