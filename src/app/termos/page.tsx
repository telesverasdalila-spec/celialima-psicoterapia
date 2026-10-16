import { LegalPage } from "@/components/legal-page";

export const metadata = {
  title: "Termos de Serviço",
  description: "Termos de uso do site da psicoterapeuta Célia Lima.",
};

export default function TermosPage() {
  return (
    <LegalPage
      title="Termos de Serviço"
      lastUpdated="15 de outubro de 2026"
      intro="Ao acessar e utilizar este site, você concorda com os termos descritos abaixo. Se não concordar com qualquer um deles, por favor não utilize o site."
      sections={[
        {
          heading: "1. Natureza do conteúdo",
          body: [
            "Este site tem caráter educativo e informativo. Os textos, artigos, práticas e materiais aqui publicados pela psicoterapeuta Célia Lima não constituem aconselhamento psicológico personalizado, diagnóstico clínico, nem substituem o acompanhamento profissional individualizado.",
            "A leitura deste material não estabelece relação terapêutica entre você e a Célia Lima. Relação terapêutica só se estabelece mediante contrato explícito, com sessões agendadas e remuneração combinada.",
            "Se você está em sofrimento psicológico, procure um psicoterapeuta ou psicólogo(a) próximo. Em emergências, ligue para o CVV (188) ou para o serviço de saúde mental da sua região.",
          ],
        },
        {
          heading: "2. Quem é Célia Lima",
          body: [
            "Célia Lima é terapeuta com formação em psicosíntese e análise junguiana (com base psicanalítica). Não é psicóloga (título protegido pela Lei 4.119/62 e Lei 5.766/71) nem psiquiatra.",
            "O uso do termo 'psicoterapia' neste site refere-se ao processo terapêutico em sentido amplo, reconhecido na prática clínica de terapeutas com formação em abordagens reconhecidas como a psicosíntese.",
          ],
        },
        {
          heading: "3. Uso permitido",
          body: [
            "Você pode ler, baixar e compartilhar os textos publicados neste site para uso pessoal e não comercial, citando a autoria de Célia Lima e o link do site.",
            "É proibido: (a) republicar os textos em outros sites sem autorização expressa; (b) usar o conteúdo para fins comerciais; (c) modificar, adaptar ou traduzir os textos sem permissão; (d) usar o conteúdo para treinar modelos de inteligência artificial sem autorização.",
            "Para uso comercial ou educacional formal (cursos, livros, antologias), entre em contato via WhatsApp para solicitar autorização específica.",
          ],
        },
        {
          heading: "4. Livro gratuito",
          body: [
            "O livro 'Caminhos do Autoconhecimento' é distribuído gratuitamente em formato PDF. Você pode baixar, ler e compartilhar livremente, citando a fonte.",
            "A venda do PDF por terceiros é estritamente proibida. A obra permanece protegida por direitos autorais (ver página 'Direitos Autorais').",
          ],
        },
        {
          heading: "5. Atendimento",
          body: [
            "As informações sobre modalidades de atendimento (psicoterapia individual, escuta inicial, mentoria pontual, grupo de estudos) são descritivas. Valores, horários e disponibilidade são combinados diretamente entre cliente e Célia Lima, em conversa privada.",
            "O agendamento de qualquer atendimento se dá mediante aceitação expressa de ambas as partes. A primeira conversa não estabelece vínculo terapêutico.",
          ],
        },
        {
          heading: "6. Limitação de responsabilidade",
          body: [
            "A Célia Lima não se responsabiliza por decisões tomadas pelo leitor com base exclusivamente na leitura dos textos deste site, sem o devido acompanhamento profissional.",
            "O site é fornecido 'no estado em que se encontra', sem garantias expressas ou implícitas de adequação a qualquer finalidade específica.",
          ],
        },
        {
          heading: "7. Alterações destes termos",
          body: [
            "Estes termos podem ser alterados a qualquer momento. A versão vigente é sempre a publicada nesta página, com a data de atualização no topo.",
            "Recomenda-se revisitar esta página periodicamente.",
          ],
        },
      ]}
    />
  );
}
