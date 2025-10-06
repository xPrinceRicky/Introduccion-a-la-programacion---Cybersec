Algoritmo internet_encasa
	Definir internet Como Logico
    Definir respuesta Como Entero
    
    Escribir "¿Tiene internet en casa? (1 = Sí, 0 = No): "
    Leer respuesta
    
    Si respuesta = 1 Entonces
        internet <- Verdadero
    SiNo
        internet <- Falso
    FinSi
    
    Escribir "Valor lógico guardado: ", internet
	
FinAlgoritmo
