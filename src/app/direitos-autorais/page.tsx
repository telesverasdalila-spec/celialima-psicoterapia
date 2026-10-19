import { LegalPage } from "@/components/legal-page";

export const metadata = {
  title: "Direitos Autorais",
  description: "Direitos autorais sobre os textos publicados no site e no livro da psicoterapeuta Célia Lima.",
};

export default function DireitosAutoraisPage() {
  return (
    <LegalPage
      title="Direitos Autorais"
      lastUpdated="15 de outubro de 2026"
      intro="Esta página descreve a propriedade intelectual dos textos, imagens e materiais publicados neste site e no livro 'Caminhos do Autoconhecimento'."
      sections={[
        {
          heading: "1. Propriedade dos textos",
          body: [
            "Todos os textos publicados neste site são obra autoral de Célia Lima, protegida pela Lei 9.610/1998 (Lei de Direitos Autorais).",
            "Os textos que compõem a coletânea foram originalmente publicados pela autora na plataforma Personare entre 2009 e 2026, e foram posteriormente organizados pelo site da autora, com a devida cessão de uso.",
          ],
        },
        {
          heading: "2. Livro 'Caminhos do Autoconhecimento'",
          body: [
            "O livro 'Caminhos do Autoconhecimento — Textos de uma trajetória terapêutica' é obra autoral de Célia Lima, distribuída gratuitamente em formato PDF neste site.",
            "A distribuição gratuita autorizada é apenas via download direto do site celialima.com.br (ou domínio oficial eventualmente adotado).",
            "É proibida a venda do PDF por terceiros, sob qualquer forma. A redistribuição gratuita, citando a fonte e a autoria, é permitida e incentivada.",
          ],
        },
        {
          heading: "3. Uso permitido",
          body: [
            "Você pode: ler, baixar, imprimir para uso pessoal, compartilhar links do site em redes sociais, citar trechos com atribuição clara à autora e link para o site.",
            "Você pode citar trechos em trabalhos acadêmicos, respeitando as normas ABNT ou APA de citação.",
            "Para uso em publicações (livros, antologias, sites comerciais, cursos), é necessária autorização expressa da autora.",
          ],
        },
        {
          heading: "4. Uso proibido",
          body: [
            "É proibido: republicar textos integrais em outros sites sem autorização; usar textos para treinar modelos de inteligência artificial; comercializar os textos ou o livro PDF; modificar, adaptar ou traduzir sem autorização; remover a atribuição de autoria.",
            "Violações serão tratadas conforme a Lei 9.610/1998 e a Lei 12.737/2012 (Lei Carolina Dieckmann, sobre crimes digitais).",
          ],
        },
        {
          heading: "5. Imagens e elementos visuais",
          body: [
            "A paleta visual, a tipografia e o design do site são originais e foram desenvolvidos especificamente para a Célia Lima.",
            "A foto da Célia Lima é pessoal e seu uso é restrito a este site. Para usar a imagem em materiais externos (eventos, publicações), solicitar autorização prévia.",
            "Eventuais ícones e ilustrações de bibliotecas (Lucide Icons, etc.) são usados sob as respectivas licenças de software livre.",
          ],
        },
        {
          heading: "6. Solicitação de licença ou autorização",
          body: [
            "Para solicitar autorização de uso comercial, acadêmico ou editorial dos textos, imagens ou do livro, entre em contato com a Célia Lima pelo WhatsApp (página /contato).",
            "Pedidos serão respondidos em até 15 dias corridos.",
          ],
        },
      ]}
    />
  );
}
