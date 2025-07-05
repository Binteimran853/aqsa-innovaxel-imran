
function redirectToOriginal() {
    const shortCode = document.getElementById("redirectCode").value.trim();
    const msg = document.getElementById("redirectMsg");

    if (!shortCode) {
        msg.textContent = "Please enter a short code.";
        msg.style.color = "red";
        return;
    }

    fetch(`http://localhost:8000/shorten/${shortCode}/`)
        .then(response => {
            if (!response.ok) {
                throw new Error("Short URL not found.");
            }
            return response.json();
        })
        .then(data => {
            const originalUrl = data.url;
            msg.textContent = "Redirecting...";
            msg.style.color = "green";

            // Redirect user to original URL
            window.location.href = originalUrl;
        })
        .catch(error => {
            msg.textContent = error.message;
            msg.style.color = "red";
        });
}








function updateShortURL() {
    const shortCode = document.getElementById("updateCode").value.trim();
    const newUrl = document.getElementById("newUrl").value.trim();
    const msg = document.getElementById("updateMsg");
    const csrftoken = getCookie('csrftoken'); // already defined above

    if (!shortCode || !newUrl) {
        msg.textContent = "Both fields are required.";
        msg.style.color = "red";
        return;
    }

    fetch(`http://localhost:8000/shorten/${shortCode}/update/`, {
        method: 'PUT',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken,
        },
        body: JSON.stringify({ url: newUrl })
    })
    .then(response => {
        if (response.status === 200) {
            return response.json();
        } else if (response.status === 404) {
            throw new Error("Short code not found.");
        } else if (response.status === 400) {
            throw new Error("Invalid URL or request.");
        } else {
            throw new Error("Something went wrong.");
        }
    })
    .then(data => {
        msg.innerHTML = `<span style="color:green;">Updated successfully:</span><br>
                         <strong>Short Code:</strong> ${data.shortCode}<br>
                         <strong>New URL:</strong> <a href="${data.url}" target="_blank">${data.url}</a>`;
    })
    .catch(error => {
        msg.innerHTML = `<span style="color:red;">${error.message}</span>`;
    });
}





function getStats() {
    const shortCode = document.getElementById("statsCode").value;
    const statsDiv = document.getElementById("statsResult");

    if (!shortCode) {
        statsDiv.innerHTML = "<p style='color:red;'>Please enter a short code.</p>";
        return;
    }

    fetch(`http://localhost:8000/shorten/${shortCode}/stats/`)
        .then(response => {
            if (!response.ok) {
                throw new Error("Stats not found for this short code.");
            }
            return response.json();
        })
     .then(data => {
    statsDiv.innerHTML = `
        <div class="result">
            <p><strong>Access Count:</strong> ${data.accessCount}</p>
        </div>
    `;
})
        .catch(error => {
            statsDiv.innerHTML = `<p style='color:red;'>${error.message}</p>`;
        });
}







function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== "") {
        const cookies = document.cookie.split(";");
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + "=")) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
function deleteShortURL() {
    const shortCode = document.getElementById("deleteCode").value;
    const msg = document.getElementById("deleteMsg");
    const csrftoken = getCookie('csrftoken'); // from cookie

    if (!shortCode) {
        msg.textContent = "Please enter a short code.";
        msg.style.color = "red";
        return;
    }

    fetch(`http://localhost:8000/shorten/${shortCode}/delete/`, {
        method: 'DELETE',
        headers: {
            'X-CSRFToken': csrftoken,
            'Content-Type': 'application/json',
        },
    })
    .then(res => {
        if (res.status === 204) {
            msg.textContent = "Short URL deleted successfully.";
            msg.style.color = "green";
        } else {
            msg.textContent = "Failed to delete. Maybe not found.";
            msg.style.color = "red";
        }
    })
    .catch(() => {
        msg.textContent = "Network or server error.";
        msg.style.color = "red";
    });
}
