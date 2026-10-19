/**
 * Gera o Manual de Revisão do Site da Célia Lima em formato .docx
 *
 * Estrutura: 16 seções, cada uma com o texto ATUAL do site à esquerda
 * e um espaço de considerações da Célia à direita (table 2-col).
 *
 * Paleta: areia #faf6f1, terracota #a05a3c, verde sálvia #7a8a5b,
 *         marrom-escuro #3d3530
 */

const {
  Document, Packer, Paragraph, TextRun, Table, TableRow, TableCell,
  Header, Footer, PageNumber, NumberFormat,
  AlignmentType, HeadingLevel, WidthType, BorderStyle, ShadingType,
  PageOrientation, PageBreak,
} = require("docx");
const fs = require("fs");
const path = require("path");

// === Paleta ===
const PALETTE = {
  areia: "FAF6F1",
  areiaEscura: "F0E9DC",
  terracota: "A05A3C",
  verdeSálvia: "7A8A5B",
  marromEscuro: "3D3530",
  marromClaro: "838179",
  borda: "D8CFC0",
  textoMuted: "838179",
};

// === Fontes (PT-BR; não usamos fonts CJK) ===
const FONT_BODY = { ascii: "Calibri", eastAsia: "Calibri" };
const FONT_HEADING = { ascii: "Calibri", eastAsia: "Calibri" };

// === Helpers ===
function tx(text, opts = {}) {
  return new TextRun({
    text,
    font: FONT_BODY,
    color: opts.color || PALETTE.marromEscuro,
    size: opts.size || 22,
    bold: opts.bold || false,
    italics: opts.italics || false,
  });
}

function p(text, opts = {}) {
  return new Paragraph({
    alignment: opts.alignment || AlignmentType.LEFT,
    spacing: { before: opts.before || 0, after: opts.after || 80, line: 320 },
    indent: opts.indent || undefined,
    children: [tx(text, opts)],
  });
}

function heading(text, level = HeadingLevel.HEADING_1, color = PALETTE.terracota) {
  const sizeMap = {
    [HeadingLevel.HEADING_1]: 36,
    [HeadingLevel.HEADING_2]: 28,
    [HeadingLevel.HEADING_3]: 24,
  };
  return new Paragraph({
    heading: level,
    spacing: { before: level === HeadingLevel.HEADING_1 ? 360 : 240, after: 160, line: 320 },
    children: [
      new TextRun({
        text,
        font: FONT_HEADING,
        color,
        size: sizeMap[level],
        bold: true,
      }),
    ],
  });
}

// Célula com padding
function paddedCell(children, opts = {}) {
  return new TableCell({
    children,
    margins: { top: 200, bottom: 200, left: 200, right: 200 },
    shading: opts.fill
      ? { type: ShadingType.CLEAR, fill: opts.fill, color: "auto" }
      : undefined,
    width: { size: opts.width || 50, type: WidthType.PERCENTAGE },
    borders: opts.borders || {
      top: { style: BorderStyle.SINGLE, size: 4, color: PALETTE.borda },
      bottom: { style: BorderStyle.SINGLE, size: 4, color: PALETTE.borda },
      left: { style: BorderStyle.SINGLE, size: 4, color: PALETTE.borda },
      right: { style: BorderStyle.SINGLE, size: 4, color: PALETTE.borda },
    },
  });
}

// Bloco de texto "site atual" — coluna esquerda
function textBlock(paragraphs, opts = {}) {
  const fill = opts.fill || PALETTE.areiaEscura;
  return paddedCell(paragraphs, { fill, width: 55 });
}

// Bloco "considerações da Célia" — coluna direita com linhas-guia robustas (texto sublinhado)
function notesBlock(opts = {}) {
  const label = opts.label || "Anotações da Célia";
  const guides = opts.guides || 8;
  const paras = [
    new Paragraph({
      spacing: { before: 0, after: 60, line: 320 },
      children: [
        new TextRun({
          text: label,
          font: FONT_BODY,
          color: PALETTE.verdeSálvia,
          size: 18,
          italics: true,
          bold: true,
        }),
      ],
    }),
    new Paragraph({
      spacing: { before: 0, after: 160, line: 320 },
      children: [
        new TextRun({
          text: "(escreva, risque, marque — não há formato certo)",
          font: FONT_BODY,
          color: PALETTE.marromClaro,
          size: 16,
          italics: true,
        }),
      ],
    }),
  ];
  // Linhas-guia: texto sublinhado com espaços + "." final (cor branca) — robusto e visível
  for (let i = 0; i < guides; i++) {
    paras.push(
      new Paragraph({
        spacing: { before: 0, after: 100, line: 320 },
        children: [
          new TextRun({
            text: "                                                                    .",
            font: FONT_BODY,
            size: 22,
            underline: { type: "single", color: "838179" },
            color: "FFFFFF",
          }),
        ],
      })
    );
  }
  return paddedCell(paras, { fill: "FFFFFF", width: 45 });
}

// Bloco completo: texto atual | considerações
function reviewBlock(textParas, notesOpts = {}) {
  return new Table({
    width: { size: 100, type: WidthType.PERCENTAGE },
    rows: [
      new TableRow({
        cantSplit: false,
        children: [
          textBlock(textParas),
          notesBlock(notesOpts),
        ],
      }),
    ],
  });
}

// === Conteúdo de cada seção ===

