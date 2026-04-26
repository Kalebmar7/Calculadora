import tkinter as tk
import speech_recognition as sr
import csv
from datetime import datetime

ARCHIVO = "historial_ventas.csv"

# -------- FUNCIONES --------

def guardar_venta(total, pago, cambio):
    with open(ARCHIVO, mode="a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([datetime.now(), total, pago, cambio])

modo = "total"

def agregar_numero(num):
    if modo == "total":
        entry_total.insert(tk.END, num)
    else:
        entry_pago.insert(tk.END, num)

def limpiar():
    entry_total.delete(0, tk.END)
    entry_pago.delete(0, tk.END)
    resultado.set("")

def cambiar_modo(nuevo):
    global modo
    modo = nuevo
    resultado.set(f"Editando: {modo.upper()}")

def calcular():
    try:
        total = float(entry_total.get())
        pago = float(entry_pago.get())
        cambio = pago - total
        resultado.set(f"Cambio: ${cambio:.2f}")
        guardar_venta(total, pago, cambio)
    except:
        resultado.set("Error en datos")

# -------- VOZ --------

def usar_voz():
    r = sr.Recognizer()

    try:
        with sr.Microphone() as source:
            resultado.set("Escuchando...")
            root.update()

            r.adjust_for_ambient_noise(source, duration=1)

            audio = r.listen(source, timeout=5, phrase_time_limit=5)

            resultado.set("Procesando...")
            root.update()

            texto = r.recognize_google(audio, language="es-MX")
            resultado.set(f"{texto}")

            palabras = texto.split()
            numeros = [float(p) for p in palabras if p.replace('.', '', 1).isdigit()]

            if len(numeros) >= 2:
                entry_total.delete(0, tk.END)
                entry_pago.delete(0, tk.END)

                entry_total.insert(0, numeros[0])
                entry_pago.insert(0, numeros[1])

                calcular()
            else:
                resultado.set("Di 2 números")

    except sr.WaitTimeoutError:
        resultado.set("No hablaste")
    except sr.UnknownValueError:
        resultado.set("No entendí")
    except Exception as e:
        resultado.set("Error micrófono")

# -------- UI --------

root = tk.Tk()
root.title("Caja Cute 💖")
root.geometry("320x520")
root.configure(bg="#fff0f5")  # rosa pastel

resultado = tk.StringVar()

# Pantalla
frame_display = tk.Frame(root, bg="#ffe4ec", bd=0)
frame_display.pack(fill="both", padx=15, pady=15)

entry_total = tk.Entry(frame_display, font=("Arial", 16), justify="right",
                       bd=0, bg="#fff", relief="flat")
entry_total.pack(fill="x", pady=5, ipady=8)

entry_pago = tk.Entry(frame_display, font=("Arial", 16), justify="right",
                      bd=0, bg="#fff", relief="flat")
entry_pago.pack(fill="x", pady=5, ipady=8)

tk.Label(frame_display, textvariable=resultado,
         bg="#ffe4ec", fg="#d63384",
         font=("Arial", 12)).pack(pady=5)

# Botones
frame = tk.Frame(root, bg="#fff0f5")
frame.pack()

botones = [
    ("7","8","9"),
    ("4","5","6"),
    ("1","2","3"),
    ("0",".","C")
]

for fila in botones:
    f = tk.Frame(frame, bg="#fff0f5")
    f.pack()
    for b in fila:
        tk.Button(
            f,
            text=b,
            width=6,
            height=2,
            bg="#ff85a2",
            fg="white",
            font=("Arial", 14),
            bd=0,
            activebackground="#ff5c8a",
            command=lambda x=b: limpiar() if x=="C" else agregar_numero(x)
        ).pack(side="left", padx=6, pady=6)

# Acciones
tk.Button(root, text="TOTAL", command=lambda: cambiar_modo("total"),
          bg="#ffc2d1", width=20, bd=0).pack(pady=5)

tk.Button(root, text="PAGO", command=lambda: cambiar_modo("pago"),
          bg="#ffc2d1", width=20, bd=0).pack(pady=5)

tk.Button(root, text="CALCULAR 💸", command=calcular,
          bg="#ff4d6d", fg="white",
          width=20, height=2, bd=0).pack(pady=8)

tk.Button(root, text="🎤 Usar voz", command=usar_voz,
          bg="#ff8fab", width=20, bd=0).pack(pady=5)

root.mainloop()
