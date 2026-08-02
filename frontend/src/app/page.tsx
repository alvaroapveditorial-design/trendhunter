import { LandingInteractions } from "@/components/LandingInteractions";

export const metadata = {
  title: "AI Trend Hunter - Detect emerging SaaS opportunities",
  description:
    "AI Trend Hunter analyzes GitHub, Hacker News, and RSS to detect emerging SaaS trends with scoring and opportunity briefs.",
  openGraph: {
    title: "AI Trend Hunter",
    description:
      "Detect emerging SaaS opportunities before they're obvious, with public signals, scoring, and actionable briefs.",
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
      <a href="#problem">Why</a>
      <a href="#solution">How it works</a>
      <a href="#features">Features</a>
      <a href="#samples">Sample output</a>
    </nav>
    <div class="nav__cta">
      <a href="/dashboard" class="btn btn--ghost">View dashboard</a>
      <a href="/pricing" class="btn btn--primary">Try 7 days</a>
      <button class="nav__burger" id="burger" aria-label="Try 7 days">
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
      <span class="eyebrow">Market intelligence for builders</span>
      <h1 class="display">Detect emerging<br>SaaS opportunities <em>before</em><br>they're obvious.</h1>
      <p class="lead">AI Trend Hunter analyzes public signal — <strong>GitHub</strong>, <strong>Hacker News</strong>, and <strong>RSS</strong> — groups it into scored trends, and delivers actionable opportunity briefs. Weak signals in, validated product ideas out.</p>
      <div class="hero__cta">
        <a href="/pricing" class="btn btn--primary btn--lg">Try 7 days free
          <svg viewBox="0 0 24 24" fill="none"><path d="M5 12h14M13 6l6 6-6 6" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>
        </a>
        <a href="/dashboard" class="btn btn--ghost btn--lg">View dashboard</a>
      </div>
      <div class="hero__meta">
        <span><b>3</b> unified public sources</span>
        <span><b>4</b> scores per trend</span>
        <span>7-day trial · 39 EUR/month after</span>
      </div>
    </div>

    <!-- dashboard mockup -->
    <div class="dashboard-wrap reveal" id="hero-dash">
      <div class="app">
        <div class="app__bar">
          <div class="app__dots"><i></i><i></i><i></i></div>
          <div class="app__omni">
            <svg viewBox="0 0 24 24" fill="none"><circle cx="11" cy="11" r="7" stroke="currentColor" stroke-width="2"/><path d="m20 20-3.5-3.5" stroke="currentColor" stroke-width="2" stroke-linecap="round"/></svg>
            app.aitrendhunter.app/dashboard
          </div>
          <div class="app__bar-right">
            <span class="tag">Sample view</span>
            <div class="app__avatar"></div>
          </div>
        </div>
        <div class="app__body">
          <!-- sidebar -->
          <aside class="app__side">
            <a class="brand" href="#"><span class="brand__mark"><svg viewBox="0 0 24 24" fill="none"><path d="M3 17.5 9.2 11l3.6 3.3L21 6.5" stroke="currentColor" stroke-width="2.1" stroke-linecap="round" stroke-linejoin="round"/></svg></span>Trend Hunter</a>
            <nav class="navlist">
              <a href="#top" class="is-active"><svg viewBox="0 0 24 24" fill="none"><path d="M4 19V9m5 10V5m5 14v-7m5 7V8" stroke="currentColor" stroke-width="2" stroke-linecap="round"/></svg>Trends</a>
              <a href="#top"><svg viewBox="0 0 24 24" fill="none"><circle cx="12" cy="12" r="3" stroke="currentColor" stroke-width="2"/><path d="M12 3v3m0 12v3m9-9h-3M6 12H3" stroke="currentColor" stroke-width="2" stroke-linecap="round"/></svg>Sources</a>
              <a href="#top"><svg viewBox="0 0 24 24" fill="none"><path d="M6 3h9l5 5v13H6z" stroke="currentColor" stroke-width="2" stroke-linejoin="round"/><path d="M9 12h7M9 16h5" stroke="currentColor" stroke-width="2" stroke-linecap="round"/></svg>Briefs</a>
              <a href="#top"><svg viewBox="0 0 24 24" fill="none"><path d="M12 4c4 4 7 5 7 5s0 8-7 11c-7-3-7-11-7-11s3-1 7-5Z" stroke="currentColor" stroke-width="2" stroke-linejoin="round"/></svg>Tracking</a>
              <span class="navlist__label">Account</span>
              <a href="#top"><svg viewBox="0 0 24 24" fill="none"><circle cx="12" cy="8" r="3.4" stroke="currentColor" stroke-width="2"/><path d="M5 20c1.5-3.5 4-5 7-5s5.5 1.5 7 5" stroke="currentColor" stroke-width="2" stroke-linecap="round"/></svg>Profile</a>
              <a href="#top"><svg viewBox="0 0 24 24" fill="none"><circle cx="12" cy="12" r="3" stroke="currentColor" stroke-width="2"/><path d="m19.4 13.5.7 1.5-2 2-1.5-.7a6 6 0 0 1-1.6.9L14.5 21h-3l-.5-1.8a6 6 0 0 1-1.6-.9l-1.5.7-2-2 .7-1.5a6 6 0 0 1-.9-1.6L4 12.5v-3l1.8-.5c.2-.6.5-1.1.9-1.6l-.7-1.5 2-2 1.5.7c.5-.4 1-.7 1.6-.9L11.5 1h3l.5 1.8c.6.2 1.1.5 1.6.9l1.5-.7 2 2-.7 1.5c.4.5.7 1 .9 1.6L22 9.5v3l-1.8.5c-.2.6-.5 1.1-.8 1.5Z" stroke="currentColor" stroke-width="1.6" stroke-linejoin="round"/></svg>Settings</a>
            </nav>
          </aside>

          <!-- main -->
          <section class="app__main">
            <div class="app__main-head">
              <div>
                <h4>Emerging trends</h4>
                <p>Sorted by opportunity score · illustrative sample, not live data</p>
              </div>
              <span class="app__week">
                <svg width="13" height="13" viewBox="0 0 24 24" fill="none"><rect x="3" y="5" width="18" height="16" rx="2" stroke="currentColor" stroke-width="2"/><path d="M3 9h18M8 3v4m8-4v4" stroke="currentColor" stroke-width="2" stroke-linecap="round"/></svg>
                Week 23 · 2026
              </span>
            </div>

            <div class="ttable">
              <div class="trow trow--head">
                <span>Trend</span><span>Category</span><span>Opportunity</span><span>Saturation</span><span>Mom.</span>
              </div>

              <div class="trow">
                <div class="trow__name">
                  <b>Self-hosted LLM gateways</b>
                  <div class="trow__sources"><span class="src src--gh"><i></i>GitHub ×41</span><span class="src src--hn"><i></i>HN ×12</span></div>
                </div>
                <div class="trow__cat"><span class="tag tag--accent">AI infra</span></div>
                <div class="meter" data-label="Opportunity"><div class="meter__row"><div class="meter__bar"><div class="meter__fill meter__fill--accent" style="--val:88%"></div></div><span class="meter__num">88</span></div></div>
                <div class="meter" data-label="Saturation"><div class="meter__row"><div class="meter__bar"><div class="meter__fill meter__fill--pos" style="--val:31%"></div></div><span class="meter__num">31</span></div></div>
                <div class="spark"><svg viewBox="0 0 64 24" preserveAspectRatio="none"><polyline points="0,20 11,18 22,15 32,12 43,7 54,5 64,2" fill="none" stroke="var(--pos)" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg><span class="spark__v">+62%</span></div>
              </div>

              <div class="trow">
                <div class="trow__name">
                  <b>AI agents for QA testing</b>
                  <div class="trow__sources"><span class="src src--gh"><i></i>GitHub ×28</span><span class="src src--rss"><i></i>RSS ×9</span></div>
                </div>
                <div class="trow__cat"><span class="tag tag--accent">Dev tools</span></div>
                <div class="meter" data-label="Opportunity"><div class="meter__row"><div class="meter__bar"><div class="meter__fill meter__fill--accent" style="--val:81%"></div></div><span class="meter__num">81</span></div></div>
                <div class="meter" data-label="Saturation"><div class="meter__row"><div class="meter__bar"><div class="meter__fill meter__fill--pos" style="--val:44%"></div></div><span class="meter__num">44</span></div></div>
                <div class="spark"><svg viewBox="0 0 64 24" preserveAspectRatio="none"><polyline points="0,18 11,16 22,17 32,12 43,10 54,6 64,4" fill="none" stroke="var(--pos)" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg><span class="spark__v">+47%</span></div>
              </div>

              <div class="trow">
                <div class="trow__name">
                  <b>Local-first sync engines</b>
                  <div class="trow__sources"><span class="src src--gh"><i></i>GitHub ×33</span><span class="src src--hn"><i></i>HN ×7</span></div>
                </div>
                <div class="trow__cat"><span class="tag tag--accent">Dev tools</span></div>
                <div class="meter" data-label="Opportunity"><div class="meter__row"><div class="meter__bar"><div class="meter__fill meter__fill--accent" style="--val:76%"></div></div><span class="meter__num">76</span></div></div>
                <div class="meter" data-label="Saturation"><div class="meter__row"><div class="meter__bar"><div class="meter__fill meter__fill--warn" style="--val:58%"></div></div><span class="meter__num">58</span></div></div>
                <div class="spark"><svg viewBox="0 0 64 24" preserveAspectRatio="none"><polyline points="0,14 11,15 22,12 32,13 43,10 54,9 64,7" fill="none" stroke="var(--pos)" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg><span class="spark__v">+29%</span></div>
              </div>

              <div class="trow">
                <div class="trow__name">
                  <b>AI compliance automation</b>
                  <div class="trow__sources"><span class="src src--rss"><i></i>RSS ×15</span><span class="src src--hn"><i></i>HN ×6</span></div>
                </div>
                <div class="trow__cat"><span class="tag tag--accent">Fintech</span></div>
                <div class="meter" data-label="Opportunity"><div class="meter__row"><div class="meter__bar"><div class="meter__fill meter__fill--accent" style="--val:73%"></div></div><span class="meter__num">73</span></div></div>
                <div class="meter" data-label="Saturation"><div class="meter__row"><div class="meter__bar"><div class="meter__fill meter__fill--pos" style="--val:27%"></div></div><span class="meter__num">27</span></div></div>
                <div class="spark"><svg viewBox="0 0 64 24" preserveAspectRatio="none"><polyline points="0,19 11,17 22,16 32,14 43,11 54,9 64,8" fill="none" stroke="var(--pos)" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg><span class="spark__v">+38%</span></div>
              </div>
            </div>
          </section>
        </div>
      </div>

      <!-- floating brief annotation -->
      <aside class="float-brief">
        <span class="eyebrow">Opportunity brief</span>
        <h5>Self-hosted LLM gateways</h5>
        <p>Teams want cost control and data residency. Tooling is fragmented, with no clear default. Strong builder demand, low commercial saturation.</p>
        <div class="float-brief__foot">
          <span class="float-brief__score">Trend score <b>91</b></span>
          <span class="tag tag--accent">Act now</span>
        </div>
      </aside>
    </div>
  </div>
</section>

<!-- ============ LOGO STRIP ============ -->
<section class="section--tight">
  <div class="container">
    <p class="eyebrow eyebrow--plain muted" style="text-align:center; display:block; margin-bottom:26px;">Signal pulled from the three places ideas show up first</p>
    <div class="logos">
      <span>GitHub</span><span>Hacker News</span><span>RSS feeds</span>
    </div>
  </div>
</section>

<!-- ============ PROBLEM ============ -->
<section class="section section--dark" id="problem">
  <div class="container">
    <div class="section-head">
      <span class="eyebrow">The problem</span>
      <h2 class="h2">By the time a trend makes it into a report, the window has already closed.</h2>
    </div>
    <div class="problem__grid">
      <div class="problem__item reveal">
        <div class="problem__n">01</div>
        <h3>Founders lose hours to scattered sources</h3>
        <p>Reading repos, threads, and feeds across a dozen tabs every week isn't research — it's a part-time job that rarely turns into a decision.</p>
      </div>
      <div class="problem__item reveal">
        <div class="problem__n">02</div>
        <h3>Signal shows up in code first, not coverage</h3>
        <p>The earliest evidence lives in GitHub repos, Hacker News threads, and RSS feeds, months before it shows up in a trend report or newsletter.</p>
      </div>
      <div class="problem__item reveal">
        <div class="problem__n">03</div>
        <h3>Noise hides the real opportunity</h3>
        <p>For every real shift there are ten hype cycles. Without scoring, it's impossible to tell a lasting opportunity from a noisy weekend.</p>
      </div>
    </div>
  </div>
</section>

<!-- ============ SOLUTION ============ -->
<section class="section" id="solution">
  <div class="container">
    <div class="section-head">
      <span class="eyebrow">How it works</span>
      <h2 class="h2">Public signals in. Scored trends out. Briefs to act on.</h2>
      <p class="lead">A single pipeline turns the flood of public developer activity into a short, ranked list of opportunities, each backed by the evidence it came from.</p>
    </div>

    <div class="pipe">
      <div class="pipe__step reveal">
        <div class="pipe__k">STEP 01</div>
        <h3>Public signals in</h3>
        <p>We continuously collect stars, commits, threads, points, and feed entries from GitHub, Hacker News, and RSS.</p>
        <div class="pipe__viz srcviz">
          <div class="srcviz__row"><span class="src src--gh"><i></i>GitHub</span><span class="srcviz__bar"><i style="--val:90%"></i></span></div>
          <div class="srcviz__row"><span class="src src--hn"><i></i>Hacker News</span><span class="srcviz__bar"><i style="--val:64%"></i></span></div>
          <div class="srcviz__row"><span class="src src--rss"><i></i>RSS</span><span class="srcviz__bar"><i style="--val:48%"></i></span></div>
        </div>
      </div>
      <div class="pipe__arrow"><svg viewBox="0 0 24 24" fill="none"><path d="M5 12h14M13 6l6 6-6 6" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg></div>
      <div class="pipe__step reveal">
        <div class="pipe__k">STEP 02</div>
        <h3>Scored trends out</h3>
        <p>Signals are clustered into trends and scored for momentum, opportunity, and saturation, so ranking stays objective.</p>
        <div class="pipe__viz scoreviz">
          <div class="scoreviz__item"><div class="scoreviz__top"><span>Opportunity</span><b>88</b></div><div class="meter__bar"><div class="meter__fill meter__fill--accent" style="--val:88%"></div></div></div>
          <div class="scoreviz__item"><div class="scoreviz__top"><span>Momentum</span><b>+62%</b></div><div class="meter__bar"><div class="meter__fill meter__fill--pos" style="--val:72%"></div></div></div>
          <div class="scoreviz__item"><div class="scoreviz__top"><span>Saturation</span><b>31</b></div><div class="meter__bar"><div class="meter__fill meter__fill--warn" style="--val:31%"></div></div></div>
        </div>
      </div>
      <div class="pipe__arrow"><svg viewBox="0 0 24 24" fill="none"><path d="M5 12h14M13 6l6 6-6 6" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg></div>
      <div class="pipe__step reveal">
        <div class="pipe__k">STEP 03</div>
        <h3>Briefs to act on</h3>
        <p>Each standout trend becomes a short SaaS opportunity brief: who, why now, and where the gap is.</p>
        <div class="pipe__viz briefviz">
          <h6>Self-hosted LLM gateways</h6>
          <ul>
            <li>Who: platform and infra teams</li>
            <li>Why now: cost + data residency</li>
            <li>Gap: no clear default</li>
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
      <span class="eyebrow">Features</span>
      <h2 class="h2">Everything you need to turn a signal into a product decision.</h2>
    </div>

    <div class="features">
      <article class="feature reveal">
        <div class="feature__ix">/01</div>
        <div class="feature__main">
          <h3>Multi-source signal collection</h3>
          <p>An ingestion layer unifies the three places opportunities show up first, so you stop tab-hopping and start comparing apples to apples.</p>
          <div class="feature__tags"><span class="tag">GitHub</span><span class="tag">Hacker News</span><span class="tag">RSS</span></div>
        </div>
        <div class="feature__viz srcviz">
          <div class="srcviz__row">Repos and stars<span class="src src--gh"><i></i>GitHub</span></div>
          <div class="srcviz__row">Threads and points<span class="src src--hn"><i></i>HN</span></div>
          <div class="srcviz__row">Changelogs and feeds<span class="src src--rss"><i></i>RSS</span></div>
        </div>
      </article>

      <article class="feature reveal">
        <div class="feature__ix">/02</div>
        <div class="feature__main">
          <h3>Trend scoring</h3>
          <p>Every trend carries four numbers — trend score, opportunity, saturation, and momentum — so prioritizing is a glance, not a debate.</p>
          <div class="feature__tags"><span class="tag tag--accent">Momentum</span><span class="tag tag--accent">Opportunity</span><span class="tag tag--accent">Saturation</span></div>
        </div>
        <div class="feature__viz scoreviz">
          <div class="scoreviz__item"><div class="scoreviz__top"><span>Trend score</span><b>91</b></div><div class="meter__bar"><div class="meter__fill meter__fill--accent" style="--val:91%"></div></div></div>
          <div class="scoreviz__item"><div class="scoreviz__top"><span>Opportunity</span><b>88</b></div><div class="meter__bar"><div class="meter__fill meter__fill--accent" style="--val:88%"></div></div></div>
          <div class="scoreviz__item"><div class="scoreviz__top"><span>Saturation</span><b>31</b></div><div class="meter__bar"><div class="meter__fill meter__fill--warn" style="--val:31%"></div></div></div>
        </div>
      </article>

      <article class="feature reveal">
        <div class="feature__ix">/03</div>
        <div class="feature__main">
          <h3>Source-backed evidence</h3>
          <p>No black box. Every score links to the exact repos, threads, and feed entries it came from, so you can verify before you bet.</p>
          <div class="feature__tags"><span class="tag">Traceable</span><span class="tag">Auditable</span></div>
        </div>
        <div class="feature__viz evidence">
          <div class="evidence__line"><span class="src src--gh"><i></i>GH</span>llm-gateway · +312 stars / 14d</div>
          <div class="evidence__line"><span class="src src--hn"><i></i>HN</span>"Show HN: route LLMs locally" · 284▲</div>
          <div class="evidence__line"><span class="src src--rss"><i></i>RSS</span>3 infra blogs · cost and residency</div>
        </div>
      </article>

      <article class="feature reveal">
        <div class="feature__ix">/04</div>
        <div class="feature__main">
          <h3>SaaS opportunity briefs</h3>
          <p>Top trends get written up as short, actionable briefs: the audience, the timing, and the specific gap a product could fill.</p>
          <div class="feature__tags"><span class="tag">Who and why now</span><span class="tag">Gap analysis</span></div>
        </div>
        <div class="feature__viz briefviz">
          <h6>Brief · AI agents for QA</h6>
          <ul>
            <li>Who: fast-shipping platform teams</li>
            <li>Why now: flaky-test fatigue + agent tooling</li>
            <li>Gap: no trusted self-healing default</li>
          </ul>
        </div>
      </article>

      <article class="feature reveal">
        <div class="feature__ix">/05</div>
        <div class="feature__main">
          <h3>Decision-first dashboard</h3>
          <p>Every session opens with the single best opportunity this week, fully briefed — ICP, competition, MVP to build, monetization, risks — plus four ranked shortlists underneath. No table to interpret first.</p>
          <div class="feature__tags"><span class="tag">Best opportunity first</span><span class="tag">Ranked shortlists</span><span class="tag">Full trend history</span></div>
        </div>
        <div class="feature__viz lockviz">
          <div class="lockviz__ic"><svg viewBox="0 0 24 24" fill="none"><rect x="5" y="11" width="14" height="9" rx="2" stroke="currentColor" stroke-width="2"/><path d="M8 11V8a4 4 0 0 1 8 0v3" stroke="currentColor" stroke-width="2"/><circle cx="12" cy="15.5" r="1.4" fill="currentColor"/></svg></div>
          <p>One best pick, every session<br>ICP, MVP, and risks included<br>Ranked opportunities, not raw data</p>
        </div>
      </article>
    </div>
  </div>
</section>

<!-- ============ USE CASES ============ -->
<section class="section section--tight" style="background:var(--surface-2); border-top:1px solid var(--line); border-bottom:1px solid var(--line);">
  <div class="container">
    <div class="section-head">
      <span class="eyebrow">Use cases</span>
      <h2 class="h2">Built for how operators actually work.</h2>
    </div>
    <div class="cases">
      <div class="case reveal">
        <div class="case__ic"><svg viewBox="0 0 24 24" fill="none"><path d="M9 18h6m-5 3h4M12 3a6 6 0 0 0-4 10.5c.7.7 1 1.3 1 2.5h6c0-1.2.3-1.8 1-2.5A6 6 0 0 0 12 3Z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg></div>
        <div>
          <h3>Find SaaS ideas</h3>
          <p>Start from a ranked list of validated gaps instead of a blank page, and save yourself months of manual tracking.</p>
        </div>
      </div>
      <div class="case reveal">
        <div class="case__ic"><svg viewBox="0 0 24 24" fill="none"><circle cx="11" cy="11" r="7" stroke="currentColor" stroke-width="2"/><path d="m20 20-3.5-3.5" stroke="currentColor" stroke-width="2" stroke-linecap="round"/></svg></div>
        <div>
          <h3>Compare momentum and saturation</h3>
          <p>Filter by category and sort by momentum or saturation to see which niches are heating up and which are already crowded, before you commit.</p>
        </div>
      </div>
      <div class="case reveal">
        <div class="case__ic"><svg viewBox="0 0 24 24" fill="none"><path d="M4 19V9m5 10V5m5 14v-7m5 7V8" stroke="currentColor" stroke-width="2" stroke-linecap="round"/></svg></div>
        <div>
          <h3>Track dev tool demand</h3>
          <p>See which primitives builders are actually adopting, by stars, threads, and release cadence — not by gut feel.</p>
        </div>
      </div>
      <div class="case reveal">
        <div class="case__ic"><svg viewBox="0 0 24 24" fill="none"><path d="M6 3h9l5 5v13H6z" stroke="currentColor" stroke-width="2" stroke-linejoin="round"/><path d="M9 12h7M9 16h5" stroke="currentColor" stroke-width="2" stroke-linecap="round"/></svg></div>
        <div>
          <h3>Review the evidence before you commit</h3>
          <p>Every score links back to the exact repos, threads, and feed entries it came from, so you can check the evidence before betting on an idea.</p>
        </div>
      </div>
    </div>
  </div>
</section>

<!-- ============ SAMPLE OUTPUT ============ -->
<section class="section" id="samples">
  <div class="container">
    <div class="section-head">
      <span class="eyebrow">Sample output</span>
      <h2 class="h2">A peek at what lands in your dashboard every week.</h2>
      <p class="lead">Illustrative sample cards showing the score, category, source signals, and brief format every trend arrives in. For a real, dated example, see <a href="/pricing#real-example" style="text-decoration:underline;">the real example on the pricing page</a>.</p>
    </div>

    <div class="samples">
      <div class="filters" id="filters">
        <button class="filter is-active" data-cat="all">All</button>
        <button class="filter" data-cat="ai">AI infra</button>
        <button class="filter" data-cat="dev">Dev tools</button>
        <button class="filter" data-cat="fintech">Fintech</button>
      </div>

      <div class="sample-grid" id="sample-grid">
        <!-- card 1 -->
        <article class="scard" data-cat="ai">
          <div class="scard__top">
            <div class="scard__big">91<small>/100</small></div>
            <div style="display:flex; gap:6px;"><span class="tag">Sample</span><span class="tag tag--accent">Act now</span></div>
          </div>
          <h3>Self-hosted LLM gateways</h3>
          <div class="scard__cat">AI infra · trend score</div>
          <p class="scard__brief">Teams want cost control and data residency without rewriting their stack. Tooling is fragmented with no clear default: an obvious wedge for a managed or self-hosted product.</p>
          <div class="scard__scores">
            <div class="scard__score"><label>Opportunity</label><div class="meter__bar"><div class="meter__fill meter__fill--accent" style="--val:88%"></div></div><b>88</b></div>
            <div class="scard__score"><label>Momentum</label><div class="meter__bar"><div class="meter__fill meter__fill--pos" style="--val:72%"></div></div><b>+62%</b></div>
            <div class="scard__score"><label>Saturation</label><div class="meter__bar"><div class="meter__fill meter__fill--warn" style="--val:31%"></div></div><b>31</b></div>
          </div>
          <div class="scard__foot">
            <div class="scard__sources"><span class="src src--gh"><i></i>GitHub</span><span class="src src--hn"><i></i>HN</span></div>
            <a href="/pricing" class="scard__link">Open brief <svg viewBox="0 0 24 24" fill="none"><path d="M7 17 17 7M9 7h8v8" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg></a>
          </div>
        </article>

        <!-- card 2 -->
        <article class="scard" data-cat="dev">
          <div class="scard__top">
            <div class="scard__big">84<small>/100</small></div>
            <div style="display:flex; gap:6px;"><span class="tag">Sample</span><span class="tag tag--accent">Rising</span></div>
          </div>
          <h3>AI agents for QA testing</h3>
          <div class="scard__cat">Dev tools · trend score</div>
          <p class="scard__brief">Flaky-test fatigue meets mature agent tooling. Builders are assembling self-healing test suites, but there's no trusted default: strong demand, moderate saturation.</p>
          <div class="scard__scores">
            <div class="scard__score"><label>Opportunity</label><div class="meter__bar"><div class="meter__fill meter__fill--accent" style="--val:81%"></div></div><b>81</b></div>
            <div class="scard__score"><label>Momentum</label><div class="meter__bar"><div class="meter__fill meter__fill--pos" style="--val:60%"></div></div><b>+47%</b></div>
            <div class="scard__score"><label>Saturation</label><div class="meter__bar"><div class="meter__fill meter__fill--warn" style="--val:44%"></div></div><b>44</b></div>
          </div>
          <div class="scard__foot">
            <div class="scard__sources"><span class="src src--gh"><i></i>GitHub</span><span class="src src--rss"><i></i>RSS</span></div>
            <a href="/pricing" class="scard__link">Open brief <svg viewBox="0 0 24 24" fill="none"><path d="M7 17 17 7M9 7h8v8" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg></a>
          </div>
        </article>

        <!-- card 3 -->
        <article class="scard" data-cat="fintech">
          <div class="scard__top">
            <div class="scard__big">79<small>/100</small></div>
            <div style="display:flex; gap:6px;"><span class="tag">Sample</span><span class="tag tag--accent">Watch</span></div>
          </div>
          <h3>AI compliance automation</h3>
          <div class="scard__cat">Fintech · trend score</div>
          <p class="scard__brief">New AI regulation is forcing teams to document model usage. Demand shows up in feeds and threads before products exist: early, low saturation, high intent.</p>
          <div class="scard__scores">
            <div class="scard__score"><label>Opportunity</label><div class="meter__bar"><div class="meter__fill meter__fill--accent" style="--val:73%"></div></div><b>73</b></div>
            <div class="scard__score"><label>Momentum</label><div class="meter__bar"><div class="meter__fill meter__fill--pos" style="--val:52%"></div></div><b>+38%</b></div>
            <div class="scard__score"><label>Saturation</label><div class="meter__bar"><div class="meter__fill meter__fill--pos" style="--val:27%"></div></div><b>27</b></div>
          </div>
          <div class="scard__foot">
            <div class="scard__sources"><span class="src src--rss"><i></i>RSS</span><span class="src src--hn"><i></i>HN</span></div>
            <a href="/pricing" class="scard__link">Open brief <svg viewBox="0 0 24 24" fill="none"><path d="M7 17 17 7M9 7h8v8" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg></a>
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
        <span class="eyebrow">Not ready to start the trial?</span>
        <h2>Stay in the loop</h2>
        <p class="lead">AI Trend Hunter is live — you can <a href="/pricing" style="text-decoration:underline;">start the 7-day trial today</a>. If you'd rather watch first, leave your email and we'll keep you posted.</p>
        <ul class="beta__points">
          <li><svg viewBox="0 0 24 24" fill="none"><path d="m5 13 4 4 10-10" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"/></svg>Occasional updates when new features ship</li>
          <li><svg viewBox="0 0 24 24" fill="none"><path d="m5 13 4 4 10-10" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"/></svg>Standout opportunities we spot along the way</li>
          <li><svg viewBox="0 0 24 24" fill="none"><path d="m5 13 4 4 10-10" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"/></svg>A direct line to shape the roadmap</li>
        </ul>
      </div>
      <div class="beta__right">
        <form class="form" id="beta-form" novalidate>
          <div class="field" id="f-email">
            <label for="email">Work email <span class="req">required</span></label>
            <input class="input" type="email" id="email" name="email" placeholder="you@company.com" autocomplete="email">
            <span class="field__err" data-err="email">Enter a valid email.</span>
          </div>

          <div class="field" id="f-role">
            <label for="role">Your role <span class="req">required</span></label>
            <select class="select" id="role" name="role">
              <option value="" disabled selected>Select your role…</option>
              <option>Founder / co-founder</option>
              <option>Indie hacker</option>
              <option>Product manager</option>
              <option>Venture scout / investor</option>
              <option>Other</option>
            </select>
            <span class="field__err" data-err="role">Choose a role.</span>
          </div>

          <div class="field" id="f-interests">
            <label>Interests <span class="muted" style="text-transform:none;letter-spacing:0;">optional · pick as many as you like</span></label>
            <div class="chips" id="chips">
              <button type="button" class="chip" data-v="AI infra" aria-pressed="false"><svg class="chip__tick" viewBox="0 0 24 24" fill="none"><path d="m5 13 4 4 10-10" stroke="currentColor" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round"/></svg>AI infra</button>
              <button type="button" class="chip" data-v="Dev tools" aria-pressed="false"><svg class="chip__tick" viewBox="0 0 24 24" fill="none"><path d="m5 13 4 4 10-10" stroke="currentColor" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round"/></svg>Dev tools</button>
              <button type="button" class="chip" data-v="Fintech" aria-pressed="false"><svg class="chip__tick" viewBox="0 0 24 24" fill="none"><path d="m5 13 4 4 10-10" stroke="currentColor" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round"/></svg>Fintech</button>
              <button type="button" class="chip" data-v="Data / analytics" aria-pressed="false"><svg class="chip__tick" viewBox="0 0 24 24" fill="none"><path d="m5 13 4 4 10-10" stroke="currentColor" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round"/></svg>Data / analytics</button>
              <button type="button" class="chip" data-v="Vertical SaaS" aria-pressed="false"><svg class="chip__tick" viewBox="0 0 24 24" fill="none"><path d="m5 13 4 4 10-10" stroke="currentColor" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round"/></svg>Vertical SaaS</button>
            </div>
            <input type="hidden" name="interests" id="interests-val">
          </div>

          <div class="form__foot">
            <button type="submit" class="btn btn--primary btn--lg btn--block" id="submit-btn">Keep me posted</button>
            <p class="form__micro">No spam — just occasional product updates and the odd standout opportunity.</p>
          </div>
        </form>

        <div class="form-success" id="form-success">
          <div class="form-success__ic"><svg viewBox="0 0 24 24" fill="none"><path d="m5 13 4 4 10-10" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"/></svg></div>
          <h3>You're on the list.</h3>
          <p>Thanks — we'll keep you posted. Whenever you're ready, the 7-day trial is one click away on the pricing page.</p>
          <div class="mono-line" id="success-line">→ confirmation queued</div>
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
        <p>Market intelligence that reads the public signal so you can build before the trend is obvious.</p>
      </div>
      <div class="footer__cols">
        <div class="footer__col">
          <h6>Product</h6>
          <a href="#solution">How it works</a>
          <a href="#features">Features</a>
          <a href="#samples">Sample output</a>
          <a href="#beta">Get product updates</a>
        </div>
        <div class="footer__col">
          <h6>Sources</h6>
          <span class="footer__static">GitHub</span>
          <span class="footer__static">Hacker News</span>
          <span class="footer__static">RSS feeds</span>
        </div>
        <div class="footer__col">
          <h6>Company</h6>
          <a href="/privacy">Privacy</a>
          <a href="/terms">Terms</a>
          <a href="/contact">Contact</a>
        </div>
      </div>
    </div>
    <div class="footer__bot">
      <span>© 2026 AI Trend Hunter</span>
      <span>Signals in · opportunities out</span>
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
