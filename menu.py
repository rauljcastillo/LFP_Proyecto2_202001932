from tkinter import *
from tkinter import ttk
from tkinter import filedialog
import webbrowser
from tkinter import messagebox
from tkinter.ttk import Treeview
from Analizador import Analizador

class Grapi:

    def __init__(self,tk:Tk) -> None:
        self.ventana=tk
        self.ob=Analizador()

    def callback(self,event):
        a,b=self.txt.index("insert").split(".")
        self.var.set(f"Lin. {a}, Col. {int(b)+1}")

    def llamar(self):
        self.ob.limpiar()
        self.tabla.delete(*self.tabla.get_children())
        self.cadena=self.txt.get("1.0","end")
        self.cadena=self.cadena.replace("\t","    ")
        self.lista=self.ob.Escanear(self.cadena)
        (erroresS,objeto)=self.ob.analisisSintactico()
        erroresL=self.ob.listaErr()
        if len(erroresS)>0 or len(erroresL)>0:
            for element in erroresL:
                self.tabla.insert("",END,values=(element.getTipo(),element.getFila(),element.getCol(),f"No se reconoce: {element.getLexema()}"))
            for element in erroresS:
                self.tabla.insert("",END,values=(element.getTipo(),element.getLinea(),"-",element.getDescrip()))
        else:
            objeto.empezar()

    def principal(self):
        menu=Menu(self.ventana)
        self.ventana.resizable(0,0)
        self.ventana.config(menu=menu)
        self.ventana.geometry("930x600")
        self.txt=Text(self.ventana,height=24,width=90)
        self.txt.place(x=20,y=20)
        btn=Button(self.ventana,text="Archivo etiquetas",command=self.etiquetas)
        btn.place(x=760,y=40,width=130,height=50)
        btn1=Button(self.ventana,text="Analizar",command=self.llamar)
        btn1.place(x=760,y=100,width=130,height=50)
        btn5=Button(self.ventana,text="Limpiar",command=self.limpiar)
        btn5.place(x=760,y=160,width=130,height=50)
        File=Menu(menu,tearoff=0)
        Ayuda=Menu(menu,tearoff=0)

        menu.add_cascade(label= "Archivo", menu=File)
        menu.add_cascade(label= "Ayuda",menu=Ayuda)
        File.add_command(label="Abrir",command=self.abrir)
        File.add_command(label="Guardar",command=self.guardar)
        File.add_command(label="Guardar como",command=self.guardarComo)
        File.add_separator()
        File.add_command(label="Salir",command=self.ventana.quit)
        Ayuda.add_command(label="Manual de usuario")
        Ayuda.add_command(label="Manual técnico")
        Ayuda.add_command(label="Ayuda")

        self.var=StringVar()
        self.var.set("Lin. 1, Col. 1")
        self.lbl=Label(self.ventana,textvariable=self.var,font=("Arial",12,"bold"))
        self.lbl.place(x=600,y=410)
        self.txt.bind("<KeyRelease>",self.callback)
        self.txt.bind("<ButtonRelease-1>",self.callback)

        self.tabla=Treeview(self.ventana,show="headings",columns=("col1","col2","col3","col4"),height=20)
        self.tabla.place(y=440,relheight=0.2,relwidth=1)
        self.tabla.heading("col1",text="Tipo de Error",anchor=CENTER)
        self.tabla.heading("col2",text="Linea",anchor=CENTER)
        self.tabla.heading("col3",text="Columna",anchor=CENTER)
        self.tabla.heading("col4",text="Descripción",anchor=CENTER)

        self.tabla.column("col1", anchor=CENTER, width=15)
        self.tabla.column("col2", anchor=CENTER, width=15)
        self.tabla.column("col3", anchor=CENTER,width=15)
        self.tabla.column("col4", anchor=CENTER)
        style=ttk.Style()
        style.theme_use('clam')
        
        style.configure(
        'Treeview',
        foreground="black",
        font=("Arial ",10,"bold"),
        rowheight=25)

        style.configure(
        'Treeview.Heading',
        font=("Arial",10,"bold"),
        rowheight=15,
        background="gray78") 
        scroll=Scrollbar(self.tabla,orient=VERTICAL,command=self.tabla.yview)
        scroll.pack(side=RIGHT,fill='y')
        self.tabla.configure(yscrollcommand=scroll.set)

        self.ventana.mainloop()

    def abrir(self):
        file=filedialog.askopenfile()
        if file:
            self.ruta=file.name
            try:
                archivo=open(self.ruta,"r")
                lectura=archivo.read()
                messagebox.showinfo(title="Exito",message="Archivo cargado con éxito")
                self.txt.delete("1.0","end")
                self.txt.insert(INSERT,lectura)
                archivo.close()
            except:
                messagebox.showerror(title="Error",message="Error al leer el archivo")
    def guardar(self):
        self.cadena=self.txt.get("1.0","end")
        try:
            file=open(self.ruta,"w")
            file.write(self.cadena)
            file.close()
            messagebox.showinfo(title="Archivo guardado",message="Archivo guardado")
        except:
            messagebox.showerror("Error",message="Error al guardar")
    
    def guardarComo(self):
        self.cadena=self.txt.get("1.0","end")
        archivos = filedialog.asksaveasfilename(filetypes=[("Archivos",".txt")],defaultextension=".txt")
        if archivos:
            ar=open(archivos,"w")
            ar.write(self.cadena)
            ar.close()
    

    def etiquetas(self):
        contador=1
        html="""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Tabla de tokens</title>
    <style>
        body {
            background-color: #C8EEFF;
            font-family: Arial, Helvetica, sans-serif;
            display: flex;
            flex-direction: column;
            align-items: center;
    }

        #contenedor {
            display: flex;
            width: 50%;
            background-color: white;
            padding: 0px,10px,10px;
            justify-content: center;
            box-shadow: 0px 7px 29px 0px gray;
    }

        table {
            width: 100%;
            text-align: center;
        }

        th,td {
            padding: 8px;
            height: 20px;
        }

        thead {
            background-color: aquamarine;
        }
    </style>
</head>
<body>
    <h1>Tabla de Tokens</h1>
    <div id="contenedor">
    <table>
        <thead>
            <tr>
                <th>No</th>
                <th>Token</th>
                <th>Valor</th>
                <th>Linea</th>
                <th>Columna</th>
            </tr>
        </thead>
"""
        for elem in self.lista:
            html+='            <tr>\n'
            html+=f'               <td>{contador}</td>\n'
            html+=f'               <td>{elem.getTipo()}</td>\n'
            html+=f'               <td>{elem.getVal()}</td>\n'
            html+=f'               <td>{elem.getFil()}</td>\n'
            html+=f'               <td>{elem.getCol()}</td>\n'
            html+='            </tr>\n'
            contador+=1
        html+='        </table>\n'
        html+='    </div>\n'
        html+='</body>\n'
        html+='</html>\n'
        file=open("Etiquetas.html","w+")
        file.write(html)
        file.close()
        print("")
        webbrowser.open_new_tab("Etiquetas.html")


    def limpiar(self):
        self.txt.delete("1.0","end")
        self.ob.limpiar()

ob=Grapi(Tk())
ob.principal()