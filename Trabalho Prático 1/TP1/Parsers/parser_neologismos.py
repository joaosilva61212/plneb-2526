import json
import re

def extrair_novo_formato(caminho_txt, caminho_json):
    with open(caminho_txt, "r", encoding="latin-1", errors="replace") as f:
        linhas = f.readlines()

    resultado = []
    i = 0
    total_linhas = len(linhas)

    while i < total_linhas:
        linha = linhas[i].strip()

        #Identificar o início de um termo: contém " s.f." ou " s.m."
        match_genero = re.search(r'\s+(s\.f\.|s\.m\.)', linha)
        
        if match_genero:
            # Separar a palavra da informação gramatical
            palavra = linha[:match_genero.start()].strip()
            genero = match_genero.group(1).strip()
            
            i += 1
            ingles = "n.d."
            espanhol = "n.d."
            
            #Verificar a linha de traduções
            if i < total_linhas:
                linha_trad = linhas[i].strip()
                if "[ing]" in linha_trad or "[esp]" in linha_trad:
                    #Separa por ";" e limpar as tags
                    partes = linha_trad.split(';')
                    for parte in partes:
                        if "[ing]" in parte:
                            ingles = parte.replace("[ing]", "").strip()
                        if "[esp]" in parte:
                            espanhol = parte.replace("[esp]", "").strip()
                    i += 1 
                else:
                    pass
            
            #Apanhar o bloco de definição
            definicao_linhas = []
            while i < total_linhas:
                prox_linha = linhas[i].strip()
                
                # Critério de paragem 1: Encontrar uma linha completamente vazia
                if prox_linha == "":
                    break
                
                # Critério de paragem 2: Encontrar o próximo termo (outro s.f. ou s.m.)
                if re.search(r'\s+(s\.f\.|s\.m\.)', prox_linha):
                    i -= 1 
                    break
                    
                definicao_linhas.append(prox_linha)
                i += 1
            
            resultado.append({
                "indice": str(len(resultado) + 1),
                "palavra": palavra,
                "info_gramatical": genero,
                "traducoes": {
                    "ingles": ingles,
                    "espanhol": espanhol
                },
                "definicao": " ".join(definicao_linhas)
            })
        else:
            i += 1

    #Guardar json
    with open(caminho_json, "w", encoding="utf-8") as f:
        json.dump(resultado, f, ensure_ascii=False, indent=4)

    print(f"Extração concluída com sucesso!")
    print(f"Foram encontrados {len(resultado)} conceitos.")

extrair_novo_formato("Textos/texto_neologismos.txt", "Dicionarios/dicionario_neologismos.json")