// --- 1. Capa ---
function buildCover() {
  return [
    new Paragraph({ spacing: { before: 2400, after: 200 }, children: [new TextRun({ text: ".", font: FONT_BODY, size: 22, color: "FFFFFF" })] }),
    new Paragraph({
      alignment: AlignmentType.CENTER,
      spacing: { before: 0, after: 240, line: 480 },
      children: [
        new TextRun({
          text: "MANUAL DE REVISÃO DO SITE",
          font: FONT_HEADING,
          color: PALETTE.terracota,
          size: 28,
          bold: true,
          characterSpacing: 60,
        }),
      ],
    }),
    new Paragraph({
      alignment: AlignmentType.CENTER,
      spacing: { before: 0, after: 80, line: 720 },
      children: [
        new TextRun({
          text: "Célia Lima",
          font: FONT_HEADING,
          color: PALETTE.marromEscuro,
          size: 72,
          bold: true,
        }),
      ],
    }),
    new Paragraph({
      alignment: AlignmentType.CENTER,
      spacing: { before: 0, after: 480, line: 400 },
      children: [
        new TextRun({
          text: "Para você ler, marcar e fazer o site ser seu.",
          font: FONT_BODY,
          color: PALETTE.marromClaro,
          size: 28,
          italics: true,
        }),
      ],
    }),
    new Paragraph({
      alignment: AlignmentType.CENTER,
      spacing: { before: 0, after: 120 },
      children: [
        new TextRun({
          text: "— outubro de 2026 —",
          font: FONT_BODY,
          color: PALETTE.marromClaro,
          size: 22,
        }),
      ],
    }),
    new Paragraph({ spacing: { before: 2400, after: 0 }, children: [new TextRun({ text: ".", font: FONT_BODY, size: 22, color: "FFFFFF" })] }),
    new Paragraph({
      alignment: AlignmentType.CENTER,
      spacing: { before: 0, after: 80 },
      children: [
        new TextRun({
          text: "Documento de trabalho — para anotações",
          font: FONT_BODY,
          color: PALETTE.marromClaro,
          size: 20,
          italics: true,
        }),
      ],
    }),
    new Paragraph({
      children: [new PageBreak()],
    }),
  ];
}

// --- 2. Como usar ---
function buildHowToUse() {
  return [
    heading("Como usar este manual", HeadingLevel.HEADING_1),
    p(
      "Este documento é um espaço de conversa entre você e o site. Em cada página, à esquerda está o texto que está no ar hoje; à direita há linhas em branco para você escrever, riscar, replanejar.",
      { size: 22, after: 160 }
    ),
    p("Você pode:", { size: 22, bold: true, after: 80 }),
    new Paragraph({
      spacing: { before: 0, after: 60, line: 320 },
      bullet: { level: 0 },
      children: [tx("Riscar o que não faz sentido e reescrever do seu jeito;", { size: 22 })],
    }),
    new Paragraph({
      spacing: { before: 0, after: 60, line: 320 },
      bullet: { level: 0 },
      children: [tx("Marcar com ✓ onde já está bom e não precisa mexer;", { size: 22 })],
    }),
    new Paragraph({
      spacing: { before: 0, after: 60, line: 320 },
      bullet: { level: 0 },
      children: [tx("Fazer perguntas do tipo \"aqui eu não entendi\" ou \"posso falar de X?\";", { size: 22 })],
    }),
    new Paragraph({
      spacing: { before: 0, after: 60, line: 320 },
      bullet: { level: 0 },
      children: [tx("Sugerir textos novos, fotos, referências, qualquer coisa;", { size: 22 })],
    }),
    new Paragraph({
      spacing: { before: 0, after: 200, line: 320 },
      bullet: { level: 0 },
      children: [tx("Deixar em branco se aquela parte não precisar de revisão.", { size: 22 })],
    }),
    p(
      "Não há pressa. Pode levar dias, semanas. Quando você me devolver (em arquivo ou em screenshots do que marcou), eu aplico as mudanças no site e te mostro o resultado.",
      { size: 22, after: 160 }
    ),
    p(
      "E lembra: este manual é só um espelho do que existe hoje. O que estiver bom, fica. O que precisar mudar, muda. O que estiver faltando, a gente cria.",
      { size: 22, after: 200 }
    ),
    new Paragraph({
      children: [new PageBreak()],
    }),
  ];
}

// --- 3. Identidade e contato ---
function buildIdentity() {
  const textParas = [
    p("Emails que encontrei na sua vida digital:", { bold: true, size: 22, color: PALETTE.terracota, after: 100 }),
    new Paragraph({
      spacing: { before: 0, after: 60, line: 320 },
      bullet: { level: 0 },
      children: [tx("celiacalima@gmail.com — aparece no rodapé do Personare (em todos os 98 artigos originais)", { size: 22 })],
    }),
    new Paragraph({
      spacing: { before: 0, after: 60, line: 320 },
      bullet: { level: 0 },
      children: [tx("celialima.terapeuta@gmail.com — aparece no rodapé do livro PDF", { size: 22 })],
    }),
    new Paragraph({
      spacing: { before: 0, after: 100, line: 320 },
      bullet: { level: 0 },
      children: [tx("WhatsApp: ainda placeholder (5599999999999) — preciso do número real", { size: 22 })],
    }),
    p("Perguntas:", { bold: true, size: 22, color: PALETTE.terracota, after: 80 }),
    new Paragraph({
      spacing: { before: 0, after: 60, line: 320 },
      bullet: { level: 0 },
      children: [tx("Qual email você quer usar publicamente no site?", { size: 22 })],
    }),
    new Paragraph({
      spacing: { before: 0, after: 60, line: 320 },
      bullet: { level: 0 },
      children: [tx("E o WhatsApp — mesmo número de sempre ou um novo só para o site?", { size: 22 })],
    }),
    new Paragraph({
      spacing: { before: 0, after: 100, line: 320 },
      bullet: { level: 0 },
      children: [tx("Tem redes sociais (Instagram, LinkedIn) que quer linkar?", { size: 22 })],
    }),
    p("Formação profissional (preciso para a página Sobre e as páginas legais):", { bold: true, size: 22, color: PALETTE.terracota, after: 80 }),
    new Paragraph({
      spacing: { before: 0, after: 60, line: 320 },
      bullet: { level: 0 },
      children: [tx("Como se descreveria: \"terapeuta\" ou \"psicoterapeuta\"?", { size: 22 })],
    }),
    new Paragraph({
      spacing: { before: 0, after: 60, line: 320 },
      bullet: { level: 0 },
      children: [tx("Tem registro em alguma associação profissional? Qual?", { size: 22 })],
    }),
    new Paragraph({
      spacing: { before: 0, after: 60, line: 320 },
      bullet: { level: 0 },
      children: [tx("Quais instituições você se formou? Ano?", { size: 22 })],
    }),
    new Paragraph({
      spacing: { before: 0, after: 60, line: 320 },
      bullet: { level: 0 },
      children: [tx("Trabalha presencialmente em qual cidade/endereço? (Se quiser divulgar)", { size: 22 })],
    }),
  ];
  return [
    heading("1. Identidade e contato", HeadingLevel.HEADING_1),
    p("Antes de mexer em qualquer texto, preciso saber qual email, telefone e formação profissional você quer usar publicamente. Tudo o resto depende disso.", { size: 22, after: 200 }),
    reviewBlock(textParas, { label: "Respostas da Célia", guides: 12 }),
    new Paragraph({ children: [new PageBreak()] }),
  ];
}

