/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'motion/react';
import { 
  Home, 
  Building2, 
  MapPin, 
  Phone, 
  Info, 
  ChevronRight, 
  Search, 
  Filter,
  ArrowLeft,
  X,
  ExternalLink,
  MessageCircle
} from 'lucide-react';
import { GoogleGenAI } from "@google/genai";

// Types
interface Product {
  id: string;
  name: string;
  type: 'Residential' | 'Commercial';
  description: string;
  priceRange: string;
  location: string;
  features: string[];
  imageUrl: string;
  status: 'Available' | 'Sold Out' | 'Coming Soon';
}

const PRODUCTS_DATA: Product[] = [
  {
    id: '1',
    name: 'Cluster Advani',
    type: 'Residential',
    description: 'Hunian modern dengan konsep smart home dan lingkungan hijau yang asri di Summarecon Emerald Karawang.',
    priceRange: 'Mulai Rp 1.2 Milyar',
    location: 'Summarecon Emerald Karawang',
    features: ['Smart Home System', 'Club House', 'Green Area', '24/7 Security'],
    imageUrl: 'https://picsum.photos/seed/advani/800/600',
    status: 'Available'
  },
  {
    id: '2',
    name: 'Cluster Elora',
    type: 'Residential',
    description: 'Elora menghadirkan kenyamanan hunian dengan desain kontemporer yang memaksimalkan sirkulasi udara dan cahaya alami.',
    priceRange: 'Mulai Rp 900 Juta',
    location: 'Summarecon Emerald Karawang',
    features: ['Modern Design', 'Jogging Track', 'Children Playground'],
    imageUrl: 'https://picsum.photos/seed/elora/800/600',
    status: 'Available'
  },
  {
    id: '3',
    name: 'Cluster Kalista',
    type: 'Residential',
    description: 'Cluster hunian eksklusif yang menawarkan ketenangan dan privasi bagi keluarga modern di Karawang.',
    priceRange: 'Mulai Rp 1.5 Milyar',
    location: 'Summarecon Emerald Karawang',
    features: ['Private Garden', 'Spacious Rooms', 'Premium Finishing'],
    imageUrl: 'https://picsum.photos/seed/kalista/800/600',
    status: 'Available'
  },
  {
    id: '4',
    name: 'Emerald Commercial',
    type: 'Commercial',
    description: 'Ruko strategis di pusat bisnis Summarecon Emerald Karawang, cocok untuk berbagai jenis usaha.',
    priceRange: 'Mulai Rp 2.5 Milyar',
    location: 'Summarecon Emerald Karawang',
    features: ['Strategic Location', 'Ample Parking', 'High Traffic Area'],
    imageUrl: 'https://picsum.photos/seed/commercial/800/600',
    status: 'Available'
  },
  {
    id: '5',
    name: 'Cluster Sevanti',
    type: 'Residential',
    description: 'Hunian kompak namun fungsional, ideal bagi pasangan muda atau profesional yang dinamis.',
    priceRange: 'Mulai Rp 800 Juta',
    location: 'Summarecon Emerald Karawang',
    features: ['Compact Design', 'Efficient Layout', 'Near Amenities'],
    imageUrl: 'https://picsum.photos/seed/sevanti/800/600',
    status: 'Sold Out'
  },
  {
    id: '6',
    name: 'Premium Verena Homes',
    type: 'Residential',
    description: 'Hunian mewah dengan desain klasik Eropa yang elegan dan eksklusif di Summarecon Emerald Karawang.',
    priceRange: 'Mulai Rp 2.5 Milyar',
    location: 'Summarecon Emerald Karawang',
    features: ['European Design', 'Private Club House', 'Premium Location', '24/7 Security'],
    imageUrl: 'https://picsum.photos/seed/verena/800/600',
    status: 'Available'
  }
];

