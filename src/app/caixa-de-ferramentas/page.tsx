'use client'

import { useMemo, useState } from "react";
import Link from "next/link";
import { Search, ArrowRight, Wrench } from "lucide-react";
import { getPraticas, contexts } from "@/lib/articles";

export default function CaixaDeFerramentasPage() {
  const [query, setQuery] = useState("");
  const [selectedContext, setSelectedContext] = useState<string>("");

  const allPraticas = useMemo(() => getPraticas(), []);

  const filtered = useMemo(() => {
    let list = allPraticas.slice();
    if (selectedContext) {
      list = list.filter((a) => a.contexts.includes(selectedContext));
    }
    const q = query.toLowerCase().trim();
    if (q) {
      list = list.filter(
        (a) =>
          a.title.toLowerCase().includes(q) ||
          a.summary.toLowerCase().includes(q) ||
          a.keywords.some((k) => k.toLowerCase().includes(q)) ||
          a.contextLabels.some((c) => c.toLowerCase().includes(q)),
      );
    }
    return list;
  }, [query, selectedContext, allPraticas]);

  return (
    <div className="flex flex-col">
      <section className="border-b border-border">
        <div className="mx-auto max-w-6xl px-6 lg:px-8 py-20 md:py-24">
          <div className="flex items-start gap-4 mb-6">
            <Wrench size={28} className="text-accent mt-1" />
            <p className="text-xs uppercase tracking-[0.25em] text-accent pt-2">
              Caixa de Ferramentas
            </p>
          </div>
          <h1
            className="text-4xl md:text-5xl lg:text-6xl text-foreground leading-[1.1] mb-6 max-w-3xl"
            style={{ fontFamily: 'var(--font-cormorant)', fontWeight: 500 }}
          >
            O que você pode fazer
            <span className="italic text-accent"> agora.</span>
          </h1>
          <p className="text-lg text-muted-foreground leading-relaxed max-w-2xl">
            Exercícios, técnicas e cuidados que você pode aplicar sozinho —
            respiração, florais, óleos essenciais, exercícios de proteção. Sempre
            como complemento, nunca como substituto do acompanhamento
            profissional.
          </p>
        </div>
      </section>

      {/* Busca + filtros */}
      <section className="border-b border-border bg-muted/20">
        <div className="mx-auto max-w-6xl px-6 lg:px-8 py-8">
          <div className="flex flex-col md:flex-row gap-4 items-stretch md:items-center">
            <div className="relative flex-1">
              <Search size={16} className="absolute left-4 top-1/2 -translate-y-1/2 text-muted-foreground" />
              <input
                type="search"
                value={query}
                onChange={(e) => setQuery(e.target.value)}
                placeholder="Buscar prática por título, tema ou palavra-chave"
                className="w-full pl-11 pr-4 py-3 bg-card border border-border rounded-sm text-foreground placeholder:text-muted-foreground focus:outline-none focus:border-accent transition-colors"
              />
            </div>
            <select
              value={selectedContext}
              onChange={(e) => setSelectedContext(e.target.value)}
              className="px-4 py-3 bg-card border border-border rounded-sm text-foreground focus:outline-none focus:border-accent transition-colors"
            >
              <option value="">Todos os contextos</option>
              {contexts.map((c) => (
                <option key={c.slug} value={c.slug}>{c.label}</option>
              ))}
            </select>
          </div>
          <p className="mt-4 text-sm text-muted-foreground">
            {filtered.length} {filtered.length === 1 ? "prática encontrada" : "práticas encontradas"}
          </p>
        </div>
      </section>

      {/* Lista */}
      <section className="border-b border-border">
        <div className="mx-auto max-w-6xl px-6 lg:px-8 py-16">
          {filtered.length === 0 ? (
            <div className="text-center py-20">
              <p className="text-muted-foreground mb-4">
                Nenhuma prática encontrada com esses critérios.
              </p>
              <button
                onClick={() => { setQuery(""); setSelectedContext(""); }}
                className="text-accent hover:underline text-sm"
              >
                Limpar filtros
              </button>
            </div>
          ) : (
            <div className="grid grid-cols-1 md:grid-cols-2 gap-x-12 gap-y-10">
              {filtered.map((article) => (
                <Link
                  key={article.slug}
                  href={`/caixa-de-ferramentas/${article.slug}`}
                  className="group flex flex-col border-b border-border pb-8 last:border-0"
                >
                  <p className="text-xs uppercase tracking-[0.2em] text-accent mb-2">
                    Prática · {article.contextLabels[0]}
                  </p>
                  <p className="text-xs text-muted-foreground mb-3">
                    {article.dateDisplay} · {article.readTime} min
                  </p>
                  <h2
                    className="text-2xl md:text-[1.65rem] text-foreground mb-3 group-hover:text-accent transition-colors leading-snug"
                    style={{ fontFamily: 'var(--font-cormorant)', fontWeight: 500 }}
                  >
                    {article.title}
                  </h2>
                  {/* Tags abaixo do título */}
                  {article.tags && article.tags.length > 0 && (
                    <div className="flex flex-wrap gap-1.5 mb-3">
                      {article.tags.slice(0, 4).map((tag, i) => (
                        <span
                          key={i}
                          className="text-[10px] px-2 py-0.5 bg-accent/8 text-accent/80 border border-accent/15 rounded-full"
                        >
                          {tag}
                        </span>
                      ))}
                    </div>
                  )}
                  <p className="text-base text-muted-foreground leading-relaxed line-clamp-3 mb-4">
                    {article.summary}
                  </p>
                  <p className="mt-auto inline-flex items-center gap-1 text-xs text-accent opacity-0 group-hover:opacity-100 transition-opacity">
                    Ver prática <ArrowRight size={12} />
                  </p>
                </Link>
              ))}
            </div>
          )}
        </div>
      </section>
    </div>
  );
}
