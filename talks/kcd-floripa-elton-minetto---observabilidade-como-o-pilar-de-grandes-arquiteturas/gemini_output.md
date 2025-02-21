# Observabilidade em Grandes Arquiteturas: Uma Visão Além do Troubleshooting

## Introdução

A observabilidade, frequentemente associada à resolução de problemas e incidentes, possui um potencial muito maior. Nesta palestra, exploramos uma perspectiva diferente, demonstrando como a observabilidade se torna um pilar essencial para a construção e manutenção de grandes arquiteturas de software. Através de exemplos práticos e da apresentação do Well-Architected Framework da AWS, desvendamos como a observabilidade pode impulsionar a excelência operacional, segurança, confiabilidade, performance e otimização de custos.

## O Que É Observabilidade? Monitoramento Versus Observabilidade

O palestrante inicia sua abordagem diferenciando monitoramento de observabilidade. Monitoramento, segundo ele, é uma abordagem *pré-definida e opaca*, onde se sabe o que será monitorado desde o início. A aplicação é vista como uma "caixa preta", com entradas e saídas conhecidas, mas sem visibilidade interna.

> "Monitoramento permite que as equipes entendam sobre como suas APIs, seus sistemas, suas arquiteturas já estão funcionando, mas é muito baseado em um conjunto de coletas, um conjunto de informações já pré-definidos. Eu sei o que eu vou monitorar."

Em contrapartida, a observabilidade é baseada na *exploração* e *transparência*.  Permite fazer perguntas e indagações ao sistema, mesmo que os padrões não tenham sido definidos antecipadamente.  A aplicação se torna transparente, expondo informações internas na forma de métricas, logs e traces. Isso permite investigar o que está acontecendo em vez de apenas observar de fora.

> "Observabilidade, Ela é baseada na exploração. Eu vou fazer perguntas, eu vou fazer indagações para o meu sistema. São padrões não definidos antes. [...] Ela dá a ideia de transparência."

## Os Três (e Mais) Pilares da Observabilidade

O palestrante então detalha os três pilares clássicos da observabilidade, expandindo para outros pilares emergentes.

### 1. Métricas

Métricas são medições numéricas coletadas ao longo do tempo. Exemplos:

*   Percentual de CPU utilizada
*   Espaço em disco disponível
*   MegaBytes de memória ocupada ou livre
*   Número de requisições por segundo

Métricas sempre incluem um valor numérico e um *timestamp*.

### 2. Logs

Logs são transcrições detalhadas do comportamento do sistema, também com *timestamp*. Contêm informações sobre o que aconteceu, como:

*   Recebimento de uma requisição com determinados parâmetros
*   Geração de um status code 200 com uma resposta específica

Uma especialização importante são os *logs estruturados* (em formatos como JSON ou Parquet), que facilitam a análise e agregação dos dados.

### 3. Traces

Traces representam a rota de interação entre componentes, juntamente com o contexto. Podem ser:

*   *Traces internos a um microserviço:* Rastreiam as chamadas entre camadas (ex: MVC) dentro do serviço.
*   *Traces distribuídos:* Rastreiam o caminho de uma requisição através de múltiplos microserviços, permitindo entender o fluxo completo da aplicação, crucial em arquiteturas complexas.

Exemplo: Em uma arquitetura de microserviços, o Trace ajuda a identificar qual microserviço está causando um timeout em uma requisição.

### Pilares Adicionais

O palestrante explora pilares adicionais que estão ganhando relevância:

*   **Eventos:** Snapshots de mudanças de estado, tanto de negócio quanto de comportamento.  Exemplo: Em uma plataforma de e-learning, um evento é gerado quando um aluno completa uma aula.  O time de marketing pode usar esses dados para segmentar ofertas de novos cursos.
*   **Profiling:** Focado em performance. Permite analisar o uso de CPU, memória e o número de chamadas de método, fornecendo um "zoom" detalhado no comportamento interno da aplicação.  O projeto OpenTelemetry está trabalhando em padrões para documentar o profiling.
*   **Exceptions:**  Uma forma especializada de log para erros, incluindo stack traces e informações sobre a linha de código que gerou o erro.  O palestrante menciona que não é um pilar universalmente adotado e que, em sua equipe, eles geralmente tratam exceptions como logs com nível de severidade apropriado.

A interligação desses pilares permite uma visão holística do sistema. Um alerta gerado por uma métrica pode levar à análise dos logs, que por sua vez podem direcionar para um trace, permitindo identificar a causa raiz do problema. O profiling pode então ser usado para otimizar o componente problemático.

## O Que É Uma Boa Arquitetura? O Well-Architected Framework da AWS

Definir uma "boa arquitetura" é um desafio, pois não existe uma resposta única. O palestrante apresenta o **Well-Architected Framework da AWS** como um guia para ajudar a entender os prós e contras das decisões arquiteturais, permitindo construir aplicações robustas e confiáveis na nuvem (ou em qualquer outro ambiente, adaptando os exemplos específicos da AWS).

O Framework é estruturado em seis pilares:

