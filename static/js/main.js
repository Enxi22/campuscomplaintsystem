// Main JS entry point

// Image preview for complaint submit
document.addEventListener('DOMContentLoaded', () => {
    const fileInput = document.getElementById('complaint-image');
    const preview = document.getElementById('image-preview');
    const previewImg = document.getElementById('preview-img');
    const removeBtn = document.getElementById('remove-image');
    const uploadZone = document.getElementById('upload-zone');

    if (fileInput) {
        fileInput.addEventListener('change', (e) => {
            const file = e.target.files[0];
            if (file) {
                const reader = new FileReader();
                reader.onload = (e) => {
                    previewImg.src = e.target.result;
                    preview.classList.remove('d-none');
                };
                reader.readAsDataURL(file);
            }
        });
    }
    
    if (removeBtn) {
        removeBtn.addEventListener('click', () => {
            fileInput.value = '';
            preview.classList.add('d-none');
            previewImg.src = '';
        });
    }

    // Drag and drop support
    if (uploadZone) {
        ['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
            uploadZone.addEventListener(eventName, preventDefaults, false);
        });
        
        function preventDefaults(e) {
            e.preventDefault();
            e.stopPropagation();
        }
        
        ['dragenter', 'dragover'].forEach(eventName => {
            uploadZone.addEventListener(eventName, () => uploadZone.classList.add('drag-over'), false);
        });
        
        ['dragleave', 'drop'].forEach(eventName => {
            uploadZone.addEventListener(eventName, () => uploadZone.classList.remove('drag-over'), false);
        });
        
        uploadZone.addEventListener('drop', (e) => {
            const dt = e.dataTransfer;
            const files = dt.files;
            if (files.length) {
                fileInput.files = files;
                const event = new Event('change', { bubbles: true });
                fileInput.dispatchEvent(event);
            }
        }, false);
        
        uploadZone.addEventListener('click', () => fileInput.click());
    }
});

// Admin dashboard charts
document.addEventListener('DOMContentLoaded', () => {
    const categoryCtx = document.getElementById('categoryChart');
    const statusCtx = document.getElementById('statusChart');

    if (categoryCtx && statusCtx) {
        fetch('/admin/stats')
            .then(res => res.json())
            .then(data => {
                new Chart(categoryCtx, {
                    type: 'doughnut',
                    data: {
                        labels: Object.keys(data.categories),
                        datasets: [{
                            data: Object.values(data.categories),
                            backgroundColor: [
                                '#2563EB', '#059669', '#D97706', '#DC2626', '#0891B2',
                                '#7C3AED', '#DB2777', '#EA580C', '#16A34A', '#6B7280', '#9CA3AF'
                            ],
                            borderWidth: 0
                        }]
                    },
                    options: {
                        responsive: true,
                        maintainAspectRatio: false,
                        plugins: { legend: { position: 'bottom', labels: { padding: 16, font: { size: 12 } } } },
                        cutout: '65%'
                    }
                });

                new Chart(statusCtx, {
                    type: 'doughnut',
                    data: {
                        labels: Object.keys(data.statuses),
                        datasets: [{
                            data: Object.values(data.statuses),
                            backgroundColor: ['#9CA3AF', '#0891B2', '#D97706', '#059669', '#DC2626'],
                            borderWidth: 0
                        }]
                    },
                    options: {
                        responsive: true,
                        maintainAspectRatio: false,
                        plugins: { legend: { position: 'bottom', labels: { padding: 16, font: { size: 12 } } } },
                        cutout: '65%'
                    }
                });
            });
    }
});

// Form loading states
document.addEventListener('DOMContentLoaded', () => {
    const forms = document.querySelectorAll('form[data-loading]');
    forms.forEach(form => {
        form.addEventListener('submit', (e) => {
            const submitBtn = form.querySelector('button[type="submit"]');
            if (submitBtn) {
                submitBtn.disabled = true;
                const originalText = submitBtn.innerHTML;
                submitBtn.innerHTML = '<span class="spinner spinner-sm me-2"></span>Saving...';
                submitBtn.dataset.originalText = originalText;
            }
        });
    });
    
    // Add data-loading to all forms
    document.querySelectorAll('form').forEach(form => {
        form.setAttribute('data-loading', 'true');
    });
});