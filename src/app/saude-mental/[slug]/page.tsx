import Link from "next/link";
import { notFound } from "next/navigation";
import { ArrowLeft, ArrowRight, MessageCircle, Wrench } from "lucide-react";
import {
  getArtigos,
  getArticle,
  getContext,
  getPraticasRelacionadas,
  getRelatedArticles,
} from "@/lib/articles";

export const dynamicParams = true;

export function generateStaticParams() {
  return getArtigos().map((a) => ({ slug: a.slug }));
}

type Params = Promise<{ slug: string }>;

export async function generateMetadata({ params }: { params: Params }) {
  const { slug } = await params;
  const article = getArticle(slug);
  if (!article) return { title: "Texto não encontrado" };
  return {
    title: article.title,
    description: article.summary,
    openGraph: {
      title: article.title,
      description: article.summary,
      type: "article",
    },
  };
}

export default async function ArtigoPage({ params }: { params: Params }) {
  const { slug } = await params;
  const article = getArticle(slug);
  if (!article) notFound();
  const ctx = article.contexts[0] ? getContext(article.contexts[0]) : undefined;
  const praticasRelacionadas = getPraticasRelacionadas(article, 3);
  const related = getRelatedArticles(article, 3);

  return (
    <div className="flex flex-col">
      <article>
        <section className="border-b border-border">
          <div className="mx-auto max-w-3xl px-6 lg:px-8 py-12 md:py-16">
            <Link
              href="/saude-mental"
              className="inline-flex items-center gap-1 text-sm text-muted-foreground hover:text-primary transition-colors mb-10"
            >
              <ArrowLeft size={14} />
              Saúde Mental
            </Link>

            <div className="mb-6">
              <Link
                href={`/contextos/${article.contexts[0]}`}
                className="inline-flex text-xs uppercase tracking-[0.2em] text-primary hover:underline"
              >
                {article.contextLabels[0]}
                {article.contextLabels[1] && (
                  <span className="text-muted-foreground ml-2">· {article.contextLabels[1]}</span>
                )}
              </Link>
            </div>

            <h1
              className="text-3xl md:text-4xl lg:text-5xl text-foreground leading-[1.15] mb-6"
              style={{ fontFamily: 'var(--font-cormorant)', fontWeight: 500 }}
            >
              {article.title}
            </h1>

            {/* Tags abaixo do título */}
            {article.tags && article.tags.length > 0 && (
              <div className="flex flex-wrap gap-2 mb-6">
                {article.tags.map((tag, i) => (
                  <span
                    key={i}
                    className="text-xs px-3 py-1 bg-primary/10 text-primary border border-primary/20 rounded-full"
                  >
                    {tag}
                  </span>
                ))}
              </div>
            )}

            <p className="text-lg text-muted-foreground italic leading-relaxed mb-6">
              {article.summary}
            </p>

            <div className="flex items-center gap-3 text-xs text-muted-foreground">
              <span>Por Célia Lima</span>
              <span>·</span>
              <span>{article.dateDisplay}</span>
              <span>·</span>
              <span>{article.readTime} min de leitura</span>
            </div>
          </div>
        </section>

        <section className="border-b border-border">
          <div className="mx-auto max-w-3xl px-6 lg:px-8 py-16 md:py-20">
            <div
              className="prose-celia"
              dangerouslySetInnerHTML={{ __html: article.html }}
            />

            {article.keywords.length > 0 && (
              <div className="mt-12 pt-6 border-t border-border">
                <p className="text-xs uppercase tracking-[0.2em] text-muted-foreground mb-3">
                  Temas relacionados
                </p>
                <div className="flex flex-wrap gap-2">
                  {article.keywords.map((kw, i) => (
                    <span
                      key={i}
                      className="text-xs px-3 py-1 bg-muted text-foreground/80 rounded-full"
                    >
                      {kw}
                    </span>
                  ))}
                </div>
              </div>
            )}
          </div>
        </section>

        {/* PRÁTICAS RELACIONADAS — articulação cruzada (lista) */}
        {praticasRelacionadas.length > 0 && (
          <section className="border-b border-border bg-accent/5">
            <div className="mx-auto max-w-3xl px-6 lg:px-8 py-16">
              <p className="text-xs uppercase tracking-[0.25em] text-accent mb-4 flex items-center gap-2">
                <Wrench size={14} />
                Para fazer agora
              </p>
              <h2
                className="text-2xl md:text-3xl text-foreground mb-4"
                style={{ fontFamily: 'var(--font-cormorant)', fontWeight: 500 }}
              >
                Práticas relacionadas a este texto.
              </h2>
              <p className="text-muted-foreground leading-relaxed mb-8">
                A leitura abriu alguma inquietação? Aqui vão práticas que conversam
                com o que você acabou de ler — pra usar no corpo.
              </p>
              <ul className="space-y-4">
                {praticasRelacionadas.map((p) => (
                  <li key={p.slug}>
                    <Link
                      href={`/caixa-de-ferramentas/${p.slug}`}
                      className="group p-5 bg-card rounded-sm border border-accent/30 hover:border-accent transition-all block"
                    >
                      <p className="text-xs uppercase tracking-[0.2em] text-accent mb-1">
                        {p.contextLabels[0]} · {p.readTime} min
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
                      <p className="mt-3 inline-flex items-center gap-1 text-xs text-accent">
                        Ver prática <ArrowRight size={12} />
                      </p>
                    </Link>
                  </li>
                ))}
              </ul>
            </div>
          </section>
        )}

        {/* CTA WhatsApp */}
        <section className="border-b border-border bg-muted/30">
          <div className="mx-auto max-w-3xl px-6 lg:px-8 py-16 md:py-20">
            <div className="text-center">
              <p className="text-xs uppercase tracking-[0.25em] text-primary mb-4">
                Tocou alguma coisa?
              </p>
              <h2
                className="text-2xl md:text-3xl text-foreground mb-5 leading-tight"
                style={{ fontFamily: 'var(--font-cormorant)', fontWeight: 500 }}
              >
                Se um texto abriu uma pergunta, talvez seja hora de conversar.
              </h2>
              <p className="text-base text-muted-foreground leading-relaxed mb-7 max-w-xl mx-auto">
                A primeira conversa comigo é sem custo e sem compromisso —
                um espaço para você sentir se faz sentido seguir.
              </p>
              <Link
                href="/contato"
                className="inline-flex items-center gap-2 px-6 py-3 bg-primary text-primary-foreground rounded-full text-sm font-medium hover:bg-primary/90 transition-colors"
              >
                <MessageCircle size={16} />
                Falar comigo
              </Link>
            </div>
          </div>
        </section>

        {/* ARTIGOS RELACIONADOS */}
        {related.length > 0 && (
          <section className="border-b border-border">
            <div className="mx-auto max-w-6xl px-6 lg:px-8 py-16 md:py-20">
              <p className="text-xs uppercase tracking-[0.25em] text-primary mb-3">
                Continue lendo
              </p>
              <h2
                className="text-3xl text-foreground mb-10"
                style={{ fontFamily: 'var(--font-cormorant)', fontWeight: 500 }}
              >
                Outros textos {ctx ? `de ${ctx.label}` : "relacionados"}.
              </h2>
              <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
                {related.map((rel) => (
                  <Link
                    key={rel.slug}
                    href={`/saude-mental/${rel.slug}`}
                    className="group flex flex-col"
                  >
                    <p className="text-xs text-muted-foreground mb-2">
                      {rel.dateDisplay} · {rel.readTime} min
                    </p>
                    <h3
                      className="text-xl text-foreground mb-2 group-hover:text-primary transition-colors leading-snug"
                      style={{ fontFamily: 'var(--font-cormorant)', fontWeight: 500 }}
                    >
                      {rel.title}
                    </h3>
                    <p className="text-sm text-muted-foreground leading-relaxed line-clamp-3">
                      {rel.summary}
                    </p>
                    <p className="mt-3 inline-flex items-center gap-1 text-xs text-primary opacity-0 group-hover:opacity-100 transition-opacity">
                      Ler <ArrowRight size={12} />
                    </p>
                  </Link>
                ))}
              </div>
            </div>
          </section>
        )}
      </article>
    </div>
  );
}
