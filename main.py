from turtle import color
from fastapi import FastAPI, Request, Form, File, UploadFile
import uvicorn
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import os
import io
import base64
import pandas as pd
import requests
import numpy as np
from bs4 import BeautifulSoup
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

app = FastAPI()

app.mount('/static', StaticFiles(directory='static'), name='static')

templates = Jinja2Templates(directory='templates')

def quad_eq(a, b, c):

    d = b**2 - 4 * a * c # discriminant

    if d < 0:
        return []
    elif d == 0:
        x = (-b + np.sqrt(d)) / (2 * a)
        if (x).is_integer():
            return [int(x)]
        return [x]
    else:
        x1 = (-b + np.sqrt(d)) / (2 * a)
        x2 = (-b - np.sqrt(d)) / (2 * a)
        if (x1).is_integer() and (x2).is_integer():
            return[int(x1), int(x2)]
        return [x1, x2]

@app.get("/")
async def root(request: Request, message='Quadratic Equations Calculator'):
    return templates.TemplateResponse('index.html', {'request': request, 'message': message})

@app.post("/plot")
async def show_plot(request: Request, 
                    a: int=Form(...),
                    b: int=Form(...),
                    c: int=Form(...)):

    if a == 0:
        return "Input correct quadratic equation"

    try:

        x=np. linspace(min(quad_eq(a, b, c)) - 10, max(quad_eq(a, b, c)) +10, 100)
        y = a*(x**2) + b*x + c
        roots = quad_eq(a, b, c)

        fig = plt.figure()

        plt.plot(x, y)
        plt.plot(roots, np.zeros(len(roots)), marker="o")
        plt.hlines(y=0, xmin=min(x), xmax=max(x), linestyles='dashed', colors='m')
        plt.vlines(x=0, ymin=min(y), ymax=max(y), linestyles='dashed', colors='m')
        plt.xlabel("x")
        plt.ylabel("y")

        pngImage = io.BytesIO()
        fig.savefig(pngImage)
        pngImageB64String = base64.b64encode(pngImage.getvalue()).decode('ascii')
        return templates.TemplateResponse("plot.html", 
                                   {"request": request, 
                                   "picture": pngImageB64String, 
                                   "a": a, 
                                   "b": b,
                                   "c": c,
                                   "roots": roots})
    except:
        return "This equation does not have roots"

@app.get("/solve")
async def solve(request: Request, a: int, b: int, c: int):
    if a == 0:
        return "Input correct quadratic equation"
    return  {"roots": quad_eq(a, b, c)} 

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)