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
            alunos_id integer primary key autoincrement, 
            Materias VARCHAR(255) NOT NULL
            );"""
    )
    cnn.commit()   

def get_data(cnn: Connection):
    df_alunos = pd.read_sql("SELECT * FROM alunos", cnn)
    df_materia = pd.read_sql("SELECT * FROM materia", cnn)
    return df_alunos, df_materia

def display_tables(cnn: Connection):
    option = st.radio("Mostrar Tabela: ", ('Alunos', 'Materias'))
    df_alunos, df_materia = get_data(cnn)
    if option == 'Alunos':
        st.dataframe(df_alunos)
    else:
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
    materias = st.multiselect('Quais materias irá fazer?', ['MATEMATICA', 'FISICA', 'QUIMICA', 'INGLES', 'PORTUGUES', 'GEOGRAFIA'], ['FISICA'])                   
    if st.button("Enviar"):
        params_alunos = (input_name, input_cpf, input_data)
        params_materias = (', '.join(materias),)
        cnn.execute("INSERT INTO alunos (nome, cpf, data_nasc) VALUES (?, ?, ?)", params_alunos)
        cnn.execute("INSERT INTO materia (Materias) VALUES (?)", params_materias)
        cnn.commit()
        st.success("Aluno Adicionado com Sucesso")
    
def delete_alunos(cnn: Connection):
    del_input_id = st.text_input(label="ID")
    del_input_button = st.button("Enviar")
    if del_input_button:
        params = (del_input_id,)
        cnn.execute("DELETE FROM alunos WHERE id= ?", params)
        cnn.execute("DELETE FROM materia WHERE alunos_id= ?", params)
        st.success("Aluno Deletado com Sucesso")

def update(cnn: Connection):
    alt_input_id = st.text_input(label="ID ANTIGO")
    new_id = st.text_input(label="NOVO ID")
    alt_input_nome = st.text_input(label='Insira o novo Nome do Aluno')
    alt_input_cpf = st.text_input(label='Digite o novo CPF')
    alt_input_data = st.date_input(label='Nova Data de Nascimento')
    materias = st.multiselect('Quais materias irá fazer?', ['MATEMATICA', 'FISICA', 'QUIMICA', 'INGLES', 'PORTUGUES', 'GEOGRAFIA'])
    alt_input_button = st.button("Enviar")
    if alt_input_button:
            params_alunos=(new_id, alt_input_nome, alt_input_cpf, alt_input_data, alt_input_id)
            params_materias = (new_id, ', '.join(materias), alt_input_id)
            cnn.execute("UPDATE alunos SET id = ?, nome = ?, cpf=?, data_nasc=? WHERE id = ?", params_alunos)
            cnn.execute("UPDATE materia SET alunos_id = ?, Materias = ? WHERE alunos_id = ?", params_materias)
            cnn.commit()
            st.success("Aluno Alterado com Sucesso")

