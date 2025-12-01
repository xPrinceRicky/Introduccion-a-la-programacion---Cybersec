import tkinter as tk

ventana = tk.Tk()
ventana.title("Mi Primera Ventana")
ventana.geometry("300x150")

mensaje = tk.Label(ventana, text="¡Bienvenido a mi aplicación!", font=("Arial", 14))
mensaje.pack(pady=20)

ventana.mainloop()