"""Entidad de dominio Estudiante."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
import re
from typing import Any

from app.exceptions import DatoInvalidoError
from app.utils.constantes_negocio import (
    EDAD_MAXIMA_ESTUDIANTE,
    EDAD_MINIMA_ESTUDIANTE,
    SEMESTRE_MAXIMO,
    SEMESTRE_MINIMO,
)

PATRON_CORREO = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


@dataclass
class Estudiante:
    """Representa a un estudiante del programa de apoyo psicologico.

    Args:
        codigo: codigo institucional unico.
        nombre_completo: nombres y apellidos del estudiante.
        edad: edad actual del estudiante.
        semestre: semestre academico cursado.
        correo: correo institucional o personal valido.
        programa: programa academico al que pertenece.
        fecha_registro: fecha de creacion del registro.
    """

    codigo: str
    nombre_completo: str
    edad: int
    semestre: int
    correo: str
    programa: str
    fecha_registro: datetime

    def __post_init__(self) -> None:
        self.codigo = self.codigo.strip().upper()
        self.nombre_completo = self.nombre_completo.strip()
        self.correo = self.correo.strip().lower()
        self.programa = self.programa.strip()
        self._validar()

    def _validar(self) -> None:
        if not self.codigo:
            raise DatoInvalidoError("El codigo no puede estar vacio.")
        if not self.nombre_completo:
            raise DatoInvalidoError(
                "El nombre completo no puede estar vacio."
            )
        if not EDAD_MINIMA_ESTUDIANTE <= self.edad <= EDAD_MAXIMA_ESTUDIANTE:
            raise DatoInvalidoError(
                "La edad debe estar entre "
                f"{EDAD_MINIMA_ESTUDIANTE} y {EDAD_MAXIMA_ESTUDIANTE}."
            )
        if not SEMESTRE_MINIMO <= self.semestre <= SEMESTRE_MAXIMO:
            raise DatoInvalidoError(
                "El semestre debe estar entre "
                f"{SEMESTRE_MINIMO} y {SEMESTRE_MAXIMO}."
            )
        if not PATRON_CORREO.match(self.correo):
            raise DatoInvalidoError("El correo ingresado no es valido.")
        if not self.programa:
            raise DatoInvalidoError("El programa no puede estar vacio.")
        if not isinstance(self.fecha_registro, datetime):
            raise DatoInvalidoError(
                "La fecha de registro debe ser un datetime."
            )
        if self.fecha_registro > datetime.now():
            raise DatoInvalidoError(
                "La fecha de registro no puede ser futura."
            )

    def to_dict(self) -> dict[str, Any]:
        """Serializa el estudiante a un diccionario JSON-compatible.

        Returns:
            Diccionario con todos los datos del estudiante.
        """
        return {
            "codigo": self.codigo,
            "nombre_completo": self.nombre_completo,
            "edad": self.edad,
            "semestre": self.semestre,
            "correo": self.correo,
            "programa": self.programa,
            "fecha_registro": self.fecha_registro.isoformat(),
        }

    @classmethod
    def from_dict(cls, datos: dict[str, Any]) -> Estudiante:
        """Crea un estudiante desde un diccionario.

        Args:
            datos: datos previamente serializados del estudiante.

        Returns:
            Instancia validada de Estudiante.
        """
        return cls(
            codigo=datos["codigo"],
            nombre_completo=datos["nombre_completo"],
            edad=int(datos["edad"]),
            semestre=int(datos["semestre"]),
            correo=datos["correo"],
            programa=datos["programa"],
            fecha_registro=datetime.fromisoformat(datos["fecha_registro"]),
        )
