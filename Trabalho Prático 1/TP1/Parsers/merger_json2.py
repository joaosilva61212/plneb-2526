import json

def carregar_json(caminho):
    try:
        with open(caminho, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Aviso: Ficheiro {caminho} não encontrado.")
        return []

def convergir_dados():
     # 1. Carregar os ficheiros
    dados_covid = carregar_json("Dicionarios/dicionario_covid19.json")
    dados_medicina = carregar_json("Dicionarios/dicionario_medicina.json")
    dados_categorias = carregar_json("Dicionarios/dicionario_categorias.json")
    dados_neologismos = carregar_json("Dicionarios/dicionario_neologismos.json")
    dados_enfermagem = carregar_json("Dicionarios/dicionario_enfermagem.json")

    glossario_global = []
    id_contador = 1

   # Função auxiliar para mapear os dados de forma uniforme
    def adicionar_ao_glossario(lista_origem, fonte, chave_termo):
        nonlocal id_contador
        for item in lista_origem:
            glossario_global.append({
                "id_global": str(id_contador),
                "termo": item.get(chave_termo, "n.d."),
                "definicao": item.get("definicao", "n.d."),
                "info_gramatical": item.get("info_gramatical", "n.d."),
                "categoria": item.get("categoria", "n.d."),
                "traducoes": item.get("traducoes", {}),
                "fonte": fonte
            })
            id_contador += 1
 
 # 2. Mapear cada dicionário respeitando as suas chaves específicas
    adicionar_ao_glossario(dados_covid, "WIPO Pearl COVID-19", "termo_en")
    adicionar_ao_glossario(dados_medicina, "Dicionário de Medicina", "termo")
    adicionar_ao_glossario(dados_categorias, "Glossário Categorias", "palavra")
    adicionar_ao_glossario(dados_neologismos, "Neologismos Saúde", "palavra")

# Como o ficheiro é um dicionário {termo: definicao}, usamos .items()
    for termo, definicao in dados_enfermagem.items():
        glossario_global.append({
            "id_global": str(id_contador),
            "termo": termo,
            "definicao": definicao,
            "info_gramatical": "n.d.",
            "categoria": "n.d.",
            "traducoes": {},  
            "fonte": "Glossário de Enfermagem"
        })
        id_contador += 1

# 3. Guardar o resultado final
    with open("Dicionarios/dicionario_global.json", "w", encoding="utf-8") as f:
        json.dump(glossario_global, f, indent=4, ensure_ascii=False)
    
    print(f"Sucesso! {len(glossario_global)} termos consolidados em 'dicionario_global.json'.")

if __name__ == "__main__":
    convergir_dados()