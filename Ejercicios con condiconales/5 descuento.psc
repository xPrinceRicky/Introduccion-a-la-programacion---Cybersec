Algoritmo numero_posnegcer
	Definir monto, descuento, total Como Real
	
	Escribir "Ingrese el monto toal de su compra"
	Leer monto
	
	Si monto > 500 Entonces
		descuento <- monto * 0.10
        total <- monto - descuento
        Escribir "Se aplicó un 10% de descuento de " descuento " pesos"
		Escribir "El monto total es " total " pesos"
    SiNo
        total <- monto
        Escribir "No se aplica descuento."
    FinSi
	
FinAlgoritmo
