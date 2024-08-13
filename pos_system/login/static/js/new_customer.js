document.addEventListener("DOMContentLoaded", function() {
    const urlParams = new URLSearchParams(window.location.search);
    const phone = urlParams.get('phone');

    if (phone) {
        document.getElementById("phone").value = phone;
    }

    const newCustomerForm = document.getElementById("new-customer-form");
    const signupResult = document.getElementById("signup-result");
    const cancelBtn = document.getElementById("cancel-btn");

    newCustomerForm.addEventListener("submit", function(event) {
        event.preventDefault();

        const name = document.getElementById("name").value;
        const birthday = document.getElementById("birthday").value;
        const phone = document.getElementById("phone").value;

        fetch('/api/add_customer', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ name: name, birthday: birthday, phone: phone }),
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                signupResult.textContent = '고객 등록이 완료되었습니다.';
                signupResult.style.color = '#28a745';
                setTimeout(() => window.close(), 1000); // 1초 후 창 닫기
            } else {
                signupResult.textContent = '고객 등록에 실패했습니다.';
                signupResult.style.color = '#ff0000';
            }
        })
        .catch(error => {
            console.error('Error:', error);
            signupResult.textContent = '오류가 발생했습니다. 다시 시도하세요.';
            signupResult.style.color = '#ff0000';
        });
    });

    cancelBtn.addEventListener("click", function() {
        window.close();  // 창 닫기
    });
});