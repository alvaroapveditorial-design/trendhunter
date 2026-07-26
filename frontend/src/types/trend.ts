export type TrendSource = {
  id: string;
  source_type: string;
  source_url?: string | null;
  title?: string | null;
  upvotes: number;
  comments: number;
  published_at?: string | null;
};

export type Trend = {
  id: string;
  title: string;
  slug: string;
  description?: string | null;
  trend_score: number;
  opportunity_score: number;
  saturation_score: number;
  momentum: number;
  category: string;
  keywords: string[];
  tags: string[];
  mentions_count: number;
  engagement_count: number;
  source_count: number;
  primary_source_type?: string | null;
  is_active: boolean;
  is_verified: boolean;
  detected_at: string;
  last_updated_at: string;
};

export type OpportunityScores = {
  market: number;
  competition: number;
  urgency: number;
  viability: number;
  potential: number;
};

export type OpportunityBrief = {
  executive_summary?: string | null;
  why_now: string;
  icp: string;
  problem: string;
  competition_level: string;
  mvp_recommendation: string;
  monetization_models: string[];
  risks: string[];
  market_velocity: string;
  market_size_signal: string;
  scores: OpportunityScores;
};

export type TrendDetail = Trend & {
  ai_insights?: string | null;
  saas_opportunities: string[];
  sources: TrendSource[];
  opportunity_brief?: OpportunityBrief | null;
};

export type TrendSpotlight = {
  best_opportunity: TrendDetail | null;
  top_opportunities: Trend[];
  emerging_markets: Trend[];
  underserved_niches: Trend[];
  accelerating: Trend[];
};

export type IngestionRun = {
  processed_signals: number;
  created_trends: number;
  updated_trends: number;
  trend_ids: string[];
  trends: Trend[];
};

export type AgentExecution = {
  id: string;
  agent_name: string;
  agent_type: string;
  status: string;
  records_processed: number;
  records_created: number;
  records_updated: number;
  duration_seconds?: number | null;
  error_message?: string | null;
  started_at: string;
  completed_at?: string | null;
};
