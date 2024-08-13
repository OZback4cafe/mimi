document.addEventListener('DOMContentLoaded', function () {
    const menuWrap = document.querySelector('#menu_wrap');
    const orderBox = document.querySelector('#order_box');
    const payButton = document.querySelector('#pay_button');
    const paymentPopup = document.querySelector('#payment_popup');
    const popupClose = document.querySelector('#popup_close');
    const confirmPaymentButton = document.querySelector('#confirm_payment');
    const cashInput = document.querySelector('#cash');
    const cardInput = document.querySelector('#card');
    const pointsInput = document.querySelector('#points');
    const couponsInput = document.querySelector('#coupons');
    const balanceSpan = document.querySelector('#balance');
    const popupTotalAmount = document.querySelector('#popup_total_amount');
    const username = "{{ username }}"; // 템플릿 엔진에서 username을 가져

    // 메뉴 페이지 클릭 이벤트
    menuWrap.querySelectorAll('div').forEach(function (menuPage) {
        menuPage.addEventListener('click', function () {
            menuWrap.querySelectorAll('div').forEach(function (sibling) {
                sibling.classList.remove('on');
            });
            menuPage.classList.add('on');
        });
    });

    // 메뉴 박스 클릭 이벤트
    document.querySelectorAll('.menu_box').forEach(function (menuBox) {
        menuBox.addEventListener('click', function () {
            const menuName = menuBox.querySelector('p').textContent;
            const menuPrice = parseInt(menuBox.dataset.price);

            let existingMenu = orderBox.querySelector(".order_list [data-name='" + menuName + "']");

            if (existingMenu) {
                let quantityElement = existingMenu.querySelector('.quantity');
                let currentQuantity = parseInt(quantityElement.textContent);
                quantityElement.textContent = currentQuantity + 1;
            } else {
                let newOrder = document.createElement('div');
                newOrder.className = 'order_item';
                newOrder.dataset.name = menuName;
                newOrder.dataset.price = menuPrice;
                newOrder.innerHTML = `<span class="menu_name">${menuName}</span> x <span class="quantity">1</span> <button class="remove_item"></button>`;
                orderBox.querySelector('.order_list').appendChild(newOrder);

                // 주문 항목 삭제 기능 추가
                newOrder.querySelector('.remove_item').addEventListener('click', function () {
                    newOrder.remove();
                    updateTotal();
                });
            }

            updateTotal();
        });
    });

    // 총 결제금액 업데이트 함수
    function updateTotal() {
        let total = 0;
        let totalQuantity = 0;
        orderBox.querySelectorAll('.order_list .order_item').forEach(function (orderItem) {
            let pricePerItem = parseInt(orderItem.dataset.price);
            let quantity = parseInt(orderItem.querySelector('.quantity').textContent);
            totalQuantity += quantity;
            total += pricePerItem * quantity;
        });
        orderBox.querySelector('.order_result .order_count').textContent = totalQuantity + ' 개';
        orderBox.querySelector('.order_result .total').textContent = total + '원';
        return total;
    }

    // 결제 버튼 클릭 이벤트
    payButton.addEventListener('click', function () {
        const totalAmount = updateTotal(); // 팝업 열릴 때 총 금액 계산
        popupTotalAmount.textContent = totalAmount;
        paymentPopup.style.display = 'block';
        updateBalance(); // 팝업 열릴 때 잔액 업데이트
        // 현금 입력 필드에 자동으로 포커스 설정
        cashInput.focus();
    });

    // 팝업 닫기 버튼 클릭 이벤트
    popupClose.addEventListener('click', function () {
        paymentPopup.style.display = 'none';
    });

    // 결제 확인 버튼 클릭 이벤트
    confirmPaymentButton.addEventListener('click', function () {
        const cash = parseInt(cashInput.value, 10) || 0;
        const card = parseInt(cardInput.value, 10) || 0;
        const points = parseInt(pointsInput.value, 10) || 0;
        const coupons = parseInt(couponsInput.value, 10) || 0;

        const totalAmount = parseInt(popupTotalAmount.textContent, 10) || 0;
        if (cash + card + points + coupons >= totalAmount) {
            alert('결제가 완료되었습니다!');
            paymentPopup.style.display = 'none';
            // 포인트 적립 페이지를 팝업으로 열기
            openPointSystemPopup(totalAmount);
        } else {
            alert('결제 금액이 부족합니다.');
        }
    });

    // 입력된 값에 따라 잔액 업데이트
    function updateBalance() {
        const cash = parseInt(cashInput.value, 10) || 0;
        const card = parseInt(cardInput.value, 10) || 0;
        const points = parseInt(pointsInput.value, 10) || 0;
        const coupons = parseInt(couponsInput.value, 10) || 0;

        const totalPayment = cash + card + points + coupons;
        const totalAmount = parseInt(popupTotalAmount.textContent, 10) || 0;
        const balance = totalAmount - totalPayment;

        balanceSpan.textContent = balance >= 0 ? balance : '0';
    }

    [cashInput, cardInput, pointsInput, couponsInput].forEach(function (input) {
        input.addEventListener('input', updateBalance);
    });

    function openPointSystemPopup(totalAmount) {
        const popupWidth = 400;
        const popupHeight = 600;
        const left = (screen.width - popupWidth) / 2;
        const top = (screen.height - popupHeight) / 2;

        const pointSystemWindow = window.open(
            `/point/${totalAmount}`,
            '포인트 적립',
            `width=${popupWidth},height=${popupHeight},top=${top},left=${left}`
        );

        // 포인트 적립 완료 또는 취소 버튼 클릭 시 창 닫기
        const intervalId = setInterval(function () {
            if (pointSystemWindow.closed) {
                clearInterval(intervalId);
                alert('포인트 적립이 완료되었습니다.');
                
                // 현재 POS 페이지를 새로 고침
                window.location.href = `/pos`;
            }
        }, 500);
    }
});
