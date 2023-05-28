#Abaixo está a definição das classes que representam os autômatos finitos não determinísticos e determinísticos. 
class NFA:
    def __init__(self):
        self.states = []
        self.alphabet = []
        self.transitions = {}
        self.start_state = None
        self.final_states = set()

    def add_state(self, state):
        self.states.append(state)

    def add_symbol(self, symbol):
        self.alphabet.append(symbol)

    def add_transition(self, state, symbol, next_states):
        if (state, symbol) not in self.transitions:
            self.transitions[(state, symbol)] = set()
        self.transitions[(state, symbol)].update(next_states)

    def set_start_state(self, state):
        self.start_state = state

    def add_final_state(self, state):
        self.final_states.add(state)


class DFA:
    def __init__(self):
        self.states = []
        self.alphabet = []
        self.transitions = {}
        self.start_state = None
        self.final_states = set()

    def add_state(self, state):
        self.states.append(state)

    def add_symbol(self, symbol):
        self.alphabet.append(symbol)
    def add_transition(self, states, symbol, next_states):
        transition_key = (frozenset(states), symbol)
        transition_value = frozenset(next_states)
        self.transitions[transition_key] = transition_value

    def set_start_state(self, state):
        self.start_state = state

    def add_final_state(self, state):
        stateF = frozenset(state)
        self.final_states.add(stateF)


#FUNÇÕES AUXILARES QUE AJUDARÃO NA CONSTRUÇÃO DO ALGORÍTIMO DE TRANSFORMAÇÃO DE NFA PARA DFA
def Closure(state, nfa):
    ClosureSet = set()
    ClosureSet.add(state)
    for transition in nfa.transitions.items():
        if (transition[0][0] == state and transition[0][1] == ""):
            for destino in transition[1]:
                value = destino
                ClosureSet.add(value)
                ClosureSet = ClosureSet | Closure(value, nfa)
    return ClosureSet

def Edge(state, symbol, nfa):
    EdgeSet = set()
    for transition in nfa.transitions.items():
        if (transition[0][0] == state and transition[0][1] == str(symbol)):
            value = tuple(transition[1])[0]
            EdgeSet.add(value)
            EdgeSet = EdgeSet | Closure(value, nfa)
    return EdgeSet


#ALGORÍTIMO DE TRANSFORMAÇÃO DE NFA PARA DFA
def NFA_TO_DFA(nfa):
    dfa = DFA()
    estadosNaoProcessados = []
    simboloInicial = nfa.start_state
    dfa.set_start_state(Closure(simboloInicial, nfa))
    estadosNaoProcessados.append(Closure(simboloInicial, nfa))
    while len(estadosNaoProcessados) != 0:
        estadoAtual = estadosNaoProcessados.pop(0)
        if estadoAtual not in dfa.states:
            dfa.add_state(estadoAtual)

        for estado in estadoAtual:
            if estado in nfa.final_states:
                dfa.add_final_state(estadoAtual)
                break
        
        for symbol in nfa.alphabet:
            proximosEstados = set()
            for estado in estadoAtual:
                proximosEstados |= Edge(estado, symbol, nfa)
            if proximosEstados:
                if proximosEstados not in dfa.states:
                    dfa.add_state(proximosEstados)
                    estadosNaoProcessados.append(proximosEstados)
                dfa.add_transition(estadoAtual, symbol, proximosEstados)
    return dfa

def to_CSV(dfa):
    file = open("saidaQ3.csv", "w")

    alphabet = "Alfabeto;"
    for symbol in dfa.alphabet:
        if (symbol == dfa.alphabet[-1]):
            alphabet += symbol
        else:
            alphabet += symbol + ","
    file.write(alphabet)
    file.write("\n")

    states = ""
    for symbol in dfa.states:
        if (symbol == dfa.states[-1]):
            states += "q"+str(symbol)
        else:
            states += "q"+str(symbol)+","
    states = "S;"+states
    file.write(states)
    file.write("\n")

    file.write("S0;"+ "q"+str(dfa.start_state))
    file.write("\n")

    final = ""    


    lista_final = list(dfa.final_states)
    for destino in lista_final:

        destino_str = str(set(destino))
        destino_str = destino_str.strip("{}")

        if (destino == lista_final[-1]):
            final += "q"+destino_str
        else:
            final += "q"+destino_str+","

    final_states = "F;"+final
    file.write(final_states)
    file.write("\n")
    file.write("\n")

    file.write("IDENTIFICADORES:")
    file.write("\n")
    for estado in identificadoresDFA:
        id_str = "q"+str(estado[0]) + ";" + estado[1]        
        file.write(id_str)
        file.write("\n")
    file.write("\n")
    file.write("\n")

    for transition in dfa.transitions.items():
        for elemento in transition[1]:
            symbol = transition[0][1]
            
            origem = str(set(transition[0][0]))
            origem = origem.strip("{}")

            stringCompleta = ("q"+origem + ";" + symbol +";"+ "q"+str(elemento))
            file.write(stringCompleta)
            file.write("\n")
    file.close()
