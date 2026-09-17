/**
 * Cars Empire - Professional PWA Single-Page Application Engine
 * Native-grade UI architecture, View Transitions, Offline Local-First caching,
 * and live Django REST API integration.
 */

// 1. Dynamic API Base URL Configuration
const API_BASE_URL = (typeof window !== 'undefined' && window.location && window.location.origin.startsWith('http'))
  ? window.location.origin + '/api'
  : 'https://carsempire.net/api';

// 2. View Order Map for Native Directional Slide
const VIEW_INDEX = {
  home: 0,
  offers: 1,
  garage: 2,
  coupons: 3,
  account: 4
};

// 3. Application State (Hydrated from LocalStorage first)
const state = {
  currentView: 'home',
  currentCategory: 'all',
  searchQuery: '',
  location: 'New Cairo',
  activeVehicle: {
    id: 1,
    make: 'Ford',
    model: 'Mustang GT',
    specs: '5.0L Coyote V8 • Fastback 2023',
    plate: 'س ق ص 482',
    odometer: 42850
  },
  vehicles: [
    {
      id: 1,
      make: 'Ford',
      model: 'Mustang GT',
      specs: '5.0L Coyote V8 • Fastback 2023',
      plate: 'س ق ص 482',
      odometer: 42850,
      status: 'Up to Date'
    },
    {
      id: 2,
      make: 'BMW',
      model: '330i M-Sport',
      specs: '2.0L Turbo B48 • Sedan 2022',
      plate: 'ط د ر 914',
      odometer: 31200,
      status: 'Brake Service Due'
    }
  ],
  deals: [
    {
      id: 101,
      title: 'Mobil 1 Full Synthetic Oil Change + 20-Point Track Inspection',
      merchant_name: 'Mobil 1 Center - Tagamoa',
      original_price: 1800,
      discount_price: 1150,
      discount_percentage: 35,
      category_slug: 'oil',
      rating: 4.8,
      reviews_count: 142,
      image_url: 'https://images.unsplash.com/photo-1487754180451-c456f719a1fc?auto=format&fit=crop&w=600&q=80',
      badge: 'POPULAR'
    },
    {
      id: 102,
      title: 'Diamond 3-Layer Ceramic Coating & Interior Steam Deep Clean',
      merchant_name: 'Empire Auto Spa - Sheikh Zayed',
      original_price: 7000,
      discount_price: 3499,
      discount_percentage: 50,
      category_slug: 'detailing',
      rating: 4.9,
      reviews_count: 89,
      image_url: 'https://images.unsplash.com/photo-1607860108855-64acf2078ed9?auto=format&fit=crop&w=600&q=80',
      badge: '50% OFF'
    },
    {
      id: 103,
      title: 'Michelin / Pirelli Laser Balancing & 4-Tyre Nitrogen Fill',
      merchant_name: 'PitStop Performance Hub - Maadi',
      original_price: 700,
      discount_price: 420,
      discount_percentage: 40,
      category_slug: 'tyres',
      rating: 4.7,
      reviews_count: 65,
      image_url: 'https://images.unsplash.com/photo-1578844251758-2f71da64c96f?auto=format&fit=crop&w=600&q=80',
      badge: 'QUICK'
    },
    {
      id: 104,
      title: 'Custom ECU Stage 1 Dyno Tune + Baseline Graphs',
      merchant_name: 'Apex Dyno Tuning Lab - Nasr City',
      original_price: 4500,
      discount_price: 3200,
      discount_percentage: 29,
      category_slug: 'tuning',
      rating: 5.0,
      reviews_count: 112,
      image_url: 'https://images.unsplash.com/photo-1617814076367-b759c7d7e738?auto=format&fit=crop&w=600&q=80',
      badge: '+45 HP'
    },
    {
      id: 105,
      title: 'Brembo Track Day Brake Pads Installation & DOT 5.1 Flush',
      merchant_name: 'PitStop Performance Hub - Maadi',
      original_price: 2400,
      discount_price: 1650,
      discount_percentage: 31,
      category_slug: 'brakes',
      rating: 4.8,
      reviews_count: 53,
      image_url: 'https://images.unsplash.com/photo-1605559424843-9e4c228bf1c2?auto=format&fit=crop&w=600&q=80',
      badge: 'TRACK SAFE'
    },
    {
      id: 106,
      title: 'Computerized OBD-II Pre-Purchase 120-Point Inspection',
      merchant_name: 'Cars Empire Certified Center - Tagamoa',
      original_price: 1200,
      discount_price: 750,
      discount_percentage: 38,
      category_slug: 'diagnostics',
      rating: 4.9,
      reviews_count: 210,
      image_url: 'https://images.unsplash.com/photo-1568605117036-5fe5e7bab0b7?auto=format&fit=crop&w=600&q=80',
      badge: 'CERTIFIED'
    }
  ],
  coupons: [
    {
      orderNum: '18459201',
      merchant: 'Empire Auto Spa',
      dealTitle: 'Exterior Polish + Nanotech Glass Rain Repellent',
      amount: 450,
      backupCode: 'CEP-8459-201-VIP',
      pin: '7824',
      validUntil: '2025-08-31',
      status: 'Paid',
      imageUrl: 'https://images.unsplash.com/photo-1607860108855-64acf2078ed9?auto=format&fit=crop&w=200&q=80'
    },
    {
      orderNum: '18421094',
      merchant: 'Castrol Service Lab',
      dealTitle: 'Castrol Edge 10,000 KM + OEM Filter Replacement',
      amount: 1350,
      backupCode: 'CEP-4210-094-VIP',
      pin: '4912',
      validUntil: '2025-07-15',
      status: 'Paid',
      imageUrl: 'https://images.unsplash.com/photo-1625047509168-a7026f36de04?auto=format&fit=crop&w=300&q=80'
    }
  ]
};

