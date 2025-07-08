document.addEventListener('DOMContentLoaded', function () {
    const form = document.getElementById('upload-form');
    const loading = document.getElementById('loading');
    const result = document.getElementById('upload-result');
    const section = document.getElementById('upload-section');

    form.addEventListener('submit', function (e) {
        e.preventDefault();

        const formData = new FormData(form);
        const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;

        section.style.display = 'none';
        loading.style.display = 'block';

        fetch(form.action || window.location.href, {
            method: 'POST',
            headers: {
                'X-CSRFToken': csrfToken
            },
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            loading.style.display = 'none';
            if (data.success) {
                result.innerHTML = `<div class="alert alert-success">${data.message}</div>`;
            } else {
                result.innerHTML = `<div class="alert alert-danger">${data.message}</div>`;
            }
        })
        .catch(error => {
            loading.style.display = 'none';
            result.innerHTML = `<div class="alert alert-danger">Upload failed. Try again.</div>`;
        });
    });
});
