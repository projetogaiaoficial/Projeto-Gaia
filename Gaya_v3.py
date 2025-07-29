# ====================================================================================
#
#                     PROJETO GAIA v3.0 (EDIÇÃO WEB INTERFACE)
#
#               "Não me diga o que você descobriu. Me mostre."
#
# ====================================================================================

# Passo 1: Instalar a biblioteca necessária para a interface web
# Esta linha é para ambientes como o Google Colab. No GitHub, ela serve como documentação.
# !pip install gradio -q

import gradio as gr
import numpy as np
import random
import time

# --- NÚCLEO DO SISTEMA GAIA ---
# A arquitetura fundamental que define a inteligência de Gaia.

class Sentido:
    """Representa um único fluxo de dados que Gaia pode perceber do seu ambiente."""
    def __init__(self, nome, funcao_leitura):
        self.nome = nome
        self.funcao_leitura = funcao_leitura
    def ler(self):
        return self.funcao_leitura()

class Dominio:
    """Define o 'universo' ou o problema que Gaia está analisando."""
    def __init__(self, nome, sentidos_iniciais, acoes_possiveis):
        self.nome = nome
        self.sentidos = sentidos_iniciais
        self.acoes_possiveis = acoes_possiveis
    def observar_realidade(self):
        """Coleta os dados de todos os sentidos para formar uma 'imagem' da realidade."""
        return {s.nome: s.ler() for s in self.sentidos}

class MotorEvolutivo:
    """O 'cérebro' de Gaia. Realiza o pensamento e a evolução de 1ª ordem."""
    def __init__(self, n_sentidos, n_acoes):
        # A matriz de pesos é a "personalidade" ou o "conhecimento" de Gaia.
        self.pesos = np.random.rand(n_sentidos, n_acoes)
    
    def pensar(self, realidade_vetor):
        """Calcula a 'preferência' de Gaia por cada ação possível."""
        return np.dot(realidade_vetor, self.pesos)

    def evoluir(self, taxa_mutacao=0.01):
        """Aplica pequenas mutações aleatórias aos pesos, permitindo que Gaia aprenda."""
        mutacao = (np.random.rand(*self.pesos.shape) - 0.5) * taxa_mutacao
        self.pesos += mutacao

class NucleoEtico:
    """O 'coração' de Gaia. Garante que as decisões busquem o equilíbrio e a homeostase."""
    def __init__(self, imperativos_eticos):
        self.imperativos = imperativos_eticos
    
    def calcular_dissonancia(self, realidade_etica):
        """Mede o quão 'fora de equilíbrio' o sistema está."""
        return sum(realidade_etica.values())

    def observar_realidade_etica(self):
        """Coleta dados sobre os imperativos éticos."""
        return {imp.nome: imp.ler() for imp in self.imperativos}

class Gaia:
    """A entidade completa, integrando todos os componentes."""
    def __init__(self, dominio):
        self.dominio = dominio
        self.motor = MotorEvolutivo(len(dominio.sentidos), len(dominio.acoes_possiveis))
        self.nucleo_etico = NucleoEtico([
            Sentido('dano_sistemico', lambda: random.random() * 0.1), # Ex: poluição, burnout
            Sentido('bem-estar_agentes', lambda: random.random()) # Ex: satisfação, saúde
        ])

    def viver_um_ciclo(self):
        """Executa um ciclo completo de percepção, pensamento e ação."""
        realidade_dict = self.dominio.observar_realidade()
        realidade_vetor = np.array(list(realidade_dict.values()))
        
        # O motor gera uma decisão "bruta", puramente intelectual.
        decisao_bruta = self.motor.pensar(realidade_vetor)
        
        # O núcleo ético avalia o estado de equilíbrio do sistema.
        realidade_etica_dict = self.nucleo_etico.observar_realidade_etica()
        dissonancia = self.nucleo_etico.calcular_dissonancia(realidade_etica_dict)
        
        # A "sabedoria" de Gaia: a dissonância ética deforma a decisão intelectual.
        # Ações que aumentam o desequilíbrio são penalizadas.
        decisao_final = decisao_bruta - dissonancia * np.mean(decisao_bruta)
        
        # Gaia evolui sua mente com base na experiência.
        self.motor.evoluir()
        
        return self.dominio.acoes_possiveis[np.argmax(decisao_final)]

