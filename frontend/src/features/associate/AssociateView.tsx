import React, { useState, useEffect } from 'react';
import { 
  Package, Truck, ArrowRight, CheckCircle2, 
  RefreshCw, Box, ClipboardCheck, ArrowUpRight, ArrowDownLeft 
} from 'lucide-react';
import { 
  api, Order, Transfer, PurchaseOrder, ProductStockSummary, StockChangeResult 
} from '../../api/client';
import { Button } from '../../components/ui/Button';
import { Badge } from '../../components/ui/Badge';
import { Card } from '../../components/ui/Card';
import { Modal } from '../../components/ui/Modal';

interface AssociateViewProps {
  selectedStore: string;
  onNavigateToBusiness: () => void;
}

export const AssociateView: React.FC<AssociateViewProps> = ({
  selectedStore,
  onNavigateToBusiness,
}) => {
  const [activeTab, setActiveTab] = useState<'orders' | 'transfers' | 'purchase_orders' | 'inventory'>('orders');
  const [orders, setOrders] = useState<Order[]>([]);
  const [transfers, setTransfers] = useState<Transfer[]>([]);
  const [purchaseOrders, setPurchaseOrders] = useState<PurchaseOrder[]>([]);
  const [stockSummary, setStockSummary] = useState<ProductStockSummary | null>(null);
  const [isLoading, setIsLoading] = useState(false);

  // Stock mutation feedback modal / toast
  const [mutationResult, setMutationResult] = useState<StockChangeResult | null>(null);
  const [actionTitle, setActionTitle] = useState('');

  // Load associate queues
  const refreshData = async () => {
    setIsLoading(true);
    try {
      const [oList, tList, poList, stock] = await Promise.all([
        api.getOrders(),
        api.getTransfers(),
        api.getPurchaseOrders(),
        api.getProductStock('RQ002'), // VoltGo Go
      ]);
      setOrders(oList);
      setTransfers(tList);
      setPurchaseOrders(poList);
      setStockSummary(stock);
    } catch (err) {
      console.error('Failed to load associate data:', err);
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    refreshData();
  }, [selectedStore]);

  // Fulfill pickup order
  const handleFulfillOrder = async (orderId: string) => {
    try {
      const res = await api.fulfillPickupOrder(orderId, 'Customer verified with photo ID');
      setActionTitle('Order Pickup Fulfilled');
      setMutationResult(res);
      refreshData();
    } catch (err: any) {
      alert(`Error fulfilling pickup: ${err.message}`);
    }
  };

  // Dispatch Transfer
  const handleDispatchTransfer = async (transferId: string) => {
    try {
      const res = await api.dispatchTransfer(transferId);
      setActionTitle('Transfer Dispatched from Source Store');
      setMutationResult(res);
      refreshData();
    } catch (err: any) {
      alert(`Error dispatching transfer: ${err.message}`);
    }
  };

  // Receive Transfer
  const handleReceiveTransfer = async (transferId: string) => {
    try {
      const res = await api.receiveTransfer(transferId);
      setActionTitle('Transfer Received at Destination Store');
      setMutationResult(res);
      refreshData();
    } catch (err: any) {
      alert(`Error receiving transfer: ${err.message}`);
    }
  };

  // Receive PO
  const handleReceivePO = async (poId: string) => {
    try {
      const res = await api.receivePurchaseOrder(poId);
      setActionTitle('Purchase Order Received at Dock');
      setMutationResult(res);
      refreshData();
    } catch (err: any) {
      alert(`Error receiving purchase order: ${err.message}`);
    }
  };

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 space-y-6">
      {/* Top Banner & Refresh */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 bg-surface p-5 rounded-card border border-border shadow-card">
        <div>
          <div className="flex items-center gap-2">
            <h1 className="text-xl font-bold text-text-primary">
              Store Associate & Stock Operations
            </h1>
            <Badge variant="cyan" size="sm">Active Store: {selectedStore}</Badge>
          </div>
          <p className="text-xs text-text-secondary mt-1">
            Fulfill in-store pickup reservations, manage transfer dispatches, and receive inbound supplier shipments.
          </p>
        </div>

        <div className="flex items-center gap-3">
          <Button
            variant="outline"
            size="sm"
            onClick={refreshData}
            isLoading={isLoading}
            className="flex items-center gap-1.5"
          >
            <RefreshCw className="w-3.5 h-3.5" />
            <span>Sync Live Stock</span>
          </Button>

          <Button
            size="sm"
            onClick={onNavigateToBusiness}
            className="flex items-center gap-1.5 bg-navy-800 hover:bg-navy-900"
          >
            <span>Manager Intelligence</span>
            <ArrowRight className="w-3.5 h-3.5" />
          </Button>
        </div>
      </div>

      {/* VoltGo Go Live Inventory Ledger */}
      {stockSummary && (
        <Card className="p-5">
          <div className="flex items-center justify-between mb-3 pb-2 border-b border-border">
            <div className="flex items-center gap-2">
              <Box className="w-4 h-4 text-primary" />
              <h2 className="font-semibold text-sm text-text-primary">
                Live Inventory Ledger: {stockSummary.product.name} ({stockSummary.product.sku})
              </h2>
            </div>
            <div className="text-xs text-text-secondary">
              Total Network ATP: <strong className="text-navy-800 font-mono text-sm">{stockSummary.atp_total}</strong> units
            </div>
          </div>

          <div className="overflow-x-auto">
            <table className="w-full text-xs text-left border-collapse">
              <thead>
                <tr className="bg-slate-50 border-b border-border text-text-secondary uppercase text-[10px] tracking-wider">
                  <th className="py-2.5 px-3">Location Code</th>
                  <th className="py-2.5 px-3">Store Name</th>
                  <th className="py-2.5 px-3">On Hand</th>
                  <th className="py-2.5 px-3">Active Holds</th>
                  <th className="py-2.5 px-3">Reserved Orders</th>
                  <th className="py-2.5 px-3">Outbound Transfer</th>
                  <th className="py-2.5 px-3">Inbound Transfer</th>
                  <th className="py-2.5 px-3 font-bold text-primary">Authoritative ATP</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-border font-mono">
                {stockSummary.locations.map((loc) => {
                  const isCurrent = loc.location_code === selectedStore;
                  return (
                    <tr key={loc.location_code} className={isCurrent ? 'bg-blue-50/40 font-semibold' : ''}>
                      <td className="py-2 px-3 text-text-primary font-bold">{loc.location_code}</td>
                      <td className="py-2 px-3 text-text-primary font-sans">{loc.location_name}</td>
                      <td className="py-2 px-3">{loc.on_hand}</td>
                      <td className="py-2 px-3 text-review">{loc.holds}</td>
                      <td className="py-2 px-3 text-review">{loc.reserved_orders}</td>
                      <td className="py-2 px-3 text-text-secondary">{loc.outbound_transfers}</td>
                      <td className="py-2 px-3 text-success">{loc.inbound_transfers}</td>
                      <td className="py-2 px-3 font-bold text-sm text-primary">{loc.atp}</td>
                    </tr>
                  );
                })}
              </tbody>
            </table>
          </div>
        </Card>
      )}

      {/* Navigation Tabs for Queues */}
      <div className="flex border-b border-border bg-surface px-4 rounded-t-card shadow-sm">
        <button
          onClick={() => setActiveTab('orders')}
          className={`py-3 px-4 text-xs font-semibold border-b-2 transition-all flex items-center gap-2 ${
            activeTab === 'orders'
              ? 'border-primary text-primary'
              : 'border-transparent text-text-secondary hover:text-text-primary'
          }`}
        >
          <ClipboardCheck className="w-4 h-4" />
          <span>Pickup Order Queue ({orders.filter((o) => o.status === 'CREATED' || o.status === 'CONFIRMED').length})</span>
        </button>

        <button
          onClick={() => setActiveTab('transfers')}
          className={`py-3 px-4 text-xs font-semibold border-b-2 transition-all flex items-center gap-2 ${
            activeTab === 'transfers'
              ? 'border-primary text-primary'
              : 'border-transparent text-text-secondary hover:text-text-primary'
          }`}
        >
          <Truck className="w-4 h-4" />
          <span>Inter-Store Transfers ({transfers.length})</span>
        </button>

        <button
          onClick={() => setActiveTab('purchase_orders')}
          className={`py-3 px-4 text-xs font-semibold border-b-2 transition-all flex items-center gap-2 ${
            activeTab === 'purchase_orders'
              ? 'border-primary text-primary'
              : 'border-transparent text-text-secondary hover:text-text-primary'
          }`}
        >
          <Package className="w-4 h-4" />
          <span>Supplier Purchase Orders ({purchaseOrders.length})</span>
        </button>
      </div>

      {/* Tab 1: Orders Queue */}
      {activeTab === 'orders' && (
        <Card className="p-5 rounded-t-none">
          <div className="flex items-center justify-between mb-4">
            <div>
              <h3 className="font-bold text-sm text-text-primary">Customer In-Store Pickup Reservations</h3>
              <p className="text-xs text-text-secondary">
                Orders with status CONFIRMED hold stock on shelf. Clicking "Fulfill Pickup" records physical customer handover and updates the stock ledger (On-hand 12 → 11).
              </p>
            </div>
          </div>

          {orders.length === 0 ? (
            <div className="text-center py-10 text-text-secondary text-xs">
              No orders found. Head to the Shopper view to reserve and place a customer pickup order!
            </div>
          ) : (
            <div className="space-y-3">
              {orders.map((order) => {
                const isPending = order.status === 'CREATED' || order.status === 'CONFIRMED';
                return (
                  <div
                    key={order.order_id}
                    className={`p-4 rounded-input border transition-all flex flex-col sm:flex-row sm:items-center justify-between gap-4 ${
                      isPending ? 'border-primary/40 bg-blue-50/20' : 'border-border bg-slate-50 opacity-80'
                    }`}
                  >
                    <div className="space-y-1">
                      <div className="flex items-center gap-2">
                        <span className="font-mono font-bold text-sm text-navy-800">
                          {order.order_code}
                        </span>
                        <Badge variant={isPending ? 'warning' : 'success'} size="sm">
                          {order.status === 'CREATED' ? 'Ready for Pickup' : 'Completed / Fulfilled'}
                        </Badge>
                      </div>
                      <div className="text-xs text-text-primary font-medium">
                        {order.product_name} (<span className="font-mono">{order.sku}</span>)
                      </div>
                      <div className="text-[11px] text-text-secondary flex items-center gap-4">
                        <span>Store: <strong>{order.location_code}</strong></span>
                        <span>Amount: <strong>₹{order.total_amount}</strong></span>
                        <span>Allocation: <strong className="font-mono">{(order.allocation_id || order.order_id || 'ALLOC-RES').slice(0, 8)}...</strong></span>
                      </div>
                    </div>

                    <div>
                      {isPending ? (
                        <Button
                          size="sm"
                          onClick={() => handleFulfillOrder(order.order_id)}
                          className="font-semibold text-xs whitespace-nowrap"
                        >
                          Fulfill Pickup Handover
                        </Button>
                      ) : (
                        <span className="text-xs text-success font-semibold flex items-center gap-1">
                          <CheckCircle2 className="w-4 h-4" /> Stock Ledger Decremented
                        </span>
                      )}
                    </div>
                  </div>
                );
              })}
            </div>
          )}
        </Card>
      )}

      {/* Tab 2: Transfers Queue */}
      {activeTab === 'transfers' && (
        <Card className="p-5 rounded-t-none">
          <div className="flex items-center justify-between mb-4">
            <div>
              <h3 className="font-bold text-sm text-text-primary">Inter-Store Stock Transfers</h3>
              <p className="text-xs text-text-secondary">
                Transfers conserve inventory across stores. Stock is decremented at the donor store upon dispatch, enters in-transit status, and is credited upon dock receipt.
              </p>
            </div>
          </div>

          {transfers.length === 0 ? (
            <div className="text-center py-10 text-text-secondary text-xs">
              No transfers active yet. Go to the Business Intelligence view to review and approve the recommended transfer!
            </div>
          ) : (
            <div className="space-y-3">
              {transfers.map((t) => {
                const isPendingDispatch = t.status === 'PENDING_DISPATCH';
                const isInTransit = t.status === 'IN_TRANSIT';
                const isReceived = t.status === 'RECEIVED';

                return (
                  <div
                    key={t.transfer_id}
                    className="p-4 rounded-input border border-border bg-surface shadow-sm space-y-3"
                  >
                    <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2">
                      <div className="flex items-center gap-2">
                        <span className="font-mono font-bold text-sm text-navy-800">{t.transfer_code}</span>
                        <Badge
                          variant={isReceived ? 'success' : isInTransit ? 'cyan' : 'warning'}
                          size="sm"
                        >
                          {t.status}
                        </Badge>
                      </div>
                      <div className="text-xs text-text-secondary">
                        ETA: <strong>{t.eta_hours} hours</strong>
                      </div>
                    </div>

                    <div className="grid grid-cols-1 sm:grid-cols-3 gap-3 text-xs bg-slate-50 p-3 rounded border border-slate-200">
                      <div>
                        <span className="text-text-secondary block text-[10px] uppercase font-semibold">SKU & Item</span>
                        <span className="font-medium text-text-primary">{t.product_name} ({t.sku})</span>
                      </div>
                      <div>
                        <span className="text-text-secondary block text-[10px] uppercase font-semibold">Route</span>
                        <span className="font-medium text-navy-800 flex items-center gap-1">
                          {t.origin_code} ({t.origin_name}) → {t.destination_code} ({t.destination_name})
                        </span>
                      </div>
                      <div>
                        <span className="text-text-secondary block text-[10px] uppercase font-semibold">Transfer Quantity</span>
                        <span className="font-mono font-bold text-sm text-primary">{t.quantity} units</span>
                      </div>
                    </div>

                    <div className="flex justify-end pt-2 border-t border-slate-100">
                      {isPendingDispatch && (
                        <Button
                          size="sm"
                          onClick={() => handleDispatchTransfer(t.transfer_id)}
                          className="text-xs font-semibold flex items-center gap-1.5"
                        >
                          <ArrowUpRight className="w-3.5 h-3.5" />
                          <span>Dispatch from {t.origin_code} ({t.quantity} units)</span>
                        </Button>
                      )}

                      {isInTransit && (
                        <Button
                          size="sm"
                          variant="success"
                          onClick={() => handleReceiveTransfer(t.transfer_id)}
                          className="text-xs font-semibold flex items-center gap-1.5"
                        >
                          <ArrowDownLeft className="w-3.5 h-3.5" />
                          <span>Receive at {t.destination_code} ({t.quantity} units)</span>
                        </Button>
                      )}

                      {isReceived && (
                        <span className="text-xs text-success font-semibold flex items-center gap-1">
                          <CheckCircle2 className="w-4 h-4" /> Received & Shelved into ATP
                        </span>
                      )}
                    </div>
                  </div>
                );
              })}
            </div>
          )}
        </Card>
      )}

      {/* Tab 3: Purchase Orders Queue */}
      {activeTab === 'purchase_orders' && (
        <Card className="p-5 rounded-t-none">
          <div className="flex items-center justify-between mb-4">
            <div>
              <h3 className="font-bold text-sm text-text-primary">Supplier Inbound Purchase Orders</h3>
              <p className="text-xs text-text-secondary">
                External supplier shipments from approved vendors. Receipt adds inventory to warehouse on-hand stock.
              </p>
            </div>
          </div>

          <div className="space-y-3">
            {purchaseOrders.map((po) => {
              const isPending = po.status === 'CREATED' || po.status === 'PLACED';
              return (
                <div
                  key={po.po_id}
                  className="p-4 rounded-input border border-border bg-surface shadow-sm flex flex-col sm:flex-row sm:items-center justify-between gap-4"
                >
                  <div className="space-y-1">
                    <div className="flex items-center gap-2">
                      <span className="font-mono font-bold text-sm text-navy-800">{po.po_code}</span>
                      <Badge variant={isPending ? 'warning' : 'success'} size="sm">
                        {po.status}
                      </Badge>
                    </div>
                    <div className="text-xs text-text-primary font-medium">
                      {po.product_name} ({po.sku}) — Supplier: <strong>{po.supplier_name}</strong>
                    </div>
                    <div className="text-[11px] text-text-secondary flex items-center gap-4">
                      <span>Dest: <strong>{po.location_code}</strong></span>
                      <span>Qty: <strong className="font-mono">{po.quantity}</strong> units</span>
                      <span>Cost: <strong>₹{po.total_cost}</strong></span>
                    </div>
                  </div>

                  <div>
                    {isPending ? (
                      <Button
                        size="sm"
                        onClick={() => handleReceivePO(po.po_id)}
                        className="text-xs font-semibold"
                      >
                        Receive PO at Dock
                      </Button>
                    ) : (
                      <span className="text-xs text-success font-semibold flex items-center gap-1">
                        <CheckCircle2 className="w-4 h-4" /> Goods Ingested
                      </span>
                    )}
                  </div>
                </div>
              );
            })}
          </div>
        </Card>
      )}

      {/* Stock Mutation Audit Feedback Modal */}
      {mutationResult && (
        <Modal
          isOpen={true}
          onClose={() => setMutationResult(null)}
          title={actionTitle}
          description="Authoritative database update confirmed with immutable audit trace"
          maxWidth="md"
        >
          <div className="space-y-4">
            <div className="bg-success-surface border border-success-border rounded-card p-4 text-center">
              <CheckCircle2 className="w-10 h-10 text-success mx-auto mb-2" />
              <div className="text-xs uppercase font-bold tracking-wider text-success mb-1">
                Database Status: {mutationResult.status}
              </div>
              <div className="font-mono text-xs text-navy-800">
                Movement ID: {mutationResult.movement_id}
              </div>
            </div>

            {/* Before / After stock comparison */}
            {mutationResult.stock_before && mutationResult.stock_after && (
              <div className="border border-border rounded-input p-3 bg-slate-50 text-xs space-y-2">
                <span className="font-semibold text-text-primary block">Store Stock Ledger Mutation:</span>
                <div className="grid grid-cols-2 gap-2 text-center">
                  <div className="bg-white p-2 rounded border border-border">
                    <span className="text-[10px] text-text-secondary uppercase block">Before Action</span>
                    <span className="font-mono font-bold text-sm text-text-primary">
                      {mutationResult.stock_before.on_hand} On-Hand
                    </span>
                  </div>
                  <div className="bg-blue-50 p-2 rounded border border-blue-200">
                    <span className="text-[10px] text-primary uppercase block">After Action</span>
                    <span className="font-mono font-bold text-sm text-primary">
                      {mutationResult.stock_after.on_hand} On-Hand
                    </span>
                  </div>
                </div>
              </div>
            )}

            <Button
              onClick={() => setMutationResult(null)}
              className="w-full text-xs"
            >
              Done & Return to Queues
            </Button>
          </div>
        </Modal>
      )}
    </div>
  );
};
