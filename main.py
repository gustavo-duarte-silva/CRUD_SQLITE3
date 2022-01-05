import pandas as pd
from pathlib import Path
import sqlite3
from sqlite3 import Connection
import streamlit as st
from database import *

def main():
    st.title("CRUD-ESCOLA")
    
    cnn = connect_sql(BANCO)
    alunos_db(cnn)
    materia_db(cnn)
    menu(cnn)

if __name__ == '__main__':
    main()