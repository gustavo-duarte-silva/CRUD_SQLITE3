import pandas as pd
from pathlib import Path
import sqlite3
from sqlite3 import Connection
import streamlit as st

BANCO = 'crud_escola.db'

@st.cache(hash_funcs={Connection: id})
def connect_sql(string: str):
    return sqlite3.connect(string, check_same_thread=False)

def alunos_db(cnn: Connection):
    cnn.execute(
        """CREATE TABLE IF NOT EXISTS alunos 
            (
            id integer primary key autoincrement, 
            nome VARCHAR(255) NOT NULL,
            cpf VARCHAR(255) NOT NULL,
            data_nasc DATE NOT NULL
            );"""
    )
    cnn.commit()

def materia_db(cnn: Connection):
    cnn.execute(
        """CREATE TABLE IF NOT EXISTS materia 
            (
            id INT PRIMARY KEY, 
            NomeMateria VARCHAR(255) NOT NULL
            );"""
    )
    cnn.commit()   

def get_data(cnn: Connection):
    df_alunos = pd.read_sql("SELECT * FROM alunos", cnn)
    df_materia = pd.read_sql("SELECT * FROM materia", cnn)
    return df_alunos, df_materia

def display_tables(cnn: Connection):
    df_alunos, df_materia = get_data(cnn)
    st.write("ALUNOS")
    st.dataframe(df_alunos)
    st.write('Materias')
    st.dataframe(df_materia)

def menu(cnn: Connection):
    user = st.sidebar.text_input(label='Login')
    senha = st.sidebar.text_input(label='Senha', type='password')
    if st.sidebar.checkbox("Logar"):
        if user=='btor' and senha =='123':
            st.sidebar.success("Seja Bem Vindo, Diretor!")
            page = st.selectbox('MENU',['Incluir', 'Alterar', 'Excluir', 'Consultar'])
            if page == 'Consultar':
                display_tables(cnn)
            if page == 'Incluir':
                inserir_alunos(cnn)
            if page == "Excluir":
                delete_alunos(cnn) 
            if page == "Alterar":   
                update(cnn)

def inserir_alunos(cnn: Connection):
    input_name = st.text_input(label='Insira o Nome do Aluno')
    input_cpf = st.text_input(label='Digite seu CPF')
    input_data = st.date_input(label='Data de Nascimento')                    
    if st.button("Save to database"):
        params = (input_name, input_cpf, input_data)
        cnn.execute("INSERT INTO alunos (nome, cpf, data_nasc) VALUES (?, ?, ?)", params)
        cnn.commit()
        st.success("Aluno Adicionado com Sucesso")
    
def delete_alunos(cnn: Connection):
    with st.form(key='excluir'):
        del_input_id = st.text_input(label="ID")
        del_input_button = st.form_submit_button("Enviar")
    if del_input_button:
        params = (del_input_button,)
        cnn.execute("DELETE FROM alunos WHERE id= ?", params)
        st.success("Aluno Deletado com Sucesso")

def update(cnn: Connection):
    with st.form(key='Alterar'):
        alt_input_id = st.text_input(label="ID")
        new_id = st.text_input(label="NEW ID")
        alt_input_nome = st.text_input(label='Insira o Nome do Aluno')
        alt_input_cpf = st.text_input(label='Digite seu CPF')
        alt_input_data = st.date_input(label='Data de Nascimento')
        alt_input_button = st.form_submit_button("Enviar")
    if alt_input_button:
            params=(new_id, alt_input_nome, alt_input_cpf, alt_input_data, alt_input_id)
            cnn.execute("UPDATE alunos SET id = ?, nome = ?, cpf=?, data_nasc=? WHERE id = ?", params)
            cnn.commit()
            st.success("Aluno Alterado com Sucesso")

