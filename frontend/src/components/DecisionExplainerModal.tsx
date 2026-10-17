import React from 'react';
import { Modal } from './ui/Modal';
import { Cpu, Database, ShieldAlert, TrendingUp } from 'lucide-react';

export interface DecisionExplainerModalProps {
  isOpen: boolean;
  onClose: () => void;
}

export const DecisionExplainerModal: React.FC<DecisionExplainerModalProps> = ({
  isOpen,
  onClose,
}) => {
  return (
    <Modal
      isOpen={isOpen}
      onClose={onClose}
      title="How RetailIQ Decisions Are Grounded & Made"
      description="The deterministic decision loop connecting customer need, real stock, and executive action"
      maxWidth="2xl"
    >
      <div className="space-y-6 text-sm text-text-primary">
        <div className="bg-primary-light border border-blue-200 rounded-card p-4">
          <p className="font-medium text-navy-800 leading-relaxed">
            <strong className="text-primary font-bold">Core Architectural Differentiator:</strong> RetailIQ never permits AI to invent stock quantities, prices, or financial commitments. Gemini handles language understanding and fact extraction, while deterministic algorithms and PostgreSQL/SQLite row locks handle all inventory reservations, lead-time simulations, and capital allocations.
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div className="border border-border rounded-card p-4 bg-surface shadow-sm">
            <div className="flex items-center gap-2 mb-2 text-primary font-semibold">
              <Cpu className="w-5 h-5" />
              <span>1. Semantic Need Interpretation</span>
            </div>
            <p className="text-xs text-text-secondary leading-relaxed">
              Gemini extracts structured intent attributes (capacity ≥ 10,000 mAh, connector = USB-C, max price = ₹1,500, fulfillment = pickup today). If preferred item (VoltGo Pro) is out of stock across the network, it locates factual alternatives without hallucinations.
            </p>
          </div>

          <div className="border border-border rounded-card p-4 bg-surface shadow-sm">
            <div className="flex items-center gap-2 mb-2 text-primary font-semibold">
              <Database className="w-5 h-5" />
              <span>2. Authoritative Database ATP</span>
            </div>
            <p className="text-xs text-text-secondary leading-relaxed">
              Available-To-Promise is calculated directly from ledger balances:
              <br />
              <code className="text-[11px] bg-slate-100 text-navy-900 px-1 py-0.5 rounded font-mono block mt-1">
                ATP = on_hand - blocked - holds - orders - transfers_out
              </code>
              Guarantees zero ghost stock and prevents over-promising across omni-channel orders.
            </p>
          </div>

          <div className="border border-border rounded-card p-4 bg-surface shadow-sm">
            <div className="flex items-center gap-2 mb-2 text-primary font-semibold">
              <TrendingUp className="w-5 h-5" />
              <span>3. Transfer vs Purchase Optimization</span>
            </div>
            <p className="text-xs text-text-secondary leading-relaxed">
              When S1 faces an impending stockout on VoltGo Go, the engine audits the entire network:
              <br />
              • <strong>Transfer from S2:</strong> 32 units excess, arrives in 1 day, ₹0 working capital, ₹15,074 margin.
              <br />
              • <strong>Purchase:</strong> Supplier MOQ 36 units, arrives in 5 days, ties up ₹25,380 capital.
            </p>
          </div>

          <div className="border border-border rounded-card p-4 bg-surface shadow-sm">
            <div className="flex items-center gap-2 mb-2 text-primary font-semibold">
              <ShieldAlert className="w-5 h-5" />
              <span>4. Mandatory Human Approval Gate</span>
            </div>
            <p className="text-xs text-text-secondary leading-relaxed">
              Every business transfer or catalog patch requires explicit manager sign-off. Approval sets the transfer to <span className="font-mono text-[11px] font-semibold text-review">PENDING_DISPATCH</span>; recipient stock remains unpromoted until warehouse physical receipt is confirmed.
            </p>
          </div>
        </div>

        <div className="border-t border-border pt-4 flex items-center justify-between">
          <span className="text-xs text-text-secondary">
            Deterministic Engine · Autonomous Multi-Echelon Replenishment
          </span>
          <button
            onClick={onClose}
            className="px-4 py-2 bg-navy-800 hover:bg-navy-900 text-white rounded-input text-xs font-semibold"
          >
            Close & Continue
          </button>
        </div>
      </div>
    </Modal>
  );
};