// 4. Haptic Feedback Utility (Progressive Enhancement)
function haptic(duration = 15) {
  if (typeof navigator !== 'undefined' && 'vibrate' in navigator) {
    try {
      navigator.vibrate(duration);
    } catch (e) {
      // Ignored if user hasn't interacted or unsupported
    }
  }
}

// 5. Toast Notification HUD
function triggerToast(message) {
  haptic(10);
  const toast = document.getElementById('toastNotification');
  const toastText = document.getElementById('toastText');
  if (!toast || !toastText) return;

  toastText.textContent = message;
  toast.classList.remove('opacity-0', 'pointer-events-none');
  toast.classList.add('opacity-100');

  clearTimeout(window.__toastTimeout);
  window.__toastTimeout = setTimeout(() => {
    toast.classList.remove('opacity-100');
    toast.classList.add('opacity-0', 'pointer-events-none');
  }, 2600);
}

// 6. Native View Transitions Router
function switchView(targetView) {
  if (state.currentView === targetView) return;

  haptic(15);
  const oldIndex = VIEW_INDEX[state.currentView] ?? 0;
  const newIndex = VIEW_INDEX[targetView] ?? 0;
  const direction = newIndex >= oldIndex ? 'forward' : 'backward';

  const updateDOM = () => {
    // Hide all view panels
    document.querySelectorAll('.view-panel').forEach(panel => {
      panel.classList.add('hidden');
    });

    // Show target view panel
    const targetPanel = document.getElementById(`view-${targetView}`);
    if (targetPanel) {
      targetPanel.classList.remove('hidden');
    }

    // Update bottom nav tab state
    document.querySelectorAll('.nav-tab').forEach(tab => {
      if (tab.getAttribute('data-view') === targetView) {
        tab.classList.add('tab-active');
        tab.classList.remove('text-on-surface-variant');
      } else {
        tab.classList.remove('tab-active');
        tab.classList.add('text-on-surface-variant');
      }
    });

    state.currentView = targetView;

    // Scroll back to top
    const scrollContainer = document.getElementById('app-scroll-container');
    if (scrollContainer) {
      scrollContainer.scrollTop = 0;
    }

    // Update URL hash / query without reloading
    if (history.pushState) {
      history.pushState({ view: targetView }, '', `/app/?tab=${targetView}`);
    }
  };

  // Check for View Transitions API
  if (document.startViewTransition) {
    document.documentElement.dataset.direction = direction;
    const transition = document.startViewTransition(() => {
      updateDOM();
    });
    transition.finished.finally(() => {
      delete document.documentElement.dataset.direction;
    });
  } else {
    updateDOM();
  }
}

// 7. Filter Categories
function filterCategory(catSlug) {
  haptic(12);
  state.currentCategory = catSlug;
  switchView('offers');

  // Update chip active classes
  document.querySelectorAll('#offersFilterChips .filter-chip').forEach(chip => {
    if (chip.getAttribute('data-category') === catSlug) {
      chip.classList.add('active', 'bg-primary-container', 'text-white');
      chip.classList.remove('bg-carbon-surface', 'text-on-surface-variant');
    } else {
      chip.classList.remove('active', 'bg-primary-container', 'text-white');
      chip.classList.add('bg-carbon-surface', 'text-on-surface-variant');
    }
  });

  renderDeals();
}

