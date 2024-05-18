import sqlite3
from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates


app = FastAPI()


# mount static and reference files
app.mount("/public/static", StaticFiles(directory="public/static"), name="static")
app.mount("/public/references", StaticFiles(directory="public/references"), name="references")

templates = Jinja2Templates(directory="public/templates")


@app.get("/", response_class=HTMLResponse)
async def root(request: Request):

    # queried data
    

    return templates.TemplateResponse(
        request=request, name="index.html"
    )


@app.post("/query_by_cif", status_code=200)
async def query_by_cif(request: Request, cif_no: str = Form(...)):
    # Query by CIF No

    ## connect to databast
    conn = sqlite3.connect("sqlite.db")

    # define cursor
    cursor = conn.cursor()

    query_script = f"""
    select * from test
    where cif_no = {cif_no}
    """
    cursor.execute(query_script)

    data = cursor.fetchall()
    name = data[0][1]

    cursor.close()
    conn.close()

    print(cif_no)
    print(data)


    return templates.TemplateResponse(
        request=request, name="index.html", context={"name": name}
    )