#CRIAMOS ENTÃO UM NFA COM AS INFORMAÇÕES DA QUESTÃO Q2 
nfa = NFA()



import q2

transitions = q2.exportTransitions
alphabet = q2.exportAlphabet
states = q2.exportStates
start_state = q2.exportStartState
final_states = q2.exportFinalStates
identificadores = q2.exportIdentificadores

# print("Transições",transitions)
# print("Simbolos",alphabet)
# print("Estados",states)
# print("Estado inicial",start_state)
# print("Estados finais",final_states)



nfa.transitions = transitions
nfa.alphabet = alphabet

for state in states:
    nfa.add_state(state)

nfa.start_state = start_state

for state in final_states:
    nfa.add_final_state(state)

# print("NFA")
# print ("Transições",nfa.transitions)
# print ("Simbolos",nfa.alphabet)
# print ("Estados",nfa.states)
# print ("Estado inicial",nfa.start_state)
# print ("Estados finais",nfa.final_states)
# print("\n")

dfa = NFA_TO_DFA(nfa)

# print("DFA")
# print ("Transições",dfa.transitions)
# print ("Simbolos",dfa.alphabet)
# print ("Estados",dfa.states)
# print ("Estado inicial",dfa.start_state)
# print ("Estados finais",dfa.final_states)
# print("\n")

DFAsimplificado = DFA()
dicionario = {}



def buscar_chave_por_valor(dicionario, valor):
    for chave, v in dicionario.items():
        if v == valor:
            return chave
    return None


for i in range(1, len(dfa.states)+1):
    dicionario[i] = dfa.states[i-1]

for state in dfa.states:
    DFAsimplificado.add_state(buscar_chave_por_valor(dicionario, state))

for transition in dfa.transitions.items():
        origem = set()
        destino = set()
        origem.add(buscar_chave_por_valor(dicionario, transition[0][0]))
        destino.add(buscar_chave_por_valor(dicionario, transition[1]))
        DFAsimplificado.add_transition(origem, transition[0][1], destino)

for final in dfa.final_states:
    state = set()
    state.add(buscar_chave_por_valor(dicionario, final))
    DFAsimplificado.add_final_state(state)


for symbol in nfa.alphabet:
    DFAsimplificado.add_symbol(symbol)

DFAsimplificado.set_start_state(buscar_chave_por_valor(dicionario, dfa.start_state))

identificadoresDFA = []
for identificador in identificadores:
    for state in dfa.states:
        if identificador[0] in state:
            identificadoresDFA.append((buscar_chave_por_valor(dicionario, state), identificador[1]))


to_CSV(DFAsimplificado)

exportTransitions = DFAsimplificado.transitions
exportFinalStates = DFAsimplificado.final_states
exportStartState = DFAsimplificado.start_state
exportIdentificadores = identificadoresDFA

#salvar dados para não precisar rodar o algoritmo novamente
file = open("dados.txt", "w")
file.write("exportTransitions = ")
file.write(str(exportTransitions))
file.write("\n")
file.write("exportFinalStates = ")
file.write(str(exportFinalStates))
file.write("\n")
file.write("exportStartState = ")
file.write(str(exportStartState))
file.write("\n")
file.write("exportIdentificadores = ")
file.write(str(exportIdentificadores))
file.close()


























# for transition in DFAsimplificado.transitions.items():
#     origem = (set(transition[0][0]))
#     simbolo = (transition[0][1])
#     destino = (set(transition[1]))

#     string =  ''.join(map(str,set(origem))) + "," + str(simbolo) + ","+''.join(map(str,set(destino))) + "\n"
#     file = open("transitions.txt", "a")
#     file.write(string)
#     file.close()

# for final in DFAsimplificado.final_states:
#     file = open("finals.txt", "a")
#     file.write(''.join(map(str,set(final))))
#     file.write("\n")
#     file.close()
