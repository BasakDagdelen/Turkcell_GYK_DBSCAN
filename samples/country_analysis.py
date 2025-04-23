# Problem 4: Ülkelere Göre Satış Deseni Analizi Veritabanı tabloları: Customers, Orders, OrderDetails
# Soru: “Farklı ülkelerden gelen siparişleri DBSCAN ile kümeleyin. Sıra dışı sipariş alışkanlığı olan ülkeleri tespit edin.”
# Özellikler: Toplam sipariş, Ortalama sipariş tutarı, Sipariş başına ürün sayısı


import pandas as pd
from database import get_engine
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import DBSCAN

def get_country_data():
  
    engine = get_engine()
  
    query = """
    select 
        c.country,
        sum(od.unit_price * od.quantity * (1 - od.discount)) as total_order_amount,
        avg(od.unit_price * od.quantity * (1 - od.discount)) as avg_order_amount,
        sum(od.quantity)/count(distinct o.order_id) as products_per_order
    from customers c
    inner join orders o on c.customer_id = o.customer_id
    inner join order_details od on o.order_id = od.order_id
    group by c.country
    """
    
    df = pd.read_sql_query(query, engine)
    return df


def country_segmentation(df):
    features = df[['total_order_amount', 'avg_order_amount', 'products_per_order']]
    scaler = StandardScaler()
    scaled_features = scaler.fit_transform(features)
    
    dbscan = DBSCAN(eps=0.5, min_samples=3)
    clusters = dbscan.fit_predict(scaled_features)
    
    df['cluster'] = clusters
    outliers = df[df['cluster'] == -1]        
    return outliers[['country']], df


def plot_country_segmentation(df, filename="country_segmentation.png"):
    normal = df[df['cluster'] != -1]
    outliers = df[df['cluster'] == -1]

    plt.figure(figsize=(10, 6))
    plt.scatter(normal['total_order_amount'], normal['avg_order_amount'],
                c=normal['cluster'], cmap='tab10', label='Normal')
    plt.scatter(outliers['total_order_amount'], outliers['avg_order_amount'],
                c='red', label='Outlier')
    plt.xlabel('Toplam Sipariş Tutarı')
    plt.ylabel('Ortalama Sipariş Tutarı')
    plt.title('Ülkelere Göre Satış Deseni (DBSCAN)')
    plt.legend()
    plt.grid(True)
    plt.savefig(filename)
    plt.close()
