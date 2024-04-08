import requests
import tkinter as tk
import tkinter.font as font
from tkinter import PhotoImage
from PIL import Image, ImageTk

def fetch_data(rut):
    url = 'https://unab.dentidesk.cl/api/validar.php'
    headers = {
        'Authorization': 'Bearer rH8X91djGOopmBXf6ajEOCnR1xrerZbZ8hiQHjA9enF7oKD0wNGKLtnMGfzIRaakYKsEhk30vsIL2u4u0pdK8jHqjPKsHkVXR8t0rcmVMIr4zjF6rJQedIfibeWmrUoS7zvS3wdyhcOo2SRkd30DYm'
    }
    data = {'rut': rut}
    response = requests.post(url, headers=headers, data=data)


    if response.status_code == 200:
        print("Paciente Encontrado!")
        return response.json()
    elif response.status_code == 404:
        error_message = response.json().get("error", "RUT no encontrado en la API")
        print("Error:", error_message)
        return {"error": error_message}
    else:
        return {"error": f"Error en la consulta: Código {response.status_code}"}


estados_cita = {
    '0': 'ELIMINADA',
    '47': 'NO CONFIRMADA',
    '48': 'CONFIRMADA',
    '49': 'HORA CANCELADA',
    '50': 'CONFIRMADO POR E-MAIL',
    '51': 'CANCELADO POR E-MAIL',
    '59': 'SALA DE ESPERA',
    '61': 'NO ASISTE',
    '52': 'ATENDIDO'
    # AÑADE AQUÍ MÁS ESTADOS SEGÚN SEA NECESARIO
}

def update_display():

    rut = rut_entry.get()
    text_to_display = ""

    if rut:  # Verificar que el campo RUT no esté vacío
        data = fetch_data(rut)

        if "error" in data:
            rut_entry.delete(0, tk.END)
            error = data['error']
            print(error)
            if error == "Paciente no encontrado":
                text_to_display = f"Error\n{data['error']}\n\nPaciente nuevo, pasar al totem"
            else:
                text_to_display = f"Error\n{data['error']}\n\nSolicitar al paciente que se registre"

            text_widget.config(state=tk.NORMAL)
            text_widget.delete(1.0, tk.END)
            text_widget.insert(tk.END, text_to_display, "custom_font")
            text_widget.tag_add("center", "1.0", "end")
            text_widget.config(state=tk.DISABLED)

        else:
            nombre_paciente = data['AGENDA']['NOMBRE_PACIENTE']
            rut_paciente = data['PACIENTE']['RUT']
            fecha_cita = data['AGENDA']['FECHA']
            estado_cita = (data['AGENDA']['ESTADO'])

            # OBTENER LA DESCRIPCIÓN DEL ESTADO
            descripcion_estado = estados_cita.get(estado_cita, 'Estado desconocido')
            rut_formateado = formatear_rut(rut_paciente)

            text_to_display += "\n"
            text_to_display += f"{nombre_paciente}\n"
            text_to_display += f"{rut_formateado}\n\n"
            text_to_display += f"Datos de la cita\n{fecha_cita}\n"
            text_to_display += f"Estado: {descripcion_estado}"

            # LIMPIAR EL ENTRY DESPUÉS DE LA BÚSQUEDA
            rut_entry.delete(0, tk.END)

            text_widget.config(state=tk.NORMAL)
            text_widget.delete(1.0, tk.END)
            text_widget.insert(tk.END, text_to_display, "custom_font")
            text_widget.tag_add("center", "1.0", "end")
            text_widget.config(state=tk.DISABLED)

            #pass

    else:

        # LIMPIAR EL ENTRY DESPUÉS DE LA BÚSQUEDA
        rut_entry.delete(0, tk.END)

        text_widget.config(state=tk.NORMAL)
        text_widget.delete(1.0, tk.END)
        text_widget.insert(tk.END, 'Por favor, ingrese un RUT', "custom_font")
        text_widget.tag_add("center", "1.0", "end")
        text_widget.config(state=tk.DISABLED)

def formatear_rut(rut):
    # Eliminar cualquier carácter que no sea un dígito o la letra 'k' (mayúscula o minúscula)
    rut = ''.join(filter(lambda x: x.isdigit() or x.lower() == 'k', rut))

    # Separar el dígito verificador del resto del RUT
    rut_body = rut[:-1]
    rut_verificador = rut[-1]

    # Formatear el cuerpo del RUT con puntos separadores cada tres dígitos
    rut_formateado = '{}.{}.{}-{}'.format(
        rut_body[-9:-6], rut_body[-6:-3], rut_body[-3:], rut_verificador
    )

    return rut_formateado




# CREAR LA VENTANA PRINCIPAL
root = tk.Tk()
root.title("Consulta de Citas")
root.state('zoomed')


# CONFIGURAR LAS FILAS Y COLUMNAS PARA QUE SE EXPANDAN
root.grid_columnconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=2)
root.grid_columnconfigure(2, weight=1)
root.grid_rowconfigure(0, weight=2)
root.grid_rowconfigure(1, weight=2)
root.grid_rowconfigure(2, weight=2)
root.grid_rowconfigure(3, weight=2)
root.grid_rowconfigure(4, weight=2)



# CONFIGURACIÓN DE LA FUENTE
label_font = font.Font(size=30)  # Ajusta el tamaño para el label
entry_font = font.Font(size=40)  # Ajusta el tamaño para el texto del entry
custom_font = font.Font(family="Helvetica", size=30)  # Cambia "Helvetica" y 12 al tipo y tamaño deseado


# LABEL CON FUENTE PERSONALIZADA
label = tk.Label(root, text="", font=label_font)
label.grid(row=0, column=1, padx=10, pady=10, sticky="sew")
label = tk.Label(root, text="Ingrese el RUT:", font=label_font)
label.grid(row=1, column=1, padx=10, pady=10, sticky="sew")

# ENTRY CON FUENTE PERSONALIZADA Y ANCHO ESPECÍFICO
rut_entry = tk.Entry(root, font=entry_font, justify=tk.CENTER, width=30)
rut_entry.grid(row=2, column=1, padx=10, pady=10, sticky="sew")
rut_entry.bind("<Return>", lambda event: update_display())  # Vinculación del evento ENTER
rut_entry.focus_set()

# CREAR UN WIDGET DE TEXTO PARA MOSTRAR LOS DATOS
text_widget = tk.Text(root, height=25, width=50)
text_widget.grid(row=3, column=1, padx=10, pady=10, sticky="ew")
text_widget.tag_configure("custom_font", font=custom_font)
text_widget.tag_configure("center", justify='center')
text_widget.config(state="disabled")

# Crear un botón para actualizar los datos
# fetch_button = tk.Button(root, text="Consultar Cita", command=update_display)
# fetch_button.grid(row=4, column=1, padx=10, pady=10, sticky="ew")

# CARGAR LA IMAGEN DEL LOGO
original_image = Image.open("logo.png")  # Reemplaza con la ruta a tu imagen
resized_image = original_image.resize((300, 120), Image.Resampling.LANCZOS)  # Cambia '50, 50' al tamaño deseado
logo_image = ImageTk.PhotoImage(resized_image)

# CREAR UN LABEL PARA EL LOGO Y POSICIONARLO EN LA PARTE SUPERIOR IZQUIERDA
logo_label = tk.Label(root, image=logo_image)
logo_label.place(x=10, y=10)

# INICIAR LA APLICACIÓN
root.mainloop()
