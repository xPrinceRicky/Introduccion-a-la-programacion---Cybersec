import tkinter as tk

def mostrar_texto():
    texto_ingresado = entrada.get()
    etiqueta_resultado.config(text=texto_ingresado)

ventana = tk.Tk()
ventana.title("Aprendiendo a usar Tkinter")
ventana.geometry("400x150")

entrada = tk.Entry(ventana, width=30)
entrada.pack(pady=10)

boton = tk.Button(ventana, text="Mostrar Texto", command=mostrar_texto)
boton.pack(pady=5)

etiqueta_resultado = tk.Label(ventana, text="")
etiqueta_resultado.pack(pady=10)


ventana.mainloop()