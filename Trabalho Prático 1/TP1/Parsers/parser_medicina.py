import re
import json

def extrair_dicionario_medicina(file_path, output_path):
    
    with open(file_path, "r", encoding="utf-8", errors='replace') as f:
        texto = f.read()

    #Limpeza 
    conteudo = re.sub(r'Vocabulario\s*\n\d+', '', texto)
    conteudo = re.sub(r'\n\s*\d+\s*\n', '\n', conteudo)

    #Expressão regular para extrair blocos de termos e traduções
    padrao_bloco = r'^(\d+)\s+(.*?)(?=\n\d+\s|\Z)'
    blocos = re.findall(padrao_bloco, conteudo, re.DOTALL | re.MULTILINE)

    dicionario_medico = []

    for id_con, resto_bloco in blocos:
        linhas = resto_bloco.strip().split('\n')
        termo_galego = linhas[0].strip()
        # Limpar o género gramatical no fim do termo (m, f, a, s, etc.)
        termo_galego = re.sub(r'\s+[mfas]\b.*', '', termo_galego).strip()
        
        traducoes = {}
        notas_bloco = []
        veja_tambem_bloco = []
        # Expressão regular para apanhar: sigla + texto (incluindo linhas seguintes indentadas)
        regex_trads = r'^(es|en|pt|la)\s+(.*?)(?=\n(?:es|en|pt|la)\s|\Z)'
        texto_traducoes = "\n".join(linhas[1:])
        trads_encontradas = re.findall(regex_trads, texto_traducoes, re.DOTALL | re.MULTILINE)
        
        for sigla, valor in trads_encontradas:
            valor_limpo = re.sub(r'\s+', ' ', valor).strip()
            
            #Adicionar os campos em que os termos aparecem seguidos com "Nota.-" ou "Vid.-" ao respetivo bloco
            if "Nota.-" in valor_limpo:
                partes = valor_limpo.split("Nota.-")
                valor_limpo = partes[0].strip()
                notas_bloco.append(partes[1].strip())

            if "Vid.-" in valor_limpo:
                partes = valor_limpo.split("Vid.-")
                valor_limpo = partes[0].strip()
                veja_tambem_bloco.append(partes[1].strip())
            
            valor_limpo = valor_limpo.rstrip(';').strip()
            traducoes[sigla] = valor_limpo
    
        if traducoes:
            entrada = {
                "id": id_con,
                "termo": termo_galego,
                "traducoes": traducoes
            }
            if notas_bloco:
                entrada["notas"] = " ".join(notas_bloco)
            if veja_tambem_bloco:
                entrada["veja_tambem"] = " ".join(veja_tambem_bloco)
                
            dicionario_medico.append(entrada)
    #Guardar json
    with open(output_path, "w", encoding="utf-8") as j:
        json.dump(dicionario_medico, j, ensure_ascii=False, indent=4)

    print(f"Sucesso! {len(dicionario_medico)} conceitos extraídos.")


extrair_dicionario_medicina("Textos/texto_medicina.txt", "Dicionarios/dicionario_medico.json")