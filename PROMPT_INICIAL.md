# Prompt inicial — colar no Claude Code

Copie o bloco abaixo na primeira mensagem do Claude Code (dentro da pasta do projeto).

---

Você está num projeto chamado "Mangas do Brasil": uma página estática (HTML único autossuficiente)
com um guia de variedades de manga e um mapa interativo de predominância por estado. Leia o
`README.md` e o `CLAUDE.md` antes de mexer — eles explicam o pipeline de build e as convenções.

Resumo do build:
- `python3 build_map.py` gera `src/brmap.json` (geometria + rótulos do mapa) a partir de `data/br.json`.
- `python3 build_html.py` injeta os dados (dicionários `varieties` e `states` dentro do próprio
  script) no `src/template.html` e gera `mangas-do-brasil.html`.
- Nunca edite `mangas-do-brasil.html` nem `src/brmap.json` na mão (são gerados).

Primeira tarefa (a principal pendência): **adicionar fotos reais de cada variedade — inteira e
cortada ao meio — embutidas no HTML em base64**. Passos:

1. Confirme que consegue acessar a rede (teste um `curl` num host de imagens). O ambiente anterior
   não tinha rede liberada; aqui deve ter.
2. Para cada variedade do dicionário `varieties`, busque 2 imagens com **licença livre** (Wikimedia
   Commons / Openverse de preferência): uma da fruta inteira e uma cortada ao meio. Para as cultivares
   brasileiras (Espada, Rosa, Ubá, Bourbon, Coquinho, Itamaracá) pode não existir foto livre — nesses
   casos, registre a lacuna numa lista e mantenha a ilustração como fallback. Não embuta foto de
   variedade errada: na dúvida, deixe a lacuna.
3. Baixe, redimensione (~800px no lado maior, JPEG/WebP ~80% de qualidade) e converta para data URI.
4. Proponha o design da mudança antes de aplicar em massa: sugiro adicionar campos opcionais
   `foto_inteira` e `foto_cortada` (data URI) em cada variedade e ajustar `src/template.html` para
   preencher os `.ph-img` correspondentes, mantendo o upload local e o fallback de ilustração.
5. Faça primeiro **uma variedade de ponta a ponta** (ex.: Tommy Atkins), rode `build_html.py`, abra o
   HTML e me mostre o resultado antes de processar as outras.
6. Guarde os créditos/licenças das imagens e adicione atribuição no rodapé se a licença exigir.

Antes de começar, me diga: (a) se a rede está acessível, (b) seu plano de fontes de imagem e quais
variedades provavelmente vão ficar sem foto, (c) o diff de design que você pretende fazer no template.
Só depois parta para a implementação. Mantenha tudo em pt-BR e preserve o caráter standalone do HTML.

---

## Ideias de próximos passos (opcional, depois das fotos)

- Galeria/lightbox ao clicar numa foto.
- Busca/filtro de variedades por fibra, °Brix, uso ou origem.
- Alternar o mapa entre "predominância" e "nível de produção" (coroplético por toneladas/área).
- Página de detalhe por variedade (rota/âncora) com mais fotos e dados de safra.
- Exportar/baixar a versão com as fotos do usuário (já que o upload hoje é só na aba).
- Dados de calendário de safra por região.
