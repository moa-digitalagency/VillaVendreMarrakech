async function uploadPDF(input) {
    const file = input.files[0];
    if (!file) return;

    const statusDiv = document.getElementById('pdfStatus');
    statusDiv.innerHTML = '<div class="pdf-loading">⏳ Analyse du PDF en cours... Cela peut prendre 30-60 secondes.</div>';

    const formData = new FormData();
    formData.append('pdf', file);

    try {
        const response = await fetch('/admin/upload-pdf', {
            method: 'POST',
            body: formData
        });

        const result = await response.json();

        if (result.success && result.data) {
            statusDiv.innerHTML = '<div class="pdf-success">✅ PDF analysé avec succès ! Les données ont été extraites.</div>';
            
            const data = result.data;
            document.querySelector('input[name="reference"]').value = data.reference || '';
            document.querySelector('input[name="title"]').value = data.title || '';
            document.querySelector('input[name="price"]').value = data.price || '';
            document.querySelector('input[name="location"]').value = data.location || '';
            document.querySelector('input[name="distance_city"]').value = data.distance_city || '';
            document.querySelector('textarea[name="description"]').value = data.description || '';
            document.querySelector('input[name="terrain_area"]').value = data.terrain_area || '';
            document.querySelector('input[name="built_area"]').value = data.built_area || '';
            document.querySelector('input[name="bedrooms"]').value = data.bedrooms || '';
            document.querySelector('input[name="pool_size"]').value = data.pool_size || '';
            document.querySelector('textarea[name="features"]').value = data.features || '';
            document.querySelector('textarea[name="equipment"]').value = data.equipment || '';
            document.querySelector('textarea[name="business_info"]').value = data.business_info || '';
            document.querySelector('textarea[name="investment_benefits"]').value = data.investment_benefits || '';
            document.querySelector('textarea[name="documents"]').value = data.documents || '';
            document.querySelector('input[name="contact_phone"]').value = data.contact_phone || '';
            document.querySelector('input[name="contact_email"]').value = data.contact_email || '';
            document.querySelector('input[name="contact_website"]').value = data.contact_website || '';

            document.getElementById('villaForm').scrollIntoView({ behavior: 'smooth' });
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

    const gallery = document.getElementById('imageGallery');
    
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
                    <img src="/static/uploads/${result.filename}" alt="Villa">
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
