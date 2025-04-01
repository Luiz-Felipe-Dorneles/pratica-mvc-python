import mysql.connector as mc  # Impotando a biblioteca do conector do MySQL
from mysql.connector import Error  # Importando a classe Error para tratar as mensagens de erro
from dotenv import load_dotenv  # Importando a função load_dotenv
from os import getenv  # Importando a função getenv

class Database:
    def __init__(self):
        load_dotenv()  # Carrega as variáveis de ambiente do arquivo .env
        self.host = getenv('DB_HOST')  # Obtém o host do banco de dados
        self.username = getenv('DB_USER')  # Obtém o nome de usuário do banco de dados
        self.password = getenv('DB_PSWD')  # Obtém a senha do banco de dados
        self.database = getenv('DB_NAME')  # Obtém o nome do banco de dados
        self.connection = None  # Inicializa a variável da conexão
        self.cursor = None  # Inicializa a variável do cursor

    def conectar(self):
        """Estabelece uma conexão com o banco de dados."""
        try:
            self.connection = mc.connect(
                host=self.host,
                database=self.database,
                user=self.username,
                password=self.password
            )
            if self.connection.is_connected():
                self.cursor = self.connection.cursor(dictionary=True)  # Cria o cursor
                print('Conexão ao banco de dados realizada com sucesso!')
        except Error as e:
            print(f'Erro de conexão: {e}')
            self.connection = None
            self.cursor = None

    def desconectar(self):
        """Encerra a conexão com o banco de dados e o cursor, se existirem."""
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()
        print('Conexão com o banco de dados encerrada com sucesso!')

    def iniciar_transacao(self):
        """Inicia uma transação no banco de dados."""
        if self.connection:
            self.connection.autocommit = False  # Desativa o autocommit para iniciar a transação

    def commit(self):
        """Confirma a transação no banco de dados."""
        if self.connection:
            self.connection.commit()

    def rollback(self):
        """Reverte a transação no banco de dados em caso de erro."""
        if self.connection:
            self.connection.rollback()

    def executar(self, sql, params=None):
        """Executa uma instrução no banco de dados."""
        if self.connection is None or self.cursor is None:
            print('Conexão ao banco de dados não estabelecida!')
            return None

        try:
            self.cursor.execute(sql, params)  # Executa a instrução SQL
            self.connection.commit()  # Confirma a transação
            return self.cursor
        except Error as e:
            print(f'Erro de execução: {e}')
            self.rollback()  # Se ocorrer erro, faz o rollback da transação
            return None

    def consultar(self, sql, params=None):
        """Executa uma instrução no banco de dados e retorna os resultados."""
        if self.connection is None or self.cursor is None:
            print('Conexão ao banco de dados não estabelecida!')
            return None

        try:
            self.cursor.execute(sql, params)  # Executa a instrução SQL
            return self.cursor.fetchall()  # Retorna os resultados da consulta
        except Error as e:
            print(f'Erro de execução: {e}')
            self.rollback()  # Se ocorrer erro, faz o rollback da transação
            return None
