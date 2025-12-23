import axios from 'axios';
import AsyncStorage from '@react-native-async-storage/async-storage';

// API Configuration
const API_BASE_URL = 'https://8002-i5cseikj92ei70k8wadux-2e77fc33.sandbox.novita.ai';

const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Cache keys
const CACHE_KEYS = {
  ANALYSIS_RESULTS: 'analysis_results',
  FEATURED_VIDEOS: 'featured_videos',
  VIDEO_LIBRARY: 'video_library',
};

/**
 * Enhanced Analysis API (Priority 9 + 10 + 11 + 13)
 */
export const analyzeSwing = async (data) => {
  try {
    const response = await api.post('/analyze/enhanced', {
      ground_score: data.groundScore,
      engine_score: data.engineScore,
      weapon_score: data.weaponScore,
      height_inches: data.heightInches,
      wingspan_inches: data.wingspanInches,
      weight_lbs: data.weightLbs,
      age: data.age,
      bat_weight_oz: data.batWeightOz || 30,
      actual_bat_speed_mph: data.actualBatSpeed,
      rotation_ke_joules: data.rotationKE,
      translation_ke_joules: data.translationKE,
      include_videos: true,
      max_videos_per_drill: 3,
    });

    // Cache the results
    await cacheData(CACHE_KEYS.ANALYSIS_RESULTS, response.data);

    return response.data;
  } catch (error) {
    console.error('Analysis API Error:', error);
    
    // Try to return cached data if available
    const cachedData = await getCachedData(CACHE_KEYS.ANALYSIS_RESULTS);
    if (cachedData) {
      return cachedData;
    }
    
    throw error;
  }
};

/**
 * Video Library API
 */
export const getFeaturedVideos = async () => {
  try {
    const response = await api.get('/videos/featured');
    await cacheData(CACHE_KEYS.FEATURED_VIDEOS, response.data);
    return response.data;
  } catch (error) {
    console.error('Featured Videos Error:', error);
    const cachedData = await getCachedData(CACHE_KEYS.FEATURED_VIDEOS);
    if (cachedData) return cachedData;
    throw error;
  }
};

export const searchVideos = async (query, tags = null, category = null, stage = null) => {
  try {
    const params = new URLSearchParams();
    if (query) params.append('q', query);
    if (tags) params.append('tags', tags);
    if (category) params.append('category', category);
    if (stage) params.append('stage', stage);

    const response = await api.get(`/videos/search?${params.toString()}`);
    return response.data;
  } catch (error) {
    console.error('Search Videos Error:', error);
    throw error;
  }
};

export const getVideoById = async (videoId) => {
  try {
    const response = await api.get(`/videos/${videoId}`);
    return response.data;
  } catch (error) {
    console.error('Get Video Error:', error);
    throw error;
  }
};

export const getVideosForDrill = async (drillId) => {
  try {
    const response = await api.get(`/videos/for-drill/${drillId}`);
    return response.data;
  } catch (error) {
    console.error('Get Drill Videos Error:', error);
    throw error;
  }
};

export const getAllVideos = async (limit = 100, offset = 0) => {
  try {
    const response = await api.get(`/videos?limit=${limit}&offset=${offset}`);
    await cacheData(CACHE_KEYS.VIDEO_LIBRARY, response.data);
    return response.data;
  } catch (error) {
    console.error('Get All Videos Error:', error);
    const cachedData = await getCachedData(CACHE_KEYS.VIDEO_LIBRARY);
    if (cachedData) return cachedData;
    throw error;
  }
};

export const incrementVideoView = async (videoId) => {
  try {
    await api.post(`/videos/${videoId}/view`);
  } catch (error) {
    console.error('Increment View Error:', error);
    // Don't throw - view tracking is not critical
  }
};

/**
 * Cache Management
 */
const cacheData = async (key, data) => {
  try {
    await AsyncStorage.setItem(key, JSON.stringify({
      data,
      timestamp: Date.now(),
    }));
  } catch (error) {
    console.error('Cache Save Error:', error);
  }
};

const getCachedData = async (key, maxAge = 3600000) => { // 1 hour default
  try {
    const cached = await AsyncStorage.getItem(key);
    if (!cached) return null;

    const { data, timestamp } = JSON.parse(cached);
    
    // Check if cache is still valid
    if (Date.now() - timestamp < maxAge) {
      return data;
    }

    // Cache expired
    return null;
  } catch (error) {
    console.error('Cache Read Error:', error);
    return null;
  }
};

export const clearCache = async () => {
  try {
    await AsyncStorage.multiRemove(Object.values(CACHE_KEYS));
  } catch (error) {
    console.error('Cache Clear Error:', error);
  }
};

/**
 * Offline Support
 */
export const isOnline = async () => {
  try {
    const response = await api.get('/health', { timeout: 5000 });
    return response.status === 200;
  } catch (error) {
    return false;
  }
};

export default api;
