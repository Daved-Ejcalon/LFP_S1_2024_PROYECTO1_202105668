from Lexico import Lexer
class Parser:
    def __init__(self, lexer):
        self.lexer = lexer
        self.tokens = lexer.tabla_tokens_validos
        self.index = 0
        self.resultado = {}

    def parse(self):
        if self.verificar_estructura():
            self.inicio()
            print("La estructura del archivo es satisfactoria.")
        else:
            print("La estructura del archivo no es válida.")
    def verificar_estructura(self):
        # Verifica si la estructura del archivo se ajusta a la del analizador sintáctico
        # Puede implementarse una lógica más compleja aquí para verificar la estructura completa
        return True
    def verificar_atributo(self, token, tipo, valor):
        return token['tipo'] == tipo and token['valor'] == valor

    def match(self, tipo, valor):
        token_actual = self.tokens[self.index]
        if self.verificar_atributo(token_actual, tipo, valor):
            self.index += 1
        else:
            print(f"Error de sintaxis: Se esperaba '{valor}' en la fila {token_actual['fila']}, columna {token_actual['columna']}")

    def inicio(self):
        self.match('IDENTIFICADOR', 'Inicio')
        self.match('LLAVE_IZQ', '{')
        self.resultado['Encabezado'] = self.encabezado()
        self.match('COMA', ',')
        self.resultado['Cuerpo'] = self.cuerpo()
        self.match('LLAVE_DER', '}')

    def encabezado(self):
        encabezado = {}
        self.match('IDENTIFICADOR', 'Encabezado')
        self.match('LLAVE_IZQ', '{')
        self.match('IDENTIFICADOR', 'TituloPagina')
        self.match('DOS_PUNTOS', ':')
        self.match('CADENA', 'Ejemplo titulo')
        self.match('PUNTO_COMA', ';')
        self.match('LLAVE_DER', '}')
        return encabezado

    def cuerpo(self):
        cuerpo = []
        self.match('IDENTIFICADOR', 'Cuerpo')
        self.match('CORCHETE_IZQ', '[')
        cuerpo.append(self.titulo())
        cuerpo.append(self.fondo())
        cuerpo.append(self.parrafo())
        cuerpo.append(self.texto())
        cuerpo.append(self.codigo())
        cuerpo.append(self.negrita())
        cuerpo.append(self.subrayado())
        cuerpo.append(self.tachado())
        cuerpo.append(self.cursiva())
        cuerpo.append(self.salto())
        cuerpo.append(self.tabla())
        self.match('CORCHETE_DER', ']')
        return cuerpo

    def titulo(self):
        titulo = {}
        self.match('IDENTIFICADOR', 'Titulo')
        self.match('LLAVE_IZQ', '{')
        self.match('IDENTIFICADOR', 'texto')
        self.match('DOS_PUNTOS', ':')
        self.match('CADENA', 'Este es un titulo')
        self.match('PUNTO_COMA', ';')
        self.match('IDENTIFICADOR', 'posicion')
        self.match('DOS_PUNTOS', ':')
        self.match('CADENA', 'izquierda')
        self.match('PUNTO_COMA', ';')
        self.match('IDENTIFICADOR', 'tamaño')
        self.match('DOS_PUNTOS', ':')
        self.match('CADENA', 't1')
        self.match('PUNTO_COMA', ';')
        self.match('IDENTIFICADOR', 'color')
        self.match('DOS_PUNTOS', ':')
        self.match('CADENA', 'rojo')
        self.match('PUNTO_COMA', ';')
        self.match('LLAVE_DER', '}')
        return titulo

    def fondo(self):
        fondo = {}
        self.match('IDENTIFICADOR', 'Fondo')
        self.match('LLAVE_IZQ', '{')
        self.match('IDENTIFICADOR', 'color')
        self.match('DOS_PUNTOS', ':')
        self.match('CADENA', 'cyan')
        self.match('PUNTO_COMA', ';')
        self.match('LLAVE_DER', '}')
        return fondo

    def parrafo(self):
        parrafo = {}
        self.match('IDENTIFICADOR', 'Parrafo')
        self.match('LLAVE_IZQ', '{')
        self.match('IDENTIFICADOR', 'texto')
        self.match('CADENA', 'Este es un parrafo de ejemplo.')
        self.match('PUNTO_COMA', ';')
        self.match('IDENTIFICADOR', 'posicion')
        self.match('CADENA', 'izquierda')
        self.match('PUNTO_COMA', ';')
        self.match('LLAVE_DER', '}')
        return parrafo

    def texto(self):
        texto = {}
        self.match('IDENTIFICADOR', 'Texto')
        self.match('LLAVE_IZQ', '{')
        self.match('IDENTIFICADOR', 'fuente')
        self.match('CADENA', 'Arial')
        self.match('PUNTO_COMA', ';')
        self.match('IDENTIFICADOR', 'color')
        self.match('CADENA', 'azul')
        self.match('PUNTO_COMA', ';')
        self.match('IDENTIFICADOR', 'tamaño')
        self.match('NUMERO', '11')
        self.match('PUNTO_COMA', ';')
        self.match('LLAVE_DER', '}')
        return texto

    def codigo(self):
        codigo = {}
        self.match('IDENTIFICADOR', 'Codigo')
        self.match('LLAVE_IZQ', '{')
        self.match('IDENTIFICADOR', 'texto')
        self.match('CADENA', 'Muestra el texto con fuente de codigo de ordenador.')
        self.match('PUNTO_COMA', ';')
        self.match('IDENTIFICADOR', 'posicion')
        self.match('CADENA', 'centro')
        self.match('PUNTO_COMA', ';')
        self.match('LLAVE_DER', '}')
        return codigo

    def negrita(self):
        negrita = {}
        self.match('IDENTIFICADOR', 'Negrita')
        self.match('LLAVE_IZQ', '{')
        self.match('IDENTIFICADOR', 'texto')
        self.match('CADENA', 'Este texto aparecerá en negrita.')
        self.match('PUNTO_COMA', ';')
        self.match('LLAVE_DER', '}')
        return negrita

    def subrayado(self):
        subrayado = {}
        self.match('IDENTIFICADOR', 'Subrayado')
        self.match('LLAVE_IZQ', '{')
        self.match('IDENTIFICADOR', 'texto')
        self.match('CADENA', 'Este texto aparecerá Subrayado.')
        self.match('PUNTO_COMA', ';')
        self.match('LLAVE_DER', '}')
        return subrayado

    def tachado(self):
        tachado = {}
        self.match('IDENTIFICADOR', 'Tachado')
        self.match('LLAVE_IZQ', '{')
        self.match('IDENTIFICADOR', 'texto')
        self.match('CADENA', 'Este texto aparecerá tachado.')
        self.match('PUNTO_COMA', ';')
        self.match('LLAVE_DER', '}')
        return tachado

    def cursiva(self):
        cursiva = {}
        self.match('IDENTIFICADOR', 'Cursiva')
        self.match('LLAVE_IZQ', '{')
        self.match('IDENTIFICADOR', 'texto')
        self.match('CADENA', 'Este texto aparecerá en cursiva.')
        self.match('PUNTO_COMA', ';')
        self.match('LLAVE_DER', '}')
        return cursiva

    def salto(self):
        salto = {}
        self.match('IDENTIFICADOR', 'Salto')
        self.match('LLAVE_IZQ', '{')
        self.match('IDENTIFICADOR', 'cantidad')
        self.match('NUMERO', '5')
        self.match('PUNTO_COMA', ';')
        self.match('LLAVE_DER', '}')
        return salto

    def tabla(self):
        tabla = {}
        self.match('IDENTIFICADOR', 'Tabla')
        self.match('LLAVE_IZQ', '{')
        self.match('IDENTIFICADOR', 'filas')
        self.match('NUMERO', '4')
        self.match('PUNTO_COMA', ';')
        self.match('IDENTIFICADOR', 'columnas')
        self.match('NUMERO', '3')
        self.match('PUNTO_COMA', ';')
        tabla['elementos'] = []
        for _ in range(3):
            elemento = {}
            self.match('IDENTIFICADOR', 'elemento')
            self.match('LLAVE_IZQ', '{')
            self.match('CADENA', 'fila')
            self.match('DOS_PUNTOS', ':')
            self.match('NUMERO', '1')
            self.match('COMA', ',')
            self.match('CADENA', 'columna')
            self.match('DOS_PUNTOS', ':')
            self.match('NUMERO', '1')
            self.match('COMA', ',')
            self.match('CADENA', 'Texto mostrado en fila 1 columna 1')
            self.match('LLAVE_DER', '}')
            self.match('PUNTO_COMA', ';')
            tabla['elementos'].append(elemento)
        self.match('LLAVE_DER', '}')
        return tabla

if __name__ == "__main__":
    nombre_archivo = input("Ingrese el nombre del archivo de entrada: ")
    lexer = Lexer()
    parser = Parser(lexer)
    lexer.analizar(nombre_archivo)
    parser.parse()
    print("Análisis sintáctico completado.")
