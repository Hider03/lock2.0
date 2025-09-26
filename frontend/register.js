class User {
    constructor(username, email, password) {
        this.username = username;
        this.email = email;
        this.password = password; // In a real application, hash this password
    }

    register() {
        fetch("/register", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ username: this.username, email: this.email, password: this.password })
        });
    }


    // In a real application, you would add methods for validating,
    // saving to a database, etc.
    displayUserInfo() {
        return `Username: ${this.username}, Email: ${this.email}`;
    }
}