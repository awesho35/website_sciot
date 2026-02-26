/**
 * Le Sciøt Cial Club - API Client
 * Configuration et fonctions pour communiquer avec l'API Django
 */

const API_CONFIG = {
    // Modifier cette URL selon l'environnement
    baseUrl: 'http://localhost:8000/api',
    
    endpoints: {
        // Configuration
        config: '/config/',
        socialLinks: '/social-links/',
        contact: '/contact/',
        
        // Événements
        events: '/events/',
        eventsWeek: '/events/week/',
        eventsUpcoming: '/events/upcoming/',
        eventsCalendar: '/events/calendar/',
        eventsCategories: '/events/categories/',
        
        // Menu
        menuFull: '/menu/full/',
        menuCategories: '/menu/categories/',
        menuItems: '/menu/items/',
        drinkCategories: '/menu/drinks/categories/',
        drinkItems: '/menu/drinks/items/',
        specialMenus: '/menu/specials/',
        
        // Médias
        carousel: '/media/carousel/',
        heroBanner: '/media/hero/',
        
        // Pages
        pages: '/pages/pages/',
        faq: '/pages/faq/'
    }
};

/**
 * Client API
 */
const SciotAPI = {
    /**
     * Effectue une requête GET vers l'API
     */
    async get(endpoint) {
        try {
            const response = await fetch(`${API_CONFIG.baseUrl}${endpoint}`);
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            return await response.json();
        } catch (error) {
            console.error(`Erreur API (${endpoint}):`, error);
            return null;
        }
    },
    
    /**
     * Effectue une requête POST vers l'API
     */
    async post(endpoint, data) {
        try {
            const response = await fetch(`${API_CONFIG.baseUrl}${endpoint}`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(data)
            });
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            return await response.json();
        } catch (error) {
            console.error(`Erreur API POST (${endpoint}):`, error);
            return null;
        }
    },
    
    // === Configuration ===
    async getConfig() {
        return this.get(API_CONFIG.endpoints.config);
    },
    
    async getSocialLinks() {
        return this.get(API_CONFIG.endpoints.socialLinks);
    },
    
    async sendContactMessage(data) {
        return this.post(API_CONFIG.endpoints.contact, data);
    },
    
    // === Événements ===
    async getEvents() {
        return this.get(API_CONFIG.endpoints.events);
    },
    
    async getWeekEvents() {
        return this.get(API_CONFIG.endpoints.eventsWeek);
    },
    
    async getUpcomingEvents(limit = 50) {
        return this.get(`${API_CONFIG.endpoints.eventsUpcoming}?limit=${limit}`);
    },
    
    async getCalendarEvents(start, end) {
        let url = API_CONFIG.endpoints.eventsCalendar;
        if (start && end) {
            url += `?start=${start}&end=${end}`;
        }
        return this.get(url);
    },
    
    async getEventCategories() {
        return this.get(API_CONFIG.endpoints.eventsCategories);
    },
    
    async getEvent(id) {
        return this.get(`${API_CONFIG.endpoints.events}${id}/`);
    },
    
    // === Menu ===
    async getFullMenu() {
        return this.get(API_CONFIG.endpoints.menuFull);
    },
    
    async getMenuCategories() {
        return this.get(API_CONFIG.endpoints.menuCategories);
    },
    
    async getMenuItems() {
        return this.get(API_CONFIG.endpoints.menuItems);
    },
    
    async getDrinkCategories() {
        return this.get(API_CONFIG.endpoints.drinkCategories);
    },
    
    async getDrinkItems() {
        return this.get(API_CONFIG.endpoints.drinkItems);
    },
    
    async getSpecialMenus() {
        return this.get(API_CONFIG.endpoints.specialMenus);
    },
    
    // === Médias ===
    async getCarousel() {
        return this.get(API_CONFIG.endpoints.carousel);
    },
    
    async getHeroBanner() {
        return this.get(API_CONFIG.endpoints.heroBanner);
    },
    
    // === Pages ===
    async getPages() {
        return this.get(API_CONFIG.endpoints.pages);
    },
    
    async getFaq() {
        return this.get(API_CONFIG.endpoints.faq);
    }
};

/**
 * Utilitaires de formatage
 */
const SciotUtils = {
    /**
     * Formate une date pour l'affichage
     */
    formatDate(dateString) {
        // Ajouter T00:00:00 pour forcer l'interprétation en heure locale (pas UTC)
        const date = new Date(dateString.includes('T') ? dateString : dateString + 'T00:00:00');
        const days = ['DIM', 'LUN', 'MAR', 'MER', 'JEU', 'VEN', 'SAM'];
        const months = ['JANV', 'FÉV', 'MARS', 'AVR', 'MAI', 'JUIN', 'JUIL', 'AOÛT', 'SEPT', 'OCT', 'NOV', 'DÉC'];
        
        return {
            day: date.getDate(),
            dayName: days[date.getDay()],
            month: months[date.getMonth()],
            year: date.getFullYear(),
            formatted: `${days[date.getDay()]}. ${date.getDate()} ${months[date.getMonth()]}.`
        };
    },
    
    /**
     * Formate une heure
     */
    formatTime(timeString) {
        if (!timeString) return '';
        return timeString.substring(0, 5).replace(':', 'h');
    },
    
    /**
     * Formate un prix
     */
    formatPrice(price) {
        return parseFloat(price).toFixed(0) + '€';
    },
    
    /**
     * Génère le badge catégorie
     */
    getCategoryBadge(category) {
        if (!category) return '';
        const color = category.color || '#1a1a2e';
        return `<span class="badge" style="background-color: ${color}">${category.name}</span>`;
    },
    
    /**
     * Génère les badges diététiques
     */
    getDietaryBadges(item) {
        let badges = '';
        if (item.is_vegetarian) badges += '<span class="badge bg-success me-1">Végétarien</span>';
        if (item.is_vegan) badges += '<span class="badge bg-warning text-dark me-1">Végan</span>';
        if (item.is_gluten_free) badges += '<span class="badge bg-info me-1">Sans gluten</span>';
        return badges;
    }
};

// Export pour utilisation globale
window.SciotAPI = SciotAPI;
window.SciotUtils = SciotUtils;
window.API_CONFIG = API_CONFIG;
