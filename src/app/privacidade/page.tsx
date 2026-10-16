import { LegalPage } from "@/components/legal-page";

export const metadata = {
  title: "Política de Privacidade",
  description: "Como o site da psicoterapeuta Célia Lima coleta e processa dados dos visitantes.",
};

export default function PrivacidadePage() {
  return (
    <LegalPage
      title="Política de Privacidade"
      lastUpdated="15 de outubro de 2026"
      intro="Esta política descreve como tratamos dados dos visitantes deste site. A Célia Lima respeita a privacidade de cada leitora e leitor, e segue as diretrizes da Lei Geral de Proteção de Dados (Lei 13.709/2018, LGPD)."
      sections={[
        {
          heading: "1. Dados coletados",
          body: [
            "Este site não coleta dados pessoais diretamente do leitor. Não há sistema de cadastro, login, comentários ou formulário de newsletter. A leitura dos textos é anônima.",
            "O formulário de contato (página /contato) abre diretamente o WhatsApp da Célia com a mensagem pré-preenchida. Os dados que você digita nesse formulário (nome, e-mail opcional e mensagem) são processados exclusivamente no seu navegador e enviados via WhatsApp — nunca armazenados neste site.",
          ],
        },
        {
          heading: "2. Cookies e analytics",
          body: [
            "Este site não utiliza cookies de rastreamento próprio.",
            "Serviços de hospedagem (Vercel) e ferramentas analíticas eventualmente conectadas (Google Analytics, Plausible, etc.) podem registrar dados técnicos padrão (endereço IP anonimizado, navegador, páginas visitadas, duração da visita) para fins de estatísticas agregadas e melhoria do serviço.",
            "Recomenda-se, quando da publicação oficial do site, configurar a ferramenta analítica escolhida em conformidade com a LGPD e o GDPR, com banner de consentimento explícito se aplicável.",
          ],
        },
        {
          heading: "3. Hospedagem",
          body: [
            "O site é hospedado na Vercel (ou provedor similar). Os servidores da Vercel estão em conformidade com práticas de segurança da informação, mas estão localizados em datacenters internacionais. Ao acessar o site, seus dados técnicos básicos (IP, request HTTP) transitam por esses provedores.",
            "Para mais informações sobre como a Vercel processa dados, consulte a política de privacidade da Vercel em vercel.com/legal/privacy-policy.",
          ],
        },
        {
          heading: "4. Atendimento e dados do cliente",
          body: [
            "Quando você se torna cliente da Célia Lima, suas informações pessoais (nome, contato, histórico de sessões) são tratadas pela Célia diretamente, fora deste site. Esses dados seguem o Código de Ética Profissional do terapeuta e a LGPD.",
            "Este site não armazena prontuários, anotações clínicas, nem qualquer dado de saúde do cliente. Toda comunicação clínica ocorre em canais privados (WhatsApp, e-mail, videochamada).",
          ],
        },
        {
          heading: "5. Seus direitos (LGPD)",
          body: [
            "Conforme a Lei 13.709/2018 (LGPD), você tem o direito de: acessar os dados que temos sobre você; corrigir dados incorretos; solicitar a exclusão dos seus dados; portar seus dados para outro serviço; retirar consentimento a qualquer momento.",
            "Para exercer qualquer desses direitos, entre em contato com a Célia Lima pelo WhatsApp (ver página /contato). Responderemos em até 15 dias corridos.",
          ],
        },
        {
          heading: "6. Links externos",
          body: [
            "Alguns textos do site podem conter links externos (originais na plataforma Personare, referências bibliográficas, etc.). Não nos responsabilizamos pela política de privacidade ou conteúdo desses sites externos.",
          ],
        },
        {
          heading: "7. Alterações desta política",
          body: [
            "Esta política pode ser atualizada periodicamente. A versão vigente é sempre a publicada nesta página, com a data no topo.",
          ],
        },
      ]}
    />
  );
}
