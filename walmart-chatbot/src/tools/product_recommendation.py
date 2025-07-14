import sqlite3
from pydantic import Field
from .base_tool import BaseTool
from litellm import completion
from langsmith import traceable

@traceable(run_type="tool", name="GetProductRecommendation")
async def get_product_recommendation(product_category, user_query):
    """
    Retrieves products from the database based on a user query by leveraging an AI agent to generate search queries.

    Args:
        product_category (str): The query from the user to search for products.
        user_query (str): The user requirements query.

    Returns:
        list: A list of JSON objects representing the products that match the query.
    """

    # Connect to SQLite database
    conn = sqlite3.connect("./database.db")
    cursor = conn.cursor()

    columns = [
        "model", "processor", "memory", "storage", "display", "graphics",
        "cooling", "dpi", "type", "capacity", "read_speed", "write_speed",
        "display_type", "resolution", "refresh_rate", "size", "connectivity",
        "stripe_price_id", "price", "category"
    ]

    query = f"SELECT * FROM products WHERE category = ?"
    try:
        cursor.execute(query, (product_category,))
        rows = cursor.fetchall()
        
        if not rows:
            return "No products found in that category."

        # Convert rows to list of dicts for easier processing
        products = [dict(zip(columns, row)) for row in rows]

        # Use LLM to find the best matching products based on user query
        prompt = f"""
        User Query: {user_query}
        Available Products: {str(products)}
        
        Based on the user's requirements, recommend the best matching products.
        Format your response in a clear, concise way focusing on the most relevant features.
        """
        
        response = await completion(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}]
        )
        
        return response.choices[0].message.content
        
    except Exception as e:
        return f"Error retrieving products: {str(e)}"
    finally:
        cursor.close()
        conn.close()

class GetProductRecommendation(BaseTool):
    """Tool for getting product recommendations."""
    
    product_category: str = Field(..., description="The category of products to search for")
    user_query: str = Field(..., description="The user's requirements and preferences")

    @traceable(run_type="tool", name="GetProductRecommendation")
    async def run(self):
        """
        Retrieves products from the database based on a user query.
        """
        return await get_product_recommendation(self.product_category, self.user_query)