export default function App() {
  const [selectedProduct, setSelectedProduct] = useState<Product | null>(null);
  const [searchQuery, setSearchQuery] = useState('');
  const [activeTab, setActiveTab] = useState<'All' | 'Residential' | 'Commercial'>('All');
  const [isSearching, setIsSearching] = useState(false);
  const [currentView, setCurrentView] = useState<'home' | 'units' | 'location' | 'contact'>('home');

  const filteredProducts = PRODUCTS_DATA.filter(p => {
    const matchesSearch = p.name.toLowerCase().includes(searchQuery.toLowerCase()) || 
                         p.description.toLowerCase().includes(searchQuery.toLowerCase());
    const matchesTab = activeTab === 'All' || p.type === activeTab;
    return matchesSearch && matchesTab;
  });

  const renderHome = () => (
    <motion.div 
      initial={{ opacity: 0 }} 
      animate={{ opacity: 1 }} 
      className="px-4 py-6"
    >
      {/* Hero Banner */}
      <div className="relative h-56 rounded-[40px] overflow-hidden shadow-2xl mb-8">
        <img 
          src="https://picsum.photos/seed/summarecon-hero/1200/800" 
          alt="Summarecon Emerald Karawang" 
          className="w-full h-full object-cover"
          referrerPolicy="no-referrer"
        />
        <div className="absolute inset-0 bg-gradient-to-t from-black/80 via-black/20 to-transparent flex flex-col justify-end p-8">
          <motion.h2 
            initial={{ y: 20, opacity: 0 }}
            animate={{ y: 0, opacity: 1 }}
            className="text-white text-3xl font-bold leading-tight"
          >
            Masa Depan <br />Hunian Anda
          </motion.h2>
          <p className="text-white/70 text-sm mt-2">Summarecon Emerald Karawang</p>
        </div>
      </div>

      {/* Quick Stats */}
      <div className="grid grid-cols-3 gap-4 mb-8">
        {[
          { label: 'Luas Area', value: '40 Ha' },
          { label: 'Cluster', value: '5+' },
          { label: 'Fasilitas', value: '10+' },
        ].map((stat, i) => (
          <div key={i} className="bg-white p-4 rounded-3xl border border-neutral-100 shadow-sm text-center">
            <p className="text-emerald-600 font-bold text-lg">{stat.value}</p>
            <p className="text-neutral-400 text-[10px] uppercase tracking-wider font-medium">{stat.label}</p>
          </div>
        ))}
      </div>

      {/* Featured Section */}
      <div className="mb-8">
        <div className="flex justify-between items-center mb-4">
          <h3 className="font-bold text-xl">Unit Pilihan</h3>
          <button 
            onClick={() => setCurrentView('units')}
            className="text-emerald-600 text-sm font-bold flex items-center gap-1"
          >
            Lihat Semua <ChevronRight size={16} />
          </button>
        </div>
        <div className="flex gap-4 overflow-x-auto no-scrollbar pb-4 -mx-4 px-4">
          {PRODUCTS_DATA.slice(0, 3).map((product) => (
            <div 
              key={product.id}
              onClick={() => setSelectedProduct(product)}
              className="min-w-[280px] bg-white rounded-[32px] overflow-hidden border border-neutral-100 shadow-sm"
            >
              <img src={product.imageUrl} alt={product.name} className="h-40 w-full object-cover" />
              <div className="p-5">
                <h4 className="font-bold">{product.name}</h4>
                <p className="text-emerald-600 font-bold text-sm mt-1">{product.priceRange}</p>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Why Karawang */}
      <div className="bg-emerald-900 rounded-[40px] p-8 text-white">
        <h3 className="text-2xl font-bold mb-4">Mengapa Summarecon Karawang?</h3>
        <ul className="space-y-4">
          {[
            'Lokasi strategis di pusat industri Karawang',
            'Akses mudah via Tol Jakarta-Cikampek',
            'Lingkungan asri dengan konsep Green Living',
            'Fasilitas lengkap bertaraf internasional',
          ].map((item, i) => (
            <li key={i} className="flex gap-3 items-start">
              <div className="w-5 h-5 bg-emerald-500 rounded-full flex-shrink-0 flex items-center justify-center text-[10px]">✓</div>
              <p className="text-emerald-100 text-sm">{item}</p>
            </li>
          ))}
        </ul>
      </div>
    </motion.div>
  );

  const renderUnits = () => (
    <motion.div 
      initial={{ opacity: 0 }} 
      animate={{ opacity: 1 }}
    >
      {/* Filter Header */}
      <div className="px-4 pt-6 pb-2 flex items-center justify-between">
        <h3 className="font-bold text-xl">Daftar Unit</h3>
        <div className="flex items-center gap-2 text-neutral-400 text-sm">
          <Filter size={16} />
          <span>Filter</span>
        </div>
      </div>

      {/* Tabs / Toggle Buttons */}
      <section className="px-4 flex gap-2 overflow-x-auto no-scrollbar py-4 sticky top-[57px] bg-neutral-50/80 backdrop-blur-md z-30">
        {(['All', 'Residential', 'Commercial'] as const).map(tab => (
          <button
            key={tab}
            onClick={() => setActiveTab(tab)}
            className={`px-6 py-2.5 rounded-2xl text-sm font-bold transition-all whitespace-nowrap flex items-center gap-2 ${
              activeTab === tab 
                ? 'bg-emerald-600 text-white shadow-lg shadow-emerald-600/20' 
                : 'bg-white text-neutral-500 border border-neutral-200 hover:border-emerald-200'
            }`}
          >
            {tab === 'All' && <Building2 size={16} />}
            {tab === 'Residential' && <Home size={16} />}
            {tab === 'Commercial' && <Building2 size={16} />}
            {tab === 'All' ? 'Semua Properti' : tab === 'Residential' ? 'Hunian' : 'Komersial'}
          </button>
        ))}
      </section>

      {/* Product List */}
      <section className="px-4 mt-2 grid gap-4">
        {filteredProducts.map((product, index) => (
          <motion.div
            key={product.id}
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: index * 0.1 }}
            onClick={() => setSelectedProduct(product)}
            className="bg-white rounded-3xl overflow-hidden border border-neutral-100 shadow-sm active:scale-[0.98] transition-transform cursor-pointer"
          >
            <div className="relative h-48">
              <img 
                src={product.imageUrl} 
                alt={product.name} 
                className="w-full h-full object-cover"
                referrerPolicy="no-referrer"
              />
              <div className="absolute top-4 left-4">
                <span className={`px-3 py-1 rounded-full text-[10px] font-bold uppercase tracking-wider ${
                  product.type === 'Residential' ? 'bg-blue-500 text-white' : 'bg-orange-500 text-white'
                }`}>
                  {product.type === 'Residential' ? 'Hunian' : 'Komersial'}
                </span>
              </div>
              {product.status === 'Sold Out' && (
                <div className="absolute inset-0 bg-black/40 flex items-center justify-center">
                  <span className="bg-red-600 text-white px-4 py-1 rounded-lg font-bold uppercase tracking-widest text-xs">Terjual Habis</span>
                </div>
              )}
            </div>
            <div className="p-5">
              <div className="flex justify-between items-start">
                <div>
                  <h3 className="font-bold text-lg">{product.name}</h3>
                  <div className="flex items-center gap-1 text-neutral-500 text-xs mt-1">
                    <MapPin size={12} />
                    <span>{product.location}</span>
                  </div>
                </div>
                <ChevronRight className="text-neutral-300" />
              </div>
              <div className="mt-4 flex items-center justify-between">
                <span className="text-emerald-600 font-bold text-sm">{product.priceRange}</span>
                <div className="flex gap-1">
                  {product.features.slice(0, 2).map((f, i) => (
                    <span key={i} className="bg-neutral-100 text-neutral-500 text-[10px] px-2 py-1 rounded-md">{f}</span>
                  ))}
                </div>
              </div>
            </div>
          </motion.div>
        ))}
      </section>
    </motion.div>
  );

  const renderLocation = () => (
    <motion.div 
      initial={{ opacity: 0 }} 
      animate={{ opacity: 1 }}
      className="px-4 py-6"
    >
      <h3 className="text-2xl font-bold mb-6">Lokasi Strategis</h3>
      <div className="bg-white rounded-[40px] overflow-hidden border border-neutral-100 shadow-sm mb-6">
        <div className="h-64 bg-neutral-200 relative">
          {/* Mock Map */}
          <img 
            src="https://picsum.photos/seed/karawang-map/800/600" 
            alt="Map Location" 
            className="w-full h-full object-cover opacity-50 grayscale"
          />
          <div className="absolute inset-0 flex items-center justify-center">
            <div className="relative">
              <div className="w-12 h-12 bg-emerald-600 rounded-full animate-ping absolute -inset-0" />
              <div className="w-12 h-12 bg-emerald-600 rounded-full flex items-center justify-center text-white relative">
                <MapPin size={24} />
              </div>
            </div>
          </div>
        </div>
        <div className="p-6">
          <h4 className="font-bold text-lg mb-2">Summarecon Emerald Karawang</h4>
          <p className="text-neutral-500 text-sm leading-relaxed">
            Jl. Bulevar Summarecon Emerald Karawang, Kondangjaya, Karawang Timur, Karawang, Jawa Barat 41371
          </p>
          <button className="w-full mt-6 bg-neutral-900 text-white py-4 rounded-2xl font-bold flex items-center justify-center gap-2">
            <ExternalLink size={18} />
            Buka di Google Maps
          </button>
        </div>
      </div>

      <div className="space-y-4">
        {[
          { label: 'Pintu Tol Karawang Timur', time: '10 Menit' },
          { label: 'Stasiun Karawang', time: '15 Menit' },
          { label: 'Pusat Kota Karawang', time: '12 Menit' },
          { label: 'Kawasan Industri KIIC', time: '20 Menit' },
        ].map((loc, i) => (
          <div key={i} className="flex justify-between items-center p-4 bg-white rounded-2xl border border-neutral-100">
            <span className="text-neutral-700 font-medium">{loc.label}</span>
            <span className="text-emerald-600 font-bold text-sm">{loc.time}</span>
          </div>
        ))}
      </div>
    </motion.div>
  );

  const renderContact = () => (
    <motion.div 
      initial={{ opacity: 0 }} 
      animate={{ opacity: 1 }}
      className="px-4 py-6"
    >
      <h3 className="text-2xl font-bold mb-6">Hubungi Kami</h3>
      
      <div className="bg-emerald-600 rounded-[40px] p-8 text-white mb-6 shadow-xl shadow-emerald-600/20">
        <p className="text-emerald-100 text-sm mb-2">In-house Sales</p>
        <h4 className="text-2xl font-bold mb-6">Dapatkan Penawaran Eksklusif Hari Ini</h4>
        <a 
          href="https://wa.me/6287884256765?text=Halo%20Summarecon%20Karawang,%20saya%20tertarik%20dengan%20produk%20Anda."
          target="_blank"
          rel="noopener noreferrer"
          className="bg-white text-emerald-600 w-full py-4 rounded-2xl font-bold flex items-center justify-center gap-2 shadow-lg active:scale-95 transition-all"
        >
          <MessageCircle size={20} />
          WhatsApp Sekarang
        </a>
      </div>

      <div className="grid gap-4">
        <div className="bg-white p-6 rounded-3xl border border-neutral-100 flex items-center gap-4">
          <div className="w-12 h-12 bg-emerald-50 text-emerald-600 rounded-2xl flex items-center justify-center">
            <MessageCircle size={24} />
          </div>
          <div>
            <p className="text-neutral-400 text-xs uppercase tracking-wider font-bold">In-house Sales</p>
            <p className="font-bold text-neutral-800">0878 8425 6765</p>
          </div>
        </div>
        <div className="bg-white p-6 rounded-3xl border border-neutral-100 flex items-center gap-4">
          <div className="w-12 h-12 bg-blue-50 text-blue-600 rounded-2xl flex items-center justify-center">
            <Phone size={24} />
          </div>
          <div>
            <p className="text-neutral-400 text-xs uppercase tracking-wider font-bold">Marketing Gallery</p>
            <p className="font-bold text-neutral-800">+62 267 8402 888</p>
          </div>
        </div>
        <div className="bg-white p-6 rounded-3xl border border-neutral-100 flex items-center gap-4">
          <div className="w-12 h-12 bg-pink-50 text-pink-600 rounded-2xl flex items-center justify-center">
            <Info size={24} />
          </div>
          <div>
            <p className="text-neutral-400 text-xs uppercase tracking-wider font-bold">Instagram</p>
            <p className="font-bold text-neutral-800">@summareconkarawang</p>
          </div>
        </div>
      </div>

      <div className="mt-12 text-center">
        <p className="text-neutral-400 text-xs">© 2026 PT Summarecon Agung Tbk.</p>
        <p className="text-neutral-400 text-[10px] mt-1">All Rights Reserved</p>
      </div>
    </motion.div>
  );

  return (
    <div className="min-h-screen bg-neutral-50 font-sans text-neutral-900 overflow-x-hidden">
      {/* Header */}
      <header className="sticky top-0 z-40 bg-white/80 backdrop-blur-md border-b border-neutral-200 px-4 py-3 flex items-center justify-between">
        <div className="flex items-center gap-2">
          <div className="w-8 h-8 bg-emerald-600 rounded-lg flex items-center justify-center text-white font-bold">S</div>
          <h1 className="font-bold text-lg tracking-tight">Summarecon <span className="text-emerald-600">Karawang</span></h1>
        </div>
        <button 
          onClick={() => setIsSearching(!isSearching)}
          className="p-2 hover:bg-neutral-100 rounded-full transition-colors"
        >
          <Search size={20} />
        </button>
      </header>

      {/* Search Bar (Animated) */}
      <AnimatePresence>
        {isSearching && (
          <motion.div 
            initial={{ height: 0, opacity: 0 }}
            animate={{ height: 'auto', opacity: 1 }}
            exit={{ height: 0, opacity: 0 }}
            className="bg-white border-b border-neutral-200 px-4 py-3 overflow-hidden"
          >
            <div className="relative">
              <Search className="absolute left-3 top-1/2 -translate-y-1/2 text-neutral-400" size={18} />
              <input 
                type="text" 
                placeholder="Cari cluster atau ruko..."
                className="w-full bg-neutral-100 border-none rounded-xl py-2 pl-10 pr-4 focus:ring-2 focus:ring-emerald-500 outline-none"
                value={searchQuery}
                onChange={(e) => {
                  setSearchQuery(e.target.value);
                  if (currentView !== 'units') setCurrentView('units');
                }}
                autoFocus
              />
              {searchQuery && (
                <button 
                  onClick={() => setSearchQuery('')}
                  className="absolute right-3 top-1/2 -translate-y-1/2 text-neutral-400"
                >
                  <X size={18} />
                </button>
              )}
            </div>
          </motion.div>
        )}
      </AnimatePresence>

      {/* Main Content */}
      <main className="pb-24">
        {currentView === 'home' && renderHome()}
        {currentView === 'units' && renderUnits()}
        {currentView === 'location' && renderLocation()}
        {currentView === 'contact' && renderContact()}
      </main>

      {/* Bottom Navigation */}
      <nav className="fixed bottom-0 left-0 right-0 bg-white/80 backdrop-blur-lg border-t border-neutral-200 px-6 py-3 flex justify-between items-center z-40">
        <button 
          onClick={() => setCurrentView('home')}
          className={`flex flex-col items-center gap-1 transition-colors ${currentView === 'home' ? 'text-emerald-600' : 'text-neutral-400'}`}
        >
          <Home size={24} />
          <span className="text-[10px] font-medium">Beranda</span>
        </button>
        <button 
          onClick={() => setCurrentView('units')}
          className={`flex flex-col items-center gap-1 transition-colors ${currentView === 'units' ? 'text-emerald-600' : 'text-neutral-400'}`}
        >
          <Building2 size={24} />
          <span className="text-[10px] font-medium">Unit</span>
        </button>
        <button 
          onClick={() => setCurrentView('location')}
          className={`flex flex-col items-center gap-1 transition-colors ${currentView === 'location' ? 'text-emerald-600' : 'text-neutral-400'}`}
        >
          <MapPin size={24} />
          <span className="text-[10px] font-medium">Lokasi</span>
        </button>
        <button 
          onClick={() => setCurrentView('contact')}
          className={`flex flex-col items-center gap-1 transition-colors ${currentView === 'contact' ? 'text-emerald-600' : 'text-neutral-400'}`}
        >
          <Phone size={24} />
          <span className="text-[10px] font-medium">Kontak</span>
        </button>
      </nav>

      {/* Detail Modal */}
      <AnimatePresence>
        {selectedProduct && (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            className="fixed inset-0 z-50 bg-black/60 backdrop-blur-sm flex items-end sm:items-center justify-center p-0 sm:p-4"
          >
            <motion.div
              initial={{ y: '100%' }}
              animate={{ y: 0 }}
              exit={{ y: '100%' }}
              className="bg-white w-full max-w-lg rounded-t-[40px] sm:rounded-[40px] overflow-hidden max-h-[90vh] flex flex-col"
            >
              <div className="relative h-64 flex-shrink-0">
                <img 
                  src={selectedProduct.imageUrl} 
                  alt={selectedProduct.name} 
                  className="w-full h-full object-cover"
                  referrerPolicy="no-referrer"
                />
                <button 
                  onClick={() => setSelectedProduct(null)}
                  className="absolute top-6 right-6 w-10 h-10 bg-white/20 backdrop-blur-md rounded-full flex items-center justify-center text-white hover:bg-white/40 transition-colors"
                >
                  <X size={24} />
                </button>
                <div className="absolute bottom-6 left-6">
                  <span className="bg-emerald-600 text-white px-4 py-1 rounded-full text-xs font-bold uppercase tracking-widest">
                    {selectedProduct.type}
                  </span>
                </div>
              </div>
              
              <div className="p-8 overflow-y-auto flex-grow">
                <div className="flex justify-between items-start mb-4">
                  <div>
                    <h2 className="text-2xl font-bold">{selectedProduct.name}</h2>
                    <div className="flex items-center gap-1 text-neutral-500 text-sm mt-1">
                      <MapPin size={14} />
                      <span>{selectedProduct.location}</span>
                    </div>
                  </div>
                  <div className="text-right">
                    <p className="text-emerald-600 font-bold text-xl">{selectedProduct.priceRange}</p>
                    <p className="text-neutral-400 text-xs mt-1">Harga mulai dari</p>
                  </div>
                </div>

                <div className="h-px bg-neutral-100 my-6" />

                <section className="mb-8">
                  <h4 className="font-bold text-neutral-900 mb-3 flex items-center gap-2">
                    <Info size={18} className="text-emerald-600" />
                    Deskripsi
                  </h4>
                  <p className="text-neutral-600 leading-relaxed">
                    {selectedProduct.description}
                  </p>
                </section>

                <section className="mb-8">
                  <h4 className="font-bold text-neutral-900 mb-3">Fasilitas & Keunggulan</h4>
                  <div className="grid grid-cols-2 gap-3">
                    {selectedProduct.features.map((feature, i) => (
                      <div key={i} className="flex items-center gap-2 bg-neutral-50 p-3 rounded-2xl border border-neutral-100">
                        <div className="w-2 h-2 bg-emerald-500 rounded-full" />
                        <span className="text-sm text-neutral-700">{feature}</span>
                      </div>
                    ))}
                  </div>
                </section>

                <div className="flex gap-4 mt-8">
                  <a 
                    href={`https://wa.me/6287884256765?text=Halo%20Summarecon%20Karawang,%20saya%20tertarik%20dengan%20${encodeURIComponent(selectedProduct.name)}.`}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="flex-1 bg-emerald-600 text-white py-4 rounded-2xl font-bold shadow-lg shadow-emerald-600/30 active:scale-95 transition-all flex items-center justify-center gap-2"
                  >
                    <MessageCircle size={20} />
                    Hubungi Sales
                  </a>
                  <button className="w-14 h-14 border border-neutral-200 rounded-2xl flex items-center justify-center text-neutral-600 active:scale-95 transition-all">
                    <ExternalLink size={20} />
                  </button>
                </div>
              </div>
            </motion.div>
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
}
