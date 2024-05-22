import pandas as pd
import numpy as np

# Putanja do originalnog skupa podataka
CSV_FILE_PATH = r'c:\Users\Ivana\OneDrive\Desktop\SIR\SIR_projekt\novi\Crash_Data_novi.csv'

# Učitavanje skupa podataka
df = pd.read_csv(CSV_FILE_PATH, delimiter=',', low_memory=False)
print("Original CSV size: ", df.shape)

# Provjeravanje prvih nekoliko redaka
print(df.head())

# Generiranje nasumičnih brojeva
num_rows = df.shape[0]
random_crash_ids = np.random.permutation(np.arange(1, num_rows + 1))

# Zamjena postojećih vrijednosti u stupcu 'Crash ID' novim nasumičnim brojevima
df['Crash ID'] = random_crash_ids

# Provjeravanje izmijenjenih vrijednosti
print(df.head())

# Spremanje ažuriranog skupa podataka natrag u CSV datoteku
df.to_csv(CSV_FILE_PATH, index=False)

print("Ažurirani CSV je spremljen.")