// --- 4. Home Hero ---
function buildHomeHero() {
  const textParas = [
    p("Texto que está no ar:", { bold: true, size: 22, color: PALETTE.terracota, after: 80 }),
    p("Kicker (pequeno, acima do título):", { italics: true, size: 20, color: PALETTE.marromClaro, after: 40 }),
    p("Psicoterapia · Autoconhecimento", { size: 22, after: 120 }),
    p("Título principal:", { italics: true, size: 20, color: PALETTE.marromClaro, after: 40 }),
    p("Um espaço para pensar a vida com mais gentileza.", { bold: true, size: 28, color: PALETTE.marromEscuro, after: 40 }),
    p("(com 'pensar a vida' em itálico e terracota)", { italics: true, size: 20, color: PALETTE.marromClaro, after: 120 }),
    p("Subtítulo:", { italics: true, size: 20, color: PALETTE.marromClaro, after: 40 }),
    p("Psicoterapia e práticas que conversam com você sobre amor, família, corpo, trabalho e espiritualidade — no ritmo próprio de cada jornada.", { size: 22, after: 120 }),
    p("Botões (chamadas para ação):", { italics: true, size: 20, color: PALETTE.marromClaro, after: 40 }),
    new Paragraph({ spacing: { before: 0, after: 60, line: 320 }, bullet: { level: 0 }, children: [tx("\"Agendar conversa\" (terracota, botão sólido)", { size: 22 })] }),
    new Paragraph({ spacing: { before: 0, after: 0, line: 320 }, bullet: { level: 0 }, children: [tx("\"Conheça meu trabalho\" (contorno, transparente)", { size: 22 })] }),
  ];
  return [
    heading("2. Home — topo (hero)", HeadingLevel.HEADING_1),
    p("É a primeira coisa que aparece quando alguém entra no site. Define o tom em 5 segundos.", { size: 22, after: 200 }),
    reviewBlock(textParas, { label: "Sua revisão do hero", guides: 10 }),
    new Paragraph({ children: [new PageBreak()] }),
  ];
}

// --- 5. Citação + cards de contexto ---
function buildHomeContexts() {
  const textParas = [
    p("Card de citação (aparece em destaque no meio dos 6 cards):", { bold: true, size: 22, color: PALETTE.terracota, after: 80 }),
    p("\"Ao persistirem os médicos, os sintomas deverão ser consultados.\"", { italics: true, size: 26, color: PALETTE.marromEscuro, after: 40 }),
    p("— Tom Zé", { size: 20, color: PALETTE.marromClaro, after: 200 }),
    p("Texto introdutório da seção dos 6 cards:", { bold: true, size: 22, color: PALETTE.terracota, after: 80 }),
    p("Kicker: \"Por onde começar\"", { italics: true, size: 20, color: PALETTE.marromClaro, after: 40 }),
    p("Título: \"O que te trouxe aqui?\"", { italics: true, size: 20, color: PALETTE.marromClaro, after: 40 }),
    p("Subtítulo: \"Cada contexto reúne textos e práticas que conversam com uma dor, uma pergunta ou um momento da vida. Comece pela epígrafe — e escolha o que ressoa.\"", { size: 22, after: 200 }),
    p("Os 6 cards de contexto, em ordem:", { bold: true, size: 22, color: PALETTE.terracota, after: 80 }),
    new Paragraph({ spacing: { before: 0, after: 40, line: 320 }, bullet: { level: 0 }, children: [tx("1. Dinâmica Familiar e Criação de Filhos", { size: 22 })] }),
    new Paragraph({ spacing: { before: 0, after: 40, line: 320 }, bullet: { level: 0 }, children: [tx("2. Relacionamentos Amorosos e Sexualidade", { size: 22 })] }),
    new Paragraph({ spacing: { before: 0, after: 40, line: 320 }, bullet: { level: 0 }, children: [tx("3. Ansiedade, Estresse e Esgotamento", { size: 22 })] }),
    new Paragraph({ spacing: { before: 0, after: 40, line: 320 }, bullet: { level: 0 }, children: [tx("4. Autocrítica, Limites e Autoestima", { size: 22 })] }),
    new Paragraph({ spacing: { before: 0, after: 40, line: 320 }, bullet: { level: 0 }, children: [tx("5. Sintomas Psicossomáticos e Saúde Emocional", { size: 22 })] }),
    new Paragraph({ spacing: { before: 0, after: 40, line: 320 }, bullet: { level: 0 }, children: [tx("6. Produtividade, Carreira e Organização", { size: 22 })] }),
    new Paragraph({ spacing: { before: 0, after: 0, line: 320 }, bullet: { level: 0 }, children: [tx("7. Espiritualidade e Autoconhecimento (sim, são 7 — o Tom Zé ocupa o 1º lugar mas não é um card de contexto)", { size: 22, italics: true })] }),
  ];
  return [
    heading("3. Home — citação e cards de contexto", HeadingLevel.HEADING_1),
    p("Logo abaixo do hero, na home, há uma seção que convida o leitor a começar pela dor/pergunta que o trouxe. Tem a epígrafe do Tom Zé e os 6 (na verdade 7) cards de contexto.", { size: 22, after: 200 }),
    reviewBlock(textParas, { label: "Sua revisão da citação e dos cards", guides: 10 }),
    new Paragraph({ children: [new PageBreak()] }),
  ];
}

