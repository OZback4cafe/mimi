document.addEventListener('DOMContentLoaded', function() {
    document.getElementById('coupon_name').addEventListener('change', function() {
        var inputField = document.getElementById('coupon_name_input');
        if (this.value === '직접 입력') {
            inputField.style.display = 'block';
            inputField.required = true;
        } else {
            inputField.style.display = 'none';
            inputField.required = false;
        }
    });
});

function setCafeName(name) {
    document.getElementById('cafe_name').value = name;
}
