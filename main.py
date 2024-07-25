from fastapi import FastAPI, Request, Form
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
import json

app = FastAPI()
templates = Jinja2Templates(directory="template")  # Assumes templates are stored in a directory named "templates"

# Home page route
@app.get("/")
async def read_root(request: Request):
    try:
        with open('sample.json', 'r') as f:
            data = json.load(f)
    except FileNotFoundError:
        data = {}
    
    return templates.TemplateResponse("index.html", {"request": request, "todo": data})

# Add new TODO item route
@app.post("/add")
async def add_todo(request: Request, newtodo: str = Form(...)):
    try:
        with open('sample.json', 'r') as f:
            data = json.load(f)
    except FileNotFoundError:
        data = {}
    
    new_id = str(len(data) + 1)  # Generate new ID (simple increment)
    data[new_id] = newtodo  # Add new TODO item to dictionary

    with open('sample.json', 'w') as f:
        json.dump(data, f)

    return RedirectResponse("/", status_code=303)

# Delete TODO item route
@app.get("/delete/{id}")
async def delete_todo(request: Request, id: str):
    try:
        with open('sample.json', 'r') as f:
            data = json.load(f)
    except FileNotFoundError:
        data = {}
    
    if id in data:
        del data[id]  # Delete TODO item with specified ID
        with open('sample.json', 'w') as f:
            json.dump(data, f)

    return RedirectResponse("/", status_code=303)

# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run(app, host="127.0.0.1", port=8000)


# async def root(request: Request):
#     with open('sample.json') as f:
#         data = json.load(f)
#     return templates.TemplateResponse("index.html",{"request":request,"todo":data})