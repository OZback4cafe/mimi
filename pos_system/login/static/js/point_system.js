document.addEventListener('DOMContentLoaded', function() {
    const pointForm = document.getElementById("point-form");
    const resultDiv = document.getElementById("result");
    const actionsDiv = document.getElementById("actions");
    const newCustomerOptions = document.getElementById("new-customer-options");
    const addPointsBtn = document.getElementById("add-points-btn");
    const newCustomerBtn = document.getElementById("new-customer-btn");
    const editCustomerBtn = document.getElementById("edit-customer-btn");
    const editCancelBtn = document.getElementById("edit-cancel-btn");
    const cancelBtn = document.getElementById("cancel-btn");

    if (pointForm) {
        pointForm.addEventListener("submit", function(event) {
            event.preventDefault();

            const phone = document.getElementById("phone").value;

            fetch('/api/get_customer_info', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ phone: phone }),
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    resultDiv.innerHTML = `
                        <p>고객 이름: ${data.customer.name}</p>
                        <p>생일: ${data.customer.birthday}</p>
                        <p>포인트: ${data.customer.points}</p>
                    `;
                    actionsDiv.style.display = "block";
                    newCustomerOptions.style.display = "none";
                } else {
                    resultDiv.textContent = '고객 정보를 찾을 수 없습니다.';
                    actionsDiv.style.display = "none";
                    newCustomerOptions.style.display = "block";
                }
            })
            .catch(error => {
                console.error('Error:', error);
                resultDiv.textContent = '오류가 발생했습니다. 다시 시도하세요.';
                actionsDiv.style.display = "none";
            });
        });

        cancelBtn.addEventListener("click", function() {
            window.close();  // 창 닫기
        });

        addPointsBtn.addEventListener("click", function() {
            const phone = document.getElementById("phone").value;

            fetch('/api/add_points', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ phone: phone, points: 10 }), // 예: 10포인트 적립
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    resultDiv.textContent = '포인트 적립이 완료되었습니다.';
                    resultDiv.style.color = '#28a745';
                    setTimeout(() => {
                        window.close(); // 창 닫기
                        if (window.opener) {
                            window.opener.location.reload(); // 원래 페이지 새로 고침
                        }
                    }, 500); // 0.5초 후 창 닫기
                } else {
                    resultDiv.textContent = '포인트 적립에 실패했습니다.';
                    resultDiv.style.color = '#ff0000';
                }
            })
            .catch(error => {
                console.error('Error:', error);
                resultDiv.textContent = '오류가 발생했습니다. 다시 시도하세요.';
                resultDiv.style.color = '#ff0000';
            });
        });

        newCustomerBtn.addEventListener("click", function() {
            const phone = document.getElementById("phone").value;
            const url = `/new_customer?phone=${encodeURIComponent(phone)}`;
            window.open(url, "신규 가입", "width=400,height=600,top=40%,left=40%");
        });

        editCustomerBtn.addEventListener("click", function() {
            const phone = document.getElementById("phone").value;
            const url = `/customer_info?phone=${encodeURIComponent(phone)}`;
            window.open(url, "고객 정보 수정", "width=400,height=600,top=40%,left=40%");
        });

        editCancelBtn.addEventListener("click", function() {
            window.close();  // 창 닫기
        });
    }
});
