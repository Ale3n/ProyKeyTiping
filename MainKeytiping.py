import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QLabel, QWidget, QVBoxLayout,QLineEdit,QApplication, QTextEdit
from PySide6.QtGui import QTextCharFormat, QColor, QTextCursor
from PySide6.QtCore import Qt


vectorText = [ "El sol de Venezuela es mucho mas azul, dice y senala al cielo tras terminar el ensayo de La fuerza del destino, una opera de Giuseppe Verdi.",

    "La obra narra un amor desventurado en medio de la guerra y aborda temas como el hambre, el poder y el exilio, realidades que Luis conoce de primera mano.",

    "Hace siete anos, debido a la precariedad en la que vivia, Luis tuvo que salir de Venezuela y dejar atras su vida cotidiana.",

    "A pesar de tener un trabajo estable y un sueldo en su pais, el dinero solo le alcanzaba para cubrir la comida del dia.",

    "En ese momento, Luis dudaba si debia abandonar su sueno de ser cantante lirico, inspirado por el peruano Juan Diego Florez.",

    "La otra opcion era viajar a Argentina para trabajar en una carniceria, una de las pocas alternativas laborales que tenia aseguradas.",

    "Finalmente decidio hacer el intento y no renunciar a su profundo deseo de cantar.",

    "Para ello, comenzo a escribir a figuras del mundo musical venezolano que residian en el exterior en busca de ayuda.",

    "Entre ellas estaba la pianista venezolana Gabriela Montero, reconocida internacionalmente por sus presentaciones en eventos de gran relevancia."]
class CustonLineEdit(QTextEdit):
    def __init__(self,indiceaux):
        super().__init__()
        self.indice = indiceaux
        self.setFixedHeight(35)
        self.setTabChangesFocus(True)

        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        self.setLineWrapMode(QTextEdit.NoWrap)

        self.textChanged.connect(self.resaltar_letra)


    def resaltar_letra(self):
        self.blockSignals(True)
        cursor = self.textCursor()
        posicion = cursor.position()
        texto = self.toPlainText()
        texto2 = vectorText[self.indice()]

        #limpiamos formato
        cursor.select(QTextCursor.SelectionType.Document)
        cursor.setCharFormat(QTextCharFormat())

        #nuevo formato en rojo
        formato = QTextCharFormat()
        formato.setForeground(QColor("White"))
        formato.setBackground(QColor("Red"))

        i = 0
        longitud = len(texto)

        while i < longitud:
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
        self.resize(500,300)
        self.indice = 0
        layout = QVBoxLayout()
        self.etiqueta1 = QLabel("Escribe esto")
        self.etiqueta2 = QLabel(vectorText[self.indice])
        self.etiqueta5 = QLabel("verdadero")
        self.etiqueta2.setWordWrap(True)
        self.Endatos = CustonLineEdit(self.getIndice)

        self.setStyleSheet("""background-color: black; color: white;""")
        self.etiqueta1.setStyleSheet("font-size: 20px; color: blue; font-weight: bold; ")
        self.etiqueta2.setStyleSheet("""
                    font-size: 20px; 
                    color: #2c3e50; 
                    font-family: Verdana;
                    font-weight: bold;
                    padding: 10px;
                    background-color: black; /* Fondo gris claro */
                    border-radius: 5px;
                """)
        self.etiqueta5.setStyleSheet("font-size: 10px; color: green")
        self.Endatos.setStyleSheet("""
                    QLineEdit {
                        height: 40px;        /* Aquí cambias la altura del input */
                        font-size: 16px;     /* Tamaño de letra al escribir */
                        border: 2px solid #3498db;
                        border-radius: 8px;
                        padding-left: 10px;
                    }
                """)
        #self.indice += 1
        #self.Endatos.returnPressed.connect()
        layout.addWidget(self.etiqueta1)
        layout.addWidget(self.etiqueta2)
        layout.addWidget(self.etiqueta5)
        layout.addWidget(self.Endatos)
        self.setLayout(layout)
    def keyPressEvent(self, event):
        # Bloquear ENTER para que sea una sola línea
        if event.key() in (Qt.Key_Return, Qt.Key_Enter):
            #print("ENTER presionado")
            self.ejeDos()
            return
        super().keyPressEvent(event)

    def cambiartexto(self):
        if self.indice < len(vectorText):
            nuevoInd = vectorText[self.indice]
            self.etiqueta2.setText(nuevoInd)
            self.Endatos.clear()
        else:
            self.etiqueta2.setText("No hay mas texto")
            self.Endatos.setDisabled(True)

    def sonIguales(self):
        textoUsua = self.Endatos.text()
        if self.indice < len(vectorText):
            textRef = vectorText[self.indice]
        else:
            return False

        if textRef == textoUsua:
            self.etiqueta5.setText("Verdadero - Correcto")
            self.etiqueta5.setStyleSheet("color: green; font-size: 15px;")
            return True
        else:
            self.etiqueta5.setText("Falso - Intenta de nuevo")
            self.etiqueta5.setStyleSheet("color: red; font-size: 15px;")
            #self.Endatos.setDisabled(True)
            return False

    def ejeDos(self):
        flag = self.sonIguales()
        if flag:
            self.indice += 1
            self.cambiartexto()

    def getIndice(self):
        return self.indice



app = QApplication(sys.argv)
ventana = VentanaPrinci()
ventana.show()
app.exit(app.exec())