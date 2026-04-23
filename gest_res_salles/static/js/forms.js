// static/js/style-forms.js
document.addEventListener("DOMContentLoaded", function() {
    // Sélectionne tous les types d'input sauf les boutons et checkboxes
    const inputs = document.querySelectorAll('input:not([type="submit"]):not([type="checkbox"]):not([type="radio"]), select, textarea');
    
    inputs.forEach(el => {
        el.classList.add('form-control');
        el.classList.add('mb-2'); // Ajoute un petit espace en bas de chaque champ
    });

    // Optionnel : Styliser spécifiquement le bouton submit
    const submitBtn = document.querySelector('button[type="submit"]');
    if (submitBtn) {
        submitBtn.classList.add('shadow-sm');
    }
});