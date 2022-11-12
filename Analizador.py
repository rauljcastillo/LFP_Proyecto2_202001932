from Token import Token
from errores import ErroresLexicos
from ErroresS import ErroresSin
from Transformar import Almacenar

class Analizador:
    palabras_reservadas={
        "Etiqueta": "tEtiqueta",
        "Boton": "tBtn",
        "Check": "tCheck",
        "RadioBoton": "tRadBtn",
        "Texto": "tTexto",
        "AreaTexto": "tAreaTxt",
        "Clave": "tClave",
        "Contenedor": "tConten",
        "Controles":"tControles",
        "setAncho": "tAncho",
        "setAlto":"tAlto",
        "setColorFondo": "tColFon",
        "setColorLetra": "tColLet",
        "setAlineacion": "tAlineac",
        "setMarcada": "tMarcada",
        "setTexto": "tsetTexto",
        "add": "tAdd",
        "propiedades": "tProp",
        "Colocacion": "tColoc",
        "setPosicion": "tsetPos",
        "this": "tkID",
        "add": "tAdd",
        "True": "tbool",
        "False": "tbool",
        "setGrupo":"tGrup"

    }

    simbolos={
        "+": "MAS",
        '"': "ComillasD",
        "'": "ComillaS",
        "<": "ANG_A",
        ">": "ANG_C",
        "-": "MENOS",
        ".": "PUNTO",
        ",": "COMA",
        "*": "MULTI",
        "!": "EXCLAM",
        ";": "PUNTCOM",
        "(": "PAREN_A",
        ")": "PAREN_C",
}
    variable1=["tEtiqueta","tBtn","tCheck","tRadBtn","tTexto","tAreaTxt","tClave","tConten","tThis"]
    variable2=["tAncho","tAlto","tColFon","tColLet","tAlineac","tMarcada","tsetTexto","tGrup"]
    numeros=["ENTERO","REAL"]
    coloc=["tAdd","tsetPos"]

    def __init__(self) -> None:
        self.Salida:list=[]
        self.estado:int=0
        self.auxLex:str=""
        self.fila=1
        self.col=1
        self.errores=[]
        self.cont=0
        self.erroresS=[]
        self.ob=Almacenar()
        self.contenedores=[]

#-----Empieza analizador léxico-----

    def Escanear(self,entrada:str):
        entrada=entrada+"#"
        self.auxLex=""
        contador=0
        c:str
        while contador<=len(entrada)-1:
            c=entrada[contador]        
            if self.estado==0:
                if c.isdigit():
                    self.estado=1
                    self.auxLex=c
                    self.col+=1
                elif c.isalpha():
                    self.estado=5
                    self.col+=1
                    self.auxLex+=c

                elif c in self.simbolos:
                    self.auxLex=c
                    self.col+=1
                    self.agregarToken(self.simbolos[c])
                
                elif c=="/":
                    if entrada[contador+1]=="/":
                        #self.auxLex="//"
                        contador+=2
                        self.col+=1
                        self.estado=4
                        continue
                    elif entrada[contador+1]=="*":
                        #self.auxLex="/*"
                        contador+=2
                        self.estado=6
                        continue
                    self.auxLex+=c
                    self.col+=1
                    self.agregarToken("SIGNO_DIV")
            
                elif c=="\n":
                    self.fila+=1
                    self.col=1
                    self.auxLex=""
                elif c==" ":
                    self.col+=1

                else:
                    self.col+=1
                    if c=="#" and contador==len(entrada)-1:
                        print("Hemos concluido el análisis")
                    else:
                        self.errores.append(ErroresLexicos("Lexico",c,self.fila,self.col))
                        self.estado=0
            elif self.estado==1:
                if c.isdigit():
                    self.estado=1
                    self.col+=1
                    self.auxLex+=c
                elif c==".":
                    self.estado=2
                    self.col+=1
                    self.auxLex+=c
                else:
                    self.agregarToken("NUM")
                    contador-=1
            elif self.estado==2:
                if c.isdigit():
                    self.estado=3
                    self.col+=1
                    self.auxLex+=c
                else:
                    self.col+=1
                    self.errores.append(ErroresLexicos("Lexico",c,self.fila,self.col))
                    self.estado=0
            elif self.estado==3:  #Este estado detecta los numeros despues del punto decimal
                if c.isdigit():
                    self.estado=3
                    self.col+=1
                    self.auxLex+=c
                else:
                    self.col+=1
                    self.agregarToken("NUM")
                    contador-=1
            
            elif self.estado==4:  #Este estado detecta los comentarios de //
                if c=="\n":
                    self.fila+=1
                    self.col=1
                    self.estado=0
                elif c.isascii():
                    self.col+=1

            elif self.estado==5:  #Este estado detecta las cadenas del alfabeto
                if c.isalpha():
                    self.auxLex+=c
                    self.col+=1
                else:
                    if c=='"':
                        self.agregarToken("tCadena")
                        contador-=1
                    elif self.auxLex in self.palabras_reservadas:
                        self.agregarToken(self.palabras_reservadas[self.auxLex])
                        contador-=1
                    elif c=="." or c==";" or c==")" or c=="("  or c=="\n":
                        self.agregarToken("tkID")
                        contador-=1
                    elif c.isdigit():
                        self.auxLex+=c
                        self.col+=1
                    elif c=="-" or c==" ":
                        self.agregarToken("palabra")
                        contador-=1
                    elif c=="'" or c=='"':
                        self.agregarToken("tCadena")
                        contador-=1
                    else:
                        self.col+=1
                        self.errores.append(ErroresLexicos("Lexico",c,self.fila,self.col))
                        self.estado=0
            elif self.estado==6:   #Detecta los comentarios multilinea
                if c=="\n":
                    self.fila+=1
                    self.col=1
                elif c=="*":
                    self.col+=1
                    if entrada[contador+1]=="/":
                        self.estado=0
                        contador+=1
                elif c.isascii():
                    self.col+=1
            

            contador+=1
        return self.Salida
    
    def agregarToken(self,tipo):
        self.Salida.append(Token(tipo,self.auxLex,self.fila,self.col))
        self.auxLex=""
        self.estado=0
    
    def imprimir(self,lista:list):
        for elem in lista:
            print(elem.getTipo(),"-->",elem.getVal())
    
    def listaErr(self):
        return self.errores

