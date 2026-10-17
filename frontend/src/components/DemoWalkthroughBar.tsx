import React, { useState, useEffect } from 'react';
import { 
  ChevronRight, ChevronLeft, Sparkles, CheckCircle2, 
  Eye, EyeOff, Video, ArrowRight
} from 'lucide-react';

export interface DemoStep {
  id: number;
  view: 'shopper' | 'associate' | 'business' | 'trace';
  title: string;
  role: string;
  duration: string;
  cue: string;
  voiceover: string;
  actionHint: string;
}

export const DEMO_STEPS: DemoStep[] = [
  {
    id: 1,
    view: 'shopper',
    title: 'Shopper Intent & AI Recovery',
    role: 'Priya (Shopper)',
    duration: '0:00 - 0:50',
    cue: 'Search for "10,000 mAh USB-C power bank under ₹1,500, pickup today. Prefer VoltGo Pro."',
    voiceover: 'A customer expresses a natural language need. Gemini extracts constraints, detects preferred VoltGo Pro is OUT OF STOCK (ATP 0), and instantly grounds a verified in-stock substitute: VoltGo Go (RQ002). We create a 15-min reservation hold and place the order.',
    actionHint: 'Click "⚡ Find Matching Stock", then "Reserve for 15 Min", then "Place Order".'
  },
  {
    id: 2,
    view: 'associate',
    title: 'Store Pickup & Stock Decrement',
    role: 'Arjun (Store Associate)',
    duration: '0:50 - 1:20',
    cue: 'Associate sees ORD-20261017-001 in queue. Fulfills handover upon customer verification.',
    voiceover: 'Store Associate Arjun receives the pickup order in real-time. With one click, Arjun fulfills pickup. Authoritative physical inventory drops from 12 to 11 units in the database ledger with zero race conditions.',
    actionHint: 'Click "Fulfill Pickup Handover" on the order card.'
  },
  {
    id: 3,
    view: 'business',
    title: 'Planning: Transfer Beats Purchase',
    role: 'Maya (Business Manager)',
    duration: '1:20 - 1:55',
    cue: 'Pickup triggers stockout risk. System evaluates Transfer vs Purchase.',
    voiceover: 'The purchase triggers an impending stockout. RetailIQ evaluates options: Supplier purchase requires 36 units and ties up ₹25,380 working capital with 5-day lead time. Inter-store transfer from Whitefield Store needs ₹0 capital, arrives in 24 hours, and recovers ₹15,074 margin. Manager approves the transfer.',
    actionHint: 'Open Priority Decisions tab and click "Approve Transfer".'
  },
  {
    id: 4,
    view: 'associate',
    title: 'Inter-Store Rebalance Execution',
    role: 'Arjun (Associate)',
    duration: '1:55 - 2:15',
    cue: 'Dispatch units from Whitefield Store and receive at Indiranagar Store.',
    voiceover: 'The transfer appears in the associate queue. Whitefield Store dispatches the units. When received at Indiranagar Store, stock is shelved into live ATP. 100% mathematical stock conservation is preserved across the network.',
    actionHint: 'Switch to Transfers tab, click "Dispatch Transfer", then "Receive Transfer".'
  },
  {
    id: 5,
    view: 'business',
    title: 'AI Restraint & Trend Intelligence',
    role: 'Maya (Manager)',
    duration: '2:15 - 2:35',
    cue: 'Show EXT01 (Solar Lantern - ACT) vs EXT02 (Glow Clip - MONITOR).',
    voiceover: 'RetailIQ demonstrates genuine AI restraint. A high-intent solar lantern search surge justifies an 18-unit safety purchase order. But a viral social media glow clip with weak basket conversion is dampened to MONITOR ONLY with 0 units ordered, protecting capital.',
    actionHint: 'Click "Demand & Trends" tab in Business Intelligence.'
  },
  {
    id: 6,
    view: 'trace',
    title: 'Cryptographic Audit & Integrity',
    role: 'Auditor & System',
    duration: '2:35 - 2:50',
    cue: 'Show immutable cryptographic event trail of all movements and approvals.',
    voiceover: 'Every single event—from shopper search to reservation, physical decrement, and rebalancing—is recorded with cryptographic hashes and movement IDs. Built with React, FastAPI, PostgreSQL, and Gemini for the AI Builder Cup 2026.',
    actionHint: 'Review the live timeline of orders, movements, and approvals.'
  }
];

interface DemoWalkthroughBarProps {
  currentView: 'shopper' | 'associate' | 'business' | 'trace';
  onNavigate: (view: 'shopper' | 'associate' | 'business' | 'trace') => void;
}

