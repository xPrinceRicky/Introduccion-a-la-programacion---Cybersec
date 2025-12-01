import tkinter as tk

class Dibujador:
    def __init__(self):
        self.ventana = tk.Tk()
        self.ventana.title("Lienzo de Dibujo")
        self.ventana.geometry("500x400")
        
        self.canvas = tk.Canvas(self.ventana, bg="white", width=480, height=350)
        self.canvas.pack(pady=10)
        
        self.dibujando = False
        self.ultimo_x = None
        self.ultimo_y = None
        
        self.canvas.bind("<Button-1>", self.iniciar_dibujo)
        self.canvas.bind("<B1-Motion>", self.dibujar)
        self.canvas.bind("<ButtonRelease-1>", self.detener_dibujo)
        
        self.boton_limpiar = tk.Button(self.ventana, text="Limpiar Canvas", command=self.limpiar_canvas)
        self.boton_limpiar.pack(pady=5)
    
    def iniciar_dibujo(self, evento):
        self.dibujando = True
        self.ultimo_x = evento.x
        self.ultimo_y = evento.y
    
    def dibujar(self, evento):
        if self.dibujando and self.ultimo_x is not None and self.ultimo_y is not None:
            self.canvas.create_line(self.ultimo_x, self.ultimo_y, evento.x, evento.y, 
                                  width=2, fill="black")
            self.ultimo_x = evento.x
            self.ultimo_y = evento.y
    
    def detener_dibujo(self, evento):
        self.dibujando = False
        self.ultimo_x = None
        self.ultimo_y = None
    
    def limpiar_canvas(self):
        self.canvas.delete("all")
    
    def ejecutar(self):
        self.ventana.mainloop()

app = Dibujador()
app.ejecutar()