"""Menu principal de consola para el CRUD de estudiantes."""

from typing import Callable

from app.exceptions import ErrorDominio
from app.models.estudiante import Estudiante
from app.services.estudiante_servicio import EstudianteServicio
from app.ui import mensajes

CANCELAR = "cancelar"


class MenuPrincipal:
    """Interfaz de consola para gestionar estudiantes.

    Args:
        servicio: servicio de negocio de estudiantes.
    """

    def __init__(self, servicio: EstudianteServicio) -> None:
        self._servicio = servicio
        self._acciones: dict[str, Callable[[], None]] = {
            "1": self._registrar,
            "2": self._listar,
            "3": self._buscar,
            "4": self._actualizar,
            "5": self._eliminar,
            "6": self._mostrar_ayuda,
        }

    def ejecutar(self) -> None:
        """Ejecuta el ciclo principal del menu."""
        print(mensajes.TITULO_APP)
        while True:
            print(mensajes.MENU_PRINCIPAL)
            opcion = input(mensajes.PROMPT_OPCION).strip().lower()
            if opcion == "0":
                print(mensajes.MENSAJE_SALIDA)
                return
            accion = self._acciones.get(opcion)
            if accion is None:
                print(mensajes.MENSAJE_OPCION_INVALIDA)
                continue
            accion()

    def _registrar(self) -> None:
        print("\nEstado: registro de estudiante")
        try:
            datos = self._capturar_datos(incluir_codigo=True)
            if datos is None:
                print(mensajes.MENSAJE_CANCELADO)
                return
            estudiante = self._servicio.registrar_estudiante(
                codigo=str(datos["codigo"]),
                nombre_completo=str(datos["nombre_completo"]),
                edad=int(datos["edad"]),
                semestre=int(datos["semestre"]),
                correo=str(datos["correo"]),
                programa=str(datos["programa"]),
            )
            print("Estudiante registrado correctamente.")
            self._mostrar_estudiante(estudiante)
        except ErrorDominio as error:
            print(f"Error: {error}")

    def _listar(self) -> None:
        print("\nEstado: listado de estudiantes")
        estudiantes = self._servicio.listar_estudiantes()
        if not estudiantes:
            print(mensajes.MENSAJE_SIN_REGISTROS)
            return
        for estudiante in estudiantes:
            self._mostrar_estudiante(estudiante)

    def _buscar(self) -> None:
        print("\nEstado: busqueda de estudiante")
        codigo = self._pedir_texto(mensajes.PROMPT_CODIGO)
        if codigo is None:
            print(mensajes.MENSAJE_CANCELADO)
            return
        try:
            estudiante = self._servicio.buscar_estudiante(codigo)
            self._mostrar_estudiante(estudiante)
        except ErrorDominio as error:
            print(f"Error: {error}")

    def _actualizar(self) -> None:
        print("\nEstado: actualizacion de estudiante")
        codigo = self._pedir_texto(mensajes.PROMPT_CODIGO)
        if codigo is None:
            print(mensajes.MENSAJE_CANCELADO)
            return
        try:
            actual = self._servicio.buscar_estudiante(codigo)
            print("Datos actuales:")
            self._mostrar_estudiante(actual)
            datos = self._capturar_datos(incluir_codigo=False)
            if datos is None:
                print(mensajes.MENSAJE_CANCELADO)
                return
            datos["codigo"] = actual.codigo
            actualizado = self._servicio.actualizar_estudiante(
                codigo=str(datos["codigo"]),
                nombre_completo=str(datos["nombre_completo"]),
                edad=int(datos["edad"]),
                semestre=int(datos["semestre"]),
                correo=str(datos["correo"]),
                programa=str(datos["programa"]),
            )
            print("Estudiante actualizado correctamente.")
            self._mostrar_estudiante(actualizado)
        except ErrorDominio as error:
            print(f"Error: {error}")

    def _eliminar(self) -> None:
        print("\nEstado: eliminacion de estudiante")
        codigo = self._pedir_texto(mensajes.PROMPT_CODIGO)
        if codigo is None:
            print(mensajes.MENSAJE_CANCELADO)
            return
        confirmacion = input(mensajes.PROMPT_CONFIRMAR_ELIMINAR).strip()
        if confirmacion.upper() != "SI":
            print(mensajes.MENSAJE_CANCELADO)
            return
        try:
            self._servicio.eliminar_estudiante(codigo)
            print("Estudiante eliminado correctamente.")
        except ErrorDominio as error:
            print(f"Error: {error}")

    def _mostrar_ayuda(self) -> None:
        print(mensajes.AYUDA)

    def _capturar_datos(
        self,
        incluir_codigo: bool,
    ) -> dict[str, str | int] | None:
        datos: dict[str, str | int] = {}
        if incluir_codigo:
            codigo = self._pedir_texto(mensajes.PROMPT_CODIGO)
            if codigo is None:
                return None
            datos["codigo"] = codigo
        nombre = self._pedir_texto(mensajes.PROMPT_NOMBRE)
        if nombre is None:
            return None
        edad = self._pedir_entero(mensajes.PROMPT_EDAD)
        if edad is None:
            return None
        semestre = self._pedir_entero(mensajes.PROMPT_SEMESTRE)
        if semestre is None:
            return None
        correo = self._pedir_texto(mensajes.PROMPT_CORREO)
        if correo is None:
            return None
        programa = self._pedir_texto(mensajes.PROMPT_PROGRAMA)
        if programa is None:
            return None
        datos.update(
            {
                "nombre_completo": nombre,
                "edad": edad,
                "semestre": semestre,
                "correo": correo,
                "programa": programa,
            }
        )
        return datos

    def _pedir_texto(self, prompt: str) -> str | None:
        valor = input(prompt).strip()
        if valor.lower() == CANCELAR:
            return None
        return valor

    def _pedir_entero(self, prompt: str) -> int | None:
        while True:
            valor = self._pedir_texto(prompt)
            if valor is None:
                return None
            try:
                return int(valor)
            except ValueError:
                print(mensajes.MENSAJE_VALOR_NUMERICO)

    def _mostrar_estudiante(self, estudiante: Estudiante) -> None:
        print(
            " | ".join(
                [
                    f"Codigo: {estudiante.codigo}",
                    f"Nombre: {estudiante.nombre_completo}",
                    f"Edad: {estudiante.edad}",
                    f"Semestre: {estudiante.semestre}",
                    f"Correo: {estudiante.correo}",
                    f"Programa: {estudiante.programa}",
                ]
            )
        )
