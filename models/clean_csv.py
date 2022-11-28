import numpy as np
import pandas as pd
import pymongo

client = pymongo.MongoClient(
    'mongodb+srv://DataLog:DataLog@cluster0.jzr1zc7.mongodb.net/')


def cleancsv(db: str, id_inventory: str, id_payment: str, year: str, month: str, day: str):
    url = 'https://drive.google.com/uc?id=' + id_inventory
    df = pd.read_csv(url)

    if 'Action' in df.columns:
        dummy = pd.get_dummies(df['Action'])
        df = df.merge(dummy, left_index=True, right_index=True)
        df.drop('Action', axis=1, inplace=True)

    if 'Cost' in df.columns:
        df.drop('Cost', axis=1, inplace=True)

    if 'SKU' in df.columns:
        df.drop('SKU', axis=1, inplace=True)

    if 'Invoice Number' in df.columns:
        df.drop('Invoice Number', axis=1, inplace=True)

    if 'PO Number' in df.columns:
        df.drop('PO Number', axis=1, inplace=True)

    if 'Transfer ID' in df.columns:
        df.drop('Transfer ID', axis=1, inplace=True)

    if 'Barcode' in df.columns:
        df.drop('Barcode', axis=1, inplace=True)

    if 'Unit' in df.columns:
        df.drop('Unit', axis=1, inplace=True)

    if 'Vendor' in df.columns:
        df.drop('Vendor', axis=1, inplace=True)

    if 'Inventory Qty' in df.columns:
        df.drop('Inventory Qty', axis=1, inplace=True)

    if 'Inv. Value After' in df.columns:
        df.drop('Inv. Value After', axis=1, inplace=True)

    if 'Inv. Value Before' in df.columns:
        df.drop('Inv. Value Before', axis=1, inplace=True)

    if 'Inv. Change Value' in df.columns:
        df.drop('Inv. Change Value', axis=1, inplace=True)

    if '%Quantity Change' in df.columns:
        df.drop('%Quantity Change', axis=1, inplace=True)

    if '%Value Change' in df.columns:
        df.drop('%Value Change', axis=1, inplace=True)

    if 'Cost After' in df.columns:
        df.drop('Cost After', axis=1, inplace=True)

    if 'Cost Before' in df.columns:
        df.drop('Cost Before', axis=1, inplace=True)

    if 'Quantity After' in df.columns:
        df.drop('Quantity After', axis=1, inplace=True)

    if 'Quantity Before' in df.columns:
        df.drop('Quantity Before', axis=1, inplace=True)

    if 'Product Class' in df.columns:
        df.drop('Product Class', axis=1, inplace=True)

    if df['Establishment'].str.contains('Organic Acres').any():
        df['Establishment'].values[:] = 0

    if df['Establishment'].str.contains('Cypress').any():
        df['Establishment'].values[:] = 1

    sales = df[df['Sales'].isin({1})].reset_index(drop=True)

    if 'Remarks' in sales.columns:
        sales.drop('Remarks', axis=1, inplace=True)

    if 'Wastage' in sales.columns:
        sales.drop('Wastage', axis=1, inplace=True)

    if 'Started' in sales.columns:
        sales.drop('Started', axis=1, inplace=True)

    if 'Return' in sales.columns:
        sales.drop('Return', axis=1, inplace=True)

    if 'Adjustment' in sales.columns:
        sales.drop('Adjustment', axis=1, inplace=True)

    if 'Sales' in sales.columns:
        sales.drop('Sales', axis=1, inplace=True)

    if 'Reset Cost' in sales.columns:
        sales.drop('Reset Cost', axis=1, inplace=True)

    if 'Received' in sales.columns:
        sales.drop('Received', axis=1, inplace=True)

    if 'Transfer In' in sales.columns:
        sales.drop('Transfer In', axis=1, inplace=True)

    if 'Transfer Out' in sales.columns:
        sales.drop('Transfer Out', axis=1, inplace=True)

    if 'Return to Vendor' in sales.columns:
        sales.drop('Return to Vendor', axis=1, inplace=True)

    # creating new columns for order ID and sales
    sales[['orderID', 'itemPrice']] = sales['Order Details'].str.split(
        pat=',', expand=True)

    # dropping order details column
    sales.drop('Order Details', axis=1, inplace=True)

    # removing specific string in a column
    sales['orderID'] = sales['orderID'].str.replace('order_id:', '')
    sales['itemPrice'] = sales['itemPrice'].str.replace('net_sales_price:', '')

    # renaming user column to employee
    sales.rename(columns={'User': 'Employee'}, inplace=True)

    # removing returns from sales
    sales = sales[~sales['orderID'].str.contains('returns_id:') == True]

    sales['ymd'] = pd.to_datetime(sales['Date/Time']).dt.date
    sales['ymd'] = pd.to_datetime(sales['ymd'], format='%Y-%m-%d')

    sales['Date'] = pd.to_datetime(sales['Date/Time']).dt.date
    sales['Time'] = pd.to_datetime(sales['Date/Time']).dt.time

    sales.drop('Date/Time', axis=1, inplace=True)

    # sales['Quantity'] = sales['Quantity'].round().astype(int)

    sales = sales.astype(
        {'orderID': int, 'itemPrice': float, 'Establishment': int})

    paymenturl = 'https://drive.google.com/uc?id=' + id_payment
    payment = pd.read_csv(paymenturl)

    if 'Transaction Status' in payment.columns:
        payment.drop('Transaction Status', axis=1, inplace=True)

    if 'Transaction Id' in payment.columns:
        payment.drop('Transaction Id', axis=1, inplace=True)

    if 'Last 4 CC Digits' in payment.columns:
        payment.drop('Last 4 CC Digits', axis=1, inplace=True)

    if 'Employee' in payment.columns:
        payment.drop('Employee', axis=1, inplace=True)

    if 'Raw Date' in payment.columns:
        payment.drop('Raw Date', axis=1, inplace=True)

    if 'Station' in payment.columns:
        payment.drop('Station', axis=1, inplace=True)

    if 'Rounding Delta' in payment.columns:
        payment.drop('Rounding Delta', axis=1, inplace=True)

    payment.rename(columns={'Order No': 'orderID'}, inplace=True)

    dummy = pd.get_dummies(payment['Card Type'])
    payment = payment.merge(dummy, left_index=True, right_index=True)

    dummy = pd.get_dummies(payment['Type'])
    payment = payment.merge(dummy, left_index=True, right_index=True)

    if 'Card Type' in payment.columns:
        payment.drop('Card Type', axis=1, inplace=True)

    if 'Type' in payment.columns:
        payment.drop('Type', axis=1, inplace=True)

    if 'Credit' in payment.columns:
        payment.drop('Credit', axis=1, inplace=True)

    if 'Adjustments' in payment.columns:
        payment.drop('Adjustments', axis=1, inplace=True)

    if 'Debit Card' in payment.columns:
        payment.drop('Debit Card', axis=1, inplace=True)

    if 'Other_x' in payment.columns:
        payment.drop('Other_x', axis=1, inplace=True)

    if 'Other_y' in payment.columns:
        payment.drop('Other_y', axis=1, inplace=True)

    if 'Customer Paid' in payment.columns:
        payment.drop('Customer Paid', axis=1, inplace=True)

    if 'Customer Change' in payment.columns:
        payment.drop('Customer Change', axis=1, inplace=True)

    payment['Date'] = pd.to_datetime(payment['Date'])

    payment['day'] = payment['Date'].dt.day
    payment['month'] = payment['Date'].dt.month
    payment['year'] = payment['Date'].dt.year
    payment['hour'] = payment['Date'].dt.hour

    payment['ymd'] = pd.to_datetime(payment[['year', 'month', 'day']])

    payment.drop('Date', axis=1, inplace=True)

    df_dailyRevenue = payment.groupby(
        ['ymd'])['Total'].sum().reset_index(name='dailyRevenue')

    payment['dailyRevenueByOrder'] = payment.groupby(['ymd'])['Total'].cumsum()

    payment = payment.merge(df_dailyRevenue, on='ymd', how='left')

    payment.drop('ymd', axis=1, inplace=True)

    df = sales.merge(payment, on='orderID', how='right')
    df = df.dropna()
    df = df.astype({'Establishment': int})

    base_url = "http://climate.weather.gc.ca/climate_data/bulk_data_e.html?"
    query_url = "format=csv&stationID={}&Year={}&Month={}&Day={}&timeframe=1".format('51442', year, month, day)
    api_endpoint = base_url + query_url
    df_temp = pd.read_csv(api_endpoint, skiprows=0)

    df_temp['Date'] = pd.to_datetime(df_temp['Date/Time (LST)']).dt.date

    df_temp['Date'] = df_temp['Date'].apply(lambda x: x.strftime('%Y-%m-%d'))

    df_temp.dropna()

    df_temp['Max_Temp_C_'] = df_temp['Temp (°C)'].max()
    df_temp['Min_Temp_C_'] = df_temp['Temp (°C)'].min()
    df_temp['Temperature'] = round(df_temp['Temp (°C)'].mean(), 2)

    df_temp = df_temp[['Date', 'Temperature', 'Min_Temp_C_', 'Max_Temp_C_']]

    df_temp = df_temp[df_temp['Date'].isin({'2022'+'-09-11'})].reset_index(drop=True)

    df_temp = df_temp.iloc[[0]]

    df['Date'] = df.Date.apply(lambda x: x.strftime('%Y-%m-%d'))
    df.drop("Time", axis=1, inplace=True)

    df = df.merge(df_temp, on='Date', how='left')

    if 'Gift Cards' not in df.columns:
        df['Gift Cards'] = 0

    if 'American Express' in df.columns:
        df.rename(columns={'American Express': 'Amex'}, inplace=True)
        df['Discover'] = 0
    elif 'Discover' in df.columns:
        df['Amex'] = 0
    else:
        df['Amex'] = 0
        df['Discover'] = 0

    df = df[['orderID', 'Establishment', 'Employee', 'Name', 'Category', 'Quantity', 'itemPrice', 'Total', 'Cash', 'Debit', 'Visa', 'Mastercard', 'Discover',
                'Amex', 'Gift Cards', 'hour', 'day', 'month', 'year', 'Date', 'dailyRevenueByOrder', 'dailyRevenue', 'Temperature', 'Min_Temp_C_', 'Max_Temp_C_']]

    df[['orderID', 'Establishment', 'Cash', 'Debit', 'Visa', 'Mastercard', 'Discover', 'Amex', 'Gift Cards', 'hour', 'day', 'month', 'year']] = df[[
            'orderID', 'Establishment', 'Cash', 'Debit', 'Visa', 'Mastercard', 'Discover', 'Amex', 'Gift Cards', 'hour', 'day', 'month', 'year']].astype(int)

    df.reset_index(inplace=True)
    df.drop("index", axis=1, inplace=True)

    steps_l = list(np.arange(0, len(df), 5000)) + [len(df)]

    for start, end in zip(steps_l, steps_l[1:]):
        client[db]['df_sales'].insert_many(
            df.iloc[start:end].to_dict(orient="records"))

    return df
