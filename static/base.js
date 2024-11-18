// Login JS
const loginForm = document.getElementById("loginForm");

if (loginForm) {
  loginForm.addEventListener("submit", async function (event) {
    event.preventDefault();

    const form = event.target;
    const formData = new FormData(form);

    const payload = new URLSearchParams();
    for (const [key, value] of formData.entries()) {
      payload.append(key, value);
    }

    try {
      const response = await fetch("/auth/token", {
        method: "POST",
        headers: {
          "Content-Type": "application/x-www-form-urlencoded",
        },
        body: payload.toString(),
      });

      if (response.ok) {
        // Handle success (e.g., redirect to dashboard)
        const data = await response.json();
        // Delete any cookies available
        logout();
        // Save token to cookie
        document.cookie = `access_token=${data.access_token}; path=/`;
        window.location.href = "/"; // Change this to your desired redirect page
      } else {
        // Handle error
        const errorData = await response.json();
        alert(`Error: ${errorData.detail}`);
      }
    } catch (error) {
      console.error("Error:", error);
      alert("An error occurred. Please try again.");
    }
  });
}

// Register JS
const registerForm = document.getElementById("registerForm");
if (registerForm) {
  registerForm.addEventListener("submit", async function (event) {
    event.preventDefault();

    const form = event.target;
    const formData = new FormData(form);
    const data = Object.fromEntries(formData.entries());

    if (data.password !== data.password2) {
      alert("Passwords do not match");
      return;
    }

    const payload = {
      email: data.email,
      name: data.name,
      password: data.password,
    };

    try {
      const response = await fetch("/user", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(payload),
      });

      if (response.ok) {
        window.location.href = "/";
      } else {
        // Handle error
        const errorData = await response.json();
        alert(`Error: ${errorData.message}`);
      }
    } catch (error) {
      console.error("Error:", error);
      alert("An error occurred. Please try again.");
    }
  });
}

// Profile JS
const profileForm = document.getElementById("profileForm");
if (profileForm) {
  profileForm.addEventListener("submit", async function (event) {
    event.preventDefault();

    const form = event.target;
    const formData = new FormData(form);
    const data = Object.fromEntries(formData.entries());

    const payload = {
      email: data.email,
      name: data.name,
    };

    try {
      const token = getCookie("access_token");
      if (!token) {
        throw new Error("Authentication token not found");
      }
      const response = await fetch(`/user/${data.id}`, {
        method: "PUT",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify(payload),
      });

      if (response.ok) {
        alert("Updated successfully");
        window.location.href = "/";
      } else {
        // Handle error
        const errorData = await response.json();
        alert(`Error: ${errorData.message}`);
      }
    } catch (error) {
      console.error("Error:", error);
      alert("An error occurred. Please try again.");
    }
  });
}

// Post Update JS
const postForm = document.getElementById("postForm");
if (postForm) {
  postForm.addEventListener("submit", async function (event) {
    event.preventDefault();

    const form = event.target;
    const formData = new FormData(form);
    const data = Object.fromEntries(formData.entries());

    const payload = {
      title: data.title,
      content: data.content,
    };

    try {
      const token = getCookie("access_token");

      if (!token) {
        throw new Error("Authentication token not found");
      }
      const response = await fetch(`/post/${data.id}`, {
        method: "PUT",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify(payload),
      });

      if (response.ok) {
        alert("Updated successfully");
        window.location.href = "/";
      } else {
        // Handle error
        const errorData = await response.json();
        alert(`Error: ${errorData.message}`);
      }
    } catch (error) {
      console.error("Error:", error);
      alert("An error occurred. Please try again.");
    }
  });
}

// Post Creation JS
const CreatePostForm = document.getElementById("CreatePostForm");
if (CreatePostForm) {
  CreatePostForm.addEventListener("submit", async function (event) {
    event.preventDefault();

    const form = event.target;
    const formData = new FormData(form);
    const data = Object.fromEntries(formData.entries());

    const payload = {
      title: data.title,
      content: data.content,
    };

    try {
      const token = getCookie("access_token");

      if (!token) {
        throw new Error("Authentication token not found");
      }

      const response = await fetch(`/post`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify(payload),
      });

      if (response.ok) {
        // alert("Created successfully");
        window.location.href = "/";
      } else {
        // Handle error
        const errorData = await response.json();
        alert(`Error: ${errorData.message}`);
      }
    } catch (error) {
      console.error("Error:", error);
      alert("An error occurred. Please try again.");
    }
  });
}

// Post delete
document
  .getElementById("deleteButton")
  .addEventListener("click", async function () {
    // var url = window.location.pathname;
    // const postId = url.substring(url.lastIndexOf("/") + 1);
    if (!confirm("Are you sure to delete?")) {
      return;
    }

    const postId = document.getElementById("postId").value;

    try {
      const token = getCookie("access_token");
      if (!token) {
        throw new Error("Authentication token not found");
      }

      const response = await fetch(`/post/${postId}`, {
        method: "DELETE",
        headers: {
          Authorization: `Bearer ${token}`,
        },
      });

      if (response.ok) {
        // Handle success
        window.location.href = "/"; // Redirect to the todo page
      } else {
        // Handle error
        const errorData = await response.json();
        alert(`Error: ${errorData.detail}`);
      }
    } catch (error) {
      console.error("Error:", error);
      alert("An error occurred. Please try again.");
    }
  });

// Helper function to get a cookie by name
function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== "") {
    const cookies = document.cookie.split(";");
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim();
      if (cookie.substring(0, name.length + 1) === name + "=") {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}

function logout() {
  // Get all cookies
  const cookies = document.cookie.split(";");

  // Iterate through all cookies and delete each one
  for (let i = 0; i < cookies.length; i++) {
    const cookie = cookies[i];
    const eqPos = cookie.indexOf("=");
    const name = eqPos > -1 ? cookie.substr(0, eqPos) : cookie;
    // Set the cookie's expiry date to a past date to delete it
    document.cookie = name + "=;expires=Thu, 01 Jan 1970 00:00:00 GMT;path=/";
  }

  // Redirect to the login page
  window.location.href = "/auth/login";
}
