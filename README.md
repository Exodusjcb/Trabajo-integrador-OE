# Sistema de Gestión de Solicitudes de Vacaciones

## 📌 Descripción
Sistema chatbot para automatizar el proceso de solicitud de vacaciones. Desarrollado como Trabajo Práctico Integrador para la materia **Organización Empresarial** de la Tecnicatura Universitaria en Programación. El sistema permite a los empleados solicitar vacaciones a través de un chatbot en consola, que verifica automáticamente la disponibilidad de días, calcula la antigüedad y gestiona la aprobación del supervisor.

## 🛠️ Tecnologías utilizadas
- **Python 3.x** - Lenguaje de programación
- **JSON** - Base de datos simulada (archivos `.json`)
- **Consola/Terminal** - Entorno de ejecución

## 📁 Estructura del proyecto

    tpi-vacaciones/
    ├── main.py # Código fuente principal
    ├── empleados.json # Base de datos de empleados
    ├── solicitudes.json # Historial de solicitudes
    ├── TPI_Organización_Empresarial.pdf # Informe completo
    ├── README.md # Este archivo
    └── images/
        ├── diagrama-bpmn-as-is.png
        ├── diagrama-bpmn-to-be.png
        ├── collage-capturas-consola.png
        └── capturas-ia/
            ├── captura-ia-1.png
            ├── captura-ia-2.png
            └── captura-ia-3.png




## 🚀 Instalación y ejecución
```bash
# Clonar el repositorio
git clone https://github.com/[tu-usuario]/tpi-vacaciones.git

# Acceder a la carpeta
cd tpi-vacaciones

# Ejecutar el programa
python main.py
📖 Cómo usar el sistema
Ejecutá python main.py

Seleccioná la opción "1. Iniciar nueva solicitud"

Ingresá tu nombre completo (ej: Juan Pérez)

Ingresá las fechas en formato DD/MM/AAAA - DD/MM/AAAA

Esperá la aprobación del supervisor y respondé Si o No

Recibí la notificación final

🧪 Casos de prueba
Caso	Descripción	Resultado esperado
Camino Feliz	Empleado con días, supervisor aprueba	✅ Solicitud APROBADA
Sin días	Empleado sin días disponibles	❌ Rechazo por falta de días
Supervisor rechaza	Supervisor responde "No"	❌ Solicitud RECHAZADA
Error de formato	Fecha con guiones (-) en lugar de barras (/)	❌ Mensaje de error de formato
Empleado inexistente	Nombre no registrado en la BD	❌ Empleado no encontrado
📊 Flujo del sistema
Empleado → Sistema verifica → Sistema calcula → Supervisor aprueba → Sistema notifica → Fin

👥 Autor
Julián García 

Informe PDF: TPI_Organizacion_Empresarial.pdf

Repositorio: https://github.com/[tu-usuario]/tpi-vacaciones

📚 Materia
Cátedra: Organización Empresarial

Institución: Tecnicatura Universitaria en Programación

Año: 2026

📝 Licencia
Este proyecto fue desarrollado con fines académicos.


