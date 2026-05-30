# CLAUDE.md

Contexto e convenções para trabalhar neste repositório com o Claude Code.

## O que é

Página estática "Mangas do Brasil": guia de variedades de manga + mapa interativo de predominância
por estado. A entrega é **um único HTML autossuficiente** (`mangas-do-brasil.html`) gerado por dois
scripts Python de build.

## Pipeline de build

```
data/br.json  --build_map.py-->  src/brmap.json
src/template.html + dados(build_html.py) + src/brmap.json  --build_html.py-->  mangas-do-brasil.html
```

- `build_map.py`: projeta o GeoJSON, simplifica (Douglas-Peucker) e calcula a posição do rótulo de
  cada estado com **polylabel** (polo de inacessibilidade — garante o código dentro do polígono).
- `build_html.py`: contém os dicionários `varieties` e `states`; injeta tudo no template no lugar do
  marcador `/*__DATA__*/`.

Sempre rode `python3 build_html.py` após editar dados ou template. Rode `build_map.py` só se mexer na
geometria/rótulos do mapa.

## Convenções

- **Não editar `mangas-do-brasil.html` na mão** — é saída gerada. Edite `src/template.html` e os
  dicionários em `build_html.py`, depois re-builde.
- **Não editar `src/brmap.json` na mão** — é gerado por `build_map.py`.
- Idioma de toda a UI e textos: **português (pt-BR)**.
- Dependências: só Python stdlib para o build. Evite adicionar libs de runtime no HTML; manter o
  arquivo standalone é um objetivo. `playwright`/`cairosvg` são aceitáveis só como ferramenta de DEV
  (validação/screenshot), nunca no HTML final.
- Estética: papel/botânico, fontes Fraunces (display) + Archivo (texto). Cores em CSS vars no `:root`.
- Ilustrações de manga: SVG por código. Silhuetas no objeto `SIL`; cada variedade referencia uma `sil`
  + um gradiente `grad` (3 stops) + cor sólida `cor`.

## Como validar (recomendado)

Se `playwright` estiver instalado:

```bash
pip install playwright && python3 -m playwright install chromium
```

Checagem mínima após mudanças:
- abrir `file://.../mangas-do-brasil.html`, conferir **0 erros de console** (ignorar 403 do Google
  Fonts se a rede bloquear; em rede normal carrega);
- `.card` deve ter 17 (ou o nº atual de variedades), cada um com 2 `.slot`;
- clicar um estado atualiza `#panel`;
- screenshot full-page para conferir layout e centralização dos rótulos do mapa.

## Tarefa prioritária: fotos reais (inteira + cortada)

Objetivo: substituir/complementar as ilustrações por **fotos reais** de cada variedade, **inteira e
cortada ao meio**, embutidas no HTML (sem depender de link externo que quebra).

Plano sugerido:
1. Para cada variedade, obter 2 imagens (inteira, cortada). Fontes com licença livre primeiro
   (Wikimedia Commons, Openverse). Para cultivares brasileiras (Espada, Rosa, Ubá, Bourbon, Coquinho,
   Itamaracá) pode não haver foto livre — registrar a lacuna e deixar a ilustração como fallback.
2. Baixar, redimensionar (ex.: ~800px lado maior, WebP/JPEG qualidade ~80) para manter o arquivo leve.
3. Embutir como **base64 data URI**. Sugestão de design: adicionar ao dicionário de cada variedade
   campos opcionais `foto_inteira` / `foto_cortada` (data URI) e fazer o template preencher o `.ph-img`
   correspondente; manter o `onerror`/fallback para a ilustração.
4. Atribuição: se a licença exigir, adicionar crédito (autor/licença) no rodapé ou num `title`.
5. Não embutir imagens que não puder verificar visualmente; preferir lacuna a foto errada.

Detalhe técnico: o ambiente anterior não tinha acesso de rede para baixar imagens. No Claude Code,
a rede local resolve isso (`curl`/`wget`/requests). Verifique cada imagem antes de embutir.

## Não fazer

- Não quebrar o caráter standalone do HTML final.
- Não inventar dados de produção/variedade — citar fonte ou marcar como estimativa (a página já
  distingue "dado oficial" vs "estimativa" por estado).