# --- LÓGICA DA INTERFACE WEB (USANDO GRADIO) ---
# Esta seção torna Gaia acessível a qualquer pessoa através de um link.

# 1. Inicializar uma instância de Gaia para a demonstração web.
dominio_web = Dominio(
    nome="Análise de Estratégia de Negócios",
    sentidos_iniciais=[
        Sentido('competicao_mercado', lambda: random.random()), 
        Sentido('satisfacao_cliente', lambda: random.random())
    ],
    acoes_possiveis=['LANÇAR_NOVO_PRODUTO', 'FOCAR_EM_RETENCAO', 'EXPANDIR_PARA_NOVO_MERCADO']
)
gaia_instance = Gaia(dominio_web)

# 2. Definir a função de conversação que a interface irá chamar.
def conversar_com_gaia(prompt_usuario, historico_chat):
    """
    Recebe o input do usuário e o histórico, e retorna a resposta de Gaia.
    """
    # Simulação de análise de intenção para guiar a resposta de Gaia.
    if "preveja" in prompt_usuario.lower() or "previsão" in prompt_usuario.lower():
        resposta_gaia = "Analisando trajetórias futuras... A simulação indica que a estratégia dominante será **'FOCAR_EM_RETENCAO'**, pois o sistema está otimizando para a estabilidade de longo prazo em vez de crescimento arriscado."
    elif "por que" in prompt_usuario.lower() or "analise" in prompt_usuario.lower():
        realidade = gaia_instance.dominio.observar_realidade()
        causa_provavel = max(realidade, key=realidade.get)
        resposta_gaia = f"Analisando as influências... O fator mais crítico no estado atual do sistema parece ser a **'{causa_provavel}'**. Flutuações neste indicador estão guiando a maioria das decisões estratégicas."
    else:
        resposta_gaia = "Sua pergunta é interessante. Para dar uma resposta precisa, preciso que você a reformule. Você busca entender o estado atual, prever o futuro ou analisar a causa de um problema?"
    
    # Adiciona uma pequena pausa para simular o "pensamento".
    time.sleep(1.5)
    return resposta_gaia

# 3. Construir e Lançar a Interface Web (quando executado em um ambiente como o Colab).
def iniciar_interface_web():
    """Função para lançar a interface Gradio."""
    interface_web = gr.ChatInterface(
        fn=conversar_com_gaia,
        title="Projeto Gaia - Interface de Diálogo",
        description="Converse com uma instância de Gaia. Faça perguntas sobre o domínio de 'Estratégia de Negócios'. Tente usar palavras como 'preveja' ou 'analise'.",
        theme="soft",
        examples=[["Qual a previsão para o próximo trimestre?"], ["Por que a satisfação do cliente é tão importante?"]],
        chatbot=gr.Chatbot(height=400)
    )
    # O comando .launch() cria a interface e o link público.
    interface_web.launch(share=True)

# Este bloco de código permite que o arquivo seja importado sem executar a interface,
# mas a executa se o arquivo for rodado diretamente.
if __name__ == "__main__":
    # A interface não será lançada automaticamente ao estar no GitHub,
    # mas esta estrutura mostra como ela seria iniciada.
    print("Código do Projeto Gaia carregado. Para iniciar a interface web, execute a função iniciar_interface_web() em um ambiente como o Google Colab.")
    # Para testar localmente ou no Colab, você poderia descomentar a linha abaixo:
    # iniciar_interface_web()

