from aqt import mw, gui_hooks
from aqt.utils import showInfo
from PyQt6.QtWidgets import QDialog, QLabel, QVBoxLayout
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap, QKeyEvent
import os
import random
from typing import Any

config: dict[str, Any] = mw.addonManager.getConfig(__name__)
ADDON_DIR: str = os.path.dirname(__file__)
IMAGES_DIR: str = os.path.join(ADDON_DIR, "user_files/images")

TESTING: bool = config.get("test", False)
NORMAL_CHANCE: float = config.get("normal_prob", 0.2)
AGAIN_CHANCE: float = config.get("again_prob", NORMAL_CHANCE)
HARD_CHANCE: float = config.get("hard_prob", NORMAL_CHANCE)
EASY_CHANCE: float = config.get("easy_prob", NORMAL_CHANCE)

ERROR_HEADER: str = "anianki addon:\n"

def images_dir_safe() -> bool:
    if not os.path.isdir(IMAGES_DIR): ## dir doesn't exist
        showInfo(ERROR_HEADER+"images folder doesn't exist\ncan't run anianki")
        return False
    if not os.listdir(IMAGES_DIR): ## dir empty
        showInfo(ERROR_HEADER+"images folder empty")
        return False
    return True


def pick_random_image() -> str:
    files = [f for f in os.listdir(IMAGES_DIR)
             if os.path.isfile(os.path.join(IMAGES_DIR, f))]  # filter files, no folders
    return os.path.join(IMAGES_DIR, random.choice(files))


class WellDoneDialog(QDialog):
    def __init__(self, image_path: str, parent=None) -> None:
        super().__init__(parent)

        self.setModal(True)  # prevent input in other windows
        self.setWindowFlags(
            Qt.WindowType.Tool | Qt.WindowType.FramelessWindowHint
        )
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

        layout = QVBoxLayout(self)

        label = QLabel(self)
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        pixmap = QPixmap(image_path)

        screen = self.screen()
        if screen is not None:
            geom = screen.availableGeometry()
            max_width = int(geom.width())
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

    def keyPressEvent(self, event: QKeyEvent) -> None:
        close_keys = (Qt.Key.Key_Return,
                      Qt.Key.Key_Enter,
                      Qt.Key.Key_Space)
        if event.key() in close_keys:
            self.close()
        else:
            super().keyPressEvent(event)


def dialog_launcher(chance:float) -> None:
    if random.random() <= chance and images_dir_safe():

        # user should be told if we tried to load an unsupported image
        image_path: str = pick_random_image()
        pixmap = QPixmap(image_path)
        if pixmap.isNull():
            showInfo(ERROR_HEADER+"couldn't load file\n"+image_path+"\nfiletype might be unsupported")
            return

        dialog = WellDoneDialog(image_path, mw)
        dialog.show()


def test_on_startup() -> None:
    dialog_launcher(1.0 if TESTING else 0.0)


def answered_popup(reviewer, card, ease: int) -> None:
    chance = (0, AGAIN_CHANCE, HARD_CHANCE, NORMAL_CHANCE, EASY_CHANCE)[ease]
    dialog_launcher(chance)

gui_hooks.main_window_did_init.append(test_on_startup)
gui_hooks.reviewer_did_answer_card.append(answered_popup)