// 7.5 Category Fallback Image Resolver
function getCategoryFallbackImage(categorySlug, title = '') {
  const t = (String(title || '') + ' ' + String(categorySlug || '')).toLowerCase();
  if (t.includes('brake') || t.includes('pad') || t.includes('rotor')) {
    return 'https://images.unsplash.com/photo-1613214149922-f1809c99b414?auto=format&fit=crop&w=600&q=80';
  }
  if (t.includes('tyre') || t.includes('tire') || t.includes('wheel') || t.includes('align')) {
    return 'https://images.unsplash.com/photo-1578844251758-2f71da64c96f?auto=format&fit=crop&w=600&q=80';
  }
  if (t.includes('ceramic') || t.includes('detail') || t.includes('wash') || t.includes('polish') || t.includes('spa')) {
    return 'https://images.unsplash.com/photo-1607860108855-64acf2078ed9?auto=format&fit=crop&w=600&q=80';
  }
  if (t.includes('dyno') || t.includes('ecu') || t.includes('tune') || t.includes('stage') || t.includes('speed')) {
    return 'https://images.unsplash.com/photo-1617814076367-b759c7d7e738?auto=format&fit=crop&w=600&q=80';
  }
  if (t.includes('track') || t.includes('sport') || t.includes('prep')) {
    return 'https://images.unsplash.com/photo-1568605117036-5fe5e7bab0b7?auto=format&fit=crop&w=600&q=80';
  }
  if (t.includes('oil') || t.includes('lube') || t.includes('filter')) {
    return 'https://images.unsplash.com/photo-1487754180451-c456f719a1fc?auto=format&fit=crop&w=600&q=80';
  }
  return 'https://images.unsplash.com/photo-1625047509168-a7026f36de04?auto=format&fit=crop&w=600&q=80';
}

// 8. Render Deals in Offers View
function renderDeals() {
  const container = document.getElementById('dynamicDealsContainer');
  const countLabel = document.getElementById('dealsCountLabel');
  if (!container) return;

  const filtered = state.deals.filter(deal => {
    const matchCat = state.currentCategory === 'all' || deal.category_slug === state.currentCategory;
    const matchSearch = !state.searchQuery ||
      deal.title.toLowerCase().includes(state.searchQuery.toLowerCase()) ||
      deal.merchant_name.toLowerCase().includes(state.searchQuery.toLowerCase());
    return matchCat && matchSearch;
  });

  if (countLabel) {
    countLabel.textContent = `${filtered.length} AVAILABLE`;
  }

  if (filtered.length === 0) {
    container.innerHTML = `
      <div class="p-8 text-center bg-carbon-surface rounded-2xl border border-carbon-border">
        <span class="material-symbols-outlined text-4xl text-outline mb-2">search_off</span>
        <h4 class="font-chivo text-sm font-bold text-white">No deals found</h4>
        <p class="text-xs text-on-surface-variant mt-1">Try searching for other keywords or select 'All Deals'</p>
        <button class="mt-3 px-3 py-1.5 bg-primary-container text-white font-chivo text-xs rounded-xl font-bold" onclick="filterCategory('all')">
          Reset Filter
        </button>
      </div>
    `;
    return;
  }

  container.innerHTML = filtered.map(deal => `
    <article class="bg-carbon-surface border border-carbon-border rounded-2xl overflow-hidden shadow-lg flex flex-col group">
      <div class="relative w-full h-36 bg-surface-container-high overflow-hidden">
        <img class="w-full h-full object-cover group-hover:scale-105 transition-transform duration-500" src="${deal.image_url}" alt="${deal.title}" onerror="this.onerror=null; this.src='https://images.unsplash.com/photo-1625047509168-a7026f36de04?auto=format&fit=crop&w=600&q=80';"/>
        <div class="absolute top-0 left-3 px-2 py-1 bg-telemetry-yellow text-on-secondary font-chivo font-black text-[11px] rounded-b shadow-md flex flex-col items-center">
          <span>${deal.discount_percentage}%</span>
          <span class="text-[8px] leading-none">OFF</span>
        </div>
        ${deal.badge ? `
          <div class="absolute top-2 right-2 px-2 py-0.5 rounded bg-black/70 backdrop-blur-sm text-telemetry-yellow font-chivo font-black text-[10px] uppercase border border-telemetry-yellow/40">
            ${deal.badge}
          </div>
        ` : ''}
        <div class="absolute bottom-2 right-2 px-2 py-0.5 rounded-full bg-black/75 backdrop-blur-sm flex items-center gap-1 text-xs">
          <span class="material-symbols-outlined text-telemetry-yellow text-[14px]">star</span>
          <span class="font-bold text-white">${deal.rating || 4.8}</span>
          <span class="text-[10px] text-outline">(${deal.reviews_count || 50})</span>
        </div>
      </div>
      <div class="p-3.5 flex flex-col gap-2">
        <div>
          <span class="text-[11px] text-primary font-bold uppercase tracking-wider block">${deal.merchant_name}</span>
          <h4 class="font-chivo text-sm font-bold text-white mt-0.5 line-clamp-2">${deal.title}</h4>
        </div>
        <div class="flex items-end justify-between bg-surface-container-low rounded-xl p-2.5 border border-carbon-border/50 mt-1">
          <div class="flex flex-col">
            <span class="text-[11px] text-outline line-through">${deal.original_price} EGP</span>
            <div class="flex items-baseline gap-1">
              <span class="font-chivo text-base font-black text-telemetry-yellow">${deal.discount_price}</span>
              <span class="text-[10px] text-on-surface-variant font-bold">EGP</span>
            </div>
          </div>
          <button class="px-3.5 py-1.5 rounded-xl bg-primary-container text-white font-chivo font-black text-xs uppercase tracking-wider hover:bg-blue-600 active:scale-95 transition-all shadow" onclick="claimDeal('${deal.title.replace(/'/g, "\\'")}', ${deal.discount_price}, ${deal.original_price}, '${deal.merchant_name.replace(/'/g, "\\'")}')">
            CLAIM
          </button>
        </div>
      </div>
    </article>
  `).join('');
}

