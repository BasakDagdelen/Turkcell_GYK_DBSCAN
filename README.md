# DBSCAN İle Kümeleme Analizi

## Proje Açıklaması

Bu proje, dört farklı problemini çözmek için FastAPI tabanlı bir API geliştirmektedir. API, aşağıdaki problemleri çözmektedir:

1. **Ülkelere Göre Satış Deseni Analizi (Country Segmentation)**
2. **Müşteri Segmentasyonu (Customer Segmentation)**
3. **Ürün Kümeleme (Product Segmentation)**
4. **Tedarikçi Segmentasyonu (Supplier Segmentation)**

Her bir problem için DBSCAN algoritması kullanılarak veriler kümelenmiş ve sıra dışı (outlier) veriler tespit edilmiştir. API, bu segmentasyonlar ve görselleştirmeleri kullanıcılara sunmaktadır.

## İçindekiler

- [Kurulum](#kurulum)
- [Proje Yapısı](#proje-yapısı)
- [Kullanım](#kullanım)
- [Teknolojiler](#teknolojiler)
- [Görseller](#görseller)

## Kurulum

Bu projeyi çalıştırmak için aşağıdaki adımları takip edebilirsiniz:

1. **Python ve gerekli paketleri yükleyin:**
   
   Python 3.8 veya daha yüksek bir sürüm gereklidir. Ayrıca proje ile çalışmak için gerekli kütüphaneleri yüklemeniz gerekmektedir.

   ```bash
   pip install -r requirements.txt

2. **Veritabanı bağlantısı:**

    PostgreSQL veritabanı bağlantısını ayarlamanız gerekir. database.py dosyasındaki bağlantı bilgilerini kendi veritabanı sunucunuza göre güncelleyin.
   
      ```bash
   user = 'kullanıcı_adı'
   password = 'şifre'
   host = 'localhost'
   port = 5432
   database = 'veritabani_adı'

3. **Veritabanı tabloları:**

    Bu projede kullanılan `customers`, `orders`, `order_details`, `products` ve `suppliers` tablolara sahip bir **PostgreSQL** veritabanına ihtiyacımız vardır. 

 
## Proje Yapısı
![image](https://github.com/user-attachments/assets/f2692384-0e32-4146-a811-0e10d7f714af)

  
### `samples` Klasörü İçeriği

Her bir Python dosyası, belirli bir probleme yönelik analiz ve kümeleme işlemlerini içermektedir:

- **`country_segmentation.py`**:  
  Ülkeler arası satış deseni analizini gerçekleştirir ve DBSCAN algoritmasıyla kümeler oluşturur.

- **`customer_segmentation.py`**:  
  Müşteri verilerini kullanarak alışveriş davranışlarını analiz eder, kümeler ve aykırı verileri tespit eder.

- **`product_clustering.py`**:  
  Ürünlerin sipariş geçmişine göre gruplandırılmasını sağlar ve niş ürünleri tanımlar.

- **`supplier_segmentation.py`**:  
  Tedarikçileri, sağladıkları ürünlerin satış performansına göre segmentlere ayırır.


## Kullanım
Proje çalıştırıldığında FastAPI uygulaması başlatılır. API'yi kullanarak dört farklı segmentasyon probleminin çözümlerine ve görselleştirmelere erişebilirsiniz.

1. **API'yi çalıştırma:**

   FastAPI uygulamasını başlatmak için terminalde şu komutu kullanabilirsiniz.  

    ```bash
   uvicorn api:app --reload

2. **API'yi kullanma:**

   API'deki her bir uç noktaya şu URL'leri kullanarak erişebilirsiniz:

- **Ülkelere Göre Satış Deseni Analizi:**  Bu endpoint, ülkelere göre satış deseni analizi yapacak ve kümelenmiş verileri döndürecektir.
 
    ```bash
   GET /country-analysis

- **Müşteri Segmentasyonu:** Bu endpoint, müşteri verilerini analiz ederek segmentlere ayırır ve aykırı müşteri verilerini döndürür.

    ```bash
   GET /customer-segmentation

- **Ürün Kümeleme:** Ürünleri, satış geçmişlerine göre gruplar ve niş ürünleri tespit eder.

    ```bash
   GET /product-segmentation

 - **Tedarikçi Segmentasyonu:** Tedarikçilerin sağladıkları ürünlerin satış performansına göre kümeleme işlemi gerçekleştirir.

    ```bash
   GET /supplier-segmentation


## Teknolojiler
Bu projede aşağıdaki teknolojiler kullanılmıştır:

- Python 3.8+

- FastAPI: API sunucusu

- PostgreSQL: Veritabanı

- DBSCAN: Kümeleme algoritması

- scikit-learn: Veri madenciliği için gerekli araçlar

- Matplotlib: Veri görselleştirmeleri

- SQLAlchemy: Veritabanı bağlantısı için ORM
