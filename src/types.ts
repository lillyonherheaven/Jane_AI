export type AgentPersonaType = 'general' | 'coder' | 'researcher' | 'sysadmin';

export type LanguageMode = 'en' | 'ar';

export interface ChatMessage {
  id: string;
  sender: 'user' | 'assistant' | 'system';
  content: string;
  timestamp: string;
  persona?: AgentPersonaType;
  toolsUsed?: string[];
  ragSources?: Array<{
    source: string;
    score: number;
    chunkId: string;
  }>;
  visionImage?: string;
  executionResult?: {
    tool: string;
    success: boolean;
    output?: any;
    error?: string;
    durationMs?: number;
  };
}

export interface HardwareMetrics {
  cpuUsagePct: number;
  ramUsedGb: number;
  ramTotalGb: number;
  ramPercent: number;
  gpuUsagePct: number;
  gpuVramUsedGb: number;
  gpuVramTotalGb: number;
  activeProcesses: number;
  ollamaStatus: 'online' | 'inferring' | 'standby';
  activeModel: string;
  temperatureC: number;
}

export interface RAGDocument {
  id: string;
  name: string;
  type: 'pdf' | 'markdown' | 'code' | 'paper';
  chunkCount: number;
  uploadedAt: string;
  sizeKb: number;
  chunks: Array<{
    id: string;
    text: string;
    vectorScore: number;
    bm25Score: number;
    combinedScore: number;
  }>;
}

export interface SecurityEvent {
  id: string;
  timestamp: string;
  type: 'injection_blocked' | 'dangerous_cmd_blocked' | 'path_traversal_blocked' | 'safe_pass';
  detail: string;
  input: string;
}

export interface PythonFileItem {
  name: string;
  path: string;
  description: string;
  category: 'core' | 'agent' | 'multimodal' | 'data' | 'security' | 'gui' | 'audio';
  content: string;
}
