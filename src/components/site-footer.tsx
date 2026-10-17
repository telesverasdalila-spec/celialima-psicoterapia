import Link from "next/link";

const footerNav = [
  { href: "/", label: "Início" },
  { href: "/sobre", label: "Sobre" },
  { href: "/atendimento", label: "Atendimento" },
  { href: "/saude-mental", label: "Publicações" },
  { href: "/caixa-de-ferramentas", label: "Caixa de Ferramentas" },
  { href: "/contato", label: "Contato" },
  { href: "/livro", label: "Livro" },
];

const footerContexts = [
  { slug: "ansiedade-stress", label: "Ansiedade & Stress" },
  { slug: "autoconhecimento-proposito", label: "Autoconhecimento & Propósito" },
  { slug: "relacionamentos", label: "Relacionamentos" },
  { slug: "luto-perdas", label: "Luto & Perdas" },
  { slug: "limites-autoestima", label: "Limites e Autoestima" },
  { slug: "familia-relacoes-parentais", label: "Família e relações parentais" },
];

const footerLegal = [
  { href: "/termos", label: "Termos de Serviço" },
  { href: "/privacidade", label: "Política de Privacidade" },
  { href: "/direitos-autorais", label: "Direitos Autorais" },
];

export function SiteFooter() {
  return (
    <footer className="mt-auto border-t border-border bg-muted/30">
      <div className="mx-auto max-w-6xl px-6 lg:px-8 py-14">
        <div className="grid grid-cols-1 md:grid-cols-4 gap-10">
          <div className="md:col-span-2">
            <h3
              className="text-2xl text-foreground mb-3"
              style={{ fontFamily: 'var(--font-cormorant)', fontWeight: 500 }}
            >
              Célia Lima
            </h3>
            <p className="text-sm text-muted-foreground leading-relaxed max-w-xs">
              Psicoterapia de orientação junguiana e psicosíntese. Um espaço
              para pensar a vida com mais gentileza e profundidade.
            </p>
          </div>

          <div>
            <h4 className="text-xs uppercase tracking-[0.2em] text-muted-foreground mb-4">
              Navegação
            </h4>
            <ul className="space-y-2 text-sm">
              {footerNav.map((item) => (
                <li key={item.href}>
                  <Link href={item.href} className="hover:text-primary transition-colors">
                    {item.label}
                  </Link>
                </li>
              ))}
            </ul>
          </div>

          <div>
            <h4 className="text-xs uppercase tracking-[0.2em] text-muted-foreground mb-4">
              Contextos
            </h4>
            <ul className="space-y-2 text-sm">
              {footerContexts.map((c) => (
                <li key={c.slug}>
                  <Link href={`/contextos/${c.slug}`} className="hover:text-primary transition-colors">
                    {c.label}
                  </Link>
                </li>
              ))}
            </ul>
          </div>
        </div>

        <div className="mt-12 pt-6 border-t border-border flex flex-col md:flex-row gap-3 justify-between items-start md:items-center">
          <div className="flex flex-col md:flex-row gap-3 md:gap-6 items-start md:items-center">
            <p className="text-xs text-muted-foreground">
              © {new Date().getFullYear()} Célia Lima · Todos os direitos reservados
            </p>
            <ul className="flex flex-wrap gap-3 md:gap-4 text-xs text-muted-foreground">
              {footerLegal.map((item) => (
                <li key={item.href}>
                  <Link href={item.href} className="hover:text-primary transition-colors underline-offset-2 hover:underline">
                    {item.label}
                  </Link>
                </li>
              ))}
            </ul>
          </div>
          <p className="text-xs text-muted-foreground italic max-w-md">
            Conteúdo psicológico é informativo e não substitui o acompanhamento profissional.
          </p>
        </div>
      </div>
    </footer>
  );
}
