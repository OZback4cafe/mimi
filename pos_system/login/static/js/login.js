document.getElementById('loginForm').addEventListener('submit', function(event) {
    event.preventDefault();

    const formData = new FormData(this);

    fetch('/login', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            // 로그인 성공 시 사용자 이름을 가져옵니다.
            const username = formData.get('username'); // 로그인 폼에서 username 입력값을 가져옵니다.

            // 성공 메시지 표시
            alert(data.message);

            // 사용자 이름을 포함한 URL로 리다이렉트
            window.location.href = `/pos/${username}`;
        } else {
            // 로그인 실패 시 에러 메시지 표시
            document.getElementById('error-message').innerText = data.message;
        }
    })
    .catch(error => console.error('Error:', error));
});
