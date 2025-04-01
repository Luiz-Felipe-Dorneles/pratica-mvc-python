from model.database import Database

class Tarefa:
    def __init__(self, id=None, titulo=None, data_conclusao=None):
        self.id = id
        self.titulo = titulo
        self.data_conclusao = data_conclusao

    def salvarTarefa(self):
        """Salva uma nova tarefa no banco de dados."""
        db = Database()
        try:
            db.conectar()
            sql = 'INSERT INTO tarefa (titulo, data_conclusao) VALUES (%s, %s)'
            params = (self.titulo, self.data_conclusao)
            db.executar(sql, params)
        except Exception as e:
            print(f"Erro ao salvar tarefa: {e}")
        finally:
            db.desconectar()

    @staticmethod
    def listarTarefas():
        """Retorna uma lista de tarefas cadastradas."""
        db = Database()
        try:
            db.conectar()
            sql = 'SELECT id, titulo, data_conclusao FROM tarefa'
            tarefas = db.consultar(sql)
        except Exception as e:
            print(f"Erro ao listar tarefas: {e}")
            tarefas = []
        finally:
            db.desconectar()

        return tarefas if tarefas else []

    def editarTarefa(self, novo_titulo=None, nova_data_conclusao=None):
        """Edita os dados da tarefa no banco de dados."""
        db = Database()
        try:
            db.conectar()
            db.iniciar_transacao()

            # Atualiza os campos somente se novos valores forem fornecidos
            if novo_titulo:
                sql = 'UPDATE tarefa SET titulo = %s WHERE id = %s'
                db.executar(sql, (novo_titulo, self.id))

            if nova_data_conclusao:
                sql = 'UPDATE tarefa SET data_conclusao = %s WHERE id = %s'
                db.executar(sql, (nova_data_conclusao, self.id))

            db.commit()
        except Exception as e:
            db.rollback()
            print(f"Erro ao editar tarefa: {e}")
        finally:
            db.desconectar()

    def apagarTarefa(self):
        """Apaga uma tarefa cadastrada no banco de dados."""
        db = Database()
        try:
            db.conectar()
            sql = 'DELETE FROM tarefa WHERE id = %s'
            db.executar(sql, (self.id,))
        except Exception as e:
            print(f"Erro ao apagar tarefa: {e}")
        finally:
            db.desconectar()
