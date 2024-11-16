const userData = {
    username: "dhy",
    email: "dhy@example.com",
    password: "password123",
};

console.log("hello world");

fetch('http://localhost:8000/api/users/create/', {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json',
    },
    body: JSON.stringify(userData),
})
    .then(response => {
        if (!response.ok) {
            return response.text().then(text => { throw new Error(text); });
        }
        return response.json();
    })
    .then(data => console.log('User created:'))
    .catch(error => console.error('Error: '));