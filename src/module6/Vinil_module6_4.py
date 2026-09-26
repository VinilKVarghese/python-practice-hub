
import ast
import operator

from langchain.agents import create_agent
from langchain.tools import tool
from langchain_ollama import ChatOllama


# -----------------------------------
# 1. CALCULATOR OPERATIONS
# -----------------------------------

# Allow only safe mathematical operations
OPERATORS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.Pow: operator.pow,
    ast.USub: operator.neg,
    ast.UAdd: operator.pos,
}


def calculate_expression(expression):
    """Safely evaluate basic arithmetic expressions."""

    def evaluate(node):
        # Numbers
        if isinstance(node, ast.Constant):
            if isinstance(node.value, (int, float)):
                return node.value
            raise ValueError("Only numbers are allowed.")

        # Arithmetic operations
        if isinstance(node, ast.BinOp):
            operation = OPERATORS.get(type(node.op))

            if operation is None:
                raise ValueError("Unsupported operation.")

            left = evaluate(node.left)
            right = evaluate(node.right)

            return operation(left, right)

        # Negative and positive numbers
        if isinstance(node, ast.UnaryOp):
            operation = OPERATORS.get(type(node.op))

            if operation is None:
                raise ValueError("Unsupported operation.")

            return operation(evaluate(node.operand))

        raise ValueError("Invalid mathematical expression.")

    tree = ast.parse(expression, mode="eval")

    return evaluate(tree.body)


# -----------------------------------
# 2. CREATE LANGCHAIN TOOL
# -----------------------------------

@tool
def calculator(expression: str) -> str:
    """Calculate a mathematical expression.

    Supports addition (+), subtraction (-),
    multiplication (*), division (/), and powers (**).

    Example: 25 * 16
    """

    try:
        result = calculate_expression(expression)
        return str(result)

    except Exception as error:
        return f"Calculation error: {error}"


# -----------------------------------
# 3. CREATE THE LLM
# -----------------------------------

llm = ChatOllama(
    model="qwen2.5:7b",
    temperature=0
)


# -----------------------------------
# 4. CREATE THE AGENT
# -----------------------------------

agent = create_agent(
    model=llm,
    tools=[calculator],
    system_prompt="""
You are a helpful math assistant.

Rules:
- Use the calculator tool for arithmetic calculations.
- Pass a valid arithmetic expression to the calculator.
- Explain the result clearly.
- Do not invent calculation results.
- If the question is not a mathematical calculation,
  respond politely.
"""
)


# -----------------------------------
# 5. GET USER INPUT
# -----------------------------------

def get_math_answer(question):
    """Send the user's question to the agent."""

    result = agent.invoke({
        "messages": [
            {"role": "user", "content": question}
        ]
    })

    # Get the final assistant response
    return result["messages"][-1].content


# -----------------------------------
# 6. RUN THE PROGRAM
# -----------------------------------

def main():
    print("=== LangChain Math Agent ===")

    question = input("Enter your math question: ")

    try:
        answer = get_math_answer(question)

        print("\nAgent Answer:")
        print(answer)

    except Exception as error:
        print(f"Error: {error}")


if __name__ == "__main__":
    main()