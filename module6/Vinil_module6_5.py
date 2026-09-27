from langchain.agents import create_agent
from langchain.tools import tool
from langchain_ollama import ChatOllama


# ---------------------------------------------------------
# 1. Create the Qwen model
# ---------------------------------------------------------

qwen_model = ChatOllama(
    model="qwen2.5:1.5b",
    temperature=0
)


# ---------------------------------------------------------
# 2. Create the calculator tool
# ---------------------------------------------------------

@tool
def calculator(expression: str) -> str:
    """
    Performs mathematical calculations.
    """

    try:
        result = eval(expression)
        return str(result)

    except Exception as error:
        return f"Error: {error}"


# ---------------------------------------------------------
# 3. Create the Math Agent
# ---------------------------------------------------------

math_agent = create_agent(
    model=qwen_model,
    tools=[calculator],
    system_prompt="""
    You are a Math Agent.

    Your job is to solve mathematical problems accurately.

    Use the calculator tool whenever a calculation is required.

    Show the calculation clearly and provide the final answer.
    """
)


# ---------------------------------------------------------
# 4. Function to run the Math Agent
# ---------------------------------------------------------

def run_math_agent(question):
    """
    Sends the question to the Math Agent
    and returns the result.
    """

    response = math_agent.invoke(
        {
            "messages": [
                {
                    "role": "user",
                    "content": question
                }
            ]
        }
    )

    return response["messages"][-1].content


# ---------------------------------------------------------
# 5. Create the Reflection Agent
# ---------------------------------------------------------

reflection_agent = create_agent(
    model=qwen_model,
    tools=[],
    system_prompt="""
    You are a Reflection Agent.

    You receive a mathematical question and the answer
    produced by the Math Agent.

    Check the answer carefully.

    Your job is to:
    1. Check the calculation.
    2. Check the reasoning.
    3. Identify any errors.
    4. Correct the answer if necessary.
    5. Confirm the answer if it is correct.

    Give the final verified answer clearly.
    """
)


# ---------------------------------------------------------
# 6. Function to run the Reflection Agent
# ---------------------------------------------------------

def run_reflection_agent(question, math_answer):
    """
    Sends the question and Math Agent output
    to the Reflection Agent.
    """

    prompt = f"""
    Original question:
    {question}

    Math Agent's answer:
    {math_answer}

    Check this answer and provide the final verified answer.
    """

    response = reflection_agent.invoke(
        {
            "messages": [
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        }
    )

    return response["messages"][-1].content


# ---------------------------------------------------------
# 7. Get input from the user
# ---------------------------------------------------------

question = input("Enter a mathematical question: ")


# ---------------------------------------------------------
# 8. Run the Math Agent
# ---------------------------------------------------------

math_answer = run_math_agent(question)

print("\n--- Math Agent Output ---")
print(math_answer)


# ---------------------------------------------------------
# 9. Send output to the Reflection Agent
# ---------------------------------------------------------

final_answer = run_reflection_agent(
    question,
    math_answer
)


# ---------------------------------------------------------
# 10. Display the final answer
# ---------------------------------------------------------

print("\n--- Reflection Agent Output ---")
print(final_answer)