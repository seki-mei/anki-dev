from aqt import mw, gui_hooks
from PyQt6.QtWidgets import QDialog, QLabel, QVBoxLayout
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap, QKeyEvent
import os
import random
from typing import Any

config: dict[str, Any] = mw.addonManager.getConfig(__name__)
ADDON_DIR: str = os.path.dirname(__file__)
IMAGES_DIR: str = os.path.join(ADDON_DIR, "user_files/images")

TESTING: bool = config["test"]
NORMAL_CHANCE: float = config["normal_prob"]
AGAIN_CHANCE: float = config["again_prob"]
HARD_CHANCE: float = NORMAL_CHANCE
EASY_CHANCE: float= NORMAL_CHANCE


def pick_random_image() -> str:
    files = [f for f in os.listdir(IMAGES_DIR)
             if os.path.isfile(os.path.join(IMAGES_DIR, f))]  # filter files
    return os.path.join(IMAGES_DIR, random.choice(files))


class WellDoneDialog(QDialog):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)

        self.setModal(True)  # prevent input in other windows
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
    if random.random() <= chance:
        dialog = WellDoneDialog(mw)
        dialog.show()


def test_on_startup() -> None:
    dialog_launcher(1.0 if TESTING else 0.0)  # 100% chance if testing, 0% if not


def answered_popup(reviewer, card, ease: int) -> None:
    chance = (0, AGAIN_CHANCE, HARD_CHANCE, NORMAL_CHANCE, EASY_CHANCE)[ease]
    dialog_launcher(chance)


gui_hooks.main_window_did_init.append(test_on_startup)
gui_hooks.reviewer_did_answer_card.append(answered_popup)