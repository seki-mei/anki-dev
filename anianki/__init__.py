from aqt import mw

from PyQt6.QtWidgets import QDialog, QLabel, QVBoxLayout
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt
import os, random

ADDON_DIR = os.path.dirname(__file__)
IMAGES_DIR = os.path.join(ADDON_DIR, "images")
IMAGE_PATH = os.path.join(IMAGES_DIR, "snow.png")

TESTING = True

NORMAL_CHANCE = 0.50
AGAIN_CHANCE  = 0.2
HARD_CHANCE   = NORMAL_CHANCE
EASY_CHANCE   = NORMAL_CHANCE


def pick_random_image():
    files = [f for f in os.listdir(IMAGES_DIR)
             if os.path.isfile(os.path.join(IMAGES_DIR, f))] # filter files
    return os.path.join(IMAGES_DIR, random.choice(files))


class WellDoneDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setModal(True) # prevent input in other windows
        self.setWindowFlags(
            Qt.WindowType.Tool | Qt.WindowType.FramelessWindowHint
        )
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

        layout = QVBoxLayout(self)

        label = QLabel(self)
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        pixmap = QPixmap(pick_random_image())

        screen = self.screen()
        if screen is not None:
            geom = screen.availableGeometry()
            max_width  = int(geom.width())
            max_height = int(geom.height())
            if pixmap.width() > max_width or pixmap.height() > max_height:
                pixmap = pixmap.scaled(
                    max_width,
                    max_height,
                    Qt.AspectRatioMode.KeepAspectRatio,
                    Qt.TransformationMode.SmoothTransformation
                )

        label.setPixmap(pixmap)
        layout.addWidget(label)

        self.adjustSize()

    def keyPressEvent(self, event):
        if event.key() in (Qt.Key.Key_Return, Qt.Key.Key_Enter, Qt.Key.Key_Space):
            self.close()
        else:
            super().keyPressEvent(event)

def dialog_launcher(chance):
    if random.random() <= chance:
        dialog = WellDoneDialog(mw)
        dialog.show()

def testOnStartup():
    dialog_launcher(float(TESTING)) # 100% chance if testing, 0% if not

def answered_popup(reviewer, card, ease):
    chance = (0, AGAIN_CHANCE, HARD_CHANCE, NORMAL_CHANCE, EASY_CHANCE)[ease]
    dialog_launcher(chance)

# Hook into Ani
from aqt import gui_hooks
gui_hooks.main_window_did_init.append(testOnStartup)
gui_hooks.reviewer_did_answer_card.append(answered_popup)