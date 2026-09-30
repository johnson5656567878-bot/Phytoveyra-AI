import { Crop, Farm, PlantScan, TreatmentRecommendation, TreatmentSchedule, RecoveryScan, WeatherData, RiskAlert } from './types';

export const getApiBaseUrl = (): string => {
  // If running on server (SSR / API route) and API_URL is provided by Vercel service binding
  if (typeof window === 'undefined' && process.env.API_URL) {
    const rawUrl = process.env.API_URL.replace(/\/$/, '');
    return rawUrl.endsWith('/api') ? rawUrl : `${rawUrl}/api`;
  }
  // If NEXT_PUBLIC_API_URL is explicitly set
  if (process.env.NEXT_PUBLIC_API_URL) {
    return process.env.NEXT_PUBLIC_API_URL.replace(/\/$/, '');
  }
  // In the browser, the unified Vercel rewrite maps /api/(.*) to the API service
  if (typeof window !== 'undefined') {
    return '/api';
  }
  return 'http://localhost:8000/api';
};

const API_BASE_URL = getApiBaseUrl();

async function fetchFromApi<T>(endpoint: string, options?: RequestInit): Promise<T | null> {
  try {
    const res = await fetch(`${API_BASE_URL}${endpoint}`, {
      headers: {
        'Content-Type': 'application/json',
        ...options?.headers
      },
      ...options
    });
    if (res.ok) {
      return await res.json();
    }
  } catch (err) {
    console.warn(`API call to ${endpoint} failed`, err);
  }
  return null;
}

export const api = {
  getFarms: async (): Promise<Farm[]> => {
    const res = await fetchFromApi<Farm[]>('/farms');
    return res || [];
  },

  getCrops: async (): Promise<Crop[]> => {
    const res = await fetchFromApi<Crop[]>('/crops');
    return res || [];
  },

  getScans: async (): Promise<PlantScan[]> => {
    const res = await fetchFromApi<PlantScan[]>('/scans');
    return res || [];
  },

  getScanById: async (scanId: string): Promise<PlantScan | null> => {
    return await fetchFromApi<PlantScan>(`/scans/${scanId}`);
  },

  getTreatmentByScanId: async (scanId: string): Promise<any | null> => {
    const res = await fetchFromApi<any>(`/treatments/${scanId}`);
    if (res) return res;
    return await fetchFromApi<any>(`/treatments/by-scan/${scanId}`);
  },

  getTreatmentRecommendation: async (title: string): Promise<TreatmentRecommendation | null> => {
    return await fetchFromApi<TreatmentRecommendation>(`/treatments/recommend?diagnosis_title=${encodeURIComponent(title)}`);
  },

  getSchedules: async (): Promise<TreatmentSchedule[]> => {
    const res = await fetchFromApi<TreatmentSchedule[]>('/schedules');
    return res || [];
  },

  createSchedule: async (data: { scan_id?: string; crop_id?: string; action_item: string; scheduled_date: string; follow_up_date: string; notes?: string }): Promise<TreatmentSchedule | null> => {
    return await fetchFromApi<TreatmentSchedule>('/schedules', {
      method: 'POST',
      body: JSON.stringify(data)
    });
  },

  getRecoveryByScanId: async (scanId: string): Promise<any | null> => {
    return await fetchFromApi<any>(`/recovery/by-scan/${scanId}`);
  },

  getWeather: async (): Promise<WeatherData | null> => {
    return await fetchFromApi<WeatherData>('/weather');
  },

  getRiskAlerts: async (): Promise<RiskAlert[]> => {
    const res = await fetchFromApi<RiskAlert[]>('/alerts');
    return res || [];
  },

  sendChatMessage: async (data: {
    text: string;
    language?: string;
    session_id?: string;
    history?: { sender: 'user' | 'assistant'; text: string }[];
  }): Promise<any | null> => {
    return await fetchFromApi<any>('/chat', {
      method: 'POST',
      body: JSON.stringify(data)
    });
  }
};
