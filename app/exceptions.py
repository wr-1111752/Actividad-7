"""Excepciones de dominio para la aplicacion."""


class ErrorDominio(Exception):
    """Clase base para los errores propios del dominio."""


class EstudianteNoEncontradoError(ErrorDominio):
    """Error lanzado cuando no existe un estudiante solicitado."""

    def __init__(self, codigo: str) -> None:
        super().__init__(
            f"No se encontro un estudiante con codigo '{codigo}'."
        )


class EstudianteDuplicadoError(ErrorDominio):
    """Error lanzado cuando se intenta registrar un codigo repetido."""

    def __init__(self, codigo: str) -> None:
        super().__init__(
            f"Ya existe un estudiante registrado con codigo '{codigo}'."
        )


class DatoInvalidoError(ErrorDominio):
    """Error lanzado cuando un dato no cumple las reglas del dominio."""

    def __init__(self, mensaje: str) -> None:
        super().__init__(mensaje)
