import tkinter as tk

def sumar():
    try:
        num1 = float(entrada1.get())
        num2 = float(entrada2.get())
        resultado = num1 + num2
        etiqueta_resultado.config(text=f"Resultado: {resultado}")
    except ValueError:
        etiqueta_resultado.config(text="Error: Ingresa números válidos")

ventana = tk.Tk()
ventana.title("Calculadora Sencilla")
ventana.geometry("300x200")

tk.Label(ventana, text="Número 1:").pack(pady=5)
entrada1 = tk.Entry(ventana)
entrada1.pack(pady=5)

tk.Label(ventana, text="Número 2:").pack(pady=5)
entrada2 = tk.Entry(ventana)
entrada2.pack(pady=5)

boton_sumar = tk.Button(ventana, text="Sumar", command=sumar)
boton_sumar.pack(pady=10)


etiqueta_resultado = tk.Label(ventana, text="Resultado: ")
etiqueta_resultado.pack(pady=10)


ventana.mainloop()