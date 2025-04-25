// helper: handle the common flow for both URL- and Name-based downloads
async function combineSongs(postUrl, payload) {
  const status = document.getElementById('status');
  status.textContent = 'Processing...';

  try {
    // kick off server processing
    const res = await fetch(postUrl, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    });
    const json = await res.json();
    if (!res.ok) {
      status.textContent = `Error: ${json.error}`;
      return;
    }

    status.textContent = 'Processing complete! Preparing download link…';

    // fetch the combined file
    const fileRes = await fetch('/download');
    const blob = await fileRes.blob();
    const blobUrl = window.URL.createObjectURL(blob);

    // configure the existing link
    const dlLink = document.getElementById('download-link');
    dlLink.href = blobUrl;
    dlLink.download = 'combined.mp3';
    dlLink.style.display = 'inline-block';

    // when the user clicks it, we revoke the URL afterwards
    dlLink.addEventListener('click', () => {
      // slight delay so the download has started
      setTimeout(() => window.URL.revokeObjectURL(blobUrl), 1000);
    }, { once: true });

    status.textContent = 'Ready! Click the download button below.';
  } catch (err) {
    status.textContent = `Error: ${err.message}`;
  }
}

// URL-based handler
document.getElementById('download_url_btn').addEventListener('click', () => {
  const dlLink = document.getElementById('download-link');
  dlLink.style.display = 'none'; // hide the link until we have a valid one
  const song1 = document.getElementById('song1_url').value.trim();
  const song2 = document.getElementById('song2_url').value.trim();
  const status = document.getElementById('status');

  if (!song1 || !song2) {
    status.textContent = 'Please enter both URLs';
    return;
  }
  combineSongs('/download_by_url', { song1_url: song1, song2_url: song2 });
});

// Name-based handler
document.getElementById('download_name_btn').addEventListener('click', () => {
  const dlLink = document.getElementById('download-link');
  dlLink.style.display = 'none'; // hide the link until we have a valid one
  const song1 = document.getElementById('song1_name').value.trim();
  const song2 = document.getElementById('song2_name').value.trim();
  const status = document.getElementById('status');

  if (!song1 || !song2) {
    status.textContent = 'Please enter both song names';
    return;
  }
  combineSongs('/download_by_name', { song1_name: song1, song2_name: song2 });
});
