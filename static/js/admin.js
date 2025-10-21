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
