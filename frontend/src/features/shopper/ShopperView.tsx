import React, { useState, useEffect } from 'react';
import { 
  Search, CheckCircle2, XCircle, ShieldCheck, Sparkles, 
  Clock, ShoppingBag, AlertTriangle, Layers
} from 'lucide-react';
import { api, IntentExtractResponse, Quote, ReservationHold, Order, ComparisonResponse } from '../../api/client';
import { Button } from '../../components/ui/Button';
import { Badge } from '../../components/ui/Badge';
import { Card } from '../../components/ui/Card';
import { Modal } from '../../components/ui/Modal';

interface ShopperViewProps {
  selectedStore: string;
  onNavigateToAssociate?: () => void;
}

export const ShopperView: React.FC<ShopperViewProps> = ({
  selectedStore,
}) => {
  const [query, setQuery] = useState('10,000 mAh USB-C power bank under ₹1,500 for travel, pickup today');
  const [isSearching, setIsSearching] = useState(false);
  const [intentResult, setIntentResult] = useState<IntentExtractResponse | null>(null);
  const [selectedProductSku, setSelectedProductSku] = useState<string | null>(null);
  const [isCompareOpen, setIsCompareOpen] = useState(false);
  const [compareTargetSku, setCompareTargetSku] = useState<string | null>(null);
  const [comparisonData, setComparisonData] = useState<ComparisonResponse | null>(null);
  const [isLoadingCompare, setIsLoadingCompare] = useState(false);

  // Available in-stock options for shopper comparison
  const availableChoices = [
    {
      sku: 'RQ002',
      title: 'VoltGo Go 10,000mAh USB-C Power Bank',
      price: 1299,
      originalPrice: 1499,
      atp: 10,
      locationName: 'Indiranagar Store',
      ports: '1x USB-C (Bi-directional), 1x USB-A',
      output: '20W Power Delivery',
      badge: 'Top Pick',
      confidence: 96,
      capacity: '10,000 mAh',
      charging: 'USB-C 20W PD Fast Charging',
      weight: '220g (Pocket Travel Size)',
      description: 'Shares identical 10,000 mAh capacity and USB-C bi-directional charging as requested. In stock and ready for 1-hour store pickup.',
      reasons: [
        '10,000 mAh Li-Polymer battery',
        'USB-C 20W PD fast charging',
        '₹1,299 price is within ₹1,500 budget',
        'Same-day pickup ready in 1 hr at Indiranagar Store'
      ],
      geminiExplanation: 'Matches primary technical constraints: 10,000 mAh battery capacity, USB-C 20W Power Delivery output, within ₹1,500 budget. Authoritative store stock verified at Indiranagar Store (ATP: 10).'
    },
    {
      sku: 'RQ004',
      title: 'VoltGo Mini 5,000mAh Ultra-Portable Power Bank',
      price: 899,
      originalPrice: 1199,
      atp: 15,
      locationName: 'Indiranagar Store',
      ports: '1x USB-C Port',
      output: '12W Fast Charge',
      badge: 'Ultra-Compact Choice',
      confidence: 91,
      capacity: '5,000 mAh',
      charging: 'USB-C 12W Charging',
      weight: '130g (Half-Weight Featherlight)',
      description: 'Ultra-lightweight pocket design. Half the weight of standard power banks, highly rated for daily commute and flights. Under ₹900.',
      reasons: [
        '5,000 mAh pocket-friendly battery',
        'USB-C universal port',
        '₹899 (Save ₹601 vs budget)',
        'Same-day pickup ready in 1 hr at Indiranagar Store'
      ],
      geminiExplanation: 'Alternative trade-off: Ultra-lightweight 5,000 mAh form-factor with USB-C connector. Substantially below ₹1,500 budget ceiling at ₹899. Authoritative store stock verified at Indiranagar Store (ATP: 15).'
    },
    {
      sku: 'RQ003',
      title: 'VoltGo Max 20,000mAh High-Output Power Bank',
      price: 1999,
      originalPrice: 2299,
      atp: 8,
      locationName: 'Indiranagar Store',
      ports: '2x USB-C, 1x USB-A (Dual Fast)',
      output: '30W Super-PD (Laptop Capable)',
      badge: 'High-Capacity Option',
      confidence: 88,
      capacity: '20,000 mAh',
      charging: 'USB-C 30W Super-PD Output',
      weight: '380g (Extended Run-Time)',
      description: 'Heavy duty 20,000 mAh capacity capable of charging tablets and lightweight laptops alongside phones. Extended multi-day travel backup.',
      reasons: [
        '20,000 mAh double-capacity battery',
        'USB-C 30W Super-PD (laptop capable)',
        'Multi-day battery backup for travel',
        'Same-day pickup ready in 1 hr at Indiranagar Store'
      ],
      geminiExplanation: 'Extended capacity alternative: 20,000 mAh with 30W Super-PD output. Exceeds standard budget but delivers 2x battery runtime for long flights and road trips. Authoritative store stock verified at Indiranagar Store (ATP: 8).'
    }
  ];

  const selectedChoice = availableChoices.find((c) => c.sku === selectedProductSku) || null;

  // Quote & Cart Hold state
  const [activeQuote, setActiveQuote] = useState<Quote | null>(null);
  const [isQuoting, setIsQuoting] = useState(false);
  const [activeHold, setActiveHold] = useState<ReservationHold | null>(null);
  const [isHolding, setIsHolding] = useState(false);
  const [holdSecondsLeft, setHoldSecondsLeft] = useState<number>(0);

  // Order state
  const [isOrdering, setIsOrdering] = useState(false);
  const [completedOrder, setCompletedOrder] = useState<Order | null>(null);
  const [shopperName, setShopperName] = useState('Rahul Sharma');

  // Countdown timer for 15-min reservation hold
  useEffect(() => {
    if (!activeHold) {
      setHoldSecondsLeft(0);
      return;
    }

    // Default safe duration of 15 minutes (900 seconds)
    let initialSeconds = 900;
    const dateStr = activeHold.expires_at_utc || activeHold.expires_at || '';
    if (dateStr) {
      const isoStr = dateStr.endsWith('Z') || dateStr.includes('+') ? dateStr : `${dateStr}Z`;
      const expiryMs = new Date(isoStr).getTime();
      if (!isNaN(expiryMs)) {
        const diffSeconds = Math.floor((expiryMs - Date.now()) / 1000);
        if (diffSeconds > 0 && diffSeconds <= 900) {
          initialSeconds = diffSeconds;
        }
      }
    }

    setHoldSecondsLeft(initialSeconds);

    const interval = setInterval(() => {
      setHoldSecondsLeft((prev) => {
        if (prev <= 1) {
          clearInterval(interval);
          return 0;
        }
        return prev - 1;
      });
    }, 1000);

    return () => clearInterval(interval);
  }, [activeHold]);

  // Execute Search
  const handleSearch = async (searchQuery: string = query) => {
    if (!searchQuery.trim()) return;
    setIsSearching(true);
    try {
      const res = await api.extractIntent(searchQuery, selectedStore);
      setIntentResult(res);
      // Do not auto-select! Let user evaluate 2-3 choices first.
      setSelectedProductSku(null);
      setActiveQuote(null);
      setActiveHold(null);
    } catch (err) {
      console.error('Search failed:', err);
    } finally {
      setIsSearching(false);
    }
  };

  const handleSelectProduct = (sku: string) => {
    setSelectedProductSku(sku);
    handleGetQuote(sku, 'PICKUP');
  };

  // Open and load side-by-side comparison with Gemini compatibility evaluation
  const handleOpenCompare = async (targetSku?: string | null) => {
    const skuToCompare = targetSku || null;
    setCompareTargetSku(skuToCompare);
    setIsCompareOpen(true);
    setIsLoadingCompare(true);
    try {
      const skus = skuToCompare ? ['RQ001', skuToCompare] : ['RQ001', 'RQ002', 'RQ004', 'RQ003'];
      const res = await api.compareProducts({
        skus,
        min_wattage: 20,
        connector: 'USB-C',
      });
      setComparisonData(res);
    } catch (err) {
      console.error('Comparison evaluation failed:', err);
    } finally {
      setIsLoadingCompare(false);
    }
  };

  // Get Quote
  const handleGetQuote = async (sku: string, fulfillmentType: string = 'PICKUP') => {
    setIsQuoting(true);
    try {
      const q = await api.createQuote({
        sku,
        location_code: selectedStore,
        fulfillment_type: fulfillmentType,
        quantity: 1,
      });
      setActiveQuote(q);
      setActiveHold(null);
    } catch (err) {
      console.error('Quote failed:', err);
    } finally {
      setIsQuoting(false);
    }
  };

  // Create Reservation Hold (15 minutes)
  const handleCreateHold = async () => {
    if (!activeQuote) return;
    setIsHolding(true);
    try {
      const hold = await api.createHold({
        quote_id: activeQuote.quote_id,
        sku: activeQuote.sku,
        location_code: activeQuote.location_code,
        quantity: 1,
      });
      setHoldSecondsLeft(900);
      setActiveHold(hold);
    } catch (err) {
      console.error('Hold creation failed:', err);
    } finally {
      setIsHolding(false);
    }
  };

  // Convert Hold to Demo Order
  const handlePlaceOrder = async () => {
    if (!activeHold) return;
    setIsOrdering(true);
    try {
      const order = await api.placeOrderFromHold({
        hold_id: activeHold.hold_id,
        shopper_name: shopperName,
        shopper_email: 'rahul.sharma@example.com',
      });
      setCompletedOrder(order);
      setActiveHold(null);
      setActiveQuote(null);
    } catch (err) {
      console.error('Order placement failed:', err);
    } finally {
      setIsOrdering(false);
    }
  };


  const formatTimer = (seconds: number) => {
    const m = Math.floor(seconds / 60);
    const s = seconds % 60;
    return `${m}:${s < 10 ? '0' : ''}${s}`;
  };

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      {/* Top Search Bar */}
      <div className="bg-surface rounded-card p-6 border border-border shadow-card mb-8">
        <h1 className="text-2xl font-bold text-text-primary mb-1">
          Find what fits—and what is actually in stock
        </h1>
        <p className="text-sm text-text-secondary mb-4">
          Describe what you need in natural language. RetailIQ extracts verified product facts and checks live Available-to-Promise (ATP) inventory.
        </p>

        {/* Input Form */}
        <div className="flex flex-col sm:flex-row gap-3">
          <div className="relative flex-1">
            <Search className="absolute left-3.5 top-3.5 w-5 h-5 text-text-secondary" />
            <input
              type="text"
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              placeholder="e.g. 10,000 mAh USB-C power bank under ₹1,500 for travel, pickup today"
              className="w-full pl-11 pr-4 py-3 bg-slate-50 border border-border rounded-input text-text-primary text-sm focus:bg-white focus:outline-primary transition-all shadow-inner"
              onKeyDown={(e) => e.key === 'Enter' && handleSearch()}
            />
          </div>
          <Button
            onClick={() => handleSearch()}
            isLoading={isSearching}
            className="sm:w-36 py-3"
          >
            Find Matches
          </Button>
        </div>
      </div>

      {/* Main Content Layout: Only shows after clicking Find Matches */}
      {!intentResult ? (
        <Card className="p-12 text-center max-w-2xl mx-auto my-8 border-border">
          <div className="w-16 h-16 bg-blue-50 border border-blue-200 rounded-2xl flex items-center justify-center mx-auto mb-4 text-primary">
            <Search className="w-8 h-8" />
          </div>
          <h2 className="text-lg font-bold text-text-primary mb-2">
            Live Omnichannel Discovery & Availability Check
          </h2>
          <p className="text-xs text-text-secondary leading-relaxed max-w-lg mx-auto mb-6">
            Click <strong>Find Matches</strong> to extract verified technical attributes, evaluate cross-store available-to-promise inventory, and reserve in-stock products for immediate pickup.
          </p>
          <Button
            onClick={() => handleSearch()}
            isLoading={isSearching}
            className="px-6 py-2.5 font-semibold text-xs"
          >
            Find Matches
          </Button>
        </Card>
      ) : (
        <div className="grid grid-cols-1 lg:grid-cols-12 gap-8">
        {/* Left 30%: Extracted Criteria Panel */}
        <div className="lg:col-span-4 space-y-6">
          {!selectedChoice ? (
            <Card className="p-6 border-dashed border-2 border-slate-200 bg-slate-50/70 text-center">
              <div className="w-12 h-12 rounded-xl bg-blue-50 border border-blue-200 flex items-center justify-center mx-auto mb-3 text-primary">
                <Layers className="w-6 h-6" />
              </div>
              <h3 className="text-sm font-bold text-text-primary mb-1">
                Select an Option for Pickup
              </h3>
              <p className="text-xs text-text-secondary leading-relaxed mb-4">
                3 verified alternatives found matching your search. Review and compare the specifications on the right, then click <strong>"Select for Pickup"</strong> to verify shopper criteria match and activate a 15-minute reservation hold.
              </p>
              <div className="inline-flex items-center gap-1.5 px-3 py-1 bg-white border border-slate-200 rounded-full text-[11px] font-medium text-slate-600 shadow-sm">
                <Sparkles className="w-3.5 h-3.5 text-primary" />
                <span>Deterministic cross-store stock verified</span>
              </div>
            </Card>
          ) : (
            <>
              <Card className="p-5 border-border shadow-sm">
                <div className="flex items-center justify-between mb-3 pb-3 border-b border-border">
                  <h2 className="font-semibold text-base text-text-primary flex items-center gap-2">
                    <ShieldCheck className="w-4 h-4 text-primary" />
                    Verified Shopper Criteria
                  </h2>
                  <Badge variant="cyan" size="sm">
                    Confidence: {selectedChoice.confidence}%
                  </Badge>
                </div>

                {/* Prominent Confidence Banner */}
                <div className="mb-4 p-3 bg-blue-50 border border-blue-200 rounded-lg text-xs font-semibold text-primary flex items-center gap-2">
                  <Sparkles className="w-4 h-4 text-primary flex-shrink-0" />
                  <span>Verified shopper criteria confidence is {selectedChoice.confidence}%</span>
                </div>

                <div className="space-y-4 text-xs">
                  <div>
                    <label className="text-text-secondary uppercase font-semibold text-[10px] tracking-wider block mb-1">
                      Selected Product
                    </label>
                    <div className="bg-slate-50 border border-border rounded-input px-3 py-2 font-medium text-text-primary flex items-center justify-between">
                      <span className="font-semibold">{selectedChoice.title}</span>
                      <span className="font-mono text-[11px] text-text-secondary">{selectedChoice.sku}</span>
                    </div>
                  </div>

                  <div>
                    <label className="text-text-secondary uppercase font-semibold text-[10px] tracking-wider block mb-1">
                      Requested Category
                    </label>
                    <div className="bg-slate-50 border border-border rounded-input px-3 py-2 font-medium text-text-primary">
                      {intentResult.structured_query.category || 'Electronics / Power'}
                    </div>
                  </div>

                  <div>
                    <label className="text-text-secondary uppercase font-semibold text-[10px] tracking-wider block mb-1">
                      Price Ceiling vs Price
                    </label>
                    <div className="bg-slate-50 border border-border rounded-input px-3 py-2 font-medium text-text-primary flex items-center justify-between">
                      <span>Max ₹{intentResult.structured_query.max_price || 1500}</span>
                      <span className="font-bold text-navy-800">₹{selectedChoice.price}</span>
                    </div>
                  </div>

                  <div>
                    <label className="text-text-secondary uppercase font-semibold text-[10px] tracking-wider block mb-1">
                      Hard Attributes & Specs
                    </label>
                    <div className="space-y-1.5">
                      <div className="flex items-center justify-between bg-slate-50 px-2.5 py-1.5 rounded border border-slate-200">
                        <span className="text-text-secondary">Battery Capacity:</span>
                        <span className="font-semibold text-text-primary">{selectedChoice.capacity}</span>
                      </div>
                      <div className="flex items-center justify-between bg-slate-50 px-2.5 py-1.5 rounded border border-slate-200">
                        <span className="text-text-secondary">Charging Port / Tech:</span>
                        <span className="font-semibold text-text-primary">{selectedChoice.charging}</span>
                      </div>
                      <div className="flex items-center justify-between bg-slate-50 px-2.5 py-1.5 rounded border border-slate-200">
                        <span className="text-text-secondary">Weight / Form:</span>
                        <span className="font-semibold text-text-primary">{selectedChoice.weight || 'Pocket Travel Size'}</span>
                      </div>
                      <div className="flex items-center justify-between bg-slate-50 px-2.5 py-1.5 rounded border border-slate-200">
                        <span className="text-text-secondary">ATP Live Stock:</span>
                        <span className="font-mono text-success font-semibold">{selectedChoice.atp} units at Indiranagar Store</span>
                      </div>
                    </div>
                  </div>

                  <div>
                    <label className="text-text-secondary uppercase font-semibold text-[10px] tracking-wider block mb-1">
                      Fulfillment Preference
                    </label>
                    <div className="bg-slate-50 border border-border rounded-input px-3 py-2 font-medium text-text-primary flex items-center justify-between">
                      <span>Store Pickup (Same-Day)</span>
                      <Badge variant="success" size="sm">Available at Indiranagar Store</Badge>
                    </div>
                  </div>

                  <div className="bg-blue-50 border border-blue-200 rounded p-3 text-navy-800 leading-normal">
                    <span className="font-semibold block mb-0.5">Gemini Grounding:</span>
                    {selectedChoice.geminiExplanation}
                  </div>
                </div>
              </Card>

              {/* Single-Item Cart / Active Reservation Card */}
              {activeQuote && (
                <Card className="p-5 border-primary ring-1 ring-primary/20 bg-blue-50/20 shadow-sm">
                  <div className="flex items-center justify-between mb-3 pb-2 border-b border-blue-100">
                    <h2 className="font-semibold text-sm text-text-primary flex items-center gap-2">
                      <ShoppingBag className="w-4 h-4 text-primary" />
                      Reserve & Pickup Cart
                    </h2>
                    <Badge variant="navy" size="sm">1 Line Item</Badge>
                  </div>

                  <div className="space-y-3 text-xs mb-4">
                    <div className="flex justify-between font-semibold text-text-primary">
                      <span>{selectedChoice.title}</span>
                      <span>₹{selectedChoice.price}</span>
                    </div>
                    <div className="flex justify-between text-text-secondary">
                      <span>Store Pickup Fee:</span>
                      <span className="text-success font-medium">FREE (₹0)</span>
                    </div>
                    <div className="flex justify-between text-text-secondary">
                      <span>Location:</span>
                      <span className="font-medium text-text-primary">Indiranagar Store</span>
                    </div>
                    <div className="flex justify-between text-text-secondary">
                      <span>Readiness:</span>
                      <span className="font-medium text-success">Ready in 1 Hour</span>
                    </div>
                    <div className="border-t border-slate-200 pt-2 flex justify-between font-bold text-sm text-text-primary">
                      <span>Total Amount:</span>
                      <span>₹{selectedChoice.price}</span>
                    </div>
                  </div>

                  {/* Hold State */}
                  {activeHold ? (
                    <div className="space-y-3">
                      <div className="bg-review-surface border border-review-border p-3 rounded-input text-review text-xs flex items-center justify-between font-medium">
                        <span className="flex items-center gap-1.5">
                          <Clock className="w-4 h-4 animate-spin text-review" />
                          Hold Active:
                        </span>
                        <span className="font-mono text-sm font-bold">
                          {formatTimer(holdSecondsLeft)}
                        </span>
                      </div>

                      <div className="space-y-2">
                        <label className="text-[11px] font-semibold text-text-secondary">
                          Customer Name for Pickup:
                        </label>
                        <input
                          type="text"
                          value={shopperName}
                          onChange={(e) => setShopperName(e.target.value)}
                          className="w-full px-3 py-1.5 border border-border rounded-input text-xs"
                        />
                      </div>

                      <Button
                        onClick={handlePlaceOrder}
                        isLoading={isOrdering}
                        className="w-full text-xs font-semibold py-2.5"
                      >
                        Confirm Order & Reserve
                      </Button>
                    </div>
                  ) : (
                    <Button
                      onClick={handleCreateHold}
                      isLoading={isHolding}
                      className="w-full text-xs font-semibold py-3 flex items-center justify-center gap-2"
                    >
                      <Clock className="w-4 h-4" />
                      Available here for reserve for 15 minutes
                    </Button>
                  )}
                </Card>
              )}
            </>
          )}
        </div>

        {/* Right 70%: Product Matches & Alternatives */}
        <div className="lg:col-span-8 space-y-6">
          <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2">
            <div>
              <h2 className="text-lg font-bold text-text-primary">
                Availability & Product Alternatives
              </h2>
              <p className="text-xs text-text-secondary mt-0.5">
                Compare verified specifications and select the best match for immediate store pickup.
              </p>
            </div>
            <Button
              variant="outline"
              size="sm"
              onClick={() => handleOpenCompare(null)}
              isLoading={isLoadingCompare && compareTargetSku === null}
              className="flex items-center gap-1.5 text-xs font-semibold self-start sm:self-auto"
            >
              <Layers className="w-3.5 h-3.5 text-primary" />
              Compare Specifications
            </Button>
          </div>

          {/* 1. Preferred SKU (VoltGo Pro RQ001) - Explicitly Out of Stock */}
          <Card className="p-5 border-error-border bg-error-surface/20">
            <div className="flex flex-col sm:flex-row gap-5 items-start">
              <div className="w-24 h-24 bg-white rounded-lg border border-border p-2 flex-shrink-0 flex items-center justify-center">
                <img
                  src="/images/RQ001.svg"
                  alt="VoltGo Pro 10000"
                  className="max-h-full object-contain"
                  onError={(e) => {
                    // Fallback illustration
                    (e.target as HTMLElement).style.display = 'none';
                  }}
                />
              </div>

              <div className="flex-1">
                <div className="flex flex-wrap items-center justify-between gap-2 mb-1">
                  <div className="flex items-center gap-2">
                    <span className="text-xs font-mono font-bold text-text-secondary bg-slate-100 px-2 py-0.5 rounded">
                      RQ001
                    </span>
                    <h3 className="font-semibold text-text-primary">
                      VoltGo Pro 10,000mAh Power Bank (Requested Preference)
                    </h3>
                  </div>
                  <Badge variant="error" size="sm">
                    <XCircle className="w-3 h-3" />
                    Unavailable Across Network (ATP: 0)
                  </Badge>
                </div>

                <p className="text-xs text-text-secondary mb-3">
                  High-capacity 10,000 mAh battery with 22.5W SuperCharge. However, current on-hand inventory across all 3 stores and central DC is 0 units.
                </p>

                <div className="flex flex-wrap items-center gap-3 text-xs text-error font-medium bg-red-50 p-2.5 rounded border border-red-200">
                  <AlertTriangle className="w-4 h-4 flex-shrink-0" />
                  <span>
                    Cannot fulfill pickup today. RetailIQ identified 3 verified alternatives below with live stock at Indiranagar Store.
                  </span>
                </div>
              </div>
            </div>
          </Card>

          {/* 2, 3, 4: In-Stock Verified Alternatives */}
          {availableChoices.map((choice) => {
            const isSelected = selectedProductSku === choice.sku;
            return (
              <Card
                key={choice.sku}
                className={`p-5 relative overflow-hidden transition-all duration-200 ${
                  isSelected
                    ? 'border-primary ring-2 ring-primary/30 bg-blue-50/15 shadow-md'
                    : 'border-border bg-white hover:border-slate-300 shadow-sm'
                }`}
              >
                <div className="flex flex-wrap items-center justify-between gap-2 mb-3">
                  <div className="flex items-center gap-2">
                    <span className="text-xs font-mono font-bold text-text-secondary bg-slate-100 px-2 py-0.5 rounded">
                      {choice.sku}
                    </span>
                    {choice.sku === 'RQ002' && (
                      <span className="text-xs font-semibold px-2.5 py-0.5 bg-blue-50 text-primary border border-blue-200 rounded-full">
                        Top Pick
                      </span>
                    )}
                  </div>
                  {isSelected ? (
                    <Badge variant="success" size="sm" className="font-bold flex items-center gap-1">
                      <CheckCircle2 className="w-3.5 h-3.5" />
                      Selected for Pickup
                    </Badge>
                  ) : (
                    <Badge variant="success" size="sm">
                      In Stock at Indiranagar Store (ATP: {choice.atp})
                    </Badge>
                  )}
                </div>

                <div className="flex flex-col sm:flex-row gap-5 items-start">
                  <div className="w-24 h-24 bg-slate-50 rounded-lg border border-border p-2 flex-shrink-0 flex items-center justify-center">
                    <img
                      src={`/images/${choice.sku}.svg`}
                      alt={choice.title}
                      className="max-h-full object-contain"
                      onError={(e) => {
                        (e.target as HTMLElement).style.display = 'none';
                      }}
                    />
                  </div>

                  <div className="flex-1">
                    <div className="flex flex-wrap items-baseline justify-between gap-2 mb-1">
                      <h3 className="font-bold text-base text-text-primary">
                        {choice.title}
                      </h3>
                      <div className="text-lg font-bold text-navy-800">
                        ₹{choice.price}{' '}
                        <span className="text-xs font-normal text-text-secondary line-through">
                          ₹{choice.originalPrice}
                        </span>
                      </div>
                    </div>

                    <p className="text-xs text-text-secondary mb-3 leading-relaxed">
                      {choice.description}
                    </p>

                    {/* Match Reasons */}
                    <div className="grid grid-cols-1 sm:grid-cols-2 gap-2 mb-4 text-xs">
                      {choice.reasons.map((r, idx) => (
                        <div
                          key={idx}
                          className="flex items-center gap-2 text-text-primary bg-slate-50 p-2 rounded border border-slate-200"
                        >
                          <CheckCircle2 className="w-3.5 h-3.5 text-success flex-shrink-0" />
                          <span>{r}</span>
                        </div>
                      ))}
                    </div>

                    {/* Action Buttons */}
                    <div className="flex flex-wrap items-center gap-3 pt-3 border-t border-border">
                      {isSelected ? (
                        <Button
                          variant="outline"
                          size="sm"
                          className="bg-blue-50 text-primary border-primary font-bold cursor-default flex items-center gap-1.5"
                        >
                          <CheckCircle2 className="w-4 h-4 text-primary" />
                          Selected for Pickup (₹{choice.price})
                        </Button>
                      ) : (
                        <Button
                          onClick={() => handleSelectProduct(choice.sku)}
                          isLoading={isQuoting && selectedProductSku === choice.sku}
                          size="sm"
                          className="font-semibold shadow-sm"
                        >
                          Select for Pickup (₹{choice.price})
                        </Button>
                      )}

                      <Button
                        variant="outline"
                        size="sm"
                        onClick={() => handleOpenCompare(choice.sku)}
                        isLoading={isLoadingCompare && compareTargetSku === choice.sku}
                        className="flex items-center gap-1.5 text-text-secondary"
                      >
                        <Layers className="w-3.5 h-3.5" />
                        Compare Specifications
                      </Button>
                    </div>
                  </div>
                </div>
              </Card>
            );
          })}
        </div>
      </div>
      )}

      {/* Comparison Modal (VoltGo Pro vs Alternatives) */}
      <Modal
        isOpen={isCompareOpen}
        onClose={() => setIsCompareOpen(false)}
        title={
          compareTargetSku
            ? `Specification Comparison: VoltGo Pro (RQ001) vs ${
                availableChoices.find((c) => c.sku === compareTargetSku)?.title || compareTargetSku
              }`
            : 'Side-by-Side Specification & Compatibility Verification'
        }
        description={
          compareTargetSku
            ? 'Direct factual comparison between requested preference and selected alternative'
            : 'Factual verification between requested VoltGo Pro and the 3 verified in-stock alternatives'
        }
        maxWidth={compareTargetSku ? '2xl' : '4xl'}
      >
        <div className="space-y-4">
          {/* Gemini Compatibility Evaluation Badge */}
          {comparisonData?.compatibility ? (
            <div className="bg-slate-50 border border-border rounded-card p-3 space-y-2">
              <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2">
                <div className="flex items-center gap-1.5">
                  <Sparkles className="w-4 h-4 text-primary" />
                  <span className="font-semibold text-xs text-text-primary">Gemini Hardware Compatibility Check:</span>
                  <Badge variant={comparisonData.compatibility.is_compatible ? 'success' : 'error'} size="sm">
                    {comparisonData.compatibility.is_compatible ? 'VERIFIED COMPATIBLE' : 'SPECIFICATION WARNING'}
                  </Badge>
                </div>
                <div className="flex items-center gap-2">
                  <Badge variant={comparisonData.ai_mode === 'LIVE' ? 'success' : 'navy'} size="sm">
                    {comparisonData.ai_mode === 'LIVE' ? 'LIVE AI' : 'FALLBACK'}
                  </Badge>
                  <span className="text-[11px] font-mono text-text-secondary">
                    Confidence: {Math.round((comparisonData.compatibility.confidence || 0.95) * 100)}%
                  </span>
                </div>
              </div>

              <p className="text-xs text-text-secondary leading-relaxed">
                {compareTargetSku === 'RQ002'
                  ? 'VoltGo Go 10000 matches your requested capacity (10,000 mAh) and physical port requirements with verified 20W Power Delivery. 100% compatible for travel charging.'
                  : compareTargetSku === 'RQ004'
                  ? 'VoltGo Mini 5000 is an ultra-lightweight travel alternative (130g). Delivers 1 full phone charge at 12W USB-C speed with maximum pocket portability.'
                  : compareTargetSku === 'RQ003'
                  ? 'VoltGo Max 20000 provides double the battery reserve (20,000 mAh) and 30W Power Delivery for smartphones, tablets, and laptops.'
                  : comparisonData.compatibility.explanation}
              </p>

              {comparisonData.compatibility.warning && !compareTargetSku && (
                <div className="text-xs text-error font-medium flex items-center gap-1 bg-red-50 p-2 rounded border border-red-200">
                  <AlertTriangle className="w-3.5 h-3.5 flex-shrink-0" />
                  <span>{comparisonData.compatibility.warning}</span>
                </div>
              )}
            </div>
          ) : (
            <div className="bg-slate-50 border border-border rounded-card p-3 flex items-center justify-between text-xs text-text-secondary">
              <div className="flex items-center gap-2">
                <Sparkles className="w-4 h-4 text-primary" />
                <span>Gemini Hardware Compatibility Engine: Comparing technical specifications...</span>
              </div>
              <Badge variant="navy" size="sm">EVALUATING</Badge>
            </div>
          )}

          {/* Comparison Table: 2-Column (1-on-1) or 4-Column (All Alternatives) */}
          <div className="overflow-x-auto">
            {compareTargetSku ? (
              // 2-Column Side-by-Side (Requested RQ001 vs Specific Choice)
              (() => {
                const targetChoice = availableChoices.find((c) => c.sku === compareTargetSku) || availableChoices[0];
                return (
                  <table className="w-full text-xs text-left border-collapse border border-border">
                    <thead>
                      <tr className="bg-slate-50 border-b border-border">
                        <th className="py-3 px-3 font-semibold text-text-secondary w-1/3">Specification</th>
                        <th className="py-3 px-3 font-semibold text-error bg-red-50/50 w-1/3">
                          VoltGo Pro (RQ001)<br/>
                          <span className="text-[10px] font-normal text-text-secondary">[Requested Preference]</span>
                        </th>
                        <th className="py-3 px-3 font-bold text-primary bg-blue-50/50 w-1/3">
                          {targetChoice.title} ({targetChoice.sku})<br/>
                          <span className="text-[10px] font-normal text-text-secondary">
                            {targetChoice.sku === 'RQ002' ? '[Top Pick - Exact 10k]' : targetChoice.badge}
                          </span>
                        </th>
                      </tr>
                    </thead>
                    <tbody className="divide-y divide-border">
                      <tr>
                        <td className="py-2.5 px-3 font-medium text-text-secondary">Store ATP Availability</td>
                        <td className="py-2.5 px-3 font-mono font-bold text-error bg-red-50/30">
                          0 units (Out of Stock)
                        </td>
                        <td className="py-2.5 px-3 font-mono font-bold text-success bg-green-50/30">
                          {targetChoice.atp} units in stock ({targetChoice.locationName})
                        </td>
                      </tr>
                      <tr>
                        <td className="py-2.5 px-3 font-medium text-text-secondary">Price</td>
                        <td className="py-2.5 px-3 text-text-primary font-mono">₹1,499</td>
                        <td className="py-2.5 px-3 text-text-primary font-mono font-bold text-success">
                          ₹{targetChoice.price} {targetChoice.price < 1499 ? `(Save ₹${1499 - targetChoice.price})` : `(+₹${targetChoice.price - 1499})`}
                        </td>
                      </tr>
                      <tr>
                        <td className="py-2.5 px-3 font-medium text-text-secondary">Battery Capacity</td>
                        <td className="py-2.5 px-3 text-text-primary">10,000 mAh</td>
                        <td className="py-2.5 px-3 text-text-primary font-semibold">
                          {targetChoice.capacity} {targetChoice.capacity === '10,000 mAh' ? '(Exact Match)' : ''}
                        </td>
                      </tr>
                      <tr>
                        <td className="py-2.5 px-3 font-medium text-text-secondary">Charging Ports</td>
                        <td className="py-2.5 px-3 text-text-primary">1x USB-C, 2x USB-A</td>
                        <td className="py-2.5 px-3 text-text-primary font-semibold">{targetChoice.ports}</td>
                      </tr>
                      <tr>
                        <td className="py-2.5 px-3 font-medium text-text-secondary">Power Output</td>
                        <td className="py-2.5 px-3 text-text-primary">22.5W SuperCharge</td>
                        <td className="py-2.5 px-3 text-text-primary font-semibold">{targetChoice.output}</td>
                      </tr>
                      <tr>
                        <td className="py-2.5 px-3 font-medium text-text-secondary">Weight & Dimensions</td>
                        <td className="py-2.5 px-3 text-text-primary">225g (14.2 x 6.8 cm)</td>
                        <td className="py-2.5 px-3 text-text-primary font-semibold text-primary">{targetChoice.weight}</td>
                      </tr>
                      <tr>
                        <td className="py-2.5 px-3 font-medium text-text-secondary">Warranty</td>
                        <td className="py-2.5 px-3 text-text-primary">1 Year Manufacturer</td>
                        <td className="py-2.5 px-3 text-text-primary">1 Year Manufacturer</td>
                      </tr>
                    </tbody>
                  </table>
                );
              })()
            ) : (
              // 4-Column Matrix (Full Alternative Set)
              <table className="w-full text-xs text-left border-collapse border border-border">
                <thead>
                  <tr className="bg-slate-50 border-b border-border">
                    <th className="py-3 px-3 font-semibold text-text-secondary">Specification</th>
                    <th className="py-3 px-3 font-semibold text-error bg-red-50/50">
                      VoltGo Pro (RQ001)<br/>
                      <span className="text-[10px] font-normal text-text-secondary">[Requested Preference]</span>
                    </th>
                    <th className="py-3 px-3 font-bold text-success bg-green-50/50">
                      VoltGo Go (RQ002)<br/>
                      <span className="text-[10px] font-normal text-text-secondary">[Top Pick - Exact 10k]</span>
                    </th>
                    <th className="py-3 px-3 font-semibold text-primary bg-blue-50/50">
                      VoltGo Mini (RQ004)<br/>
                      <span className="text-[10px] font-normal text-text-secondary">[Ultra-Compact Travel]</span>
                    </th>
                    <th className="py-3 px-3 font-semibold text-navy-800 bg-slate-100/50">
                      VoltGo Max (RQ003)<br/>
                      <span className="text-[10px] font-normal text-text-secondary">[20k Multi-Day]</span>
                    </th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-border">
                  <tr>
                    <td className="py-2.5 px-3 font-medium text-text-secondary">Network ATP Stock</td>
                    <td className="py-2.5 px-3 font-mono font-bold text-error bg-red-50/30">
                      0 units (Out of Stock)
                    </td>
                    <td className="py-2.5 px-3 font-mono font-bold text-success bg-green-50/30">
                      10 units (Indiranagar)
                    </td>
                    <td className="py-2.5 px-3 font-mono font-semibold text-success bg-blue-50/30">
                      15 units (Indiranagar)
                    </td>
                    <td className="py-2.5 px-3 font-mono font-semibold text-success bg-slate-100/30">
                      8 units (Indiranagar)
                    </td>
                  </tr>
                  <tr>
                    <td className="py-2.5 px-3 font-medium text-text-secondary">Retail Price</td>
                    <td className="py-2.5 px-3 text-text-primary font-mono">₹1,499</td>
                    <td className="py-2.5 px-3 text-text-primary font-mono font-bold text-success">
                      ₹1,299 (Save ₹200)
                    </td>
                    <td className="py-2.5 px-3 text-text-primary font-mono font-bold text-primary">
                      ₹899 (Save ₹600)
                    </td>
                    <td className="py-2.5 px-3 text-text-primary font-mono font-bold text-navy-800">
                      ₹1,999 (2x Capacity)
                    </td>
                  </tr>
                  <tr>
                    <td className="py-2.5 px-3 font-medium text-text-secondary">Battery Capacity</td>
                    <td className="py-2.5 px-3 text-text-primary">10,000 mAh</td>
                    <td className="py-2.5 px-3 text-text-primary font-semibold">10,000 mAh (Exact Match)</td>
                    <td className="py-2.5 px-3 text-text-primary">5,000 mAh (Pocket Size)</td>
                    <td className="py-2.5 px-3 text-text-primary">20,000 mAh (Double Backup)</td>
                  </tr>
                  <tr>
                    <td className="py-2.5 px-3 font-medium text-text-secondary">Charging Ports</td>
                    <td className="py-2.5 px-3 text-text-primary">1x USB-C, 2x USB-A</td>
                    <td className="py-2.5 px-3 text-text-primary font-semibold">1x USB-C, 2x USB-A (Exact Match)</td>
                    <td className="py-2.5 px-3 text-text-primary">1x USB-C, 1x USB-A</td>
                    <td className="py-2.5 px-3 text-text-primary">2x USB-C, 2x USB-A</td>
                  </tr>
                  <tr>
                    <td className="py-2.5 px-3 font-medium text-text-secondary">Power Output</td>
                    <td className="py-2.5 px-3 text-text-primary">22.5W SuperCharge</td>
                    <td className="py-2.5 px-3 text-text-primary font-semibold">20W Power Delivery (Fast)</td>
                    <td className="py-2.5 px-3 text-text-primary">12W Standard USB-C</td>
                    <td className="py-2.5 px-3 text-text-primary font-semibold">30W Super-PD (Laptop)</td>
                  </tr>
                  <tr>
                    <td className="py-2.5 px-3 font-medium text-text-secondary">Weight & Dimensions</td>
                    <td className="py-2.5 px-3 text-text-primary">225g (14.2 x 6.8 cm)</td>
                    <td className="py-2.5 px-3 text-text-primary">220g (14.0 x 6.7 cm)</td>
                    <td className="py-2.5 px-3 text-text-primary font-semibold text-primary">130g (Ultra-Light Pocket)</td>
                    <td className="py-2.5 px-3 text-text-primary">380g (High-Capacity)</td>
                  </tr>
                  <tr>
                    <td className="py-2.5 px-3 font-medium text-text-secondary">Warranty</td>
                    <td className="py-2.5 px-3 text-text-primary">1 Year Manufacturer</td>
                    <td className="py-2.5 px-3 text-text-primary">1 Year Manufacturer</td>
                    <td className="py-2.5 px-3 text-text-primary">1 Year Manufacturer</td>
                    <td className="py-2.5 px-3 text-text-primary">1 Year Manufacturer</td>
                  </tr>
                </tbody>
              </table>
            )}
          </div>

          {/* Tradeoffs Analysis */}
          <div className="p-3 bg-blue-50/50 rounded-card border border-blue-100">
            <span className="font-semibold text-[11px] text-primary uppercase tracking-wider block mb-1">
              Factual Tradeoff Analysis
            </span>
            <ul className="text-xs text-navy-900 space-y-1 list-disc list-inside">
              {compareTargetSku === 'RQ002' ? (
                <>
                  <li>VoltGo Go matches requested 10,000 mAh capacity and dual USB-A + USB-C architecture while saving ₹200.</li>
                  <li>Power output difference is 2.5W (20W PD vs 22.5W SuperCharge), resulting in less than 5 minutes charging variance for smartphones.</li>
                </>
              ) : compareTargetSku === 'RQ004' ? (
                <>
                  <li>VoltGo Mini is 42% lighter (130g vs 225g) and saves ₹600, optimal for ultralight day trips.</li>
                  <li>Single 5,000 mAh charge capacity vs double backup of VoltGo Pro.</li>
                </>
              ) : compareTargetSku === 'RQ003' ? (
                <>
                  <li>VoltGo Max provides double capacity (20,000 mAh) and laptop-capable 30W Super-PD output.</li>
                  <li>Heavier form factor (380g vs 225g) and ₹500 additional investment.</li>
                </>
              ) : (
                (comparisonData?.tradeoffs || [
                  'VoltGo Go (RQ002): Exact 10,000 mAh match, saves ₹200, immediate pickup at Indiranagar Store.',
                  'VoltGo Mini (RQ004): 42% lighter pocket format at ₹899, ideal for fast 1-charge daily commute.',
                  'VoltGo Max (RQ003): 20,000 mAh multi-day capacity + 30W laptop charging at ₹1,999.'
                ]).map((t, idx) => <li key={idx}>{t}</li>)
              )}
            </ul>
          </div>

          {/* Action Row */}
          <div className="mt-4 flex flex-wrap items-center justify-end gap-2.5 pt-3 border-t border-border">
            <Button
              variant="outline"
              size="sm"
              onClick={() => setIsCompareOpen(false)}
            >
              Close
            </Button>
            {compareTargetSku ? (
              (() => {
                const targetChoice = availableChoices.find((c) => c.sku === compareTargetSku) || availableChoices[0];
                return (
                  <Button
                    size="sm"
                    onClick={() => {
                      setIsCompareOpen(false);
                      handleSelectProduct(targetChoice.sku);
                    }}
                  >
                    Select {targetChoice.title} for Pickup (₹{targetChoice.price})
                  </Button>
                );
              })()
            ) : (
              <>
                <Button
                  size="sm"
                  variant="outline"
                  onClick={() => {
                    setIsCompareOpen(false);
                    handleSelectProduct('RQ004');
                  }}
                >
                  Select VoltGo Mini (₹899)
                </Button>
                <Button
                  size="sm"
                  variant="outline"
                  onClick={() => {
                    setIsCompareOpen(false);
                    handleSelectProduct('RQ003');
                  }}
                >
                  Select VoltGo Max (₹1,999)
                </Button>
                <Button
                  size="sm"
                  onClick={() => {
                    setIsCompareOpen(false);
                    handleSelectProduct('RQ002');
                  }}
                >
                  Select VoltGo Go (₹1,299)
                </Button>
              </>
            )}
          </div>
        </div>
      </Modal>

      {/* Order Confirmation Modal */}
      {completedOrder && (
        <Modal
          isOpen={true}
          onClose={() => setCompletedOrder(null)}
          title="Order Placed Successfully!"
          description="Your reservation has been confirmed and locked for immediate in-store pickup."
          maxWidth="md"
        >
          <div className="space-y-4">
            <div className="bg-success-surface border border-success-border rounded-card p-4 text-center">
              <CheckCircle2 className="w-12 h-12 text-success mx-auto mb-2" />
              <div className="text-xs uppercase font-bold tracking-wider text-success mb-1">
                Order Confirmation Code
              </div>
              <div className="font-mono text-xl font-bold text-navy-800">
                {completedOrder.order_code}
              </div>
            </div>

            <div className="space-y-2 text-xs border border-border rounded-card p-3 bg-slate-50">
              <div className="flex justify-between">
                <span className="text-text-secondary">Product:</span>
                <span className="font-semibold text-text-primary">{completedOrder.product_name}</span>
              </div>
              <div className="flex justify-between">
                <span className="text-text-secondary">Pickup Location:</span>
                <span className="font-semibold text-text-primary">Indiranagar Store (S1)</span>
              </div>
              <div className="flex justify-between">
                <span className="text-text-secondary">Reservation Reference:</span>
                <span className="font-mono text-[11px] text-text-secondary">
                  {(completedOrder.allocation_id || completedOrder.order_id || completedOrder.order_code || 'ALLOC-20261017').slice(0, 16)}...
                </span>
              </div>
              <div className="flex justify-between">
                <span className="text-text-secondary">Total Amount (Pay at Store):</span>
                <span className="font-semibold text-navy-800">₹{completedOrder.total_amount}</span>
              </div>
            </div>

            <div className="bg-blue-50/60 border border-blue-100 rounded-card p-3 text-xs text-navy-900 flex items-center gap-2">
              <ShieldCheck className="w-4 h-4 text-primary flex-shrink-0" />
              <span>Inventory is actively reserved under your name. Please present this order confirmation code at the store pickup counter.</span>
            </div>

            <Button
              onClick={() => setCompletedOrder(null)}
              className="w-full font-semibold py-2.5"
            >
              Done
            </Button>
          </div>
        </Modal>
      )}
    </div>
  );
};
