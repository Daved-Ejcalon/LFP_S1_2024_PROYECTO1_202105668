class Lexer:
    def __init__(self):
        self.letras = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z"]
        self.numeros = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "0"]
        self.tabla_tokens = []
        self.cadena = ''
        self.fila = 0
        self.columna = 0
        self.estado_actual = 0
        self.tabla_errores = []

    def analizar(self, cadena):
        self.cadena = cadena
        self.fila = 1
        self.columna = 1
        self.estado_actual = 0
        lexema = ''
        
        for caracter in cadena:
            if caracter == '\n':
                self.fila += 1
                self.columna = 0
            elif caracter.isspace():
                if lexema:
                    self.guardar_token('PALABRA', lexema)
                    lexema = ''
                self.columna += 1
                continue
            else:
                lexema += caracter
                self.columna += 1
                
                if caracter in self.letras:
                    self.estado_actual = 1
                elif caracter in self.numeros:
                    self.estado_actual = 2
                elif caracter == ':':
                    self.guardar_token('DOS_PUNTOS', ':')
                elif caracter == ',':
                    self.guardar_token('COMA', ',')
                elif caracter == '"':
                    self.estado_actual = 3
                elif caracter == '[':
                    self.guardar_token('CORCHETE_IZQ', '[')
                elif caracter == ']':
                    self.guardar_token('CORCHETE_DER', ']')
                elif caracter == '{':
                    self.guardar_token('LLAVE_IZQ', '{')
                elif caracter == '}':
                    self.guardar_token('LLAVE_DER', '}')
                elif caracter == ';':
                    self.guardar_token('PUNTO_COMA', ';')
                else:
                    self.recuperar_error(caracter)

        # Verificación de estado al final de la cadena
        if lexema:
            self.guardar_token('PALABRA', lexema)

    def guardar_token(self, tipo, valor):
        self.tabla_tokens.append({'tipo': tipo, 'valor': valor, 'fila': self.fila, 'columna': self.columna})
        self.estado_actual = 0

    def recuperar_error(self, caracter):
        self.tabla_errores.append({'caracter': caracter, 'fila': self.fila, 'columna': self.columna})
    
    def get_next_token(self):
        if self.tabla_tokens:
            return self.tabla_tokens.pop(0)
        else:
            return None
