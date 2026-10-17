import Link from "next/link";
import Image from "next/image";
import { ArrowRight, MessageCircle, BookOpen } from "lucide-react";
import {
  contexts,
  getRecentArtigos,
  getPraticasRelacionadas,
} from "@/lib/articles";

export default function Home() {
  const artigoDaSemana = getRecentArtigos(1)[0];
  const praticaCoerente = artigoDaSemana ? getPraticasRelacionadas(artigoDaSemana, 1)[0] : undefined;

  return (
    <div className="flex flex-col">
      {/* HERO com imagem de fundo + overlay */}
      <section className="relative overflow-hidden">
        {/* Imagem de fundo */}
        <div className="absolute inset-0">
          <Image
            src="/hero-fundo.svg"
            alt=""
            fill
            className="object-cover"
            sizes="100vw"
            priority
          />
          {/* Overlay — escurece sutilmente pra texto legível */}
          <div className="absolute inset-0 bg-background/55" />
          {/* Overlay com gradiente pra profundidade */}
          <div className="absolute inset-0 bg-gradient-to-b from-background/30 via-background/40 to-background/85" />
        </div>

        {/* Conteúdo do hero */}
        <div className="relative mx-auto max-w-4xl px-6 lg:px-8 py-32 md:py-44 text-center">
          <p className="text-xs uppercase tracking-[0.25em] text-primary mb-6">
            Psicoterapia · Autoconhecimento
          </p>
          <h1
            className="text-5xl md:text-6xl lg:text-7xl text-foreground leading-[1.05] mb-8"
            style={{ fontFamily: 'var(--font-cormorant)', fontWeight: 500 }}
          >
            Um espaço para
            <span className="block italic text-primary">pensar a vida</span>
            <span className="block">com mais gentileza.</span>
          </h1>
          <p className="text-lg md:text-xl text-muted-foreground leading-relaxed mb-10 max-w-2xl mx-auto">
            Psicoterapia e práticas que conversam com você sobre amor, família,
            corpo, trabalho e espiritualidade — no ritmo próprio de cada jornada.
          </p>
          <div className="flex flex-wrap gap-4 justify-center">
            <Link
              href="/contato"
              className="inline-flex items-center gap-2 px-6 py-3 bg-primary text-primary-foreground rounded-full text-sm font-medium hover:bg-primary/90 transition-colors shadow-md"
            >
              <MessageCircle size={16} />
              Agendar conversa
            </Link>
            <Link
              href="/atendimento"
              className="inline-flex items-center gap-2 px-6 py-3 border border-primary/40 text-primary bg-background/70 backdrop-blur-sm rounded-full text-sm font-medium hover:bg-primary hover:text-primary-foreground transition-colors"
            >
              Conheça meu trabalho
              <ArrowRight size={16} />
            </Link>
          </div>
        </div>
      </section>

      {/* 6 CARDS DE CONTEXTO — com imagem à esquerda */}
      <section className="border-b border-border bg-muted/20">
        <div className="mx-auto max-w-6xl px-6 lg:px-8 py-20 md:py-24">
          <div className="mb-12 max-w-2xl">
            <p className="text-xs uppercase tracking-[0.25em] text-primary mb-4">
              Por onde começar
            </p>
            <h2
              className="text-3xl md:text-4xl text-foreground mb-4"
              style={{ fontFamily: 'var(--font-cormorant)', fontWeight: 500 }}
            >
              O que te trouxe aqui?
            </h2>
            <p className="text-muted-foreground leading-relaxed">
              Cada contexto reúne textos e práticas que conversam com uma dor,
              uma pergunta ou um momento da vida. Comece pela epígrafe — e
              escolha o que ressoa.
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            {/* Card especial: citação do Tom Zé (primeira posição, sem moldura) */}
            <div className="p-6 bg-secondary rounded-sm flex flex-col justify-center h-[176px]">
              <p
                className="text-5xl text-primary leading-none mb-2"
                style={{ fontFamily: 'var(--font-cormorant)', fontWeight: 500 }}
                aria-hidden="true"
              >
                &ldquo;
              </p>
              <p
                className="text-xl md:text-2xl text-foreground leading-relaxed italic"
                style={{ fontFamily: 'var(--font-cormorant)', fontWeight: 500 }}
              >
                Ao persistirem os médicos, os sintomas deverão ser consultados.
              </p>
              <p
                className="text-sm text-muted-foreground italic mt-3"
                style={{ fontFamily: 'var(--font-cormorant)', fontWeight: 400 }}
              >
                &mdash; Tom Zé
              </p>
            </div>

            {contexts.map((ctx, i) => {
              // Alterna lado: cards em posição par (0, 2, 4, 6) = imagem à direita
              //                cards em posição ímpar (1, 3, 5) = imagem à esquerda
              // Cria "espelhamento" visual ao longo das colunas
              const imgRight = i % 2 === 0;
              return (
                <Link
                  key={ctx.slug}
                  href={`/contextos/${ctx.slug}`}
                  className="group flex bg-card rounded-sm border border-border hover:border-primary/40 transition-all hover:shadow-sm overflow-hidden h-[176px]"
                >
                  {/* Imagem (à direita ou à esquerda, alternando) */}
                  <div
                    className={`relative w-32 flex-shrink-0 ${imgRight ? 'order-2' : 'order-1'}`}
                  >
                    <Image
                      src={`/contextos/${ctx.slug}.svg`}
                      alt=""
                      fill
                      className="object-cover"
                      sizes="128px"
                    />
                  </div>
                  {/* Conteúdo */}
                  <div className={`flex-1 p-5 flex flex-col justify-center ${imgRight ? 'order-1' : 'order-2'}`}>
                    <h3
                      className="text-xl text-foreground mb-2 group-hover:text-primary transition-colors"
                      style={{ fontFamily: 'var(--font-cormorant)', fontWeight: 500 }}
                    >
                      {ctx.label}
                    </h3>
                    <p className="text-sm text-muted-foreground leading-relaxed line-clamp-3">
                      {ctx.description}
                    </p>
                    <p className="mt-3 inline-flex items-center gap-1 text-xs text-primary opacity-0 group-hover:opacity-100 transition-opacity">
                      Explorar <ArrowRight size={12} />
                    </p>
                  </div>
                </Link>
              );
            })}
          </div>
        </div>
      </section>

      {/* ARTIGO DA SEMANA + PRÁTICA COERENTE */}
      {artigoDaSemana && (
        <section className="border-b border-border">
          <div className="mx-auto max-w-6xl px-6 lg:px-8 py-20 md:py-24">
            <p className="text-xs uppercase tracking-[0.25em] text-primary mb-4">
              Publicação da semana
            </p>
            <h2
              className="text-3xl md:text-4xl text-foreground mb-12"
              style={{ fontFamily: 'var(--font-cormorant)', fontWeight: 500 }}
            >
              Para começar a ler.
            </h2>

            <div className="grid md:grid-cols-2 gap-8">
              <Link
                href={`/saude-mental/${artigoDaSemana.slug}`}
                className="group p-8 bg-card rounded-sm border border-border hover:border-primary/40 transition-all"
              >
                <p className="text-xs uppercase tracking-[0.2em] text-primary mb-3">
                  Publicação · {artigoDaSemana.contextLabels[0]}
                </p>
                <h3
                  className="text-2xl md:text-3xl text-foreground mb-4 group-hover:text-primary transition-colors leading-snug"
                  style={{ fontFamily: 'var(--font-cormorant)', fontWeight: 500 }}
                >
                  {artigoDaSemana.title}
                </h3>
                <p className="text-base text-muted-foreground leading-relaxed mb-4 line-clamp-4">
                  {artigoDaSemana.summary}
                </p>
                <div className="mt-auto flex items-center gap-3 text-xs text-muted-foreground">
                  <span>{artigoDaSemana.dateDisplay}</span>
                  <span>·</span>
                  <span>{artigoDaSemana.readTime} min de leitura</span>
                </div>
              </Link>

              {praticaCoerente && (
                <Link
                  href={`/caixa-de-ferramentas/${praticaCoerente.slug}`}
                  className="group p-8 bg-accent/10 rounded-sm border border-accent/30 hover:border-accent transition-all"
                >
                  <p className="text-xs uppercase tracking-[0.2em] text-accent mb-3">
                    Da Caixa de Ferramentas · para fazer agora
                  </p>
                  <h3
                    className="text-2xl md:text-3xl text-foreground mb-4 group-hover:text-accent transition-colors leading-snug"
                    style={{ fontFamily: 'var(--font-cormorant)', fontWeight: 500 }}
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
              )}
            </div>
          </div>
        </section>
      )}

      {/* CTA LIVRO + WHATSAPP */}
      <section className="border-b border-border bg-muted/30">
        <div className="mx-auto max-w-6xl px-6 lg:px-8 py-16 md:py-20">
          <div className="grid md:grid-cols-2 gap-8">
            <Link
              href="/livro"
              className="group p-8 bg-card rounded-sm border border-border hover:border-primary/40 transition-all"
            >
              <BookOpen size={28} className="text-primary mb-4" />
              <h3
                className="text-2xl text-foreground mb-3 group-hover:text-primary transition-colors"
                style={{ fontFamily: 'var(--font-cormorant)', fontWeight: 500 }}
              >
                Caminhos do Autoconhecimento
              </h3>
              <p className="text-sm text-muted-foreground leading-relaxed mb-4">
                O livro da Célia, com os 98 textos publicados ao longo de mais
                de uma década de prática clínica. Download gratuito.
              </p>
              <p className="inline-flex items-center gap-1 text-xs text-primary">
                Baixar PDF gratuito <ArrowRight size={12} />
              </p>
            </Link>

            <div className="p-8 bg-primary text-primary-foreground rounded-sm">
              <MessageCircle size={28} className="mb-4" />
              <h3
                className="text-2xl mb-3"
                style={{ fontFamily: 'var(--font-cormorant)', fontWeight: 500 }}
              >
                A leitura abriu alguma pergunta?
              </h3>
              <p className="text-sm text-primary-foreground/90 leading-relaxed mb-5">
                Se algum texto tocou algo que você quer explorar com mais atenção,
                considere uma conversa inicial. Sem compromisso, sem pressa.
              </p>
              <Link
                href="/contato"
                className="inline-flex items-center gap-2 px-5 py-2.5 bg-primary-foreground text-primary rounded-full text-sm font-medium hover:bg-primary-foreground/90 transition-colors"
              >
                <MessageCircle size={14} />
                Falar com a Célia
              </Link>
            </div>
          </div>
        </div>
      </section>
    </div>
  );
}
