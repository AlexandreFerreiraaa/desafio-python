from getpass import getpass
import os
from Crypto.Cipher import AES
from Crypto.Protocol.KDF import scrypt
from Crypto.Random import get_random_bytes

def obter_senha():
    senha = getpass("Digite a senha para criptografia: ")
    return senha

def acessar_pasta(caminho_pasta):
    arquivos = []
    for nome_arquivo in os.listdir(caminho_pasta):
        caminho_arquivo = os.path.join(caminho_pasta, nome_arquivo)
        if os.path.isfile(caminho_arquivo):
            arquivos.append(caminho_arquivo)
    return arquivos

def criptografar_arquivo(arquivo, senha):
    chave = scrypt(senha.encode(), b'salt', dklen=32, N=2**14, r=8, p=1)  # Gerando a chave AES a partir da senha
    iv = get_random_bytes(16)  # Vetor de inicialização
    cipher = AES.new(chave, AES.MODE_CBC, iv)

    with open(arquivo, 'rb') as f:
        dados = f.read()

    # Adiciona padding para garantir que os dados sejam múltiplos de 16 bytes
    padding = 16 - len(dados) % 16
    dados = dados + bytes([padding]) * padding

    dados_criptografados = cipher.encrypt(dados)

    return iv + dados_criptografados

def salvar_arquivo_criptografado(arquivo_criptografado, caminho_backup, nome_arquivo):
    caminho_salvo = os.path.join(caminho_backup, nome_arquivo + '.enc')
    with open(caminho_salvo, 'wb') as f:
        f.write(arquivo_criptografado)

def descriptografar_arquivo(arquivo_criptografado, senha):
    chave = scrypt(senha.encode(), b'salt', dklen=32, N=2**14, r=8, p=1)  # Gerando a chave AES a partir da senha
    iv = arquivo_criptografado[:16]  # O vetor de inicialização está nos primeiros 16 bytes
    dados_criptografados = arquivo_criptografado[16:]

    cipher = AES.new(chave, AES.MODE_CBC, iv)
    dados_descriptografados = cipher.decrypt(dados_criptografados)

    # Remove o padding
    padding = dados_descriptografados[-1]
    dados_descriptografados = dados_descriptografados[:-padding]

    return dados_descriptografados

def main():
    # Entrada da senha
    senha = obter_senha()

    # Acesso à pasta original
    pasta_origem = input("Digite o caminho da pasta com os arquivos a serem criptografados: ")
    arquivos = acessar_pasta(pasta_origem)

    # Criação da pasta de backup
    pasta_backup = input("Digite o caminho da pasta onde os arquivos criptografados serão salvos: ")
    if not os.path.exists(pasta_backup):
        os.makedirs(pasta_backup)

    # Criptografia dos arquivos
    for arquivo in arquivos:
        print(f"Criptografando: {arquivo}")
        arquivo_criptografado = criptografar_arquivo(arquivo, senha)
        salvar_arquivo_criptografado(arquivo_criptografado, pasta_backup, os.path.basename(arquivo))
        print(f"Arquivo criptografado salvo em: {pasta_backup}/{os.path.basename(arquivo)}.enc")

    # Descriptografando um arquivo
    arquivo_para_descriptografar = input("Digite o caminho de um arquivo criptografado para descriptografar: ")
    with open(arquivo_para_descriptografar, 'rb') as f:
        arquivo_criptografado = f.read()

    dados_descriptografados = descriptografar_arquivo(arquivo_criptografado, senha)
    caminho_original = input("Digite o caminho onde deseja salvar o arquivo descriptografado: ")
    with open(caminho_original, 'wb') as f:
        f.write(dados_descriptografados)

    print(f"Arquivo descriptografado salvo em: {caminho_original}")

if __name__ == "__main__":
    main()

def acessar_pasta(caminho_pasta):
    print(f"Verificando a pasta: {caminho_pasta}")  # Adicionando print para verificar o caminho
    arquivos = []
    if not os.path.exists(caminho_pasta):  # Verificando se o caminho existe
        print(f"A pasta {caminho_pasta} não existe.")
        return arquivos

    for nome_arquivo in os.listdir(caminho_pasta):
        caminho_arquivo = os.path.join(caminho_pasta, nome_arquivo)
        if os.path.isfile(caminho_arquivo):
            arquivos.append(caminho_arquivo)
    return arquivos
