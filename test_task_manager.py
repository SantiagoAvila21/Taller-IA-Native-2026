import pytest

import task_manager_ai_native as tm


@pytest.fixture(autouse=True)
def clean_tasks():
    tm.tasks.clear()
    yield
    tm.tasks.clear()


def test_crear_tarea():
    task = tm.add_task("  Comprar leche  ", "ana")

    assert task["title"] == "Comprar leche"
    assert task["user"] == "ana"
    assert task["completed"] is False
    assert tm.tasks == [task]


def test_crear_tarea_titulo_vacio():
    with pytest.raises(tm.TaskError):
        tm.add_task("   ", "ana")

    assert tm.tasks == []


def test_crear_tarea_titulo_no_texto():
    with pytest.raises(tm.TaskError):
        tm.add_task(None, "ana")


def test_crear_tarea_titulo_demasiado_largo():
    with pytest.raises(tm.TaskError):
        tm.add_task("x" * (tm.MAX_TITLE_LENGTH + 1), "ana")


def test_crear_tarea_usuario_inexistente():
    with pytest.raises(tm.TaskError):
        tm.add_task("Tarea", "pepe")


def test_listar_solo_tareas_propias():
    tm.add_task("A", "ana")
    tm.add_task("B", "jorge")
    tm.add_task("C", "ana")

    assert [t["title"] for t in tm.list_tasks("ana")] == ["A", "C"]
    assert [t["title"] for t in tm.list_tasks("jorge")] == ["B"]
    assert tm.list_tasks("jojo") == []


def test_listar_usuario_inexistente():
    with pytest.raises(tm.TaskError):
        tm.list_tasks("pepe")


def test_completar_tarea():
    tm.add_task("A", "ana")

    assert tm.complete_task(0, "ana") == "Tarea completada"
    assert tm.list_tasks("ana")[0]["completed"] is True


def test_completar_indice_invalido():
    tm.add_task("A", "ana")

    with pytest.raises(tm.TaskError):
        tm.complete_task(5, "ana")


def test_completar_indice_no_entero():
    with pytest.raises(tm.TaskError):
        tm.complete_task("0", "ana")


def test_completar_indice_negativo():
    tm.add_task("A", "ana")

    with pytest.raises(tm.TaskError):
        tm.complete_task(-1, "ana")


def test_no_completar_tarea_de_otro_usuario():
    tm.add_task("A", "ana")

    # Jorge no tiene tareas: el indice 0 no debe apuntar a la de ana.
    with pytest.raises(tm.TaskError):
        tm.complete_task(0, "jorge")

    assert tm.list_tasks("ana")[0]["completed"] is False


def test_eliminar_tarea():
    tm.add_task("A", "ana")
    tm.add_task("B", "ana")

    assert tm.delete_task(0, "ana") == "Tarea eliminada"
    assert [t["title"] for t in tm.list_tasks("ana")] == ["B"]
    assert len(tm.tasks) == 1


def test_eliminar_no_afecta_otros_usuarios():
    tm.add_task("A", "ana")
    tm.add_task("B", "jorge")

    tm.delete_task(0, "ana")

    assert [t["title"] for t in tm.list_tasks("jorge")] == ["B"]
    assert len(tm.tasks) == 1


def test_eliminar_indice_invalido():
    with pytest.raises(tm.TaskError):
        tm.delete_task(0, "ana")


def test_eliminar_tarea_de_otro_usuario():
    tm.add_task("A", "ana")

    with pytest.raises(tm.TaskError):
        tm.delete_task(0, "jorge")

    assert len(tm.tasks) == 1
