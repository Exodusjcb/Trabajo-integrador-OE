"""
SISTEMA DE GESTIÓN DE VACACIONES - CHATBOT SIMULADOR
Trabajo Práctico Integrador - Organización Empresarial
"""

import json
import datetime
from typing import Dict, List, Optional

# ============== CARGA DE DATOS ==============

def cargar_empleados() -> List[Dict]:
    """Carga la base de datos de empleados desde JSON"""
    try:
        with open("empleados.json", "r", encoding="utf-8") as archivo:
            return json.load(archivo)
    except FileNotFoundError:
        print("⚠️ Archivo empleados.json no encontrado. Creando base vacía.")
        return []

def cargar_solicitudes() -> List[Dict]:
    """Carga el historial de solicitudes desde JSON"""
    try:
        with open("solicitudes.json", "r", encoding="utf-8") as archivo:
            return json.load(archivo)
    except FileNotFoundError:
        return []

def guardar_solicitudes(solicitudes: List[Dict]):
    """Guarda las solicitudes en JSON"""
    with open("solicitudes.json", "w", encoding="utf-8") as archivo:
        json.dump(solicitudes, archivo, indent=4, ensure_ascii=False)

# ============== MÁQUINA DE ESTADOS ==============

class ChatBotVacaciones:
    """Simulador de chatbot para gestión de vacaciones"""

    def __init__(self):
        self.empleados = cargar_empleados()
        self.solicitudes = cargar_solicitudes()
        self.estado_actual = "INICIO"
        self.usuario_actual = None
        self.solicitud_actual = None

    def iniciar(self):
        """Inicia la conversación con el usuario"""
        print("\n" + "="*60)
        print("🤖 ¡Hola! Soy el asistente de gestión de vacaciones.")
        print("📅 ¿En qué puedo ayudarte hoy?")
        print("="*60)
        self.estado_actual = "ESPERANDO_NOMBRE"
        self.pedir_nombre()

    def pedir_nombre(self):
        """Pide el nombre del empleado"""
        print("\n👤 Por favor, ingresá tu nombre completo:")
        self.estado_actual = "ESPERANDO_NOMBRE"

    def verificar_empleado(self, nombre: str) -> Optional[Dict]:
        """Busca al empleado por nombre en la base de datos"""
        for empleado in self.empleados:
            if empleado["nombre"].lower() == nombre.lower():
                return empleado
        return None

    def calcular_antiguedad(self, empleado: Dict) -> int:
        """Calcula los años de antigüedad del empleado"""
        fecha_ingreso = datetime.datetime.strptime(
            empleado["fecha_ingreso"], "%Y-%m-%d"
        ).date()
        hoy = datetime.date.today()
        años = hoy.year - fecha_ingreso.year
        if hoy.month < fecha_ingreso.month or (
            hoy.month == fecha_ingreso.month and hoy.day < fecha_ingreso.day
        ):
            años -= 1
        return años

    def calcular_dias_extras(self, empleado: Dict) -> int:
        """Calcula días extras según antigüedad (Gateway 2)"""
        años = self.calcular_antiguedad(empleado)
        if años > 5:
            return 5  # +5 días extra
        return 0

    def procesar_mensaje(self, mensaje: str) -> str:
        """Procesa el mensaje del usuario según el estado actual"""

        # ESTADO: ESPERANDO_NOMBRE
        if self.estado_actual == "ESPERANDO_NOMBRE":
            empleado = self.verificar_empleado(mensaje)
            if empleado:
                self.usuario_actual = empleado
                # Verificar si tiene días disponibles
                if empleado["dias_disponibles"] <= 0:
                    self.estado_actual = "RECHAZADO"
                    return (
                        f"❌ Hola {empleado['nombre']}, no tenés días disponibles.\n"
                        f"📊 Días disponibles: {empleado['dias_disponibles']}\n"
                        f"💡 Consultá con tu supervisor para más información."
                    )
                else:
                    self.estado_actual = "ESPERANDO_FECHAS"
                    return (
                        f"✅ ¡Hola {empleado['nombre']}! "
                        f"Tenés {empleado['dias_disponibles']} días disponibles.\n"
                        f"📅 ¿Qué fechas querés solicitar? (formato: DD/MM/AAAA - DD/MM/AAAA)"
                    )
            else:
                return (
                    "❌ No encontré un empleado con ese nombre. "
                    "Por favor, verificá que esté escrito correctamente."
                )

        # ESTADO: ESPERANDO_FECHAS
        if self.estado_actual == "ESPERANDO_FECHAS":
            try:
                # Parsear fechas (ej: "10/07/2026 - 20/07/2026")
                partes = mensaje.split(" - ")
                if len(partes) != 2:
                    return "❌ Formato incorrecto. Usá: DD/MM/AAAA - DD/MM/AAAA"

                desde = datetime.datetime.strptime(partes[0].strip(), "%d/%m/%Y").date()
                hasta = datetime.datetime.strptime(partes[1].strip(), "%d/%m/%Y").date()

                if hasta < desde:
                    return "❌ La fecha 'hasta' debe ser posterior a la fecha 'desde'"

                # Calcular días solicitados
                dias_solicitados = (hasta - desde).days + 1

                # Gateway 1: Verificar disponibilidad
                dias_extras = self.calcular_dias_extras(self.usuario_actual)
                total_disponible = self.usuario_actual["dias_disponibles"] + dias_extras

                if dias_solicitados > total_disponible:
                    self.estado_actual = "RECHAZADO"
                    return (
                        f"❌ No tenés suficientes días disponibles.\n"
                        f"📊 Disponible: {total_disponible} días | Solicitado: {dias_solicitados} días\n"
                        f"💡 Podés solicitar hasta {total_disponible} días."
                    )

                # Crear solicitud
                self.solicitud_actual = {
                    "id": len(self.solicitudes) + 1,
                    "empleado_id": self.usuario_actual["id"],
                    "empleado_nombre": self.usuario_actual["nombre"],
                    "fecha_desde": desde.strftime("%Y-%m-%d"),
                    "fecha_hasta": hasta.strftime("%Y-%m-%d"),
                    "dias_solicitados": dias_solicitados,
                    "dias_extras": dias_extras,
                    "estado": "PENDIENTE",
                    "supervisor": self.usuario_actual["supervisor"],
                    "fecha_solicitud": datetime.date.today().strftime("%Y-%m-%d")
                }

                self.estado_actual = "NOTIFICANDO_SUPERVISOR"
                return (
                    f"✅ Solicitud registrada:\n"
                    f"📅 {dias_solicitados} días ({desde.strftime('%d/%m/%Y')} - {hasta.strftime('%d/%m/%Y')})\n"
                    f"📊 Días extra por antigüedad: +{dias_extras}\n"
                    f"👔 Enviando notificación a tu supervisor: {self.usuario_actual['supervisor']}\n"
                    f"\n⏳ Esperá la aprobación de tu supervisor...\n"
                    f"📝 ¿Aprueba la solicitud? (Si/No)"
                )

            except ValueError:
                return "❌ Formato de fecha inválido. Usá: DD/MM/AAAA - DD/MM/AAAA"

        # ESTADO: NOTIFICANDO_SUPERVISOR / ESPERANDO_APROBACION
        if self.estado_actual == "NOTIFICANDO_SUPERVISOR":
            if mensaje.lower() in ["si", "sí", "s"]:
                self.solicitud_actual["estado"] = "APROBADO"
                self.solicitudes.append(self.solicitud_actual)
                guardar_solicitudes(self.solicitudes)

                # Actualizar días disponibles del empleado
                for emp in self.empleados:
                    if emp["id"] == self.usuario_actual["id"]:
                        emp["dias_disponibles"] -= self.solicitud_actual["dias_solicitados"]

                self.estado_actual = "APROBADO"
                return (
                    f"✅ ¡FELICITACIONES! Tu solicitud de vacaciones fue APROBADA.\n"
                    f"📅 Disfrutá tus {self.solicitud_actual['dias_solicitados']} días.\n"
                    f"🌴 ¡Buenas vacaciones!"
                )
            elif mensaje.lower() in ["no", "n"]:
                self.solicitud_actual["estado"] = "RECHAZADO"
                self.solicitudes.append(self.solicitud_actual)
                guardar_solicitudes(self.solicitudes)
                self.estado_actual = "RECHAZADO"
                return (
                    f"❌ Lo sentimos. Tu solicitud de vacaciones fue RECHAZADA.\n"
                    f"💡 Te recomendamos consultar con tu supervisor para más información."
                )
            else:
                return "❌ Respondé con 'Si' o 'No' para continuar."

        # Estado FINAL
        if self.estado_actual in ["APROBADO", "RECHAZADO"]:
            return "🔚 El proceso ha finalizado. Gracias por usar el sistema."

