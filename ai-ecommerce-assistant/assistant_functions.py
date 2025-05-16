import json
import os
# AI E-Commerce Assistant - ShopBot
# Author: Manuela Cortés Granados
# Since: 2025-05-16 1:34 AM GMT -5:00
# Description: Python app using OpenAI’s GPT-4o model to create a virtual e-commerce assistant
#              that can provide product information and check stock availability.

# ✅ SRP (Single Responsibility Principle): 
# This function has one clear responsibility — loading the product catalog from a JSON file.
def load_product_catalog():
    """
    📦 Loads the product catalog from a local JSON file.

    📍 Location: The file is expected to be in the same directory as this script.

    Returns:
        list[dict]: A list of product dictionaries containing keys such as:
            - id (int)
            - name (str)
            - description (str)
            - price (float)
            - stock (int)

    💥 Raises:
        FileNotFoundError: If the catalog file does not exist.
        json.JSONDecodeError: If the file content is not valid JSON.

    🧠 SOLID Principles:
        - SRP: Dedicated solely to file reading and JSON parsing.
        - OCP: You can extend this to read from APIs or databases later without modifying this function.
    """
    # 📁 Build absolute path to the product catalog file
    path = os.path.join(os.path.dirname(__file__), 'product_catalog.json')

    # 📖 Read the file content safely using UTF-8 encoding
    with open(path, 'r', encoding='utf-8') as file:
        catalog = json.load(file)

    # ✅ Return the parsed product list
    return catalog


# ✅ SRP: This function only handles product lookup.
# ✅ OCP: We can add filters (e.g., by category or price) without changing existing logic.
def get_product_info(product_name, catalog):
    """
    🔍 Fetches detailed information of a product by its name.

    Args:
        product_name (str): Name of the product to search (case-insensitive).
        catalog (list[dict]): The product catalog list.

    Returns:
        dict | None: A dictionary containing product info if found:
            - id (int)
            - name (str)
            - description (str)
            - price (float)
            - stock (int)
        Returns `None` if no product matches the name.

    Example:
        >>> get_product_info("EcoFriendly Water Bottle", catalog)

    🧠 SOLID Principles:
        - SRP: Responsible only for searching and returning a single product’s data.
        - OCP: You can easily add logging, metrics, or fallback behavior.
        - LSP: This function behaves correctly even if the catalog contains subclasses of dict.
    """
    # 🔁 Loop through all products in the catalog
    for product in catalog:
        # 🆚 Compare names case-insensitively for better UX
        if product["name"].lower() == product_name.lower():
            return {
                "id": product["id"],
                "name": product["name"],
                "description": product["description"],
                "price": product["price"],
                "stock": product["stock"],
            }

    # ❌ Product not found
    return None


# ✅ SRP: Verifies stock availability only.
# ✅ DIP: Depends on an abstract catalog input (list of dicts), not a specific data source.
def check_stock(product_name, catalog):
    """
    📦 Checks whether a product is currently in stock.

    Args:
        product_name (str): The product name to verify.
        catalog (list[dict]): The list of product dictionaries.

    Returns:
        bool: 
            - True ✅ if the product exists and has stock > 0.
            - False ❌ if product not found or stock is zero.

    Example:
        >>> check_stock("EcoFriendly Water Bottle", catalog)

    🧠 SOLID Principles:
        - SRP: Only evaluates stock levels — does not concern itself with fetching or displaying.
        - LSP: Works with any compatible product catalog data structure.
        - DIP: Accepts the catalog as an injected dependency, enabling flexibility in how data is provided.
    """
    # 🧾 Get the product details first
    product = get_product_info(product_name, catalog)

    # 📈 If product exists, check if its stock is positive
    if product:
        return product["stock"] > 0

    # 🛑 Product not found or out of stock
    return False
