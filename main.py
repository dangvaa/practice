"""Приложение для работы с изображениями"""
import sys
import cv2
import numpy as np
from PyQt5 import QtWidgets
from PyQt5.QtGui import QPixmap, QImage, QFont
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QPushButton,
    QVBoxLayout,
    QFileDialog,
    QMessageBox,
    QInputDialog,
    QWidget,
)


class ImageProcessingApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.cv_image = None
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Обработка фото")

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout()

        self.image_label = QtWidgets.QLabel(self)
        self.image_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.image_label)

        open_image_button = QPushButton("Открыть изображение", self)
        open_image_button.clicked.connect(self.open_image)
        layout.addWidget(open_image_button)

        capture_webcam_button = QPushButton("Сделать снимок с веб-камеры",
                                            self)
        capture_webcam_button.clicked.connect(self.capture_from_webcam)
        layout.addWidget(capture_webcam_button)

        show_red_channel_button = QPushButton("Показать красный канал", self)
        show_red_channel_button.clicked.connect(lambda: self.show_channel(2))
        layout.addWidget(show_red_channel_button)

        show_green_channel_button = QPushButton("Показать зеленый канал",
                                                self)
        show_green_channel_button.clicked.connect(lambda: self.show_channel(1))
        layout.addWidget(show_green_channel_button)

        show_blue_channel_button = QPushButton("Показать синий канал", self)
        show_blue_channel_button.clicked.connect(lambda: self.show_channel(0))
        layout.addWidget(show_blue_channel_button)

        show_negative_button = QPushButton("Показать негативное изображение",
                                           self)
        show_negative_button.clicked.connect(self.show_negative)
        layout.addWidget(show_negative_button)

        apply_gaussian_blur_button = QPushButton(
            "Сделать размытие изображения по Гауссу", self)
        apply_gaussian_blur_button.clicked.connect(self.apply_gaussian_blur)
        layout.addWidget(apply_gaussian_blur_button)

        draw_red_circle_button = QPushButton(
            "Нарисовать круг на изображении красным цветом",
            self)
        draw_red_circle_button.clicked.connect(self.draw_red_circle)
        layout.addWidget(draw_red_circle_button)

        central_widget.setLayout(layout)

        font = QFont()
        font.setPointSize(12)
        style_sheet = "font-size: {}pt;".format(font.pointSize())

        open_image_button.setStyleSheet(style_sheet)
        capture_webcam_button.setStyleSheet(style_sheet)
        show_red_channel_button.setStyleSheet(style_sheet)
        show_green_channel_button.setStyleSheet(style_sheet)
        show_blue_channel_button.setStyleSheet(style_sheet)
        show_negative_button.setStyleSheet(style_sheet)
        apply_gaussian_blur_button.setStyleSheet(style_sheet)
        draw_red_circle_button.setStyleSheet(style_sheet)

    def open_image(self):
        """Открывает изображение на устройстве"""
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Открыть изображение", "", "(*.png *.jpg *.bmp)"
        )
        if file_path:
            self.cv_image = cv2.imread(file_path)
            if self.cv_image is None:
                QMessageBox.critical(self, "Ошибка",
                                     "Ошибка при загрузке изображения")
            else:
                self.display_image(self.cv_image)

    def capture_from_webcam(self):
        """Захват изображения с веб-камеры"""
        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            QMessageBox.critical(
                self,
                "Ошибка",
                "Не удается получить доступ к веб-камере. "
                + "Убедитесь, что она подключена, и повторите попытку.",
            )
            return

        ret, frame = cap.read()
        cap.release()
        if not ret:
            QMessageBox.critical(self, "Ошибка",
                                 "Ошибка при снимке с веб-камеры")
        else:
            self.cv_image = frame
            self.display_image(self.cv_image)

    def display_image(self, cv_image):
        """Функция для отображения изображения в приложении"""
        rgb_image = cv2.cvtColor(cv_image, cv2.COLOR_BGR2RGB)
        h, w, ch = rgb_image.shape
        bytes_per_line = ch * w
        qt_image = QImage(rgb_image.data, w, h,
                          bytes_per_line, QImage.Format_RGB888)
        pixmap = QPixmap.fromImage(qt_image)

        area_width = self.image_label.width()
        area_height = self.image_label.height()

        scaled_pixmap = pixmap.scaled(area_width, area_height, Qt.KeepAspectRatio)
        self.image_label.setPixmap(scaled_pixmap)
        self.image_label.adjustSize()

    def resizeEvent(self, event):
        """Подгоняет размер изображения для приложения"""
        if self.cv_image is not None:
            self.display_image(self.cv_image)

    def show_channel(self, channel):
        """Отображает выбранный цветовой канал"""
        if self.cv_image is None:
            QMessageBox.warning(self, "Предупреждение", "Изображения нет")
            return

        channel_image = np.zeros_like(self.cv_image)
        channel_image[:, :, channel] = self.cv_image[:, :, channel]
        self.display_image(channel_image)

    def show_negative(self):
        """Отображает негативное изображение"""
        if self.cv_image is None:
            QMessageBox.warning(self, "Предупреждение", "Изображения нет")
            return

        negative_image = 255 - self.cv_image
        self.display_image(negative_image)

    def apply_gaussian_blur(self):
        """Делает размытие по Гауссу"""
        if self.cv_image is None:
            QMessageBox.warning(self, "Предупреждение", "Изображения нет")
            return

        kernel_size, ok = QInputDialog.getInt(
            self,
            "Размытие по Гауссу",
            "Введите размер ядра (1-99, нечетное число):",
            min=1,
            max=99,
            step=2,
        )
        if ok:
            if kernel_size % 2 == 0:
                QMessageBox.warning(self, "Предупреждение",
                                    "Введите нечетное число")
                return

            blurred_image = cv2.GaussianBlur(
                self.cv_image, (kernel_size, kernel_size), 0
            )
            self.display_image(blurred_image)

    def draw_red_circle(self):
        """Рисует красный круг на изображении"""
        if self.cv_image is None:
            QMessageBox.warning(self, "Предупреждение", "Изображения нет")
            return

        h, w, _ = self.cv_image.shape
        coord_info = f"Диапазон координат: x [0, {w - 1}], y [0, {h - 1}]"

        x, ok = QInputDialog.getInt(self, "Красный круг",
                                    f"{coord_info}\nВведите координату x:")
        if not ok:
            return
        if x < 0:
            QMessageBox.warning(self, "Ошибка",
                                "Вводите положительные числа")
            return

        y, ok = QInputDialog.getInt(self, "Красный круг",
                                    f"{coord_info}\nВведите координату y:")
        if not ok:
            return
        if y < 0:
            QMessageBox.warning(self, "Ошибка",
                                "Вводите положительные числа")
            return

        radius, ok = QInputDialog.getInt(self, "Красный круг",
                                         "Введите радиус:")
        if not ok:
            return
        if radius <= 0:
            QMessageBox.warning(self, "Ошибка",
                                "Вводите положительные числа")
            return

        if x >= w or y >= h:
            QMessageBox.warning(self, "Предупреждение",
                                "Круг выходит за пределы изображения")
            return

        if radius > min(w, h):
            QMessageBox.warning(self, "Предупреждение",
                                f"Максимальный радиус: {min(w,h)}")
            return

        circled_image = self.cv_image.copy()
        cv2.circle(circled_image, (x, y), radius, (0, 0, 255), -1)
        self.display_image(circled_image)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = ImageProcessingApp()
    main_window.showMaximized()
    sys.exit(app.exec_())