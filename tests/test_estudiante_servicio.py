"""Pruebas del servicio de estudiantes."""

import pytest

from app.exceptions import EstudianteNoEncontradoError
from app.repositories.estudiante_json_repositorio import (
    EstudianteJsonRepositorio,
)
from app.services.estudiante_servicio import EstudianteServicio


def test_registrar_estudiante(
    repositorio_temporal: EstudianteJsonRepositorio,
) -> None:
    """Debe registrar un estudiante desde datos primitivos."""
    servicio = EstudianteServicio(repositorio_temporal)

    estudiante = servicio.registrar_estudiante(
        codigo="est010",
        nombre_completo="Carlos Ruiz",
        edad=21,
        semestre=5,
        correo="carlos@universidad.edu",
        programa="Ciencia de Datos",
    )

    assert estudiante.codigo == "EST010"
    assert len(servicio.listar_estudiantes()) == 1


def test_listar_estudiantes_ordenados_por_nombre(
    repositorio_temporal: EstudianteJsonRepositorio,
) -> None:
    """Debe listar estudiantes en orden alfabetico por nombre."""
    servicio = EstudianteServicio(repositorio_temporal)
    servicio.registrar_estudiante(
        "EST2",
        "Zoraida Cano",
        24,
        8,
        "zoraida@universidad.edu",
        "Psicologia",
    )
    servicio.registrar_estudiante(
        "EST1",
        "Andrea Mora",
        18,
        1,
        "andrea@universidad.edu",
        "Ciencia de Datos",
    )

    nombres = [
        estudiante.nombre_completo
        for estudiante in servicio.listar_estudiantes()
    ]

    assert nombres == ["Andrea Mora", "Zoraida Cano"]


def test_actualizar_estudiante(
    repositorio_temporal: EstudianteJsonRepositorio,
) -> None:
    """Debe actualizar los datos editables de un estudiante."""
    servicio = EstudianteServicio(repositorio_temporal)
    servicio.registrar_estudiante(
        "EST5",
        "Nombre Inicial",
        20,
        3,
        "inicial@universidad.edu",
        "Administracion",
    )

    actualizado = servicio.actualizar_estudiante(
        "est5",
        "Nombre Actualizado",
        21,
        4,
        "actualizado@universidad.edu",
        "Ciencia de Datos",
    )

    assert actualizado.nombre_completo == "Nombre Actualizado"
    assert actualizado.semestre == 4


def test_eliminar_estudiante(
    repositorio_temporal: EstudianteJsonRepositorio,
) -> None:
    """Debe eliminar un estudiante registrado."""
    servicio = EstudianteServicio(repositorio_temporal)
    servicio.registrar_estudiante(
        "EST9",
        "Estudiante Temporal",
        19,
        2,
        "temporal@universidad.edu",
        "Psicologia",
    )

    servicio.eliminar_estudiante("est9")

    with pytest.raises(EstudianteNoEncontradoError):
        servicio.buscar_estudiante("EST9")
