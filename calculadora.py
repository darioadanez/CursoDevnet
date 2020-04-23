import sys
import math
from getch import getch
ans = 0 #Variable global utilizada para guardar el resultado de la última operación
def logaritmo ():
    #Define e inicializa las variables que va a usar para guardar el resultado y salir del bucle while
    s=""
    global ans
    while s != 'q':
        print("\n¡Si desea realizar una operación con el resultado de la operación anterior introduzca 'ans'!")
        #Solicita la introducción de los dos 
        try:
            n1 = input("Introduzca el número que desee obtener su logaritmo neperiano: ")
        
            if n1 == 'ans':
                n1 = ans
            #Convierte a punto flotante los números introducidos
            
            n1=float(n1)
        except ValueError:
            print("\n¡¡¡ATENCIÓN!!!\nUno de los datos introducidos no es un número.")
            return
        except:
            print("Ha ocurrido un error")
            
        #Realiza la operación y muestra el resultado
        try:

            ans = math.log(n1)
            print("\nEl número resultante es", "{:.2f}".format(ans))
        except ValueError:
            print("\n¡¡¡ANTENCIÓN!!! \nDebe introducir un número positivo.")
        except:
            print("\nHa ocurrido un error.")

        s= input("\nSi desea salir introduzca 'q', de lo contrario, pulse cualquier botón: ")

def potencia():
    #Define e inicializa las variables que va a usar para guardar el resultado y salir del bucle while
    s=""
    global ans
    while s != 'q':
        print("\n¡Si desea realizar una operación con el resultado de la operación anterior introduzca 'ans'!")
        #Solicita la introducción de los dos 
        try:
            n1 = input("Introduzca la base: ")
            n2 = input("Introduzca el exponente: ")
            
            if n1 == 'ans':
                n1 = ans
            if n2 == 'ans':
                n2 = ans
            #Convierte a punto flotante los números introducidos
            
            n1=float(n1)
            n2=float(n2)
        
            #Realiza la potencia y muestra el resultado
            ans = math.pow(n1,n2) 
            print("\nEl número resultante es", "{:.2f}".format(ans))
        except ValueError:
            print("Uno de los datos introducidos no es un número.")
        except:
            print("Ha ocurrido un error")

        s= input("\nSi desea salir introduzca 'q', de lo contrario, pulse cualquier botón: ")
def raiz_cuadrada():
    s=""
    global ans
    while s != 'q':
        print("\n¡Si desea realizar una operación con el resultado de la operación anterior introduzca 'ans'!")
        #Solicita la introducción de los dos 
        try:
            n1 = input("Introduzca el número real sobre el que quiere obtener la raíz cuadrada: ")
            
            
            if n1 == 'ans':
                n1 = ans
            #Convierte a punto flotante el número introducido
            
            n1=float(n1)
        
            
        except ValueError:
            print("El dato introducido es introducido no es un número.")
            pass
        except:
            print("Ha ocurrido un error")
            pass
        try:
            #Hace la raíz y muestra el resultado
            ans = math.sqrt(n1)
            print("\nLa raíz cuadrada de",n1,"es","{:.2f}".format(ans),"y","{:.2f}".format(-ans))
        except ValueError:
                #Comprueba si el número es -1 para mostrar directamente la raiz
                if n1 == -1:
                    print("La raíz cuadrada de -1 es i")
                    return
                #Convierte el número a positivo para hacer la raiz
                n2 = n1 * (-1)
                ans = math.sqrt(n2)
                #Muestra el resultado incluyendo el número imaginario 'i'
                print("La raíz cuadrada de",n1,"es","{:.2f}".format(ans) + "i","y","{:.2f}".format(-ans) + "i") 
        except:
            print("Ha ocurrido un error")

        s= input("\nSi desea salir introduzca 'q', de lo contrario, pulse cualquier botón: ")

def division():
     #Define e inicializa las variables que va a usar para guardar el resultado y salir del bucle while
    s=""
    global ans
    while s != 'q':
        print("\n¡Si desea realizar una operación con el resultado de la operación anterior introduzca 'ans'!")
        #Solicita la introducción de los dos 
        try:
            n1 = input("Introduzca el dividendo: ")
            n2 = input("Introduzca el divisor: ")
            
            if n1 == 'ans':
                n1 = ans
            if n2 == 'ans':
                n2 = ans
            #Convierte a punto flotante los números introducidos
            
            n1=float(n1)
            n2=float(n2)
        
            #Realiza la suma y muestra el resultado
            ans = n1 / n2 
            print("\nEl resultado de la división es", "{:.2f}".format(ans))
        except ValueError:
            print("Uno de los datos introducidos no es un número.")
        except ZeroDivisionError:
            print("¡No se puede dividir un número por 0!")
        except:
            print("Ha ocurrido un error")
            
        s= input("\nSi desea salir introduzca 'q', de lo contrario, pulse cualquier botón: ")
