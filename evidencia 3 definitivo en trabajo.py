import datetime
import sys
import pandas as pd
import csv
import os
import sqlite3
from sqlite3 import Error


def crearTabla():
    try:
        with sqlite3.connect("Evidencia.db") as conn:
            c = conn.cursor()
            c.execute("CREATE TABLE IF NOT EXISTS cosmetiqueria (clave INTEGER PRIMARY KEY, descripción_Articulo TEXT NOT NULL, cantidad_Vendida INTEGER NOT NULL, precio_Venta BOOLEAN NOT NULL, tiempo_Venta DATETIME NOT NULL);")
            print("Tabla creada exitosamente\n")
    except Error as e:
        print (e)
    except:
        print(f"Se produjo el siguiente error: {sys.exc_info()[0]}")

def InsertarRegistro():
    try:
        with sqlite3.connect("Evidencia.db") as conn:
            c = conn.cursor()
            c.execute("INSERT INTO cosmetiqueria VALUES()")
            print("registro creado exitosamente\n")
    except Error as e:
        print (e)
    except:
        print(f"Se produjo el siguiente error: {sys.exc_info()[0]}")
    finally:
        if (conn):
            conn.close()
    
    
def registroVentas():
    clave=1
    respuesta = 1
    dic_ventas={}
    total=[]
    print("***Registro de Venta***")
    
    while respuesta == 1:
        
        descArticulo=[]
        cantVendidas=[]
        precioVenta=[]
        tiempoVenta=[]
        
        #Aqui va el numero "clave" de la venta.
        print(f"Venta numero {clave}")
        
        #Aqui va una descripción breve del producto.
        descripcionArticulo = input("¿Cual es la descripción del articulo?: ")
        descArticulo.append(descripcionArticulo)
        
        #Aqui van las piezas compradas por el usuario.
        cantidadPiezasVendidas = int(input("¿Cual es la cantidad de piezas vendidas?: "))
        cantVendidas.append(cantidadPiezasVendidas)
        
        #Aqui va el precio de venta del articulo.
        precioDeVenta = int(input("¿Cual es el precio de venta?: "))
        
        #Aqui se multiplican las piezas vendidas por el precio unitario.
        total.append(precioDeVenta*cantidadPiezasVendidas)
        precioVenta.append(precioDeVenta)
        
        #Aqui se toma el tiempo de la maquina (dia/mes/año).
        time = datetime.datetime.now()
        time_1=time.strftime('%d/%m/%Y')
        tiempoVenta.append(str(time_1))
        
        dic_ventas["Descripcion_Articulo"]=descArticulo
        dic_ventas["Cantidad_Vendida"]=cantVendidas
        dic_ventas["Precio_Venta"]=precioVenta
        dic_ventas["Tiempo"]=tiempoVenta
        dic2=pd.DataFrame(dic_ventas)
        
        #Aqui se crea el archivo de CSV (Valores separados por comas)
        #Para la creacion de la hoja donde se guardan los datos de la venta.
        ruta = "ventas.csv"
        dic2.to_csv(ruta, index=None, mode="a", header=not os.path.isfile(ruta))
        
        #Aqui se cierra o se abre otra venta, mediante una pregunta al usuario.
        clave = clave + 1  
        respuesta = int(input("¿DESEA REGISTRAR OTRA VENTA?: 1-.SI/2-.NO: "))
        
        #Aqui cuando el usuario haya terminado de registrar sus ventas, se da el total de todos los articulos.
        if respuesta == 2:
            print(f"***TOTAL DE COMPRA***: {sum(total)}")

def consulta():
    try:
        dic3={}
        descArticulo2=[]
        cantVendidas2=[]
        precioVenta2=[]
        tiempoVenta2=[]
        clave=1
        clave1=0
        clave2=0
        
        print("***Consulta de Venta***")
        
        #Aqui se le pedira al usuario la fecha de su registro de venta para consulta.
        diaVenta=input("Dime el dia de la venta: ")
        mesVenta=input("Dime el mes de la venta: ")
        añoVenta=input("Dime el año de la venta: ")
                                                                                
        if len(mesVenta)==1:
            mesVenta=("0"+ mesVenta)
                                                                                    
        if len(diaVenta)==1:
            diaVenta2=("0"+diaVenta+"/")
            fecha=(diaVenta2+mesVenta+"/"+añoVenta)
        else:
            fecha=(diaVenta+"/"+mesVenta+"/"+añoVenta)
            print("")

        with open ('ventas.csv') as file:
            reader=csv.reader(file)
            for registro in reader:
                clave1=clave1+1
                if registro[-1]==fecha:
                    
                    descArticulo2.append(registro[0])
                    cantVendidas2.append(registro[1])
                    precioVenta2.append(registro[2])
                    tiempoVenta2.append(registro[3])
                                                        
                    clave=clave+1
                        
                elif registro[-1]!=fecha:
                    clave2=clave2+1
                    
            if clave2==clave1:
                print(f"No se tiene registro con esta fecha:( {fecha} ")
                
        try:
            dic3["Descripcion_del_Articulo"]=descArticulo2
            dic3["Cantidad_Vendido"]=cantVendidas2
            dic3["Precio_de_Venta"]=precioVenta2
            dic3["Tiempo_Compra"]=tiempoVenta2
            dataframe=pd.DataFrame(dic3)
            print(dataframe)
        except:
            print("No esta registrado")

    except:
        print("No esta registrado")

#Aqui se se encuentran las clases con el menu principal.
while True:
    print ("-CREANDO TABLA-")
    print ("." * 20)
    crearTabla()
    print ("********MENÚ********")
    
    print ("1-.Registrar una venta\n2-.Consultar venta por fecha\n3-.Salir")
    
    opcionInicial = int(input("Ingrese la opción que quiera realizar: "))
    
    if opcionInicial == 1:
        registroVentas()
        InsertarRegistro()
    
    if opcionInicial == 2:
        consulta()
    
    if opcionInicial == 3:
        break