def symulacja_bazowa():

    # --- WCZYTYWANIE DANYCH ---
    dane = pd.read_excel("C:/Users/qb4co/Desktop/research do filmów/MonteCarlo tutotial/dane/dane.xlsx", sheet_name="ogólne")
    
    # --- WEKTORY ---
    ludnosc_k = np.array(dane['Liczba kobiet'])
    ludnosc_m = np.array(dane['Liczba mężczyzn'])
    p_urodzenia = np.array(dane['P-stwo urodzenia'])
    p_zgonu_k = np.array(dane['P-stwo zgonu K'])
    p_zgonu_m = np.array(dane['P-stwo zgonu M'])
    
    # --- PARAMETRY ---
    n_rows_dane = len(dane)
    n_days = 1000
    
    # --- MACIERZE ---
    zdrowi_k = np.zeros(n_rows_dane)
    zdrowi_m = np.zeros(n_rows_dane)
    
    zdrowi_k_stan_baza = np.zeros(n_days)
    zdrowi_m_stan_baza = np.zeros(n_days)
    urodzeni_k_stan_baza = np.zeros(n_days)
    urodzeni_m_stan_baza = np.zeros(n_days)
    urodzeni_k = np.zeros((n_days, n_rows_dane))
    urodzeni_m = np.zeros((n_days, n_rows_dane))
    zmarli_k = np.zeros((n_days, n_rows_dane))
    zmarli_m = np.zeros((n_days, n_rows_dane))
    zmarli_ogolem_k_stan_baza = np.zeros(n_days)
    zmarli_ogolem_m_stan_baza = np.zeros(n_days)
    
    # --- INICJALIZACJA ---
    zdrowi_k[:] = ludnosc_k[:]
    zdrowi_m[:] = ludnosc_m[:]
    
    # --- SYMULACJA ---
    dzien = 0
    while dzien < n_days:
        
        # zgony naturalne
        mean_k = zdrowi_k * p_zgonu_k
        mean_m = zdrowi_m * p_zgonu_m
        for grupa in range(n_rows_dane):
            z_k = np.random.poisson(np.clip(mean_k[grupa], 0, None))
            z_m = np.random.poisson(np.clip(mean_m[grupa], 0, None))
            zdrowi_k[grupa] -= z_k
            zdrowi_m[grupa] -= z_m
            zmarli_k[dzien, grupa] = z_k
            zmarli_m[dzien, grupa] = z_m
    
        # urodzenia
        mean = zdrowi_k * p_urodzenia
        for grupa in range(n_rows_dane):
            u = np.random.poisson(np.clip(mean[grupa], 0, None))
            dz = np.random.binomial(n=u, p=0.5)
            zdrowi_k[0] += dz
            zdrowi_m[0] += u - dz
            urodzeni_k[dzien, grupa] = dz
            urodzeni_m[dzien, grupa] = u - dz
    
            #zapisywanie stanu urodzeń (reszta jest zapisana na końcu)
            urodzeni_k_stan_baza[dzien] += dz
            urodzeni_m_stan_baza[dzien] += u - dz
            
        # MECHANIZM STARZENIA SIĘ
        p_dzien_starzenie = 1 / 1825  # dzienne prawdopodobieństwo starzenia się (5 lat = 1825 dni)
        
        for i in reversed(range(n_rows_dane - 1)):  # ostatnia grupa nie starzeje się
            
            lambda_k = zdrowi_k[i] * p_dzien_starzenie
            lambda_m = zdrowi_m[i] * p_dzien_starzenie
    
            przesun_k = np.random.poisson(lambda_k)
            przesun_m = np.random.poisson(lambda_m)
    
            przesun_k = min(przesun_k, zdrowi_k[i])
            przesun_m = min(przesun_m, zdrowi_m[i])
    
            zdrowi_k[i] -= przesun_k
            zdrowi_k[i + 1] += przesun_k
    
            zdrowi_m[i] -= przesun_m
            zdrowi_m[i + 1] += przesun_m
        
        # zapisz stany
        zdrowi_k_stan_baza[dzien] = np.sum(zdrowi_k)
        zdrowi_m_stan_baza[dzien] = np.sum(zdrowi_m)
        zmarli_ogolem_k_stan_baza[dzien] = np.sum(zmarli_k[dzien])
        zmarli_ogolem_m_stan_baza[dzien] = np.sum(zmarli_m[dzien])
    
        dzien += 1

    return zdrowi_k_stan_baza, zdrowi_m_stan_baza, urodzeni_k_stan_baza, urodzeni_m_stan_baza, zmarli_ogolem_k_stan_baza, zmarli_ogolem_m_stan_baza