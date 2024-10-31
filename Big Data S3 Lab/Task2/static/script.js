const BASE_URL = 'http://127.0.0.1:5000';

// Handle user creation
document.getElementById('user-form').addEventListener('submit', async (e) => {
    e.preventDefault();
    const formData = new FormData();
    formData.append('name', document.getElementById('user-name').value);
    formData.append('email', document.getElementById('user-email').value);
    formData.append('password', document.getElementById('user-password').value);
    formData.append('image', document.getElementById('user-image').files[0]);

    const response = await fetch(`${BASE_URL}/users`, {
        method: 'POST',
        body: formData,
    });

    const result = await response.json();
    alert('User created successfully!');
    console.log(result);
});

// Handle post creation
document.getElementById('post-form').addEventListener('submit', async (e) => {
    e.preventDefault();
    const formData = new FormData();
    formData.append('email', document.getElementById('post-email').value);
    formData.append('content', document.getElementById('post-content').value);
    const mediaFile = document.getElementById('post-media').files[0];
    if (mediaFile) {
        formData.append('media', mediaFile);
    }

    const response = await fetch(`${BASE_URL}/posts`, {
        method: 'POST',
        body: formData,
    });

    const result = await response.json();
    alert('Post created successfully!');
    console.log(result);
    loadPosts(); // Refresh the posts
});

// Load all posts
async function loadPosts() {
    const response = await fetch(`${BASE_URL}/posts`);
    const posts = await response.json();
    const postList = document.getElementById('post-list');
    postList.innerHTML = '';

    posts.forEach((post) => {
        const postDiv = document.createElement('div');
        postDiv.className = 'post';
        postDiv.innerHTML = `
            <h3>${post.content}</h3>
            <p>Posted by: ${post.email}</p>
            ${post.media ? `<img src="${post.media}" alt="Post media" width="100%">` : ''}
            <p>Likes: ${post.likes}</p>
            <button onclick="likePost('${post.post_id}')">Like</button>
            <div>
                <h4>Comments</h4>
                <ul>${post.comments.map(c => `<li>${c.email}: ${c.text}</li>`).join('')}</ul>
                <input type="text" placeholder="Add a comment" id="comment-${post.post_id}">
                <button onclick="commentPost('${post.post_id}')">Comment</button>
            </div>
        `;
        postList.appendChild(postDiv);
    });
}

// Handle liking a post
async function likePost(postId) {
    await fetch(`${BASE_URL}/posts/${postId}/like`, { method: 'POST' });
    alert('Post liked!');
    loadPosts(); // Refresh the posts
}

// Handle commenting on a post
async function commentPost(postId) {
    const commentText = document.getElementById(`comment-${postId}`).value;
    const email = prompt('Enter your email:'); // Basic prompt to get user email

    await fetch(`${BASE_URL}/posts/${postId}/comment`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email, text: commentText }),
    });

    alert('Comment added!');
    loadPosts(); // Refresh the posts
}

// Initial load of posts
loadPosts();
