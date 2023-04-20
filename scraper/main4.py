import sqlite3
import pandas as pd


# Функция для подсчета количества положительных продаж
def count_positive_sales(row, unique_dates):
    count = 0
    for idx, date in enumerate(unique_dates):
        if idx > 0:
            if row[f'diff_qty{unique_dates[idx - 1]}_{date}'] > 0:
                count += 1
    return count


# Устанавливаем соединение с базой данных
conn = sqlite3.connect('products.db')

# Загружаем данные из таблицы в DataFrame
df = pd.read_sql_query('SELECT category, name, brand, days_until_shipment, quantity, price, date FROM compel_data',
                       conn)

# Выбираем уникальные даты в данных
unique_dates = df['date'].unique()

# Создаем пустой DataFrame для результатов
result = None

# Переменная для предыдущей даты
prev_date = None

for date in unique_dates:
    # Фильтруем данные для текущей даты
    df_qty = df[df['date'] == date][['category', 'name', 'brand', 'days_until_shipment', 'quantity', 'price']]

    # Переименовываем столбцы с количеством товаров и ценами на определенную дату
    df_qty = df_qty.rename(columns={'quantity': f'qty{date}', 'price': f'price{date}'})

    # Объединяем текущий DataFrame с результатами
    if result is None:
        result = df_qty
    else:
        result = result.merge(df_qty, on=['category', 'name', 'brand', 'days_until_shipment'], how='outer')

    # Рассчитываем разницу в продажах между двумя датами
    if prev_date is not None:
        result[f'diff_qty{prev_date}_{date}'] = result[f'qty{prev_date}'] - result[f'qty{date}']

    # Обновляем предыдущую дату
    prev_date = date

# Заполняем пустые значения нулями
result = result.fillna(0)


# Добавляем датафрейм для аналитики
analytics_result = result.loc[:, ['category', 'name', 'brand', 'days_until_shipment']]
analytics_result = analytics_result.rename(columns={'category': 'Категория', 'name': 'Номер', 'brand': 'Бренд',
                                                    'days_until_shipment': 'Дней до отгрузки'})

# Добавляем новый столбец с количеством положительных продаж
analytics_result['Кол-во продаж'] = result.apply(lambda row: count_positive_sales(row, unique_dates), axis=1)


# Добавляем переменные для общего количества проданных штук и суммарной цены для каждого товара
total_qty_sales = result.filter(regex='diff_qty\d+').sum(axis=1)
mean_price = result.filter(regex='price\d+').mean(axis=1)

analytics_result['Продано шт.'] = total_qty_sales
analytics_result['Средняя цена'] = mean_price
analytics_result['Продано в руб.'] = total_qty_sales * mean_price


with pd.ExcelWriter('Result1.xlsx') as writer:
    analytics_result.to_excel(writer, index=False, sheet_name='Анализ')
    result.to_excel(writer, index=False, sheet_name='Данные')