// 9. Claim Deal -> Add to Coupons Vault
function claimDeal(title, price, origPrice, merchant = 'Cars Empire Partner') {
  haptic(25);
  const newOrderNum = String(Math.floor(10000000 + Math.random() * 90000000));
  const newBackupCode = `CEP-${newOrderNum.slice(0, 4)}-${newOrderNum.slice(4, 7)}-VIP`;
  const newPin = String(Math.floor(1000 + Math.random() * 9000));

  const newCoupon = {
    orderNum: newOrderNum,
    merchant: merchant,
    dealTitle: title,
    amount: price,
    backupCode: newBackupCode,
    pin: newPin,
    validUntil: '2025-09-30',
    status: 'Paid',
    imageUrl: getCategoryFallbackImage('', title)
  };

  state.coupons.unshift(newCoupon);
  saveState();
  updateCouponsUI();

  triggerToast(`Unlocked: ${title} saved to voucher vault!`);
}

// 10. Update Coupons List UI
function updateCouponsUI() {
  const container = document.getElementById('couponsListContainer');
  const countBadge = document.getElementById('activeCouponsBadge');
  const countSpan = document.getElementById('countActiveCoupons');
  const cartBadge = document.getElementById('cartCountBadge');

  if (countBadge) countBadge.textContent = `${state.coupons.length} Live Vouchers`;
  if (countSpan) countSpan.textContent = String(state.coupons.length);
  if (cartBadge) cartBadge.textContent = String(state.coupons.length);

  if (!container) return;

  container.innerHTML = state.coupons.map((coupon) => `
    <div class="bg-carbon-surface border border-carbon-border rounded-2xl overflow-hidden shadow-xl flex flex-col">
      <div class="p-3.5 bg-surface-container-low/60 flex flex-col gap-2">
        <div class="grid grid-cols-2 gap-y-1.5 text-xs">
          <div class="flex justify-between pr-2">
            <span class="text-outline uppercase text-[10px]">Order Num</span>
            <span class="font-chivo font-bold text-white">#${coupon.orderNum}</span>
          </div>
          <div class="flex justify-between pl-2">
            <span class="text-outline uppercase text-[10px]">Date</span>
            <span class="font-medium text-white">Today</span>
          </div>
          <div class="flex justify-between pr-2">
            <span class="text-outline uppercase text-[10px]">Payment</span>
            <span class="font-medium text-white">Cars Wallet</span>
          </div>
          <div class="flex justify-between pl-2">
            <span class="text-outline uppercase text-[10px]">Status</span>
            <span class="text-tach-green font-bold flex items-center gap-0.5">
              <span class="material-symbols-outlined text-[12px]">check_circle</span> ${coupon.status}
            </span>
          </div>
        </div>
      </div>

      <div class="p-3.5 bg-surface-container-lowest flex flex-col gap-3">
        <div class="bg-surface-container border border-carbon-border rounded-xl p-3 flex gap-3">
          <img src="${coupon.imageUrl || 'https://images.unsplash.com/photo-1625047509168-a7026f36de04?auto=format&fit=crop&w=300&q=80'}" alt="Coupon" class="w-16 h-16 rounded-lg object-cover flex-shrink-0" onerror="this.onerror=null; this.src='https://images.unsplash.com/photo-1625047509168-a7026f36de04?auto=format&fit=crop&w=300&q=80';"/>
          <div class="flex flex-col justify-between flex-1 min-w-0">
            <div>
              <div class="flex items-center justify-between">
                <span class="font-chivo text-xs font-bold text-white truncate">${coupon.merchant}</span>
                <span class="px-1.5 py-0.2 bg-telemetry-yellow text-on-secondary font-chivo font-black text-[9px] rounded">ACTIVE</span>
              </div>
              <p class="text-[11px] text-on-surface-variant line-clamp-1 mt-0.5">${coupon.dealTitle}</p>
            </div>
            <div class="flex items-baseline justify-between mt-1">
              <span class="text-[10px] text-outline">1 Voucher</span>
              <div class="flex items-baseline gap-1">
                <span class="font-chivo text-base font-black text-telemetry-yellow">${coupon.amount}</span>
                <span class="text-[10px] text-telemetry-yellow font-bold uppercase">EGP</span>
              </div>
            </div>
          </div>
        </div>

        <div class="relative flex items-center justify-between my-0.5">
          <div class="w-3 h-3 rounded-full bg-surface-container-lowest -ml-5 border border-carbon-border"></div>
          <div class="flex-1 border-t border-dashed border-outline-variant mx-1 opacity-50"></div>
          <div class="w-3 h-3 rounded-full bg-surface-container-lowest -mr-5 border border-carbon-border"></div>
        </div>

        <div class="flex items-center justify-between gap-3">
          <button class="flex-1 flex items-center justify-center gap-1.5 py-2.5 px-3 bg-telemetry-yellow hover:bg-yellow-400 text-on-secondary rounded-xl font-chivo font-black text-xs uppercase tracking-wider transition-all shadow-[0_0_15px_rgba(255,208,0,0.25)] active:scale-95" onclick="openQRModal('${coupon.orderNum}', '${coupon.merchant.replace(/'/g, "\\'")}', '${coupon.dealTitle.replace(/'/g, "\\'")}', ${coupon.amount}, '${coupon.backupCode}', '${coupon.pin}')">
            <span class="material-symbols-outlined text-[18px]">qr_code_2</span>
            <span>Use Discount Coupon</span>
          </button>
          <div class="flex flex-col items-end shrink-0">
            <span class="text-[9px] text-outline uppercase">Valid Until</span>
            <span class="font-chivo text-xs font-bold text-primary">${coupon.validUntil}</span>
          </div>
        </div>
      </div>
    </div>
  `).join('');
}

