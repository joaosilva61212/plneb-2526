import json
import re

def extrair_dicionario_por_categorias(caminho_txt, caminho_json):
    with open(caminho_txt, 'r', encoding='latin-1', errors='replace') as f:
        linhas_brutas = f.readlines()

    #Limpeza do ficheiro
    linhas_limpas = []
    for linha in linhas_brutas:
        l = linha.strip()
        if not l: continue
        
        if l.isdigit(): continue # Remove números de página puros
        if len(l) == 1 and l.isalpha(): continue # Remove letras de índice
        if re.match(r'^\d+\s+[A-Z]+$', l): continue # Remove cabeçalhos estranhos (ex: "16 ACI")
        if l.startswith("Ver ") and l.endswith("."): continue  # Remove referências
        
        linhas_limpas.append(l)

    indices_categorias = [i for i, linha in enumerate(linhas_limpas) if linha.startswith("Categoria:")]
    blocos = []
    
    # 3. EXTRAIR O TERMO (PALAVRA) PARA CADA CATEGORIA
    for i, idx_cat in enumerate(indices_categorias):
        categoria = linhas_limpas[idx_cat].replace("Categoria:", "").strip()
        
        # Andar para trás para encontrar as linhas da palavra
        # O limite é bater na linha que acabe em ponto final "." (fim da definição anterior)
        linhas_palavra = []
        j = idx_cat - 1
        while j >= 0:
            # Se a linha anterior terminar com ponto final, significa que entrámos na definição do termo anterior
            if j < idx_cat - 1 and linhas_limpas[j].endswith('.'):
                break
            linhas_palavra.insert(0, linhas_limpas[j])
            j -= 1
            
        inicio_palavra = j + 1
        palavra = " ".join(linhas_palavra)
        
        blocos.append({
            "idx_cat": idx_cat,
            "inicio_palavra": inicio_palavra,
            "palavra": palavra,
            "categoria": categoria
        })

    resultado = []

    #Extrair definição
    for i, bloco in enumerate(blocos):
        linha_inicio_def = bloco["idx_cat"] + 1
        if i + 1 < len(blocos):
            linha_fim_def = blocos[i+1]["inicio_palavra"]
        else:
            linha_fim_def = len(linhas_limpas) 
        texto_definicao = " ".join(linhas_limpas[linha_inicio_def:linha_fim_def]).strip()
        
        resultado.append({
            "indice": str(i + 1),
            "palavra": bloco["palavra"],
            "categoria": bloco["categoria"],
            "definicao": texto_definicao
        })

    #Guardar json
    with open(caminho_json, 'w', encoding='utf-8') as f:
        json.dump(resultado, f, ensure_ascii=False, indent=4)

    print(f"Nova estrutura dominada! Foram extraídos {len(resultado)} conceitos com categoria.")

extrair_dicionario_por_categorias("Textos/texto_ms.txt", "Dicionarios/dicionario_categorias.json")