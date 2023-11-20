import typing
from ast import *

from ..util import CompilingNodeTransformer

"""
Rewrites all occurences of assignments to tuples to assignments to single values
"""


class RewriteTupleAssign(CompilingNodeTransformer):
    step = "Rewriting tuple deconstruction in assignments"

    unique_id = 0

    def visit_Assign(self, node: Assign) -> typing.List[stmt]:
        if not isinstance(node.targets[0], Tuple):
            return [node]
        uid = self.unique_id
        self.unique_id += 1
        assignments = [Assign([Name(f"{uid}_tup", Store())], self.visit(node.value))]
        assignments.extend(
            Assign(
                [t],
                Subscript(
                    value=Name(f"{uid}_tup", Load()),
                    slice=Index(value=Constant(i)),
                    ctx=Load(),
                ),
            )
            for i, t in enumerate(node.targets[0].elts)
        )
        return sum((self.visit(a) for a in assignments), [])