// 11. QR Code Voucher Modal Logic
function openQRModal(orderNum, merchant, dealTitle, amount, backupCode, pin) {
  haptic(15);
  const modal = document.getElementById('modalQRRedemption');
  if (!modal) return;

  document.getElementById('qrModalOrderNum').textContent = `Order #${orderNum}`;
  document.getElementById('qrModalMerchantName').textContent = merchant;
  document.getElementById('qrModalDealTitle').textContent = dealTitle;
  document.getElementById('qrModalAmount').textContent = amount;
  document.getElementById('qrModalBackupCode').textContent = backupCode;
  document.getElementById('qrModalCashierPIN').textContent = pin.split('').join(' ');

  modal.classList.remove('hidden');
}

function closeQRModal() {
  haptic(10);
  const modal = document.getElementById('modalQRRedemption');
  if (modal) modal.classList.add('hidden');
}

function copyBackupCode() {
  const code = document.getElementById('qrModalBackupCode')?.textContent;
  if (code && navigator.clipboard) {
    navigator.clipboard.writeText(code).then(() => {
      triggerToast(`Copied code: ${code}`);
    }).catch(() => {
      triggerToast(`Code: ${code}`);
    });
  } else {
    triggerToast(`Code: ${code}`);
  }
}

// 12. Garage Fleet Management
function updateGarageUI() {
  const listContainer = document.getElementById('garageVehiclesList');
  const activeTitle = document.getElementById('garageVehicleTitle');
  const activeSpecs = document.getElementById('garageVehicleSpecs');
  const activeOdo = document.getElementById('garageVehicleOdo');
  const activePlate = document.getElementById('garageVehiclePlate');
  const homeWidgetTitle = document.getElementById('homeActiveVehicleName');

  if (state.activeVehicle) {
    if (activeTitle) activeTitle.textContent = `${state.activeVehicle.make} ${state.activeVehicle.model}`;
    if (activeSpecs) activeSpecs.textContent = state.activeVehicle.specs || 'Custom Setup';
    if (activeOdo) activeOdo.textContent = `${state.activeVehicle.odometer?.toLocaleString() || '0'} KM`;
    if (activePlate) activePlate.textContent = state.activeVehicle.plate || '---';
    if (homeWidgetTitle) homeWidgetTitle.textContent = `${state.activeVehicle.make} ${state.activeVehicle.model}`;
  }

  if (!listContainer) return;

  listContainer.innerHTML = state.vehicles.map(v => {
    const isCurrent = state.activeVehicle && state.activeVehicle.id === v.id;
    return `
      <div class="bg-carbon-surface border ${isCurrent ? 'border-telemetry-yellow/60' : 'border-carbon-border'} rounded-2xl p-3.5 flex items-center justify-between shadow-sm cursor-pointer active:scale-95 transition-all" onclick="selectActiveVehicle(${v.id})">
        <div class="flex items-center gap-3">
          <div class="w-10 h-10 rounded-xl ${isCurrent ? 'bg-telemetry-yellow/20 text-telemetry-yellow' : 'bg-surface-container text-on-surface-variant'} flex items-center justify-center">
            <span class="material-symbols-outlined text-[22px]">directions_car</span>
          </div>
          <div class="flex flex-col">
            <div class="flex items-center gap-2">
              <span class="font-chivo text-xs font-bold text-white">${v.make} ${v.model}</span>
              ${isCurrent ? '<span class="font-chivo text-[9px] bg-telemetry-yellow text-on-secondary px-1.5 py-0.2 rounded font-black">ACTIVE</span>' : ''}
            </div>
            <span class="text-[10px] text-on-surface-variant">${v.plate} • ${v.odometer?.toLocaleString()} KM</span>
          </div>
        </div>
        <span class="material-symbols-outlined text-[18px] text-outline">chevron_right</span>
      </div>
    `;
  }).join('');
}

