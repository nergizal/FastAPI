from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = "sqlite:///./todoai_app.db" #database urlsini giriyoruz.Bizim databaseimiz burada oluşacak.
#veritabanı farklı sunucuda uygulama farklı sunucuda olur genelde
engine = create_engine( #bizden url yi alıyor nasıl bağlantı açacağın bakıyor
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
#Bağlantı açmak
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
#Modelleri oluştururken kullanıcaz.
Base = declarative_base()
