'use client'

import { useState } from "react";
import { MessageCircle, Send } from "lucide-react";

export default function ContatoPage() {
  const [form, setForm] = useState({ name: "", email: "", message: "" });
  const [sent, setSent] = useState(false);

  function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    // Por enquanto: monta link WhatsApp com a mensagem
    const text = `Olá Célia, meu nome é ${form.name}. ${form.message}`;
    const url = `https://wa.me/5599999999999?text=${encodeURIComponent(text)}`;
    window.open(url, "_blank");
    setSent(true);
  }

  return (
    <div className="flex flex-col">
      {/* Hero */}
      <section className="border-b border-border">
        <div className="mx-auto max-w-5xl px-6 lg:px-8 py-20 md:py-28">
          <p className="text-xs uppercase tracking-[0.25em] text-primary mb-6">
            Contato
          </p>
          <h1
            className="text-4xl md:text-5xl lg:text-6xl text-foreground leading-[1.1] mb-6 max-w-3xl"
            style={{ fontFamily: 'var(--font-cormorant)', fontWeight: 500 }}
          >
            Vamos conversar.
          </h1>
          <p className="text-lg text-muted-foreground leading-relaxed max-w-2xl">
            Se algum texto tocou algo, ou se você sente que é hora de começar a terapia,
            escreva aqui. Respondo pelo WhatsApp, no tempo que a agenda permite.
          </p>
        </div>
      </section>

      <section className="border-b border-border">
        <div className="mx-auto max-w-5xl px-6 lg:px-8 py-16 md:py-20">
          <div className="grid md:grid-cols-2 gap-12">
            {/* Formulário */}
            <div>
              <h2
                className="text-2xl text-foreground mb-6"
                style={{ fontFamily: 'var(--font-cormorant)', fontWeight: 500 }}
              >
                Escreva sua mensagem
              </h2>
              <form onSubmit={handleSubmit} className="flex flex-col gap-4">
                <div>
                  <label className="text-xs uppercase tracking-[0.2em] text-muted-foreground mb-2 block">
                    Nome
                  </label>
                  <input
                    type="text"
                    required
                    value={form.name}
                    onChange={(e) => setForm({ ...form, name: e.target.value })}
                    className="w-full px-4 py-3 bg-card border border-border rounded-sm text-foreground placeholder:text-muted-foreground focus:outline-none focus:border-primary transition-colors"
                    placeholder="Seu nome"
                  />
                </div>
                <div>
                  <label className="text-xs uppercase tracking-[0.2em] text-muted-foreground mb-2 block">
                    E-mail (opcional)
                  </label>
                  <input
                    type="email"
                    value={form.email}
                    onChange={(e) => setForm({ ...form, email: e.target.value })}
                    className="w-full px-4 py-3 bg-card border border-border rounded-sm text-foreground placeholder:text-muted-foreground focus:outline-none focus:border-primary transition-colors"
                    placeholder="seu@email.com"
                  />
                </div>
                <div>
                  <label className="text-xs uppercase tracking-[0.2em] text-muted-foreground mb-2 block">
                    Mensagem
                  </label>
                  <textarea
                    required
                    rows={5}
                    value={form.message}
                    onChange={(e) => setForm({ ...form, message: e.target.value })}
                    className="w-full px-4 py-3 bg-card border border-border rounded-sm text-foreground placeholder:text-muted-foreground focus:outline-none focus:border-primary transition-colors resize-none"
                    placeholder="Conte brevemente o que te trouxe aqui. Não precisa de detalhe — só o bastante para começarmos a conversa."
                  />
                </div>
                <button
                  type="submit"
                  className="inline-flex items-center justify-center gap-2 px-6 py-3 bg-primary text-primary-foreground rounded-full text-sm font-medium hover:bg-primary/90 transition-colors mt-2"
                >
                  <Send size={16} />
                  Enviar via WhatsApp
                </button>
                {sent && (
                  <p className="text-sm text-accent">
                    Abrindo o WhatsApp... Se não abrir automaticamente, clique
                    <a
                      href={`https://wa.me/5599999999999?text=${encodeURIComponent(
                        `Olá Célia, meu nome é ${form.name}. ${form.message}`,
                      )}`}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="underline ml-1"
                    >
                      aqui
                    </a>.
                  </p>
                )}
              </form>
            </div>

            {/* Info lateral */}
            <div className="flex flex-col gap-6">
              <div className="p-6 bg-muted/30 rounded-sm border border-border">
                <h3 className="text-lg text-foreground mb-3" style={{ fontFamily: 'var(--font-cormorant)', fontWeight: 600 }}>
                  Como funciona
                </h3>
                <ol className="space-y-3 text-sm text-foreground/85">
                  <li className="flex gap-3">
                    <span className="text-primary font-semibold">1.</span>
                    <span>Você manda a primeira mensagem, sem compromisso.</span>
                  </li>
                  <li className="flex gap-3">
                    <span className="text-primary font-semibold">2.</span>
                    <span>Respondo e combinamos horário para uma conversa inicial.</span>
                  </li>
                  <li className="flex gap-3">
                    <span className="text-primary font-semibold">3.</span>
                    <span>A primeira conversa serve para você sentir se faz sentido seguir.</span>
                  </li>
                </ol>
              </div>

              <div className="p-6 bg-muted/30 rounded-sm border border-border">
                <h3 className="text-lg text-foreground mb-3" style={{ fontFamily: 'var(--font-cormorant)', fontWeight: 600 }}>
                  Atendimento
                </h3>
                <ul className="space-y-2 text-sm text-foreground/85">
                  <li>Online (videochamada) ou presencial</li>
                  <li>Sessões de 50 minutos</li>
                  <li>Segunda a sexta, horário comercial</li>
                  <li className="pt-2 italic text-muted-foreground text-xs">
                    O contato é feito por mim, sem secretária eletrônica.
                  </li>
                </ul>
              </div>

              <div className="p-6 bg-primary text-primary-foreground rounded-sm">
                <h3 className="text-lg mb-3" style={{ fontFamily: 'var(--font-cormorant)', fontWeight: 600 }}>
                  Prefere falar direto?
                </h3>
                <p className="text-sm text-primary-foreground/90 mb-4">
                  Se for mais confortável, mande uma mensagem direta no WhatsApp.
                </p>
                <a
                  href="https://wa.me/5599999999999"
                  target="_blank"
                  rel="noopener noreferrer"
                  className="inline-flex items-center gap-2 px-4 py-2 bg-primary-foreground text-primary rounded-full text-sm font-medium hover:bg-primary-foreground/90 transition-colors"
                >
                  <MessageCircle size={14} />
                  Abrir WhatsApp
                </a>
              </div>
            </div>
          </div>
        </div>
      </section>
    </div>
  );
}
