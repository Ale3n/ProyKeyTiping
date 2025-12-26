import sys
from PySide6.QtWidgets import QApplication, QLabel, QWidget, QVBoxLayout, QTextEdit
from PySide6.QtGui import QTextCharFormat, QColor, QTextCursor
from PySide6.QtCore import Qt, Signal  # Importamos Signal

vectorText = [
    "El sol de Venezuela es mucho mas azul, dice y senala al cielo tras terminar el ensayo de La fuerza del destino, una opera de Giuseppe Verdi.",
    "La obra narra un amor desventurado en medio de la guerra y aborda temas como el hambre, el poder y el exilio, realidades que Luis conoce de primera mano.",
    "Hace siete anos, debido a la precariedad en la que vivia, Luis tuvo que salir de Venezuela y dejar atras su vida cotidiana.",
    "A pesar de tener un trabajo estable y un sueldo en su pais, el dinero solo le alcanzaba para cubrir la comida del dia.",
    "En ese momento, Luis dudaba si debia abandonar su sueno de ser cantante lirico, inspirado por el peruano Juan Diego Florez.",
    "La otra opcion era viajar a Argentina para trabajar en una carniceria, una de las pocas alternativas laborales que tenia aseguradas.",
    "Finalmente decidio hacer el intento y no renunciar a su profundo deseo de cantar.",
    "Para ello, comenzo a escribir a figuras del mundo musical venezolano que residian en el exterior en busca de ayuda.",
    "Entre ellas estaba la pianista venezolana Gabriela Montero, reconocida internacionalmente por sus presentaciones en eventos de gran relevancia."
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

                if char1.lower() != char2.lower():
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
        self.setStyleSheet("""background-color: black; color: white;""")
        self.etiqueta1.setStyleSheet("font-size: 20px; color: blue; font-weight: bold; ")
        self.etiqueta2.setStyleSheet("""
                    font-size: 18px; 
                    color: #bdc3c7; 
                    font-family: Verdana;
                    padding: 10px;
                    border: 1px solid #444;
                    border-radius: 5px;
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