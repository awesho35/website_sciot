/**
 * Script principal pour charger les éléments de layout et les données communes.
 */

/**
 * Charge le header et le footer depuis des fichiers externes.
 */
async function loadLayout() {
    const headerPlaceholder = document.getElementById('main-header');
    const footerPlaceholder = document.getElementById('main-footer');

    if (!headerPlaceholder || !footerPlaceholder) return;

    try {
        const [headerRes, footerRes] = await Promise.all([
            fetch('/header.html'),
            fetch('/footer.html')
        ]);

        headerPlaceholder.innerHTML = await headerRes.text();
        footerPlaceholder.innerHTML = await footerRes.text();

        // Compense la hauteur de la navbar qui est maintenant en "fixed-top"
        const navbar = headerPlaceholder.querySelector('.navbar');
        if (navbar) {
            const navbarHeight = navbar.offsetHeight;
            document.body.style.paddingTop = `${navbarHeight}px`;
            // Crée une variable CSS pour que d'autres éléments puissent connaître la hauteur de la navbar
            document.documentElement.style.setProperty('--navbar-height', `${navbarHeight}px`);
        }

        // Met en surbrillance le lien de navigation actif
        const currentPage = window.location.pathname.split('/').pop() || 'index.html';
        const navLinks = document.querySelectorAll('#main-header .nav-link');
        navLinks.forEach(link => {
            if (link.getAttribute('href') === currentPage) {
                link.classList.add('active');
            }
        });
    } catch (error) {
        console.error('Erreur lors du chargement du layout:', error);
    }
}

/**
 * Charge la configuration globale du site (ex: numéro de téléphone).
 */
async function loadSiteConfig() {
    try {
        const config = await SciotAPI.getConfig();
        if (!config) return;
        
        const phoneLink = document.querySelector('#main-footer a[href^="tel:"]');
        if (phoneLink && config.phone) {
            phoneLink.textContent = config.phone;
            phoneLink.href = 'tel:' + config.phone.replace(/\s/g, '');
        }
    } catch (error) {
        console.error('Erreur chargement config:', error);
    }
}

/**
 * Charge les liens des réseaux sociaux dans le header et le footer.
 */
async function loadSocialLinks() {
    try {
        const links = await SciotAPI.getSocialLinks() || [];
        if (links.length === 0) return;
        
        const navContainer = document.getElementById('nav-social-links');
        const footerContainer = document.getElementById('footer-social-links');

        const linksHtml = links.map(link => 
            `<a href="${link.url}" target="_blank" class="text-primary fs-4"><i class="bi bi-${link.platform}"></i></a>`
        ).join('');

        if (navContainer) navContainer.innerHTML = linksHtml;
        if (footerContainer) footerContainer.innerHTML = linksHtml;
    } catch (error) {
        console.error('Erreur chargement réseaux sociaux:', error);
    }
}

document.addEventListener('DOMContentLoaded', async () => {
    await loadLayout();
    await Promise.all([loadSiteConfig(), loadSocialLinks()]);
});

// Gère l'effet de parallaxe des vagues au scroll
window.addEventListener('scroll', () => {
    // Calcule un décalage pour la vague basé sur la position de scroll
    const waveOffset = window.scrollY * 0.2;
    // Met à jour la variable CSS utilisée par les vagues
    document.documentElement.style.setProperty('--wave-offset', `${waveOffset}px`);
}, { passive: true });