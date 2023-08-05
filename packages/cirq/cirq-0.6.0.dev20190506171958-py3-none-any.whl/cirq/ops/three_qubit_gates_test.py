# Copyright 2018 The Cirq Developers
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import itertools
import numpy as np
import pytest

import cirq


@pytest.mark.parametrize('eigen_gate_type', [
    cirq.CCXPowGate,
    cirq.CCZPowGate,
    ]
)
def test_eigen_gates_consistent_protocols(eigen_gate_type):
    cirq.testing.assert_eigengate_implements_consistent_protocols(
            eigen_gate_type, ignoring_global_phase=True)


def test_consistent_protocols():
    cirq.testing.assert_implements_consistent_protocols(cirq.CSWAP)


def test_init():
    assert (cirq.CCZ**0.5).exponent == 0.5
    assert (cirq.CCZ**0.25).exponent == 0.25
    assert (cirq.CCX**0.5).exponent == 0.5
    assert (cirq.CCX**0.25).exponent == 0.25


def test_unitary():
    assert cirq.has_unitary(cirq.CCX)
    np.testing.assert_allclose(cirq.unitary(cirq.CCX), np.array([
        [1, 0, 0, 0, 0, 0, 0, 0],
        [0, 1, 0, 0, 0, 0, 0, 0],
        [0, 0, 1, 0, 0, 0, 0, 0],
        [0, 0, 0, 1, 0, 0, 0, 0],
        [0, 0, 0, 0, 1, 0, 0, 0],
        [0, 0, 0, 0, 0, 1, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 1],
        [0, 0, 0, 0, 0, 0, 1, 0],
    ]), atol=1e-8)

    assert cirq.has_unitary(cirq.CCX**0.5)
    np.testing.assert_allclose(cirq.unitary(cirq.CCX**0.5), np.array([
        [1, 0, 0, 0, 0, 0, 0, 0],
        [0, 1, 0, 0, 0, 0, 0, 0],
        [0, 0, 1, 0, 0, 0, 0, 0],
        [0, 0, 0, 1, 0, 0, 0, 0],
        [0, 0, 0, 0, 1, 0, 0, 0],
        [0, 0, 0, 0, 0, 1, 0, 0],
        [0, 0, 0, 0, 0, 0, 0.5 + 0.5j, 0.5 - 0.5j],
        [0, 0, 0, 0, 0, 0, 0.5 - 0.5j, 0.5 + 0.5j],
    ]), atol=1e-8)

    assert cirq.has_unitary(cirq.CCZ)
    np.testing.assert_allclose(cirq.unitary(cirq.CCZ),
                               np.diag([1, 1, 1, 1, 1, 1, 1, -1]),
                               atol=1e-8)

    assert cirq.has_unitary(cirq.CCZ**0.5)
    np.testing.assert_allclose(cirq.unitary(cirq.CCZ**0.5),
                               np.diag([1, 1, 1, 1, 1, 1, 1, 1j]),
                               atol=1e-8)

    assert cirq.has_unitary(cirq.CSWAP)
    np.testing.assert_allclose(cirq.unitary(cirq.CSWAP), np.array([
        [1, 0, 0, 0, 0, 0, 0, 0],
        [0, 1, 0, 0, 0, 0, 0, 0],
        [0, 0, 1, 0, 0, 0, 0, 0],
        [0, 0, 0, 1, 0, 0, 0, 0],
        [0, 0, 0, 0, 1, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 1, 0],
        [0, 0, 0, 0, 0, 1, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 1],
    ]), atol=1e-8)


def test_str():
    assert str(cirq.CCX) == 'TOFFOLI'
    assert str(cirq.TOFFOLI) == 'TOFFOLI'
    assert str(cirq.CSWAP) == 'FREDKIN'
    assert str(cirq.FREDKIN) == 'FREDKIN'
    assert str(cirq.CCZ) == 'CCZ'

    assert str(cirq.CCX**0.5) == 'TOFFOLI**0.5'
    assert str(cirq.CCZ**0.5) == 'CCZ**0.5'


def test_repr():
    assert repr(cirq.CCX) == 'cirq.TOFFOLI'
    assert repr(cirq.TOFFOLI) == 'cirq.TOFFOLI'
    assert repr(cirq.CSWAP) == 'cirq.FREDKIN'
    assert repr(cirq.FREDKIN) == 'cirq.FREDKIN'
    assert repr(cirq.CCZ) == 'cirq.CCZ'

    assert repr(cirq.CCX**0.5) == '(cirq.TOFFOLI**0.5)'
    assert repr(cirq.CCZ**0.5) == '(cirq.CCZ**0.5)'


