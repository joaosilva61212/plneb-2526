import json
import re

def extrair_glossario_wipo_blindado(caminho_txt, caminho_json):
    with open(caminho_txt, 'r', encoding='utf-8', errors='ignore') as f:
        linhas_raw = f.readlines()

    #Limpeza 
    linhas = []
    lixo = ['WIPO Pearl', 'COVID-19 Glossary', 'Multilingual Glossary', 'List of abbreviations']
    for l in linhas_raw:
        ls = l.strip()
        if not ls: continue 
        if ls in lixo: continue 
        if len(ls) == 1 and ls.isupper(): continue 
        if ls.isdigit(): continue 
        linhas.append(ls)
        
    inicio = 0
    for i, l in enumerate(linhas):
        if l == "acute respiratory distress syndrome":
            inicio = i
            break
    linhas = linhas[inicio:]

# Encontrar os pilares do documento: As Categorias
    padrao_categoria = re.compile(r'^(MEDI|CHEM|ENVR|SCIE)[,\s]')
    idx_cats = [i for i, l in enumerate(linhas) if padrao_categoria.match(l)]
    
    resultados = []
    #Expressão regular para identificar linhas de traduções
    padrao_lingua = re.compile(r'^(AR|DE|ES|FR|JA|KO|PT|RU|ZH)(?:\s+(.*))?$')
    
    next_term_start = 0
    
    for k in range(len(idx_cats)):
        idx_cat = idx_cats[k]
        categoria = linhas[idx_cat]
        
        # --- PARTE A: TERMO, SINÓNIMO E DEFINIÇÃO ---
        termo = linhas[next_term_start]
        sinonimo = "n.d."
        def_start = next_term_start + 1

        # Verifica se tem sinónimo
        if def_start < idx_cat and linhas[def_start].startswith('(syn.)'):
            sinonimo = linhas[def_start].replace('(syn.)', '').strip()
            def_start += 1

        # Tudo o que sobra entre o Termo/Sinónimo e a Categoria, é a Definição
        definicao = " ".join(linhas[def_start:idx_cat])
        # --- PARTE B: TRADUÇÕES ---
        traducoes = {}
        current_lang = None
        j = idx_cat + 1
        
        while j < len(linhas):
            if k + 1 < len(idx_cats) and j >= idx_cats[k+1]:
                break
                
            l = linhas[j]
            match_lang = padrao_lingua.match(l)
            
            if match_lang:
                current_lang = match_lang.group(1)
                texto = match_lang.group(2) or ""
                traducoes[current_lang] = texto.strip()
            elif current_lang:
                if current_lang == 'ZH':
                    if not re.search(r'[\u4e00-\u9fff]', l) and re.search(r'[a-zA-Z]', l):
                        break
                    else:
                        traducoes[current_lang] += " " + l
                else:
                    traducoes[current_lang] += " " + l
            else:
                break
            j += 1
        next_term_start = j 

        traducoes_limpas = {k_lang: v_lang.strip() for k_lang, v_lang in traducoes.items()}
        
        resultados.append({
            "indice": str(k + 1),
            "termo_en": termo,
            "sinonimo_en": sinonimo,
            "categoria": categoria,
            "definicao": definicao,
            "traducoes": traducoes_limpas
        })
    with open(caminho_json, 'w', encoding='utf-8') as f:
        json.dump(resultados, f, ensure_ascii=False, indent=4)

    print(f"🎯 Na mouche! Foram processados {len(resultados)} conceitos estruturados na perfeição.")

extrair_glossario_wipo_blindado("Textos/texto_covid19.txt", "Dicionarios/dicionario_covid19.json")