import sys
from PySide6.QtWidgets import QApplication, QLabel, QWidget, QVBoxLayout, QTextEdit
from PySide6.QtGui import QTextCharFormat, QColor, QTextCursor
from PySide6.QtCore import Qt, Signal  # Importamos Signal
#dividelo para un vector en python que los elementos nos sean muy largos
vectorText = [
"this change addresses safety concerns in emergencies, such as crashes or power failures",
    "all new models must have exterior door handles with mechanical redundancy and sufficient operating space",
    "When Stunning or inflicting attribute Anomaly on an enemy",
    "All squad members gain 1 dexterity Count, stacking up to 3 times",
    "Police labor activities are normally conducted in pairs",
    "you lack what it takes to win this war",
    "Upcoming character shown briefly but otherwise the story presence is very minimal",
    "might make an appearance during the averyone is here moment",
    "Police labor activities are normally conducted in pairs",
    "So could the 1st Unit go on watch while we go home?",
    "You should've gotten it long ago","By withholding the facts from us",
    "schedule"
]


class CustonLineEdit(QTextEdit):
    # 1. Definimos una señal personalizada para avisar cuando se pulse Enter
    returnPressed = Signal()

    def __init__(self, indiceaux):
        super().__init__()
        self.indice = indiceaux
        self.setFixedHeight(50)  # Aumenté un poco la altura para que se vea bien
        self.setTabChangesFocus(True)

        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        self.setLineWrapMode(QTextEdit.NoWrap)

        self.textChanged.connect(self.resaltar_letra)

    # 2. Capturamos el evento AQUÍ, dentro del widget que tiene el foco
    def keyPressEvent(self, event):
        if event.key() in (Qt.Key_Return, Qt.Key_Enter):
            # Si es Enter, emitimos la señal y NO llamamos al super (para evitar el salto de línea)
            self.returnPressed.emit()
        else:
            # Si es cualquier otra tecla, dejamos que el QTextEdit funcione normal
            super().keyPressEvent(event)

    def resaltar_letra(self):
        self.blockSignals(True)
        cursor = self.textCursor()
        posicion = cursor.position()
        texto = self.toPlainText()

        # Obtenemos el texto de referencia usando la funcion self.indice()
        idx = self.indice()
        if idx < len(vectorText):
            texto2 = vectorText[idx]
        else:
            texto2 = ""

        # Limpiamos formato
        cursor.select(QTextCursor.SelectionType.Document)
        cursor.setCharFormat(QTextCharFormat())

        # Nuevo formato en rojo
        formato = QTextCharFormat()
        formato.setForeground(QColor("White"))
        formato.setBackground(QColor("Red"))

        i = 0
        longitud = len(texto)

        while i < longitud:
            # CORRECCIÓN IMPORTANTE: Verificar que no nos pasemos del largo del texto original
            if i >= len(texto2):
                # Si escribimos más que la frase original, marcamos
                cursor.setPosition(i)
                cursor.movePosition(QTextCursor.Right, QTextCursor.KeepAnchor)
                cursor.setCharFormat(formato)
            else:
                char1 = texto[i]
                char2 = texto2[i]

                if char1 != char2:
                    cursor.setPosition(i)
                    cursor.movePosition(QTextCursor.Right, QTextCursor.KeepAnchor)
                    cursor.setCharFormat(formato)

            i += 1

        cursor.setPosition(posicion)
        self.setTextCursor(cursor)
        self.blockSignals(False)


class VentanaPrinci(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("KerTipping")
        self.resize(600, 300)
        self.indice = 0
        layout = QVBoxLayout()

        self.etiqueta1 = QLabel("Escribe esto:")
        self.etiqueta2 = QLabel(vectorText[self.indice])
        self.etiqueta5 = QLabel("")

        self.etiqueta2.setWordWrap(True)

        # Pasamos la función self.getIndice
        self.Endatos = CustonLineEdit(self.getIndice)

        # CONECTAMOS LA SEÑAL DEL HIJO A LA FUNCIÓN DEL PADRE
        self.Endatos.returnPressed.connect(self.ejeDos)

        # Estilos
        self.setStyleSheet("""background-color: #1A1A1A; color: white;""")
        self.etiqueta1.setStyleSheet("font-size: 20px; color: white; font-weight: bold; ")
        self.etiqueta2.setStyleSheet("""
                    font-size: 18px; 
                    color: #bdc3c7; 
                    font-family: Helvetica;
                    padding: 10px;
                    border: 3px solid #707070;
                    border-radius: 10px;
                    background-color: #424242;
                """)
        self.etiqueta5.setStyleSheet("font-size: 14px; font-weight: bold;")
        self.Endatos.setStyleSheet("""
                    QTextEdit {
                        font-size: 18px;
                        border: 2px solid #3498db;
                        border-radius: 8px;
                        background-color: #222;
                        color: white;
                    }
                """)

        layout.addWidget(self.etiqueta1)
        layout.addWidget(self.etiqueta2)
        layout.addWidget(self.Endatos)
        layout.addWidget(self.etiqueta5)
        self.setLayout(layout)

    def cambiartexto(self):
        if self.indice < len(vectorText):
            nuevoInd = vectorText[self.indice]
            self.etiqueta2.setText(nuevoInd)
            self.Endatos.clear()
            self.etiqueta5.setText("")  # Limpiar mensaje de estado
        else:
            self.etiqueta2.setText("¡Fin del ejercicio!")
            self.Endatos.setDisabled(True)

    def sonIguales(self):
        # CORRECCIÓN: QTextEdit usa toPlainText(), no text()
        textoUsua = self.Endatos.toPlainText().strip()  # .strip() quita espacios extra al final

        if self.indice < len(vectorText):
            textRef = vectorText[self.indice]
        else:
            return False

        if textRef == textoUsua:
            self.etiqueta5.setText("¡Correcto!")
            self.etiqueta5.setStyleSheet("color: #2ecc71; font-size: 15px; font-weight: bold;")
            return True
        else:
            self.etiqueta5.setText("Error: El texto no coincide exactamente.")
            self.etiqueta5.setStyleSheet("color: #e74c3c; font-size: 15px; font-weight: bold;")
            return False

    def ejeDos(self):
        flag = self.sonIguales()
        if flag:
            self.indice += 1
            self.cambiartexto()

    def getIndice(self):
        return self.indice


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana = VentanaPrinci()
    ventana.show()
    sys.exit(app.exec())