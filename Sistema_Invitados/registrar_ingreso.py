import cv2
import face_recognition as fr
import os
import numpy as np
from datetime import datetime

# === CONFIGURACIÓN ===
EVENTO = "Casamiento Juanma 2025"
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
RUTA_INVITADOS = os.path.join(SCRIPT_DIR, 'Invitados')
RUTA_REGISTROS = os.path.join(SCRIPT_DIR, 'Registros')
ARCHIVO_ASISTENCIA = os.path.join(RUTA_REGISTROS, 'asistencia.csv')

os.makedirs(RUTA_REGISTROS, exist_ok=True)

mis_imagenes = []
nombres_empleados = []
lista_empleados = os.listdir(RUTA_INVITADOS)

for nombre in lista_empleados:
    if nombre.endswith(('.jpg', '.jpeg', '.png')):
        imagen_actual = cv2.imread(os.path.join(RUTA_INVITADOS, nombre))
        if imagen_actual is not None:
            mis_imagenes.append(imagen_actual)
            nombres_empleados.append(os.path.splitext(nombre)[0])

print("[INFO] Invitados cargados:", nombres_empleados)

def codificar_imagenes(imagenes):
    lista_codificada = []
    for imagen in imagenes:
        imagen_rgb = cv2.cvtColor(imagen, cv2.COLOR_BGR2RGB)
        try:
            codificado = fr.face_encodings(imagen_rgb)[0]
            lista_codificada.append(codificado)
        except IndexError:
            print("[ERROR] No se pudo codificar una imagen. Asegúrate de que tenga un rostro visible.")
            continue
    return lista_codificada

lista_empleados_codificada = codificar_imagenes(mis_imagenes)

def registrar_ingresos(persona, evento=EVENTO):
    archivo_path = ARCHIVO_ASISTENCIA

    if not os.path.exists(archivo_path):
        with open(archivo_path, 'w', encoding='utf-8') as f:
            f.write("Nombre,Hora,Evento\n")

    with open(archivo_path, 'r', encoding='utf-8') as f:
        lineas = f.readlines()
        nombres_registrados = [linea.split(',')[0].strip() for linea in lineas[1:]]

    if persona not in nombres_registrados:
        ahora = datetime.now().strftime('%H:%M:%S')
        with open(archivo_path, 'a', encoding='utf-8') as f:
            f.write(f"{persona},{ahora},{evento}\n")
        print(f"[REGISTRADO] {persona} a las {ahora}")
    else:
        print(f"[YA REGISTRADO] {persona}")

# === ABRE LA CÁMARA VIRTUAL DE OBS CON DETECCIÓN AUTOMÁTICA ===
backends = [cv2.CAP_DSHOW, cv2.CAP_MSMF, None]
indices_a_probar = [0, 1, 2, 3, 4]
captura = None

for idx in indices_a_probar:
    for backend in backends:
        if backend is None:
            captura = cv2.VideoCapture(idx)
        else:
            captura = cv2.VideoCapture(idx, backend)
        
        if captura.isOpened():
            ret, frame = captura.read()
            if ret:
                print(f"[INFO] Cámara abierta con índice {idx} y backend {backend if backend else 'auto'}")
                break
            else:
                captura.release()
                captura = None
    if captura is not None:
        break

if captura is None:
    print("[ERROR] No se pudo abrir ninguna cámara. Verifica que OBS VirtualCam esté activo.")
    exit()

print("[INFO] Sistema activo. Presiona 'q' para salir.")

while True:
    exito, imagen = captura.read()
    if not exito:
        print("[ERROR] Error al capturar imagen.")
        break

    cara_locations = fr.face_locations(imagen)
    cara_encodings = fr.face_encodings(imagen, cara_locations)

    for (top, right, bottom, left), face_encoding in zip(cara_locations, cara_encodings):
        coincidencias = fr.compare_faces(lista_empleados_codificada, face_encoding, tolerance=0.6)
        distancias = fr.face_distance(lista_empleados_codificada, face_encoding)

        if len(distancias) > 0:
            indice_mejor_coincidencia = np.argmin(distancias)

            if coincidencias[indice_mejor_coincidencia]:
                nombre = nombres_empleados[indice_mejor_coincidencia]
                color_rect = (0, 255, 0)
                texto = nombre
                registrar_ingresos(nombre)
            else:
                nombre = "Desconocido"
                color_rect = (0, 0, 255)
                texto = "Desconocido"

            cv2.rectangle(imagen, (left, top), (right, bottom), color_rect, 2)
            cv2.rectangle(imagen, (left, bottom - 35), (right, bottom), color_rect, cv2.FILLED)
            cv2.putText(imagen, texto, (left + 6, bottom - 6),
                        cv2.FONT_HERSHEY_DUPLEX, 0.8, (255, 255, 255), 1)

    cv2.imshow('Sistema de Asistencia Facial', imagen)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

captura.release()
cv2.destroyAllWindows()
print("[INFO] Sistema cerrado.")