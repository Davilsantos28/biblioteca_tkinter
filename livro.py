class Livro:
    def __init__(self, titulo, autor, ano):
        self.titulo = titulo
        self.autor = autor
        self.ano = ano
        self.status_ = True

    def verificar_disponibilidade(self, mydb):
        mycursor = mydb.cursor()
        sql = "SELECT COUNT(*) FROM emprestimos WHERE id_livro = (SELECT id_livro FROM livros WHERE titulo = %s)"
        val = (self.titulo,)
        mycursor.execute(sql, val)
        emprestado = mycursor.fetchone()[0] > 0
        mycursor.close()
        return not emprestado

    def emprestar(self, mydb):
        if self.verificar_disponibilidade(mydb):
            self.status_ = False
            return True
        else:
            return False

    def devolver(self):
        if not self.status_:
            self.status_ = True
            return True
        else:
            return False
