from datetime import datetime
import json
from statistics import mean, median, stdev, StatisticsError
from typing import List, Optional
import pandas as pd
import plotly.graph_objects as go
from io import BytesIO
from sqlalchemy import select, and_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError
from database import Product, ProductData
from database import get_async_session
from sqlalchemy.orm import selectinload
from plotly.utils import PlotlyJSONEncoder
import plotly.express as px



class StatisticsService:
    async def get_price_history(
        self,
        seller_id: int,
        start_date: datetime,
        end_date: datetime,
        product_ids: Optional[List[int]] = None
    ) -> List[ProductData]:
        """Асинхронно получает историю цен для товаров продавца"""
        async with get_async_session() as session:
            try:
                query = select(ProductData).options(
                selectinload(ProductData.product)  # Явно загружаем связанный продукт
            ).join(Product).where(
                    and_(
                        Product.seller_id == seller_id,
                        ProductData.date_receipt >= start_date,
                        ProductData.date_receipt <= end_date
                    )
                )
                
                if product_ids:
                    query = query.where(Product.id.in_(product_ids))
                    
                result = await session.execute(query)
                return result.scalars().all()
            except SQLAlchemyError as e:
                await session.rollback()
                raise e
            
        
    def calculate_statistics(self, prices):
        """Calculate basic statistics for a list of prices."""
        # if not prices:
            # raise ValueError("The list of prices cannot be empty.")

        if not prices:
            return None

        stats = {}
        try:
            stats["mean"] = mean(prices)
        except StatisticsError:
            stats["mean"] = None

        try:
            stats["median"] = median(prices)
        except StatisticsError:
            stats["median"] = None

        try:
            stats["stdev"] = stdev(prices) if len(prices) > 1 else 0.0
        except StatisticsError:
            stats["stdev"] = None

        return stats
            


    async def generate_interactive_price_chart(
            self,
            seller_id: int,
            start_date: datetime,
            end_date: datetime,
            product_ids: Optional[List[int]] = None
        ) -> dict:
            """Генерирует данные для графика с группировкой по товарам"""
            data = await self.get_price_history(seller_id, start_date, end_date, product_ids)
            
            if not data:
                return {'status': 'error', 'message': 'Данные не найдены', 'data': None}

            # Структура для хранения данных
            products_data = {}
            all_dates = set()
            products_statistics = {}
            
            for item in data:
                date_str = item.date_receipt.strftime("%Y-%m-%d %H:%M:%S")
                all_dates.add(date_str)
                product_name = item.product.name
                
                if product_name not in products_data:
                    products_data[product_name] = {
                        'dates': [], 'base': [], 'discount': [], 'ozon_card': []
                    }
                    products_statistics[product_name] = {
                    'base': [],
                    'discount': [],
                    'ozon_card': []
                }
                
                # Добавляем только валидные цены
                products_data[product_name]['dates'].append(date_str)
                products_data[product_name]['base'].append(
                    float(item.base_price) if item.base_price and item.base_price > 0 else None
                )
                products_data[product_name]['discount'].append(
                    float(item.discount_price) if item.discount_price and item.discount_price > 0 else None
                )
                products_data[product_name]['ozon_card'].append(
                    float(item.ozon_card_price) if item.ozon_card_price and item.ozon_card_price > 0 else None
                )
            
                # Собираем цены для статистики каждого продукта
                if item.base_price and item.base_price > 0:
                    products_statistics[product_name]['base'].append(float(item.base_price))
                if item.discount_price and item.discount_price > 0:
                    products_statistics[product_name]['discount'].append(float(item.discount_price))
                if item.ozon_card_price and item.ozon_card_price > 0:
                    products_statistics[product_name]['ozon_card'].append(float(item.ozon_card_price))

            # Сортируем даты и получаем список товаров
            sorted_dates = sorted(all_dates)
            product_names = list(products_data.keys())
            
            # Создаем фигуру
            fig = go.Figure()
            colors = px.colors.qualitative.Plotly
            
            # Добавляем все товары (изначально все видимы)
            for i, (product_name, data) in enumerate(products_data.items()):
                color = colors[i % len(colors)]
                
                for price_type in ['base', 'discount', 'ozon_card']:
                    fig.add_trace(
                        go.Scatter(
                            x=data['dates'],
                            y=data[price_type],
                            name=f"{product_name} ({price_type})",
                            line=dict(
                                color=color,
                                width=3 if price_type == 'base' else 1.5,
                                dash='solid' if price_type == 'base' else 'dash' if price_type == 'ozon_card' else 'dot'
                            ),
                            visible=True,  # Все данные изначально видимы
                            hovertemplate=(
                                "<b>%{text}</b><br>"
                                "Дата: %{x}<br>"
                                "Цена: %{y:.2f} руб<extra></extra>"
                            ),
                            text=[product_name + " (" + price_type + ")"] * len(data['dates'])
                        )
                    )
            
            # Настройки layout
            fig.update_layout(
                title='Динамика цен товаров',
                xaxis_title='Дата',
                yaxis_title='Цена (руб)',
                hovermode='x unified',
                legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
            )

            # Рассчитываем статистику для каждого продукта
            products_stats = {}
            for product_name, stats_data in products_statistics.items():
                products_stats[product_name] = {
                    'base': self.calculate_statistics(stats_data['base']),
                    'discount': self.calculate_statistics(stats_data['discount']),
                    'ozon_card': self.calculate_statistics(stats_data['ozon_card'])
            }
            
            return {
                'status': 'success',
                'data': json.loads(json.dumps(fig.to_dict(), default=str)),
                'products': product_names,
                'dates': sorted_dates,
                'statistics': products_stats
            }        
    