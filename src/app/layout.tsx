import type { Metadata } from "next";
import { Cormorant_Garamond, Inter } from "next/font/google";
import "./globals.css";
import { Toaster } from "@/components/ui/toaster";
import { SiteHeader } from "@/components/site-header";
import { SiteFooter } from "@/components/site-footer";

const cormorant = Cormorant_Garamond({
  variable: "--font-cormorant",
  subsets: ["latin"],
  weight: ["400", "500", "600", "700"],
  style: ["normal", "italic"],
  display: "swap",
});

const inter = Inter({
  variable: "--font-inter",
  subsets: ["latin"],
  weight: ["300", "400", "500", "600"],
  display: "swap",
});

export const metadata: Metadata = {
  title: {
    default: "Célia Lima — Psicoterapia e Autoconhecimento",
    template: "%s · Célia Lima",
  },
  description:
    "Psicoterapia, autoconhecimento e terapias integrativas. Textos, reflexões e práticas da psicoterapeuta Célia Lima sobre amor, família, saúde, carreira e espiritualidade.",
  keywords: [
    "psicoterapia",
    "autoconhecimento",
    "terapia",
    "Célia Lima",
    "amor",
    "família",
    "saúde emocional",
    "terapias integrativas",
    "psicodrama",
  ],
  authors: [{ name: "Célia Lima" }],
  openGraph: {
    title: "Célia Lima — Psicoterapia e Autoconhecimento",
    description:
      "Psicoterapia, autoconhecimento e terapias integrativas com a psicoterapeuta Célia Lima.",
    type: "website",
    locale: "pt_BR",
  },
  twitter: {
    card: "summary_large_image",
    title: "Célia Lima — Psicoterapia e Autoconhecimento",
    description: "Psicoterapia, autoconhecimento e terapias integrativas.",
  },
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="pt-BR" suppressHydrationWarning>
      <body
        className={`${cormorant.variable} ${inter.variable} antialiased bg-background text-foreground flex flex-col min-h-screen`}
      >
        <SiteHeader />
        <main className="flex-1">{children}</main>
        <SiteFooter />
        <Toaster />
      </body>
    </html>
  );
}
