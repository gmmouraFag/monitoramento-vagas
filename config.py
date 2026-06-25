"""
Arquivo de configuração para o sistema de detecção de vagas
"""

# Configurações de Vaga
LARGURA_VAGA = 107
ALTURA_VAGA = 48

# Configurações de Detecção
LIMIAR_VAGA_LIVRE = 900  # Ajuste este valor conforme necessário

# Configurações de Processamento de Imagem
BLUR_KERNEL = (3, 3)
BLUR_SIGMA = 1
ADAPTIVE_THRESHOLD_BLOCK_SIZE = 25
ADAPTIVE_THRESHOLD_C = 16
MEDIAN_BLUR_SIZE = 5
DILATE_ITERATIONS = 1

# Configurações de Visualização
COR_VAGA_LIVRE = (0, 255, 0)      # Verde
COR_VAGA_OCUPADA = (0, 0, 255)    # Vermelho
ESPESSURA_BORDA = 2

# Caminhos de Arquivo
CAMINHO_VIDEO = "../videos/estacionamento.mp4"
CAMINHO_IMAGEM = "../images/estacionamento.jpg"
CAMINHO_DADOS = "../data/vagas.pkl"