// --- 6. Página Sobre ---
function buildSobre() {
  const textParas = [
    p("Texto que está no ar na página /sobre:", { bold: true, size: 22, color: PALETTE.terracota, after: 100 }),
    p("Título:", { italics: true, size: 20, color: PALETTE.marromClaro, after: 40 }),
    p("Célia Lima — Psicoterapeuta", { bold: true, size: 26, color: PALETTE.marromEscuro, after: 120 }),
    p("Bio completa (4 parágrafos):", { italics: true, size: 20, color: PALETTE.marromClaro, after: 40 }),
    p("\"Sou psicoterapeuta com mais de 30 anos de prática clínica. Acompanho pessoas em seus processos emocionais com uma escuta atenta e direta, sem jargão técnico, e com profundo respeito pelo ritmo próprio de cada um.\"", { size: 22, after: 80 }),
    p("\"Minha escrita nasceu da prática: cada texto partiu de uma situação concreta vivida no consultório — uma dor, uma pergunta, um impasse — e ganhou forma para conversar com mais gente do que aqueles que conseguem sentar na poltrona da terapia.\"", { size: 22, after: 80 }),
    p("\"Trabalho com psicoterapia de orientação junguiana e psicosíntese, terapias integrativas (florais, óleos essenciais, respiração) e uma escuta que integra razão e emoção. Meu foco é ajudar você a reconhecer os movimentos internos que se repetem — e a encontrar, dentro de si, o fio do qual dar um novo passo.\"", { size: 22, after: 80 }),
    p("\"Ao longo dessa trajetória publiquei uma reunião dos meus principais artigos sobre autoconhecimento, amor, família, saúde, trabalho e espiritualidade — reunidos hoje neste site e no livro Caminhos do Autoconhecimento.\"", { size: 22, after: 200 }),
    p("3 cards de abordagem (logo abaixo):", { bold: true, size: 22, color: PALETTE.terracota, after: 80 }),
    p("Escuta — \"Antes de qualquer técnica, a escuta. O espaço onde você pode falar sem medo de julgamento, e onde o silêncio também é palavra. Aquilo que ainda não consegue ser dito costuma ser o mais importante.\"", { size: 22, after: 60 }),
    p("Símbolos e sonhos — \"O inconsciente fala por imagens, não por palavras. Um sonho, um sintoma do corpo, uma frase que escapa — tudo isso é linguagem. A terapia aprende a ler essa linguagem.\"", { size: 22, after: 60 }),
    p("Integrativo — \"Florais, óleos essenciais, respiração colorida: recursos que conversam com o corpo quando só a palavra não dá conta. Sempre como complemento, nunca como substituto da escuta e do trabalho psicológico.\"", { size: 22, after: 0 }),
  ];
  return [
    heading("4. Página Sobre", HeadingLevel.HEADING_1),
    p("A página onde você se apresenta. Tem a bio (4 parágrafos) e 3 cards de abordagem. É a única página onde o leitor te conhece além dos textos.", { size: 22, after: 200 }),
    reviewBlock(textParas, { label: "Sua revisão da página Sobre", guides: 14 }),
    new Paragraph({ children: [new PageBreak()] }),
  ];
}

// --- 7. Página Atendimento ---
function buildAtendimento() {
  const textParas = [
    p("Texto que está no ar em /atendimento:", { bold: true, size: 22, color: PALETTE.terracota, after: 100 }),
    p("Título: \"Como atuo na caminhada terapêutica.\"", { bold: true, size: 24, color: PALETTE.marromEscuro, after: 80 }),
    p("Intro: \"Com mais de 30 anos de experiência em psicoterapias de orientação junguiana e psicosíntese, meu foco é apoiar você a olhar para a própria história com clareza e profundidade. Trabalho com escuta ativa, atenção aos símbolos e ao corpo. Quando fazem sentido pra pessoa, uso como apoio terapêutico os recursos das terapias energéticas e vivências integrativas, acelerando meus pacientes na conquista da saúde física e emocional mais plena.\"", { size: 22, after: 80 }),
    p("Citação em destaque: \"Não se trata só de parar de sofrer. Trata-se de virar a pessoa inteira que você veio ser.\"", { italics: true, size: 22, color: PALETTE.terracota, after: 200 }),
    p("Os 4 serviços (cada um com nome, para quem é, formato, modalidade):", { bold: true, size: 22, color: PALETTE.terracota, after: 80 }),
    p("1. Psicoterapia individual", { bold: true, size: 22, after: 40 }),
    p("Para quem: \"Quem quer trabalho profundo e contínuo\". Formato: \"Sessões semanais de 50 min, em curso\". Modalidade: presencial ou virtual.", { size: 22, after: 80 }),
    p("2. Sessão de escuta inicial", { bold: true, size: 22, after: 40 }),
    p("Para quem: \"Quem está em dúvida se faz terapia\". Formato: \"Conversa única, 90 min, sem compromisso\". Modalidade: presencial ou virtual.", { size: 22, after: 80 }),
    p("3. Mentoria terapêutica pontual", { bold: true, size: 22, after: 40 }),
    p("Para quem: \"Quem tem uma questão, não quer entrar em processo\". Formato: \"Sessão única sobre um tema específico (ex.: luto, separação)\". Modalidade: presencial ou virtual.", { size: 22, after: 80 }),
    p("4. Grupo de estudos/terapia", { bold: true, size: 22, after: 40 }),
    p("Para quem: \"Quem quer trabalhar questões em comunidade\". Formato: \"Grupo fechado de 2 a N pessoas, encontros mensais\". Modalidade: virtual.", { size: 22, after: 200 }),
    p("3 cards de método (Subpersonalidades, Símbolos e sonhos, Sentido e totalidade):", { bold: true, size: 22, color: PALETTE.terracota, after: 80 }),
    p("Subpersonalidades — \"A gente não é uma pessoa só. Tem a profissional, a mãe, a filha, a adolescente que ainda mora dentro de você, a crítica, a medrosa. A terapia trabalha como essas partes conversam entre si — e como às vezes elas se boicotam.\"", { size: 22, after: 60 }),
    p("Símbolos e sonhos — \"O inconsciente fala por imagens, não por palavras. Um sonho, um sintoma do corpo, uma frase que escapa — tudo isso é linguagem. A terapia aprende a ler essa linguagem.\"", { size: 22, after: 60 }),
    p("Sentido e totalidade — \"Não se trata só de parar de sofrer. Trata-se de virar a pessoa inteira que você veio ser. A junguiana chama isso de individuação; a psicosíntese chama de auto-realização. É o mesmo convite: ser mais você mesmo.\"", { size: 22, after: 0 }),
  ];
  return [
    heading("5. Página Atendimento", HeadingLevel.HEADING_1),
    p("A página que descreve como você trabalha. Tem a introdução, os 4 serviços (modalidades de atendimento) e os 3 cards de método (Subpersonalidades, Símbolos, Sentido).", { size: 22, after: 200 }),
    reviewBlock(textParas, { label: "Sua revisão da página Atendimento", guides: 18 }),
    new Paragraph({ children: [new PageBreak()] }),
  ];
}

