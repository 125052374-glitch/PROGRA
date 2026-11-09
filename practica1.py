
 
    #Practica de tipos de datos
 
 
TIEMPO_DE_ESPERA = 5
SEPARADOR = "*" * 54
    
print(SEPARADOR)
    
def demo_datos():
    """Tiene que estar comitado hasta los cometarios"""
    print("Vamosa imprimir los tipos de datos")
    print(SEPARADOR)
    print()
    print()
    print()
    puerto = 443 #valor entero
    latencia = 67.8 #valor float
    hostname= "Hola+adios" #cadena de texto
    
    for valor in (puerto, latencia, hostname):
        print(f"{str(valor):<12} -> {type(valor)}")
        
    
if __name__ == "__main__":
    demo_datos() 


#https://github.com/massgravel/microsoft-activation-scripts
    
    