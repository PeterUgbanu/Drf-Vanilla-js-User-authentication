const $ = (id) => {
  return document.getElementById(id);
};

const signUpButton = $("signUp");
const signInButton = $("signIn");
const container = $("container");

signUpButton.addEventListener("click", () => {
  container.classList.add("right-panel-active");
});

signInButton.addEventListener("click", () => {
  container.classList.remove("right-panel-active");
});

const register = $("register-form");
const login = $("login-form");

const login_url = "http://127.0.0.1:8000/api/auth/login/";
const register_url = "http://127.0.0.1:8000/api/auth/register/";

const fetch_data = async (url, payload) => {
  try {
    const res = await fetch(url, payload);
    const data = await res.json();
    return data;
  } catch (error) {
    console.log(error);
  }
};

register.addEventListener("submit", (e) => {
  e.preventDefault();
  const first_name = $("firstname").value;
  const username = $("username").value;
  const last_name = $("lastname").value;
  const email = $("email").value;
  const password = $("password").value;

  const payload = {
    method: "POST",
    headers: {
      "Content-Type": "application/json;charset=UTF-8",
    },
    body: JSON.stringify({
      first_name,
      username,
      last_name,
      email,
      password,
    }),
  };
  container.classList.remove("right-panel-active");

  const data = fetch_data(register_url, payload);
  const res = data.json();
  console.log(res);
});

login.addEventListener("submit", async (e) => {
  e.preventDefault();
  const username = $("login-username").value;
  const password = $("login-password").value;
  const payload = {
    method: "POST",
    headers: {
      "Content-Type": "application/json;charset=UTF-8",
    },
    body: JSON.stringify({
      username,
      password,
    }),
  };
  try {
    await fetch(login_url, payload)
      .then((res) => res.json())
      .then((res_data) => {
        console.log(res_data);
        auth = res_data.token;
        auth && localStorage.setItem("auth", auth);
        auth && window.location.replace("/js_user/home.html");
      });
  } catch (err) {
    console.log(err);
    if (err.detail === "Invalid token") {
      window.location.replace("/js_user/register_login.html");
    }
  }
});