function selectActiveVehicle(vehicleId) {
  const found = state.vehicles.find(v => v.id === vehicleId);
  if (found) {
    state.activeVehicle = found;
    saveState();
    updateGarageUI();
    triggerToast(`Active vehicle: ${found.make} ${found.model}`);
  }
}

function openAddVehicleModal() {
  haptic(10);
  document.getElementById('modalAddVehicle')?.classList.remove('hidden');
}

function closeAddVehicleModal() {
  haptic(10);
  document.getElementById('modalAddVehicle')?.classList.add('hidden');
}

function handleSaveVehicle(event) {
  event.preventDefault();
  haptic(20);

  const make = document.getElementById('inputVehicleMake')?.value.trim();
  const model = document.getElementById('inputVehicleModel')?.value.trim();
  const year = document.getElementById('inputVehicleYear')?.value;
  const plate = document.getElementById('inputVehiclePlate')?.value.trim();
  const odo = parseInt(document.getElementById('inputVehicleOdo')?.value || '0', 10);

  if (!make || !model) return;

  const newCar = {
    id: Date.now(),
    make: make,
    model: model,
    specs: `${model} • ${year}`,
    plate: plate,
    odometer: odo,
    status: 'Synced'
  };

  state.vehicles.push(newCar);
  state.activeVehicle = newCar;
  saveState();
  updateGarageUI();
  closeAddVehicleModal();

  // Reset form
  document.getElementById('formAddVehicle')?.reset();
  triggerToast(`${make} ${model} added to your garage!`);
}

// 13. Location Modal
function openLocationModal() {
  haptic(10);
  document.getElementById('modalLocation')?.classList.remove('hidden');
}

function closeLocationModal() {
  document.getElementById('modalLocation')?.classList.add('hidden');
}

function selectLocation(loc) {
  haptic(12);
  state.location = loc;
  const textElem = document.getElementById('currentLocationText');
  if (textElem) textElem.textContent = loc;
  closeLocationModal();
  triggerToast(`Location updated: ${loc}`);
}

// 14. Persistent Local State Caching
function saveState() {
  try {
    localStorage.setItem('cars_empire_pwa_state', JSON.stringify({
      vehicles: state.vehicles,
      activeVehicle: state.activeVehicle,
      coupons: state.coupons
    }));
  } catch (e) {
    console.warn('LocalStorage save error:', e);
  }
}

function loadCachedState() {
  try {
    const raw = localStorage.getItem('cars_empire_pwa_state');
    if (raw) {
      const parsed = JSON.parse(raw);
      if (parsed.vehicles && parsed.vehicles.length > 0) state.vehicles = parsed.vehicles;
      if (parsed.activeVehicle) state.activeVehicle = parsed.activeVehicle;
      if (parsed.coupons && parsed.coupons.length > 0) state.coupons = parsed.coupons;
    }
  } catch (e) {
    console.warn('LocalStorage load error:', e);
  }
}

