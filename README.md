# Mangas do Brasil

Página estática (HTML único, sem build de runtime) com um **guia visual das variedades de manga**
cultivadas no Brasil e um **mapa interativo do país** mostrando a variedade predominante por estado.

A página final é **autossuficiente**: um único arquivo `mangas-do-brasil.html` que abre direto no
navegador, sem servidor. Fontes vêm do Google Fonts (precisa de internet só pra isso; o resto é inline).

## O que tem

- **Catálogo de 17 variedades** em cards, cada um com origem, peso, fibra, °Brix, uso e descrição.
- **Slots de foto "Inteira / Cortada"** por card, com upload local (no navegador) e fallback para
  ilustração SVG quando não há foto.
- **Mapa interativo do Brasil** (SVG, 27 estados) pintado pela variedade predominante; hover/clique
  abre um painel com detalhes, nível de produção e selo de confiança. Legenda filtra por variedade.
- **Ilustrações de manga em SVG** geradas por código (silhueta + gradiente por variedade).

## Estrutura

```
.
├── mangas-do-brasil.html      # SAÍDA final (é isto que se abre/publica)
├── build_map.py               # gera src/brmap.json a partir de data/br.json
├── build_html.py              # injeta dados no template -> mangas-do-brasil.html
├── src/
│   ├── template.html          # HTML+CSS+JS com placeholder /*__DATA__*/
│   └── brmap.json             # paths SVG + centróides dos estados (gerado)
├── data/
│   └── br.json                # GeoJSON bruto dos estados (fonte do mapa)
├── README.md
├── CLAUDE.md                  # contexto pro Claude Code
└── PROMPT_INICIAL.md          # prompt pra colar no Claude Code
```

## Como buildar

Requisito: Python 3 (só biblioteca padrão). Pra validar render/screenshot, opcional: `playwright`.

```bash
python3 build_map.py     # (re)gera src/brmap.json  — só precisa rodar se mexer no mapa
python3 build_html.py    # gera mangas-do-brasil.html
```

Abra `mangas-do-brasil.html` no navegador.

## Onde editar o quê

- **Variedades** (adicionar/editar/remover): dicionário `varieties` em `build_html.py`.
  Cada item tem `key, nome, sil, grad, origem, peso, fibra, brix, uso, cor, desc`.
  - `sil` é a silhueta da ilustração; valores válidos estão em `SIL` dentro de `src/template.html`
    (`oval, elong, keitt, long, heart, beak, broad, haden, flat, small`).
  - `grad` são 3 cores (claro→escuro) do gradiente da casca; `cor` é a cor sólida do card/mapa.
- **Predominância por estado**: dicionário `states` em `build_html.py`
  (`predom`, lista `vars`, `tier`, `conf`, `nota`).
- **Layout / estilo / interações**: `src/template.html` (CSS no `<style>`, lógica no `<script>`).
  Os dados entram via `const DATA = /*__DATA__*/;`.
- **Geometria do mapa / posição dos rótulos**: `build_map.py` (projeção, simplificação Douglas-Peucker,
  e `polylabel` para centralizar o código da UF dentro do polígono).

## Pendência principal: fotos reais

Hoje os cards usam ilustração + upload local. Falta um acervo de **fotos reais (inteira e cortada)**
por variedade, embutidas no arquivo. Isso não foi feito no ambiente anterior por falta de acesso de
rede para baixar/verificar imagens. No Claude Code (rede local liberada) dá pra resolver — ver
`CLAUDE.md` e `PROMPT_INICIAL.md`.

## Fontes dos dados

- Produção/exportação: Observatório do Mercado da Manga (Embrapa Semiárido) e PAM/IBGE (safras 2023–2024).
- Características das variedades: Embrapa, JBox e literatura de fruticultura.
- GeoJSON dos estados: projeto `geodata-br-states` (giuliano-macedo), via GitHub.

> Nota de confiança: a predominância por estado tem respaldo oficial só para os 6 grandes produtores
> (BA, PE, SP, MG, CE, RN). Para os demais é estimativa de variedades comuns de quintal/mercado —
> o IBGE não publica produção desagregada por cultivar. Isso está sinalizado na própria página.
