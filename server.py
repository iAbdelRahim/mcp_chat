from mcp.server.fastmcp import FastMCP
from dotenv import load_dotenv
from openai import OpenAI
from typing import List, Dict, Any

import httpx
import math
import os

# load environment variables
load_dotenv(dotenv_path=".env")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")


# set client
client = OpenAI(
    api_key = OPENAI_API_KEY
)

# instantiate an MCP server client
mcp = FastMCP("mcp-server")

# DEFINE TOOLS

# Tool to get all datasets from civ opendata
@mcp.tool()
def get_all_datasets() -> List[Dict[str, Any]]:
    """
    Récupère tous les jeux de données publics depuis le catalogue de data.gouv.ci,
    et retourne une liste de dictionnaires contenant toutes les informations disponibles.
    """
    url = "https://data.gouv.ci/data-fair/api/v1/catalog/datasets"
    response = httpx.get(url)
    response.raise_for_status()

    datasets = response.json().get("results", [])
    return datasets

# Include web search results for the completion
@mcp.tool()
def websearch_newssearch(prompt: str):
    """Fetches news articles based on a user's query.
    The prompt should be a question or statement that you want the news search to address,
    such as "What was a positive news story from today?".
    """
    completion = client.chat.completions.create(
        model="gpt-4o-search-preview",
        web_search_options={},
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
    )
    return completion.choices[0].message.content

#addition tool
@mcp.tool()
def add(a: int, b: int) -> int:
    """Add two numbers"""
    return int(a + b)

# subtraction tool
@mcp.tool()
def subtract(a: int, b: int) -> int:
    """Subtract two numbers"""
    return int(a - b)

# multiplication tool
@mcp.tool()
def multiply(a: int, b: int) -> int:
    """Multiply two numbers"""
    return int(a * b)

#  division tool
@mcp.tool() 
def divide(a: int, b: int) -> float:
    """Divide two numbers"""
    return float(a / b)

# power tool
@mcp.tool()
def power(a: int, b: int) -> int:
    """Power of two numbers"""
    return int(a ** b)

# square root tool
@mcp.tool()
def sqrt(a: int) -> float:
    """Square root of a number"""
    return float(a ** 0.5)

# cube root tool
@mcp.tool()
def cbrt(a: int) -> float:
    """Cube root of a number"""
    return float(a ** (1/3))

# factorial tool
@mcp.tool()
def factorial(a: int) -> int:
    """factorial of a number"""
    return int(math.factorial(a))

# log tool
@mcp.tool()
def log(a: int) -> float:
    """log of a number"""
    return float(math.log(a))

# remainder tool
@mcp.tool()
def remainder(a: int, b: int) -> int:
    """remainder of two numbers divison"""
    return int(a % b)

# sin tool
@mcp.tool()
def sin(a: int) -> float:
    """sin of a number"""
    return float(math.sin(a))

# cos tool
@mcp.tool()
def cos(a: int) -> float:
    """cos of a number"""
    return float(math.cos(a))

# tan tool
@mcp.tool()
def tan(a: int) -> float:
    """tan of a number"""
    return float(math.tan(a))

# DEFINE RESOURCES

# Add a dynamic greeting resource
@mcp.resource("greeting://{name}")
def get_greeting(name: str) -> str:
    """Get a personalized greeting"""
    return f"Hello, {name}!"
    
 
# execute and return the stdio output
if __name__ == "__main__":
    mcp.run(transport="streamable-http")

