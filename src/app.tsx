import React, { useState, useEffect } from 'react';
import { Sidebar } from './components/Sidebar';
import { ChatView } from './components/ChatView';
import { VisionInspector } from './components/VisionInspector';
import { RAGVault } from './components/RAGVault';
import { AutomationSandbox } from './components/AutomationSandbox';
import { CodeExplorer } from './components/CodeExplorer';
import { SetupGuide } from './components/SetupGuide';
import { FloatingWidget } from './components/FloatingWidget';
import { AgentPersonaType, ChatMessage, HardwareMetrics, LanguageMode } from './types';

export default function App() {
  const [activeTab, setActiveTab] = useState<'chat' | 'vision' | 'rag' | 'automation' | 'code' | 'setup'>('chat');
  const [activePersona, setActivePersona] = useState<AgentPersonaType>('general');
  const [language, setLanguage] = useState<LanguageMode>('en');
  const [ragEnabled, setRagEnabled] = useState(true);
  const [webSearchEnabled, setWebSearchEnabled] = useState(false);
  const [audioState, setAudioState] = useState<'idle' | 'listening' | 'thinking' | 'speaking'>('idle');
  const [isFloatingWidgetOpen, setIsFloatingWidgetOpen] = useState(false);

  const [hardware, setHardware] = useState<HardwareMetrics>({
    cpuUsagePct: 16,
    ramUsedGb: 6.4,
    ramTotalGb: 16.0,
    ramPercent: 40,
    gpuUsagePct: 10,
    gpuVramUsedGb: 4.2,
    gpuVramTotalGb: 8.0,
    activeProcesses: 188,
    ollamaStatus: 'online',
    activeModel: 'llama3.2:latest',
    temperatureC: 44
  });

  const [messages, setMessages] = useState<ChatMessage[]>([
    {
      id: 'msg_1',
      sender: 'assistant',
      content: `Hello. I am Jane-AI, your 100% local, privacy-first autonomous companion.

• Core Intelligence: Ollama (Llama 3.2 & Llama 3.2 Vision)
• Knowledge Vault: ChromaDB + Rank-BM25 Hybrid Retrieval
• Desktop Automation: Sandboxed PyAutoGUI & psutil tool execution
• Zero-Cloud Guarantee: All processing and encryption remain strictly on your local machine.

How can I assist your workflow today?`,
      timestamp: '10:45 AM',
      persona: 'general'
    }
  ]);

  // Global hotkey Ctrl+Space listener
  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      if ((e.ctrlKey || e.metaKey) && e.code === 'Space') {
        e.preventDefault();
        setIsFloatingWidgetOpen((prev) => !prev);
      }
    };
    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, []);

  // Hardware telemetry simulator
  useEffect(() => {
    const interval = setInterval(() => {
      setHardware((prev) => ({
        ...prev,
        cpuUsagePct: Math.floor(Math.random() * 12) + 12,
        ramUsedGb: Number((6.2 + Math.random() * 0.3).toFixed(1)),
        ramPercent: Math.floor(Math.random() * 3) + 39,
      }));
    }, 4000);
    return () => clearInterval(interval);
  }, []);

  const handleSendMessage = (text: string) => {
    const userMsg: ChatMessage = {
      id: `msg_${Date.now()}`,
      sender: 'user',
      content: text,
      timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
    };

    setMessages((prev) => [...prev, userMsg]);
    setAudioState('thinking');

    // Multi-Agent response generator
    setTimeout(() => {
      const lower = text.toLowerCase();
      let persona: AgentPersonaType = activePersona;
      let reply = '';
      let toolsUsed: string[] | undefined;
      let executionResult: any;
      let ragSources: any;

      if (lower.includes('code') || lower.includes('python') || lower.includes('bug') || lower.includes('كود') || lower.includes('دالة')) {
        persona = 'coder';
        reply = language === 'ar'
          ? `[رد مهندس البرمجيات: Coder Specialist]
لقد قمت بفحص الهيكلية وتجهيز الدالة المطلوبة باستخدام بايثون 3.10+ مع التحقق من الأنواع والتعامل مع الاستثناءات:

\`\`\`python
import asyncio
from typing import List, Dict, Any

async def process_chunks_concurrently(chunks: List[str]) -> List[Dict[str, Any]]:
    """معالجة متزامنة غير متزامنة لمقاطع النصوص المحلية."""
    tasks = [asyncio.create_task(_async_embed_chunk(c)) for c in chunks]
    return await asyncio.gather(*tasks)

async def _async_embed_chunk(chunk: str) -> Dict[str, Any]:
    await asyncio.sleep(0.01)
    return {"length": len(chunk), "status": "processed"}
\`\`\`
هذا الكود مُهيأ ليعمل داخل البيئة المعزولة محلياً.`
          : `[Lead Coder Response]
Here is the clean, type-annotated, modular implementation for local execution:

\`\`\`python
import asyncio
from typing import List, Dict, Any

async def process_chunks_concurrently(chunks: List[str]) -> List[Dict[str, Any]]:
    """Asynchronously processes and embeds document chunks locally."""
    tasks = [asyncio.create_task(_async_embed_chunk(c)) for c in chunks]
    return await asyncio.gather(*tasks)

async def _async_embed_chunk(chunk: str) -> Dict[str, Any]:
    await asyncio.sleep(0.01)
    return {"length": len(chunk), "status": "processed"}
\`\`\`
Adheres strictly to PEP 8 standards with zero external telemetry.`;
      } else if (lower.includes('cpu') || lower.includes('ram') || lower.includes('process') || lower.includes('telemetry') || lower.includes('معالج') || lower.includes('ذاكرة')) {
        persona = 'sysadmin';
        toolsUsed = ['psutil.get_system_telemetry'];
        executionResult = {
          tool: 'psutil.get_system_telemetry',
          success: true,
          durationMs: 38,
          output: {
            cpu_percent: hardware.cpuUsagePct,
            ram_used_gb: hardware.ramUsedGb,
            ram_total_gb: hardware.ramTotalGb,
            ram_percent: hardware.ramPercent,
            top_process: 'ollama_llama3.2 (PID 1084)',
            status: 'HEALTHY'
          }
        };
        reply = language === 'ar'
          ? `[تقرير مدير النظام: SysAdmin Agent]
تم استرجاع مقاييس العتاد المحلي بنجاح عبر psutil. جميع الموارد تعمل في نطاق آمن ومستقر دون أي ضغط حراري.`
          : `[SysAdmin Agent Report]
Retrieved real-time hardware telemetry via psutil. The host system is performing normally with ample available RAM.`;
      } else if (lower.includes('rag') || lower.includes('pdf') || lower.includes('paper') || lower.includes('vault') || lower.includes('بحث') || lower.includes('لخص')) {
        persona = 'researcher';
        ragSources = [
          { source: 'Llama_3_2_Technical_Report.pdf', score: 0.92, chunkId: 'llama_chunk_1' },
          { source: 'ChromaDB_Hybrid_BM25_Specification.md', score: 0.87, chunkId: 'chroma_chunk_1' }
        ];
        reply = language === 'ar'
          ? `[ملخص باحث الوثائق: ChromaDB + BM25 Hybrid]
بناءً على مقاطع البحث المسترجعة من مستودع المعرفة المحلي:
1. يدعم نموذج Llama 3.2 نافذة سياق تصل إلى 128 ألف رمز مع تحسينات GQA للأجهزة الشخصية.
2. يدمج محرك البحث الهجين تطابق الكلمات المفتاحية BM25 مع التشابه الدلالي Cosine بدقة عالية.`
          : `[Academic Research Synthesis: ChromaDB + BM25 Hybrid]
Based on the retrieved context from your local document vault:
1. Llama 3.2 Architecture: Features Grouped-Query Attention (GQA) optimized for efficient desktop and on-device execution with 128k context windows.
2. Hybrid RAG Precision: Combining dense embeddings with Okapi BM25 sparse keyword indices prevents terminology hallucinations.`;
      } else if (lower.includes('ignore') || lower.includes('system: override') || lower.includes('bypass') || lower.includes('jailbreak')) {
        reply = language === 'ar'
          ? `[تنبيه حارس الأمان: Security Guard]
تم حجب محاولة حقن التوجيهات (Prompt Injection). يعمل النظام وفق سياسات أمان محلية صارمة تمنع تعديل أوامر النظام الأساسية.`
          : `[Security Guard Alert]
Adversarial prompt injection pattern detected and sanitized. System prompts and sandbox constraints remain securely locked.`;
      } else {
        reply = language === 'ar'
          ? `أنا في خدمتك. يمكنك سؤالي عن البرمجة، إدارة مهام سطح المكتب، فحص الوثائق عبر مستودع RAG، أو التقاط الشاشة وتحليل الأخطاء عبر Llama 3.2 Vision.`
          : `I am ready to assist. You can ask me to write code, inspect desktop screens with Llama 3.2 Vision, query the hybrid ChromaDB RAG vault, or execute sandboxed PC automation tools.`;
      }

      const botMsg: ChatMessage = {
        id: `msg_${Date.now() + 1}`,
        sender: 'assistant',
        content: reply,
        timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
        persona,
        toolsUsed,
        executionResult,
        ragSources
      };

      setMessages((prev) => [...prev, botMsg]);
      setAudioState('speaking');
      setTimeout(() => setAudioState('idle'), 2200);
    }, 1100);
  };

  return (
    <div className="flex h-screen w-screen bg-[#0D0D0D] text-[#F4F4F5] overflow-hidden select-none font-sans">
      {/* Left Sidebar */}
      <Sidebar
        activeTab={activeTab}
        setActiveTab={setActiveTab}
        activePersona={activePersona}
        setActivePersona={setActivePersona}
        language={language}
        setLanguage={setLanguage}
        ragEnabled={ragEnabled}
        setRagEnabled={setRagEnabled}
        webSearchEnabled={webSearchEnabled}
        setWebSearchEnabled={setWebSearchEnabled}
        hardware={hardware}
        onToggleFloatingWidget={() => setIsFloatingWidgetOpen(true)}
      />

      {/* Primary Dynamic Workspace View */}
      <main className="flex-1 flex flex-col h-full overflow-hidden">
        {activeTab === 'chat' && (
          <ChatView
            messages={messages}
            onSendMessage={handleSendMessage}
            activePersona={activePersona}
            language={language}
            audioState={audioState}
            setAudioState={setAudioState}
            onQuickVision={() => setActiveTab('vision')}
            onQuickRAG={() => setActiveTab('rag')}
          />
        )}

        {activeTab === 'vision' && <VisionInspector language={language} />}

        {activeTab === 'rag' && <RAGVault language={language} />}

        {activeTab === 'automation' && <AutomationSandbox language={language} />}

        {activeTab === 'code' && <CodeExplorer language={language} />}

        {activeTab === 'setup' && <SetupGuide language={language} />}
      </main>

      {/* Global Quick-Access Floating Overlay (Ctrl+Space) */}
      <FloatingWidget
        isOpen={isFloatingWidgetOpen}
        onClose={() => setIsFloatingWidgetOpen(false)}
        onSubmit={(query) => {
          setActiveTab('chat');
          handleSendMessage(query);
        }}
        language={language}
      />
    </div>
  );
}
