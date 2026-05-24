"""Ejecuta operaciones CRUD de ejemplo para la entidad Estudiante."""

from __future__ import annotations

import json
from pathlib import Path
import sys
from typing import Any

RAIZ_PROYECTO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RAIZ_PROYECTO))

from app.repositories.estudiante_json_repositorio import (  # noqa: E402
    EstudianteJsonRepositorio,
)
from app.services.estudiante_servicio import EstudianteServicio  # noqa: E402
from app.utils.constantes_negocio import RUTA_ESTUDIANTES_JSON  # noqa: E402

RUTA_RESULTADOS = Path("data/resultados_crud_estudiantes.json")


def guardar_resultados(resultados: dict[str, Any]) -> None:
    """Guarda el resumen de operaciones CRUD en un archivo JSON.

    Args:
        resultados: datos generados durante la ejecucion del CRUD.
    """
    RUTA_RESULTADOS.parent.mkdir(parents=True, exist_ok=True)
    with RUTA_RESULTADOS.open("w", encoding="utf-8") as archivo:
        json.dump(resultados, archivo, indent=2, ensure_ascii=False)


def ejecutar_crud() -> dict[str, Any]:
    """Ejecuta crear, leer, actualizar y eliminar estudiantes.

    Returns:
        Resumen JSON-compatible de las operaciones realizadas.
    """
    ruta_estudiantes = Path(RUTA_ESTUDIANTES_JSON)
    ruta_estudiantes.parent.mkdir(parents=True, exist_ok=True)
    ruta_estudiantes.write_text("[]", encoding="utf-8")

    servicio = EstudianteServicio(EstudianteJsonRepositorio())

    ana = servicio.registrar_estudiante(
        codigo="est001",
        nombre_completo="Ana Maria Lopez",
        edad=20,
        semestre=4,
        correo="ana.lopez@universidad.edu",
        programa="Ciencia de Datos",
    )
    carlos = servicio.registrar_estudiante(
        codigo="est002",
        nombre_completo="Carlos Andres Ruiz",
        edad=22,
        semestre=6,
        correo="carlos.ruiz@universidad.edu",
        programa="Psicologia",
    )
    laura = servicio.registrar_estudiante(
        codigo="est003",
        nombre_completo="Laura Sofia Gomez",
        edad=19,
        semestre=2,
        correo="laura.gomez@universidad.edu",
        programa="Trabajo Social",
    )

    listado_inicial = servicio.listar_estudiantes()
    estudiante_consultado = servicio.buscar_estudiante("EST002")
    estudiante_actualizado = servicio.actualizar_estudiante(
        codigo="EST002",
        nombre_completo="Carlos Andres Ruiz Martinez",
        edad=23,
        semestre=7,
        correo="carlos.ruiz.m@universidad.edu",
        programa="Psicologia",
    )
    servicio.eliminar_estudiante("EST003")
    listado_final = servicio.listar_estudiantes()

    return {
        "crear": [
            ana.to_dict(),
            carlos.to_dict(),
            laura.to_dict(),
        ],
        "leer": {
            "listado_inicial": [
                estudiante.to_dict()
                for estudiante in listado_inicial
            ],
            "busqueda_por_codigo": estudiante_consultado.to_dict(),
        },
        "actualizar": estudiante_actualizado.to_dict(),
        "eliminar": {
            "codigo_eliminado": "EST003",
            "mensaje": "Estudiante eliminado correctamente.",
        },
        "estado_final": [
            estudiante.to_dict()
            for estudiante in listado_final
        ],
    }


def main() -> None:
    """Ejecuta el flujo CRUD y guarda el resultado."""
    resultados = ejecutar_crud()
    guardar_resultados(resultados)
    print("CRUD ejecutado correctamente.")
    print(f"Estado final: {RUTA_ESTUDIANTES_JSON}")
    print(f"Resumen de operaciones: {RUTA_RESULTADOS}")


if __name__ == "__main__":
    main()
