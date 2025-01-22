const container = document.getElementById('container');
const registerBtn = document.getElementById('register');
const loginBtn = document.getElementById('login');
const signInButton = document.getElementById('signInButton');
const emailInput = document.getElementById('email');
const passwordInput = document.getElementById('password');
const errorMessage = document.getElementById('error-message');

// Fixed password in the system
const fixedPassword = "Open@1234"; // Change this value to whatever fixed password you want

// Register and login button event listeners
registerBtn.addEventListener('click', () => {
    container.classList.add("active");
});

loginBtn.addEventListener('click', () => {
    container.classList.remove("active");
});

// Function to validate Sign In form
function validateSignIn() {
    const email = emailInput.value.trim(); // Use .trim() to remove leading/trailing spaces
    const password = passwordInput.value.trim();

    // Enable the sign-in button only if email and password are valid (email must include '@', password can be anything)
    if (email && password && email.includes('@')) {
        signInButton.disabled = false;
    } else {
        signInButton.disabled = true;
    }
}

// Event listeners for real-time input validation
emailInput.addEventListener('input', validateSignIn);
passwordInput.addEventListener('input', validateSignIn);

// Sign In Button logic
signInButton.addEventListener('click', (e) => {
    e.preventDefault(); // Prevent default form submission

    const email = emailInput.value.trim(); // Trim input values to avoid leading/trailing spaces
    const password = passwordInput.value.trim();

    // Check if fields are empty
    if (!email || !password) {
        errorMessage.style.display = "block"; // Show the error message
        errorMessage.textContent = "Please fill in both email and password fields.";
    } else if (!email.includes('@')) {
        // Check for valid email format
        errorMessage.style.display = "block";
        errorMessage.textContent = "Please enter a valid email address (must contain '@').";
    } else if (password !== fixedPassword) {
        // Compare password against the fixed password in the code
        errorMessage.style.display = "block";
        errorMessage.textContent = "Invalid password.";
    } else {
        // If email is valid and password matches, hide error message and proceed
        errorMessage.style.display = "none"; // Hide the error message if credentials are correct
        // Redirect to the index page (or wherever you want after successful login)
        window.location.href = "/index";
    }
});
