from Parsers import parser_covid
from Parsers import parser_neologismos
from Parsers import parser_ministerio
from Parsers import parser_medicina 
from Parsers import merger_json2 
from Parsers import parser_enfermagem

def main():
    print("🚀 A iniciar o pipeline de PLN...")

    print("\n--- A correr Parsers ---")
    
    print("A processar WIPO...")
    parser_covid.extrair_glossario_wipo_blindado("Textos/texto_covid19.txt", "Dicionarios/dicionario_covid19.json")
    
    print("A processar Neologismos...")
    parser_neologismos.extrair_novo_formato("Textos/texto_neologismos.txt", "Dicionarios/dicionario_neologismos.json")
    
    print("A processar Categorias...")
    parser_ministerio.extrair_dicionario_por_categorias("Textos/texto_ms.txt", "Dicionarios/dicionario_categorias.json")

    print("A processar Medicina...")
    parser_medicina.extrair_dicionario_medicina("Textos/texto_medicina.txt", "Dicionarios/dicionario_medicina.json")
    print("A processar Glossário de Enfermagem...")
    parser_enfermagem.extrair_glossario_enfermagem("Textos/Glossário de Enfermagem.txt","Dicionarios/dicionario_enfermagem.json")

    print("\n--- A Convergir Dados ---")
    merger_json2.convergir_dados()
    
    print("\n Processo terminado! O ficheiro global está pronto a entregar.")

if __name__ == "__main__":
    main()