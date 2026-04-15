import re
import json

def extrair_glossario_enfermagem(file_path, output_path):
    with open(file_path, "r", encoding="utf-8") as f:
        texto = f.read().replace('\r\n', '\n')

    #Limpeza
    cabecalho = r'GLOSSÁRIO DA LINGUAGEM ESPECIAL DE ENFERMAGEM.*?CONTEXTO AMAZÔNICO'
    texto = re.sub(cabecalho, '', texto, flags=re.DOTALL)
    texto = re.sub(r'\n\s*\d+\s*\n', '\n\n', texto)
    texto = re.sub(r'\f', '', texto)

    # Expressão regular
    padrao_bloco = r'(?:^|\n)([A-ZÀ-Ú][^\n]+)\n(?!\s*FONTE:)(.+?)\n\s*FONTE:\s*\n?(.*?)(?=\n\s*[A-ZÀ-Ú][^\n]+\n(?!\s*FONTE:)|\n\n|\Z)'

    matches = re.finditer(padrao_bloco, texto, flags=re.DOTALL)

    res = {}
    #Associar os grupos de captura aos campos do dicionário
    for match in matches:
        termo = match.group(1).strip()
        definicao = match.group(2).strip() 
        definicao_limpa = re.sub(r'\s+', ' ', definicao)
        
        # Validação de segurança para evitar termos muito longos ou com conteúdo indesejado
        if len(termo) > 1 and "Dicionário Houaiss" not in termo:
            if len(termo.split()) < 10:
                res[termo] = definicao_limpa

    # Guardar o resultado final
    with open(output_path, "w", encoding="utf-8") as f_out:
        json.dump(res, f_out, indent=4, ensure_ascii=False)

    print(f"Sucesso! Foram extraídos {len(res)} conceitos")

extrair_glossario_enfermagem("Textos/Glossário de Enfermagem.txt", "Dicionarios/glossario_enfermagem.json")