# ============== MENÚ PRINCIPAL ==============

def mostrar_menu():
    print("\n" + "="*60)
    print("🌍 SISTEMA DE GESTIÓN DE VACACIONES 🌍")
    print("="*60)
    print("1. Iniciar nueva solicitud (Chatbot)")
    print("2. Ver empleados registrados")
    print("3. Ver historial de solicitudes")
    print("4. Salir")
    print("="*60)

def main():
    """Función principal del programa"""
    while True:
        mostrar_menu()
        opcion = input("\n📌 Elegí una opción: ")

        if opcion == "1":
            bot = ChatBotVacaciones()
            bot.iniciar()

            while True:
                # Mostrar el prompt según el estado
                if bot.estado_actual == "NOTIFICANDO_SUPERVISOR":
                    mensaje = input("\n👔 Supervisor: ")
                else:
                    mensaje = input("\n💬 Vos: ")

                if mensaje.lower() in ["salir", "exit", "fin", "chao"]:
                    print("👋 ¡Hasta luego! Gracias por usar el sistema.")
                    break

                respuesta = bot.procesar_mensaje(mensaje)
                print(f"\n🤖 Bot: {respuesta}")

                if bot.estado_actual in ["APROBADO", "RECHAZADO"]:
                    print("\n" + "=" * 60)
                    break

        elif opcion == "2":
            empleados = cargar_empleados()
            if empleados:
                print("\n📋 EMPLEADOS REGISTRADOS:")
                print("-" * 60)
                for emp in empleados:
                    print(f"👤 {emp['nombre']} | Días: {emp['dias_disponibles']} | Supervisor: {emp['supervisor']}")
            else:
                print("⚠️ No hay empleados registrados.")

        elif opcion == "3":
            solicitudes = cargar_solicitudes()
            if solicitudes:
                print("\n📋 HISTORIAL DE SOLICITUDES:")
                print("-" * 60)
                for sol in solicitudes:
                    estado = "✅ APROBADO" if sol["estado"] == "APROBADO" else "❌ RECHAZADO" if sol["estado"] == "RECHAZADO" else "⏳ PENDIENTE"
                    print(f"📅 {sol['empleado_nombre']} | {sol['dias_solicitados']} días | {estado}")
            else:
                print("⚠️ No hay solicitudes registradas.")

        elif opcion == "4":
            print("👋 ¡Hasta luego!")
            break

        else:
            print("❌ Opción inválida. Intentá de nuevo.")

if __name__ == "__main__":
    main()