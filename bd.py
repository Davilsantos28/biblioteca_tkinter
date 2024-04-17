from livro import Livro

def insert(mydb, titulo, autor, ano, status_):
    mycursor = mydb.cursor()

    sql = "INSERT INTO livros (titulo, autor, ano, status_) VALUES (%s, %s, %s, %s)"
    val = (titulo, autor, ano, status_)

    mycursor.execute(sql, val)

    mydb.commit()

    print(mycursor.rowcount, "Inserido com Sucesso.")

    mycursor.close()


def update(mydb, titulo_antigo, titulo_novo, autor, ano, status_):
    mycursor = mydb.cursor()

    sql = "UPDATE livros SET titulo = %s, autor = %s, ano = %s, status_ = %s WHERE titulo = %s"
    val = (titulo_novo, autor, ano, status_, titulo_antigo)

    mycursor.execute(sql, val)

    mydb.commit()

    print(mycursor.rowcount, "registro(s) atualizado(s).")

    mycursor.close()


def delete(mydb, titulo):
    mycursor = mydb.cursor()

    sql = "DELETE FROM livros WHERE titulo = %s"
    val = (titulo,)

    mycursor.execute(sql, val)

    mydb.commit()

    print(mycursor.rowcount, "registro(s) excluído(s).")

    mycursor.close()



def query(mydb):
    mycursor = mydb.cursor()

    sql = "SELECT titulo, autor, ano, status_ FROM livros"
    mycursor.execute(sql)

    rows = mycursor.fetchall()

    # Imprime o cabeçalho da tabela
    print("\n{: <20} {: <30} {: <10} {: <10}".format(
        "Título", "Autor", "Ano", "Status"))
    print("-" * 70)

    # Itera sobre cada linha retornada pela consulta e imprime os dados formatados
    for row in rows:
        # Verifica se o valor é None antes de formatá-lo na string de impressão
        titulo = row[0] if row[0] is not None else ""
        autor = row[1] if row[1] is not None else ""
        ano = row[2] if row[2] is not None else ""
        status_ = "Disponível" if row[3] else "Indisponível" if row[3] is not None else ""

        print("{: <20} {: <30} {: <10} {: <10}".format(
            titulo, autor, ano, status_))

    mycursor.close()



def register(mydb, nome, senha):
    mycursor = mydb.cursor()

    sql = "INSERT INTO usuarios (nome, senha) VALUES (%s, %s)"
    val = (nome, senha)

    mycursor.execute(sql, val)

    mydb.commit()

    print("Usuário registrado com sucesso.")

    mycursor.close()


def login(mydb, nome, senha):
    mycursor = mydb.cursor()

    sql = "SELECT * FROM usuarios WHERE nome = %s AND senha = %s"
    val = (nome, senha)

    mycursor.execute(sql, val)

    user = mycursor.fetchone()

    if user:
        print("Login bem-sucedido.")
        return user
    else:
        print("Credenciais inválidas.")
        return None


def to_lend(mydb, user, titulo):
    mycursor = mydb.cursor()

    # Verificar se o usuário está logado
    if user:
        # Criar um objeto Livro apenas com o título
        livro = Livro(titulo, "", "")

        # Verificar se o livro está disponível
        # Passa a conexão com o banco de dados para verificar a disponibilidade
        if livro.verificar_disponibilidade(mydb):
            try:
                # Inserir registro de empréstimo na tabela emprestimos
                sql_insert_emprestimo = "INSERT INTO emprestimos (id_usuario, id_livro, data_emprestimo) VALUES (%s, (SELECT id_livro FROM livros WHERE titulo = %s), CURDATE())"
                # Acessa o id_usuario da tupla user
                val_insert_emprestimo = (user[0], titulo)
                mycursor.execute(sql_insert_emprestimo, val_insert_emprestimo)

                # Atualizar o status do livro para indisponível
                sql_update_status = "UPDATE livros SET status_ = 0 WHERE titulo = %s"
                mycursor.execute(sql_update_status, (titulo,))

                mydb.commit()
                print("Livro emprestado com sucesso!")
            except Exception as e:
                print("Erro ao emprestar livro:", e)
        else:
            print("Livro não disponível para empréstimo.")
    else:
        print("Você precisa fazer login para emprestar um livro.")

    mycursor.close()



def give_back(mydb, user, titulo):
    mycursor = mydb.cursor()

    livro = Livro(titulo, "", "")  # Criar um objeto Livro apenas com o título

    # Verifica se o usuário está logado
    if user:
        # Verificar se o livro foi emprestado pelo usuário
        sql_check_emprestimo = "SELECT id_emprestimo FROM emprestimos WHERE id_usuario = %s AND id_livro = (SELECT id_livro FROM livros WHERE titulo = %s)"
        val_check_emprestimo = (user[0], titulo)
        mycursor.execute(sql_check_emprestimo, val_check_emprestimo)
        emprestimo = mycursor.fetchone()

        if emprestimo:  # Se o livro foi emprestado pelo usuário
            try:
                # Remover o registro de empréstimo
                sql_delete_emprestimo = "DELETE FROM emprestimos WHERE id_usuario = %s AND id_livro = (SELECT id_livro FROM livros WHERE titulo = %s)"
                mycursor.execute(sql_delete_emprestimo, val_check_emprestimo)

                # Atualizar o status do livro para disponível
                sql_update_status = "UPDATE livros SET status_ = 1 WHERE titulo = %s"
                mycursor.execute(sql_update_status, (titulo,))

                mydb.commit()
                print("Livro devolvido com sucesso!")
            except Exception as e:
                print("Erro ao devolver livro:", e)
        else:
            print("Você não pode devolver este livro, pois não o emprestou.")
    else:
        print("Você precisa fazer login para devolver um livro.")

    mycursor.close()
