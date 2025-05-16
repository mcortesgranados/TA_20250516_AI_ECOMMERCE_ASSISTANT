import json
import os
from openai import OpenAI
from assistant_functions import load_product_catalog, get_product_info, check_stock

# AI E-Commerce Assistant - ShopBot
# Author: Manuela Cortés Granados
# Since: 2025-05-16 1:34 AM GMT -5:00

# 🧠 S: Single Responsibility Principle
# This list defines the available functions that the assistant can call
# Each dictionary here represents a *declarative* schema of a callable function
# The assistant uses this to understand what capabilities it has access to
functions = [
    {
        "name": "get_product_info",
        "description": "Returns details of a product by name.",
        "parameters": {
            "type": "object",
            "properties": {
                "product_name": {
                    "type": "string",
                    "description": "Name of the product to retrieve details for",
                },
            },
            "required": ["product_name"],
        },
    },
    {
        "name": "check_stock",
        "description": "Checks if the product is in stock.",
        "parameters": {
            "type": "object",
            "properties": {
                "product_name": {
                    "type": "string",
                    "description": "Name of the product to check stock for",
                },
            },
            "required": ["product_name"],
        },
    },
]

def main():
    """
    🧠 Main entry point for the assistant app.
    
    📌 Responsibilities:
    - Load product data
    - Accept user input
    - Use OpenAI function calling to interpret and respond
    - Handle dynamic calls to business logic functions (SRP)
    """
    
    # 🔐 Set your API key before running (env-based for security)
    # For Windows (PowerShell): setx OPENAI_API_KEY "your_key"
    # For macOS/Linux: export OPENAI_API_KEY="your_key"
    client = OpenAI()

    # 📦 Load the product catalog from local storage
    catalog = load_product_catalog()

    print("¡Bienvenido al asistente de e-commerce! Escribe 'salir' para terminar.\n")

    # 🧠 System prompt helps define assistant behavior
    messages = [
        {
            "role": "system",
            "content": (
                "Eres ShopBot, un asistente virtual para una tienda online. "
                "Ayudas a los usuarios a obtener información y disponibilidad de productos."
            ),
        }
    ]

    while True:
        user_input = input("Usuario: ")
        if user_input.lower() in ["salir", "exit", "quit"]:
            print("Asistente: ¡Gracias por usar el asistente! Hasta luego.")
            break

        # Add user message to conversation context
        messages.append({"role": "user", "content": user_input})

        # 🎯 First call: Let OpenAI decide whether a function call is needed
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=messages,
            functions=functions,
            function_call="auto",
        )

        message = response.choices[0].message

        # 🧩 O: Open/Closed Principle
        # We can extend with more functions without modifying main logic
        if hasattr(message, "function_call") and message.function_call is not None:
            function_name = message.function_call.name
            arguments_json = message.function_call.arguments

            try:
                arguments = json.loads(arguments_json)
            except Exception:
                arguments = {}

            # 🧱 L: Liskov Substitution — consistent output for each function
            # 📌 Dynamically handle supported function calls
            if function_name == "get_product_info":
                product_name = arguments.get("product_name", "")
                product = get_product_info(product_name, catalog)
                if product:
                    function_response = (
                        f"🛍️ Product: {product['name']}\n"
                        f"📄 Description: {product['description']}\n"
                        f"💲 Price: ${product['price']:.2f}\n"
                        f"📦 Stock: {product['stock']} units"
                    )
                else:
                    function_response = f"❌ No product found with name '{product_name}'."

            elif function_name == "check_stock":
                product_name = arguments.get("product_name", "")
                in_stock = check_stock(product_name, catalog)
                if in_stock:
                    function_response = f"✅ '{product_name}' is available in stock."
                else:
                    function_response = f"⚠️ '{product_name}' is currently out of stock."

            else:
                function_response = "❓ Unknown function requested."

            # Add the assistant function result to message history
            messages.append({
                "role": "function",
                "name": function_name,
                "content": function_response,
            })

            # 🗣️ Second call: Assistant reads the function output and responds naturally
            second_response = client.chat.completions.create(
                model="gpt-4o",
                messages=messages,
            )
            assistant_reply = second_response.choices[0].message.content
            print("Asistente:", assistant_reply)

            # Store assistant message in history
            messages.append({"role": "assistant", "content": assistant_reply})

        else:
            # 🤖 If no function was called, use the direct model response
            assistant_reply = message.content
            print("Asistente:", assistant_reply)
            messages.append({"role": "assistant", "content": assistant_reply})

# ✅ D: Dependency Inversion Principle
# main() is the high-level module and relies on abstractions, not direct implementations
if __name__ == "__main__":
    main()
