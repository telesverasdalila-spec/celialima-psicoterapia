import Link from "next/link";
import { notFound } from "next/navigation";
import Image from "next/image";
import { ArrowRight, ArrowLeft, MessageCircle, Wrench, BookOpen } from "lucide-react";
import { contexts, getContext, getArtigosByContext, getPraticasByContext } from "@/lib/articles";

export const dynamicParams = true;

export function generateStaticParams() {
  return categories_slugs();
}

function categories_slugs() {
  return contexts.map((c) => ({ slug: c.slug }));
}

type Params = Promise<{ slug: string }>;

export async function generateMetadata({ params }: { params: Params }) {
  const { slug } = await params;
  const ctx = getContext(slug);
  if (!ctx) return { title: "Contexto não encontrado" };
  return {
    title: ctx.label,
    description: ctx.description,
  };
}

export default async function ContextoPage({ params }: { params: Params }) {
  const { slug } = await params;
  const ctx = getContext(slug);
  if (!ctx) notFound();
  const artigos = getArtigosByContext(slug);
  const praticas = getPraticasByContext(slug);
  const total = artigos.length + praticas.length;

  return (
    <div className="flex flex-col">
      {/* HERO do contexto — imagem + overlay + título + texto intro */}
      <section className="relative overflow-hidden">
        <div className="absolute inset-0">
          <Image
            src={`/contextos/${ctx.slug}.svg`}
            alt=""
            fill
            className="object-cover"
            sizes="100vw"
            priority
          />
          <div className="absolute inset-0 bg-background/55" />
          <div className="absolute inset-0 bg-gradient-to-b from-background/30 via-background/40 to-background/85" />
        </div>

        <div className="relative mx-auto max-w-4xl px-6 lg:px-8 py-28 md:py-36 text-center">
          <Link
            href="/"
            className="inline-flex items-center gap-1 text-sm text-muted-foreground hover:text-primary transition-colors mb-8"
          >
            <ArrowLeft size={14} />
            Início
          </Link>
          <p className="text-xs uppercase tracking-[0.25em] text-primary mb-5">
            {total} {total === 1 ? "texto" : "textos"} neste contexto
          </p>
          <h1
            className="text-4xl md:text-5xl lg:text-6xl text-foreground leading-[1.1] mb-6"
            style={{ fontFamily: 'var(--font-cormorant)', fontWeight: 500 }}
          >
            {ctx.label}
          </h1>
          <p className="text-lg md:text-xl text-muted-foreground leading-relaxed max-w-2xl mx-auto">
            {ctx.description}
          </p>
        </div>
      </section>

      {/* 2 COLUNAS — Artigos × Práticas */}
      <section className="border-b border-border">
        <div className="mx-auto max-w-6xl px-6 lg:px-8 py-16 md:py-20">
          <div className="grid md:grid-cols-2 gap-12">
            {/* COLUNA ESQUERDA — Artigos */}
            <div>
              <div className="flex items-center gap-3 mb-8 pb-4 border-b border-border">
                <BookOpen size={22} className="text-primary" />
                <div>
                  <p className="text-xs uppercase tracking-[0.2em] text-muted-foreground">
                    Saúde Mental
                  </p>
                  <h2
                    className="text-2xl text-foreground"
                    style={{ fontFamily: 'var(--font-cormorant)', fontWeight: 500 }}
                  >
                    Artigos
                  </h2>
                </div>
              </div>

              {artigos.length === 0 ? (
                <p className="text-sm text-muted-foreground italic">
                  Nenhum artigo neste contexto ainda.
                </p>
              ) : (
                <ul className="space-y-6">
                  {artigos.map((a) => (
                    <li key={a.slug}>
                      <Link
                        href={`/saude-mental/${a.slug}`}
                        className="group block"
                      >
                        <p className="text-xs text-muted-foreground mb-1">
                          {a.dateDisplay} · {a.readTime} min
                        </p>
                        <h3
                          className="text-lg text-foreground mb-2 group-hover:text-primary transition-colors leading-snug"
                          style={{ fontFamily: 'var(--font-cormorant)', fontWeight: 500 }}
                        >
                          {a.title}
                        </h3>
                        <p className="text-sm text-muted-foreground leading-relaxed line-clamp-2">
                          {a.summary}
                        </p>
                      </Link>
                    </li>
                  ))}
                </ul>
              )}
            </div>

            {/* COLUNA DIREITA — Práticas */}
            <div>
              <div className="flex items-center gap-3 mb-8 pb-4 border-b border-border">
                <Wrench size={22} className="text-accent" />
                <div>
                  <p className="text-xs uppercase tracking-[0.2em] text-muted-foreground">
                    Caixa de Ferramentas
                  </p>
                  <h2
                    className="text-2xl text-foreground"
                    style={{ fontFamily: 'var(--font-cormorant)', fontWeight: 500 }}
                  >
                    Práticas relacionadas
                  </h2>
                </div>
              </div>

              {praticas.length === 0 ? (
                <p className="text-sm text-muted-foreground italic">
                  Nenhuma prática específica neste contexto ainda.
                </p>
              ) : (
                <ul className="space-y-6">
                  {praticas.map((p) => (
                    <li key={p.slug}>
                      <Link
                        href={`/caixa-de-ferramentas/${p.slug}`}
                        className="group block"
                      >
                        <p className="text-xs text-muted-foreground mb-1">
                          {p.dateDisplay} · {p.readTime} min
                        </p>
                        <h3
                          className="text-lg text-foreground mb-2 group-hover:text-accent transition-colors leading-snug"
                          style={{ fontFamily: 'var(--font-cormorant)', fontWeight: 500 }}
                        >
                          {p.title}
                        </h3>
                        <p className="text-sm text-muted-foreground leading-relaxed line-clamp-2">
                          {p.summary}
                        </p>
                      </Link>
                    </li>
                  ))}
                </ul>
              )}
            </div>
          </div>
        </div>
      </section>

      {/* CTA WhatsApp específico do contexto */}
      <section className="border-b border-border bg-muted/30">
        <div className="mx-auto max-w-3xl px-6 lg:px-8 py-16 md:py-20">
          <div className="text-center">
            <h2
              className="text-2xl md:text-3xl text-foreground mb-5 leading-tight"
              style={{ fontFamily: 'var(--font-cormorant)', fontWeight: 500 }}
            >
              {ctx.label} te levando pra cá?
            </h2>
            <p className="text-base text-muted-foreground leading-relaxed mb-7 max-w-xl mx-auto">
              Se algum desses textos ressoou com algo que você está vivendo,
              talvez seja o momento de uma conversa. A primeira é sem custo e
              sem compromisso.
            </p>
            <Link
              href="/contato"
              className="inline-flex items-center gap-2 px-6 py-3 bg-primary text-primary-foreground rounded-full text-sm font-medium hover:bg-primary/90 transition-colors"
            >
              <MessageCircle size={16} />
              Falar com a Célia sobre {ctx.label.toLowerCase()}
            </Link>
          </div>
        </div>
      </section>
    </div>
  );
}
