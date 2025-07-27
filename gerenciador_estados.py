class GerenciadorEstados:
    def __init__(self):
        self.estado_atual = None
        self.estados = {}

    def adicionar_estado(self, nome, estado):
        self.estados[nome] = estado

    def mudar_estado(self, nome):
        if self.estado_atual:
            self.estado_atual.sair()
        self.estado_atual = self.estados[nome]
        self.estado_atual.entrar()

    def atualizar(self):
        if self.estado_atual:
            return self.estado_atual.atualizar()
        return False

    def desenhar(self, tela):
        if self.estado_atual:
            self.estado_atual.desenhar(tela)