// --- 8. Os 7 contextos terapêuticos ---
function buildContexts() {
  const ctxs = [
    {
      label: "Dinâmica Familiar e Criação de Filhos",
      desc: "Mães, pais, filhos, sogras, avós. A família como primeiro espelho e território de aprendizado.",
    },
    {
      label: "Relacionamentos Amorosos e Sexualidade",
      desc: "Amor, parceria, sexo, escolhas, separação. Tudo que envolve escolher e ser escolhido por outro.",
    },
    {
      label: "Ansiedade, Estresse e Esgotamento",
      desc: "Quando o corpo pede calma e a cabeça não consegue parar. Cansaço, exaustão, dificuldade de relaxar.",
    },
    {
      label: "Autocrítica, Limites e Autoestima",
      desc: "Aprender a dizer não, reconhecer o próprio valor, calar o juiz interior, cuidar de si sem culpa.",
    },
    {
      label: "Sintomas Psicossomáticos e Saúde Emocional",
      desc: "Emoção e corpo: como o que sentimos vira sintoma, doença como mensagem, terapias integrativas.",
    },
    {
      label: "Produtividade, Carreira e Organização",
      desc: "Vocação, propósito, dinheiro como energia, trabalho como construção de sentido.",
    },
    {
      label: "Espiritualidade e Autoconhecimento",
      desc: "Espiritualidade no cotidiano, meditação, exercícios de proteção, autoavaliação, paz interior.",
    },
  ];

  const flowables = [
    heading("6. Os 7 contextos terapêuticos", HeadingLevel.HEADING_1),
    p("São os 7 \"territórios\" que organizam os 98 artigos. Cada um tem um nome curto e uma descrição de 1 frase. Se quiser mudar o nome ou a frase, é aqui.", { size: 22, after: 200 }),
  ];

  ctxs.forEach((c, i) => {
    const textParas = [
      p(`Contexto ${i + 1}`, { bold: true, size: 20, color: PALETTE.verdeSálvia, after: 40 }),
      p(c.label, { bold: true, size: 24, color: PALETTE.marromEscuro, after: 80 }),
      p(c.desc, { italics: true, size: 22, color: PALETTE.marromClaro, after: 60 }),
      p(`(atualmente ${countByContext(i)} artigos + práticas neste contexto)`, { italics: true, size: 18, color: PALETTE.marromClaro, after: 0 }),
    ];
    flowables.push(reviewBlock(textParas, { label: `Sua revisão do contexto ${i + 1}`, guides: 5 }));
    flowables.push(p(".", { after: 100, color: "FFFFFF" }));
  });

  flowables.push(new Paragraph({ children: [new PageBreak()] }));
  return flowables;
}

// === Distribuição aproximada de artigos por contexto (do articles.ts) ===
const ctxCounts = [48, 36, 30, 14, 8, 5, 7];
function countByContext(i) {
  return ctxCounts[i] || 0;
}

// --- 9. Saúde Mental ---
function buildSaudeMental() {
  const textParas = [
    p("Texto que está no ar em /saude-mental:", { bold: true, size: 22, color: PALETTE.terracota, after: 100 }),
    p("Kicker: \"Publicações\"", { italics: true, size: 20, color: PALETTE.marromClaro, after: 40 }),
    p("Título: \"Histórias e reflexões de consultório.\"", { bold: true, size: 26, color: PALETTE.marromEscuro, after: 80 }),
    p("Intro: \"Em mais de três décadas ouvindo as dores e angústias no meu espaço, decidi transformar as experiências dessa trajetória em conteúdos e artigos que possam ser compartilhados não só com meus pacientes, mas com todos os interessados em alcançar uma vida mais plena e íntegra — num processo de autoconhecimento conduzido com leveza, acolhimento e gentileza.\"", { size: 22, after: 80 }),
    p("Assinatura: \"— Célia Lima\"", { italics: true, size: 22, color: PALETTE.marromClaro, after: 200 }),
    p("Detalhes da página:", { bold: true, size: 22, color: PALETTE.terracota, after: 80 }),
    new Paragraph({ spacing: { before: 0, after: 40, line: 320 }, bullet: { level: 0 }, children: [tx("Tem busca por título/tema/palavra-chave", { size: 22 })] }),
    new Paragraph({ spacing: { before: 0, after: 40, line: 320 }, bullet: { level: 0 }, children: [tx("Tem filtro por contexto (dropdown com os 7)", { size: 22 })] }),
    new Paragraph({ spacing: { before: 0, after: 0, line: 320 }, bullet: { level: 0 }, children: [tx("Lista 83 artigos reflexivos em grid de 2 colunas", { size: 22 })] }),
  ];
  return [
    heading("7. Saúde Mental — página índice", HeadingLevel.HEADING_1),
    p("A página índice dos 83 artigos reflexivos. Tem um título, intro, busca e filtro por contexto.", { size: 22, after: 200 }),
    reviewBlock(textParas, { label: "Sua revisão da página Saúde Mental", guides: 10 }),
    new Paragraph({ children: [new PageBreak()] }),
  ];
}

// --- 10. Caixa de Ferramentas ---
function buildCaixaFerramentas() {
  const textParas = [
    p("Texto que está no ar em /caixa-de-ferramentas:", { bold: true, size: 22, color: PALETTE.terracota, after: 100 }),
    p("Kicker: \"Caixa de Ferramentas\" (em verde sálvia)", { italics: true, size: 20, color: PALETTE.marromClaro, after: 40 }),
    p("Título: \"O que você pode fazer agora.\"", { bold: true, size: 26, color: PALETTE.marromEscuro, after: 80 }),
    p("Subtítulo: \"Exercícios, técnicas e cuidados que você pode aplicar sozinho — respiração, florais, óleos essenciais, exercícios de proteção. Sempre como complemento, nunca como substituto do acompanhamento profissional.\"", { size: 22, after: 200 }),
    p("Detalhes da página:", { bold: true, size: 22, color: PALETTE.terracota, after: 80 }),
    new Paragraph({ spacing: { before: 0, after: 40, line: 320 }, bullet: { level: 0 }, children: [tx("Tem busca por título/tema/palavra-chave", { size: 22 })] }),
    new Paragraph({ spacing: { before: 0, after: 40, line: 320 }, bullet: { level: 0 }, children: [tx("Tem filtro por contexto (em verde sálvia)", { size: 22 })] }),
    new Paragraph({ spacing: { before: 0, after: 0, line: 320 }, bullet: { level: 0 }, children: [tx("Lista 15 práticas em grid de 2 colunas", { size: 22 })] }),
  ];
  return [
    heading("8. Caixa de Ferramentas — página índice", HeadingLevel.HEADING_1),
    p("A página índice das 15 práticas (respiração, florais, óleos, exercícios de proteção). É o que diferencia o site de um blog de psicologia comum.", { size: 22, after: 200 }),
    reviewBlock(textParas, { label: "Sua revisão da Caixa de Ferramentas", guides: 10 }),
    new Paragraph({ children: [new PageBreak()] }),
  ];
}

