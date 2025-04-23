# Problem 3: Tedarikçi Segmentasyonu Veritabanı tabloları: Suppliers, Products, OrderDetails
# Soru: “Tedarikçileri sağladıkları ürünlerin satış performansına göre gruplandırın. Az katkı sağlayan veya sıra dışı tedarikçileri bulun.”
# Özellik vektörleri: Tedarik ettiği ürün sayısı, Bu ürünlerin toplam satış miktarı, Ortalama satış fiyatı, Ortalama müşteri sayısı


import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import DBSCAN
from sklearn.neighbors import NearestNeighbors
from kneed import KneeLocator
from database import get_engine
import matplotlib.pyplot as plt


def get_supplier_data():
   
    engine = get_engine()

    query = """
    select
        s.supplier_id,
        s.company_name as supplier_name,
        count(distinct p.product_id) as supplied_product_count,
        sum(od.unit_price * od.quantity * (1 - od.discount)) as total_sales_amount,
        avg(od.unit_price * (1 - od.discount)) as average_selling_price,
        count(distinct o.customer_id) as unique_customer_count
    from suppliers s
    inner join products p on s.supplier_id = p.supplier_id
    inner join order_details od on p.product_id = od.product_id
    inner join orders o on od.order_id = o.order_id
    group by s.supplier_id, s.company_name
    """

    return pd.read_sql_query(query, engine)



def find_optimal_eps(X_scaled, min_samples=3):
    neighbors = NearestNeighbors(n_neighbors=min_samples).fit(X_scaled)
    distances, _ = neighbors.kneighbors(X_scaled)
    distances = np.sort(distances[:, min_samples - 1])
    kneedle = KneeLocator(range(len(distances)), distances, curve='convex', direction='increasing')
    return distances[kneedle.elbow]



def supplier_segmentation():
    df = get_supplier_data()
    X = df[["supplied_product_count", "total_sales_amount", "average_selling_price", "unique_customer_count"]]

    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    optimal_eps = find_optimal_eps(X_scaled)
    dbscan = DBSCAN(eps=optimal_eps, min_samples=3)
    df['cluster'] = dbscan.fit_predict(X_scaled)

    niche_suppliers = df[df['cluster'] == -1]
    return df, niche_suppliers



def plot_supplier_segmentation(df, filename="supplier_segmentation.png"):
    plt.figure(figsize=(10, 6))
    plt.scatter(
        df['supplied_product_count'],
        df['total_sales_amount'],
        c=df['cluster'],
        cmap='plasma',
        s=80,
        edgecolors='k'
    )
    plt.xlabel("Tedarik Edilen Ürün Sayısı")
    plt.ylabel("Toplam Satış Miktarı (₺)")
    plt.title("Tedarikçi Segmentasyonu (DBSCAN)")
    plt.grid(True)
    plt.colorbar(label='Küme No')
    plt.savefig(filename)
    plt.close()
