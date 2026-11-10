import Link from "next/link";
import Image from "next/image";
import { ArrowRight, MessageCircle, BookOpen } from "lucide-react";
import { HeroStagger, HeroItem, FadeIn } from "@/components/home/motion";
import {
  contexts,
  getRecentArtigos,
  getPraticasRelacionadas,
} from "@/lib/articles";

/* ---------------------------------------------------------------------------
 * Bento config — 7 contextos + card de citação (8 total)
 *
 * Layout no desktop (grid lg: 4 cols):
 *  Row 1 — Citação Tom Zé     (col-span-4)  · full width
 *  Row 2 — ctx[0] + ctx[1]    (col-span-2 + col-span-2) · featured
 *  Row 3 — ctx[2] + ctx[3] + ctx[4]  (1 + 1 + 2)         · compact + compact + featured
 *  Row 4 — ctx[5] + ctx[6]    (col-span-2 + col-span-2) · featured
 *
 * No tablet (md: 2 cols): citação full, demais col-span-1 (par a par)
 * No mobile: tudo stacked em 1 col
 * ------------------------------------------------------------------------- */

type BentoCfg = { span: string; featured: boolean };

const bentoConfig: BentoCfg[] = [
  { span: "lg:col-span-2", featured: true },   // 0 — Dinâmica Familiar
  { span: "lg:col-span-2", featured: true },   // 1 — Relacionamentos
  { span: "lg:col-span-1", featured: false },  // 2 — Ansiedade (compact)
  { span: "lg:col-span-1", featured: false },  // 3 — Autocrítica (compact)
  { span: "lg:col-span-2", featured: true },   // 4 — Psicossomáticos
  { span: "lg:col-span-2", featured: true },   // 5 — Produtividade
  { span: "lg:col-span-2", featured: true },   // 6 — Espiritualidade
];