#------Inicia analizador sintáctico------

    def contiene3(self,tkn,lexema):
        if tkn in self.coloc:
            self.cont+=1
            return True
        self.erroresS.append(ErroresSin("Sintáctico",self.Salida[self.cont].getFil(),"Se esperaba: "+lexema))
        a=self.cont+1
        for elem in self.Salida[a:]:
            traer=elem.getTipo()
            self.cont+=1
            if traer=="PUNTCOM":
                self.cont+=1
                return False
            elif len(self.Salida)==a or traer=="ANG_A" or traer=="MENOS" or traer=="tColoc":
               return False
            

    def params(self):
        tipe=self.Salida[self.cont-2].getTipo()
        if tipe=="tAncho" or tipe=="tAlto":
            if self.Parseo("NUM","un numero"):
                x=self.Salida[self.cont-5].getVal()
                y=tipe.lstrip("t").lower()
                z=self.Salida[self.cont-1].getVal()
                self.ob.almacenarPropiedades(x,y,z)
                return
            elif self.Salida[self.cont]=="PAREN_C":
                return
            else:
                self.cont+=1

        elif tipe=="tsetTexto":
            a=self.Parseo("ComillasD",'"')
            b=self.Parseo("tCadena","una cadena")
            c=self.Parseo("ComillasD",'"')
            if a and b and c:
                x=self.Salida[self.cont-7].getVal()
                z=self.Salida[self.cont-2].getVal()
                self.ob.almacenarPropiedades(x,"cadena",z)
                return   
            elif b==None and a and c:
                x=self.Salida[self.cont-6].getVal()
                self.ob.almacenarPropiedades(x,"cadena",'')
                return
            self.cont+=1

        elif tipe=="tColFon" or tipe=="tColLet":
            self.Parseo("NUM","un numero")
            self.Parseo("COMA",",")
            self.Parseo("NUM","un numero")
            self.Parseo("COMA",",")
            self.Parseo("NUM","un numero")
            x=self.Salida[self.cont-9].getVal()
            z=[self.Salida[self.cont-5].getVal(),self.Salida[self.cont-3].getVal(),self.Salida[self.cont-1].getVal()]
            if tipe=="tColFon":
                if x=="this":
                    self.ob.almacenarPropiedades(x,"fondo",z)
                    return
                self.ob.almacenarPropiedades(x,"fondo",z)
            elif tipe=="tColLet":
                self.ob.almacenarPropiedades(x,"color",z)
        elif tipe=="tMarcada":
            if self.Parseo("tbool","un booleano"):
                x=self.Salida[self.cont-5].getVal()
                y=self.Salida[self.cont-1].getVal()
                if y=="True":
                    self.ob.almacenarPropiedades(x,"marcada","checked")
                    return
                else:
                    self.ob.almacenarPropiedades(x,"marcada","")
                    return
            self.cont+=1
        elif tipe=="tsetPos":
            self.Parseo("NUM","un numero")
            self.Parseo("COMA",",")
            self.Parseo("NUM","un numero")
            x=self.Salida[self.cont-7].getVal()
            z=[self.Salida[self.cont-3].getVal(),self.Salida[self.cont-1].getVal()]
            self.ob.almacenarPropiedades(x,"posicion",z)

        elif tipe=="tAdd":
            if self.Parseo("tkID","un identificador") and self.Salida[self.cont-1].getVal() in self.contenedores:
                x=self.Salida[self.cont-5].getVal()
                z=self.Salida[self.cont-1].getVal()
                if x=="this":
                    self.ob.almacenarPropiedades(z,x,z)
                    return
                self.ob.almacenarPropiedades(x,"add",z)
                return
            elif self.Salida[self.cont-1].getTipo()=="PAREN_C":
                return
            self.erroresS.append(ErroresSin("Sintáctico",self.Salida[self.cont].getFil(),"Id no definido"))
            #print("Error jajaj no se encuentra ese id mano")  
        elif tipe=="tAlineac":
            a=self.Salida[self.cont].getVal()
            x=self.Salida[self.cont-4].getVal()
            if a=="Centro":
                self.ob.almacenarPropiedades(x,"alineacion","center")
                self.cont+=1
            elif a=="Izquierda":
                self.ob.almacenarPropiedades(x,"alineacion","left")
                self.cont+=1
            elif a=="Derecha":
                self.ob.almacenarPropiedades(x,"alineacion","right")
                self.cont+=1
            else:
                self.erroresS.append(ErroresSin("Sintáctico",self.Salida[self.cont].getFil(),"Se esperaba: alineacion"))
                self.cont+=1
        elif tipe=="tGrup":
            if self.Parseo("tkID","identificador"):
                x=self.Salida[self.cont-5].getVal()
                y=self.Salida[self.cont-1].getVal()
                self.ob.almacenarPropiedades(x,"grupo",y)

                

    def contiene1(self,tkn,lexema):
        if tkn in self.variable2:
            self.cont+=1
            return True
        self.erroresS.append(ErroresSin("Sintáctico",self.Salida[self.cont].getFil(),"Se esperaba: "+lexema))
        a=self.cont+1
        for elem in self.Salida[a:]:
            traer=elem.getTipo()
            self.cont+=1
            if len(self.Salida)==a or traer=="tkID" or traer=="ANG_A" or traer=="MENOS" or traer=="tProp":
                return False
        
    def contiene(self,tkn,lexema):
        if tkn in self.variable1:
            self.cont+=1
            return True
        self.erroresS.append(ErroresSin("Sintáctico",self.Salida[self.cont].getFil(),"Se esperaba: "+lexema))     
        a=self.cont+1
        for elem in self.Salida[a:]:
            traer=elem.getTipo()
            self.cont+=1
            if len(self.Salida)==a or traer=="ANG_A" or traer=="MENOS" or traer=="tControles":
                return False

    def gramatica_contenido(self):
        x=self.Salida[self.cont].getTipo()
        if x=="tControles" or x=="tkID" or x=="MENOS" or x=="ANG_A":
            return None
        else:
            if self.contiene(self.Salida[self.cont].getTipo(),"un elemento") is False:
                return self.gramatica_contenido()
            self.Parseo("tkID","un identificador")
            if self.Parseo("PUNTCOM",";"):
                a=self.Salida[self.cont-3].getVal()
                b=self.Salida[self.cont-2].getVal()
            else:  
                a=self.Salida[self.cont-2].getVal()
                b=self.Salida[self.cont-1].getVal()
            if b in self.contenedores:
                self.erroresS.append(ErroresSin("Sintáctico",self.Salida[self.cont-1].getFil(),"id repetido"))
            else:
                self.contenedores.append(b)
                self.ob.llenarA({"tipo": a,"id": b}) 
            return self.gramatica_contenido()
    
    def gramaticaprop(self):
        x=self.Salida[self.cont].getTipo()
        if x=="tProp" or x=="MENOS" or x=="ANG_A" or x=="palabra":
            return None
        else:
            
            self.Parseo("tkID","un identificador")
            a=self.Salida[self.cont-1].getVal()
            if a not in self.contenedores:
                self.erroresS.append(ErroresSin("Sintáctico",self.Salida[self.cont-1].getFil(),f"id {a} no definido"))
            self.Parseo("PUNTO",".")
            if self.contiene1(self.Salida[self.cont].getTipo(),"una propiedad") is False:
                return self.gramaticaprop()
            self.Parseo("PAREN_A","(")
            self.params()
            self.Parseo("PAREN_C",")")
            self.Parseo("PUNTCOM",";")
            return self.gramaticaprop()
    
    def gramaticaColoc(self):
        x=self.Salida[self.cont].getTipo()
        if len(self.Salida)==self.cont or x=="palabra" or x=="tColoc" or x=="MENOS" or x=="ANG_C":
            return None
        else:
            self.Parseo("tkID","un identificador")
            a=self.Salida[self.cont-1].getVal()
            if a not in self.contenedores:
                self.erroresS.append(ErroresSin("Sintáctico",self.Salida[self.cont-1].getFil(),f"id {a} no definido"))
            self.Parseo("PUNTO",".")
            if self.contiene3(self.Salida[self.cont].getTipo(),"una propiedad") is False:
                return self.gramaticaColoc()
            self.Parseo("PAREN_A","(")
            self.params()
            self.Parseo("PAREN_C",')')
            self.Parseo("PUNTCOM",";")
            return self.gramaticaColoc()

    def Parseo(self,Tk,Lexema):
        if self.cont<len(self.Salida):
            if self.Salida[self.cont].getTipo()==Tk:
                self.cont+=1
                return True
            elif Tk=="tCadena":
                return
                
            else:
                x=self.Salida[self.cont].getTipo()
                if Tk=="tProp" and (x=="palabra" or x=="tkID"):
                    self.erroresS.append(ErroresSin("Sintáctico",self.Salida[self.cont-1].getFil(),"Se esparaba: "+Lexema))
                    
                    self.cont+=1
                    return False
                elif Tk=="tControles" and (x=="palabra" or x=="tkID"):
                    self.erroresS.append(ErroresSin("Sintáctico",self.Salida[self.cont-1].getFil(),"Se esparaba: "+Lexema))
                    
                    self.cont+=1
                    return False
                elif Tk=="tColoc" and (x=="palabra" or x=="tkID"):
                    self.erroresS.append(ErroresSin("Sintáctico",self.Salida[self.cont-1].getFil(),"Se esparaba: "+Lexema))
                    
                    self.cont+=1
                    return False
                
                self.erroresS.append(ErroresSin("Sintáctico",self.Salida[self.cont-1].getFil(),"Se esparaba: "+Lexema))
                return False


    def analisisSintactico(self):
        self.contenedores.append("this")
    #Controles
        self.Parseo("ANG_A","<")
        self.Parseo("EXCLAM","!")
        self.Parseo("MENOS","-")
        self.Parseo("MENOS","-")
        self.Parseo("tControles","Controles")
        self.gramatica_contenido()
        self.Parseo("tControles","Controles")
        self.Parseo("MENOS","-")
        self.Parseo("MENOS","-")
        self.Parseo("ANG_C",">")

    #Propiedades
        
        self.Parseo("ANG_A","<")
        self.Parseo("EXCLAM","!")
        self.Parseo("MENOS","-")
        self.Parseo("MENOS","-")
        self.Parseo("tProp","propiedades")
        self.gramaticaprop()
        self.Parseo("tProp","propiedades")
        self.Parseo("MENOS","-")
        self.Parseo("MENOS","-")
        self.Parseo("ANG_C",">")

    #Colocacion 
        self.Parseo("ANG_A","<")
        self.Parseo("EXCLAM","!")
        self.Parseo("MENOS","-")
        self.Parseo("MENOS","-")
        self.Parseo("tColoc","etiqueta Colocacion")
        self.gramaticaColoc()
        self.Parseo("tColoc","etiqueta Colocacion")
        self.Parseo("MENOS","-")
        self.Parseo("MENOS","-")
        self.Parseo("ANG_C",">")
        return (self.erroresS,self.ob)
        

    def limpiar(self):
        self.errores.clear()
        self.Salida.clear()
        self.contenedores.clear()
        self.erroresS.clear()
        self.ob.limpiar()
        self.cont=0
        self.fila=1
        self.col=1