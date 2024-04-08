import sqlite3

class Backend:
    def __init__(self) -> None:
        pass

    
    def criar_tabela(self):
        conn = sqlite3.connect('Cliente.db')
        cursor = conn.cursor()
        query = '''CREATE TABLE IF NOT EXISTS Cliente(
                    ID INTEGER    PRIMARY KEY AUTOINCREMENT,
                    Nome     TEXT,
                    Email    TEXT,
                    Telefone TEXT (15),
                    sexo     TEXT (5),
                    Senha    TEXT (255) 
            );'''
        cursor.execute(query)
        conn.close()
    
    def inserir(self,nome,email,senha,tel,sexo):
        try:
            conn = sqlite3.connect('Cliente.db')
            cursor = conn.cursor() #é um interador que permite navegar e manipular os registros do bd
            query_insert = """
                            INSERT INTO CLIENTE (Nome,Email,Telefone,Sexo,Senha) 
                            VALUES(?,?,?,?,?)"""#query é uma string que contém a instrução SQL. Os ? são placeholders que serão substituídos pelos valores em params
            params = (nome,email,tel,sexo,senha) #é uma tupla que contém os valores que você deseja inserir no banco de dados. A ordem dos valores na tupla corresponde à ordem dos placeholders na consulta.
            cursor.execute(query_insert,params)
            conn.commit()
            conn.close()
        except sqlite3.OperationalError:
            self.criar_tabela()
        except sqlite3.DatabaseError as e:
            print(f'(Ocorreu um erro: {e})')
        except Exception as e:
            print(f'Ocorreu um erro:{e}')
            
    
    def visualizar(self):
        conn = sqlite3.connect('Cliente.db')
        cursor = conn.cursor()
        cursor.execute("""SELECT * FROM Cliente""")
        col_names = [description[0] for description in cursor.description] # obetenção dos nomes das colunas
        rows = cursor.fetchall() #esse metodo busca todos os registros
        conn.close()
        data = [dict(zip(col_names,row))for row in rows] #converte para um dicionario
        return data
        
    def editar_dado(self,id,campo,novo_campo):
        conn = sqlite3.connect('Cliente.db')
        cursor = conn.cursor()
        query = (f"""UPDATE cliente SET ? = ? WHERE ID = ? """)
        params = (campo,novo_campo,id)
        cursor.execute(query,params)
        conn.commit()
        conn.close()    
    def excluir(self,id):
        conn = sqlite3.connect('Cliente.db')
        cursor = conn.cursor()
        query = ("""DELETE FROM Cliente WHERE ID = ? """)
        params = (id,)
        cursor.execute(query,params)
        conn.commit()
        conn.close()  
           
                        
            
