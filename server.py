# Lado passivo/server

import socket

HOST = ''     # '' possibilita acessar qualquer endereco alcancavel da maquina local
PORTA = 5000  # porta onde chegarao as mensagens para essa aplicacao

def word_count(string):
    """ Metodo para contar as ocorrencias de cada palavra em um determinado texto """
    result = {}
    unique_words = set(string.split())
    for word in unique_words:
        # errado, usar regex e dar match nos espacos em volta
        # pois ira contar palavras dentro de outras palavras
        result[word] = string.count(word)
    return result

def high_words(counted, i=1):
    # ordena o dicionario por valor
    # pega os i primeiros em uma lista de tuplas
    # e retorna apenas uma lista com as chaves
    return dict(sorted(x.items(), key=lambda item: item[1])[:i]).keys()

def read_file(filename):
    # realiza a leitura do arquivo
    with open(filename, "r") as f:
        return f.read()

def main():

    # inicializa o servidor
    with socket.create_server((HOST, PORTA)) as s:
        s.listen(1)
        print(f"Server started, listening on port {PORTA}")

        while True:
            # Aguarda uma nova conexao
            conn, addr = s.accept()
            with conn:
                # Informa quem conectou
                print("Accepted connection from", addr)

                # Recebe os dados enviados pelo cliente
                data = conn.recv(1024)
                if not data:
                    break

                try:
                    # tenta realizar a leitura do arquivo
                    contents = read_file(str(data,  encoding='utf-8'));
                    # se der certo, conta as palavras e envia o resultado pro cliente
                    conn.sendall(", ".join(high_words(word_count(contents), 5)))
                except:
                    # se der errado, envia para o cliente uma string vazia
                    conn.sendall("")

main()