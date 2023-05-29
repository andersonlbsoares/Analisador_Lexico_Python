import ast

class DFA:
    def __init__(self):
        self.states = []
        self.alphabet = set()
        self.transitions = {}
        self.start_state = None
        self.final_states = set()

    def add_state(self, state):
        self.states.append(state)

    def add_symbol(self, symbol):
        self.alphabet.add(symbol)

    def add_transition(self, states, symbol, next_states):
        self.transitions[(states), symbol] = next_states

    def set_start_state(self, state):
        self.start_state = state

    def add_final_state(self, state):
        self.final_states.add(state)
    

def is_accepted(dfa, input_string):
    current_state = dfa.start_state

    for symbol in input_string:
        for transition in dfa.transitions:
            if transition[0] == current_state and transition[1] == symbol:
                current_state = dfa.transitions[transition]
                break
        else:
            return (current_state,False)
        
    return (current_state in dfa.final_states, current_state)

def remover_caracteres(string, caracteres):
    nova_string = ""
    for char in string:
        if char not in caracteres:
            nova_string += char
    return nova_string

dfa = DFA()


file = open("dados.txt", "r")
contents = file.read()
file.close()

exportTransitions = contents.split("exportTransitions = ")[1].split("\n")[0]
exportFinalStates = contents.split("exportFinalStates = ")[1].split("\n")[0]
exportStartState = contents.split("exportStartState = ")[1].split("\n")[0]
exportIdentificadores = contents.split("exportIdentificadores = ")[1].split("\n")[0]



transitions = {}
dfa.start_state = int(exportStartState)
identificadores = ast.literal_eval(exportIdentificadores)
transitions = eval(exportTransitions)
final_states = exportFinalStates   

caracteres_indesejados = "frozenst(){} "
final_states_att = remover_caracteres(final_states, caracteres_indesejados)
final_states_att = final_states_att.split(',')



for transition in transitions.items():
    origem = str(set(transition[0][0]))
    origem = origem.strip("{}")

    destino = str(set(transition[1]))
    destino = destino.strip("{}")

    dfa.add_transition(origem, transition[0][1], destino)

for final in final_states_att:
    dfa.add_final_state((final))

dfa.set_start_state('1')


#ler entrada do arquivo
file = open("entradaQ4.txt", "r")
entrada = file.read()
file.close()

palavras_e_linhas = []
palavra_atual = ""

for caractere in entrada:
    if caractere == " ":
        if palavra_atual:
            palavras_e_linhas.append(palavra_atual)
            palavra_atual = ""
    elif caractere == "\n":
        if palavra_atual:
            palavras_e_linhas.append(palavra_atual)
            palavra_atual = ""
        palavras_e_linhas.append("\n")
    else:
        palavra_atual += caractere

if palavra_atual:
    palavras_e_linhas.append(palavra_atual)


#saida
file = open("saidaQ4.txt", "w")


for palavra in palavras_e_linhas:
    if palavra == "-":
        palavra = "_"
    elif palavra == "(":
        palavra = "°"
    elif palavra == ")":
        palavra = "^"
    elif palavra == "*":
        palavra = ":"


    resultado = is_accepted(dfa,palavra)
    bool, id = resultado

    if (bool==True):
        ident = []
        for identificador in identificadores:
            if(int(identificador[0]) == int(id)):
                ident.append(str(identificador[1]))
        
        if 'KEYWORD_INT' in ident:
            file.write("KEYWORD_INT ")
        elif 'KEYWORD_STRING' in ident:
            file.write("KEYWORD_STRING ")
        elif 'IF' in ident:
            file.write("IF ")
        elif 'ELSE' in ident:
            file.write("ELSE ")
        elif 'RETURN' in ident:
            file.write("RETURN ")
        elif 'IDENTIFIER' in ident:
            file.write("IDENTIFIER ")
        else:
            file.write(ident[0] + " ")
    elif palavra == "\n":
        file.write("\n")
    else:
        file.write("ERRO ")

print ("Arquivo saidaQ4.txt gerado com sucesso!")