// 15. Asynchronous Live API Fetching (Stale-While-Revalidate)
async function fetchLiveBackendData() {
  try {
    // 1. Fetch Deals
    const dealsRes = await fetch(`${API_BASE_URL}/deals/`);
    if (dealsRes.ok) {
      const data = await dealsRes.json();
      const results = Array.isArray(data) ? data : (data.results || []);
      if (results.length > 0) {
        state.deals = results.map(d => {
          const fallbackImg = getCategoryFallbackImage(d.category?.slug, d.title);
          const imgUrl = (d.main_image && typeof d.main_image === 'string' && d.main_image.startsWith('http'))
            ? d.main_image
            : ((d.image && typeof d.image === 'string' && d.image.startsWith('http')) ? d.image : fallbackImg);
          return {
            id: d.id,
            title: d.title,
            merchant_name: d.merchant?.name || d.merchant_name || 'Certified Garage',
            original_price: parseFloat(d.original_price || d.price || 1000),
            discount_price: parseFloat(d.discount_price || d.final_price || 650),
            discount_percentage: d.discount_percentage || 35,
            category_slug: d.category?.slug || 'oil',
            rating: parseFloat(d.rating || 4.8),
            reviews_count: d.views_count || 45,
            image_url: imgUrl,
            badge: d.is_flash_sale ? 'FLASH' : (d.is_trending ? 'HOT' : null)
          };
        });
        renderDeals();
      }
    }
  } catch (err) {
    console.log('[PWA] Using cached deals data');
  }

  try {
    // 2. Fetch User Profile
    const profileRes = await fetch(`${API_BASE_URL}/users/profile/`);
    if (profileRes.ok) {
      const user = await profileRes.json();
      const nameElem = document.getElementById('accountUserName');
      if (nameElem && user.name) {
        nameElem.textContent = user.name;
      }
    }
  } catch (err) {
    // Expected when guest
  }
}

// 16. Countdown Timers
function initTimers() {
  // Hero Banner Timer
  let heroSecs = 8 * 3600 + 42 * 60 + 19;
  const heroElem = document.getElementById('heroCountdown');
  
  // Flash Deal Timer
  let flashSecs = 23 * 3600 + 41 * 60 + 9;
  const flashElem = document.getElementById('flashTimer');

  // Security QR PIN Timer (5 minutes rolling)
  let pinSecs = 299;
  const pinTimerElem = document.getElementById('qrPINExpiryTimer');

  setInterval(() => {
    // Hero
    if (heroSecs > 0) heroSecs--;
    if (heroElem) {
      const h = String(Math.floor(heroSecs / 3600)).padStart(2, '0');
      const m = String(Math.floor((heroSecs % 3600) / 60)).padStart(2, '0');
      const s = String(heroSecs % 60).padStart(2, '0');
      heroElem.textContent = `${h}h : ${m}m : ${s}s`;
    }

    // Flash
    if (flashSecs > 0) flashSecs--;
    if (flashElem) {
      const fh = String(Math.floor(flashSecs / 3600)).padStart(2, '0');
      const fm = String(Math.floor((flashSecs % 3600) / 60)).padStart(2, '0');
      const fs = String(flashSecs % 60).padStart(2, '0');
      flashElem.textContent = `${fh}:${fm}:${fs}`;
    }

    // PIN
    if (pinSecs > 0) {
      pinSecs--;
    } else {
      pinSecs = 299;
      // Generate new pin
      const newPin = String(Math.floor(1000 + Math.random() * 9000)).split('').join(' ');
      const cashierPinElem = document.getElementById('qrModalCashierPIN');
      if (cashierPinElem) cashierPinElem.textContent = newPin;
    }
    if (pinTimerElem) {
      const pm = String(Math.floor(pinSecs / 60)).padStart(2, '0');
      const ps = String(pinSecs % 60).padStart(2, '0');
      pinTimerElem.textContent = `${pm}:${ps}`;
    }
  }, 1000);
}

// 17. Search & Input Handling
function initSearch() {
  const searchInput = document.getElementById('globalSearchInput');
  const btnClear = document.getElementById('btnClearSearch');

  if (searchInput) {
    searchInput.addEventListener('input', (e) => {
      state.searchQuery = e.target.value.trim();
      if (btnClear) {
        if (state.searchQuery.length > 0) {
          btnClear.classList.remove('hidden');
        } else {
          btnClear.classList.add('hidden');
        }
      }
      if (state.currentView !== 'offers' && state.searchQuery.length > 0) {
        switchView('offers');
      }
      renderDeals();
    });
  }

  if (btnClear) {
    btnClear.addEventListener('click', () => {
      if (searchInput) searchInput.value = '';
      state.searchQuery = '';
      btnClear.classList.add('hidden');
      renderDeals();
    });
  }

  // Location selector trigger
  const btnLoc = document.getElementById('btnLocation');
  if (btnLoc) {
    btnLoc.addEventListener('click', openLocationModal);
  }
}

