const home_url = "http://127.0.0.1:8000/api/auth/user/";

auth = localStorage.getItem("auth");
if (!auth || auth === "undefined")
  window.location.replace("/js_user/register_login.html");

const $ = (id) => {
  return document.getElementById(id);
};

let user = "";

async function getUser(url) {
  await fetch(url, {
    method: "GET",
    headers: {
      Authorization: `Token ${auth}`,
    },
  })
    .then((res) => res.json())
    .then((data) => {
      console.log(data);
      user = data.username;
      $("user").textContent += ` ${data.username}`;
      $("email").textContent += `${data.email}`;
      $("firstname").textContent += ` ${data.first_name}`;
      $("lastname").textContent += ` ${data.last_name}`;
    })
    .catch((err) => console.log(err));
}

getUser(home_url);
