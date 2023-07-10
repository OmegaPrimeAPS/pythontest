document.addEventListener('DOMContentLoaded', function () {
    const signInTab = document.querySelector('.active');
    const signUpTab = document.querySelector('.inactive');

    signupForm.style.display = 'none';

    signInTab.addEventListener('click', function () {
        signInTab.classList.add('active');
        signUpTab.classList.remove('active');
        signUpTab.classList.add('inactive');

        document.getElementById('loginForm').style.display = 'block';
        document.getElementById('signupForm').style.display = 'none';
    });

    signUpTab.addEventListener('click', function () {
        signUpTab.classList.add('active');
        signInTab.classList.remove('active');
        signInTab.classList.add('inactive');

        document.getElementById('signupForm').style.display = 'block';
        document.getElementById('loginForm').style.display = 'none';
    });
});
