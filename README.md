# try_fastmcp

This project is a Python application that uses the `FastMCP` library to create an MCP server. It also uses the `openai` library to interact with the OpenAI API.

## Prerequisites

- Python 3.6 or higher
- An OpenAI API key

## Installation

1. Clone the repository:

   ```bash
   git clone <repository_url>
   cd try_fastmcp
   ```

2. Create a virtual environment:

   ```bash
   python -m venv env
   ```

3. Activate the virtual environment:

   ```bash
   env\Scripts\activate
   ```

4. Install the dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Set the OpenAI API key:

   rename `.env.example` file to `.env` and fill your `OPENAI_API_KEY`


## Usage

To run the MCP server, execute the following command:

```bash
python server.py
```
To run the MCP client, execute the following command:

```bash
streamlit run client.py
```

## Description

This MCP server provides the following tools:

- `get_all_datasets`: Retrieves all public datasets from the data.gouv.ci catalog.
- `websearch_newssearch`: Fetches news articles based on a user's query.
- `add`: Adds two numbers.
- `subtract`: Subtracts two numbers.
- `multiply`: Multiplies two numbers.
- `divide`: Divides two numbers.
- `power`: Calculates the power of two numbers.
- `sqrt`: Calculates the square root of a number.
- `cbrt`: Calculates the cube root of a number.
- `factorial`: Calculates the factorial of a number.
- `log`: Calculates the logarithm of a number.
- `remainder`: Calculates the remainder of two numbers division.
- `sin`: Calculates the sine of a number.
- `cos`: Calculates the cosine of a number.
- `tan`: Calculates the tangent of a number.

It also provides the following resource:

- `greeting://{name}`: Get a personalized greeting.
