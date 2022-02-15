function show_hide_password(target){
    var input = document.getElementById('password-input-login');
    if (input.getAttribute('type') == 'password') {
        target.classList.add('view');
        input.setAttribute('type', 'text');
    } else {
        target.classList.remove('view');
        input.setAttribute('type', 'password');
    }
    return false;
}
function show_hide_password_confirm(target){
var input_confirm = document.getElementById('password-input-login-confirm');
if (input_confirm.getAttribute('type') == 'password') {
    target.classList.add('view');
    input_confirm.setAttribute('type', 'text');
} else{
    target.classList.remove('view');
    input_confirm.setAttribute('type', 'password');

}
    return false;

}

// Проверка на надежность
var s_letters = "qwertyuiopasdfghjklzxcvbnm"; // Буквы в нижнем регистре
var b_letters = "QWERTYUIOPLKJHGFDSAZXCVBNM"; // Буквы в верхнем регистре
var digits = "0123456789"; // Цифры
var specials = "!@#$%^&*()_-+=\|/.,:;[]{}"; // Спецсимволы
           
var input_test = document.getElementById('password-input-login');//получаем поле
var block_check = document.getElementById('block_check');//получаем блок с индикатором
       
input_test.addEventListener('keyup', function(evt){
var input_test_val = input_test.value;//получаем значение из поля
        
var is_s = false; // Есть ли в пароле буквы в нижнем регистре
var is_b = false; // Есть ли в пароле буквы в верхнем регистре
var is_d = false; // Есть ли в пароле цифры
var is_sp = false; // Есть ли в пароле спецсимволы
        
for (var i = 0; i < input_test_val.length; i++) {
    /* Проверяем каждый символ пароля на принадлежность к тому или иному типу */
    if (!is_s && s_letters.indexOf(input_test_val[i]) != -1) {
         is_s = true
    }
    else if (!is_b && b_letters.indexOf(input_test_val[i]) != -1) {
          is_b = true
    }
    else if (!is_d && digits.indexOf(input_test_val[i]) != -1) {
           is_d = true
    }
    else if (!is_sp && specials.indexOf(input_test_val[i]) != -1) {
           is_sp = true
    }
}

var rating = 0;
if (is_s) rating++; // Если в пароле есть символы в нижнем регистре, то увеличиваем рейтинг сложности
if (is_b) rating++; // Если в пароле есть символы в верхнем регистре, то увеличиваем рейтинг сложности
if (is_d) rating++; // Если в пароле есть цифры, то увеличиваем рейтинг сложности
if (is_sp) rating++; // Если в пароле есть спецсимволы, то увеличиваем рейтинг сложности
/* Далее идёт анализ длины пароля и полученного рейтинга, и на основании этого готовится текстовое описание сложности пароля */
if (input_test_val.length < 6 && rating < 3) {
    block_check.style.width = "10%";
    block_check.style.backgroundColor = '#e7140d';
}
else if (input_test_val.length < 6 && rating >= 3) {
    block_check.style.width = "50%";
    block_check.style.backgroundColor = '#ffdb00';
}
else if (input_test_val.length >= 8 && rating < 3) {
    block_check.style.width = "50%";
    block_check.style.backgroundColor = '#ffdb00';
}
else if (input_test_val.length >= 8 && rating >= 3) {
    block_check.style.width = "100%";
    block_check.style.backgroundColor = '#61ac27';
}
else if (input_test_val.length >= 6 && rating == 1) {
    block_check.style.width = "10%";
    block_check.style.backgroundColor = '#e7140d';
}
else if (input_test_val.length >= 6 && rating > 1 && rating < 4) {
    block_check.style.width = "50%";
    block_check.style.backgroundColor = '#ffdb00';
}
else if (input_test_val.length >= 6 && rating == 4) {
    block_check.style.width = "100%";
    block_check.style.backgroundColor = '#61ac27';
};
});


function checkPasswordMatch() {
var password = $("#password-input-login").val();
var confirmPassword = $("#password-input-login-confirm").val();
var elem = document.querySelector('#divCheckPasswordMatch')
    
if (password != confirmPassword){

 elem.classList.remove('alert-success')

 elem.classList.add('alert-danger')
$("#divCheckPasswordMatch").html("Пароли не савподают");

}
if (password == confirmPassword){
elem.classList.remove('alert-danger')
elem.classList.add('alert-success')
var elem = document.querySelector('#divCheckPasswordMatch')
$("#divCheckPasswordMatch").html("Пароли совподают!");

 
    }}
    $(document).ready(function () {
        $("#password-input-login, #password-input-login-confirm").keyup(checkPasswordMatch);
});
                  