/**
 * API Service
 * Handles all API requests
 */

class APIService {
    constructor() {
        this.baseURL = CONFIG.API_BASE_URL;
    }

    getToken() {
        return localStorage.getItem(CONFIG.TOKEN_KEY);
    }

    getHeaders() {
        const headers = {
            'Content-Type': 'application/json'
        };

        const token = this.getToken();
        if (token) {
            headers['Authorization'] = `Bearer ${token}`;
        }

        return headers;
    }

    async request(endpoint, options = {}) {
        const url = `${this.baseURL}${endpoint}`;
        
        const config = {
            ...options,
            headers: this.getHeaders()
        };

        try {
            const response = await fetch(url, config);
            const data = await response.json();

            if (!response.ok) {
                throw new Error(data.error || 'Request failed');
            }

            return data;
        } catch (error) {
            console.error('API Error:', error);
            throw error;
        }
    }

    // Auth endpoints
    async login(username, password) {
        return this.request('/api/auth/login', {
            method: 'POST',
            body: JSON.stringify({ username, password })
        });
    }

    async register(userData) {
        return this.request('/api/auth/register', {
            method: 'POST',
            body: JSON.stringify(userData)
        });
    }

    async getProfile() {
        return this.request('/api/auth/me');
    }

    // Persons endpoints
    async getPersons(params = {}) {
        const queryString = new URLSearchParams(params).toString();
        return this.request(`/api/persons?${queryString}`);
    }

    async getPerson(id) {
        return this.request(`/api/persons/${id}`);
    }

    async createPerson(personData) {
        return this.request('/api/persons', {
            method: 'POST',
            body: JSON.stringify(personData)
        });
    }

    async updatePerson(id, personData) {
        return this.request(`/api/persons/${id}`, {
            method: 'PUT',
            body: JSON.stringify(personData)
        });
    }

    async deletePerson(id) {
        return this.request(`/api/persons/${id}`, {
            method: 'DELETE'
        });
    }

    async addPersonEncoding(id, encoding, imageUrl) {
        return this.request(`/api/persons/${id}/encodings`, {
            method: 'POST',
            body: JSON.stringify({ encoding, imageUrl })
        });
    }

    async updatePersonStatus(id, status) {
        return this.request(`/api/persons/updateStatus/${id}`, {
            method: 'PUT',
            body: JSON.stringify({ status })
        });
    }

    // Reports endpoints
    async getReports(params = {}) {
        const queryString = new URLSearchParams(params).toString();
        return this.request(`/api/reports?${queryString}`);
    }

    async getReport(id) {
        return this.request(`/api/reports/${id}`);
    }

    async verifyReport(id, status) {
        return this.request(`/api/reports/${id}/verify`, {
            method: 'PATCH',
            body: JSON.stringify({ verificationStatus: status })
        });
    }

    async getReportStats(params = {}) {
        const queryString = new URLSearchParams(params).toString();
        return this.request(`/api/reports/stats/summary?${queryString}`);
    }

    // Recognition endpoint
    async recognizeFace(encoding, metadata) {
        return this.request('/api/recognize', {
            method: 'POST',
            body: JSON.stringify({ encoding, metadata })
        });
    }
}

// Create global instance
const api = new APIService();
