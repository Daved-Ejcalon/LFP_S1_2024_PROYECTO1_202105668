from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QPushButton, QLabel, QHBoxLayout, QStackedWidget, QVBoxLayout, QTextEdit, QFileDialog, QMessageBox
from PyQt6.QtCore import Qt
from Lexico import Lexer
import webbrowser
import sys
import os

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
        self.boton_traducir.clicked.connect(self.traducir)

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
        Abre el explorador de archivos para seleccionar un archivo de cualquier tipo.
        """
        file_dialog = QFileDialog(self)
        file_path, _ = file_dialog.getOpenFileName(self, "Abrir Archivo", "", "Todos los archivos (*.*);;Archivos JSON (*.json)")
        if file_path:  
            with open(file_path, 'r') as file:
                file_data = file.read()
                self.entrada_texto.setPlainText(file_data)

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
    
    def traducir(self):
        texto_a_traducir = self.entrada_texto.toPlainText()

        # La logica de mi analizador lexico...
        
        lexer = Lexer()
        lexer.analizar(texto_a_traducir)

        ruta_reportes = os.path.join("C:\\", "Users", "Revydubz", "OneDrive", "Documentos", "Practicas", "I Semestre (2024)", "Proyecto1_LFP", "Reportes")

        # Generar HTML para tokens válidos
        
        with open(os.path.join(ruta_reportes, 'Validos.html'), 'w') as archivo_html:
            archivo_html.write('<!DOCTYPE html>\n')
            archivo_html.write('<html>\n')
            archivo_html.write('<head>\n')
            archivo_html.write('<title>Tokens Analizados</title>\n')
            archivo_html.write('<style>\n')
            archivo_html.write('body {\n')
            archivo_html.write('    font-family: Arial, sans-serif;\n')
            archivo_html.write('    background-color: #f2f2f2;\n')
            archivo_html.write('    margin: 0;\n')
            archivo_html.write('    padding: 20px;\n')
            archivo_html.write('}\n')
            archivo_html.write('h2 {\n')
            archivo_html.write('    color: #333;\n')
            archivo_html.write('}\n')
            archivo_html.write('table {\n')
            archivo_html.write('    width: 100%;\n')
            archivo_html.write('    border-collapse: collapse;\n')
            archivo_html.write('    border-radius: 8px;\n')
            archivo_html.write('    overflow: hidden;\n')
            archivo_html.write('    box-shadow: 0 0 20px rgba(0, 0, 0, 0.1);\n')
            archivo_html.write('    background-color: #fff;\n')
            archivo_html.write('}\n')
            archivo_html.write('th, td {\n')
            archivo_html.write('    padding: 12px 15px;\n')
            archivo_html.write('    text-align: left;\n')
            archivo_html.write('}\n')
            archivo_html.write('th {\n')
            archivo_html.write('    background-color: #007bff;\n')
            archivo_html.write('    color: #fff;\n')
            archivo_html.write('    font-weight: bold;\n')
            archivo_html.write('    border-bottom: 2px solid #ddd;\n')
            archivo_html.write('}\n')
            archivo_html.write('tr:nth-child(even) {\n')
            archivo_html.write('    background-color: #f2f2f2;\n')
            archivo_html.write('}\n')
            archivo_html.write('tr:hover {\n')
            archivo_html.write('    background-color: #ddd;\n')
            archivo_html.write('}\n')
            archivo_html.write('</style>\n')
            archivo_html.write('</head>\n')
            archivo_html.write('<body>\n')
            archivo_html.write('<h2>Tokens Analizados</h2>\n')
            archivo_html.write('<table>\n')
            archivo_html.write('<tr><th>Tipo</th><th>Valor</th><th>Fila</th><th>Columna</th></tr>\n')
            for token in lexer.tabla_tokens_validos:
                archivo_html.write(f'<tr><td>{token["tipo"]}</td><td>{token["valor"]}</td><td>{token["fila"]}</td><td>{token["columna"]}</td></tr>\n')
            archivo_html.write('</table>\n')
            archivo_html.write('</body>\n')
            archivo_html.write('</html>\n')

        # Generar HTML para tokens invalidos
        
        with open(os.path.join(ruta_reportes, 'Invalidos.html'), 'w') as archivo_html_erroneos:
            archivo_html_erroneos.write('<!DOCTYPE html>\n')
            archivo_html_erroneos.write('<html>\n')
            archivo_html_erroneos.write('<head>\n')
            archivo_html_erroneos.write('<title>Tokens Erróneos Analizados</title>\n')
            archivo_html_erroneos.write('<style>\n')
            archivo_html_erroneos.write('body {\n')
            archivo_html_erroneos.write('    font-family: Arial, sans-serif;\n')
            archivo_html_erroneos.write('    background-color: #f2f2f2;\n')
            archivo_html_erroneos.write('    margin: 0;\n')
            archivo_html_erroneos.write('    padding: 20px;\n')
            archivo_html_erroneos.write('}\n')
            archivo_html_erroneos.write('h2 {\n')
            archivo_html_erroneos.write('    color: #333;\n')
            archivo_html_erroneos.write('}\n')
            archivo_html_erroneos.write('table {\n')
            archivo_html_erroneos.write('    width: 100%;\n')
            archivo_html_erroneos.write('    border-collapse: collapse;\n')
            archivo_html_erroneos.write('    border-radius: 8px;\n')
            archivo_html_erroneos.write('    overflow: hidden;\n')
            archivo_html_erroneos.write('    box-shadow: 0 0 20px rgba(0, 0, 0, 0.1);\n')
            archivo_html_erroneos.write('    background-color: #fff;\n')
            archivo_html_erroneos.write('}\n')
            archivo_html_erroneos.write('th, td {\n')
            archivo_html_erroneos.write('    padding: 12px 15px;\n')
            archivo_html_erroneos.write('    text-align: left;\n')
            archivo_html_erroneos.write('}\n')
            archivo_html_erroneos.write('th {\n')
            archivo_html_erroneos.write('    background-color: #ff6347;\n')  # Cambio de color de fondo
            archivo_html_erroneos.write('    color: #fff;\n')
            archivo_html_erroneos.write('    font-weight: bold;\n')
            archivo_html_erroneos.write('    border-bottom: 2px solid #ddd;\n')
            archivo_html_erroneos.write('}\n')
            archivo_html_erroneos.write('tr:nth-child(even) {\n')
            archivo_html_erroneos.write('    background-color: #f2f2f2;\n')
            archivo_html_erroneos.write('}\n')
            archivo_html_erroneos.write('tr:hover {\n')
            archivo_html_erroneos.write('    background-color: #ddd;\n')
            archivo_html_erroneos.write('}\n')
            archivo_html_erroneos.write('</style>\n')
            archivo_html_erroneos.write('</head>\n')
            archivo_html_erroneos.write('<body>\n')
            archivo_html_erroneos.write('<h2>Tokens Erróneos Analizados</h2>\n')
            archivo_html_erroneos.write('<table>\n')
            archivo_html_erroneos.write('<tr><th>Carácter</th><th>Fila</th><th>Columna</th></tr>\n')
            for token in lexer.tabla_tokens_erroneos:
                archivo_html_erroneos.write(f'<tr><td>{token["caracter"]}</td><td>{token["fila"]}</td><td>{token["columna"]}</td></tr>\n')
            archivo_html_erroneos.write('</table>\n')
            archivo_html_erroneos.write('</body>\n')
            archivo_html_erroneos.write('</html>\n')

        # Abrir los archivos generados en el navegador
        
        webbrowser.open_new_tab(os.path.join(ruta_reportes, 'Validos.html'))
        webbrowser.open_new_tab(os.path.join(ruta_reportes, 'Invalidos.html'))

        # Mensaje satisfactorio
        
        QMessageBox.information(self, "Archivos Generados", "Se han generado los archivos HTML de tokens válidos y erróneos.", QMessageBox.StandardButton.Ok)
    

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
