import pandas as pd
import numpy as np

# Učitajte stari CSV datoteku
old_csv_path = r'c:\Users\Ivana\OneDrive\Desktop\SIR\SIR_projekt\novi\Crash_Data_novi.csv'
df = pd.read_csv(old_csv_path)

# Izaberite samo potrebne stupce za tablicu crash
crash_df = df[['Crash ID', 'Crash Type']].copy()

# Generirajte iste nasumične brojeve za sve nove stupce
num_rows = len(crash_df)
random_numbers = np.random.randint(1, 31755, size=(
    num_rows, 1))  # Samo jedan set nasumičnih brojeva

# Dodajem stupac Penalty Price s nasumičnim vrijednostima iz zadanog skupa
# Kreirajte niz brojeva od 30 do 400 s korakom 10
penalty_prices = np.arange(30, 410, 10)
crash_df.loc[:, 'Penalty Price'] = np.random.choice(
    penalty_prices, size=num_rows)


# Dodajte nove stupce u DataFrame
crash_df.loc[:, 'State_id'] = np.random.randint(1, 249, size=(num_rows, 1))
crash_df.loc[:, 'Hour_id'] = random_numbers
crash_df.loc[:, 'Victim_id'] = random_numbers
crash_df.loc[:, 'Speed_id'] = random_numbers
crash_df.loc[:, 'Holiday_id'] = random_numbers


# Spremite podatke u novu CSV datoteku
new_csv_path = r'c:\Users\Ivana\OneDrive\Desktop\SIR\SIR_projekt\novi\Crashtablica.csv'
crash_df.to_csv(new_csv_path, index=False)
