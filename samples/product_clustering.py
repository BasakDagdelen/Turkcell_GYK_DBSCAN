# Problem 2: Ürün Kümeleme (Benzer Ürünler) Veritabanı tabloları: Products, OrderDetails 
# Soru:  “Benzer sipariş geçmişine sahip ürünleri DBSCAN ile gruplandırın. Az satılan ya da alışılmadık kombinasyonlarda geçen ürünleri belirleyin.” 
# Özellik vektörleri:  Ortalama satış fiyatı, Satış sıklığı, Sipariş başına ortalama miktar, Kaç farklı müşteriye satıldı 
# Amaç:  Benzer ürünlerin segmentasyonu,  -1 olan ürünler → belki özel ürünler veya niş ihtiyaçlar


import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import DBSCAN
from sklearn.neighbors import NearestNeighbors
from kneed import KneeLocator
from database import get_engine
import matplotlib.pyplot as plt


def get_product_data():
    
    engine = get_engine()

    query = """
    select
      p.product_id, 
      p.product_name,
      count(distinct od.order_id) as order_frequency,
      avg(od.unit_price * (1 - od.discount)) as average_sale_price,
      avg(od.quantity) as average_quantity_per_order,
      count(distinct o.customer_id) as unique_customer_count
    from products p
    inner join order_details od on p.product_id = od.product_id
    inner join orders o on o.order_id = od.order_id
    group by p.product_id, p.product_name
    """

    return pd.read_sql_query(query, engine)


def find_optimal_eps(X_scaled, min_samples=3):
    neighbors = NearestNeighbors(n_neighbors=min_samples).fit(X_scaled)
    distances, _ = neighbors.kneighbors(X_scaled)
    distances = np.sort(distances)[:, min_samples - 1]
    kneedle = KneeLocator(range(len(distances)), distances, curve='convex', direction='increasing')
    optimal_eps = distances[kneedle.elbow]
    return optimal_eps


def product_segmentation():
    df = get_product_data()
    X = df[["order_frequency", "average_sale_price", "average_quantity_per_order", "unique_customer_count"]]

    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    optimal_eps = find_optimal_eps(X_scaled)
    dbscan = DBSCAN(eps=optimal_eps, min_samples=3)

    df['cluster'] = dbscan.fit_predict(X_scaled)
    niche_products = df[df['cluster'] == -1]

    return df, niche_products


def plot_product_segmentation(df, filename="product_segmentation.png"):
    plt.figure(figsize=(10, 6))
    plt.scatter(
        df['order_frequency'],
        df['average_sale_price'],
        c=df['cluster'],
        cmap='viridis',
        s=80,
        edgecolors='k'
    )
    plt.xlabel("Sipariş Sıklığı")
    plt.ylabel("Ortalama Satış Fiyatı (₺)")
    plt.title("Ürün Segmentasyonu (DBSCAN)")
    plt.grid(True)
    plt.colorbar(label='Küme No')
    plt.savefig(filename)
    plt.close()
