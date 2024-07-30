import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QMessageBox

def show_message():
    QMessageBox.information(window, 'Message', 'You clicked the button!')

app = QApplication(sys.argv)
window = QWidget()
window.setWindowTitle('PyQt5 Example')
window.setGeometry(240, 120, 720, 480)

button = QPushButton('Click Me', window)
button.clicked.connect(show_message)
button.resize(button.sizeHint())
button.move(100, 30)

window.show()
sys.exit(app.exec_())