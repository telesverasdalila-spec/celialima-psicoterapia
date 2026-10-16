'use client'

import Link from "next/link";
import { useState } from "react";
import { Menu, X, BookOpen } from "lucide-react";
import { cn } from "@/lib/utils";

const navItems = [
  { href: "/", label: "Início" },
  { href: "/sobre", label: "Sobre" },
  { href: "/atendimento", label: "Atendimento" },
  { href: "/saude-mental", label: "Saúde Mental" },
  { href: "/caixa-de-ferramentas", label: "Caixa de Ferramentas" },
  { href: "/contato", label: "Contato" },
];

export function SiteHeader() {
  const [open, setOpen] = useState(false);

  return (
    <header className="sticky top-0 z-50 bg-background/85 backdrop-blur-md border-b border-border">
      <div className="mx-auto max-w-7xl px-6 lg:px-8">
        <div className="flex h-20 items-center justify-between gap-4">
          <Link href="/" className="group flex items-baseline gap-2 flex-shrink-0" onClick={() => setOpen(false)}>
            <span
              className="text-2xl md:text-3xl text-foreground group-hover:text-primary transition-colors"
              style={{ fontFamily: 'var(--font-cormorant)', fontWeight: 500, letterSpacing: '0.02em' }}
            >
              Célia Lima
            </span>
            <span className="hidden sm:inline text-xs uppercase tracking-[0.2em] text-muted-foreground ml-1">
              Psicoterapia
            </span>
          </Link>

          {/* Desktop nav */}
          <nav className="hidden lg:flex items-center gap-6 flex-1 justify-center">
            {navItems.map((item) => (
              <Link
                key={item.href}
                href={item.href}
                className="text-sm text-foreground/80 hover:text-primary transition-colors relative group whitespace-nowrap"
              >
                {item.label}
                <span className="absolute -bottom-1 left-0 w-0 group-hover:w-full transition-all duration-300 h-px bg-primary" />
              </Link>
            ))}
          </nav>

          {/* Livro CTA — botão destacado */}
          <div className="hidden lg:flex items-center flex-shrink-0">
            <Link
              href="/livro"
              className="inline-flex items-center gap-2 px-4 py-2 bg-primary/10 text-primary border border-primary/30 rounded-full text-sm font-medium hover:bg-primary hover:text-primary-foreground transition-all"
            >
              <BookOpen size={14} />
              Livro
            </Link>
          </div>

          {/* Mobile toggle */}
          <button
            className="lg:hidden p-2 -mr-2 text-foreground flex-shrink-0"
            onClick={() => setOpen(!open)}
            aria-label={open ? "Fechar menu" : "Abrir menu"}
          >
            {open ? <X size={22} /> : <Menu size={22} />}
          </button>
        </div>

        {/* Mobile nav */}
        {open && (
          <nav className="lg:hidden pb-6 pt-2 border-t border-border">
            <ul className="flex flex-col gap-1">
              {navItems.map((item) => (
                <li key={item.href}>
                  <Link
                    href={item.href}
                    onClick={() => setOpen(false)}
                    className={cn(
                      "block px-2 py-3 text-base text-foreground/90 hover:text-primary hover:bg-muted/50 rounded-md transition-colors"
                    )}
                  >
                    {item.label}
                  </Link>
                </li>
              ))}
              <li>
                <Link
                  href="/livro"
                  onClick={() => setOpen(false)}
                  className="block px-2 py-3 text-base text-primary font-medium hover:bg-primary/10 rounded-md transition-colors"
                >
                  📖 Livro (download gratuito)
                </Link>
              </li>
            </ul>
          </nav>
        )}
      </div>
    </header>
  );
}