def multiplicacion():

     #Define e inicializa las variables que va a usar para guardar el resultado y salir del bucle while
    s=""
    global ans
    while s != 'q':
        print("\n¡Si desea realizar una operación con el resultado de la operación anterior introduzca 'ans'!")
        #Solicita la introducción de los dos 
        try:
            n1 = input("Introduzca el multiplicando: ")
            n2 = input("Introduzca el multiplicador: ")
            
            if n1 == 'ans':
                n1 = ans
            if n2 == 'ans':
                n2 = ans
            #Convierte a punto flotante los números introducidos
            
            n1=float(n1)
            n2=float(n2)
        
            #Realiza la multiplicación y muestra el resultado
            ans = n1 * n2 
            print("\nEl producto de la multiplicación es", "{:.2f}".format(ans))
        except ValueError:
            print("Uno de los datos introducidos no es un número.")
        except:
            print("Ha ocurrido un error")

        s= input("\nSi desea salir introduzca 'q', de lo contrario, pulse cualquier botón: ")

def resta():
    #Define e inicializa las variables que va a usar para guardar el resultado y salir del bucle while
    s=""
    global ans
    while s != 'q':
        print("\n¡Si desea realizar una operación con el resultado de la operación anterior introduzca 'ans'!")
        #Solicita la introducción de los dos 
        try:
            n1 = input("Introduzca el minuendo: ")
            n2 = input("Introduzca el sustraendo: ")
            
            if n1 == 'ans':
                n1 = ans
            if n2 == 'ans':
                n2 = ans
            #Convierte a punto flotante los números introducidos
            
            n1=float(n1)
            n2=float(n2)
        
            #Realiza la resta y muestra el resultado
            ans = n1 - n2 
            print("\nEl resultado de la resta es", ans)
        except ValueError:
            print("Uno de los datos introducidos no es un número.")
        except:
            print("Ha ocurrido un error")   
        s= input("\nSi desea salir introduzca 'q', de lo contrario, pulse cualquier botón: ")



def suma():
    #Define e inicializa las variables que va a usar para guardar el resultado y salir del bucle while
    s=""
    global ans
    while s != 'q':
        print("\n¡Si desea realizar una operación con el resultado de la operación anterior introduzca 'ans'!")
        #Solicita la introducción de los dos 
        try:
            n1 = input("Introduzca el primer sumando: ")
            n2 = input("Introduzca el segundo sumando: ")
            
            if n1 == 'ans':
                n1 = ans
            if n2 == 'ans':
                n2 = ans
            #Convierte a punto flotante los números introducidos
            
            n1=float(n1)
            n2=float(n2)
        
            #Realiza la suma y muestra el resultado
            ans = n1 + n2 
            print("\nEl resultado de la suma es", ans)
        except ValueError:
            print("Uno de los sumandos introducidos no es un número.")
        except:
            print("Ha ocurrido un error")
        s= input("\nSi desea salir introduzca 'q', de lo contrario, pulse cualquier botón: ")
def default():
    print("\n!La opción que ha introducido no es válida!")
def adios():
    print("!Adiós! Ha sido un placer.")
def main():
    
    opcion = 0 # Inicializa la variable opción, que almacenará la opción elegida por el usuario
    #Crea un diccionario para emular la estructura switch-case de otros lenguajes de programación
    dict= {

            1 : suma,
            2 : resta,
            3 : multiplicacion,
            4 : division,
            5 : raiz_cuadrada,
            6 : potencia,
            7 : logaritmo, 
            8 : adios
        }
    #Mientras la opción introducida. Mientras no sea la de salir, sigue en el programa
    while opcion != 8:
       
        print(
        """
        +=============================================+
        | ¡Bienvenido a la calculadora Python!        |
        | Seleccione la operación que desee realizar. |
        +=============================================+
        """)
        print("""
        +=============================================+
        | 1.- Suma                                    |
        | 2.- Resta                                   |
        | 3.- Multiplicación                          |
        | 4.- División                                |
        | 5.- Raíz cuadrada                           |
        | 6.- Potencia                                |
        | 7.- Logaritmo neperiano                     |
        | 8.- Salir de a calculadora                  |
        +=============================================+
        """)
        try:
            opcion = int(input("Opción: "))
        except:
            print("Debe introducir un número entero")
        
        dict.get(opcion,default)()
    
if __name__ == "__main__":
    
    
    main()


        

