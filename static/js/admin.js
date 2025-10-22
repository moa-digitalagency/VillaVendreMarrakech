/*
Logique JavaScript Admin - Villa à Vendre Marrakech

Script pour gérer toutes les interactions du panneau d'administration.
Gère le changement de mode, upload PDF/images, extraction IA, amélioration de texte.

Fonctionnalités principales:
1. Changement de mode (PDF vs Formulaire)
2. Upload et extraction PDF via IA (Claude 3.5 Sonnet)
3. Upload et optimisation d'images (JPEG)
4. Amélioration de texte via IA (Mistral Large) pour chaque champ
5. Enregistrement des données de villa
6. Gestion de la galerie d'images (ajout, suppression)
7. Réinitialisation complète de la base de données

API Endpoints utilisés:
- POST /admin/upload-pdf : Upload PDF et extraction IA (60-90s)
- POST /admin/upload : Upload et optimisation d'image
- POST /admin/save : Enregistrement de la villa (mode PDF ou formulaire)
- POST /api/enhance : Amélioration de texte via IA
- POST /admin/delete-image/<filename> : Suppression d'image
- POST /admin/reset : Réinitialisation complète

Variables globales:
- window.pdfExtractedData : Données extraites du PDF par l'IA

Développé par: MOA Digital Agency LLC
Développeur: Aisance KALONJI
Email: moa@myoneart.com
Web: www.myoneart.com
*/

// ========== CHANGEMENT DE MODE (PDF vs FORMULAIRE) ==========
document.getElementById('mode-pdf')?.addEventListener('click', () => switchMode('pdf'));
document.getElementById('mode-manual')?.addEventListener('click', () => switchMode('manual'));

function switchMode(mode) {
    const pdfOption = document.getElementById('mode-pdf');
    const manualOption = document.getElementById('mode-manual');
    const pdfContent = document.getElementById('content-pdf');
    const manualContent = document.getElementById('content-manual');
    
    if (mode === 'pdf') {
        pdfOption.classList.add('active');
        manualOption.classList.remove('active');
        pdfContent.classList.add('active');
        manualContent.classList.remove('active');
    } else {
        manualOption.classList.add('active');
        pdfOption.classList.remove('active');
        manualContent.classList.add('active');
        pdfContent.classList.remove('active');
    }
}

// PDF Upload
document.getElementById('pdfUpload')?.addEventListener('change', async function() {
    const file = this.files[0];
    if (!file) return;

    const statusDiv = document.getElementById('pdfStatus');
    statusDiv.innerHTML = '<div class="pdf-loading">⏳ Analyse du PDF en cours... Cela peut prendre 60-90 secondes (Claude 3.5 Sonnet).</div>';

    const formData = new FormData();
    formData.append('pdf', file);

    try {
        const response = await fetch('/admin/upload-pdf', {
            method: 'POST',
            body: formData
        });

        const result = await response.json();

        if (result.success && result.data) {
            statusDiv.innerHTML = '<div class="pdf-success">✅ PDF analysé avec succès ! Les données ont été extraites. Ajoutez maintenant les photos puis cliquez sur Enregistrer.</div>';
            
            // Stocker les données extraites temporairement
            window.pdfExtractedData = result.data;
        } else {
            statusDiv.innerHTML = `<div class="pdf-error">❌ Erreur: ${result.error || 'Impossible d\'extraire les données'}</div>`;
        }
    } catch (error) {
        statusDiv.innerHTML = `<div class="pdf-error">❌ Erreur réseau: ${error.message}</div>`;
    } finally {
        this.value = '';
    }
});

// Save button for PDF mode
document.getElementById('btn-save-pdf')?.addEventListener('click', async function() {
    if (!window.pdfExtractedData) {
        alert('Veuillez d\'abord uploader et analyser un PDF.');
        return;
    }

    this.textContent = '💾 Enregistrement...';
    this.disabled = true;

    try {
        const formData = new FormData();
        const data = window.pdfExtractedData;
        
        for (let key in data) {
            if (data[key]) {
                formData.append(key, data[key]);
            }
        }

        const response = await fetch('/admin/save', {
            method: 'POST',
            body: formData
        });

        const result = await response.json();

        if (result.success) {
            alert('✅ ' + result.message);
            window.location.reload();
        } else {
            alert('❌ Erreur: ' + result.error);
        }
    } catch (error) {
        alert('❌ Erreur: ' + error.message);
    } finally {
        this.textContent = '💾 Enregistrer la Villa';
        this.disabled = false;
    }
});

// Image uploads
document.getElementById('imageUploadPDF')?.addEventListener('change', function() {
    uploadImages(this, 'imageGalleryPDF');
});

