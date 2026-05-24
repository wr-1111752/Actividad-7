"""Pruebas del repositorio JSON de estudiantes."""

import pytest

from app.exceptions import (
    EstudianteDuplicadoError,
    EstudianteNoEncontradoError,
)
from app.models.estudiante import Estudiante
from app.repositories.estudiante_json_repositorio import (
    EstudianteJsonRepositorio,
)


def test_crear_y_buscar_estudiante(
    repositorio_temporal: EstudianteJsonRepositorio,
    estudiante_valido: Estudiante,
) -> None:
    """Debe crear y recuperar un estudiante por codigo."""
    repositorio_temporal.crear(estudiante_valido)

    encontrado = repositorio_temporal.buscar_por_codigo("est001")

    assert encontrado == estudiante_valido


def test_crear_rechaza_codigo_duplicado(
    repositorio_temporal: EstudianteJsonRepositorio,
    estudiante_valido: Estudiante,
) -> None:
    """Debe impedir dos estudiantes con el mismo codigo."""
    repositorio_temporal.crear(estudiante_valido)

    with pytest.raises(EstudianteDuplicadoError):
        repositorio_temporal.crear(estudiante_valido)


def test_actualizar_estudiante(
    repositorio_temporal: EstudianteJsonRepositorio,
    estudiante_valido: Estudiante,
) -> None:
    """Debe reemplazar los datos de un estudiante existente."""
    repositorio_temporal.crear(estudiante_valido)
    estudiante_valido.nombre_completo = "Ana Lopez Gomez"

    repositorio_temporal.actualizar(estudiante_valido)

    actualizado = repositorio_temporal.buscar_por_codigo("EST001")
    assert actualizado.nombre_completo == "Ana Lopez Gomez"


def test_eliminar_estudiante(
    repositorio_temporal: EstudianteJsonRepositorio,
    estudiante_valido: Estudiante,
) -> None:
    """Debe eliminar un estudiante existente."""
    repositorio_temporal.crear(estudiante_valido)

    repositorio_temporal.eliminar("EST001")

    with pytest.raises(EstudianteNoEncontradoError):
        repositorio_temporal.buscar_por_codigo("EST001")
