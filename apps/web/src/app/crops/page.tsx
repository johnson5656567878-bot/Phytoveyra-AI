'use client';

import React, { useState, useEffect } from 'react';
import { useTranslation } from '@/lib/i18n';
import { api } from '@/lib/api';
import { Crop } from '@/lib/types';
import { Sprout, Plus, MapPin, Droplets, Sun, Calendar, Layers, ShieldCheck, Activity } from 'lucide-react';

export default function CropsPage() {
  const { t } = useTranslation();
  const [crops, setCrops] = useState<Crop[]>([]);
  const [loading, setLoading] = useState(true);
  const [showAddModal, setShowAddModal] = useState(false);
  const [formData, setFormData] = useState({
    name: 'Paddy Rice',
    variety: 'ADT 43',
    planting_date: new Date().toISOString().split('T')[0],
    area_acres: 1.0,
    growth_stage: 'Vegetative Stage'
  });

  useEffect(() => {
    async function loadCrops() {
      try {
        const res = await api.getCrops();
        setCrops(res);
      } catch (err) {
        console.error("Crops load error", err);
      } finally {
        setLoading(false);
      }
    }
    loadCrops();
  }, []);

  const handleAddCrop = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api';
      const res = await fetch(`${API_URL}/crops`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          name: formData.name,
          variety: formData.variety,
          planting_date: formData.planting_date,
          area_acres: Number(formData.area_acres),
          growth_stage: formData.growth_stage,
          health_status: 'Healthy'
        })
      });
      if (res.ok) {
        const created = await res.json();
        setCrops([created, ...crops]);
      } else {
        const localCrop: Crop = {
          id: `crop-${Date.now()}`,
          farm_id: 'farm-1',
          name: formData.name,
          variety: formData.variety,
          planting_date: formData.planting_date,
          area_acres: Number(formData.area_acres),
          growth_stage: formData.growth_stage,
          health_status: 'Healthy',
          created_at: new Date().toISOString()
        };
        setCrops([localCrop, ...crops]);
      }
    } catch (err) {
      console.error("Add crop error", err);
    } finally {
      setShowAddModal(false);
    }
  };

  return (
    <div className="space-y-6 max-w-7xl mx-auto">
      
      {/* Header */}
      <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4">
        <div>
          <h1 className="text-2xl sm:text-3xl font-extrabold text-white flex items-center gap-2">
            <Sprout className="w-8 h-8 text-emerald-400" />
            {t('nav.crops')} & Field Management
          </h1>
          <p className="text-sm text-emerald-200/80 mt-1">
            Track registered farm fields, crop growth stages, and soil irrigation details.
          </p>
        </div>

        <button
          onClick={() => setShowAddModal(true)}
          className="flex items-center space-x-2 bg-gradient-to-r from-emerald-500 to-teal-400 text-emerald-950 font-bold px-4 py-2.5 rounded-xl shadow-lg hover:scale-105 transition-transform text-sm"
        >
          <Plus className="w-4 h-4 stroke-[3]" />
          <span>Add New Crop</span>
        </button>
      </div>

      {/* Crops List Grid */}
      {crops.length === 0 ? (
        <div className="glass-panel p-12 rounded-2xl border border-emerald-800/60 text-center space-y-4">
          <div className="w-16 h-16 rounded-full bg-emerald-500/10 text-emerald-400 border border-emerald-500/20 flex items-center justify-center mx-auto">
            <Sprout className="w-8 h-8" />
          </div>
          <div>
            <h3 className="text-base font-bold text-white">No crops added yet.</h3>
            <p className="text-xs text-emerald-300/70 max-w-sm mx-auto mt-1">
              Click &quot;Add New Crop&quot; above or run an AI plant scan to register your crops in the database.
            </p>
          </div>
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {crops.map((crop) => (
            <div key={crop.id} className="glass-card rounded-2xl p-6 border border-emerald-800/60 hover:border-emerald-600 transition-all space-y-4">
              
              <div className="flex items-start justify-between">
                <div>
                  <h3 className="text-lg font-bold text-white">{crop.name}</h3>
                  <p className="text-xs text-emerald-300/80">Variety: {crop.variety || 'Standard'}</p>
                </div>
                <span className={`text-xs font-bold px-3 py-1 rounded-full border ${
                  crop.health_status === 'Healthy'
                    ? 'bg-emerald-950 text-emerald-300 border-emerald-700'
                    : 'bg-amber-950 text-amber-300 border-amber-700'
                }`}>
                  {crop.health_status}
                </span>
              </div>

              <div className="space-y-2 text-xs text-emerald-200/90 pt-2 border-t border-emerald-800/40">
                <div className="flex justify-between">
                  <span>Growth Stage:</span>
                  <strong className="text-teal-300">{crop.growth_stage}</strong>
                </div>
                <div className="flex justify-between">
                  <span>Planted Area:</span>
                  <strong className="text-emerald-200">{crop.area_acres} Acres</strong>
                </div>
                <div className="flex justify-between">
                  <span>Planting Date:</span>
                  <strong className="text-emerald-200">{crop.planting_date || new Date().toISOString().split('T')[0]}</strong>
                </div>
              </div>

              <div className="pt-2">
                <a
                  href={`/scan?cropId=${crop.id}`}
                  className="w-full inline-flex items-center justify-center space-x-2 bg-emerald-800/80 hover:bg-emerald-700 text-emerald-100 font-bold py-2 rounded-xl text-xs transition-colors"
                >
                  <span>Run AI Health Scan</span>
                </a>
              </div>

            </div>
          ))}
        </div>
      )}

      {/* Add Crop Modal */}
      {showAddModal && (
        <div className="fixed inset-0 z-50 bg-black/80 backdrop-blur-sm flex items-center justify-center p-4">
          <div className="bg-emerald-950 border border-emerald-700/60 rounded-3xl p-6 max-w-md w-full space-y-4 shadow-2xl">
            <h3 className="text-lg font-bold text-white">Add New Crop Field</h3>
            
            <form onSubmit={handleAddCrop} className="space-y-3 text-xs">
              <div>
                <label className="block text-emerald-300 mb-1">Crop Name</label>
                <input
                  type="text"
                  value={formData.name}
                  onChange={(e) => setFormData({ ...formData, name: e.target.value })}
                  placeholder="e.g. Paddy Rice, Chilli, Maize, Wheat"
                  className="w-full bg-emerald-900/60 border border-emerald-700 rounded-xl p-2.5 text-white focus:outline-none focus:border-emerald-400"
                  required
                />
              </div>

              <div>
                <label className="block text-emerald-300 mb-1">Variety</label>
                <input
                  type="text"
                  value={formData.variety}
                  onChange={(e) => setFormData({ ...formData, variety: e.target.value })}
                  placeholder="e.g. ADT 43"
                  className="w-full bg-emerald-900/60 border border-emerald-700 rounded-xl p-2.5 text-white focus:outline-none focus:border-emerald-400"
                />
              </div>

              <div className="grid grid-cols-2 gap-3">
                <div>
                  <label className="block text-emerald-300 mb-1">Area (Acres)</label>
                  <input
                    type="number"
                    step="0.1"
                    value={formData.area_acres}
                    onChange={(e) => setFormData({ ...formData, area_acres: Number(e.target.value) })}
                    className="w-full bg-emerald-900/60 border border-emerald-700 rounded-xl p-2.5 text-white focus:outline-none focus:border-emerald-400"
                  />
                </div>
                <div>
                  <label className="block text-emerald-300 mb-1">Growth Stage</label>
                  <select
                    value={formData.growth_stage}
                    onChange={(e) => setFormData({ ...formData, growth_stage: e.target.value })}
                    className="w-full bg-emerald-900/60 border border-emerald-700 rounded-xl p-2.5 text-white focus:outline-none focus:border-emerald-400"
                  >
                    <option value="Seedling">Seedling</option>
                    <option value="Vegetative Stage">Vegetative Stage</option>
                    <option value="Flowering Stage">Flowering Stage</option>
                    <option value="Fruiting Stage">Fruiting Stage</option>
                    <option value="Harvesting">Harvesting</option>
                  </select>
                </div>
              </div>

              <div className="flex items-center justify-end space-x-3 pt-3">
                <button
                  type="button"
                  onClick={() => setShowAddModal(false)}
                  className="px-4 py-2 bg-emerald-900 text-emerald-300 rounded-xl font-semibold"
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  className="px-5 py-2 bg-gradient-to-r from-emerald-500 to-teal-400 text-emerald-950 font-bold rounded-xl shadow-md"
                >
                  Save Crop
                </button>
              </div>
            </form>
          </div>
        </div>
      )}

    </div>
  );
}
