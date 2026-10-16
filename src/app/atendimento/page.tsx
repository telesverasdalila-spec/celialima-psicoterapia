import Link from "next/link";
import { ArrowRight, MessageCircle, MapPin, Video } from "lucide-react";
import { services } from "@/lib/articles";

export const metadata = {
  title: "Atendimento",
  description:
    "Como funciona o atendimento de psicoterapia da Célia Lima: abordagem, modalidades e serviços para diferentes momentos da vida.",
};

export default function AtendimentoPage() {
  return (
    <div className="flex flex-col">
      {/* Header */}
      <section className="border-b border-border">
        <div className="mx-auto max-w-5xl px-6 lg:px-8 py-20 md:py-28">
          <p className="text-xs uppercase tracking-[0.25em] text-primary mb-6">
            Atendimento
          </p>
          <h1
            className="text-4xl md:text-5xl lg:text-6xl text-foreground leading-[1.1] mb-8 max-w-3xl"
            style={{ fontFamily: 'var(--font-cormorant)', fontWeight: 500 }}
          >
            Como a Célia trabalha.
          </h1>
          <div className="space-y-5 text-lg text-foreground/85 leading-relaxed max-w-3xl">
            <p>
              A Célia Lima é <strong>psicoterapeuta de orientação junguiana e
              psicosíntese</strong>, com mais de 30 anos de prática clínica.
              Trabalha com escuta ativa, atenção aos símbolos e ao que o corpo
              diz, e uso integrativo de recursos como florais, óleos essenciais,
              respiração e psicodrama — quando fazem sentido para cada pessoa.
            </p>
            <p className="italic text-muted-foreground border-l-2 border-primary pl-4">
              "Não se trata só de parar de sofrer. Trata-se de virar a pessoa
              inteira que você veio ser."
            </p>
          </div>
        </div>
      </section>

      {/* Serviços */}
      <section className="border-b border-border bg-muted/20">
        <div className="mx-auto max-w-6xl px-6 lg:px-8 py-20 md:py-24">
          <div className="mb-12 max-w-2xl">
            <p className="text-xs uppercase tracking-[0.25em] text-primary mb-4">
              Para quem é o atendimento
            </p>
            <h2
              className="text-3xl md:text-4xl text-foreground mb-4"
              style={{ fontFamily: 'var(--font-cormorant)', fontWeight: 500 }}
            >
              Quatro portas de entrada.
            </h2>
            <p className="text-muted-foreground leading-relaxed">
              Não existe um jeito único de começar. Escolha a que faz sentido
              para o seu momento — a Célia te ajuda a decidir na primeira
              conversa.
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            {services.map((svc, idx) => (
              <div
                key={svc.id}
                className="group p-8 bg-card rounded-sm border border-border hover:border-primary/40 transition-all"
              >
                <p className="text-xs uppercase tracking-[0.2em] text-primary mb-3">
                  Serviço {idx + 1}
                </p>
                <h3
                  className="text-2xl text-foreground mb-4"
                  style={{ fontFamily: 'var(--font-cormorant)', fontWeight: 500 }}
                >
                  {svc.name}
                </h3>
                <div className="space-y-3 text-sm">
                  <div>
                    <p className="text-xs uppercase tracking-[0.15em] text-muted-foreground mb-1">
                      Para quem é
                    </p>
                    <p className="text-foreground/85 leading-relaxed">{svc.forWhom}</p>
                  </div>
                  <div>
                    <p className="text-xs uppercase tracking-[0.15em] text-muted-foreground mb-1">
                      Formato
                    </p>
                    <p className="text-foreground/85 leading-relaxed">{svc.format}</p>
                  </div>
                  <div className="flex items-center gap-2 text-xs text-muted-foreground pt-2 border-t border-border">
                    {svc.modality.includes('virtual') && (
                      <span className="inline-flex items-center gap-1">
                        <Video size={12} /> Virtual
                      </span>
                    )}
                    {svc.modality.includes('Presencial') && (
                      <span className="inline-flex items-center gap-1">
                        <MapPin size={12} /> Presencial
                      </span>
                    )}
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Abordagem explicada */}
      <section className="border-b border-border">
        <div className="mx-auto max-w-5xl px-6 lg:px-8 py-20 md:py-24">
          <p className="text-xs uppercase tracking-[0.25em] text-primary mb-4">
            Abordagem
          </p>
          <h2
            className="text-3xl md:text-4xl text-foreground mb-12"
            style={{ fontFamily: 'var(--font-cormorant)', fontWeight: 500 }}
          >
            Três ideias que organizam o trabalho.
          </h2>

          <div className="grid md:grid-cols-3 gap-8">
            <div>
              <h3 className="text-xl text-primary mb-3" style={{ fontFamily: 'var(--font-cormorant)', fontWeight: 600 }}>
                Subpersonalidades
              </h3>
              <p className="text-sm text-foreground/80 leading-relaxed">
                A gente não é uma pessoa só. Tem a profissional, a mãe, a filha,
                a adolescente que ainda mora dentro de você, a crítica, a
                medrosa. A terapia trabalha como essas partes conversam entre
                si — e como às vezes elas se boicotam.
              </p>
            </div>
            <div>
              <h3 className="text-xl text-primary mb-3" style={{ fontFamily: 'var(--font-cormorant)', fontWeight: 600 }}>
                Símbolos e sonhos
              </h3>
              <p className="text-sm text-foreground/80 leading-relaxed">
                O inconsciente fala por imagens, não por palavras. Um sonho, um
                sintoma do corpo, uma frase que escapa — tudo isso é linguagem.
                A terapia aprende a ler essa linguagem.
              </p>
            </div>
            <div>
              <h3 className="text-xl text-primary mb-3" style={{ fontFamily: 'var(--font-cormorant)', fontWeight: 600 }}>
                Sentido e totalidade
              </h3>
              <p className="text-sm text-foreground/80 leading-relaxed">
                Não se trata só de parar de sofrer. Trata-se de virar a pessoa
                inteira que você veio ser. A junguiana chama isso de individuação;
                a psicosíntese chama de auto-realização. É o mesmo convite: ser
                mais você mesmo.
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* CTA */}
      <section className="bg-primary text-primary-foreground">
        <div className="mx-auto max-w-5xl px-6 lg:px-8 py-20">
          <div className="max-w-2xl">
            <h2
              className="text-3xl md:text-4xl mb-5 leading-tight"
              style={{ fontFamily: 'var(--font-cormorant)', fontWeight: 500 }}
            >
              Quer conversar com a Célia?
            </h2>
            <p className="text-primary-foreground/90 leading-relaxed mb-7">
              A primeira conversa é sem custo e sem compromisso. É um momento
              para você sentir se faz sentido seguir, e para a Célia entender
              o que você está procurando.
            </p>
            <Link
              href="/contato"
              className="inline-flex items-center gap-2 px-6 py-3 bg-primary-foreground text-primary rounded-full text-sm font-medium hover:bg-primary-foreground/90 transition-colors"
            >
              <MessageCircle size={16} />
              Agendar conversa inicial
            </Link>
          </div>
        </div>
      </section>
    </div>
  );
}
