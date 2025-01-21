$(document).ready(function () {
    $('#start-camera').click(async () => {
        $('#result').html('<p>Starting camera...</p>');
        try {
            const response = await fetch('/start_camera', { method: 'POST' });
            const data = await response.json();
            $('#result').html(`<p class="text-success">${data.message}</p>`);
        } catch (error) {
            $('#result').html('<p class="text-danger">Failed to start the camera.</p>');
        }
    });

    $('#stop-camera').click(async () => {
        $('#result').html('<p>Stopping camera...</p>');
        try {
            const response = await fetch('/stop_camera', { method: 'POST' });
            const data = await response.json();
            $('#result').html(`<p class="text-success">${data.message}</p>`);
        } catch (error) {
            $('#result').html('<p class="text-danger">Failed to stop the camera.</p>');
        }
    });
});
