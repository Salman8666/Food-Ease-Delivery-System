// Asynchronous Interface State Handler Core Logic Engine
document.addEventListener('DOMContentLoaded', () => {
    console.log("FoodEase Platform Core UI Engine fully initialized.");
    
    // Smooth interception handler for asynchronous AJAX Cart updates
    const dynamicCartButtons = document.querySelectorAll('.btn-add-cart-async');
    dynamicCartButtons.forEach(button => {
        button.addEventListener('click', async (e) => {
            e.preventDefault();
            const foodItemId = button.dataset.itemId;
            
            try {
                const response = await fetch('/api/cart/add', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ item_id: foodItemId, quantity: 1 })
                });
                const result = await response.json();
                if (result.status === "success") {
                    showToastNotification(result.message, "success");
                }
            } catch (error) {
                console.error("Network synchronization failed:", error);
            }
        });
    });
});

// Toast notification container injector
function showToastNotification(message, type = "success") {
    const toastContainer = document.createElement('div');
    toastContainer.className = `alert alert-${type} position-fixed bottom-0 end-0 m-4 shadow-lg z-3 border-0 rounded-3`;
    toastContainer.style.minWidth = "300px";
    toastContainer.innerHTML = `
        <div class="d-flex align-items-center justify-content-between">
            <span><i class="fa-solid fa-circle-check me-2"></i> ${message}</span>
            <button type="button" class="btn-close btn-close-white" data-bs-dismiss="alert"></button>
        </div>
    `;
    document.body.appendChild(toastContainer);
    setTimeout(() => { toastContainer.remove(); }, 4000);
}