def test_eq():
    a, b, c, d = cirq.LineQubit.range(4)
    eq = cirq.testing.EqualsTester()
    eq.add_equality_group(cirq.CCZ(a, b, c),
                          cirq.CCZ(a, c, b),
                          cirq.CCZ(b, c, a))
    eq.add_equality_group(cirq.CCZ(a, b, c)**0.5,
                          cirq.CCZ(a, c, b)**2.5,
                          cirq.CCZ(b, c, a)**-1.5)
    eq.add_equality_group(cirq.TOFFOLI(a, b, c)**0.5,
                          cirq.TOFFOLI(b, a, c)**2.5,
                          cirq.TOFFOLI(a, b, c)**-1.5)
    eq.add_equality_group(cirq.CCZ(a, b, d))
    eq.add_equality_group(cirq.TOFFOLI(a, b, c), cirq.CCX(a, b, c))
    eq.add_equality_group(cirq.TOFFOLI(a, c, b), cirq.TOFFOLI(c, a, b))
    eq.add_equality_group(cirq.TOFFOLI(a, b, d))
    eq.add_equality_group(cirq.CSWAP(a, b, c), cirq.FREDKIN(a, b, c))
    eq.add_equality_group(cirq.CSWAP(b, a, c), cirq.CSWAP(b, c, a))


@pytest.mark.parametrize('op,max_two_cost', [
    (cirq.CCZ(*cirq.LineQubit.range(3)), 8),
    (cirq.CCX(*cirq.LineQubit.range(3)), 8),
    (cirq.CCZ(cirq.LineQubit(0),
              cirq.LineQubit(2),
              cirq.LineQubit(1)), 8),
    (cirq.CSWAP(*cirq.LineQubit.range(3)), 9),
    (cirq.CSWAP(*reversed(cirq.LineQubit.range(3))), 9),
    (cirq.CSWAP(cirq.LineQubit(1),
                cirq.LineQubit(0),
                cirq.LineQubit(2)), 12),
])
def test_decomposition_cost(op: cirq.Operation, max_two_cost: int):
    ops = tuple(
        cirq.flatten_op_tree(cirq.google.ConvertToXmonGates().convert(op)))
    two_cost = len([e for e in ops if len(e.qubits) == 2])
    over_cost = len([e for e in ops if len(e.qubits) > 2])
    assert over_cost == 0
    assert two_cost == max_two_cost


@pytest.mark.parametrize('gate', [
    cirq.CCX, cirq.CSWAP, cirq.CCZ,
])
def test_decomposition_respects_locality(gate):
    a = cirq.GridQubit(0, 0)
    b = cirq.GridQubit(1, 0)
    c = cirq.GridQubit(0, 1)

    for x, y, z in itertools.permutations([a, b, c]):
        circuit = cirq.Circuit.from_ops(gate(x, y, z))
        cirq.google.ConvertToXmonGates().optimize_circuit(circuit)
        cirq.google.Foxtail.validate_circuit(circuit)


def test_diagram():
    a, b, c, d = cirq.LineQubit.range(4)
    circuit = cirq.Circuit.from_ops(
        cirq.TOFFOLI(a, b, c),
        cirq.TOFFOLI(a, b, c)**0.5,
        cirq.CCX(a, c, b),
        cirq.CCZ(a, d, b),
        cirq.CCZ(a, d, b)**0.5,
        cirq.CSWAP(a, c, d),
        cirq.FREDKIN(a, b, c)
    )
    cirq.testing.assert_has_diagram(circuit, """
0: ───@───@───────@───@───@───────@───@───
      │   │       │   │   │       │   │
1: ───@───@───────X───@───@───────┼───×───
      │   │       │   │   │       │   │
2: ───X───X^0.5───@───┼───┼───────×───×───
                      │   │       │
3: ───────────────────@───@^0.5───×───────
""")
    cirq.testing.assert_has_diagram(circuit, """
0: ---@---@-------@---@---@-------@------@------
      |   |       |   |   |       |      |
1: ---@---@-------X---@---@-------|------swap---
      |   |       |   |   |       |      |
2: ---X---X^0.5---@---|---|-------swap---swap---
                      |   |       |
3: -------------------@---@^0.5---swap----------
""", use_unicode_characters=False)
