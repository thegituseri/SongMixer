document.getElementById('download_url_btn').addEventListener('click', async () => {
    const song1_url = document.getElementById('song1_url').value;
    const song2_url = document.getElementById('song2_url').value;
    const status = document.getElementById('status');

    if (!song1_url || !song2_url) {
        status.textContent = 'Please enter both URLs';
        return;
    }

    status.textContent = 'Processing...';

    try {
        const response = await fetch('/download_by_url', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ song1_url, song2_url })
        });

        if (!response.ok) {
            const error = await response.json();
            status.textContent = `Error: ${error.error}`;
            return;
        }

        // Trigger file download
        const blob = await response.blob();
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = 'combined.mp3';
        document.body.appendChild(a);
        a.click();
        a.remove();
        window.URL.revokeObjectURL(url);

        status.textContent = 'Download complete!';
    } catch (error) {
        status.textContent = `Error: ${error.message}`;
    }
});

document.getElementById('download_name_btn').addEventListener('click', async () => {
    const song1_name = document.getElementById('song1_name').value;
    const song2_name = document.getElementById('song2_name').value;
    const status = document.getElementById('status');

    if (!song1_name || !song2_name) {
        status.textContent = 'Please enter both song names';
        return;
    }

    status.textContent = 'Processing...';

    try {
        const response = await fetch('/download_by_name', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ song1_name, song2_name })
        });

        if (!response.ok) {
            const error = await response.json();
            status.textContent = `Error: ${error.error}`;
            return;
        }

        // Trigger file download
        const blob = await response.blob();
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = 'combined.mp3';
        document.body.appendChild(a);
        a.click();
        a.remove();
        window.URL.revokeObjectURL(url);

        status.textContent = 'Download complete!';
    } catch (error) {
        status.textContent = `Error: ${error.message}`;
    }
});

