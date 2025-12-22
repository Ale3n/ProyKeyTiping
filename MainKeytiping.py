import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QLabel, QWidget, QVBoxLayout,QLineEdit


vectorText = [ "El sol de Venezuela es mucho mas azul, dice y senala al cielo tras terminar el ensayo de La fuerza del destino, una opera de Giuseppe Verdi.",

    "La obra narra un amor desventurado en medio de la guerra y aborda temas como el hambre, el poder y el exilio, realidades que Luis conoce de primera mano.",

    "Hace siete anos, debido a la precariedad en la que vivia, Luis tuvo que salir de Venezuela y dejar atras su vida cotidiana.",

    "A pesar de tener un trabajo estable y un sueldo en su pais, el dinero solo le alcanzaba para cubrir la comida del dia.",

    "En ese momento, Luis dudaba si debia abandonar su sueno de ser cantante lirico, inspirado por el peruano Juan Diego Florez.",

    "La otra opcion era viajar a Argentina para trabajar en una carniceria, una de las pocas alternativas laborales que tenia aseguradas.",

    "Finalmente decidio hacer el intento y no renunciar a su profundo deseo de cantar.",

    "Para ello, comenzo a escribir a figuras del mundo musical venezolano que residian en el exterior en busca de ayuda.",

    "Entre ellas estaba la pianista venezolana Gabriela Montero, reconocida internacionalmente por sus presentaciones en eventos de gran relevancia."]
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
        self.Endatos = QLineEdit()

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
        self.Endatos.returnPressed.connect(self.ejeDos)


        layout.addWidget(self.etiqueta1)
        layout.addWidget(self.etiqueta2)
        layout.addWidget(self.etiqueta5)
        layout.addWidget(self.Endatos)
        self.setLayout(layout)



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



app = QApplication(sys.argv)
ventana = VentanaPrinci()
ventana.show()
app.exit(app.exec())