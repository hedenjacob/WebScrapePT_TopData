# Web Scraper og Databaseopdatering

Dette script er specifikt designet til at skrabe produktpriser fra Topdata's hjemmeside og opdatere en database med disse priser og tilknyttede produktspecifikationer. Det er udviklet som et testprojekt for at øve Python-programmering og SQL-databaseintegration samt for at udføre datavisualisering i Power BI.

## Funktioner

- **Databaseopsætning**: Koden opretter en database med tre tabeller: `produkter`, `pris_historik` og `produkt_specifikationer`, ved hjælp af SQLAlchemy.
- **Produktklasser**: Der er tre klasser defineret for produkter, pris historik og produkt specifikationer, der afspejler strukturen i databasen.
- **Web Scraping**: Der bruges Selenium til at besøge Topdata's hjemmesider og indsamle produktpriser og navne baseret på den specifikke CSS-struktur på webstedet.
- **Datahåndtering**: Produkter og deres specifikationer oprettes eller opdateres i databasen efter behov.
- **Prishistorik**: Der holdes styr på ændringer i priser over tid ved at opdatere en separat tabel med pris historik.
- **Produktspecifikationer**: Produktnavne analyseres for at ekstrahere CPU, RAM og GPU-specifikationer.

## Installation

1. Installer de nødvendige biblioteker ved at køre `pip install -r requirements.txt`.
2. Sørg for at have en MySQL-database opsat, og opdater forbindelsesstrengen i koden efter behov.
3. Kør scriptet ved at køre `python your_script.py`.

## Anvendelse

- Tilpas listerne af URL'er efter dine behov, og kør scriptet for at opdatere databasen med de nyeste priser og specifikationer.

## Bemærkninger

- Dette script er skræddersyet til Topdata's hjemmeside og forudsætter en ensartet CSS-struktur på de angivne URL'er. Tilpas scriptet, hvis det skal anvendes på andre websteder.
- Vær opmærksom på webstedsbrugsbetingelser og de data, du skraber, for at undgå brud på reglerne eller krænkelser af ophavsret.
- Efter opdatering af databasen kan du udføre datavisualisering i Power BI eller andre værktøjer for at analysere dataene yderligere.
