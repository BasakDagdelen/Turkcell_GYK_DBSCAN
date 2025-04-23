from fastapi import FastAPI
from samples.country_analysis import country_segmentation, plot_country_segmentation
from samples.customer_segmentation import customer_segmentation, plot_segmentation
from samples.product_clustering import product_segmentation, plot_product_segmentation
from samples.supplier_segmentation import supplier_segmentation, plot_supplier_segmentation
from fastapi.responses import JSONResponse


app = FastAPI()

@app.get("/")
def root():
    return {"message": "FastAPI çalışıyor!"}


@app.get("/country-analysis")
def get_country_analysis():
    df, outliers = country_segmentation()
    plot_country_segmentation(df)
    
    return {
        "countries": df.to_dict(orient="records"),
        "outliers": outliers[["country"]].to_dict(orient="records"),
        "segmentation_image": "/static/country_segmentation.png"
    }


@app.get("/customer-segmentation")
def get_customer_segmentation():
    try:
        df, outliers = customer_segmentation()   
        customers_normal = df[df["cluster"] != -1]  
        outliers_data = outliers[["customer_id", "total_orders", "total_spent"]].to_dict(orient="records")
        plot_segmentation(df)
        return JSONResponse(content={
            "customers_normal": customers_normal[["customer_id", "total_orders", "total_spent", "avg_order_value", "cluster"]].to_dict(orient="records"),
            "outliers": outliers_data,
            "segmentation_image": "/static/customer_segmentation.png"
        })
    except Exception as e:
        return {"error": str(e)}


@app.get("/product-segmentation")
def get_product_segmentation():
    df, niche_products = product_segmentation()
    plot_product_segmentation(df)

    return {
        "products": df.to_dict(orient="records"),
        "niche_products": niche_products[["product_name", "cluster"]].to_dict(orient="records"),
        "segmentation_image": "/static/product_segmentation.png"
    }


@app.get("/supplier-segmentation")
def get_supplier_segmentation():
    df, niche_suppliers = supplier_segmentation()
    plot_supplier_segmentation(df)

    return {
        "suppliers": df.to_dict(orient="records"),
        "niche_suppliers": niche_suppliers[["supplier_name", "cluster"]].to_dict(orient="records"),
        "segmentation_image": "/static/supplier_segmentation.png"
    }