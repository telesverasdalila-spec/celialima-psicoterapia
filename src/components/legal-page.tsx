import { AlertCircle } from "lucide-react";

type LegalPageProps = {
  title: string;
  lastUpdated: string;
  intro: string;
  sections: { heading: string; body: string[] }[];
};

export function LegalPage({ title, lastUpdated, intro, sections }: LegalPageProps) {
  return (
    <div className="flex flex-col">
      <section className="border-b border-border">
        <div className="mx-auto max-w-3xl px-6 lg:px-8 py-16 md:py-20">
          <p className="text-xs uppercase tracking-[0.25em] text-primary mb-5">
            Documento legal
          </p>
          <h1
            className="text-3xl md:text-4xl lg:text-5xl text-foreground leading-[1.1] mb-4"
            style={{ fontFamily: 'var(--font-cormorant)', fontWeight: 500 }}
          >
            {title}
          </h1>
          <p className="text-sm text-muted-foreground italic">
            Última atualização: {lastUpdated}
          </p>
        </div>
      </section>

      {/* Disclaimer */}
      <section className="border-b border-border bg-muted/30">
        <div className="mx-auto max-w-3xl px-6 lg:px-8 py-6">
          <div className="flex items-start gap-3 p-4 border border-amber-400/40 bg-amber-50/40 rounded-sm">
            <AlertCircle size={20} className="text-amber-600 flex-shrink-0 mt-0.5" />
            <p className="text-sm text-foreground/80 leading-relaxed">
              <strong>Importante:</strong> Este documento é um <em>modelo</em>{" "}
              gerado automaticamente. Antes de publicar o site oficialmente,
              solicite a revisão de um advogado(a) ou contador(a) que cuide
              da parte legal do consultório da Célia. Textos legais devem ser
              adaptados à realidade específica de cada profissional.
            </p>
          </div>
        </div>
      </section>

      {/* Conteúdo */}
      <section className="border-b border-border">
        <div className="mx-auto max-w-3xl px-6 lg:px-8 py-12 md:py-16">
          <p className="text-base text-foreground/85 leading-relaxed mb-8 italic">
            {intro}
          </p>
          <div className="space-y-8">
            {sections.map((section, idx) => (
              <div key={idx}>
                <h2
                  className="text-xl md:text-2xl text-foreground mb-3"
                  style={{ fontFamily: 'var(--font-cormorant)', fontWeight: 600 }}
                >
                  {section.heading}
                </h2>
                <div className="space-y-3">
                  {section.body.map((para, pidx) => (
                    <p
                      key={pidx}
                      className="text-base text-foreground/80 leading-relaxed"
                    >
                      {para}
                    </p>
                  ))}
                </div>
              </div>
            ))}
          </div>
        </div>
      </section>
    </div>
  );
}
