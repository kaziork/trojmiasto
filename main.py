# 5. Prototyp aplikacji webowej
##  Streamlit
# Utwórz aplikację z prostym interfejsem do wprowadzenia danych (metraż, liczba pokoi, dzielnica, zdjęcia itp.).
# Po kliknięciu przycisku „Oblicz cenę” aplikacja wyświetla szacowaną cenę i wizualizację porównawczą.
from pdb import run
import streamlit as st
import pandas as pd
import joblib
import plotly.express as px

# === Funkcja predykcji ===
def predict_price(area_m2, rooms, photos, locality, city, owner_direct):
   # Wczytanie modelu z pliku
   model = joblib.load("model_regresji_liniowej_trojmiasto.pkl")

   # surowy 1-wierszowy DataFrame
   
   X_tested_df = pd.DataFrame([{
       "area_m2": float(area_m2),
       "rooms": int(rooms),
       "photos": float(photos),
       "owner_direct": owner_direct,
       "locality": locality,
       "city": city,
   }])
   
   # one-hot encoding tak jak w treningu + wyrównanie kolumn
   X_tested_dummy = pd.get_dummies(X_tested_df, columns=['locality', 'city', 'owner_direct']).astype(float)
   
   # X_new = X_new.reindex(columns=TRAIN_COLUMNS, fill_value=0).astype(float)
   TRAIN_COLUMNS = joblib.load("train_columns.joblib")
   missing_cols = set(TRAIN_COLUMNS) - set(X_tested_dummy.columns)
   for c in missing_cols:
    X_tested_dummy[c] = 0.0

   # Ensure the order of columns is the same
   X_tested_dummy = X_tested_dummy[TRAIN_COLUMNS]

   # stosuję ten sam scaler co w treningu
   scaler = joblib.load("scaler_trojmiasto.pkl")
   X_tested_standard = scaler.transform(X_tested_dummy)
   
   return model.predict(X_tested_standard)[0]


df = pd.read_csv("cleaned_trojmiasto.csv")


# === Główna logika aplikacji ===
def main():
   st.title("Predykcja ceny mieszkania (Trojmiasto)")
   st.write("Podaj dane mieszkania, aby uzyskać szacowaną cenę:")

   # Komponenty UI
   area = st.number_input("Powierzchnia (m²)", min_value=10.0, max_value=300.0, value=50.0)
   rooms = st.slider("Liczba pokoi", 1, 7, 3)
   photos = st.number_input("Liczba zdjęć", 0, 50, 10)

   owner_direct = st.selectbox("Oferta bezpośrednio od właściciela", sorted(df['owner_direct'].unique()))
   city = st.selectbox("Miasto", sorted(df['city'].unique()))

   # filtrowanie dostępnych dzielnic tylko dla wybranego miasta
   available_localities = sorted(df[df['city'] == city]['locality'].unique())
   locality = st.selectbox("Dzielnica", available_localities)
   

   if st.button("Oblicz cenę"):
       price = predict_price(area, rooms, photos, locality, city, owner_direct)
       st.success(f"Szacowana cena: {price:,.0f} zł")

       # === Scatterplot dla danego miasta (bez outlierów) ===
       city_subset = df[df['city'] == city]
       # usuń outliery: area_m2 > 160 i price_total_zl_cleaned > 3.5 mln
       city_subset = city_subset[
           (city_subset['area_m2'] <= 160) &
           (city_subset['price_total_zl_cleaned'] <= 3_500_000)
       ]
       if not city_subset.empty:
           fig_scatter = px.scatter(
               city_subset,
               x='area_m2',
               y='price_total_zl_cleaned',
               title=f'Twoje mieszkanie względem innych ofert ({city})',
               hover_data=['locality', 'rooms', 'price_per_m2_zl_cleaned']
           )
           # wszystkie punkty na niebiesko
           fig_scatter.update_traces(marker=dict(color='blue', size=6, opacity=0.7))
           # dodaj punkt prognozy: większy i czerwony
           fig_scatter.add_scatter(
               x=[area],
               y=[price],
               mode='markers',
               marker=dict(color='red', size=14),
               name='Prognoza'
           )
           fig_scatter.update_layout(
               xaxis_title='Powierzchnia (m²)',
               yaxis_title='Cena całkowita (zł)'
           )
           st.plotly_chart(fig_scatter, use_container_width=True)
      
# === Punkt wejścia ===
if __name__ == "__main__":
   main()