document.getElementById('imageUploadManual')?.addEventListener('change', function() {
    uploadImages(this, 'imageGalleryManual');
});

async function uploadImages(input, galleryId) {
    const files = input.files;
    if (!files.length) return;

    const gallery = document.getElementById(galleryId);
    
    for (let file of files) {
        const formData = new FormData();
        formData.append('image', file);

        try {
            const response = await fetch('/admin/upload', {
                method: 'POST',
                body: formData
            });

            const result = await response.json();
            
            if (result.success) {
                const div = document.createElement('div');
                div.className = 'image-item';
                div.dataset.filename = result.filename;
                div.innerHTML = `
                    <img src="/static/uploads/${result.filename}" alt="Villa Marrakech">
                    <button type="button" class="btn-delete" data-filename="${result.filename}">×</button>
                `;
                gallery.appendChild(div);
            } else {
                alert('Erreur lors de l\'upload: ' + result.error);
            }
        } catch (error) {
            alert('Erreur réseau: ' + error.message);
        }
    }
    
    input.value = '';
}

// Delete image - Event delegation
document.addEventListener('click', async function(e) {
    if (e.target.classList.contains('btn-delete')) {
        const filename = e.target.dataset.filename || e.target.closest('.image-item')?.dataset.filename;
        if (!filename) return;

        if (!confirm('Voulez-vous vraiment supprimer cette image ?')) {
            return;
        }

        try {
            const response = await fetch(`/admin/delete-image/${filename}`, {
                method: 'POST'
            });

            const result = await response.json();
            
            if (result.success) {
                const item = document.querySelector(`[data-filename="${filename}"]`);
                if (item) {
                    item.remove();
                }
            } else {
                alert('Erreur lors de la suppression: ' + result.error);
            }
        } catch (error) {
            alert('Erreur réseau: ' + error.message);
        }
    }
});

// AI enhancement buttons
document.querySelectorAll('.btn-ai').forEach(button => {
    button.addEventListener('click', async function() {
        const fieldId = this.dataset.field;
        const field = document.getElementById(fieldId);
        const originalText = field.value.trim();
        
        if (!originalText) {
            alert('Veuillez d\'abord saisir du texte à améliorer.');
            return;
        }

        this.disabled = true;
        this.textContent = '⏳';
        
        try {
            const response = await fetch('/api/enhance', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    text: originalText,
                    field: fieldId
                })
            });

            const result = await response.json();
            
            if (result.enhanced) {
                if (confirm('Texte amélioré par l\'IA. Voulez-vous le remplacer ?\n\nNouveau texte:\n' + result.enhanced)) {
                    field.value = result.enhanced;
                }
            }
        } catch (error) {
            alert('Erreur lors de l\'amélioration: ' + error.message);
        } finally {
            this.disabled = false;
            this.textContent = '✨ AI';
        }
    });
});

// Form submit
document.getElementById('villaForm')?.addEventListener('submit', function(e) {
    const button = this.querySelector('.btn-save');
    button.textContent = '💾 Enregistrement...';
    button.disabled = true;
});

// Reset modal
document.getElementById('btn-reset')?.addEventListener('click', openResetModal);
document.getElementById('btn-reset-manual')?.addEventListener('click', openResetModal);
document.getElementById('cancel-reset-btn')?.addEventListener('click', closeResetModal);
document.getElementById('confirm-reset-btn')?.addEventListener('click', confirmReset);

function openResetModal() {
    document.getElementById('resetModal').classList.add('active');
    document.getElementById('confirmInput').value = '';
    document.getElementById('confirmInput').focus();
}

function closeResetModal() {
    document.getElementById('resetModal').classList.remove('active');
}

async function confirmReset() {
    const confirmInput = document.getElementById('confirmInput');
    const confirmation = confirmInput.value.trim();
    
    if (confirmation !== 'SUPPRIMER') {
        alert('Veuillez taper exactement "SUPPRIMER" pour confirmer.');
        return;
    }
    
    const formData = new FormData();
    formData.append('confirmation', confirmation);
    
    try {
        const response = await fetch('/admin/reset', {
            method: 'POST',
            body: formData
        });
        
        const result = await response.json();
        
        if (result.success) {
            alert('✅ ' + result.message);
            window.location.reload();
        } else {
            alert('❌ Erreur: ' + result.error);
        }
    } catch (error) {
        alert('❌ Erreur réseau: ' + error.message);
    } finally {
        closeResetModal();
    }
}

// Close modal on background click
document.getElementById('resetModal')?.addEventListener('click', function(e) {
    if (e.target === this) {
        closeResetModal();
    }
});
