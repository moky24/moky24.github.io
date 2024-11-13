# --- ULOHA 1 ---
# nacitanie dat pomocou balicku pandas

# import balicku pandas
import pandas as pd

# nacitanie dat
df = pd.read_csv("Radioactive_Decay_Data.csv")

print(df.head()) # nahlad dat

# --- ULOHA 2 ---
# graf poctu jadier jednotlivych prvkov v zavislosti na case

# pre vykreslenie dat pouzijeme balicek matplotlib
import matplotlib.pyplot as plt

# funkcia plot() pre kazdy ElementX
plt.plot(df.Time, df.Element1, ".", label = "Element1") # df["Time"]
plt.plot(df.Time, df.Element2, ".", label = "Element2")
plt.plot(df.Time, df.Element3, ".", label = "Element3")

# popisky
plt.title('radioactive decay of elements')
plt.xlabel('cas')
plt.ylabel('pocet jadier')

# legenda a zobrazenie
plt.legend()
plt.show()

# --- ULOHA 3 ---
# definovanie funkcie, ktorou data nafitujeme

# nacitame curve_fit z balicku scipy
from scipy.optimize import curve_fit
import numpy as np

def f(x, a, b):
    return a * np.exp(-b*x)

# --- ULOHA 4 ---
# graf s nafitovanymi zavislostami

# funkcia pre vykreslenie prvkov (pre zjednodusenie opakovania kodu)
def fitted(prvok_nazov, farba1, farba2):
    prvok = df[prvok_nazov] # vytiahneme stlpec s prvkom
    parametre, kov_matica = curve_fit(f, df.Time, prvok) # nafitujeme data na funkciu f()
    a, b = parametre # ulozime parametre
    plt.plot(df.Time, prvok, ".", color = farba1, label = f"namerane {prvok_nazov}") # plot povodne data
    plt.plot(df.Time, f(df.Time, a, b), "--", color = farba2, label = f"fitted {prvok_nazov}") # plot vyrovnane hodnoty
    return parametre

plt.figure(figsize=(8, 5)) # zvacsenie figure window
# zavolame funkciu fitted() pre kazdy ElementX
params1 = fitted("Element1", [1, 0, 0], [0.85, 0.7, 0.7]) # red and mid red
params2 = fitted("Element2", [0, 1, 0], [0.7, 0.85, 0.7]) # green and mid green
params3 = fitted("Element3", [0, 0, 1], [0.7, 0.7, 0.85]) # blue and mid blue

# format
plt.title("vyrovnane a namerane hodnoty")
plt.xlabel("cas [roky]")
plt.ylabel("pocet jadier [N]")
plt.legend(bbox_to_anchor=(1.01, 1.0), loc='upper left') # legenda v pravo hore
plt.tight_layout() # aby nebola legenda / plot orezane (aby sa zmestili do figure)
plt.show()

# --- ULOHA 5 ---
# pre kazdy prvok spocitat jeho polcas rozpadu a urcit, o ake prvky sa jedna

# konstanta pre ln(2) pomoocu numpy
ln2 = np.log(2)

# funkcia pre vypocet half-life
def calculate_half_life(b):
    return ln2 / b

# zavolame funkciu pre prametre kazdeho prvku
half_life1 = calculate_half_life(params1[1])
half_life2 = calculate_half_life(params2[1])
half_life3 = calculate_half_life(params3[1])

print(f"Half-life Element1: {half_life1} rokov")
print(f"Half-life Element2: {half_life2} rokov")
print(f"Half-life Element3: {half_life3} rokov")

# import slovniku "half_life" z Half_lives.py
from Half_lives import half_lives

# slovnik jednotiek
units_conversion = {
    "billion years": 1e9,
    "million years": 1e6,
    "years": 1,
    "days": 1 / 365.25,
    "hours": 1 / (365.25 * 24),
    "minutes": 1 / (365.25 * 24 * 60),
    "miliseconds": 1 / (365.25 * 24 * 60 * 60 * 1000)
}

# zistenie elementov na zaklade vypocitanych half-life
def find_element(half_life):
    closest_element = "unknown" # prvotny najblizsi prvok
    min_diff = float("inf")  # prvotna diferencia
    
    # pre kazdy element v slovniku half_lives
    for element in half_lives: 
        element_half_life = half_lives[element]["half-life"] * units_conversion[half_lives[element]["unit"]] # vytiahneme hodnotu half-life pre iterovany prvok a premenime jednotky
        diff = abs(element_half_life - half_life) # zistime diferenciu medzi iterovanym prvkom a nami hladanym prvkom
        
        if diff < min_diff: # ak je diferencia mensia nez nasa ulozena min_diff
            min_diff = diff # tak ju prepiseme novou najnizsou
            closest_element = element # a ulozime si prvok
    
    return closest_element

# zavolame funkciu pre kazdy half-life (prvok)
element1 = find_element(half_life1)
element2 = find_element(half_life2)
element3 = find_element(half_life3)

print(f"Element1 je: {element1}")
print(f"Element2 je: {element2}")
print(f"Element3 je: {element3}")

# --- ULOHA 6 + 7 ---
# pre vsetky prvky pomocou for cyklu:
# a. urcit, kolko jadier prvku bude obsahovat vzorka v roku 114 od pociatku merania rozpadu
# b. spocitat aktivitu prvku v roku 85
# c. vyhladat na aky prvok sa premienaju študované radioaktivne prvky po rozpade - ?

elements = {"Element1": params1, "Element2": params2, "Element3": params3}  # slovnik prvkov

results = {}  # slovnik pre ukladanie vysledkov

for elem, params in elements.items(): # iterujeme napriec ElementX a paramsX
    a, b = params
    init_N = a
    lambda_const = b

    # 6a. pocet jadier v roku 114
    rok_114_N = init_N * np.exp(-lambda_const * 114) # vzorec rozpadu
    #print(f"{elem} pocet v roku 114: {rok_114_N}")

    # 6b. aktivita v roku 85
    year_85_count = init_N * np.exp(-lambda_const * 85)
    aktivita_85 = lambda_const * year_85_count # vzorec aktivity
    #print(f"{elem} aktivita v roku 85: {aktivita_85} Bq")

    # 7. ulozenie vysledkov do slovnika
    results[elem] = {
        "polcas_rozpadu": calculate_half_life(lambda_const), 
        "prvok": find_element(calculate_half_life(lambda_const)), 
        "N_rok_114": rok_114_N,
        "aktivita_rok_85": aktivita_85
    }

# vysledky
for elem, info in results.items(): # iteracia napriec slovnikom vysledkov
    print(f"{elem}:")
    print(f"  Pocet v roku 114: {info['N_rok_114']}")
    print(f"  Aktivita v roku 85: {info['aktivita_rok_85']} Bq")

