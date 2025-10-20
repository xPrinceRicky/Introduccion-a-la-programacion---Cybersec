Proceso GestorContraseñasSeguras
    Definir totalUsuarios, opcion, tope, i, j Como Entero
    Definir usuario, contra, contraMask, mensajeFallo Como Cadena
    Definir esDebil Como Logico
	
    totalUsuarios <- 0
    tope <- 5
	
    Dimension usuarios[tope]
    Dimension contrasenas[tope]
    Dimension debil[tope]
	
    Repetir
        Escribir ""
        Escribir "GESTOR DE CONTRASEÑAS SEGURAS"
        Escribir "1. Registrar usuario"
        Escribir "2. Mostrar todos los registros"
        Escribir "3. Salir"
        Escribir "Seleccione una opción: "
        Leer opcion
		
        Segun opcion Hacer
            1:
                Si totalUsuarios < tope Entonces
                    totalUsuarios <- totalUsuarios + 1
                    Escribir "Ingrese nombre de usuario: "
                    Leer usuarios[totalUsuarios]
                    Escribir "Ingrese contraseña: "
                    Leer contrasenas[totalUsuarios]
					
                    
                    esDebil <- Verificar_Contrasena_Pro(contrasenas[totalUsuarios], mensajeFallo)
                    debil[totalUsuarios] <- esDebil
					
                    Si esDebil Entonces
                        Escribir "?? Contraseña débil: ", mensajeFallo
                    SiNo
                        Escribir "? Contraseña segura."
                    FinSi
                SiNo
                    Escribir "Error: máximo de registros alcanzado (", tope, ")."
                FinSi
				
            2:
                Si totalUsuarios = 0 Entonces
                    Escribir "No hay usuarios registrados."
                SiNo
                    Escribir "=== LISTA DE USUARIOS ==="
                    Para i <- 1 Hasta totalUsuarios Con Paso 1 Hacer
                        
                        contraMask <- ""
                        Para j <- 1 Hasta Longitud(contrasenas[i]) Con Paso 1 Hacer
                            contraMask <- contraMask + "*"
                        FinPara
                        Escribir i, ". Usuario: ", usuarios[i], " | Contraseña: ", contraMask
                        Si debil[i] Entonces
                            Escribir "   ?? Débil: ", mensajeFallo
                        FinSi
                    FinPara
                FinSi
				
            3:
                Escribir "Saliendo..."
        FinSegun
    Hasta Que opcion = 3
FinProceso


Funcion resultado <- Verificar_Contrasena_Pro(contra, mensaje)
    Definir i, lon Como Entero
    Definir caracter Como Caracter
    Definir tieneMayus, tieneMinus, tieneNum, tieneSimbolo Como Logico
	
    tieneMayus <- Falso
    tieneMinus <- Falso
    tieneNum <- Falso
    tieneSimbolo <- Falso
    mensaje <- ""
	
    lon <- Longitud(contra)
	
    Si lon = 0 Entonces
        resultado <- Verdadero
        mensaje <- "Contraseña vacía"
    SiNo
        Para i <- 1 Hasta lon Con Paso 1 Hacer
            caracter <- Subcadena(contra, i, i)
			
            
            Si caracter = "A" O caracter = "B" O caracter = "C" O caracter = "D" O caracter = "E" O caracter = "F" O caracter = "G" O caracter = "H" O caracter = "I" O caracter = "J" O caracter = "K" O caracter = "L" O caracter = "M" O caracter = "N" O caracter = "O" O caracter = "P" O caracter = "Q" O caracter = "R" O caracter = "S" O caracter = "T" O caracter = "U" O caracter = "V" O caracter = "W" O caracter = "X" O caracter = "Y" O caracter = "Z" Entonces
                tieneMayus <- Verdadero
            FinSi
			
            
            Si caracter = "a" O caracter = "b" O caracter = "c" O caracter = "d" O caracter = "e" O caracter = "f" O caracter = "g" O caracter = "h" O caracter = "i" O caracter = "j" O caracter = "k" O caracter = "l" O caracter = "m" O caracter = "n" O caracter = "o" O caracter = "p" O caracter = "q" O caracter = "r" O caracter = "s" O caracter = "t" O caracter = "u" O caracter = "v" O caracter = "w" O caracter = "x" O caracter = "y" O caracter = "z" Entonces
                tieneMinus <- Verdadero
            FinSi
			
            
            Si caracter = "0" O caracter = "1" O caracter = "2" O caracter = "3" O caracter = "4" O caracter = "5" O caracter = "6" O caracter = "7" O caracter = "8" O caracter = "9" Entonces
                tieneNum <- Verdadero
            FinSi
			
            
            Si caracter = "@" O caracter = "#" O caracter = "$" O caracter = "%" O caracter = "&" O caracter = "!" Entonces
                tieneSimbolo <- Verdadero
            FinSi
        FinPara
		
        resultado <- Falso
        mensaje <- ""
		
        Si lon < 8 Entonces
            resultado <- Verdadero
            mensaje <- mensaje + "Contraseña muy corta; "
        FinSi
        Si No tieneMayus Entonces
            resultado <- Verdadero
            mensaje <- mensaje + "Falta mayúscula; "
        FinSi
        Si No tieneMinus Entonces
            resultado <- Verdadero
            mensaje <- mensaje + "Falta minúscula; "
        FinSi
        Si No tieneNum Entonces
            resultado <- Verdadero
            mensaje <- mensaje + "Falta número; "
        FinSi
        Si No tieneSimbolo Entonces
            resultado <- Verdadero
            mensaje <- mensaje + "Falta símbolo especial (@,#,$,%,&,!); "
        FinSi
    FinSi
FinFuncion