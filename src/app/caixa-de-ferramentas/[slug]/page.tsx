import Link from "next/link";
import { notFound } from "next/navigation";
import { ArrowLeft, ArrowRight, MessageCircle, BookOpen } from "lucide-react";
import {
  getPraticas,
  getArticle,
  getContext,
  getArtigosRelacionados,
  getRelatedArticles,
} from "@/lib/articles";

export const dynamicParams = true;

export function generateStaticParams() {
  return getPraticas().map((a) => ({ slug: a.slug }));
}

type Params = Promise<{ slug: string }>;

export async function generateMetadata({ params }: { params: Params }) {
  const { slug } = await params;
  const article = getArticle(slug);
  if (!article) return { title: "Prática não encontrada" };
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

export default async function PraticaPage({ params }: { params: Params }) {
  const { slug } = await params;
  const article = getArticle(slug);
  if (!article) notFound();
  const ctx = article.contexts[0] ? getContext(article.contexts[0]) : undefined;
  const artigosRelacionados = getArtigosRelacionados(article, 3);
  const related = getRelatedArticles(article, 3);

  return (
    <div className="flex flex-col">
      <article>
        <section className="border-b border-border bg-accent/5">
          <div className="mx-auto max-w-3xl px-6 lg:px-8 py-12 md:py-16">
            <Link
              href="/caixa-de-ferramentas"
              className="inline-flex items-center gap-1 text-sm text-muted-foreground hover:text-accent transition-colors mb-10"
            >
              <ArrowLeft size={14} />
              Caixa de Ferramentas
            </Link>

            <div className="mb-6">
              <Link
                href={`/contextos/${article.contexts[0]}`}
                className="inline-flex text-xs uppercase tracking-[0.2em] text-accent hover:underline"
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
                    className="text-xs px-3 py-1 bg-accent/10 text-accent border border-accent/30 rounded-full"
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
              <span>{article.readTime} min de prática</span>
            </div>
          </div>
        </section>

        <section className="border-b border-border">
          <div className="mx-auto max-w-3xl px-6 lg:px-8 py-16 md:py-20">
            <div
              className="prose-celia"
              dangerouslySetInnerHTML={{ __html: article.html }}
            />

            <div className="mt-12 p-5 bg-muted/40 border-l-2 border-accent rounded-r-sm">
              <p className="text-xs uppercase tracking-[0.2em] text-accent mb-2">
                Importante
              </p>
              <p className="text-sm text-muted-foreground leading-relaxed">
                Esta prática é complementar e não substitui o acompanhamento
                profissional. Se você está em sofrimento psicológico, considere
                procurar um psicoterapeuta.
              </p>
            </div>
          </div>
        </section>

        {/* ARTIGOS RELACIONADOS — articulação cruzada (lista) */}
        {artigosRelacionados.length > 0 && (
          <section className="border-b border-border">
            <div className="mx-auto max-w-3xl px-6 lg:px-8 py-16">
              <p className="text-xs uppercase tracking-[0.25em] text-primary mb-4 flex items-center gap-2">
                <BookOpen size={14} />
                Para entender melhor
              </p>
              <h2
                className="text-2xl md:text-3xl text-foreground mb-4"
                style={{ fontFamily: 'var(--font-cormorant)', fontWeight: 500 }}
              >
                Textos para acompanhar esta prática.
              </h2>
              <p className="text-muted-foreground leading-relaxed mb-8">
                Antes ou depois de praticar, vale ler os textos que conversam
                com o mesmo tema. A prática fica mais profunda quando se entende
                o que está em jogo.
              </p>
              <ul className="space-y-4">
                {artigosRelacionados.map((a) => (
                  <li key={a.slug}>
                    <Link
                      href={`/saude-mental/${a.slug}`}
                      className="group p-5 bg-card rounded-sm border border-primary/30 hover:border-primary transition-all block"
                    >
                      <p className="text-xs uppercase tracking-[0.2em] text-primary mb-1">
                        {a.contextLabels[0]} · {a.readTime} min
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
                      <p className="mt-3 inline-flex items-center gap-1 text-xs text-primary">
                        Ler texto <ArrowRight size={12} />
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
                A prática não foi suficiente?
              </p>
              <h2
                className="text-2xl md:text-3xl text-foreground mb-5 leading-tight"
                style={{ fontFamily: 'var(--font-cormorant)', fontWeight: 500 }}
              >
                Talvez seja o momento de ter acompanhamento.
              </h2>
              <p className="text-base text-muted-foreground leading-relaxed mb-7 max-w-xl mx-auto">
                A primeira conversa com a Célia é sem custo e sem compromisso.
              </p>
              <Link
                href="/contato"
                className="inline-flex items-center gap-2 px-6 py-3 bg-primary text-primary-foreground rounded-full text-sm font-medium hover:bg-primary/90 transition-colors"
              >
                <MessageCircle size={16} />
                Falar com a Célia
              </Link>
            </div>
          </div>
        </section>

        {/* PRÁTICAS RELACIONADAS */}
        {related.length > 0 && (
          <section className="border-b border-border">
            <div className="mx-auto max-w-6xl px-6 lg:px-8 py-16 md:py-20">
              <p className="text-xs uppercase tracking-[0.25em] text-accent mb-3">
                Outras práticas
              </p>
              <h2
                className="text-3xl text-foreground mb-10"
                style={{ fontFamily: 'var(--font-cormorant)', fontWeight: 500 }}
              >
                Pra experimentar também.
              </h2>
              <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
                {related.map((rel) => (
                  <Link
                    key={rel.slug}
                    href={`/caixa-de-ferramentas/${rel.slug}`}
                    className="group flex flex-col"
                  >
                    <p className="text-xs text-muted-foreground mb-2">
                      {rel.dateDisplay} · {rel.readTime} min
                    </p>
                    <h3
                      className="text-xl text-foreground mb-2 group-hover:text-accent transition-colors leading-snug"
                      style={{ fontFamily: 'var(--font-cormorant)', fontWeight: 500 }}
                    >
                      {rel.title}
                    </h3>
                    <p className="text-sm text-muted-foreground leading-relaxed line-clamp-3">
                      {rel.summary}
                    </p>
                    <p className="mt-3 inline-flex items-center gap-1 text-xs text-accent opacity-0 group-hover:opacity-100 transition-opacity">
                      Ver prática <ArrowRight size={12} />
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