// --- 11. Header e Footer ---
function buildHeaderFooter() {
  const textParas = [
    p("Header (topo, fixo em todas as páginas):", { bold: true, size: 22, color: PALETTE.terracota, after: 80 }),
    p("Logo: \"Célia Lima\" + \"Psicoterapia\" ao lado (texto, não imagem)", { size: 22, after: 60 }),
    p("Menu (6 itens): Início · Sobre · Atendimento · Publicações · Caixa de Ferramentas · Contato", { size: 22, after: 60 }),
    p("Botão destacado: \"Livro\" (em terracota, leva pra /livro)", { size: 22, after: 200 }),
    p("Footer (rodapé, em todas as páginas):", { bold: true, size: 22, color: PALETTE.terracota, after: 80 }),
    p("Coluna 1 (mais larga): \"Célia Lima\" + tagline: \"Psicoterapia de orientação junguiana e psicosíntese. Um espaço para pensar a vida com mais gentileza e profundidade.\"", { size: 22, after: 60 }),
    p("Coluna 2 (Navegação): os 7 links do menu", { size: 22, after: 60 }),
    p("Coluna 3 (Contextos): os 6 contextos", { size: 22, after: 60 }),
    p("Coluna 4 (Legal): Termos · Privacidade · Direitos Autorais", { size: 22, after: 60 }),
    p("Linha do rodapé: \"© 2026 Célia Lima · Todos os direitos reservados\" + \"Conteúdo psicológico é informativo e não substitui o acompanhamento profissional.\"", { size: 22, after: 0 }),
  ];
  return [
    heading("9. Header e Footer", HeadingLevel.HEADING_1),
    p("O cabeçalho e o rodapé aparecem em todas as páginas do site. São a \"moldura\" da identidade.", { size: 22, after: 200 }),
    reviewBlock(textParas, { label: "Sua revisão do header/footer", guides: 10 }),
    new Paragraph({ children: [new PageBreak()] }),
  ];
}

// --- 12. Página Livro ---
function buildLivro() {
  const textParas = [
    p("Texto que está no ar em /livro:", { bold: true, size: 22, color: PALETTE.terracota, after: 100 }),
    p("Título: \"Caminhos do Autoconhecimento\"", { bold: true, size: 24, color: PALETTE.marromEscuro, after: 40 }),
    p("Subtítulo: \"Textos de uma trajetória terapêutica — uma reunião dos meus principais artigos publicados\"", { italics: true, size: 22, after: 80 }),
    p("Descrição: \"Uma coletânea que reúne os meus principais artigos publicados ao longo de mais de uma década de prática clínica. Organizados por áreas da vida — autoconhecimento, amor, família, saúde, trabalho e espiritualidade —, no ritmo de cada leitora e leitor.\"", { size: 22, after: 200 }),
    p("Botões:", { bold: true, size: 22, color: PALETTE.terracota, after: 40 }),
    new Paragraph({ spacing: { before: 0, after: 40, line: 320 }, bullet: { level: 0 }, children: [tx("\"Baixar PDF gratuito\" (botão terracota sólido)", { size: 22 })] }),
    new Paragraph({ spacing: { before: 0, after: 200, line: 320 }, bullet: { level: 0 }, children: [tx("\"Ler no navegador\" (link com contorno)", { size: 22 })] }),
    p("Seção \"O que tem dentro\" — agora diz \"Organizados em seis capítulos\" (sem número de páginas, sem número de textos por capítulo):", { bold: true, size: 22, color: PALETTE.terracota, after: 80 }),
    p("Os 6 capítulos como aparecem hoje (sem números de texto):", { italics: true, size: 20, color: PALETTE.marromClaro, after: 60 }),
    new Paragraph({ spacing: { before: 0, after: 40, line: 320 }, bullet: { level: 0 }, children: [tx("1. Autoconhecimento — Movimentos internos, juiz interior, carência, emoções que alimentamos.", { size: 22 })] }),
    new Paragraph({ spacing: { before: 0, after: 40, line: 320 }, bullet: { level: 0 }, children: [tx("2. Amor e Relacionamentos — Relações, escolhas, limites, codependência, sexualidade, separação.", { size: 22 })] }),
    new Paragraph({ spacing: { before: 0, after: 40, line: 320 }, bullet: { level: 0 }, children: [tx("3. Família — Mães e filhas, pais e filhos, sogras, avós, netos.", { size: 22 })] }),
    new Paragraph({ spacing: { before: 0, after: 40, line: 320 }, bullet: { level: 0 }, children: [tx("4. Saúde e Corpo — Corpo e emoção, terapias integrativas, sinais que o corpo emite.", { size: 22 })] }),
    new Paragraph({ spacing: { before: 0, after: 40, line: 320 }, bullet: { level: 0 }, children: [tx("5. Carreira, Dinheiro e Casa — Vocação, dinheiro como energia, espaço como espelho.", { size: 22 })] }),
    new Paragraph({ spacing: { before: 0, after: 0, line: 320 }, bullet: { level: 0 }, children: [tx("6. Futuro, Espiritualidade e Alimentação — Ansiedade, presença, espiritualidade no cotidiano.", { size: 22 })] }),
  ];
  return [
    heading("10. Página Livro", HeadingLevel.HEADING_1),
    p("A vitrine do livro PDF, com download gratuito e a descrição dos 6 capítulos. Obs.: a organização do site é por 7 contextos terapêuticos, mas o livro está organizado por 6 capítulos (mais antigos, da época da classificação do Personare).", { size: 22, after: 200 }),
    reviewBlock(textParas, { label: "Sua revisão da página Livro", guides: 12 }),
    new Paragraph({ children: [new PageBreak()] }),
  ];
}

