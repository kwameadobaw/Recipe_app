// Theme switcher functionality
document.addEventListener('DOMContentLoaded', function() {
    // Check for saved theme preference or use preferred color scheme
    const savedTheme = localStorage.getItem('theme');
    const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
    
    // Set initial theme
    if (savedTheme === 'dark' || (!savedTheme && prefersDark)) {
        document.documentElement.setAttribute('data-bs-theme', 'dark');
        document.getElementById('theme-toggle-icon').classList.replace('fa-moon', 'fa-sun');
    } else {
        document.documentElement.setAttribute('data-bs-theme', 'light');
        document.getElementById('theme-toggle-icon').classList.replace('fa-sun', 'fa-moon');
    }
    
    // Theme toggle button functionality
    document.getElementById('theme-toggle').addEventListener('click', function() {
        const currentTheme = document.documentElement.getAttribute('data-bs-theme');
        const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
        const icon = document.getElementById('theme-toggle-icon');
        
        // Update theme
        document.documentElement.setAttribute('data-bs-theme', newTheme);
        
        // Update icon
        if (newTheme === 'dark') {
            icon.classList.replace('fa-moon', 'fa-sun');
        } else {
            icon.classList.replace('fa-sun', 'fa-moon');
        }
        
        // Save preference
        localStorage.setItem('theme', newTheme);
    });
});