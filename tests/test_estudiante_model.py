"""Pruebas de la entidad Estudiante."""

from datetime import datetime, timedelta

import pytest

from app.exceptions import DatoInvalidoError
from app.models.estudiante import Estudiante


def test_estudiante_normaliza_codigo_y_correo(
    estudiante_valido: Estudiante,
) -> None:
    """Debe normalizar codigo en mayusculas y correo en minusculas."""
    assert estudiante_valido.codigo == "EST001"
    assert estudiante_valido.correo == "ana.lopez@universidad.edu"


def test_estudiante_to_dict_y_from_dict_conservan_datos(
    estudiante_valido: Estudiante,
) -> None:
    """Debe serializar y deserializar sin perder informacion."""
    datos = estudiante_valido.to_dict()

    reconstruido = Estudiante.from_dict(datos)

    assert reconstruido == estudiante_valido


def test_estudiante_rechaza_correo_invalido() -> None:
    """Debe rechazar correos sin formato valido."""
    with pytest.raises(DatoInvalidoError):
        Estudiante(
            codigo="EST002",
            nombre_completo="Luis Perez",
            edad=19,
            semestre=2,
            correo="correo-invalido",
            programa="Psicologia",
            fecha_registro=datetime.now(),
        )


def test_estudiante_rechaza_fecha_futura() -> None:
    """Debe rechazar fechas de registro futuras."""
    with pytest.raises(DatoInvalidoError):
        Estudiante(
            codigo="EST003",
            nombre_completo="Marta Diaz",
            edad=22,
            semestre=6,
            correo="marta@universidad.edu",
            programa="Ingenieria",
            fecha_registro=datetime.now() + timedelta(days=1),
        )