export const DemoWalkthroughBar: React.FC<DemoWalkthroughBarProps> = ({
  currentView,
  onNavigate,
}) => {
  const [currentStepIndex, setCurrentStepIndex] = useState(0);
  const [isExpanded, setIsExpanded] = useState(true);

  // Sync step if currentView changed outside
  useEffect(() => {
    const matchingStep = DEMO_STEPS.findIndex(s => s.view === currentView);
    if (matchingStep !== -1 && DEMO_STEPS[currentStepIndex].view !== currentView) {
      setCurrentStepIndex(matchingStep);
    }
  }, [currentView, currentStepIndex]);

  const step = DEMO_STEPS[currentStepIndex];

  const handleStepClick = (idx: number) => {
    setCurrentStepIndex(idx);
    onNavigate(DEMO_STEPS[idx].view);
  };

  const handleNext = () => {
    if (currentStepIndex < DEMO_STEPS.length - 1) {
      handleStepClick(currentStepIndex + 1);
    }
  };

  const handlePrev = () => {
    if (currentStepIndex > 0) {
      handleStepClick(currentStepIndex - 1);
    }
  };

  return (
    <div className="bg-navy-900 text-white border-b border-navy-800 shadow-md transition-all">
      <div className="max-w-7xl mx-auto px-4 py-2.5 sm:px-6 lg:px-8">
        {/* Top Control Bar */}
        <div className="flex items-center justify-between gap-3 text-xs">
          <div className="flex items-center gap-2">
            <span className="flex items-center gap-1.5 px-2 py-0.5 rounded bg-primary text-white font-bold tracking-wider text-[11px] uppercase">
              <Video className="w-3.5 h-3.5" />
              Demo Director
            </span>
            <span className="text-slate-300 font-medium hidden sm:inline">
              Step {step.id} of {DEMO_STEPS.length}:
            </span>
            <span className="font-semibold text-cyan truncate max-w-[200px] sm:max-w-none">
              {step.title}
            </span>
            <span className="text-slate-400 text-[11px] hidden md:inline">
              ({step.duration})
            </span>
          </div>

          <div className="flex items-center gap-2">
            {/* Step navigation buttons */}
            <div className="flex items-center bg-navy-800 rounded border border-navy-700 p-0.5">
              <button
                onClick={handlePrev}
                disabled={currentStepIndex === 0}
                className="p-1 text-slate-300 hover:text-white disabled:opacity-40 hover:bg-navy-700 rounded transition-colors"
                title="Previous Demo Step"
              >
                <ChevronLeft className="w-3.5 h-3.5" />
              </button>
              <span className="px-2 font-mono text-[11px] text-slate-300">
                {currentStepIndex + 1}/{DEMO_STEPS.length}
              </span>
              <button
                onClick={handleNext}
                disabled={currentStepIndex === DEMO_STEPS.length - 1}
                className="p-1 text-slate-300 hover:text-white disabled:opacity-40 hover:bg-navy-700 rounded transition-colors"
                title="Next Demo Step"
              >
                <ChevronRight className="w-3.5 h-3.5" />
              </button>
            </div>

            {/* Toggle collapse */}
            <button
              onClick={() => setIsExpanded(!isExpanded)}
              className="flex items-center gap-1 px-2 py-1 text-slate-300 hover:text-white hover:bg-navy-800 rounded transition-colors text-[11px]"
              title={isExpanded ? 'Collapse presenter cue' : 'Expand presenter cue'}
            >
              {isExpanded ? <EyeOff className="w-3.5 h-3.5" /> : <Eye className="w-3.5 h-3.5" />}
              <span className="hidden sm:inline">{isExpanded ? 'Hide Cue' : 'Show Cue'}</span>
            </button>
          </div>
        </div>

        {/* Step Indicator Pills */}
        <div className="flex items-center gap-1.5 mt-2 overflow-x-auto pb-1 scrollbar-none">
          {DEMO_STEPS.map((s, idx) => (
            <button
              key={s.id}
              onClick={() => handleStepClick(idx)}
              className={`flex-shrink-0 px-2.5 py-1 rounded text-[11px] font-medium transition-all flex items-center gap-1.5 ${
                currentStepIndex === idx
                  ? 'bg-cyan text-navy-900 font-bold shadow-sm'
                  : 'bg-navy-800 text-slate-300 hover:bg-navy-700 hover:text-white'
              }`}
            >
              <span className={`w-4 h-4 rounded-full flex items-center justify-center text-[10px] font-bold ${
                currentStepIndex === idx ? 'bg-navy-900 text-cyan' : 'bg-navy-700 text-slate-300'
              }`}>
                {s.id}
              </span>
              <span>{s.title}</span>
            </button>
          ))}
        </div>

        {/* Expanded Script Cue & Guidance Box */}
        {isExpanded && (
          <div className="mt-2.5 p-3 rounded-lg bg-navy-800/90 border border-navy-700 text-xs text-slate-200 grid grid-cols-1 md:grid-cols-3 gap-3">
            <div className="md:col-span-2 space-y-1.5">
              <div className="flex items-center gap-2 text-cyan font-semibold">
                <Sparkles className="w-3.5 h-3.5" />
                <span>Voiceover Script ({step.duration}):</span>
              </div>
              <p className="italic text-slate-300 leading-relaxed pl-5 border-l-2 border-cyan/60">
                "{step.voiceover}"
              </p>
            </div>

            <div className="space-y-1.5 md:border-l md:border-navy-700 md:pl-3">
              <div className="text-amber-300 font-semibold flex items-center gap-1.5">
                <CheckCircle2 className="w-3.5 h-3.5" />
                <span>Action to Perform:</span>
              </div>
              <p className="text-slate-300 text-[11px] leading-relaxed">
                {step.actionHint}
              </p>
              <button
                onClick={() => onNavigate(step.view)}
                className="mt-1 inline-flex items-center gap-1 text-[11px] text-cyan hover:underline font-semibold"
              >
                Go to {step.role} View <ArrowRight className="w-3 h-3" />
              </button>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};
