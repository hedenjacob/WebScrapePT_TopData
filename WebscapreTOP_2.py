import re
from sqlalchemy import create_engine, Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

Base = declarative_base()

class Produkt(Base):
    __tablename__ = 'produkter'
    id = Column(Integer, primary_key=True)
    navn = Column(String(255), unique=True)
    pris = Column(String(255))
    tidspunkt = Column(DateTime, default=datetime.utcnow)
    specifikationer = relationship("ProduktSpecifikation", back_populates="produkt")

class PrisHistorik(Base):
    __tablename__ = 'pris_historik'
    id = Column(Integer, primary_key=True)
    produkt_id = Column(Integer, ForeignKey('produkter.id'))
    pris = Column(String(255))
    tidspunkt = Column(DateTime, default=datetime.utcnow)

class ProduktSpecifikation(Base):
    __tablename__ = 'produkt_specifikationer'
    id = Column(Integer, primary_key=True)
    produkt_id = Column(Integer, ForeignKey('produkter.id'))
    cpu = Column(String(255))
    ram = Column(String(255))
    gpu = Column(String(255))  # Tilføjet en GPU-kolonne

Produkt.specifikationer = relationship("ProduktSpecifikation", back_populates="produkt")
ProduktSpecifikation.produkt = relationship("Produkt", back_populates="specifikationer")

# Databaseforbindelse og sessionsopsætning
engine = create_engine('mysql+mysqlconnector://root:root@localhost:3306/testtop', echo=True)
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)

def extract_specifikationer(produkt_navn):
    specifikationer = {}

    # Regex mønstre for CPU, RAM og GPU
    cpu_pattern = r'(?:RYZEN-\d{3,5}[a-zA-Z]?|i\d{3,5}[a-zA-Z]?|7800X3D|i7-\d{4,5}[a-zA-Z]?|RYZEN7-7700|i5-12400F)'
    ram_pattern = r'\d+G-6000-RAM|\d+G-6000-D5-RAM'
    gpu_pattern = r'RTX\d+SUPER-\d+G|RTX\d+-\d+G|TUF-RTX\d+SUPER-\d+G|TUF-RTX\d+-\d+G|RTX4060TI-\d+G|RTX4070TISUPER-\d+G'


    # Søg efter specifikationer i produkt_navn
    cpu_match = re.search(cpu_pattern, produkt_navn)
    ram_match = re.search(ram_pattern, produkt_navn)
    gpu_match = re.search(gpu_pattern, produkt_navn)

    # Gem matchede specifikationer i dictionary
    if cpu_match:
        specifikationer['cpu'] = cpu_match.group().strip()
    if ram_match:
        specifikationer['ram'] = ram_match.group().strip()
    if gpu_match:
        specifikationer['gpu'] = gpu_match.group().strip()

    return specifikationer


def skrab_priser_og_opdater_prishistorik(urls):
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    
    session = None
    try:
        session = Session()
        
        for url in urls:
            print(f"Besøger URL: {url}")
            driver.get(url)
            driver.implicitly_wait(10)
            
            produkter = driver.find_elements(By.CSS_SELECTOR, ".m-productlist-title")
            priser = driver.find_elements(By.CSS_SELECTOR, ".m-productlist-price.h5.is-block")

            for produkt, pris in zip(produkter, priser):
                print(f"Produkt: {produkt.text}, Pris: {pris.text}")
                produkt_obj = session.query(Produkt).filter_by(navn=produkt.text).first()

                # Opret produkt og dets specifikationer, hvis det ikke allerede eksisterer
                if not produkt_obj:
                    print(f"Produkt '{produkt.text}' findes ikke i databasen. Tilføjer nyt produkt.")
                    produkt_obj = Produkt(navn=produkt.text, pris=pris.text)
                    session.add(produkt_obj)
                    session.commit()

                    # Ekstraher specifikationer fra produktnavnet
                    specifikationer = extract_specifikationer(produkt.text)
                    if specifikationer:
                        print(f"Specifikationer for produkt '{produkt.text}': {specifikationer}")
                        # Opret specifikationer for produktet
                        produkt_spec = ProduktSpecifikation(produkt_id=produkt_obj.id, **specifikationer)
                        session.add(produkt_spec)
                        session.commit()

                    # Opret også prishistorik
                    ny_pris_historik = PrisHistorik(produkt_id=produkt_obj.id, pris=pris.text)
                    session.add(ny_pris_historik)
                    session.commit()

                else:
                    print(f"Produkt '{produkt.text}' er allerede i databasen.")

                    pris_opdateret = False
                    if produkt_obj.pris != pris.text:
                        print(
                            f"Opdaterer pris for '{produkt.text}' fra {produkt_obj.pris} til {pris.text}."
                        )
                        produkt_obj.pris = pris.text
                        pris_opdateret = True

                    specifikationer = extract_specifikationer(produkt.text)
                    eksisterende_spec = (
                        session.query(ProduktSpecifikation)
                        .filter_by(produkt_id=produkt_obj.id)
                        .first()
                    )

                    if specifikationer:
                        if eksisterende_spec:
                            spec_opdateret = False
                            for felt, vaerdi in specifikationer.items():
                                if getattr(eksisterende_spec, felt) != vaerdi:
                                    print(
                                        f"Opdaterer {felt} for '{produkt.text}' til {vaerdi}."
                                    )
                                    setattr(eksisterende_spec, felt, vaerdi)
                                    spec_opdateret = True
                            if spec_opdateret:
                                session.commit()
                        else:
                            print(
                                f"Tilføjer manglende specifikationer for '{produkt.text}': {specifikationer}"
                            )
                            ny_spec = ProduktSpecifikation(
                                produkt_id=produkt_obj.id, **specifikationer
                            )
                            session.add(ny_spec)
                            session.commit()

                    if pris_opdateret:
                        ny_pris_historik = PrisHistorik(
                            produkt_id=produkt_obj.id, pris=pris.text
                        )
                        session.add(ny_pris_historik)
                        session.commit()

    finally:
        if session is not None:
            session.close()
        driver.quit()

urls = [
    "https://topdata.dk/",
    "https://topdata.dk/shop/443-top-professional/",
    "https://topdata.dk/shop/452-top-prime/",
    "https://topdata.dk/shop/444-top-performance/",
    "https://topdata.dk/shop/447-game-saet/",
]
skrab_priser_og_opdater_prishistorik(urls)
