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

async function uploadPDF(input) {
    const file = input.files[0];
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
            
            const data = result.data;
            document.getElementById('pdf-reference').value = data.reference || '';
            document.getElementById('pdf-title').value = data.title || '';
            document.getElementById('pdf-price').value = data.price || '';
            document.getElementById('pdf-location').value = data.location || '';
            document.getElementById('pdf-distance_city').value = data.distance_city || '';
            document.getElementById('pdf-description').value = data.description || '';
            document.getElementById('pdf-terrain_area').value = data.terrain_area || '';
            document.getElementById('pdf-built_area').value = data.built_area || '';
            document.getElementById('pdf-bedrooms').value = data.bedrooms || '';
            document.getElementById('pdf-pool_size').value = data.pool_size || '';
            document.getElementById('pdf-features').value = data.features || '';
            document.getElementById('pdf-equipment').value = data.equipment || '';
            document.getElementById('pdf-business_info').value = data.business_info || '';
            document.getElementById('pdf-investment_benefits').value = data.investment_benefits || '';
            document.getElementById('pdf-documents').value = data.documents || '';
            document.getElementById('pdf-contact_phone').value = data.contact_phone || '';
            document.getElementById('pdf-contact_email').value = data.contact_email || '';
            document.getElementById('pdf-contact_website').value = data.contact_website || '';
        } else {
            statusDiv.innerHTML = `<div class="pdf-error">❌ Erreur: ${result.error || 'Impossible d\'extraire les données'}</div>`;
        }
    } catch (error) {
        statusDiv.innerHTML = `<div class="pdf-error">❌ Erreur réseau: ${error.message}</div>`;
    } finally {
        input.value = '';
    }
}

async function uploadImages(input) {
    const files = input.files;
    if (!files.length) return;

    const isPDFMode = document.getElementById('content-pdf').classList.contains('active');
    const gallery = isPDFMode ? document.getElementById('imageGalleryPDF') : document.getElementById('imageGalleryManual');
    
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
                    <button type="button" class="btn-delete" onclick="deleteImage('${result.filename}')">×</button>
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

async function deleteImage(filename) {
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

async function enhanceField(fieldId) {
    const field = document.getElementById(fieldId);
    const button = event.target;
    const originalText = field.value.trim();
    
    if (!originalText) {
        alert('Veuillez d\'abord saisir du texte à améliorer.');
        return;
    }

    button.disabled = true;
    button.textContent = '⏳';
    
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
        button.disabled = false;
        button.textContent = '✨ AI';
    }
}

document.getElementById('villaForm')?.addEventListener('submit', function(e) {
    const button = this.querySelector('.btn-save');
    button.textContent = '💾 Enregistrement...';
    button.disabled = true;
});

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

document.getElementById('resetModal')?.addEventListener('click', function(e) {
    if (e.target === this) {
        closeResetModal();
    }
});
