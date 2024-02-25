import streamlit as st

# Zdefiniowanie prawidłowych danych logowania 
valid_username = "admin"
valid_password = "admin"

# Interfejs użytkownika
st.title("Ekran Logowania")

# Pola do wprowadzania nazwy użytkownika i hasła
username = st.text_input("Nazwa Użytkownika")
password = st.text_input("Hasło", type="password")

# Przycisk do zatwierdzania danych logowania
if st.button("Zaloguj"):
    # Sprawdzenie czy dane logowania są poprawne
    if username == valid_username and password == valid_password:
        st.success("Zalogowano pomyślnie!")
        st.header('Pomarańcza wita')
        st.write('---')
        st.info('Aplikacja do zarządzania siecią sklepów Pomarańcza.  \n Projekt Studencki :)')

    else:
        st.error("Błąd logowania. Sprawdź nazwę użytkownika i hasło.")

