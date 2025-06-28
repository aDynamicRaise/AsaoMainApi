import json
import statistics
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse, ORJSONResponse
from .services import StatisticsService
from .schemas import PriceTrendRequest


router = APIRouter(tags=["statistics"])
stats_service = StatisticsService()
from .test_data.upload_data import main


# Для тестовых данных из файла
# @router.post("/upload_test_data")
# async def upload():
#     await main()


@router.get("/stats")
async def get_stats(prices):
    """Calculate basic statistics for a list of prices."""
    if not prices:
        raise ValueError("The list of prices cannot be empty.")

    mean_price = statistics.mean(prices)
    median_price = statistics.median(prices)
    stdev_price = statistics.stdev(prices) if len(prices) > 1 else 0.0

    return {
        "mean": mean_price,
        "median": median_price,
        "stdev": stdev_price
    }


@router.post("/price-trend")
async def get_price_trend(request: PriceTrendRequest = Depends()):
    try:
        return await stats_service.generate_interactive_price_chart(
            seller_id=request.seller_id,
            start_date=request.start_date,
            end_date=request.end_date,
            product_ids=request.product_ids
        )
    except ValueError as e:
        return {'status': 'error', 'message': str(e)}



@router.post("/interactive-chart", response_class=HTMLResponse)
async def show_interactive_chart(request: PriceTrendRequest = Depends()):
    result = await stats_service.generate_interactive_price_chart(
        seller_id=request.seller_id,
        start_date=request.start_date,
        end_date=request.end_date,
        product_ids=request.product_ids
    )
    
    if result['status'] == 'error':
        return HTMLResponse(f"<h1>Ошибка</h1><p>{result['message']}</p>")
    
    return HTMLResponse(f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Анализ цен</title>
        <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
        <style>
            body {{ font-family: Arial, sans-serif; margin: 20px; }}
            #chart {{ width: 100%; height: 70vh; }}
            .control-panel {{ margin: 20px 0; }}
            select {{ padding: 8px; font-size: 16px; min-width: 300px; }}
        </style>
    </head>
    <body>
        <h1>Анализ изменения цен</h1>
        
        <div class="control-panel">
            <label for="product-filter">Фильтр по товару:</label>
            <select id="product-filter">
                <option value="all">Все товары</option>
                {''.join(f'<option value="{product}">{product}</option>' for product in result['products'])}
            </select>
        </div>
        
        <div id="chart"></div>
        
        <script>
            // Инициализация графика
            const chartData = {json.dumps(result['data'])};
            const plot = Plotly.newPlot('chart', chartData.data, chartData.layout);
            
            // Функция фильтрации
            function filterProduct(productName) {{
                const traces = chartData.data;
                const visibility = [];
                
                traces.forEach(trace => {{
                    // trace.name выглядит как "Название товара (price_type)"
                    const traceProduct = trace.name.split(' (')[0];
                    visibility.push(productName === 'all' || traceProduct === productName);
                }});
                
                Plotly.restyle('chart', 'visible', visibility);
                
                // Обновляем заголовок
                const title = productName === 'all' 
                    ? 'Динамика цен всех товаров' 
                    : `Динамика цен: ${{productName}}`;
                
                Plotly.relayout('chart', 'title', title);
            }}
            
            // Обработчик выбора товара
            document.getElementById('product-filter').addEventListener('change', function() {{
                filterProduct(this.value);
            }});
        </script>
    </body>
    </html>
    """)