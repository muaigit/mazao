document.addEventListener("DOMContentLoaded", () => {
    // Toggle mobile menu
    const menuToggle = document.querySelector(".fa-bars");
    const navbar = document.querySelector(".navbar");
    
    if (menuToggle) {
        menuToggle.addEventListener("click", () => {
            navbar.style.display = navbar.style.display === "block" ? "none" : "block";
        });
    }
    
    // Handle button click for fetching data
    const button = document.querySelector("button");
    const loadingMessage = document.getElementById("loading");
    const dataTable = document.getElementById("data-table");
    const tableBody = document.getElementById("table-body");
    
    if (button) {
        button.addEventListener("click", () => {
            loadingMessage.style.display = "block";
            fetch("http://127.0.0.1:8000/weather-api/")
                .then(response => response.json())
                .then(data => {
                    loadingMessage.style.display = "none";
                    if (data.length > 0) {
                        dataTable.style.display = "table";
                        tableBody.innerHTML = ""; // Clear previous data
                        data.forEach(entry => {
                            const row = `
                                <tr>
                                    <td>${entry.cityName}</td>
                                    <td>${entry.day}</td>
                                    <td>${entry.willitraintommorow}</td>
                                </tr>
                            `;
                            tableBody.innerHTML += row;
                        });
                    } else {
                        loadingMessage.innerText = "No data available";
                    }
                })
                .catch(error => {
                    console.error("Error:", error);
                    loadingMessage.innerText = "Failed to fetch data";
                });
        });
    }
});
