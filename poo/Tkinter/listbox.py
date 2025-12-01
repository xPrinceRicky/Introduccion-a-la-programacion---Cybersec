import tkinter as tk

def agregar_elemento():
    nuevo_elemento = entrada.get()
    if nuevo_elemento:
        lista.insert(tk.END, nuevo_elemento)
        entrada.delete(0, tk.END)

ventana = tk.Tk()
ventana.title("Lista de Dispositivos Electrónicos")
ventana.geometry("300x300")

entrada = tk.Entry(ventana, width=30)
entrada.pack(pady=10)

boton_agregar = tk.Button(ventana, text="Agregar dispositivo", command=agregar_elemento)
boton_agregar.pack(pady=5)

lista = tk.Listbox(ventana, width=40, height=10)
lista.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)

dispositivos_iniciales = ["Laptop", "Smartphone", "Tablet", "Smartwatch", "Auriculares", "Televisor", "PS5"]
for dispositivo in dispositivos_iniciales:
    lista.insert(tk.END, dispositivo)

ventana.mainloop()