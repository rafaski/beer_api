from fastapi import FastAPI

description = """
## Beer API ##
"""

app = FastAPI(
    title="Beer API",
    description=description
)
