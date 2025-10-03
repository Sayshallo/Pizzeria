function open_reg() {
  const modal = new bootstrap.Modal(document.querySelector('#exampleModalToggle'));
  modal.modal('hide');
  console.log("Hiding...")
  console.log(modal)
}

function delete_cookie(name) {
          document.cookie = name +'=; Path=/; Expires=Thu, 01 Jan 1970 00:00:01 GMT;';
          window.location.replace('/')
        }

        function getCookie(name) {
          const value = `; ${document.cookie}`;
          const parts = value.split(`; ${name}=`);
          if (parts.length === 2) return parts.pop().split(';').shift();
        }
        let session_id = getCookie('session');

        let login_button = document.getElementById("login-button");
        let first_modal = document.getElementById("login-button");
        console.log(login_button.innerText);

        if (session_id != null) {
            login_button.innerText = 'Аккаунт / Выход';
            login_button.dataset.bsTarget = '#exampleModal-2';
            login_button.classList.add("account-button", "btn-light");
            login_button.classList.remove("btn-outline-warning");
            login_button.style.opacity = "1";
            login_button.disabled = false;
        }
        else {
            login_button.dataset.bsTarget = '#exampleModal';
            login_button.classList.remove("account-button", "btn-light");
            login_button.classList.add("btn-outline-warning");
            login_button.style.opacity = "1";
            login_button.disabled = false;
        }

        document.getElementById("nav-about").style.opacity = "1";
        document.getElementById("nav-constr").style.opacity = "1";
        document.getElementById("nav-main").style.opacity = "1";


