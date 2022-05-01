import axios from 'axios';
import constants from '@/utils/constants';

const API_URL = process.env.VUE_APP_API_URL || constants.DEFAULT_API_URL;

const session = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

session.interceptors.request.use((config) => {
  const token = localStorage.getItem(constants.TOKEN_STORAGE_KEY);
  config.headers.Authorization = token ? `Token ${token}` : '';
  return config;
});

export default session;
