import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QPushButton, QLabel, QHBoxLayout, QStackedWidget, QVBoxLayout, QTextEdit, QFileDialog, QMessageBox
from PyQt6.QtCore import Qt

class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setWindowTitle("Traductor HTML")
        self.setStyleSheet("background-color: #121212; color: #FFFFFF;")

        self.central_widget = QStackedWidget()
        self.setCentralWidget(self.central_widget)

        main_widget = Inicio(self)
        main_widget.boton_continuar.clicked.connect(self.continuar)
        self.central_widget.addWidget(main_widget)

        traductor_widget = TraductorVentana(self)
        traductor_widget.boton_regresar.clicked.connect(self.returning)
        self.central_widget.addWidget(traductor_widget)

    def continuar(self):
        self.central_widget.setCurrentIndex(1)

    def returning(self):
        self.central_widget.setCurrentIndex(0)

def hex_lighten(hex_color, factor=0.5):
    if not hex_color.startswith('#'):
        return hex_color

    rgb_color = tuple(int(hex_color[i:i+2], 16) for i in (1, 3, 5))
    r, g, b = rgb_color
    r_nuevo = min(255, int(r + (255 - r) * factor))
    g_nuevo = min(255, int(g + (255 - g) * factor))
    b_nuevo = min(255, int(b + (255 - b) * factor))

    nuevo_hex_color = "#{:02X}{:02X}{:02X}".format(r_nuevo, g_nuevo, b_nuevo)

    return nuevo_hex_color

def cambiar_estilo(boton, font_size, hover=True):
    color_normal = "#424242"
    if hover:
        color_light = hex_lighten(color_normal)
        boton.setStyleSheet(f"background-color: {color_light}; color: #FFFFFF; font-size: {font_size}px;")
    else:
        boton.setStyleSheet(f"background-color: {color_normal}; color: #FFFFFF; font-size: {font_size}px;")

class Inicio(QWidget):
    def __init__(self, parent=None):
        super(Inicio, self).__init__(parent)
        self.setWindowTitle("Editor HTML")
        
        self.etiqueta_curso_seccion = QLabel(
            "Daved Abshalon Ejcalon Chonay\nCurso: Lenguajes Formales y de Programación\nSección: B+"
        )
        self.etiqueta_curso_seccion.setStyleSheet("color: #FFFFFF; font-size: 15px; font-weight: bold;")
        self.etiqueta_curso_seccion.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.boton_salir = QPushButton("Salir")
        self.boton_salir.clicked.connect(self.salir)

        self.boton_continuar = QPushButton("Continuar")

        for btn in [self.boton_salir, self.boton_continuar]:
            btn.setStyleSheet("background-color: #616161; color: #FFFFFF; font-size: 12px")
            btn.setCursor(Qt.CursorShape.PointingHandCursor)
            btn.enterEvent = lambda event, boton=btn: cambiar_estilo(boton, 12, True)
            btn.leaveEvent = lambda event, boton=btn: cambiar_estilo(boton, 12, False)

        layout = QVBoxLayout()
        layout.addWidget(self.etiqueta_curso_seccion)
        layout.addWidget(self.boton_continuar)
        layout.addWidget(self.boton_salir)

        self.setLayout(layout)

    def salir(self):
        sys.exit()

class TraductorVentana(QWidget):
    def __init__(self, parent=None):
        super(TraductorVentana, self).__init__(parent)
        self.setWindowTitle("Traductor HTML")

        self.entrada_texto = QTextEdit()
        self.entrada_texto.setPlaceholderText("Ingrese el texto a traducir")
        self.entrada_texto.setStyleSheet("background-color: #424242; color: #FFFFFF;")

        self.etiqueta_entrada = QLabel("RESULTADO HTML")
        self.etiqueta_entrada.setStyleSheet("color: #FFFFFF; font-size: 15px; font-weight: bold;")
        self.etiqueta_entrada.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.salida_texto = QTextEdit()
        self.salida_texto.setPlaceholderText("Resultado de la traducción")
        self.salida_texto.setStyleSheet("background-color: #424242; color: #FFFFFF;")
        self.salida_texto.setReadOnly(True)

        self.etiqueta_salida = QLabel("TEXTO JSON")
        self.etiqueta_salida.setStyleSheet("color: #FFFFFF; font-size: 15px; font-weight: bold;")
        self.etiqueta_salida.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.boton_anadir_archivo = QPushButton("Añadir Archivo")
        self.boton_anadir_archivo.clicked.connect(self.abrir_explorador_archivos)  

        self.boton_traducir = QPushButton("Traducir")
        
        self.boton_regresar = QPushButton("Regresar a Inicio")

        self.boton_guardar_archivo = QPushButton("Guardar Archivo")
        self.boton_guardar_archivo.clicked.connect(self.guardar_archivo)
        
        for btn in [self.boton_anadir_archivo, self.boton_traducir, self.boton_regresar, self.boton_guardar_archivo]:
            btn.setStyleSheet("background-color: #616161; color: #FFFFFF; font-size: 12px")
            btn.setCursor(Qt.CursorShape.PointingHandCursor)
            btn.enterEvent = lambda event, boton=btn: cambiar_estilo(boton, 12, True)
            btn.leaveEvent = lambda event, boton=btn: cambiar_estilo(boton, 12, False)

        layout_titulo = QHBoxLayout()
        layout_titulo.addWidget(self.etiqueta_salida)
        layout_titulo.addWidget(self.etiqueta_entrada)
        layout_titulo.setAlignment(self.etiqueta_salida, Qt.AlignmentFlag.AlignCenter)

        layout_entrada = QVBoxLayout()
        layout_entrada.addWidget(self.entrada_texto)
        layout_entrada.addWidget(self.boton_anadir_archivo)
        layout_entrada.addWidget(self.boton_traducir)

        layout_salida = QVBoxLayout()
        layout_salida.addWidget(self.salida_texto)
        layout_salida.addWidget(self.boton_guardar_archivo)
        layout_salida.addWidget(self.boton_regresar)

        layout_orden = QHBoxLayout()
        layout_orden.addLayout(layout_entrada)
        layout_orden.addLayout(layout_salida)

        layout_principal = QVBoxLayout()
        layout_principal.addLayout(layout_titulo)
        layout_principal.addLayout(layout_orden)

        self.setLayout(layout_principal)

    def abrir_explorador_archivos(self):
        """
        Abre el explorador de archivos para seleccionar un archivo JSON.
        """
        file_dialog = QFileDialog(self)
        file_path, _ = file_dialog.getOpenFileName(self, "Abrir Archivo", "", "Archivos JSON (*.json)")
        if file_path:  
            with open(file_path, 'r') as file:
                json_data = file.read()
                self.entrada_texto.setPlainText(json_data)

    def guardar_archivo(self):
        """
        Guarda el contenido de la caja de texto de salida en un archivo HTML.
        """
        file_dialog = QFileDialog(self)
        file_path, _ = file_dialog.getSaveFileName(self, "Guardar Archivo", "", "Archivos HTML (*.html)")
        if file_path:
            with open(file_path, 'w') as file:
                file.write(self.salida_texto.toPlainText())

            QMessageBox.information(self, "Archivo Guardado", "El archivo se ha guardado correctamente.", QMessageBox.StandardButton.Ok)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
