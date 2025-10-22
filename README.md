# Proyecto: Sistema de Gestión de Invitados con Reconocimiento Facial
## Objetivo
Automatizar el registro de invitados en eventos privados mediante reconocimiento facial,
evitando listas manuales y mejorando la seguridad y la experiencia de ingreso.

# Componentes del Sistema
## 1. Base de datos de invitados
-Carpeta con imágenes de los rostros de invitados autorizados.
-Los nombres se extraen del nombre del archivo (ej: juan_perez.jpg).

## 2. Script de registro en tiempo real
-Captura el rostro con la cámara web.
-Compara con la base de datos.
-Si hay coincidencia, registra nombre + hora en un archivo CSV.
-Muestra en pantalla el nombre del invitado y su rostro con un rectángulo.

## 3. Archivo de asistencia
-CSV con columnas: Nombre, Hora de ingreso, Evento.
-Se actualiza automáticamente cada vez que se reconoce un rostro.

# Estructura de carpetas
## Código
/proyecto_gestion_invitados/
│
├── invitados/ # Imágenes de invitados autorizados
│ ├── juan_perez.jpg
│ ├── maria_gomez.jpg
│
├── registros/
│ └── asistencia.csv # Archivo generado automáticamente
│
├── registrar_ingreso.py # Script principal
└── comparar_faces.py # Script auxiliar para pruebas

# Librerías necesarias
Librería Uso principal
face_recognition Detección y comparación de rostros
cv2 (OpenCV) Captura de cámara y visualización de imágenes
os Manejo de archivos e imágenes
datetime Registro de hora de ingreso
numpy Cálculo de distancias entre codificaciones

# Ideas para pruebas y mejoras
-Agregar detección de múltiples rostros en una misma imagen.
-Mostrar alerta si el rostro no está en la base.
-Agregar campo de evento o ubicación en el CSV.
-Simular distintos eventos con diferentes carpetas de invitado