// 17. App Theme Management (Light / Dark Mode)
function setTheme(theme) {
  haptic(12);
  const isDark = theme === 'dark';
  const html = document.documentElement;

  if (isDark) {
    html.classList.add('dark');
  } else {
    html.classList.remove('dark');
  }

  try {
    localStorage.setItem('carsempire_theme', theme);
  } catch (e) {}

  // Update theme-color meta tag
  const metaTheme = document.querySelector('meta[name="theme-color"]');
  if (metaTheme) {
    metaTheme.setAttribute('content', isDark ? '#0F141B' : '#F8FAFC');
  }

  // Update UI buttons and badge in Account tab
  const btnDark = document.getElementById('btnThemeDark');
  const btnLight = document.getElementById('btnThemeLight');
  const label = document.getElementById('currentThemeLabel');

  if (btnDark && btnLight) {
    if (isDark) {
      btnDark.className = 'flex items-center justify-center gap-1.5 py-2 px-3 rounded-lg font-chivo text-xs font-bold uppercase transition-all bg-primary-container text-white shadow active:scale-95';
      btnLight.className = 'flex items-center justify-center gap-1.5 py-2 px-3 rounded-lg font-chivo text-xs font-bold uppercase transition-all text-on-surface-variant hover:text-white active:scale-95';
    } else {
      btnLight.className = 'flex items-center justify-center gap-1.5 py-2 px-3 rounded-lg font-chivo text-xs font-bold uppercase transition-all bg-primary-container text-white shadow active:scale-95';
      btnDark.className = 'flex items-center justify-center gap-1.5 py-2 px-3 rounded-lg font-chivo text-xs font-bold uppercase transition-all text-on-surface-variant hover:text-slate-900 active:scale-95';
    }
  }

  if (label) {
    label.textContent = isDark ? 'Dark Mode' : 'Light Mode';
  }
}

function initTheme() {
  const savedTheme = localStorage.getItem('carsempire_theme') || 'dark';
  setTheme(savedTheme);
}

// 18. Dynamic Top Padding to ensure header never covers the first feed element
function adjustScrollPadding() {
  const header = document.querySelector('header');
  const scrollContainer = document.getElementById('app-scroll-container');
  if (header && scrollContainer) {
    const headerHeight = header.offsetHeight;
    scrollContainer.style.paddingTop = `${headerHeight + 12}px`;
  }
}
window.addEventListener('resize', adjustScrollPadding);
window.addEventListener('orientationchange', adjustScrollPadding);

// 19. Service Worker Registration
function registerServiceWorker() {
  if ('serviceWorker' in navigator) {
    // Auto-reload when new service worker takes control
    navigator.serviceWorker.addEventListener('controllerchange', () => {
      console.log('[PWA] ServiceWorker updated, refreshing application...');
      window.location.reload();
    });

    window.addEventListener('load', () => {
      navigator.serviceWorker.register('/app/sw.js?v=6', { scope: '/app/' })
        .then((reg) => {
          console.log('[PWA] ServiceWorker registered with scope:', reg.scope);
          // Check for update immediately to bust stale cache
          reg.update();
        })
        .catch((err) => {
          console.warn('[PWA] ServiceWorker registration failed:', err);
        });
    });
  }
}

// 20. Popstate / Back Gesture Integration
window.addEventListener('popstate', (event) => {
  const target = event.state?.view || 'home';
  switchView(target);
});

// 21. Initialization on DOMContentLoaded
document.addEventListener('DOMContentLoaded', () => {
  initTheme();
  loadCachedState();
  renderDeals();
  updateCouponsUI();
  updateGarageUI();
  initTimers();
  initSearch();
  adjustScrollPadding();
  registerServiceWorker();

  // Check URL query on start (e.g. ?tab=offers)
  const params = new URLSearchParams(window.location.search);
  const initialTab = params.get('tab');
  if (initialTab && VIEW_INDEX[initialTab] !== undefined) {
    switchView(initialTab);
  }

  // Adjust again after fonts / layout settle
  setTimeout(adjustScrollPadding, 200);

  // Fetch fresh data in background
  fetchLiveBackendData().then(() => {
    adjustScrollPadding();
  });
});
