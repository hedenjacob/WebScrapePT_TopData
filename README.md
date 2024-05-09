# Web Scraper og Databaseopdatering

Dette script er specifikt udviklet til privat brug som et øvelsesprojekt for at lære Python-programmering, webscraping, SQL-databaseintegration og datavisualisering i Power BI.

## Funktioner

- **Databaseopsætning**: Koden opretter en database med tre tabeller: `produkter`, `pris_historik` og `produkt_specifikationer`, ved hjælp af SQLAlchemy.
- **Produktklasser**: Der er tre klasser defineret for produkter, pris historik og produkt specifikationer, der afspejler strukturen i databasen.
- **Web Scraping**: Der bruges Selenium til at skrabe produktpriser fra Topdata's hjemmeside baseret på en specifik CSS-struktur.
- **Datahåndtering**: Produkter og deres specifikationer oprettes eller opdateres i databasen efter behov.
- **Prishistorik**: Der holdes styr på ændringer i priser over tid ved at opdatere en separat tabel med pris historik.
- **Produktspecifikationer**: Produktnavne analyseres for at ekstrahere CPU, RAM og GPU-specifikationer.

## Bemærkninger

- Dette script er kun beregnet til privat brug og ren interesse. Det er udviklet som et øvelsesprojekt og bør tilpasses eller udvides efter behov.
- Vær opmærksom på webstedsbrugsbetingelser og de data, du skraber, for at undgå brud på reglerne eller krænkelser af ophavsret.
- Efter opdatering af databasen kan du udføre datavisualisering i Power BI eller andre værktøjer for at analysere dataene yderligere.
