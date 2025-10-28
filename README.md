# Analiza rynku mieszkań w Trójmieście  

Projekt przedstawia analizę rynku nieruchomości w Trójmieście (Gdańsk, Gdynia, Sopot) na podstawie danych z portalu **adresowo.pl**.  
Celem projektu było przygotowanie pełnego pipeline’u: od pobrania danych, poprzez ich oczyszczenie, analizę i wizualizację, aż po stworzenie modelu predykcyjnego oraz prototypu aplikacji webowej.

---

## 1. Pobieranie danych (web scraping)
- **`scrapper/`** – folder zawierający skrypt do scrapowania danych z adresowo.pl  
- **`ogloszenia_trojmiasto.csv`** – surowe dane zebrane z portalu (przed czyszczeniem)

---

## 2. Czyszczenie i przygotowanie danych
- **`data_cleaning.ipynb`** – notebook z procesem czyszczenia danych, usuwaniem błędów i konwersją typów  
- **`cleaned_trojmiasto.csv`** – dane po oczyszczeniu, gotowe do analizy  

---

## 3. Analiza i wizualizacja danych
- **`analiza_i_wizualizacja.ipynb`** – główny notebook z analizą eksploracyjną (EDA) i wizualizacjami  
- **`box_plot_rozkladu_cen.pdf`** – wykres rozkładu cen w Trójmieście  
- **`powierzchnia_a_cena.pdf`** – wykres zależności ceny od powierzchni  
- **`ranking_dzielnic_po_cenie.pdf`** – ranking dzielnic wg średniej ceny za m²  

---

## 🤖 4. Model predykcyjny
- **`regresja.ipynb`** – eksperymenty z modelami regresyjnymi (m.in. Random Forest, Linear Regression)  
- **`model_regresji_liniowej_trojmiasto.pkl`** – zapisany model regresji liniowej  
- **`main.py`** – skrypt do testowania modelu i generowania prognoz lokalnie
- **`train_columns.joblib`** – zapisany układ kolumn wykorzystany w modelu  
- **`scaler_trojmiasto.pkl`** – zapisany obiekt skalera do normalizacji cech  

---

## 🌐 5. Prototyp aplikacji webowej
- **`app.py`** – aplikacja Streamlit wykorzystująca zapisany model do przewidywania cen mieszkań  
  - umożliwia wprowadzenie danych mieszkania,  
  - zwraca prognozowaną cenę,  
  - pokazuje lokalizację mieszkania na scatterplocie (w kontekście innych ofert).

---

## ⚙️ 6. Uruchomienie projektu

### Instalacja zależności
Jeśli chcesz uruchomić projekt w nowym środowisku:
```bash
pip install -r requirements.txt
