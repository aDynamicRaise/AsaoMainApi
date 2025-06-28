import base64
from typing import List
from fastapi import APIRouter, Depends, HTTPException, Request

import io
from fastapi.templating import Jinja2Templates
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from fastapi import FastAPI, Response
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from sklearn.linear_model import LinearRegression
from statsmodels.tsa.arima.model import ARIMA
from prophet import Prophet
import plotly.express as px
from datetime import datetime, timedelta




router = APIRouter(tags=["forecast"])

# Данные из БД: Замените generate_sample_data() на загрузку из вашей базы:

# import sqlite3
# conn = sqlite3.connect("prices.db")
# df = pd.read_sql("SELECT date, price FROM prices", conn)

# Параметры моделей: Настройте order=(p,d,q) в ARIMA или добавьте сезонность в Prophet



# --- Генерация тестовых данных ---
def generate_sample_data(days: int = 30):
    np.random.seed(42)
    dates = pd.date_range(start="2024-01-01", periods=days, freq="D")
    base_price = 100
    prices = [base_price + i * 2 + np.random.normal(0, 3) for i in range(days)]
    return pd.DataFrame({"date": dates, "price": prices})

df = generate_sample_data()

# --- Общие функции для прогноза ---
def plot_to_png():
    """Конвертирует текущий график matplotlib в PNG."""
    buf = io.BytesIO()
    plt.savefig(buf, format="png", dpi=100)
    buf.seek(0)
    plt.close()
    return buf

# --- Ручки API ---
@router.get("/linear")
async def linear_forecast(plot_type: str = "png"):
    """Линейная регрессия: /linear?plot_type=png|html"""
    df_ = df.copy()
    df_["days"] = (df_["date"] - df_["date"].iloc[0]).dt.days
    
    # Разделение на train/test
    train = df_.iloc[:20]
    test = df_.iloc[20:]
    
    # Обучение модели
    model = LinearRegression()
    model.fit(train[["days"]], train["price"])
    test["predicted"] = model.predict(test[["days"]])
    
    # Визуализация
    plt.figure(figsize=(12, 6))
    plt.plot(train["date"], train["price"], label="Исторические данные")
    plt.plot(test["date"], test["price"], label="Реальные значения (тест)")
    plt.plot(test["date"], test["predicted"], label="Прогноз (линейная регрессия)", linestyle="--")
    plt.title("Линейный прогноз цен")
    plt.legend()
    
    if plot_type == "png":
        buf = plot_to_png()
        return Response(content=buf.read(), media_type="image/png")
    else:
        # Plotly HTML
        fig = px.line(df_, x="date", y="price", title="Линейный прогноз")
        fig.add_scatter(x=test["date"], y=test["predicted"], name="Прогноз")
        return HTMLResponse(fig.to_html())



@router.get("/prophet")
async def prophet_forecast(plot_type: str = "png"):
    """Prophet: /prophet?plot_type=png|html"""
    df_ = df.rename(columns={"date": "ds", "price": "y"})
    train = df_.iloc[:20]
    
    # Обучение Prophet
    model = Prophet()
    model.fit(train)
    future = model.make_future_dataframe(periods=10)
    forecast = model.predict(future)
    
    # Визуализация
    if plot_type == "png":
        fig1 = model.plot(forecast)
        buf = io.BytesIO()
        fig1.savefig(buf, format="png")
        buf.seek(0)
        return Response(content=buf.read(), media_type="image/png")
    else:
        # Plotly HTML
        fig = px.line(forecast, x="ds", y="yhat", title="Прогноз Prophet")
        fig.add_scatter(x=df_["ds"], y=df_["y"], name="Исторические данные")
        return HTMLResponse(fig.to_html())



# Примеры запросов в web
# http://localhost:8000/linear?plot_type=png
# http://localhost:8000/linear?plot_type=html




class PriceData(BaseModel):
    dates: List[str]
    prices: List[float]

class ForecastResponse(BaseModel):
    forecast: List[float]
    plot: str

def create_test_data():
    dates = pd.date_range(start='2025-04-21', periods=14, freq='12H')
    prices = [89, 89, 92, 92, 95, 95, 92, 89, 89, 92, 95, 98, 98, 95]
    return dates, prices

def train_arima_model(data, order=(5, 1, 0)):
    model = ARIMA(data, order=order)
    model_fit = model.fit()
    return model_fit

def forecast_prices(model, steps):
    forecast = model.forecast(steps=steps)
    return forecast

def plot_results(dates, actual, forecast):
    plt.figure(figsize=(12, 6))
    plt.plot(dates, actual, label='Actual Prices')
    future_dates = pd.date_range(start=dates[-1], periods=len(forecast)+1, freq='12H')[1:]
    plt.plot(future_dates, forecast, label='Forecasted Prices', color='green')
    plt.title('Price Forecast')
    plt.xlabel('Date')
    plt.ylabel('Price')
    plt.legend()

    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    plt.close()

    return buf

@router.get("/plot_png")
async def get_plot():
    dates, prices = create_test_data()

    model = train_arima_model(prices)
    forecast_steps = 5
    forecast = forecast_prices(model, forecast_steps)

    image_stream = plot_results(dates, prices, forecast)

    return Response(content=image_stream.getvalue(), media_type="image/png")

















# @router.get("/arima")
# async def arima_forecast(plot_type: str = "png"):
#     """ARIMA: /arima?plot_type=png|html"""
#     df_ = df.set_index("date")
#     train = df_.iloc[:20]
#     test = df_.iloc[20:]
    
#     # Обучение ARIMA
#     model = ARIMA(train["price"], order=(1, 1, 1))
#     model_fit = model.fit()
#     test["predicted"] = model_fit.forecast(steps=len(test))
    
#     # Визуализация
#     plt.figure(figsize=(12, 6))
#     plt.plot(train.index, train["price"], label="Исторические данные")
#     plt.plot(test.index, test["price"], label="Реальные значения (тест)")
#     plt.plot(test.index, test["predicted"], label="Прогноз ARIMA", linestyle="--")
#     plt.title("Прогноз ARIMA")
#     plt.legend()
    
#     if plot_type == "png":
#         buf = plot_to_png()
#         return Response(content=buf.read(), media_type="image/png")
#     else:
#         # Plotly HTML
#         fig = px.line(df_, x=df_.index, y="price", title="Прогноз ARIMA")
#         fig.add_scatter(x=test.index, y=test["predicted"], name="Прогноз")
#         return HTMLResponse(fig.to_html())