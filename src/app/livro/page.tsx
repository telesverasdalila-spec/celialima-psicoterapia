import Link from "next/link";
import { BookOpen, Download, FileText } from "lucide-react";

export const metadata = {
  title: "Livro — Caminhos do Autoconhecimento",
  description:
    "Baixe gratuitamente o livro 'Caminhos do Autoconhecimento', uma reunião dos meus principais artigos publicados ao longo de mais de uma década de prática clínica. PDF gratuito.",
};

export default function LivroPage() {
  return (
    <div className="flex flex-col">
      {/* Hero do livro */}
      <section className="border-b border-border bg-muted/20">
        <div className="mx-auto max-w-5xl px-6 lg:px-8 py-20 md:py-28">
          <div className="grid md:grid-cols-[1fr_2fr] gap-12 items-center">
            <div className="relative">
              <div className="relative aspect-[3/4] w-full max-w-xs mx-auto">
                <div className="absolute inset-0 -rotate-3 bg-accent/20 rounded-sm shadow-lg" />
                <div className="absolute inset-0 rotate-1 bg-primary/10 rounded-sm shadow-md" />
                <div className="relative h-full w-full bg-card border border-border rounded-sm shadow-lg flex flex-col items-center justify-center p-8">
                  <BookOpen size={48} className="text-primary mb-4" />
                  <p
                    className="text-xs uppercase tracking-[0.2em] text-primary mb-2"
                  >
                    Coletânea Terapêutica
                  </p>
                  <h3
                    className="text-2xl text-foreground text-center mb-2"
                    style={{ fontFamily: 'var(--font-cormorant)', fontWeight: 500 }}
                  >
                    Caminhos do<br/><em className="text-primary italic">Autoconhecimento</em>
                  </h3>
                  <p className="text-sm text-muted-foreground italic text-center mt-4">
                    Célia Lima
                  </p>
                  <p className="text-xs text-muted-foreground mt-2">Edição 2026</p>
                </div>
              </div>
            </div>

            <div>
              <p className="text-xs uppercase tracking-[0.25em] text-primary mb-5">
                Livro gratuito
              </p>
              <h1
                className="text-4xl md:text-5xl text-foreground leading-[1.1] mb-6"
                style={{ fontFamily: 'var(--font-cormorant)', fontWeight: 500 }}
              >
                Caminhos do Autoconhecimento
              </h1>
              <p className="text-lg text-muted-foreground italic leading-relaxed mb-6">
                Textos de uma trajetória terapêutica — uma reunião dos meus principais artigos publicados
              </p>
              <p className="text-base text-foreground/85 leading-relaxed mb-8">
                Uma coletânea que reúne os meus principais artigos publicados ao longo de mais de
                uma década de prática clínica. Organizados por áreas da vida —
                autoconhecimento, amor, família, saúde, trabalho e
                espiritualidade —, no ritmo de cada leitora e leitor.
              </p>
              <div className="flex flex-wrap gap-4">
                <Link
                  href="/Celia-Lima-Caminhos-do-Autoconhecimento.pdf"
                  className="inline-flex items-center gap-2 px-6 py-3 bg-primary text-primary-foreground rounded-full text-sm font-medium hover:bg-primary/90 transition-colors"
                  download
                >
                  <Download size={16} />
                  Baixar PDF gratuito
                </Link>
                <a
                  href="/Celia-Lima-Caminhos-do-Autoconhecimento.pdf"
                  target="_blank"
                  rel="noopener noreferrer"
                  className="inline-flex items-center gap-2 px-6 py-3 border border-border text-foreground rounded-full text-sm font-medium hover:border-primary hover:text-primary transition-colors"
                >
                  <FileText size={16} />
                  Ler no navegador
                </a>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* O que tem no livro */}
      <section className="border-b border-border">
        <div className="mx-auto max-w-5xl px-6 lg:px-8 py-16 md:py-20">
          <p className="text-xs uppercase tracking-[0.25em] text-primary mb-4">
            O que tem dentro
          </p>
          <h2
            className="text-3xl md:text-4xl text-foreground mb-10"
            style={{ fontFamily: 'var(--font-cormorant)', fontWeight: 500 }}
          >
            Organizados em seis capítulos.
          </h2>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            {[
              { titulo: "Autoconhecimento", descricao: "Movimentos internos, juiz interior, carência, emoções que alimentamos." },
              { titulo: "Amor e Relacionamentos", descricao: "Relações, escolhas, limites, codependência, sexualidade, separação." },
              { titulo: "Família", descricao: "Mães e filhas, pais e filhos, sogras, avós, netos." },
              { titulo: "Saúde e Corpo", descricao: "Corpo e emoção, terapias integrativas, sinais que o corpo emite." },
              { titulo: "Carreira, Dinheiro e Casa", descricao: "Vocação, dinheiro como energia, espaço como espelho." },
              { titulo: "Futuro, Espiritualidade e Alimentação", descricao: "Ansiedade, presença, espiritualidade no cotidiano." },
            ].map((cap, i) => (
              <div key={i} className="p-5 bg-muted/30 rounded-sm border border-border">
                <h3
                  className="text-xl text-foreground mb-2"
                  style={{ fontFamily: 'var(--font-cormorant)', fontWeight: 500 }}
                >
                  {cap.titulo}
                </h3>
                <p className="text-sm text-muted-foreground leading-relaxed">
                  {cap.descricao}
                </p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Sobre o livro */}
      <section className="border-b border-border bg-muted/20">
        <div className="mx-auto max-w-3xl px-6 lg:px-8 py-16 md:py-20">
          <h2
            className="text-2xl md:text-3xl text-foreground mb-6"
            style={{ fontFamily: 'var(--font-cormorant)', fontWeight: 500 }}
          >
            Sobre o livro.
          </h2>
          <div className="space-y-4 text-base text-foreground/85 leading-relaxed">
            <p>
              "Caminhos do Autoconhecimento" reúne os textos que publiquei
              ao longo de mais de quinze anos de prática como psicoterapeuta.
              São artigos que percorrem o arco de uma trajetória dedicada
              a acompanhar pessoas em seus processos emocionais.
            </p>
            <p>
              Minha escrita tem o tom do consultório: direto, acolhedor,
              sem jargão. Cada texto parte de uma situação concreta — uma dor,
              uma pergunta, um impasse — e aí encontra o fio para conversar
              sobre o que está em jogo.
            </p>
            <p>
              Esta coletânea foi montada em 2026 a partir do acervo que publiquei
              originalmente na plataforma Personare. Os textos são apresentados
              em sua forma integral, sem alterações de conteúdo — apenas com a
              revisão mínima necessária à publicação em livro. A ordem dentro
              de cada capítulo é cronológica, para que o leitor possa acompanhar
              a maturação das ideias ao longo do tempo.
            </p>
          </div>
        </div>
      </section>

      {/* CTA */}
      <section className="bg-primary text-primary-foreground">
        <div className="mx-auto max-w-3xl px-6 lg:px-8 py-16 md:py-20 text-center">
          <h2
            className="text-2xl md:text-3xl mb-5 leading-tight"
            style={{ fontFamily: 'var(--font-cormorant)', fontWeight: 500 }}
          >
            Baixe e leia com calma.
          </h2>
          <p className="text-primary-foreground/90 leading-relaxed mb-7 max-w-xl mx-auto">
            O livro é gratuito. Se algum texto abrir uma pergunta, considere
            voltar aqui para conversar.
          </p>
          <Link
            href="/Celia-Lima-Caminhos-do-Autoconhecimento.pdf"
            download
            className="inline-flex items-center gap-2 px-6 py-3 bg-primary-foreground text-primary rounded-full text-sm font-medium hover:bg-primary-foreground/90 transition-colors"
          >
            <Download size={16} />
            Baixar PDF gratuito
          </Link>
        </div>
      </section>
    </div>
  );
}
