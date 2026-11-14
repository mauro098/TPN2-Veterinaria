from estructuras.arbol_bst import ArbolBST
from servicios.busqueda import buscar_por_codigo


def comparar_busqueda_codigo(codigo: int, lista_pacientes: list, arbol_bst: ArbolBST) -> dict:
    codigo_str = f"{codigo:03d}"

    paciente_lista, comparaciones_lista = buscar_por_codigo(lista_pacientes, codigo_str)
    paciente_bst, comparaciones_bst = arbol_bst.buscar(codigo_str)

    busqueda_lista = {
        "paciente": paciente_lista,
        "comparaciones": comparaciones_lista,
        "metodo": "busqueda lineal en lista",
    }
    busqueda_bst = {
        "paciente": paciente_bst,
        "comparaciones": comparaciones_bst,
        "metodo": "busqueda en arbol BST",
    }

    ahorro = comparaciones_lista - comparaciones_bst
    porcentaje = (
        (ahorro / comparaciones_lista) * 100 if comparaciones_lista > 0 else 0.0
    )

    return {
        "busqueda_lista": busqueda_lista,
        "busqueda_bst": busqueda_bst,
        "ahorro_comparaciones": ahorro,
        "porcentaje_eficiencia": porcentaje,
    }


def generar_reporte_consola(reporte: dict) -> str:
    lista = reporte["busqueda_lista"]
    bst = reporte["busqueda_bst"]

    paciente_lista = lista["paciente"] if lista["paciente"] is not None else "No encontrado"
    paciente_bst = bst["paciente"] if bst["paciente"] is not None else "No encontrado"

    lineas = []
    lineas.append("REPORTE DE COMPARACION DE BUSQUEDA")
    lineas.append("==================================")
    lineas.append("")
    lineas.append("Busqueda en lista lineal:")
    lineas.append(f"  Paciente: {str(paciente_lista)}")
    lineas.append(f"  Comparaciones: {str(lista['comparaciones'])}")
    lineas.append(f"  Metodo: {lista['metodo']}")
    lineas.append("")
    lineas.append("Busqueda en arbol BST:")
    lineas.append(f"  Paciente: {str(paciente_bst)}")
    lineas.append(f"  Comparaciones: {str(bst['comparaciones'])}")
    lineas.append(f"  Metodo: {bst['metodo']}")
    lineas.append("")
    lineas.append(f"Ahorro de comparaciones: {str(reporte['ahorro_comparaciones'])}")
    lineas.append(f"Porcentaje de eficiencia: {reporte['porcentaje_eficiencia']:.1f}%")

    return "\n".join(lineas)
