"""Fixtures compartidas para pruebas."""

from datetime import datetime
from pathlib import Path

import pytest

from app.models.estudiante import Estudiante
from app.repositories.estudiante_json_repositorio import (
    EstudianteJsonRepositorio,
)


@pytest.fixture
def estudiante_valido() -> Estudiante:
    """Retorna un estudiante valido para pruebas."""
    return Estudiante(
        codigo="est001",
        nombre_completo="Ana Maria Lopez",
        edad=20,
        semestre=4,
        correo="ana.lopez@universidad.edu",
        programa="Ciencia de Datos",
        fecha_registro=datetime(2026, 5, 20, 10, 30),
    )


@pytest.fixture
def repositorio_temporal(tmp_path: Path) -> EstudianteJsonRepositorio:
    """Retorna un repositorio JSON aislado en un archivo temporal."""
    ruta = tmp_path / "estudiantes.json"
    return EstudianteJsonRepositorio(str(ruta))
