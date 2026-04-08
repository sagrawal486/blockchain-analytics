import axios from 'axios';

const API = axios.create({
  baseURL: import.meta.env.VITE_API_URL || 'http://localhost:8000',
  headers: { 'Content-Type': 'application/json' }
});

// ─── Auto attach token to every request ───────────────
API.interceptors.request.use((config) => {
  const token = localStorage.getItem('token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// ─── Auto redirect to login on 401 ────────────────────
API.interceptors.response.use(
  response => response,
  error => {
    if (error.response?.status === 401) {
      localStorage.removeItem('token');
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

export const authAPI = {
  login   : (username, password) => {
    const form = new FormData();
    form.append('username', username);
    form.append('password', password);
    return API.post('/auth/login', form, {
      headers: { 'Content-Type': 'multipart/form-data' }
    });
  },
  me      : () => API.get('/auth/me'),
};

export const walletAPI = {
  getAll  : ()      => API.get('/wallets'),
  add     : (data)  => API.post('/wallets', data),
  delete  : (addr)  => API.delete(`/wallets/${addr}`),
};

export const transactionAPI = {
  getAll      : (address, limit=25, offset=0) =>
                  API.get(`/transactions/${address}?limit=${limit}&offset=${offset}`),
  getSummary  : (address) => API.get(`/transactions/${address}/summary`),
};

export const syncAPI = {
  trigger     : (address) => API.post(`/sync/${address}`),
  getStatus   : (address) => API.get(`/sync/${address}/status`),
};
