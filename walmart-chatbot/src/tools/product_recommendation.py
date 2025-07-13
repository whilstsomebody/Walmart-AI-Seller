import sqlite3
from pydantic import Field
from .base_tool import BaseTool
from litellm import completion
from langsmith import traceable

@traceable(run_type="tool", name="GetProductRecommendation")
def get_product_recommendation(product_category, user_query):
    """
    Retrieves products from the database based on a user query by leveraging an AI agent to generate search queries.

    Args:
        product_category (str): The query from the user to search for products.
        user_query (str): The user requiremenets query.

    Returns:
        list: A list of JSON objects representing the products that match the query.
    """

    # Connect to SQLite database
    conn = sqlite3.connect("./database.db")
    cursor = conn.cursor()

    products = [
        (
            "model",
            "processor",
            "memory",
            "storage",
            "display",
            "graphics",
            "cooling",
            "dpi",
            "type",
            "capacity",
            "read_speed",
            "write_speed",
            "display_type",
            "resolution",
            "refresh_rate",
            "size",
            "connectivity",
            "stripe_price_id",
            "price",
        )
    ]
    query = f"SELECT * FROM products WHERE category = '{product_category}'"
    try:
        cursor.execute(query)
        rows = cursor.fetchall()
        for row in rows:
            products.append(row)
    except Exception as e:
        print(f"An error occurred: {e}")

    # Close the database connection
    conn.close()

    # Define the prompt for the AI agent
    prompt = """
You are a Walmart Sales Assistant specializing in computer equipment and electronics. 
Engage the customer in a friendly, professional, and natural manner, just like a real Walmart seller. 
Recommend products based on the user's needs and preferences, using the provided requirements and available products in our store.

- Adapt your speaking style to match the customer's personality and context.
- If appropriate, suggest bundles, deals, or negotiate on price.
- Handle multiple topics if the user asks about features, pricing, availability, or comparisons.
- Your answer must list all products that are a good fit, with clear, concise descriptions and prices.
- Respond as if you are speaking directly to the customer, not as a technical expert.

Example:
Based on your needs, here are our best options:
1. **Product A**: Brief description, key features, and price.
2. **Product B**: Brief description, key features, and price.
If you want a bundle, a deal, or have other preferences, let me know!
"""

    message = f"""
    USER QUERY: {user_query}
    PRODUCTS: {products}
    """

    messages = [
        {"role": "system", "content": prompt},
        {"role": "user", "content": message},
    ]

    # Request to the AI agent to generate the SQL query
    response = completion(
        model="groq/mixtral-8x7b-32768", messages=messages, temperature=0.1
    )

    # Extract the SQL queries from the response
    output = response.choices[0].message.content

    return output


class GetProductRecommendation(BaseTool):
    """
    A tool that retrieves products from the database based on a user query by leveraging an AI agent to generate search queries.
    """

    product_category: str = Field(description="Product category")
    user_query: str = Field(description="User query")

    def run(self):
        return get_product_recommendation(self.product_category, self.user_query)