// --- 13. Contato ---
function buildContato() {
  const textParas = [
    p("Texto que está no ar em /contato:", { bold: true, size: 22, color: PALETTE.terracota, after: 100 }),
    p("Título: \"Vamos conversar.\"", { bold: true, size: 26, color: PALETTE.marromEscuro, after: 80 }),
    p("Intro: \"Se algum texto tocou algo, ou se você sente que é hora de começar a terapia, escreva aqui. A Célia responde pelo WhatsApp, no tempo que a agenda permite.\"", { size: 22, after: 200 }),
    p("Card \"Como funciona\" (3 passos):", { bold: true, size: 22, color: PALETTE.terracota, after: 80 }),
    new Paragraph({ spacing: { before: 0, after: 40, line: 320 }, bullet: { level: 0 }, children: [tx("1. Você manda a primeira mensagem, sem compromisso.", { size: 22 })] }),
    new Paragraph({ spacing: { before: 0, after: 40, line: 320 }, bullet: { level: 0 }, children: [tx("2. A Célia responde e vocês combinam horário para uma conversa inicial.", { size: 22 })] }),
    new Paragraph({ spacing: { before: 0, after: 200, line: 320 }, bullet: { level: 0 }, children: [tx("3. A primeira conversa serve para você sentir se faz sentido seguir.", { size: 22 })] }),
    p("Card \"Atendimento\":", { bold: true, size: 22, color: PALETTE.terracota, after: 80 }),
    new Paragraph({ spacing: { before: 0, after: 40, line: 320 }, bullet: { level: 0 }, children: [tx("Online (videochamada) ou presencial", { size: 22 })] }),
    new Paragraph({ spacing: { before: 0, after: 40, line: 320 }, bullet: { level: 0 }, children: [tx("Sessões de 50 minutos", { size: 22 })] }),
    new Paragraph({ spacing: { before: 0, after: 40, line: 320 }, bullet: { level: 0 }, children: [tx("Segunda a sexta, horário comercial", { size: 22 })] }),
    new Paragraph({ spacing: { before: 0, after: 0, line: 320 }, bullet: { level: 0 }, children: [tx("\"O contato é feito pela própria Célia, sem secretária eletrônica.\"", { size: 22, italics: true })] }),
  ];
  return [
    heading("11. Página Contato", HeadingLevel.HEADING_1),
    p("A página de conversão: o leitor chega aqui quando quer falar com você. Tem o formulário (que monta link de WhatsApp) e cards laterais com informações práticas.", { size: 22, after: 200 }),
    reviewBlock(textParas, { label: "Sua revisão da página Contato", guides: 12 }),
    new Paragraph({ children: [new PageBreak()] }),
  ];
}

// --- 14. Páginas Legais ---
function buildLegal() {
  const textParas = [
    p("Termos de Serviço — trechos críticos:", { bold: true, size: 22, color: PALETTE.terracota, after: 80 }),
    p("§2 \"Quem é Célia Lima\": \"Célia Lima é terapeuta com formação em psicosíntese e análise junguiana (com base psicanalítica). Não é psicóloga (título protegido pela Lei 4.119/62 e Lei 5.766/71) nem psiquiatra.\"", { size: 22, after: 60 }),
    p("§2 (continuação): \"O uso do termo 'psicoterapia' neste site refere-se ao processo terapêutico em sentido amplo, reconhecido na prática clínica de terapeutas com formação em abordagens reconhecidas como a psicosíntese.\"", { size: 22, after: 200 }),
    p("Política de Privacidade — pontos principais:", { bold: true, size: 22, color: PALETTE.terracota, after: 80 }),
    p("§1 \"Dados coletados\": \"Este site não coleta dados pessoais diretamente do leitor. Não há sistema de cadastro, login, comentários ou formulário de newsletter. A leitura dos textos é anônima.\"", { size: 22, after: 60 }),
    p("§4 \"Atendimento e dados do cliente\": \"Quando você se torna cliente da Célia Lima, suas informações pessoais (nome, contato, histórico de sessões) são tratadas pela Célia diretamente, fora deste site.\"", { size: 22, after: 60 }),
    p("§5 \"Seus direitos (LGPD)\": resposta em até 15 dias corridos para exercício de direitos.", { size: 22, after: 200 }),
    p("Direitos Autorais — pontos principais:", { bold: true, size: 22, color: PALETTE.terracota, after: 80 }),
    p("§1 \"Propriedade dos textos\": \"Todos os textos publicados neste site são obra autoral de Célia Lima, protegida pela Lei 9.610/1998 (Lei de Direitos Autorais).\"", { size: 22, after: 60 }),
    p("§4 \"Uso proibido\": \"É proibido: republicar textos integrais em outros sites sem autorização; usar textos para treinar modelos de inteligência artificial; comercializar os textos ou o livro PDF; modificar, adaptar ou traduzir sem autorização.\"", { size: 22, after: 200 }),
    p("⚠️ IMPORTANTE: todas as 3 páginas têm disclaimer visível no topo: \"Este texto é um modelo gerado e precisa de revisão de advogado/contador antes da publicação oficial.\"", { italics: true, size: 22, color: PALETTE.terracota, after: 0 }),
  ];
  return [
    heading("12. Páginas Legais", HeadingLevel.HEADING_1),
    p("São 3 páginas: Termos de Serviço, Política de Privacidade, Direitos Autorais. Já estão no ar com modelos completos, mas com um disclaimer no topo: \"Este texto é um modelo gerado e precisa de revisão de advogado/contador antes da publicação oficial.\"", { size: 22, after: 200 }),
    reviewBlock(textParas, { label: "Sua revisão das páginas legais", guides: 12 }),
    new Paragraph({ children: [new PageBreak()] }),
  ];
}

