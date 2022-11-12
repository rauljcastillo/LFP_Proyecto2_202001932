class ErroresSin:
    def __init__(self,tipo,linea,descrip) -> None:
        self.tipo=tipo
        self.linea=linea
        self.descripcion=descrip

    def getTipo(self):
        return self.tipo
    def getLinea(self):
        return self.linea
    def getDescrip(self):
        return self.descripcion