export default function Home() {
  const artigoDaSemana = getRecentArtigos(1)[0];
  const praticaCoerente = artigoDaSemana
    ? getPraticasRelacionadas(artigoDaSemana, 1)[0]
    : undefined;

  return (
    <div className="flex flex-col">
      {/* ===================================================================
          HERO — imagem de fundo + overlay rico + orbs + fade-in escalonado
      =================================================================== */}
      <section className="relative overflow-hidden">
        <div className="absolute inset-0">
          <Image
            src="/hero-fundo.svg"
            alt=""
            fill
            className="object-cover"
            sizes="100vw"
            priority
          />
          {/* Gradientes em camadas pra profundidade (não mais overlay sólido) */}
          <div className="absolute inset-0 bg-gradient-to-b from-background/35 via-background/55 to-background/92" />
          <div className="absolute inset-0 bg-gradient-to-tr from-primary/12 via-transparent to-accent/12" />
          {/* Orbs decorativos — luz suave nas extremidades */}
          <div
            className="absolute -top-24 -right-24 w-[28rem] h-[28rem] rounded-full bg-primary/15 blur-3xl pointer-events-none"
            aria-hidden="true"
          />
          <div
            className="absolute -bottom-32 -left-24 w-[26rem] h-[26rem] rounded-full bg-accent/15 blur-3xl pointer-events-none"
            aria-hidden="true"
          />
        </div>

        <HeroStagger className="relative mx-auto max-w-4xl px-6 lg:px-8 py-32 md:py-44 text-center">
          <HeroItem className="text-xs uppercase tracking-[0.25em] text-primary mb-6">
            <p>Psicoterapia · Autoconhecimento</p>
          </HeroItem>

          <HeroItem className="text-5xl md:text-6xl lg:text-7xl text-foreground leading-[1.05] mb-8">
            <h1 style={{ fontFamily: "var(--font-cormorant)", fontWeight: 500 }}>
              Um espaço para
              <span className="block italic text-primary">pensar a vida</span>
              <span className="block">com mais gentileza.</span>
            </h1>
          </HeroItem>

          <HeroItem className="text-lg md:text-xl text-foreground/80 leading-relaxed mb-10 max-w-2xl mx-auto">
            <p>
              Psicoterapia e práticas que conversam com você sobre amor,
              família, corpo, trabalho e espiritualidade — no ritmo próprio de
              cada jornada.
            </p>
          </HeroItem>

          <HeroItem className="flex flex-wrap gap-4 justify-center">
            <Link
              href="/contato"
              className="inline-flex items-center gap-2 px-6 py-3 bg-primary text-primary-foreground rounded-full text-sm font-medium shadow-md transition-all hover:scale-[1.04] active:scale-[0.98] hover:bg-primary/90"
            >
              <MessageCircle size={16} />
              Agendar conversa
            </Link>
            <Link
              href="/atendimento"
              className="inline-flex items-center gap-2 px-6 py-3 border border-primary/40 text-primary bg-background/70 backdrop-blur-sm rounded-full text-sm font-medium transition-all hover:scale-[1.04] active:scale-[0.98] hover:bg-primary hover:text-primary-foreground"
            >
              Conheça meu trabalho
              <ArrowRight size={16} />
            </Link>
          </HeroItem>
        </HeroStagger>
      </section>

      {/* ===================================================================
          BENTO GRID — Citação + 7 contextos
      =================================================================== */}
      <section className="relative border-b border-border bg-muted/20 overflow-hidden">
        {/* Orbs decorativos de fundo */}
        <div
          className="absolute top-32 -left-40 w-96 h-96 rounded-full bg-primary/5 blur-3xl pointer-events-none"
          aria-hidden="true"
        />
        <div
          className="absolute bottom-40 -right-40 w-96 h-96 rounded-full bg-accent/5 blur-3xl pointer-events-none"
          aria-hidden="true"
        />

        <div className="relative mx-auto max-w-6xl px-6 lg:px-8 py-20 md:py-24">
          {/* Cabeçalho da seção */}
          <FadeIn className="mb-12 max-w-2xl">
            <p className="text-xs uppercase tracking-[0.25em] text-primary mb-4">
              Por onde começar
            </p>
            <h2
              className="text-3xl md:text-4xl text-foreground mb-4"
              style={{ fontFamily: "var(--font-cormorant)", fontWeight: 500 }}
            >
              O que te trouxe aqui?
            </h2>
            <p className="text-muted-foreground leading-relaxed">
              Cada contexto reúne textos e práticas que conversam com uma dor,
              uma pergunta ou um momento da vida. Comece pela epígrafe — e
              escolha o que ressoa.
            </p>
          </FadeIn>

          {/* Bento grid */}
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-5 items-stretch">
            {/* Card especial: citação do Tom Zé — full width */}
            <FadeIn className="md:col-span-2 lg:col-span-4">
              <div className="glass-card-strong rounded-xl p-8 md:p-12 flex flex-col justify-center relative overflow-hidden h-full min-h-[180px]">
                <span
                  className="absolute top-1 left-6 md:left-10 text-8xl text-primary/25 leading-none select-none pointer-events-none"
                  style={{ fontFamily: "var(--font-cormorant)" }}
                  aria-hidden="true"
                >
                  &ldquo;
                </span>
                <p
                  className="text-xl md:text-3xl text-foreground leading-relaxed italic relative z-10 max-w-4xl"
                  style={{ fontFamily: "var(--font-cormorant)", fontWeight: 500 }}
                >
                  Ao persistirem os médicos, os sintomas deverão ser consultados.
                </p>
                <p
                  className="text-sm md:text-base text-muted-foreground italic mt-4 relative z-10"
                  style={{ fontFamily: "var(--font-cormorant)", fontWeight: 400 }}
                >
                  &mdash; Tom Zé
                </p>
              </div>
            </FadeIn>

            {/* Cards de contexto (bento) */}
            {contexts.map((ctx, i) => {
              const cfg = bentoConfig[i] ?? { span: "lg:col-span-1", featured: false };
              // Alterna lado da imagem nos cards featured — espelhamento visual
              const imgRight = i % 2 === 0;

              return (
                <FadeIn key={ctx.slug} className={cfg.span} delay={(i % 3) * 0.06}>
                  <Link
                    href={`/contextos/${ctx.slug}`}
                    className="group glass-card lift-on-hover rounded-xl overflow-hidden flex flex-col md:flex-row h-full min-h-[260px] block"
                  >
                    {/* Imagem (à direita ou à esquerda, alternando) */}
                    <div
                      className={`relative flex-shrink-0 ${
                        cfg.featured
                          ? "w-full md:w-2/5 h-32 md:h-auto min-h-[8rem]"
                          : "w-full h-36 md:h-40"
                      } ${imgRight ? "md:order-2" : "md:order-1"}`}
                    >
                      <Image
                        src={`/contextos/${ctx.slug}.svg`}
                        alt=""
                        fill
                        className="object-cover"
                        sizes={
                          cfg.featured
                            ? "(max-width: 768px) 100vw, 40vw"
                            : "(max-width: 768px) 100vw, 25vw"
                        }
                      />
                      {/* Gradient overlay que mistura imagem no vidro */}
                      <div
                        className={`absolute inset-0 ${
                          imgRight
                            ? "bg-gradient-to-l from-transparent via-white/5 to-white/30"
                            : "bg-gradient-to-r from-transparent via-white/5 to-white/30"
                        } pointer-events-none`}
                        aria-hidden="true"
                      />
                    </div>

                    {/* Conteúdo */}
                    <div
                      className={`flex-1 p-5 md:p-6 flex flex-col justify-center ${
                        imgRight ? "md:order-1" : "md:order-2"
                      }`}
                    >
                      <h3
                        className={`text-foreground mb-2 group-hover:text-primary transition-colors ${
                          cfg.featured ? "text-xl md:text-2xl" : "text-lg"
                        }`}
                        style={{ fontFamily: "var(--font-cormorant)", fontWeight: 500 }}
                      >
                        {ctx.label}
                      </h3>
                      <p className="text-sm text-muted-foreground leading-relaxed line-clamp-3 mb-3">
                        {ctx.description}
                      </p>
                      <p className="inline-flex items-center gap-1 text-xs text-primary opacity-0 group-hover:opacity-100 transition-opacity">
                        Explorar <ArrowRight size={12} />
                      </p>
                    </div>
                  </Link>
                </FadeIn>
              );
            })}
          </div>
        </div>
      </section>

      {/* ===================================================================
          ARTIGO DA SEMANA + PRÁTICA COERENTE
      =================================================================== */}
      {artigoDaSemana && (
        <section className="relative border-b border-border overflow-hidden">
          <div
            className="absolute top-20 right-0 w-72 h-72 rounded-full bg-primary/5 blur-3xl pointer-events-none"
            aria-hidden="true"
          />
          <div className="relative mx-auto max-w-6xl px-6 lg:px-8 py-20 md:py-24">
            <FadeIn>
              <p className="text-xs uppercase tracking-[0.25em] text-primary mb-4">
                Publicação da semana
              </p>
              <h2
                className="text-3xl md:text-4xl text-foreground mb-12"
                style={{ fontFamily: "var(--font-cormorant)", fontWeight: 500 }}
              >
                Para começar a ler.
              </h2>
            </FadeIn>

            <div className="grid md:grid-cols-2 gap-8">
              {/* Artigo da semana — glass card forte (texto longo) */}
              <FadeIn delay={0.05}>
                <Link
                  href={`/saude-mental/${artigoDaSemana.slug}`}
                  className="group glass-card-strong lift-on-hover rounded-xl block p-8 h-full"
                >
                  <p className="text-xs uppercase tracking-[0.2em] text-primary mb-3">
                    Publicação · {artigoDaSemana.contextLabels[0]}
                  </p>
                  <h3
                    className="text-2xl md:text-3xl text-foreground mb-4 group-hover:text-primary transition-colors leading-snug"
                    style={{ fontFamily: "var(--font-cormorant)", fontWeight: 500 }}
                  >
                    {artigoDaSemana.title}
                  </h3>
                  <p className="text-base text-muted-foreground leading-relaxed mb-4 line-clamp-4">
                    {artigoDaSemana.summary}
                  </p>
                  <div className="mt-auto flex items-center gap-3 text-xs text-muted-foreground">
                    <span>{artigoDaSemana.dateDisplay}</span>
                    <span aria-hidden="true">·</span>
                    <span>{artigoDaSemana.readTime} min de leitura</span>
                  </div>
                </Link>
              </FadeIn>

              {/* Prática coerente — verde sálvia com tratamento glass */}
              {praticaCoerente && (
                <FadeIn delay={0.12}>
                  <Link
                    href={`/caixa-de-ferramentas/${praticaCoerente.slug}`}
                    className="group rounded-xl block p-8 h-full border border-accent/30 bg-accent/15 backdrop-blur-md transition-all hover:border-accent/60 hover:-translate-y-1 hover:shadow-lg"
                    style={{ boxShadow: "0 10px 30px -14px rgb(122 138 91 / 0.25)" }}
                  >
                    <p className="text-xs uppercase tracking-[0.2em] text-accent mb-3">
                      Da Caixa de Ferramentas · para fazer agora
                    </p>
                    <h3
                      className="text-2xl md:text-3xl text-foreground mb-4 group-hover:text-accent transition-colors leading-snug"
                      style={{ fontFamily: "var(--font-cormorant)", fontWeight: 500 }}
                    >
                      {praticaCoerente.title}
                    </h3>
                    <p className="text-base text-muted-foreground leading-relaxed mb-4 line-clamp-4">
                      {praticaCoerente.summary}
                    </p>
                    <div className="mt-auto flex items-center gap-3 text-xs text-muted-foreground">
                      <span>{praticaCoerente.readTime} min de prática</span>
                    </div>
                  </Link>
                </FadeIn>
              )}
            </div>
          </div>
        </section>
      )}

      {/* ===================================================================
          CTA LIVRO + WHATSAPP
      =================================================================== */}
      <section className="relative border-b border-border bg-muted/30 overflow-hidden">
        <div
          className="absolute -bottom-20 left-1/4 w-80 h-80 rounded-full bg-primary/5 blur-3xl pointer-events-none"
          aria-hidden="true"
        />
        <div className="relative mx-auto max-w-6xl px-6 lg:px-8 py-16 md:py-20">
          <div className="grid md:grid-cols-2 gap-8">
            {/* Card do livro — glass card leve */}
            <FadeIn>
              <Link
                href="/livro"
                className="group glass-card lift-on-hover rounded-xl block p-8 h-full"
              >
                <BookOpen size={28} className="text-primary mb-4" />
                <h3
                  className="text-2xl text-foreground mb-3 group-hover:text-primary transition-colors"
                  style={{ fontFamily: "var(--font-cormorant)", fontWeight: 500 }}
                >
                  Caminhos do Autoconhecimento
                </h3>
                <p className="text-sm text-muted-foreground leading-relaxed mb-4">
                  Uma reunião dos meus principais artigos publicados ao longo de
                  mais de uma década de prática clínica. Download gratuito.
                </p>
                <p className="inline-flex items-center gap-1 text-xs text-primary">
                  Baixar PDF gratuito <ArrowRight size={12} />
                </p>
              </Link>
            </FadeIn>

            {/* Card WhatsApp — terracota sólido com orb decorativo */}
            <FadeIn
              delay={0.08}
              className="relative rounded-xl p-8 bg-primary text-primary-foreground overflow-hidden"
            >
              <div
                className="absolute -top-12 -right-12 w-48 h-48 rounded-full bg-primary-foreground/10 blur-2xl pointer-events-none"
                aria-hidden="true"
              />
              <div className="relative">
                <MessageCircle size={28} className="mb-4" />
                <h3
                  className="text-2xl mb-3"
                  style={{ fontFamily: "var(--font-cormorant)", fontWeight: 500 }}
                >
                  A leitura abriu alguma pergunta?
                </h3>
                <p className="text-sm text-primary-foreground/90 leading-relaxed mb-5">
                  Se algum texto tocou algo que você quer explorar com mais
                  atenção, considere uma conversa inicial. Sem compromisso, sem
                  pressa.
                </p>
                <Link
                  href="/contato"
                  className="inline-flex items-center gap-2 px-5 py-2.5 bg-primary-foreground text-primary rounded-full text-sm font-medium transition-all hover:scale-[1.04] active:scale-[0.98] hover:bg-primary-foreground/90"
                >
                  <MessageCircle size={14} />
                  Falar comigo
                </Link>
              </div>
            </FadeIn>
          </div>
        </div>
      </section>
    </div>
  );
}
