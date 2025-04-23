# müşterilerin alışveriş davranışlarına göre gruplanması ve aykırı verrilerin keşfi
# order_details, customers, orders


import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import DBSCAN
from sklearn.neighbors import NearestNeighbors
from kneed import KneeLocator
from database import get_engine
import matplotlib.pyplot as plt


def get_customer_data():
    
    engine = get_engine()

    query = """
    select c.customer_id, 
            count(o.order_id) as total_orders, 
            sum(od.quantity * od.unit_price) as total_spent,
            avg(od.quantity * od.unit_price)as avg_order_value
    from customers c 
    inner join orders o on c.customer_id = o.customer_id
    inner join order_details od on o.order_id = od.order_id
    group by c.customer_id 
    having count(o.order_id)>0
    """
    
    df = pd.read_sql_query(query, engine)
    return df

# Optimum eps değeri için Elbow Method
def find_optimal_eps(X_scaled, min_samples=3):
    neighbors = NearestNeighbors(n_neighbors=min_samples).fit(X_scaled)
    distances, _ = neighbors.kneighbors(X_scaled)
    
    distances = np.sort(distances)[:, min_samples-1]
    kneedle = KneeLocator(range(len(distances)), distances, curve='convex', direction='increasing')
    optimal_eps = distances[kneedle.elbow]
    
    return optimal_eps

# DBSCAN ile müşteri segmentasyonu
def customer_segmentation():
    df = get_customer_data()
    X = df[["total_orders", "total_spent", "avg_order_value"]]

    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    optimal_eps = find_optimal_eps(X_scaled)
    dbscan = DBSCAN(eps=optimal_eps, min_samples=3)

    df['cluster'] = dbscan.fit_predict(X_scaled)
    # Aykırı verileri tespit etme
    outliers = df[df["cluster"] == -1]
    return df, outliers


def plot_segmentation(df):
    plt.figure(figsize=(10, 6))
    plt.scatter(df['total_orders'], df['total_spent'], c=df['cluster'], cmap='plasma', s=60)
    plt.xlabel("Toplam Sipariş Sayısı")
    plt.ylabel("Toplam Harcama")
    plt.title("Müşteri Segmentasyonu (DBSCAN)")
    plt.grid(True)
    plt.colorbar(label='Küme No')
    
    plt.savefig("customer_segmentation.png")
    plt.close()
