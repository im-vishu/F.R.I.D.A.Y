import ast
import operator


_ALLOWED_OPERATORS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.FloorDiv: operator.floordiv,
    ast.Mod: operator.mod,
    ast.Pow: operator.pow,
    ast.USub: operator.neg,
}


def _eval_node(node):
    if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
        return node.value

    if isinstance(node, ast.BinOp) and type(node.op) in _ALLOWED_OPERATORS:
        left = _eval_node(node.left)
        right = _eval_node(node.right)
        return _ALLOWED_OPERATORS[type(node.op)](left, right)

    if isinstance(node, ast.UnaryOp) and type(node.op) in _ALLOWED_OPERATORS:
        operand = _eval_node(node.operand)
        return _ALLOWED_OPERATORS[type(node.op)](operand)

    raise ValueError("Unsupported or unsafe expression")


def run_calculator(input_data: dict):
    expression = input_data.get("expression")

    if not expression:
        return {
            "success": False,
            "error": "expression is required",
        }

    try:
        tree = ast.parse(expression, mode="eval")
        result = _eval_node(tree.body)

        return {
            "success": True,
            "expression": expression,
            "result": result,
        }
    except Exception as error:
        return {
            "success": False,
            "expression": expression,
            "error": str(error),
        }