1.  **Excelência Operacional:**  Foco na execução e monitoramento do sistema. Automação de processos, boas práticas de deploy e build são cruciais.
2.  **Segurança:** Implementação de criptografia (em repouso e em trânsito), SSL, autorização e autenticação adequadas.
3.  **Confiabilidade:**  Arquitetura resiliente a falhas e desastres. Capacidade de recuperação rápida e de manter a disponibilidade do serviço.
4.  **Excelência de Performance:**  Capacidade de escalar rapidamente para atender a demandas variáveis, com respostas rápidas e eficientes.
5.  **Custos:** Otimização dos custos operacionais, evitando desperdícios e garantindo a eficiência financeira da aplicação. A prática de FinOps é cada vez mais importante.
6.  **Sustentabilidade:**  Minimização do impacto ambiental, utilizando menos recursos (CPU, memória, energia) e otimizando o consumo.

O palestrante argumenta que a **observabilidade é fundamental para sustentar todos esses pilares**. Sem observabilidade, é difícil (ou impossível) garantir performance, confiabilidade, segurança e otimização de custos.

### A Relação Entre os Pilares da AWS e da Observabilidade

O palestrante apresenta uma matriz relacionando os pilares do Well-Architected Framework com os pilares da observabilidade:

| Pilar da AWS          | Pilares da Observabilidade Relevantes |
| ----------------------- | ------------------------------------- |
| Excelência Operacional  | Eventos, Métricas, Logs                |
| Segurança               | Eventos, Logs                         |
| Confiabilidade        | Métricas, Traces, Exceptions/Logs       |
| Performance            | Métricas, Traces, Profiling           |
| Custos                 | Eventos, Métricas                      |

Por exemplo, a *excelência operacional* depende de *eventos* (de negócio e do ciclo de vida do software), *métricas* (tempo de deploy, taxa de rollback) e *logs* para monitorar e otimizar os processos. A *segurança* se beneficia de *eventos* (login, troca de senha, tentativas de acesso) e *logs* para detectar potenciais ameaças.

## Como Garantir Uma Boa Arquitetura? Fitness Functions e Observability Driven Development

Para garantir que a arquitetura permaneça "bem arquitetada" ao longo do tempo, o palestrante apresenta duas técnicas:

### 1. Fitness Functions

Fitness Functions (originário da programação evolutiva) são testes automatizados que avaliam o quão próximo a arquitetura está de atingir um objetivo específico (confiabilidade, segurança, performance, etc.). São análogas a testes unitários, mas em vez de testar funcionalidades, testam a arquitetura.

> "É como se você fizesse um teste unitário, só que teste para arquitetura."

Exemplo: Para garantir a resiliência de um sistema, pode-se criar um fitness function que verifica se um novo deploy resulta em menos de 1% de erros. Isso é feito usando métricas e observabilidade.

```
# Pseudocódigo de um fitness function para resiliência:
def verifica_resiliencia_deploy(taxa_erros):
  assert taxa_erros < 0.01, "Taxa de erros no deploy excedeu o limite (1%)"
```

Fitness functions podem ser integrados à pipeline de CI/CD para garantir que a arquitetura não seja degradada com novas mudanças. Em um ambiente com 1800 microserviços, fitness functions ajudam a garantir que um serviço não penalize os outros.

### 2. Observability Driven Development (ODD)

ODD é uma abordagem inspirada no Test Driven Development (TDD), mas com a observabilidade como guia do desenvolvimento. Em vez de adicionar observabilidade após o surgimento de problemas, o ODD propõe que os desenvolvedores já escrevam o código pensando nas métricas, logs e traces necessários para monitorar e entender o sistema.

> "Assim como o TDD enfatiza que você primeiro escreve o teste para depois escrever o código, o ODD você escreve o código já pensando na observabilidade."

O ciclo do ODD consiste em:

1.  Definir o objetivo esperado (ex: diminuir a taxa de erros).
2.  Escrever o código já com a instrumentação de observabilidade necessária.
3.  Fazer o deploy.
4.  Monitorar os resultados em produção.
5.  Se o objetivo não for atingido, voltar ao começo e refatorar.

O ODD expande a responsabilidade dos desenvolvedores para além dos testes, incluindo a monitoração e a validação dos resultados em produção.

## Conclusão

A observabilidade vai além do simples *troubleshooting*. É um pilar fundamental para a construção e manutenção de grandes arquiteturas de software, permitindo garantir a excelência operacional, segurança, confiabilidade, performance e otimização de custos. Técnicas como fitness functions e Observability Driven Development ajudam a garantir que a arquitetura evolua de forma consistente e alinhada com os objetivos de negócio. A observabilidade não deve ser uma reflexão tardia, mas sim um componente essencial de todo o ciclo de vida do desenvolvimento de software.

## Links e Recursos Adicionais

*   [Cell-Based Architectures](Link para o artigo sobre Cell-Based Architectures) - Fonte de inspiração principal para a palestra.
*   [Temple - Os seis pilares da observabilidade](Link para o artigo da Temple sobre os 6 pilares)
*   [Dora Metrics e ODD](Link para o artigo que relaciona Dora Metrics e ODD)
