from typing import NamedTuple, Optional


class Receita(NamedTuple):
    id: Optional[int]
    cliente: str
    oficina: str
    motor_cabecote: str
    placa: str
    data: str


class Tarefa(NamedTuple):
    id: int
    nome: str


class TarefaReceita(NamedTuple):
    id: int
    nome: str
    quantidade: int
    valor: float
    observacoes: str
