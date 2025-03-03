/**
 * Kelio Jobs - Main JavaScript
 * Gère les fonctionnalités de l'interface utilisateur pour l'application Kelio Jobs
 */

document.addEventListener('DOMContentLoaded', function () {
  // Éléments DOM
  const searchInput = document.getElementById('searchInput');
  const locationFilter = document.getElementById('locationFilter');
  const sortFilter = document.getElementById('sortFilter');
  const jobItems = document.querySelectorAll('.job-item');
  const jobsContainer = document.getElementById('jobsContainer');
  const runScraperBtn = document.getElementById('runScraperBtn');
  const clearJobsBtn = document.getElementById('clearJobsBtn');
  const toastContainer = document.querySelector('.toast-container');
  const navLinks = document.querySelectorAll('.nav-link');
  const backToTopBtn = document.getElementById('backToTopBtn');
  const themeToggle = document.getElementById('themeToggle');

  /**
   * Gestion du thème (clair/sombre)
   */
  if (themeToggle) {
    // Vérifier si un thème est déjà enregistré
    const currentTheme = localStorage.getItem('theme') || 'light';
    document.documentElement.setAttribute('data-theme', currentTheme);
    
    // Gestionnaire d'événement pour le bouton de changement de thème
    themeToggle.addEventListener('click', function() {
      const currentTheme = document.documentElement.getAttribute('data-theme');
      const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
      
      // Mettre à jour l'attribut et enregistrer la préférence
      document.documentElement.setAttribute('data-theme', newTheme);
      localStorage.setItem('theme', newTheme);
      
      // Afficher une notification
      showToast(`Mode ${newTheme === 'dark' ? 'sombre' : 'clair'} activé`, 'success');
    });
  }

  /**
   * Gestion du bouton "Retour en haut"
   */
  if (backToTopBtn) {
    // Afficher/masquer le bouton en fonction du défilement
    window.addEventListener('scroll', function() {
      if (window.pageYOffset > 300) {
        backToTopBtn.classList.add('visible');
      } else {
        backToTopBtn.classList.remove('visible');
      }
    });

    // Action du bouton
    backToTopBtn.addEventListener('click', function() {
      window.scrollTo({
        top: 0,
        behavior: 'smooth'
      });
    });
  }

  /**
   * Défilement fluide pour les liens de navigation
   */
  navLinks.forEach(link => {
    link.addEventListener('click', function(e) {
      // Ne pas appliquer aux liens externes
      if (this.getAttribute('target') === '_blank') return;
      
      const href = this.getAttribute('href');
      
      // Si c'est un lien d'ancrage
      if (href.startsWith('#') && href.length > 1) {
        e.preventDefault();
        const targetElement = document.querySelector(href);
        
        if (targetElement) {
          window.scrollTo({
            top: targetElement.offsetTop - 80, // Offset pour la navbar
            behavior: 'smooth'
          });
        }
      }
    });
  });

  /**
   * Trie les offres d'emploi en fonction du critère sélectionné
   */
  function sortJobs() {
    const sortValue = sortFilter.value;
    const jobItemsArray = Array.from(jobItems);
    
    jobItemsArray.sort((a, b) => {
      switch (sortValue) {
        case 'date-desc':
          return compareDates(b.getAttribute('data-date'), a.getAttribute('data-date'));
        case 'date-asc':
          return compareDates(a.getAttribute('data-date'), b.getAttribute('data-date'));
        case 'title-asc':
          return a.getAttribute('data-title').localeCompare(b.getAttribute('data-title'));
        case 'title-desc':
          return b.getAttribute('data-title').localeCompare(a.getAttribute('data-title'));
        default:
          return 0;
      }
    });
    
    // Réorganiser les éléments dans le DOM
    jobItemsArray.forEach(item => {
      jobsContainer.appendChild(item);
    });
  }
  
  /**
   * Compare deux dates pour le tri
   * @param {string} dateA - Première date à comparer
   * @param {string} dateB - Seconde date à comparer
   * @returns {number} - Résultat de la comparaison
   */
  function compareDates(dateA, dateB) {
    // Si une des dates est vide, la placer à la fin
    if (!dateA) return 1;
    if (!dateB) return -1;
    
    // Extraire la première partie de la date (avant l'espace)
    const cleanDateA = dateA.split(' ')[0];
    const cleanDateB = dateB.split(' ')[0];
    
    // Convertir au format français (JJ/MM/AAAA) en format Date
    const partsA = cleanDateA.split('/');
    const partsB = cleanDateB.split('/');
    
    // Si le format n'est pas valide, utiliser la comparaison de chaînes
    if (partsA.length !== 3 || partsB.length !== 3) {
      return cleanDateA.localeCompare(cleanDateB);
    }
    
    // Créer des objets Date (format MM/JJ/AAAA pour JavaScript)
    const dateObjA = new Date(`${partsA[1]}/${partsA[0]}/${partsA[2]}`);
    const dateObjB = new Date(`${partsB[1]}/${partsB[0]}/${partsB[2]}`);
    
    // Comparer les objets Date
    return dateObjA - dateObjB;
  }

  /**
   * Filtre les offres d'emploi en fonction des critères de recherche
   */
  function filterJobs() {
    const searchValue = searchInput.value.toLowerCase();
    const locationValue = locationFilter.value;
    const resultsCount = document.getElementById('resultsCount');
    let visibleCount = 0;

    jobItems.forEach(item => {
      const title = item.getAttribute('data-title').toLowerCase();
      const location = item.getAttribute('data-location');

      const matchesSearch = title.includes(searchValue);
      const matchesLocation = !locationValue || location === locationValue;

      if (matchesSearch && matchesLocation) {
        item.style.display = '';
        visibleCount++;
      } else {
        item.style.display = 'none';
      }
    });
    
    // Mettre à jour le compteur de résultats
    if (resultsCount) {
      resultsCount.textContent = visibleCount;
    }
    
    // Appliquer le tri après le filtrage
    sortJobs();
  }

  /**
   * Affiche une notification toast avancée avec des options supplémentaires
   * @param {Object} options - Options de configuration
   * @param {string} options.message - Le message à afficher
   * @param {string} options.type - Le type de notification ('success', 'error', 'info', 'warning')
   * @param {number} options.duration - Durée d'affichage en ms (défaut: 5000)
   * @param {boolean} options.dismissible - Si la notification peut être fermée (défaut: true)
   */
  function showAdvancedToast(options) {
    const {
      message,
      type = 'success',
      duration = 5000,
      dismissible = true
    } = options;

    // Déterminer l'icône en fonction du type
    let icon, color;
    switch (type) {
      case 'success':
        icon = 'check-circle';
        color = '#10b981';
        break;
      case 'error':
        icon = 'exclamation-circle';
        color = '#ef4444';
        break;
      case 'info':
        icon = 'info-circle';
        color = '#3b82f6';
        break;
      case 'warning':
        icon = 'exclamation-triangle';
        color = '#f59e0b';
        break;
      default:
        icon = 'bell';
        color = '#6b7280';
    }

    const toast = document.createElement('div');
    toast.classList.add('toast');
    toast.classList.add(type);

    // Créer le contenu HTML simplifié sans titre
    toast.innerHTML = `
      <div class="toast-content">
        <i class="fas fa-${icon}" style="color: ${color};"></i>
        <div class="toast-message">${message}</div>
        ${dismissible ? `
          <button type="button" class="btn-close" aria-label="Fermer" onclick="this.parentNode.parentNode.remove()">
            <i class="fas fa-times"></i>
          </button>
        ` : ''}
      </div>
      <div class="toast-progress"></div>
    `;

    // Ajouter au conteneur
    toastContainer.appendChild(toast);

    // Afficher avec animation
    setTimeout(() => {
      toast.classList.add('show');
    }, 10);

    // Supprimer automatiquement après la durée spécifiée
    if (duration !== 0) {
      // Ajuster l'animation de la barre de progression
      const progressBar = toast.querySelector('.toast-progress');
      if (progressBar) {
        progressBar.style.animation = `toastProgress ${duration/1000}s linear forwards`;
      }

      setTimeout(() => {
        toast.classList.remove('show');
        setTimeout(() => {
          toast.remove();
        }, 400);
      }, duration);
    }

    return toast;
  }

  // Fonctions d'aide pour les notifications
  function showSuccessToast(message) {
    return showAdvancedToast({
      message,
      type: 'success'
    });
  }

  function showErrorToast(message) {
    return showAdvancedToast({
      message,
      type: 'error'
    });
  }

  function showInfoToast(message) {
    return showAdvancedToast({
      message,
      type: 'info',
      duration: 7000
    });
  }

  function showWarningToast(message) {
    return showAdvancedToast({
      message,
      type: 'warning'
    });
  }

  /**
   * Affiche une notification toast (version compatible avec l'ancienne implémentation)
   * @param {string} message - Le message à afficher
   * @param {string} type - Le type de notification ('success' ou 'error')
   */
  function showToast(message, type = 'success') {
    return showAdvancedToast({
      message,
      type
    });
  }

  /**
   * Gère l'appel API avec indicateur de chargement
   * @param {HTMLElement} button - Le bouton qui a déclenché l'action
   * @param {string} url - L'URL de l'API à appeler
   * @param {string} loadingText - Le texte à afficher pendant le chargement
   * @param {Function} successCallback - Fonction à exécuter en cas de succès
   */
  function handleApiCall(button, url, loadingText, successCallback) {
    // Sauvegarder le contenu original du bouton
    const originalContent = button.innerHTML;
    
    // Afficher l'indicateur de chargement
    button.innerHTML = `<span class="loader" style="display: inline-block;"></span> ${loadingText}`;
    button.disabled = true;

    // Afficher une notification de chargement
    const loadingToast = showAdvancedToast({
      message: `${loadingText} Veuillez patienter...`,
      type: 'info',
      duration: 0 // Ne pas fermer automatiquement
    });

    // Appeler l'API
    fetch(url, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      }
    })
      .then(response => {
        if (!response.ok) {
          throw new Error(`HTTP error! Status: ${response.status}`);
        }
        return response.json();
      })
      .then(data => {
        // Fermer la notification de chargement
        if (loadingToast) {
          loadingToast.classList.remove('show');
          setTimeout(() => loadingToast.remove(), 400);
        }

        if (data.success) {
          showSuccessToast(data.message);
          if (successCallback) {
            successCallback(data);
          }
        } else {
          showErrorToast(data.message || 'Une erreur s\'est produite.');
        }
      })
      .catch(error => {
        console.error('Error:', error);
        
        // Fermer la notification de chargement
        if (loadingToast) {
          loadingToast.classList.remove('show');
          setTimeout(() => loadingToast.remove(), 400);
        }

        showErrorToast('Une erreur s\'est produite lors de l\'opération. Veuillez réessayer plus tard.');
      })
      .finally(() => {
        // Restaurer le bouton
        button.innerHTML = originalContent;
        button.disabled = false;
      });
  }

  // Gestionnaire d'événement pour le bouton d'exécution du scraper
  if (runScraperBtn) {
    runScraperBtn.addEventListener('click', function () {
      handleApiCall(
        this, 
        '/run-scraper', 
        'Actualisation...', 
        () => {
          // Recharger la page pour afficher les nouvelles offres
          setTimeout(() => {
            window.location.reload();
          }, 1000);
        }
      );
    });
  }

  // Gestionnaire d'événement pour le bouton de suppression des offres
  if (clearJobsBtn) {
    clearJobsBtn.addEventListener('click', function () {
      if (!confirm('Êtes-vous sûr de vouloir supprimer toutes les offres d\'emploi ?')) {
        return;
      }

      handleApiCall(
        this, 
        '/clear-jobs', 
        'Suppression...', 
        () => {
          // Recharger la page pour mettre à jour l'interface
          setTimeout(() => {
            window.location.reload();
          }, 1000);
        }
      );
    });
  }

  // Ajouter les écouteurs d'événements pour la recherche, le filtrage et le tri
  if (searchInput) {
    searchInput.addEventListener('input', filterJobs);
  }
  
  if (locationFilter) {
    locationFilter.addEventListener('change', filterJobs);
  }
  
  if (sortFilter) {
    sortFilter.addEventListener('change', filterJobs);
  }
  
  // Appliquer le tri initial
  if (sortFilter && jobsContainer) {
    sortJobs();
  }
}); 