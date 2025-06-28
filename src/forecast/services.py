import pandas as pd
import matplotlib.pyplot as plt
from statsmodels.tsa.arima.model import ARIMA
from sklearn.metrics import mean_squared_error
from math import sqrt

# Создание тестовых данных
def create_test_data():
    dates = pd.date_range(start='2025-04-21', end='2025-04-27', freq='12H')
    prices = [89, 89, 92, 92, 95, 95, 92, 89, 89, 92, 95, 98, 98, 95]
    data = pd.DataFrame({'date': dates, 'price': prices})
    data.set_index('date', inplace=True)
    return data

# Подготовка данных
def prepare_data(data):
    return data['price'].dropna()

# Обучение модели ARIMA
def train_arima_model(data, order=(5, 1, 0)):
    model = ARIMA(data, order=order)
    model_fit = model.fit()
    return model_fit

# Прогнозирование цен
def forecast_prices(model, steps):
    forecast = model.forecast(steps=steps)
    return forecast

# Оценка модели
def evaluate_model(actual, predicted):
    rmse = sqrt(mean_squared_error(actual, predicted))
    return rmse

# Визуализация данных
def plot_results(actual, predicted, forecast):
    plt.figure(figsize=(12, 6))
    plt.plot(actual, label='Actual Prices')
    plt.plot(predicted, label='Predicted Prices', color='orange')
    plt.plot(range(len(actual), len(actual) + len(forecast)), forecast, label='Forecasted Prices', color='green')
    plt.title('Price Forecast')
    plt.xlabel('Date')
    plt.ylabel('Price')
    plt.legend()
    plt.show()

# Основная функция
def main():
    # Создание тестовых данных
    data = create_test_data()

    # Подготовка данных
    prices = prepare_data(data)

    # Разделение данных на обучающую и тестовую выборки
    train_size = int(len(prices) * 0.8)
    train, test = prices[:train_size], prices[train_size:]

    # Обучение модели ARIMA
    model = train_arima_model(train)

    # Прогнозирование на тестовой выборке
    predicted = model.predict(start=len(train), end=len(train)+len(test)-1, typ='levels')

    # Оценка модели
    rmse = evaluate_model(test, predicted)
    print(f'RMSE: {rmse}')

    # Прогнозирование на будущие периоды
    forecast_steps = 5  # Прогнозирование на 5 периодов вперед
    forecast = forecast_prices(model, forecast_steps)

    # Визуализация результатов
    plot_results(prices, predicted, forecast)

if __name__ == "__main__":
    main()