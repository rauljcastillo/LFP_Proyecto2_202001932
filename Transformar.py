import webbrowser
import os
class Almacenar:
    def __init__(self) -> None:
        self.arreglo=[]
        self.cont=1
        self.Concat=""
        self.elementos=[]

    def llenarA(self,dic):
        self.arreglo.append(dic)
    #id #nombrepropiedad #valor de esa prop
    def almacenarPropiedades(self,id,nombP,valor):
        for elem in self.arreglo:
            if elem["id"]==id:
                if nombP=="add" and "add" in elem:
                    elem[f"{nombP}{self.cont}"]=valor
                    self.cont+=1
                    break
                elem[f"{nombP}"]=valor
                break

    def imprimir(self):
        print(self.arreglo)
    
    def empezar(self):
        self.html="""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8" />
            <meta http-equiv="X-UA-Compatible" content="IE=edge" />
            <meta name="viewport" content="width=device-width, initial-scale=1.0" />
            <title>Document</title>
            <link rel="stylesheet" href="./primero.css" />
        </head>
        <body>
        </body>
        </html>
        """
        self.css=""
        for elem in self.arreglo:
            if elem["tipo"]=="Contenedor":
                cont=f'\n<div id="{elem["id"]}">\n</div>'
                self.elementos.append(cont)
                self.css+=f'#{elem["id"]}'
                self.css+='{'+"\n"
                self.css+=f'width: {elem["ancho"]}px;\n'
                self.css+=f'height: {elem["alto"]}px;\n'
                self.css+=f'position: absolute;\n'
                if "posicion" in elem:
                    self.css+=f'left: {elem["posicion"][0]}px; top: {elem["posicion"][1]}px;\n'
                else:
                    self.css+=f'left: 15px; top: 50px;\n'
                if "fondo" in elem:
                    self.css+=f'background-color: rgb({elem["fondo"][0]},{elem["fondo"][1]},{elem["fondo"][2]});\n'
                self.css+='}\n\n'
            elif elem["tipo"]=="Texto":
                if "alineacion" in elem:
                    cont=f'\n<input type="text" id="{elem["id"]}" style="text-align: {elem["alineacion"]}" value="{elem["cadena"]}">'
                else:
                    cont=f'\n<input type="text" id="{elem["id"]}" style="text-align: left" value="{elem["cadena"]}">'
                self.css+=f'#{elem["id"]}'
                self.css+='{\n'
                self.css+='position: absolute;\n'
                if "posicion" in elem:
                    self.css+=f'left: {elem["posicion"][0]}px;\n'
                    self.css+=f'top: {elem["posicion"][1]}px;\n'
                else:
                    self.css+=f'left: 10px;\n'
                    self.css+=f'top: 10px;\n' 
                self.css+='width: 100px;\n'
                self.css+='height: 25px;\n'
                self.css+='}\n\n'
                self.elementos.append(cont)
            elif elem["tipo"]=="AreaTexto":
                if "cadena" in elem:
                    cont=f'<Textarea id="{elem["id"]}">{elem["cadena"]}\n</Textarea>'
                else:
                    cont=f'<Textarea id="{elem["id"]}">\n</Textarea>'
                
                self.css+=f'#{elem["id"]}'
                self.css+='{\n'
                if "posicion" in elem:
                    self.css+=f'position: absolute;\n'
                    self.css+=f'left: {elem["posicion"][0]}px;\n'
                    self.css+=f'top: {elem["posicion"][1]}px;\n'
                self.css+='width: 150px;\n'
                self.css+='height: 150px;\n'
                self.css+='}\n\n'
                self.elementos.append(cont)
            elif elem["tipo"]=="Boton":
                cont=f'<input type="submit" id="{elem["id"]}" value="{elem["cadena"]}">'
                self.css+=f'#{elem["id"]}'
                self.css+='{\n'
                self.css+='border-radius: 10px;\n'
                self.css+='border-width: 0.2px;\n'
                self.css+='width: 100px;\n'
                self.css+='height: 25px;\n'
                self.css+='position: absolute;\n'
                if "alineacion" in elem:
                    self.css+=f'text-align: {elem["alineacion"]};\n'
                else:
                    self.css+=f'text-align: left;\n'
                self.css+=f'left: {elem["posicion"][0]}px;\n'
                self.css+=f'top: {elem["posicion"][1]}px;\n'
                self.css+='}\n\n'
                self.elementos.append(cont)
            elif elem["tipo"]=="Etiqueta":
                cont=f'<label id="{elem["id"]}">{elem["cadena"]}\n</label>'
                self.css+=f'#{elem["id"]}'
                self.css+='{\n'
                if "color" in elem:
                    self.css+=f'color: rgb({elem["color"][0]},{elem["color"][1]},{elem["color"][2]});\n'
                if "fondo" in elem:
                    self.css+=f'background-color: rgb({elem["fondo"][0]},{elem["fondo"][1]},{elem["fondo"][2]});'
                self.css+=f'position: absolute;\n'
                self.css+=f'left: {elem["posicion"][0]}px;\n'
                self.css+=f'top: {elem["posicion"][1]}px;\n'
                self.css+='width: 100px;\n'
                self.css+='height: 25px;\n'
                self.css+='}\n\n'
                self.elementos.append(cont)
            elif elem["tipo"]=="Clave":
                if "cadena" in elem:
                    cont=f'<input type="password" id="{elem["id"]}" value="{elem["cadena"]}">\n'
                else:
                    cont=f'<input type="password" id="{elem["id"]}">\n'
                self.css+=f'#{elem["id"]}'
                self.css+='{\n'
                self.css+='width: 100px;\n'
                self.css+='height: 25px;\n'
                self.css+='position: absolute;\n'
                if "alineacion" in elem:
                    self.css+=f'text-align: {elem["alineacion"]};\n'
                else:
                    self.css+=f'text-align: left;\n'
                self.css+=f'left: {elem["posicion"][0]}px;\n'
                self.css+=f'top: {elem["posicion"][1]}px;\n'
                self.css+='}\n\n'
                self.elementos.append(cont)
            elif elem["tipo"]=="Check":
                if "grupo" in elem:
                    cont=f'\n<label id="{elem["id"]}"><input type="checkbox" {elem["marcada"]} name="{elem["grupo"]}"/>{elem["cadena"]}</label>'
                else:
                    cont=f'\n<label id="{elem["id"]}"><input type="checkbox" {elem["marcada"]}/>{elem["cadena"]}</label>'
                self.css+=f'#{elem["id"]}'
                self.css+='{\n'
                self.css+='position: absolute;\n'
                self.css+=f'left: {elem["posicion"][0]}px;\n'
                self.css+=f'top: {elem["posicion"][1]}px;\n'
                self.css+='}\n\n'
                self.elementos.append(cont)
            elif elem["tipo"]=="RadioBoton":
                if "marcada" in elem:
                    cont=f'\n<label id="{elem["id"]}"><input type="radio" name="{elem["grupo"]}" {elem["marcada"]}/>{elem["cadena"]}</label>'
                else:
                    cont=f'\n<label id="{elem["id"]}"><input type="radio" name="{elem["grupo"]}"/>{elem["cadena"]}</label>'
                self.css+=f'#{elem["id"]}'
                self.css+='{\n'
                self.css+='position: absolute;\n'
                if "posicion" in elem:
                    self.css+=f'left: {elem["posicion"][0]}px;\n'
                    self.css+=f'top: {elem["posicion"][1]}px;\n'
                else:
                    self.css+=f'left: 10px;\n'
                    self.css+=f'top: 10px;\n'
                self.css+='}\n\n'
                self.elementos.append(cont)
        self.aniadir()
        #print(self.css)
        #print(self.elementos)
    
    def aniadir(self):
        for elem in self.arreglo:
            if "add" in elem:
                for key,value in elem.items():
                    if "add" in key:
                        #id del padre, #id del hijo
                        self.buscar(elem["id"],value)

        self.verificaThis()

    
    def buscar(self,idP,idH):

        padre=""
        hijo=""
        for arr in self.elementos:
            if f'id="{idP}"' in arr:
                padre=arr
                break 

        for arr in self.elementos:
            if f'id="{idH}"' in arr:
                hijo=arr
                break
        #Agrega los hijos a un contenedor
        if f'id="{idP}"' in self.Concat:
            a=self.Concat.find(idP)
            indice=self.Concat[a:].find(">")+a+1
            izquierda=self.Concat[:indice]
            derecha=self.Concat[indice:]
            self.Concat=izquierda+hijo+derecha
            return
        elif f'id="{idH}"' in self.Concat:
            a=padre.find(idP)
            indice=padre[a:].find(">")+a+1
            izquierda=padre[:indice]
            derecha=padre[indice:]
            self.Concat=izquierda+self.Concat+derecha
            return
 
        indice=padre.find(">")+1
        izquierda=padre[:indice]
        derecha=padre[indice:]
        self.Concat+=izquierda+ hijo+derecha
    

    def verificaThis(self):
        for elem in self.arreglo:
            if "this" in elem:
                self.detectarThis(elem["id"])

        file=open("./primero.html","w+")
        file.write(self.html)
        file.close()
        file=open("./primero.css","w+")
        file.write(self.css)
        file.close()
        webbrowser.open_new_tab("primero.html")

    def detectarThis(self,id):
        if f'id="{id}"' not in self.Concat:
            indice=self.html.find("<body>")
            indice=self.html[indice:].find(">")+indice+1
            izquierda=self.html[:indice]
            derecha=self.html[indice+1:]
            a=[elem for elem in self.elementos if f'id="{id}"' in elem][0]
            self.html=izquierda+a+"\n"+derecha
        else:
            indice=self.html.find("<body>")
            indice=self.html[indice:].find(">")+indice+1
            izquierda=self.html[:indice]
            derecha=self.html[indice+1:]
            self.html=izquierda+self.Concat+"\n"+derecha

    def limpiar(self):
        self.Concat=""
        self.elementos.clear()
        self.arreglo.clear()