// --- 15. Itens pendentes ---
function buildPending() {
  const textParas = [
    p("Foto profissional:", { bold: true, size: 22, color: PALETTE.terracota, after: 80 }),
    p("Hoje o site usa /celia.jpg e /celia-sobre.png (uma foto placeholder). Quando você tiver uma foto profissional, substituo. Não precisa ser de estúdio — qualquer foto bem-feita funciona.", { size: 22, after: 200 }),
    p("Paleta visual:", { bold: true, size: 22, color: PALETTE.terracota, after: 80 }),
    new Paragraph({ spacing: { before: 0, after: 40, line: 320 }, bullet: { level: 0 }, children: [tx("Areia (fundo): #faf6f1", { size: 22 })] }),
    new Paragraph({ spacing: { before: 0, after: 40, line: 320 }, bullet: { level: 0 }, children: [tx("Terracota (primária): #a05a3c", { size: 22 })] }),
    new Paragraph({ spacing: { before: 0, after: 40, line: 320 }, bullet: { level: 0 }, children: [tx("Verde sálvia (acento): #7a8a5b", { size: 22 })] }),
    new Paragraph({ spacing: { before: 0, after: 200, line: 320 }, bullet: { level: 0 }, children: [tx("Marrom-escuro (texto): #3d3530", { size: 22 })] }),
    p("Fontes: Cormorant Garamond (títulos) + Inter (corpo). Não consigo usar exatamente essas no PDF/Word (licença), mas no site elas renderizam perfeitamente.", { size: 22, after: 200 }),
    p("Domínio:", { bold: true, size: 22, color: PALETTE.terracota, after: 80 }),
    p("Hoje o site está rodando em domínio de teste (preview-z.ai). Para publicar oficialmente, precisa registrar um domínio. Sugestão: celialima.com.br (R$ 40/ano no Registro.br).", { size: 22, after: 200 }),
    p("Google Analytics:", { bold: true, size: 22, color: PALETTE.terracota, after: 80 }),
    p("Hoje não temos. Posso configurar Google Analytics (gratuito, com LGPD) ou Plausible (pago, mais simples e respeita privacidade por padrão). A Célia decide.", { size: 22, after: 200 }),
    p("Hospedagem:", { bold: true, size: 22, color: PALETTE.terracota, after: 80 }),
    p("Vercel (gratuito para sites pequenos). Quando publicar oficialmente, conectamos o domínio próprio e está no ar.", { size: 22, after: 0 }),
  ];
  return [
    heading("13. Itens pendentes — checklist", HeadingLevel.HEADING_1),
    p("Lista do que ainda não está 100% pronto. Marque o que você já pode providenciar e o que precisa de mais tempo.", { size: 22, after: 200 }),
    reviewBlock(textParas, { label: "Status da Célia", guides: 10 }),
    new Paragraph({ children: [new PageBreak()] }),
  ];
}

// --- 16. Notas livres ---
function buildFreeNotes() {
  const flowables = [
    heading("14. Notas livres", HeadingLevel.HEADING_1),
    p("Use estas páginas para anotar o que não se encaixou nas seções anteriores — ideias, dúvidas, sensações, pedidos que vieram durante a leitura. Não há formato certo: escreva como vier.", { size: 22, after: 200 }),
  ];
  // 3 páginas de linhas-guia (texto sublinhado com caractere invisível)
  for (let pg = 0; pg < 3; pg++) {
    for (let i = 0; i < 14; i++) {
      // Cada linha é um longo text run de espaços com um "." no fim (cor branca) para ter conteúdo
      flowables.push(
        new Paragraph({
          spacing: { before: 0, after: 200, line: 320 },
          children: [
            new TextRun({
              text: "                                                                                        .",
              font: FONT_BODY,
              size: 22,
              underline: { type: "single", color: "838179" },
              color: "FFFFFF",
            }),
          ],
        })
      );
    }
    if (pg < 2) {
      flowables.push(new Paragraph({ children: [new PageBreak()] }));
    }
  }
  return flowables;
}

// === Build ===
async function main() {
  const OUT = "/home/z/my-project/download/Manual-Revisao-Site-Celia-Lima.docx";

  const sections = [
    // Section 1: Capa (sem header/footer)
    {
      properties: {
        page: {
          size: { width: 11906, height: 16838, orientation: PageOrientation.PORTRAIT },
          margin: { top: 1440, bottom: 1440, left: 1701, right: 1417 },
        },
      },
      children: buildCover(),
    },
    // Section 2: Corpo (com header + footer)
    {
      properties: {
        page: {
          size: { width: 11906, height: 16838, orientation: PageOrientation.PORTRAIT },
          margin: { top: 1440, bottom: 1440, left: 1417, right: 1417 },
          pageNumbers: { start: 1, formatType: NumberFormat.DECIMAL },
        },
      },
      headers: {
        default: new Header({
          children: [
            new Paragraph({
              alignment: AlignmentType.LEFT,
              border: {
                bottom: { style: BorderStyle.SINGLE, size: 4, color: PALETTE.borda, space: 4 },
              },
              spacing: { before: 0, after: 80, line: 320 },
              children: [
                new TextRun({
                  text: "Manual de Revisão do Site",
                  font: FONT_BODY,
                  color: PALETTE.marromClaro,
                  size: 18,
                  italics: true,
                }),
                new TextRun({ text: "\t", font: FONT_BODY, size: 18 }),
                new TextRun({
                  text: "Célia Lima",
                  font: FONT_BODY,
                  color: PALETTE.terracota,
                  size: 18,
                  bold: true,
                }),
              ],
            }),
          ],
        }),
      },
      footers: {
        default: new Footer({
          children: [
            new Paragraph({
              alignment: AlignmentType.CENTER,
              border: {
                top: { style: BorderStyle.SINGLE, size: 4, color: PALETTE.borda, space: 4 },
              },
              spacing: { before: 80, after: 0, line: 320 },
              children: [
                new TextRun({
                  children: [PageNumber.CURRENT],
                  font: FONT_BODY,
                  color: PALETTE.marromClaro,
                  size: 18,
                }),
              ],
            }),
          ],
        }),
      },
      children: [
        ...buildHowToUse(),
        ...buildIdentity(),
        ...buildHomeHero(),
        ...buildHomeContexts(),
        ...buildSobre(),
        ...buildAtendimento(),
        ...buildContexts(),
        ...buildSaudeMental(),
        ...buildCaixaFerramentas(),
        ...buildHeaderFooter(),
        ...buildLivro(),
        ...buildContato(),
        ...buildLegal(),
        ...buildPending(),
        ...buildFreeNotes(),
      ],
    },
  ];

  const doc = new Document({
    creator: "Célia Lima",
    title: "Manual de Revisão do Site — Célia Lima",
    description:
      "Manual de trabalho para revisão dos textos e da estrutura do site celialima.com.br.",
    styles: {
      default: {
        document: {
          run: { font: FONT_BODY, size: 22, color: PALETTE.marromEscuro },
          paragraph: { spacing: { line: 320 } },
        },
      },
    },
    sections,
  });

  const buf = await Packer.toBuffer(doc);
  fs.writeFileSync(OUT, buf);
  console.log(`[ok] ${OUT}`);
  console.log(`     ${fs.statSync(OUT).size / 1024} KB`);
}

main().catch((err) => {
  console.error(err);
  process.exit(1);
});
