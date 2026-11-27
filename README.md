# Histórias da Terra Mineira

Versão em HTML do livro *Historias da Terra Mineira*, de **Carlos Góes** (12ª edição, Rio de Janeiro, 1938), um livro de leitura escolar com 24 contos sobre a história de Minas Gerais.

## Sobre o projeto

- **Extração via IA:** o texto e as ilustrações foram extraídos do PDF original com o auxílio de inteligência artificial.
- **Modernização via IA:** as palavras do português brasileiro antigo foram atualizadas para a grafia atual (por exemplo, `estylo` → estilo, `typicamente` → tipicamente, `elle` → ele), mantendo a estrutura do texto original: capítulos, parágrafos, versos, notas, imagens e pontuação.

- **Revisão via IA:** o texto modernizado foi relido por inteiro, e erros evidentes de impressão do livro foram corrigidos somente nessa versão (veja [`_work/correcoes.tsv`](_work/correcoes.tsv)).

> **Atenção:** não houve revisão humana nem conferência de todas as páginas contra as digitalizações. Pode haver erros de extração ou de modernização. Em caso de dúvida, vale o livro original.

## Como ler

Abra um dos arquivos no navegador:

| Arquivo | Conteúdo |
|---|---|
| [`index-moderno.html`](index-moderno.html) | Texto com a ortografia atual |
| [`index.html`](index.html) | Texto com a grafia original de 1938 |

Em `index-moderno.html`, mantêm a grafia original o nome do autor, as assinaturas da certidão, os títulos de livros nas referências e na lista de obras do autor, as citações em latim e a imagem da capa. Trechos ilegíveis aparecem como `[?]`.

## Estrutura

```
index.html                    texto de 1938 (gerado por _work/build.py)
index-moderno.html            texto modernizado (gerado por _work/modernizar.py)
images/                       capa e ilustrações
_work/text/                   transcrição, um fragmento HTML por folha digitalizada
_work/build.py                monta o index.html a partir dos fragmentos
_work/modernizar.py           gera o index-moderno.html a partir do index.html
_work/modernizar-mapa.tsv     tabela de palavras: grafia antiga → atual
_work/correcoes.tsv           hifenização, nomes e erros impressos: antes → depois
_work/inventory-notes.md      notas da extração e convenções de transcrição
_work/pt.sh                   imprime o texto puro dos fragmentos
```

As digitalizações intermediárias (`_work/orig/` e `_work/halves/`) e o PDF original não fazem parte do repositório.

## Como regenerar

Requer Python 3, sem dependências externas.

```sh
python3 _work/build.py        # fragmentos -> index.html
python3 _work/modernizar.py   # index.html -> index-moderno.html
```

Para corrigir a transcrição, edite os arquivos em `_work/text/`. Para corrigir uma palavra modernizada, edite `_work/modernizar-mapa.tsv`; as regras que dependem do contexto ficam em `_work/modernizar.py` e as correções pontuais em `_work/correcoes.tsv`. Depois, rode os dois comandos acima.
