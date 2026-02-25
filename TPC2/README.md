Exercício 1: 
1.1 (re.match): Verificação se uma linha começa com a palavra "hello".

1.2 (re.search): Pesquisa da palavra "hello" em qualquer posição da string.

1.3 (re.findall): Extração de todas as ocorrências de "hello", ignorando a diferença entre maiúsculas e minúsculas (case-insensitive).

1.4 (re.sub): Substituição de todas as ocorrências de "hello" por um marcador visual (*YEP*).

1.5 (re.split): Divisão de uma string em múltiplos elementos usando a vírgula como delimitador.

Exercício 2: 
Implementação de uma função que valida se uma frase termina com a expressão "por favor" seguida de um sinal de pontuação válido (., ,, ;, :, !, ?, etc.).

Exercício 3: 
Uso do re.findall com word boundaries (\b) para contar especificamente as ocorrências da palavra "eu" (isolada), evitando que sejam contadas partes de outras palavras (como "teu" ou "meu").

Exercício 4:
Desenvolvimento de uma função de substituição dinâmica que troca a sigla de um curso ("LEI") por um novo nome fornecido pelo utilizador, mantendo a integridade do texto.

Exercício 5: 
Conversão de uma string de números separados por vírgulas numa lista de inteiros recorrendo ao re.split, seguida do cálculo da sua soma total.

Exercício 6: 
Criação de um padrão complexo para identificar pronomes pessoais (eu, tu, ele, ela, nós, vós) e as suas variantes no plural, demonstrando o uso de grupos de captura e o operador de união (|).

Exercício 7: 
Aplicação de âncoras de início (^) e fim ($) de linha para validar se uma string cumpre as regras de nomeação de variáveis em muitas linguagens de programação: começar por letra/underscore e conter apenas caracteres alfanuméricos ou underscores.

Exercício 8: 
Uso de quantificadores e tratamento de sinais opcionais (-?) para extrair todos os números inteiros (positivos e negativos) presentes num bloco de texto.

Exercício 9: 
Utilização de re.sub para substituir espaços em branco por underscores. O exercício foca na simplificação de múltiplos espaços consecutivos para apenas um único caracter de ligação.

Exercício 10: 
Processamento de uma lista de códigos postais no formato português (0000-000), utilizando o re.split para separar a parte postal principal do sub-setor, resultando numa lista de pares (tuplos/listas).