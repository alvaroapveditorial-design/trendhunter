import { LandingInteractions } from "@/components/LandingInteractions";

export const metadata = {
  title: "AI Trend Hunter - Detecta oportunidades SaaS emergentes",
  description:
    "AI Trend Hunter analiza GitHub, Hacker News y RSS para detectar tendencias SaaS emergentes con score y briefs de oportunidad.",
  openGraph: {
    title: "AI Trend Hunter",
    description:
      "Detecta oportunidades SaaS emergentes antes de que sean obvias con señales públicas, scoring y briefs accionables.",
    type: "website",
  },
};

const landingMarkup = String.raw`<!-- ============ NAV ============ -->
<header class="nav" id="nav">
  <div class="container nav__in">
    <a class="brand" href="#top">
      <span class="brand__mark">
        <svg viewBox="0 0 24 24" fill="none"><path d="M3 17.5 9.2 11l3.6 3.3L21 6.5" stroke="currentColor" stroke-width="2.1" stroke-linecap="round" stroke-linejoin="round"/><circle cx="9.2" cy="11" r="1.7" fill="currentColor"/><circle cx="12.8" cy="14.3" r="1.7" fill="currentColor"/></svg>
      </span>
      AI Trend Hunter
    </a>
    <nav class="nav__links">
      <a href="#problem">Por qué</a>
      <a href="#solution">Cómo funciona</a>
      <a href="#features">Funciones</a>
      <a href="#samples">Ejemplo de salida</a>
    </nav>
    <div class="nav__cta">
      <a href="/dashboard" class="btn btn--ghost">Ver dashboard</a>
      <a href="/pricing" class="btn btn--primary">Probar 7 días</a>
      <button class="nav__burger" id="burger" aria-label="Probar 7 días">
        <svg viewBox="0 0 24 24" fill="none"><path d="M4 7h16M4 12h16M4 17h16" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"/></svg>
      </button>
    </div>
  </div>
</header>

<main id="top">

<!-- ============ HERO ============ -->
<section class="hero">
  <div class="hero__grid"></div>
  <div class="container hero__inner">
    <div class="hero__head reveal">
      <span class="eyebrow">Inteligencia de mercado para builders</span>
      <h1 class="display">Detecta oportunidades<br>SaaS emergentes <em>antes</em><br>de que sean obvias.</h1>
      <p class="lead">AI Trend Hunter analiza la señal pública — <strong>GitHub</strong>, <strong>Hacker News</strong> y <strong>RSS</strong> —, la agrupa en tendencias con score y te entrega briefs de oportunidad accionables. Entran señales débiles, salen ideas de producto validadas.</p>
      <div class="hero__cta">
        <a href="/pricing" class="btn btn--primary btn--lg">Probar 7 días gratis
          <svg viewBox="0 0 24 24" fill="none"><path d="M5 12h14M13 6l6 6-6 6" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>
        </a>
        <a href="/dashboard" class="btn btn--ghost btn--lg">Ver dashboard</a>
      </div>
      <div class="hero__meta">
        <span><b>3</b> fuentes públicas unificadas</span>
        <span><b>4</b> scores por tendencia</span>
        <span>7 días de prueba · 39 EUR/mes después</span>
      </div>
    </div>

    <!-- dashboard mockup -->
    <div class="dashboard-wrap reveal" id="hero-dash">
      <div class="app">
        <div class="app__bar">
          <div class="app__dots"><i></i><i></i><i></i></div>
          <div class="app__omni">
            <svg viewBox="0 0 24 24" fill="none"><circle cx="11" cy="11" r="7" stroke="currentColor" stroke-width="2"/><path d="m20 20-3.5-3.5" stroke="currentColor" stroke-width="2" stroke-linecap="round"/></svg>
            app.aitrendhunter.com/dashboard
          </div>
          <div class="app__bar-right">
            <span class="tag tag--accent">BETA</span>
            <div class="app__avatar"></div>
          </div>
        </div>
        <div class="app__body">
          <!-- sidebar -->
          <aside class="app__side">
            <a class="brand" href="#"><span class="brand__mark"><svg viewBox="0 0 24 24" fill="none"><path d="M3 17.5 9.2 11l3.6 3.3L21 6.5" stroke="currentColor" stroke-width="2.1" stroke-linecap="round" stroke-linejoin="round"/></svg></span>Trend Hunter</a>
            <nav class="navlist">
              <a href="#top" class="is-active"><svg viewBox="0 0 24 24" fill="none"><path d="M4 19V9m5 10V5m5 14v-7m5 7V8" stroke="currentColor" stroke-width="2" stroke-linecap="round"/></svg>Tendencias</a>
              <a href="#top"><svg viewBox="0 0 24 24" fill="none"><circle cx="12" cy="12" r="3" stroke="currentColor" stroke-width="2"/><path d="M12 3v3m0 12v3m9-9h-3M6 12H3" stroke="currentColor" stroke-width="2" stroke-linecap="round"/></svg>Fuentes</a>
              <a href="#top"><svg viewBox="0 0 24 24" fill="none"><path d="M6 3h9l5 5v13H6z" stroke="currentColor" stroke-width="2" stroke-linejoin="round"/><path d="M9 12h7M9 16h5" stroke="currentColor" stroke-width="2" stroke-linecap="round"/></svg>Briefs</a>
              <a href="#top"><svg viewBox="0 0 24 24" fill="none"><path d="M12 4c4 4 7 5 7 5s0 8-7 11c-7-3-7-11-7-11s3-1 7-5Z" stroke="currentColor" stroke-width="2" stroke-linejoin="round"/></svg>Seguimiento</a>
              <span class="navlist__label">Cuenta</span>
              <a href="#top"><svg viewBox="0 0 24 24" fill="none"><circle cx="12" cy="8" r="3.4" stroke="currentColor" stroke-width="2"/><path d="M5 20c1.5-3.5 4-5 7-5s5.5 1.5 7 5" stroke="currentColor" stroke-width="2" stroke-linecap="round"/></svg>Perfil</a>
              <a href="#top"><svg viewBox="0 0 24 24" fill="none"><circle cx="12" cy="12" r="3" stroke="currentColor" stroke-width="2"/><path d="m19.4 13.5.7 1.5-2 2-1.5-.7a6 6 0 0 1-1.6.9L14.5 21h-3l-.5-1.8a6 6 0 0 1-1.6-.9l-1.5.7-2-2 .7-1.5a6 6 0 0 1-.9-1.6L4 12.5v-3l1.8-.5c.2-.6.5-1.1.9-1.6l-.7-1.5 2-2 1.5.7c.5-.4 1-.7 1.6-.9L11.5 1h3l.5 1.8c.6.2 1.1.5 1.6.9l1.5-.7 2 2-.7 1.5c.4.5.7 1 .9 1.6L22 9.5v3l-1.8.5c-.2.6-.5 1.1-.8 1.5Z" stroke="currentColor" stroke-width="1.6" stroke-linejoin="round"/></svg>Ajustes</a>
            </nav>
          </aside>

          <!-- main -->
          <section class="app__main">
            <div class="app__main-head">
              <div>
                <h4>Tendencias emergentes</h4>
                <p>Ordenadas por opportunity score · 1.284 señales procesadas</p>
              </div>
              <span class="app__week">
                <svg width="13" height="13" viewBox="0 0 24 24" fill="none"><rect x="3" y="5" width="18" height="16" rx="2" stroke="currentColor" stroke-width="2"/><path d="M3 9h18M8 3v4m8-4v4" stroke="currentColor" stroke-width="2" stroke-linecap="round"/></svg>
                Semana 23 · 2026
              </span>
            </div>

            <div class="kpis">
              <div class="kpi"><div class="kpi__l">Tendencias seguidas</div><div class="kpi__v">142 <span class="kpi__d up">+18</span></div></div>
              <div class="kpi"><div class="kpi__l">Nuevas esta semana</div><div class="kpi__v">23 <span class="kpi__d up">+6</span></div></div>
              <div class="kpi"><div class="kpi__l">Momentum medio</div><div class="kpi__v">+34% <span class="kpi__d up">▲</span></div></div>
              <div class="kpi"><div class="kpi__l">Briefs listos</div><div class="kpi__v">9 <span class="kpi__d up">nuevos</span></div></div>
            </div>

            <div class="ttable">
              <div class="trow trow--head">
                <span>Tendencia</span><span>Categoría</span><span>Oportunidad</span><span>Saturación</span><span>Mom.</span>
              </div>

              <div class="trow">
                <div class="trow__name">
                  <b>Gateways LLM self-hosted</b>
                  <div class="trow__sources"><span class="src src--gh"><i></i>GitHub ×41</span><span class="src src--hn"><i></i>HN ×12</span></div>
                </div>
                <div class="trow__cat"><span class="tag tag--accent">AI infra</span></div>
                <div class="meter" data-label="Oportunidad"><div class="meter__row"><div class="meter__bar"><div class="meter__fill meter__fill--accent" style="--val:88%"></div></div><span class="meter__num">88</span></div></div>
                <div class="meter" data-label="Saturación"><div class="meter__row"><div class="meter__bar"><div class="meter__fill meter__fill--pos" style="--val:31%"></div></div><span class="meter__num">31</span></div></div>
                <div class="spark"><svg viewBox="0 0 64 24" preserveAspectRatio="none"><polyline points="0,20 11,18 22,15 32,12 43,7 54,5 64,2" fill="none" stroke="var(--pos)" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg><span class="spark__v">+62%</span></div>
              </div>

              <div class="trow">
                <div class="trow__name">
                  <b>Agentes de IA para testing QA</b>
                  <div class="trow__sources"><span class="src src--gh"><i></i>GitHub ×28</span><span class="src src--rss"><i></i>RSS ×9</span></div>
                </div>
                <div class="trow__cat"><span class="tag tag--accent">Dev tools</span></div>
                <div class="meter" data-label="Oportunidad"><div class="meter__row"><div class="meter__bar"><div class="meter__fill meter__fill--accent" style="--val:81%"></div></div><span class="meter__num">81</span></div></div>
                <div class="meter" data-label="Saturación"><div class="meter__row"><div class="meter__bar"><div class="meter__fill meter__fill--pos" style="--val:44%"></div></div><span class="meter__num">44</span></div></div>
                <div class="spark"><svg viewBox="0 0 64 24" preserveAspectRatio="none"><polyline points="0,18 11,16 22,17 32,12 43,10 54,6 64,4" fill="none" stroke="var(--pos)" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg><span class="spark__v">+47%</span></div>
              </div>

              <div class="trow">
                <div class="trow__name">
                  <b>Motores de sync local-first</b>
                  <div class="trow__sources"><span class="src src--gh"><i></i>GitHub ×33</span><span class="src src--hn"><i></i>HN ×7</span></div>
                </div>
                <div class="trow__cat"><span class="tag tag--accent">Dev tools</span></div>
                <div class="meter" data-label="Oportunidad"><div class="meter__row"><div class="meter__bar"><div class="meter__fill meter__fill--accent" style="--val:76%"></div></div><span class="meter__num">76</span></div></div>
                <div class="meter" data-label="Saturación"><div class="meter__row"><div class="meter__bar"><div class="meter__fill meter__fill--warn" style="--val:58%"></div></div><span class="meter__num">58</span></div></div>
                <div class="spark"><svg viewBox="0 0 64 24" preserveAspectRatio="none"><polyline points="0,14 11,15 22,12 32,13 43,10 54,9 64,7" fill="none" stroke="var(--pos)" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg><span class="spark__v">+29%</span></div>
              </div>

              <div class="trow">
                <div class="trow__name">
                  <b>Automatización de compliance para IA</b>
                  <div class="trow__sources"><span class="src src--rss"><i></i>RSS ×15</span><span class="src src--hn"><i></i>HN ×6</span></div>
                </div>
                <div class="trow__cat"><span class="tag tag--accent">Fintech</span></div>
                <div class="meter" data-label="Oportunidad"><div class="meter__row"><div class="meter__bar"><div class="meter__fill meter__fill--accent" style="--val:73%"></div></div><span class="meter__num">73</span></div></div>
                <div class="meter" data-label="Saturación"><div class="meter__row"><div class="meter__bar"><div class="meter__fill meter__fill--pos" style="--val:27%"></div></div><span class="meter__num">27</span></div></div>
                <div class="spark"><svg viewBox="0 0 64 24" preserveAspectRatio="none"><polyline points="0,19 11,17 22,16 32,14 43,11 54,9 64,8" fill="none" stroke="var(--pos)" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg><span class="spark__v">+38%</span></div>
              </div>
            </div>
          </section>
        </div>
      </div>

      <!-- floating brief annotation -->
      <aside class="float-brief">
        <span class="eyebrow">Brief de oportunidad</span>
        <h5>Gateways LLM self-hosted</h5>
        <p>Los equipos quieren control de costes y residencia de datos. El tooling está fragmentado, sin un default claro. Fuerte demanda de builders, baja saturación comercial.</p>
        <div class="float-brief__foot">
          <span class="float-brief__score">Trend score <b>91</b></span>
          <span class="tag tag--accent">Actúa ya</span>
        </div>
      </aside>
    </div>
  </div>
</section>

<!-- ============ LOGO STRIP ============ -->
<section class="section--tight">
  <div class="container">
    <p class="eyebrow eyebrow--plain muted" style="text-align:center; display:block; margin-bottom:26px;">Señales extraídas de los lugares donde las ideas aparecen primero</p>
    <div class="logos">
      <span>GitHub</span><span>Hacker News</span><span>Feeds RSS</span><span>Changelogs de producto</span><span>Notas de versión</span><span>Foros dev</span>
    </div>
  </div>
</section>

<!-- ============ PROBLEM ============ -->
<section class="section section--dark" id="problem">
  <div class="container">
    <div class="section-head">
      <span class="eyebrow">El problema</span>
      <h2 class="h2">Cuando una tendencia llega a un informe, la ventana ya se ha cerrado.</h2>
    </div>
    <div class="problem__grid">
      <div class="problem__item reveal">
        <div class="problem__n">01</div>
        <h3>Los founders pierden horas en fuentes dispersas</h3>
        <p>Leer repos, hilos y feeds en una docena de pestañas cada semana no es investigar: es un trabajo a media jornada que rara vez se convierte en una decisión.</p>
      </div>
      <div class="problem__item reveal">
        <div class="problem__n">02</div>
        <h3>Las señales aparecen primero en el código, no en la cobertura</h3>
        <p>La evidencia más temprana vive en repos de GitHub, hilos de Hacker News y feeds RSS, meses antes de aparecer en un informe de tendencias o una newsletter.</p>
      </div>
      <div class="problem__item reveal">
        <div class="problem__n">03</div>
        <h3>El ruido esconde la oportunidad real</h3>
        <p>Por cada cambio real hay diez ciclos de hype. Sin scoring, es imposible distinguir una oportunidad duradera de un fin de semana ruidoso.</p>
      </div>
    </div>
  </div>
</section>

<!-- ============ SOLUTION ============ -->
<section class="section" id="solution">
  <div class="container">
    <div class="section-head">
      <span class="eyebrow">Cómo funciona</span>
      <h2 class="h2">Entran señales públicas. Salen tendencias con score. Briefs sobre los que actuar.</h2>
      <p class="lead">Un único pipeline convierte el torrente de actividad pública de desarrolladores en una lista corta y ordenada de oportunidades, cada una respaldada por la evidencia de la que surge.</p>
    </div>

    <div class="pipe">
      <div class="pipe__step reveal">
        <div class="pipe__k">PASO 01</div>
        <h3>Entran señales públicas</h3>
        <p>Recogemos de forma continua stars, commits, hilos, puntos y entradas de feeds de GitHub, Hacker News y RSS.</p>
        <div class="pipe__viz srcviz">
          <div class="srcviz__row"><span class="src src--gh"><i></i>GitHub</span><span class="srcviz__bar"><i style="--val:90%"></i></span></div>
          <div class="srcviz__row"><span class="src src--hn"><i></i>Hacker News</span><span class="srcviz__bar"><i style="--val:64%"></i></span></div>
          <div class="srcviz__row"><span class="src src--rss"><i></i>RSS</span><span class="srcviz__bar"><i style="--val:48%"></i></span></div>
        </div>
      </div>
      <div class="pipe__arrow"><svg viewBox="0 0 24 24" fill="none"><path d="M5 12h14M13 6l6 6-6 6" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg></div>
      <div class="pipe__step reveal">
        <div class="pipe__k">PASO 02</div>
        <h3>Salen tendencias con score</h3>
        <p>Las señales se agrupan en tendencias y reciben score de momentum, oportunidad y saturación, para que el ranking sea objetivo.</p>
        <div class="pipe__viz scoreviz">
          <div class="scoreviz__item"><div class="scoreviz__top"><span>Oportunidad</span><b>88</b></div><div class="meter__bar"><div class="meter__fill meter__fill--accent" style="--val:88%"></div></div></div>
          <div class="scoreviz__item"><div class="scoreviz__top"><span>Momentum</span><b>+62%</b></div><div class="meter__bar"><div class="meter__fill meter__fill--pos" style="--val:72%"></div></div></div>
          <div class="scoreviz__item"><div class="scoreviz__top"><span>Saturación</span><b>31</b></div><div class="meter__bar"><div class="meter__fill meter__fill--warn" style="--val:31%"></div></div></div>
        </div>
      </div>
      <div class="pipe__arrow"><svg viewBox="0 0 24 24" fill="none"><path d="M5 12h14M13 6l6 6-6 6" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg></div>
      <div class="pipe__step reveal">
        <div class="pipe__k">PASO 03</div>
        <h3>Briefs para actuar</h3>
        <p>Cada tendencia destacada se convierte en un breve brief de oportunidad SaaS: quién, por qué ahora y dónde está el hueco.</p>
        <div class="pipe__viz briefviz">
          <h6>Gateways LLM self-hosted</h6>
          <ul>
            <li>Quién: equipos de plataforma e infra</li>
            <li>Por qué ahora: coste + residencia de datos</li>
            <li>Hueco: sin un default claro</li>
          </ul>
        </div>
      </div>
    </div>
  </div>
</section>

<hr class="rule">

<!-- ============ FEATURES ============ -->
<section class="section" id="features">
  <div class="container">
    <div class="section-head">
      <span class="eyebrow">Funciones</span>
      <h2 class="h2">Todo lo que necesitas para convertir una señal en una decisión de producto.</h2>
    </div>

    <div class="features">
      <article class="feature reveal">
        <div class="feature__ix">/01</div>
        <div class="feature__main">
          <h3>Recolección de señales multifuente</h3>
          <p>Una capa de ingesta unifica los tres lugares donde las oportunidades aparecen primero, para que dejes de saltar entre pestañas y empieces a comparar peras con peras.</p>
          <div class="feature__tags"><span class="tag">GitHub</span><span class="tag">Hacker News</span><span class="tag">RSS</span></div>
        </div>
        <div class="feature__viz srcviz">
          <div class="srcviz__row">Repos y stars<span class="src src--gh"><i></i>GitHub</span></div>
          <div class="srcviz__row">Hilos y puntos<span class="src src--hn"><i></i>HN</span></div>
          <div class="srcviz__row">Changelogs y feeds<span class="src src--rss"><i></i>RSS</span></div>
        </div>
      </article>

      <article class="feature reveal">
        <div class="feature__ix">/02</div>
        <div class="feature__main">
          <h3>Scoring de tendencias</h3>
          <p>Cada tendencia lleva cuatro números — trend score, oportunidad, saturación y momentum — para que priorizar sea un vistazo, no un debate.</p>
          <div class="feature__tags"><span class="tag tag--accent">Momentum</span><span class="tag tag--accent">Oportunidad</span><span class="tag tag--accent">Saturación</span></div>
        </div>
        <div class="feature__viz scoreviz">
          <div class="scoreviz__item"><div class="scoreviz__top"><span>Trend score</span><b>91</b></div><div class="meter__bar"><div class="meter__fill meter__fill--accent" style="--val:91%"></div></div></div>
          <div class="scoreviz__item"><div class="scoreviz__top"><span>Oportunidad</span><b>88</b></div><div class="meter__bar"><div class="meter__fill meter__fill--accent" style="--val:88%"></div></div></div>
          <div class="scoreviz__item"><div class="scoreviz__top"><span>Saturación</span><b>31</b></div><div class="meter__bar"><div class="meter__fill meter__fill--warn" style="--val:31%"></div></div></div>
        </div>
      </article>

      <article class="feature reveal">
        <div class="feature__ix">/03</div>
        <div class="feature__main">
          <h3>Evidencia respaldada por fuentes</h3>
          <p>Sin caja negra. Cada score enlaza con los repos, hilos y entradas de feed exactos de los que surge, para que verifiques antes de apostar.</p>
          <div class="feature__tags"><span class="tag">Trazable</span><span class="tag">Auditable</span></div>
        </div>
        <div class="feature__viz evidence">
          <div class="evidence__line"><span class="src src--gh"><i></i>GH</span>llm-gateway · +312 stars / 14d</div>
          <div class="evidence__line"><span class="src src--hn"><i></i>HN</span>"Show HN: route LLMs locally" · 284▲</div>
          <div class="evidence__line"><span class="src src--rss"><i></i>RSS</span>3 blogs de infra · coste y residencia</div>
        </div>
      </article>

      <article class="feature reveal">
        <div class="feature__ix">/04</div>
        <div class="feature__main">
          <h3>Briefs de oportunidad SaaS</h3>
          <p>Las tendencias top se redactan como briefs concisos y accionables: la audiencia, el momento y el hueco concreto que un producto podría cubrir.</p>
          <div class="feature__tags"><span class="tag">Quién y por qué ahora</span><span class="tag">Análisis del hueco</span></div>
        </div>
        <div class="feature__viz briefviz">
          <h6>Brief · Agentes IA para QA</h6>
          <ul>
            <li>Quién: equipos de plataforma ágiles que envían rápido</li>
            <li>Por qué ahora: fatiga de tests flaky + tooling de agentes</li>
            <li>Hueco: sin un default self-healing de confianza</li>
          </ul>
        </div>
      </article>

      <article class="feature reveal">
        <div class="feature__ix">/05</div>
        <div class="feature__main">
          <h3>Dashboard operativo para priorizar</h3>
          <p>Tendencias, fuentes, scores e historial viven en una misma vista para revisar señales, comparar oportunidades y decidir qué investigar después.</p>
          <div class="feature__tags"><span class="tag">Dashboard MVP</span><span class="tag">Historial de runs</span><span class="tag">Exportable pronto</span></div>
        </div>
        <div class="feature__viz lockviz">
          <div class="lockviz__ic"><svg viewBox="0 0 24 24" fill="none"><rect x="5" y="11" width="14" height="9" rx="2" stroke="currentColor" stroke-width="2"/><path d="M8 11V8a4 4 0 0 1 8 0v3" stroke="currentColor" stroke-width="2"/><circle cx="12" cy="15.5" r="1.4" fill="currentColor"/></svg></div>
          <p>Vista centralizada<br>Scores y fuentes trazables<br>Preparado para auth y equipos</p>
        </div>
      </article>
    </div>
  </div>
</section>

<!-- ============ USE CASES ============ -->
<section class="section section--tight" style="background:var(--surface-2); border-top:1px solid var(--line); border-bottom:1px solid var(--line);">
  <div class="container">
    <div class="section-head">
      <span class="eyebrow">Casos de uso</span>
      <h2 class="h2">Diseñado para cómo trabajan de verdad los operadores.</h2>
    </div>
    <div class="cases">
      <div class="case reveal">
        <div class="case__ic"><svg viewBox="0 0 24 24" fill="none"><path d="M9 18h6m-5 3h4M12 3a6 6 0 0 0-4 10.5c.7.7 1 1.3 1 2.5h6c0-1.2.3-1.8 1-2.5A6 6 0 0 0 12 3Z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg></div>
        <div>
          <h3>Encuentra ideas SaaS</h3>
          <p>Empieza desde una lista ordenada de huecos validados en vez de una página en blanco, y ahórrate meses de rastreo manual.</p>
        </div>
      </div>
      <div class="case reveal">
        <div class="case__ic"><svg viewBox="0 0 24 24" fill="none"><circle cx="11" cy="11" r="7" stroke="currentColor" stroke-width="2"/><path d="m20 20-3.5-3.5" stroke="currentColor" stroke-width="2" stroke-linecap="round"/></svg></div>
        <div>
          <h3>Monitoriza nichos emergentes</h3>
          <p>Añade una categoría a tu seguimiento y recibe un aviso en cuanto el momentum o la saturación crucen tu umbral.</p>
        </div>
      </div>
      <div class="case reveal">
        <div class="case__ic"><svg viewBox="0 0 24 24" fill="none"><path d="M4 19V9m5 10V5m5 14v-7m5 7V8" stroke="currentColor" stroke-width="2" stroke-linecap="round"/></svg></div>
        <div>
          <h3>Rastrea la demanda de herramientas dev</h3>
          <p>Mira qué primitivas están adoptando de verdad los builders, por stars, hilos y cadencia de releases, no por intuición.</p>
        </div>
      </div>
      <div class="case reveal">
        <div class="case__ic"><svg viewBox="0 0 24 24" fill="none"><path d="M6 3h9l5 5v13H6z" stroke="currentColor" stroke-width="2" stroke-linejoin="round"/><path d="M9 12h7M9 16h5" stroke="currentColor" stroke-width="2" stroke-linecap="round"/></svg></div>
        <div>
          <h3>Prepara informes de oportunidad semanales</h3>
          <p>Exporta un brief limpio y respaldado por fuentes para tu equipo o inversores en minutos, sin copiar y pegar de doce pestañas.</p>
        </div>
      </div>
    </div>
  </div>
</section>

<!-- ============ SAMPLE OUTPUT ============ -->
<section class="section" id="samples">
  <div class="container">
    <div class="section-head">
      <span class="eyebrow">Ejemplo de salida</span>
      <h2 class="h2">Un vistazo a lo que llega a tu dashboard cada semana.</h2>
      <p class="lead">Ejemplos reales de tendencias con score, categoría, señales de origen y un breve brief. Este es el formato en el que llega cada tendencia.</p>
    </div>

    <div class="samples">
      <div class="filters" id="filters">
        <button class="filter is-active" data-cat="all">Todas</button>
        <button class="filter" data-cat="ai">AI infra</button>
        <button class="filter" data-cat="dev">Dev tools</button>
        <button class="filter" data-cat="fintech">Fintech</button>
      </div>

      <div class="sample-grid" id="sample-grid">
        <!-- card 1 -->
        <article class="scard" data-cat="ai">
          <div class="scard__top">
            <div class="scard__big">91<small>/100</small></div>
            <span class="tag tag--accent">Actúa ya</span>
          </div>
          <h3>Gateways LLM self-hosted</h3>
          <div class="scard__cat">AI infra · trend score</div>
          <p class="scard__brief">Los equipos quieren control de costes y residencia de datos sin reescribir su stack. El tooling está fragmentado y sin un default claro: una cuña evidente para un producto managed o self-hosted.</p>
          <div class="scard__scores">
            <div class="scard__score"><label>Oportunidad</label><div class="meter__bar"><div class="meter__fill meter__fill--accent" style="--val:88%"></div></div><b>88</b></div>
            <div class="scard__score"><label>Momentum</label><div class="meter__bar"><div class="meter__fill meter__fill--pos" style="--val:72%"></div></div><b>+62%</b></div>
            <div class="scard__score"><label>Saturación</label><div class="meter__bar"><div class="meter__fill meter__fill--warn" style="--val:31%"></div></div><b>31</b></div>
          </div>
          <div class="scard__foot">
            <div class="scard__sources"><span class="src src--gh"><i></i>GitHub</span><span class="src src--hn"><i></i>HN</span></div>
            <a href="#beta" class="scard__link">Abrir brief <svg viewBox="0 0 24 24" fill="none"><path d="M7 17 17 7M9 7h8v8" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg></a>
          </div>
        </article>

        <!-- card 2 -->
        <article class="scard" data-cat="dev">
          <div class="scard__top">
            <div class="scard__big">84<small>/100</small></div>
            <span class="tag tag--accent">Al alza</span>
          </div>
          <h3>Agentes de IA para testing QA</h3>
          <div class="scard__cat">Dev tools · trend score</div>
          <p class="scard__brief">La fatiga de tests flaky se une a un tooling de agentes maduro. Los builders montan suites de tests self-healing, pero no hay un default de confianza: fuerte demanda, saturación moderada.</p>
          <div class="scard__scores">
            <div class="scard__score"><label>Oportunidad</label><div class="meter__bar"><div class="meter__fill meter__fill--accent" style="--val:81%"></div></div><b>81</b></div>
            <div class="scard__score"><label>Momentum</label><div class="meter__bar"><div class="meter__fill meter__fill--pos" style="--val:60%"></div></div><b>+47%</b></div>
            <div class="scard__score"><label>Saturación</label><div class="meter__bar"><div class="meter__fill meter__fill--warn" style="--val:44%"></div></div><b>44</b></div>
          </div>
          <div class="scard__foot">
            <div class="scard__sources"><span class="src src--gh"><i></i>GitHub</span><span class="src src--rss"><i></i>RSS</span></div>
            <a href="#beta" class="scard__link">Abrir brief <svg viewBox="0 0 24 24" fill="none"><path d="M7 17 17 7M9 7h8v8" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg></a>
          </div>
        </article>

        <!-- card 3 -->
        <article class="scard" data-cat="fintech">
          <div class="scard__top">
            <div class="scard__big">79<small>/100</small></div>
            <span class="tag tag--accent">Vigilar</span>
          </div>
          <h3>Automatización de compliance para IA</h3>
          <div class="scard__cat">Fintech · trend score</div>
          <p class="scard__brief">La nueva regulación de IA obliga a los equipos a documentar el uso de modelos. La demanda aparece en feeds e hilos antes de que existan productos: temprano, poco saturado y de alta intención.</p>
          <div class="scard__scores">
            <div class="scard__score"><label>Oportunidad</label><div class="meter__bar"><div class="meter__fill meter__fill--accent" style="--val:73%"></div></div><b>73</b></div>
            <div class="scard__score"><label>Momentum</label><div class="meter__bar"><div class="meter__fill meter__fill--pos" style="--val:52%"></div></div><b>+38%</b></div>
            <div class="scard__score"><label>Saturación</label><div class="meter__bar"><div class="meter__fill meter__fill--pos" style="--val:27%"></div></div><b>27</b></div>
          </div>
          <div class="scard__foot">
            <div class="scard__sources"><span class="src src--rss"><i></i>RSS</span><span class="src src--hn"><i></i>HN</span></div>
            <a href="#beta" class="scard__link">Abrir brief <svg viewBox="0 0 24 24" fill="none"><path d="M7 17 17 7M9 7h8v8" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg></a>
          </div>
        </article>
      </div>
    </div>
  </div>
</section>

<!-- ============ BETA CTA ============ -->
<section class="section" id="beta">
  <div class="container">
    <div class="beta__card reveal">
      <div class="beta__left">
        <span class="eyebrow">Beta privada</span>
        <h2>Únete a la beta privada</h2>
        <p class="lead">Estamos incorporando a un grupo reducido de founders y product operators para dar forma a lo que se puntúa, se resume y se construye a continuación.</p>
        <ul class="beta__points">
          <li><svg viewBox="0 0 24 24" fill="none"><path d="m5 13 4 4 10-10" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"/></svg>Acceso anticipado al dashboard de tendencias con score</li>
          <li><svg viewBox="0 0 24 24" fill="none"><path d="m5 13 4 4 10-10" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"/></svg>Briefs de oportunidad cuando abramos la beta</li>
          <li><svg viewBox="0 0 24 24" fill="none"><path d="m5 13 4 4 10-10" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"/></svg>Línea directa para influir en el roadmap</li>
        </ul>
      </div>
      <div class="beta__right">
        <form class="form" id="beta-form" novalidate>
          <div class="field" id="f-email">
            <label for="email">Email de trabajo <span class="req">obligatorio</span></label>
            <input class="input" type="email" id="email" name="email" placeholder="tu@empresa.com" autocomplete="email">
            <span class="field__err" data-err="email">Introduce un email válido.</span>
          </div>

          <div class="field" id="f-role">
            <label for="role">Tu rol <span class="req">obligatorio</span></label>
            <select class="select" id="role" name="role">
              <option value="" disabled selected>Selecciona tu rol…</option>
              <option>Founder / cofundador</option>
              <option>Indie hacker</option>
              <option>Product manager</option>
              <option>Venture scout / inversor</option>
              <option>Otro</option>
            </select>
            <span class="field__err" data-err="role">Elige un rol.</span>
          </div>

          <div class="field" id="f-interests">
            <label>Intereses <span class="muted" style="text-transform:none;letter-spacing:0;">opcional · elige los que quieras</span></label>
            <div class="chips" id="chips">
              <button type="button" class="chip" data-v="AI infra" aria-pressed="false"><svg class="chip__tick" viewBox="0 0 24 24" fill="none"><path d="m5 13 4 4 10-10" stroke="currentColor" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round"/></svg>AI infra</button>
              <button type="button" class="chip" data-v="Dev tools" aria-pressed="false"><svg class="chip__tick" viewBox="0 0 24 24" fill="none"><path d="m5 13 4 4 10-10" stroke="currentColor" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round"/></svg>Dev tools</button>
              <button type="button" class="chip" data-v="Fintech" aria-pressed="false"><svg class="chip__tick" viewBox="0 0 24 24" fill="none"><path d="m5 13 4 4 10-10" stroke="currentColor" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round"/></svg>Fintech</button>
              <button type="button" class="chip" data-v="Datos / analítica" aria-pressed="false"><svg class="chip__tick" viewBox="0 0 24 24" fill="none"><path d="m5 13 4 4 10-10" stroke="currentColor" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round"/></svg>Datos / analítica</button>
              <button type="button" class="chip" data-v="Vertical SaaS" aria-pressed="false"><svg class="chip__tick" viewBox="0 0 24 24" fill="none"><path d="m5 13 4 4 10-10" stroke="currentColor" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round"/></svg>Vertical SaaS</button>
            </div>
            <input type="hidden" name="interests" id="interests-val">
          </div>

          <div class="form__foot">
            <button type="submit" class="btn btn--primary btn--lg btn--block" id="submit-btn">Solicitar acceso a la beta</button>
            <p class="form__micro">Estamos incorporando a un grupo reducido de founders y product operators. Sin spam: solo acceso anticipado y algún brief de vez en cuando.</p>
          </div>
        </form>

        <div class="form-success" id="form-success">
          <div class="form-success__ic"><svg viewBox="0 0 24 24" fill="none"><path d="m5 13 4 4 10-10" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"/></svg></div>
          <h3>Estás en la lista.</h3>
          <p>Gracias. Te escribiremos cuando abramos la siguiente tanda de plazas de la beta. Echa un ojo a tu inbox.</p>
          <div class="mono-line" id="success-line">→ confirmación en cola</div>
        </div>
      </div>
    </div>
  </div>
</section>

</main>

<!-- ============ FOOTER ============ -->
<footer class="footer">
  <div class="container">
    <div class="footer__top">
      <div class="footer__brand">
        <a class="brand" href="#top">
          <span class="brand__mark"><svg viewBox="0 0 24 24" fill="none"><path d="M3 17.5 9.2 11l3.6 3.3L21 6.5" stroke="currentColor" stroke-width="2.1" stroke-linecap="round" stroke-linejoin="round"/></svg></span>
          AI Trend Hunter
        </a>
        <p>Inteligencia de mercado que lee la señal pública para que construyas antes de que la tendencia sea obvia.</p>
      </div>
      <div class="footer__cols">
        <div class="footer__col">
          <h6>Producto</h6>
          <a href="#solution">Cómo funciona</a>
          <a href="#features">Funciones</a>
          <a href="#samples">Ejemplo de salida</a>
          <a href="#beta">Únete a la beta</a>
        </div>
        <div class="footer__col">
          <h6>Fuentes</h6>
          <a href="#top">GitHub</a>
          <a href="#top">Hacker News</a>
          <a href="#top">Feeds RSS</a>
        </div>
        <div class="footer__col">
          <h6>Empresa</h6>
          <a href="#top">Sobre nosotros</a>
          <a href="/privacy">Privacidad</a>
          <a href="/terms">Terminos</a>
          <a href="#top">Contacto</a>
        </div>
      </div>
    </div>
    <div class="footer__bot">
      <span>© 2026 AI Trend Hunter</span>
      <span>Señales dentro · oportunidades fuera</span>
    </div>
  </div>
</footer>`;

export default function LandingPage() {
  return (
    <>
      <div
        className="landing-page"
        data-hero="centered"
        data-density="regular"
        dangerouslySetInnerHTML={{ __html: landingMarkup }}
      />
      <LandingInteractions />
    </>
  );
}
