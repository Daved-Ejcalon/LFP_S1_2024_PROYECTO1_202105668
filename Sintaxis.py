
class Parser:
    def __init__(self, lexer):
        self.lexer = lexer
        self.html_output = ""

    def parse(self):
        token = self.lexer.get_next_token()
        while token:
            if token['tipo'] == 'INICIO':
                self.html_output += "<html>\n"
            elif token['tipo'] == 'ETIQUETA' and token['valor'] == "Encabezado:":
                self.html_output += "\t<head>\n"
                # Procesar el bloque Encabezado
                token = self.lexer.get_next_token()  # Saltar el token de la etiqueta "Encabezado:"
                token = self.lexer.get_next_token()  # Obtener el primer token del bloque Encabezado
                while token['tipo'] != "LLAVE_DER":
                    if token['tipo'] == 'ETIQUETA' and token['valor'] == "TituloPagina:":
                        token = self.lexer.get_next_token()  # Saltar el token de la etiqueta "TituloPagina:"
                        token = self.lexer.get_next_token()  # Obtener el token del valor del atributo
                        self.html_output += "\t\t<title>{}</title>\n".format(token['valor'])
                    token = self.lexer.get_next_token()
                self.html_output += "\t</head>\n"
            elif token['tipo'] == 'ETIQUETA' and token['valor'] == "Cuerpo:":
                self.html_output += "\t<body>\n"
                # Procesar el bloque Cuerpo
                token = self.lexer.get_next_token()  # Saltar el token de la etiqueta "Cuerpo:"
                token = self.lexer.get_next_token()  # Obtener el primer token del bloque Cuerpo
                while token['tipo'] != "LLAVE_DER":
                    # Procesar cada elemento dentro del bloque Cuerpo
                    if token['tipo'] == 'ETIQUETA':
                        if token['valor'] == "Parrafo:":
                            self.parse_parrafo()
                        elif token['valor'] == "Titulo:":
                            self.parse_titulo()
                        elif token['valor'] == "Texto:":
                            self.parse_texto()
                        elif token['valor'] == "Codigo:":
                            self.parse_codigo()
                        elif token['valor'] == "Negrita:":
                            self.parse_negrita()
                        elif token['valor'] == "Subrayado:":
                            self.parse_subrayado()
                        elif token['valor'] == "Tachado:":
                            self.parse_tachado()
                        elif token['valor'] == "Cursiva:":
                            self.parse_cursiva()
                        elif token['valor'] == "Salto:":
                            self.parse_salto()
                        elif token['valor'] == "Tabla:":
                            self.parse_tabla()
                    token = self.lexer.get_next_token()
                self.html_output += "\t</body>\n"
            token = self.lexer.get_next_token()

    def parse_parrafo(self):
        # Implementación de la regla para procesar el elemento Parrafo
        self.html_output += "\t\t<p>"
        token = self.lexer.get_next_token()  # Saltar el token de la etiqueta "Parrafo:"
        token = self.lexer.get_next_token()  # Obtener el primer token del contenido del párrafo
        while token['tipo'] != "LLAVE_DER":
            if token['tipo'] == 'ETIQUETA' and token['valor'] == "texto:":
                token = self.lexer.get_next_token()  # Saltar el token de la etiqueta "texto:"
                self.html_output += "{}".format(token['valor'])
            # Agregar más reglas para otros atributos del elemento "Parrafo"
            token = self.lexer.get_next_token()
        self.html_output += "</p>\n"

    def parse_titulo(self):
        # Implementación de la regla para procesar el elemento Titulo
        self.html_output += "\t\t<h1>"
        token = self.lexer.get_next_token()  # Saltar el token de la etiqueta "Titulo:"
        token = self.lexer.get_next_token()  # Obtener el primer token del contenido del título
        while token['tipo'] != "LLAVE_DER":
            if token['tipo'] == 'ETIQUETA' and token['valor'] == "texto:":
                token = self.lexer.get_next_token()  # Saltar el token de la etiqueta "texto:"
                self.html_output += "{}".format(token['valor'])
            # Agregar más reglas para otros atributos del elemento "Titulo"
            token = self.lexer.get_next_token()
        self.html_output += "</h1>\n"

    def parse_texto(self):
        # Implementación de la regla para procesar el elemento Texto
        self.html_output += "\t\t<p style=\""
        token = self.lexer.get_next_token()  # Saltar el token de la etiqueta "Texto:"
        token = self.lexer.get_next_token()  # Obtener el primer token del contenido del texto
        while token['tipo'] != "LLAVE_DER":
            if token['tipo'] == 'ETIQUETA' and token['valor'] == "fuente=":
                token = self.lexer.get_next_token()  # Saltar el token de la etiqueta "fuente="
                token = self.lexer.get_next_token()  # Obtener el token del valor del atributo "fuente"
                self.html_output += "font-family:{};".format(token['valor'])
            elif token['tipo'] == 'ETIQUETA' and token['valor'] == "color=":
                token = self.lexer.get_next_token()  # Saltar el token de la etiqueta "color="
                token = self.lexer.get_next_token()  # Obtener el token del valor del atributo "color"
                if token['valor'] in ["rojo", "amarillo", "azul"]:
                    self.html_output += "color:{};".format(token['valor'])
                else:
                    self.html_output += "color:{};".format(token['valor'])
            elif token['tipo'] == 'ETIQUETA' and token['valor'] == "tamaño=":
                token = self.lexer.get_next_token()  # Saltar el token de la etiqueta "tamaño="
                token = self.lexer.get_next_token()
                self.html_output += "font-size:{};".format(token['valor'])
            token = self.lexer.get_next_token()
        self.html_output += "\">\n"

    def parse_codigo(self):
        # Implementación de la regla para procesar el elemento Codigo
        self.html_output += "\t\t<p style=\"font-family:monospace; text-align:center;\">"
        token = self.lexer.get_next_token()  # Saltar el token de la etiqueta "Codigo:"
        token = self.lexer.get_next_token()  # Obtener el primer token del contenido del código
        while token['tipo'] != "LLAVE_DER":
            if token['tipo'] == 'ETIQUETA' and token['valor'] == "texto:":
                token = self.lexer.get_next_token()  # Saltar el token de la etiqueta "texto:"
                self.html_output += "{}".format(token['valor'])
            # Agregar más reglas para otros atributos del elemento "Codigo"
            token = self.lexer.get_next_token()
        self.html_output += "</p>\n"

    def parse_negrita(self):
        # Implementación de la regla para procesar el elemento Negrita
        self.html_output += "<strong>"
        token = self.lexer.get_next_token()  # Saltar el token de la etiqueta "Negrita:"
        token = self.lexer.get_next_token()  # Obtener el primer token del contenido en negrita
        while token['tipo'] != "LLAVE_DER":
            if token['tipo'] == 'ETIQUETA' and token['valor'] == "texto:":
                token = self.lexer.get_next_token()  # Saltar el token de la etiqueta "texto:"
                self.html_output += "{}".format(token['valor'])
            # Agregar más reglas para otros atributos del elemento "Negrita"
            token = self.lexer.get_next_token()
        self.html_output += "</strong>\n"

    def parse_subrayado(self):
        # Implementación de la regla para procesar el elemento Subrayado
        self.html_output += "<u>"
        token = self.lexer.get_next_token()  # Saltar el token de la etiqueta "Subrayado:"
        token = self.lexer.get_next_token()  # Obtener el primer token del contenido subrayado
        while token['tipo'] != "LLAVE_DER":
            if token['tipo'] == 'ETIQUETA' and token['valor'] == "texto:":
                token = self.lexer.get_next_token()  # Saltar el token de la etiqueta "texto:"
                self.html_output += "{}".format(token['valor'])
            # Agregar más reglas para otros atributos del elemento "Subrayado"
            token = self.lexer.get_next_token()
        self.html_output += "</u>\n"

    def parse_tachado(self):
        # Implementación de la regla para procesar el elemento Tachado
        self.html_output += "<strike>"
        token = self.lexer.get_next_token()  # Saltar el token de la etiqueta "Tachado:"
        token = self.lexer.get_next_token()  # Obtener el primer token del contenido tachado
        while token['tipo'] != "LLAVE_DER":
            if token['tipo'] == 'ETIQUETA' and token['valor'] == "texto:":
                token = self.lexer.get_next_token()  # Saltar el token de la etiqueta "texto:"
                self.html_output += "{}".format(token['valor'])
            # Agregar más reglas para otros atributos del elemento "Tachado"
            token = self.lexer.get_next_token()
        self.html_output += "</strike>\n"

    def parse_cursiva(self):
        # Implementación de la regla para procesar el elemento Cursiva
        self.html_output +=  "\t\t<em>"
        token = self.lexer.get_next_token()  # Saltar el token de la etiqueta "Cursiva:"
        token = self.lexer.get_next_token()  # Obtener el primer token del contenido en cursiva
        while token['tipo'] != "LLAVE_DER":
            if token['tipo'] == 'ETIQUETA' and token['valor'] == "texto:":
                token = self.lexer.get_next_token()  # Saltar el token de la etiqueta "texto:"
                self.html_output += "{}".format(token['valor'])
            # Agregar más reglas para otros atributos del elemento "Cursiva"
            token = self.lexer.get_next_token()
        self.html_output += "</em>\n"

    def parse_salto(self):
        # Implementación de la regla para procesar el elemento Salto
        self.html_output += "\t\t<br>"
        token = self.lexer.get_next_token()  # Saltar el token de la etiqueta "Salto:"
        token = self.lexer.get_next_token()  # Obtener el primer token del contenido del salto
        while token['tipo'] != "LLAVE_DER":
            if token['tipo'] == 'ETIQUETA' and token['valor'] == "cantidad:":
                token = self.lexer.get_next_token()  # Saltar el token de la etiqueta "cantidad:"
                self.html_output += "\n" * int(token['valor'])
            # Agregar más reglas para otros atributos del elemento "Salto"
            token = self.lexer.get_next_token()
        self.html_output += "</br>\n"

    def parse_tabla(self):
        # Implementación de la regla para procesar el elemento Tabla
        self.html_output += "\t\t<table>\n"
        token = self.lexer.get_next_token()  # Saltar el token de la etiqueta "Tabla:"
        token = self.lexer.get_next_token()  # Obtener el primer token del contenido de la tabla
        while token['tipo'] != "LLAVE_DER":
            if token['tipo'] == 'ETIQUETA' and token['valor'] == "filas:":
                token = self.lexer.get_next_token()  # Saltar el token de la etiqueta "filas:"
                filas = int(token['valor'])
            elif token['tipo'] == 'ETIQUETA' and token['valor'] == "columnas:":
                token = self.lexer.get_next_token()  # Saltar el token de la etiqueta "columnas:"
                columnas = int(token['valor'])
            elif token['tipo'] == 'ETIQUETA' and token['valor'] == "elemento:":
                elemento = {"fila": "", "columna": "", "contenido": ""}
                token = self.lexer.get_next_token()  # Saltar el token de la etiqueta "elemento:"
                token = self.lexer.get_next_token()  # Obtener el primer token del contenido del elemento
                while token['tipo'] != "LLAVE_DER":
                    if token['tipo'] == 'ETIQUETA' and token['valor'] == "fila:":
                        token = self.lexer.get_next_token()  # Saltar el token de la etiqueta "fila:"
                        token = self.lexer.get_next_token()  # Obtener el token del valor de la fila
                        elemento["fila"] = int(token['valor'])
                    elif token['tipo'] == 'ETIQUETA' and token['valor'] == "columna:":
                        token = self.lexer.get_next_token()  # Saltar el token de la etiqueta "columna:"
                        token = self.lexer.get_next_token()  # Obtener el token del valor de la columna
                        elemento["columna"] = int(token['valor'])
                    elif token['tipo'] == 'ETIQUETA' and token['valor'] == "texto:":
                        token = self.lexer.get_next_token()  # Saltar el token de la etiqueta "texto:"
                        elemento["contenido"] = token['valor']
                    token = self.lexer.get_next_token()
                self.html_output += "\t\t\t<tr>"
                for i in range(1, filas + 1):
                    for j in range(1, columnas + 1):
                        if elemento["fila"] == i and elemento["columna"] == j:
                            self.html_output += "<td>{}</td>".format(elemento["contenido"])
                        else:
                            self.html_output += "<td></td>"
                self.html_output += "</tr>\n"
            token = self.lexer.get_next_token()
        self.html_output += "\t\t</table>\n"
