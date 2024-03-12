import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QPushButton, QLabel, QHBoxLayout, QStackedWidget, QVBoxLayout, QTextEdit
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor

class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)

        # Titulo de la ventana
        self.setWindowTitle("Traductor HTML")

        # Color de fondo
        self.setStyleSheet(f"background-color: #637A9F ;")

        self.central_widget = QStackedWidget()
        self.setCentralWidget(self.central_widget)

        # Ventana de inicio (puedes personalizarla según tus necesidades)
        main_widget = Inicio(self)
        main_widget.boton_continuar.clicked.connect(self.continuar)
        self.central_widget.addWidget(main_widget)

        # Otra ventana (por ejemplo, la ventana de búsqueda)
        traductor_widget = TraductorVentana(self)
        traductor_widget.boton_regresar.clicked.connect(self.returning)
        self.central_widget.addWidget(traductor_widget)

    def continuar(self):
        # Cambia a la ventana de búsqueda
        self.central_widget.setCurrentIndex(1)

    def returning(self):
        # Regresa a la ventana de inicio
        self.central_widget.setCurrentIndex(0)

def hex_darken( hex_color, factor=0.7):
    """
    Genera un color ligeramente más oscuro a partir de un código de color hexadecimal.

    :param hex_color: Cadena que representa el código de color hexadecimal.
    :param factor: Factor de oscurecimiento, un valor entre 0 y 1.
    """
    # Asegúrate de que la cadena comience con '#'
    if not hex_color.startswith('#'):
        return hex_color

    # Convierte el código hexadecimal a valores RGB
    rgb_color = tuple(int(hex_color[i:i+2], 16) for i in (1, 3, 5))
    
    # Aplica el factor de oscurecimiento
    r, g, b = rgb_color
    r_nuevo = max(0, int(r * factor))
    g_nuevo = max(0, int(g * factor))
    b_nuevo = max(0, int(b * factor))

    nuevo_hex_color = "#{:02X}{:02X}{:02X}".format(r_nuevo, g_nuevo, b_nuevo)

    return nuevo_hex_color

def cambiar_estilo(boton, font_size, hover=True):
    color_normal = "#C9D7DD"
    if hover: # Si el mouse está sobre el botón
        # Aumentar tamaño, cambiar color de fondo y color de texto
        color_dark = hex_darken(color_normal)
        boton.setStyleSheet(f"background-color: {color_dark}; color: white; font-size: {font_size}px;")
    else:
        boton.setStyleSheet(f"background-color: {color_normal}; color: black; font-size: {font_size}px;")

class Inicio(QWidget):
    def __init__(self, parent=None):
        super(Inicio, self).__init__(parent)

        self.setWindowTitle("Editor HTML")
        
        # Etiqueta con el nombre del curso y la sección
        self.etiqueta_curso_seccion = QLabel(
            "Daved Abshalon Ejcalon Chonay\nCurso: Lenguajes Formales y de Programación\nSección: B+"
        )
        self.etiqueta_curso_seccion.setStyleSheet("color: white; font-size: 15px; font-weight: bold;")

        # Botón para salir de la aplicación
        self.boton_salir = QPushButton("Salir")
        self.boton_salir.clicked.connect(self.salir)

        # Botón para continuar
        self.boton_continuar = QPushButton("Continuar")

        # Estilos de boton
        for btn in [self.boton_salir, self.boton_continuar]:
            btn.setStyleSheet("background-color: #C9D7DD; color: black; font-size: 12px")
            btn.setCursor(Qt.CursorShape.PointingHandCursor)
            btn.enterEvent = lambda event, boton=btn: cambiar_estilo(boton, 12, True)
            btn.leaveEvent = lambda event, boton=btn: cambiar_estilo(boton, 12, False)

        layout = QVBoxLayout()
        layout.addWidget(self.etiqueta_curso_seccion)
        layout.addWidget(self.boton_continuar)
        layout.addWidget(self.boton_salir)

        # Centrar el contenido
        layout.setAlignment(self.etiqueta_curso_seccion, Qt.AlignmentFlag.AlignCenter)

        self.setLayout(layout)

    def salir(self):
        # Salir de la aplicación
        sys.exit()

class TraductorVentana(QWidget):
    def __init__(self, parent=None):
        super(TraductorVentana, self).__init__(parent)
        self.setWindowTitle("Traductor HTML")

        # Cuadro de texto para ingresar el archivo de texto de entrada
        self.entrada_texto = QTextEdit()
        self.entrada_texto.setPlaceholderText("Ingrese el texto a traducir")
        self.entrada_texto.setStyleSheet("background-color: white;")

        self.etiqueta_entrada = QLabel("Ingreso de Texto a Traducir")
        self.etiqueta_entrada.setStyleSheet("color: white; font-size: 15px; font-weight: bold;")


        # Cuadro de texto para mostrar el resultado de la traducción
        self.salida_texto = QTextEdit()
        self.salida_texto.setPlaceholderText("Resultado de la traducción")
        self.salida_texto.setStyleSheet("background-color: white;")
        self.salida_texto.setReadOnly(True) # No se puede editar

        self.etiqueta_salida = QLabel("Resultado de Traducción")
        self.etiqueta_salida.setStyleSheet("color: white; font-size: 15px; font-weight: bold;")

        # Botón para añadir archivo
        self.boton_anadir_archivo = QPushButton("Añadir Archivo")

        # Botón para traducir
        self.boton_traducir = QPushButton("Traducir")
        
        # Botón para regresar a la ventana de inicio
        self.boton_regresar = QPushButton("Regresar a Inicio")

        # Estilos de boton
        for btn in [self.boton_anadir_archivo, self.boton_traducir, self.boton_regresar]:
            btn.setStyleSheet("background-color: #C9D7DD; color: black; font-size: 12px")
            btn.setCursor(Qt.CursorShape.PointingHandCursor)
            btn.enterEvent = lambda event, boton=btn: cambiar_estilo(boton, 12, True)
            btn.leaveEvent = lambda event, boton=btn: cambiar_estilo(boton, 12, False)

        layout_titulo = QHBoxLayout()
        layout_titulo.addWidget(self.etiqueta_salida)
        layout_titulo.addWidget(self.etiqueta_entrada)
        layout_titulo.setAlignment(self.etiqueta_salida, Qt.AlignmentFlag.AlignCenter)

        layout_entrada = QVBoxLayout()
        layout_entrada.addWidget(self.entrada_texto) # QeditText
        layout_entrada.addWidget(self.boton_anadir_archivo)
        layout_entrada.addWidget(self.boton_traducir)

        layout_salida = QVBoxLayout()
        layout_salida.addWidget(self.salida_texto) # QeditText
        layout_salida.addWidget(self.boton_regresar)

        layout_orden = QHBoxLayout()
        layout_orden.addLayout(layout_entrada)
        layout_orden.addLayout(layout_salida)

        layout_principal = QVBoxLayout()
        layout_principal.addLayout(layout_titulo)
        layout_principal.addLayout(layout_orden)

        self.setLayout(layout_principal)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())