import React, { useState, useEffect } from 'react';
import { AppHeader } from './components/AppHeader';
import { DecisionExplainerModal } from './components/DecisionExplainerModal';
import { ShopperView } from './features/shopper/ShopperView';
import { AssociateView } from './features/associate/AssociateView';
import { BusinessManagerView } from './features/business/BusinessManagerView';
import { TraceView } from './features/trace/TraceView';
import { api } from './api/client';

export const App: React.FC = () => {
  const [currentView, setCurrentView] = useState<'shopper' | 'associate' | 'business' | 'trace'>('shopper');
  const [selectedStore, setSelectedStore] = useState<string>('S1');
  const [isBackendHealthy, setIsBackendHealthy] = useState<boolean>(false);
  const [isDecisionExplainerOpen, setIsDecisionExplainerOpen] = useState<boolean>(false);
  const [isResetting, setIsResetting] = useState<boolean>(false);
  const [resetKey, setResetKey] = useState<number>(0);
  const [isInitialized, setIsInitialized] = useState<boolean>(false);

  // Automatically restore pristine canonical prototype state on every refresh / page load
  useEffect(() => {
    let mounted = true;
    const initApp = async () => {
      try {
        await api.resetSession();
      } catch (err) {
        console.warn('Initial prototype session reset:', err);
      } finally {
        if (mounted) {
          setIsInitialized(true);
        }
      }

      try {
        const res = await api.getHealthReady();
        if (mounted && (res.status === 'ready' || res.status === 'ok')) {
          setIsBackendHealthy(true);
        }
      } catch {
        if (mounted) setIsBackendHealthy(false);
      }
    };

    initApp();

    const interval = setInterval(async () => {
      try {
        const res = await api.getHealthReady();
        if (mounted && (res.status === 'ready' || res.status === 'ok')) {
          setIsBackendHealthy(true);
        }
      } catch {
        if (mounted) setIsBackendHealthy(false);
      }
    }, 15000);

    return () => {
      mounted = false;
      clearInterval(interval);
    };
  }, []);

  const handleResetState = async () => {
    setIsResetting(true);
    try {
      await api.resetSession();
      setResetKey((k) => k + 1);
    } catch (err) {
      console.error('Failed to reset prototype baseline:', err);
    } finally {
      setIsResetting(false);
    }
  };

  return (
    <div className="min-h-screen flex flex-col bg-background text-text-primary">
      {/* Top Application Header */}
      <AppHeader
        currentView={currentView}
        onViewChange={setCurrentView}
        selectedStore={selectedStore}
        onStoreChange={setSelectedStore}
        isBackendHealthy={isBackendHealthy}
        onOpenDecisionExplainer={() => setIsDecisionExplainerOpen(true)}
        onResetState={handleResetState}
        isResetting={isResetting}
      />

      {/* Main Dynamic View */}
      <main className="flex-1 pb-16">
        {!isInitialized ? (
          <div className="max-w-7xl mx-auto px-4 py-16 flex flex-col items-center justify-center text-center">
            <div className="w-8 h-8 border-2 border-primary border-t-transparent rounded-full animate-spin mb-3" />
            <p className="text-sm font-medium text-text-secondary">Restoring pristine prototype state...</p>
          </div>
        ) : (
          <>
            {currentView === 'shopper' && (
              <ShopperView
                key={`shopper-${resetKey}`}
                selectedStore={selectedStore}
                onNavigateToAssociate={() => setCurrentView('associate')}
              />
            )}

            {currentView === 'associate' && (
              <AssociateView
                key={`associate-${resetKey}`}
                selectedStore={selectedStore}
                onNavigateToBusiness={() => setCurrentView('business')}
              />
            )}

            {currentView === 'business' && (
              <BusinessManagerView
                key={`business-${resetKey}`}
                onNavigateToAssociate={() => setCurrentView('associate')}
                onNavigateToTrace={() => setCurrentView('trace')}
              />
            )}

            {currentView === 'trace' && <TraceView key={`trace-${resetKey}`} />}
          </>
        )}
      </main>

      {/* Decision Engine Architecture Modal */}
      <DecisionExplainerModal
        isOpen={isDecisionExplainerOpen}
        onClose={() => setIsDecisionExplainerOpen(false)}
      />

      {/* Persistent Global Footer */}
      <footer className="bg-surface border-t border-border py-6 text-center text-xs text-text-secondary">
        <div className="max-w-7xl mx-auto px-4 flex flex-col sm:flex-row items-center justify-between gap-2">
          <span>
            RetailIQ — Prototype built for <strong>AI Builder Cup 2026</strong> (Retail & Commerce)
          </span>
          <div className="flex items-center gap-4">
            <button
              onClick={() => setIsDecisionExplainerOpen(true)}
              className="hover:text-primary transition-colors underline"
            >
              Decision Architecture
            </button>
            <span>·</span>
            <span>Deterministic ATP & Planning Ledger</span>
            <span>·</span>
            <span>Isolated Synthetic Enterprise Dataset</span>
          </div>
        </div>
      </footer>
    </div>
  );
};

export default App;
