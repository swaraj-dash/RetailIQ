import React from 'react';
import { Store, ShoppingBag, PackageCheck, BarChart3, History, RotateCcw } from 'lucide-react';

export interface AppHeaderProps {
  currentView: 'shopper' | 'associate' | 'business' | 'trace';
  onViewChange: (view: 'shopper' | 'associate' | 'business' | 'trace') => void;
  selectedStore: string;
  onStoreChange: (store: string) => void;
  isBackendHealthy: boolean;
  onOpenDecisionExplainer?: () => void;
  onResetState?: () => void;
  isResetting?: boolean;
}

export const AppHeader: React.FC<AppHeaderProps> = ({
  currentView,
  onViewChange,
  selectedStore,
  onStoreChange,
  isBackendHealthy,
  onResetState,
  isResetting,
}) => {
  const stores = [
    { code: 'S1', name: 'Indiranagar Store' },
    { code: 'S2', name: 'Whitefield Store' },
    { code: 'S3', name: 'Koramangala Store' },
    { code: 'DC1', name: 'Nelamangala Central DC' },
  ];

  return (
    <header className="sticky top-0 z-40 bg-white border-b border-border shadow-sm">
      {/* Main Header Row: Brand & Context Controls */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-14 border-b border-slate-100">
          {/* Left: Brand Identity */}
          <div className="flex items-center gap-3">
            <div className="w-8 h-8 rounded-lg bg-primary flex items-center justify-center text-white shadow font-black text-base tracking-wider">
              R
            </div>
            <div className="flex items-center gap-2">
              <span className="text-lg font-black tracking-tight text-slate-900">
                Retail<span className="text-primary font-bold">IQ</span>
              </span>
              <span className="hidden sm:inline-block text-[11px] font-semibold px-2 py-0.5 bg-blue-50 text-primary border border-blue-200 rounded-full">
                Retail & Commerce
              </span>
            </div>
          </div>

          {/* Right: Operational Store Context & System Status */}
          <div className="flex items-center gap-3">
            {/* Store Location Switcher */}
            <div className="flex items-center gap-1.5 bg-slate-50 border border-slate-200 rounded-lg px-2.5 py-1">
              <Store className="w-3.5 h-3.5 text-slate-500" />
              <span className="text-xs text-slate-500 font-medium hidden sm:inline">Store:</span>
              <select
                value={selectedStore}
                onChange={(e) => onStoreChange(e.target.value)}
                aria-label="Select Store Location"
                className="text-xs font-semibold bg-transparent text-slate-800 focus:outline-none cursor-pointer pr-1"
              >
                {stores.map((s) => (
                  <option key={s.code} value={s.code}>
                    {s.name}
                  </option>
                ))}
              </select>
            </div>

            {/* Live Health Status */}
            <div
              className="flex items-center gap-1.5 pl-2 border-l border-slate-200 text-xs"
              title={isBackendHealthy ? 'Database and API live' : 'Connecting to local backend...'}
            >
              <span
                className={`w-2 h-2 rounded-full ${
                  isBackendHealthy ? 'bg-emerald-500 shadow-[0_0_6px_rgba(16,185,129,0.7)]' : 'bg-amber-500 animate-pulse'
                }`}
              />
              <span className="text-[11px] font-medium text-slate-600 hidden md:inline">
                {isBackendHealthy ? 'Live API' : 'Syncing'}
              </span>
            </div>

            {/* Reset Prototype Baseline */}
            {onResetState && (
              <button
                onClick={onResetState}
                disabled={isResetting}
                title="Restore prototype baseline (resets pending decisions, inventory ATP & orders back to initial)"
                className="flex items-center gap-1.5 px-2.5 py-1 text-xs font-semibold rounded-lg border border-slate-200 bg-slate-50 hover:bg-slate-100 text-slate-700 transition-colors shadow-sm disabled:opacity-50"
              >
                <RotateCcw className={`w-3.5 h-3.5 text-slate-600 ${isResetting ? 'animate-spin text-primary' : ''}`} />
                <span className="hidden sm:inline">Reset Prototype</span>
              </button>
            )}
          </div>
        </div>

        {/* Sub-Header Row: Perspectives Navigation Bar */}
        <nav className="flex items-center gap-1 sm:gap-2 overflow-x-auto py-1.5 no-scrollbar">
          <button
            onClick={() => onViewChange('shopper')}
            className={`px-3 py-2 text-xs sm:text-sm font-semibold rounded-md transition-all flex items-center gap-2 whitespace-nowrap ${
              currentView === 'shopper'
                ? 'bg-blue-50/80 text-primary border-b-2 border-primary shadow-sm'
                : 'text-slate-600 hover:text-slate-900 hover:bg-slate-50'
            }`}
          >
            <ShoppingBag className="w-4 h-4" />
            <span>Shopper Discovery</span>
          </button>

          <button
            onClick={() => onViewChange('associate')}
            className={`px-3 py-2 text-xs sm:text-sm font-semibold rounded-md transition-all flex items-center gap-2 whitespace-nowrap ${
              currentView === 'associate'
                ? 'bg-blue-50/80 text-primary border-b-2 border-primary shadow-sm'
                : 'text-slate-600 hover:text-slate-900 hover:bg-slate-50'
            }`}
          >
            <PackageCheck className="w-4 h-4" />
            <span>Store Associate Operations</span>
          </button>

          <button
            onClick={() => onViewChange('business')}
            className={`px-3 py-2 text-xs sm:text-sm font-semibold rounded-md transition-all flex items-center gap-2 whitespace-nowrap ${
              currentView === 'business'
                ? 'bg-blue-50/80 text-primary border-b-2 border-primary shadow-sm'
                : 'text-slate-600 hover:text-slate-900 hover:bg-slate-50'
            }`}
          >
            <BarChart3 className="w-4 h-4" />
            <span>Business Intelligence & Replenishment</span>
          </button>

          <button
            onClick={() => onViewChange('trace')}
            className={`px-3 py-2 text-xs sm:text-sm font-semibold rounded-md transition-all flex items-center gap-2 whitespace-nowrap ${
              currentView === 'trace'
                ? 'bg-blue-50/80 text-primary border-b-2 border-primary shadow-sm'
                : 'text-slate-600 hover:text-slate-900 hover:bg-slate-50'
            }`}
          >
            <History className="w-4 h-4" />
            <span>Audit & Decision Trace</span>
          </button>
        </nav>
      </div>
    </header>
  );
};
