import webbrowser
import os

class Lexer:
    def __init__(self):
        self.tabla_tokens_validos = []
        self.tabla_tokens_erroneos = []
        self.cadena = ''
        self.fila = 0
        self.columna = 0

    def analizar(self, cadena):
        self.cadena = cadena
        self.fila = 1
        self.columna = 0
        estado_actual = 0
        lexema = ''

        for caracter in cadena:
            if caracter == '\n':
                self.fila += 1
                self.columna = 0
                continue
            self.columna += 1

            if estado_actual == 0:
                if caracter.isspace():
                    continue
                elif caracter.isalpha() or caracter == '_':
                    estado_actual = 1
                    lexema += caracter
                elif caracter == '{':
                    self.guardar_token_valido('LLAVE_IZQ', caracter)
                elif caracter == '}':
                    self.guardar_token_valido('LLAVE_DER', caracter)
                elif caracter == ':':
                    self.guardar_token_valido('DOS_PUNTOS', caracter)
                elif caracter == ';':
                    self.guardar_token_valido('PUNTO_COMA', caracter)
                elif caracter == ',':
                    self.guardar_token_valido('COMA', caracter)
                elif caracter == '[':
                    self.guardar_token_valido('CORCHETE_IZQ', caracter)
                elif caracter == ']':
                    self.guardar_token_valido('CORCHETE_DER', caracter)
                elif caracter == '=':
                    self.guardar_token_valido('IGUAL', caracter)
                elif caracter == '"':
                    estado_actual = 3
                elif caracter.isdigit():  
                    estado_actual = 2       
                    lexema += caracter      
                elif caracter == '(':
                    estado_actual = 4
                else:
                    self.recuperar_error(caracter)

            elif estado_actual == 1:
                if caracter.isalnum() or caracter == '_':
                    lexema += caracter
                else:
                    self.guardar_token_valido('IDENTIFICADOR', lexema)
                    estado_actual = 0
                    lexema = ''
                    continue
            elif estado_actual == 2:
                if caracter.isdigit():
                    lexema += caracter
                else:
                    self.guardar_token_valido('NUMERO', lexema)
                    estado_actual = 0
                    lexema = ''
                    continue
            elif estado_actual == 3:
                if caracter == '"':
                    
                    if lexema.replace(' ', '') == '':
                        self.recuperar_error('Cadena vacía')
                        estado_actual = 0
                        lexema = ''
                        continue
                    
                    if lexema.isdigit():
                        self.guardar_token_valido('NUMERO', lexema)
                        estado_actual = 0
                        lexema = ''
                    else:
                        self.guardar_token_valido('CADENA', lexema)
                        estado_actual = 0
                        lexema = ''
                    continue
                
                else:
                    lexema += caracter
            elif estado_actual == 4:
                if caracter.isalpha() or caracter == '_':
                    lexema += caracter
                elif caracter == ')':
                    if lexema[0].isupper() and len(lexema) == 1:
                        self.guardar_token_valido('IDENTIFICADOR', lexema)
                    else:
                        self.recuperar_error(lexema)
                    estado_actual = 0
                    lexema = ''
                else:
                    self.recuperar_error(caracter)

        if lexema:
            if estado_actual == 1:
                self.guardar_token_valido('IDENTIFICADOR', lexema)
            elif estado_actual == 2:
                self.guardar_token_valido('NUMERO', lexema)
            elif estado_actual == 3:
                self.recuperar_error('Fin de cadena dentro de una cadena')
            elif estado_actual == 4:
                self.recuperar_error('Fin de identificador entre paréntesis sin cerrar')

    def guardar_token_valido(self, tipo, valor):
        self.tabla_tokens_validos.append({'tipo': tipo, 'valor': valor, 'fila': self.fila, 'columna': self.columna})

    def guardar_token_erroneo(self, caracter):
        self.tabla_tokens_erroneos.append({'caracter': caracter, 'fila': self.fila, 'columna': self.columna})

    def recuperar_error(self, caracter):
        #mensaje_error = f"Error: Carácter no válido '{caracter}' en la fila {self.fila}, columna {self.columna}."
        self.guardar_token_erroneo(caracter)
        #print(mensaje_error)

    def generar_html_tokens(self, nombre_archivo):
        ruta_reportes = os.path.join("C:\\", "Users", "Revydubz", "OneDrive", "Documentos", "Practicas", "I Semestre (2024)", "Proyecto1_LFP", "Reportes")
        
        with open(nombre_archivo, 'r', encoding='utf-8') as archivo:
            contenido = archivo.read()
            self.analizar(contenido)

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
            for token in self.tabla_tokens_validos:
                archivo_html.write(f'<tr><td>{token["tipo"]}</td><td>{token["valor"]}</td><td>{token["fila"]}</td><td>{token["columna"]}</td></tr>\n')
            archivo_html.write('</table>\n')
            archivo_html.write('</body>\n')
            archivo_html.write('</html>\n')

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
            for token in self.tabla_tokens_erroneos:
                archivo_html_erroneos.write(f'<tr><td>{token["caracter"]}</td><td>{token["fila"]}</td><td>{token["columna"]}</td></tr>\n')
            archivo_html_erroneos.write('</table>\n')
            archivo_html_erroneos.write('</body>\n')
            archivo_html_erroneos.write('</html>\n')
        
        webbrowser.open_new_tab(os.path.join(ruta_reportes, 'Validos.html'))
        webbrowser.open_new_tab(os.path.join(ruta_reportes, 'Invalidos.html'))
        
if __name__ == "__main__":
    nombre_archivo = input("Ingrese el nombre del archivo de entrada: ")
    lexer = Lexer()
    lexer.generar_html_tokens(nombre_archivo)
    print("Archivos HTML generados con los tokens válidos y erróneos analizados.")
