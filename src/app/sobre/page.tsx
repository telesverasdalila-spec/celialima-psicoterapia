import Link from "next/link";
import Image from "next/image";
import { ArrowRight, MessageCircle } from "lucide-react";

export const metadata = {
  title: "Sobre",
  description:
    "Conheça a trajetória e o método da psicoterapeuta Célia Lima — psicodrama, terapias integrativas e uma escuta ativa que acompanha pessoas em seus processos emocionais há mais de quinze anos.",
};

export default function SobrePage() {
  return (
    <div className="flex flex-col">
      {/* Intro */}
      <section className="border-b border-border">
        <div className="mx-auto max-w-5xl px-6 lg:px-8 py-20 md:py-28">
          <div className="grid md:grid-cols-[1fr_2fr] gap-12 items-start">
            <div className="relative">
              <div className="relative aspect-square w-full max-w-xs mx-auto">
                <div className="absolute -right-3 -top-3 bottom-3 -left-3 bg-accent/15 rounded-sm" />
                <div className="absolute -right-3 -top-3 bottom-3 -left-3 border border-accent/30 rounded-sm" />
                <div className="relative h-full w-full overflow-hidden rounded-sm shadow-xl">
                  <Image
                    src="/celia.png"
                    alt="Célia Lima"
                    fill
                    className="object-cover"
                    sizes="(max-width: 768px) 80vw, 30vw"
                  />
                </div>
              </div>
            </div>
            <div>
              <p className="text-xs uppercase tracking-[0.25em] text-primary mb-6">
                Sobre
              </p>
              <h1
                className="text-4xl md:text-5xl text-foreground leading-[1.1] mb-8"
                style={{ fontFamily: 'var(--font-cormorant)', fontWeight: 500 }}
              >
                Célia Lima
                <span className="block italic text-primary mt-1">Psicoterapeuta</span>
              </h1>
              <div className="space-y-5 text-base md:text-lg text-foreground/85 leading-relaxed">
                <p>
                  Célia Lima é psicoterapeuta com mais de quinze anos de prática clínica.
                  Acompanha pessoas em seus processos emocionais com uma escuta atenta
                  e direta, sem jargão técnico, e com profundo respeito pelo ritmo próprio
                  de cada um.
                </p>
                <p>
                  Sua escrita nasceu da prática: cada texto partiu de uma situação concreta
                  vivida no consultório — uma dor, uma pergunta, um impasse — e ganhou
                  forma para conversar com mais gente do que aqueles que conseguem sentar
                  na poltrona da terapia.
                </p>
                <p>
                  Trabalha com <strong>psicodrama</strong>, <strong>terapias integrativas</strong>
                  {' '}(florais, óleos essenciais, respiração) e uma escuta que integra razão
                  e emoção. Sua especialidade é ajudar o cliente a reconhecer os movimentos
                  internos que se repetem — e a encontrar, dentro de si, o fio do qual dar
                  um novo passo.
                </p>
                <p>
                  Ao longo dessa trajetória publicou{" "}
                  <strong>98 textos</strong> sobre autoconhecimento, amor, família, saúde,
                  trabalho e espiritualidade — reunidos hoje neste site e no livro{" "}
                  <em>Caminhos do Autoconhecimento</em>.
                </p>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Método */}
      <section className="border-b border-border bg-muted/20">
        <div className="mx-auto max-w-5xl px-6 lg:px-8 py-20 md:py-24">
          <p className="text-xs uppercase tracking-[0.25em] text-primary mb-4">
            Abordagem
          </p>
          <h2
            className="text-3xl md:text-4xl text-foreground mb-12"
            style={{ fontFamily: 'var(--font-cormorant)', fontWeight: 500 }}
          >
            Como a Célia trabalha.
          </h2>

          <div className="grid md:grid-cols-3 gap-8">
            <div>
              <h3 className="text-xl text-primary mb-3" style={{ fontFamily: 'var(--font-cormorant)', fontWeight: 600 }}>
                Escuta
              </h3>
              <p className="text-sm text-foreground/80 leading-relaxed">
                Antes de qualquer técnica, a escuta. O espaço onde a pessoa pode falar sem
                medo de julgamento, e onde o silêncio também é palavra. Aquilo que ainda não
                consegue ser dito costuma ser o mais importante.
              </p>
            </div>
            <div>
              <h3 className="text-xl text-primary mb-3" style={{ fontFamily: 'var(--font-cormorant)', fontWeight: 600 }}>
                Psicodrama
              </h3>
              <p className="text-sm text-foreground/80 leading-relaxed">
                Método criado por Jacob Levy Moreno que encena emoções e situações —
                colocar fora do corpo o que estava preso dentro. Permite ver, sob outro
                ângulo, aquele diálogo que se repete há anos.
              </p>
            </div>
            <div>
              <h3 className="text-xl text-primary mb-3" style={{ fontFamily: 'var(--font-cormorant)', fontWeight: 600 }}>
                Integrativo
              </h3>
              <p className="text-sm text-foreground/80 leading-relaxed">
                Florais, óleos essenciais, respiração colorida: recursos que conversam
                com o corpo quando só a palavra não dá conta. Sempre como complemento,
                nunca como substituto da escuta e do trabalho psicológico.
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
              A primeira conversa é sem custo e sem compromisso. É um momento para você
              sentir se faz sentido seguir, e para a Célia entender o que você está
              procurando.
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
