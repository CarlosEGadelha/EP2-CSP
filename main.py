from satisfacao_restricoes import Restricao, SatisfacaoRestricoes
import math

# Dicionário de todas as equipes
# equipe = {
#   "Campos FC": {"cidade": "Campos", "torcedores": 23},
#   "Guardiões FC": {"cidade": "Guardião", "torcedores": 40},
#   "CA Protetores": {"cidade": "Guardião", "torcedores": 20},
#   "SE Leões": {"cidade": "Leão", "torcedores": 40},
#   "Simba FC": {"cidade": "Leão", "torcedores": 15},
#   "SE Granada": {"cidade": "Granada", "torcedores": 10},
#   "CA Lagos": {"cidade": "Lagos", "torcedores": 20},
#   "Solaris RC": {"cidade": "Ponte-do-Sol", "torcedores": 30},
#   "Porto EC": {"cidade": "Porto", "torcedores": 45},
#   "Ferroviária EC": {"cidade": "Campos", "torcedores": 38},
#   "Portuários AA": {"cidade": "Porto", "torcedores": 12},
#   "CA Azedos": {"cidade": "Limões", "torcedores": 18},
#   "SE Escondidos": {"cidade": "Escondidos", "torcedores": 50},
#   "Secretos FC": {"cidade": "Escondidos", "torcedores": 25}
# }

# Dicionário reduzido para teste
equipe = {
  "Campos FC": {"cidade": "Campos", "torcedores": 23},
  "Guardiões FC": {"cidade": "Guardião", "torcedores": 40},
  "CA Protetores": {"cidade": "Guardião", "torcedores": 20},
  "SE Leões": {"cidade": "Leão", "torcedores": 40},
  "SE Granada": {"cidade": "Granada", "torcedores": 10},
  "CA Lagos": {"cidade": "Lagos", "torcedores": 20},
}


RODADAS = (len(equipe)-1) * 2
JOGOS = int(len(equipe)/2)
NUM_CLASSICOS = math.ceil(len(equipe)/3)
# NUM_CLASSICOS = 5
# gera combinação de todos os jogos

combinacao_de_todos_jogos = []
for e1 in equipe.keys():
  for e2 in equipe.keys():
    # # remove jogos com o mesmo time
    if e1 != e2:
      combinacao_de_todos_jogos.append((e1, e2))

# ---------------------------- [ Restricao 2 ] ---------------------------- #
      
# Dica 1: Fazer Restrições Genéricas
class UmTimePorRodadaRestricao(Restricao):
  def __init__(self,variaveis):
    super().__init__(variaveis)

  # atribuicao = {"variavel1": "valor1", "variavel2": "valor2", ...}
  def esta_satisfeita(self, atribuicao):
    rodadas = {}
    for i in range(RODADAS): # rodadas
      rodadas["R" + str(i)] = []

    for variavel in atribuicao.keys():
      rodada = variavel[0:2]
      times = atribuicao[variavel]
      if times is not None:
        time1 = times[0]
        time2 = times[1]
        if time1 in rodadas[rodada] or time2 in rodadas[rodada]:
          return False
        else:
          rodadas[rodada].append(time1)
          rodadas[rodada].append(time2)
    return True

# ---------------------------- [ Restricao 1 ] ---------------------------- #

class TurnoReturnoRestricao(Restricao):
  def __init__(self,variaveis):
    super().__init__(variaveis)

  # atribuicao = {"variavel1": "valor1", "variavel2": "valor2", ...}
  def esta_satisfeita(self, atribuicao):
    rodadas = {}
    for i in range(RODADAS): # rodadas
      rodadas["R" + str(i)] = []

    for variavel in atribuicao.keys():
      for i in range(RODADAS):
        rodada = "R" + str(i)
        times = atribuicao[variavel]
        if times is not None:
          if times in rodadas[rodada]:
            return False
          else:
            rodadas[rodada].append(times)
    return True

# ---------------------------- [ Restricao 3 ] ---------------------------- #

class MesmaCidadeRestricao(Restricao):
  def __init__(self,variaveis):
    super().__init__(variaveis)

  # atribuicao = {"variavel1": "valor1", "variavel2": "valor2", ...}
  def esta_satisfeita(self, atribuicao):
    rodadas = {}
    cidades = {}
    for i in range(RODADAS): # rodadas
      rodadas["R" + str(i)] = []
      cidades["R" + str(i)] = []

    for variavel in atribuicao.keys():
      rodada = variavel[0:2]
      times = atribuicao[variavel]
      if times is not None:
        time1 = times[0]
        if times in rodadas[rodada] or equipe[time1]["cidade"] in cidades[rodada]:
          return False
        else:
          cidades[rodada].append(equipe[time1]["cidade"])
          rodadas[rodada].append(times)
    return True


# ---------------------------- [ Restricao 4 ] ---------------------------- #

class ClassicosRestricoes(Restricao):
  def __init__(self,variaveis):
    super().__init__(variaveis)

  # atribuicao = {"variavel1": "valor1", "variavel2": "valor2", ...}
  def esta_satisfeita(self, atribuicao):
    rodadas = {}
    classicos = {}
    torcedores = []
    mais_torcedores = []

    for i in equipe:
      torcedores.append(equipe[i]["torcedores"])

    torcedores.sort(reverse = True)

    for i in range(NUM_CLASSICOS):
      mais_torcedores.append(torcedores[i])
    
    for i in range(RODADAS): # rodadas
      rodadas["R" + str(i)] = []
      classicos["R" + str(i)] = []

    for variavel in atribuicao.keys():
      rodada = variavel[0:2]
      times = atribuicao[variavel]
      if times is not None:
        if equipe[times[0]]["torcedores"] in mais_torcedores and equipe[times[1]]["torcedores"] in mais_torcedores:
          if classicos[rodada]:
            return False 
          else:
            rodadas[rodada].append(times)
            classicos[rodada].append(True)
    return True

    
    
if __name__ == "__main__":
    variaveis = []
    for i in range(RODADAS): # rodadas
      for j in range(JOGOS): # jogos
        # Variável RnJm, tal que n é o número da rodada e m é o jogo da rodada
        variaveis.append("R" + str(i) + "J" + str(j))
      
    dominios = {}
    for variavel in variaveis:
        # o domínio são as combinações de todos os possívels jogos
        dominios[variavel] = combinacao_de_todos_jogos
    
    problema = SatisfacaoRestricoes(variaveis, dominios)
    problema.adicionar_restricao(UmTimePorRodadaRestricao(variaveis))
    problema.adicionar_restricao(TurnoReturnoRestricao(variaveis))
    problema.adicionar_restricao(MesmaCidadeRestricao(variaveis))
    problema.adicionar_restricao(ClassicosRestricoes(variaveis))
    
    resposta = problema.busca_backtracking()
  
    if resposta is None:
      print("Nenhuma resposta encontrada")
    else:
      for i in range(RODADAS): # rodadas
        print("\n---------- Rodada " + str(i+1) + " ----------\n")
        for j in range(JOGOS): # jogos
          jogo = resposta["R" + str(i) + "J" + str(j)]
          print("Jogo " + str(j+1) + ": " + jogo[0] + " x " + jogo[1] + "\tCidade: " + equipe[jogo[0]]["cidade"])