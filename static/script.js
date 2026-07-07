// ===============================
// API URL
// ===============================

const API_URL = "http://127.0.0.1:8000";

// ===============================
// HTML Elements
// ===============================

const postForm = document.getElementById("postForm");
const titleInput = document.getElementById("title");
const contentInput = document.getElementById("content");
const refreshBtn = document.getElementById("refreshBtn");
const postsContainer = document.getElementById("postsContainer");

// ===============================
// Load Posts When Page Opens
// ===============================

document.addEventListener("DOMContentLoaded", loadPosts);

refreshBtn.addEventListener("click", loadPosts);

// ===============================
// Create New Post
// ===============================

postForm.addEventListener("submit", async (e) => {

    e.preventDefault();

    const title = titleInput.value.trim();
    const content = contentInput.value.trim();

    if (!title || !content) {
        alert("Please fill all fields");
        return;
    }

    const response = await fetch(`${API_URL}/posts`, {

        method: "POST",

        headers: {
            "Content-Type": "application/json"
        },

        body: JSON.stringify({
            title,
            content
        })

    });

    if (response.ok) {

        postForm.reset();

        loadPosts();

    } else {

        alert("Unable to create post.");

    }

});

// ===============================
// Load All Posts
// ===============================

async function loadPosts() {

    postsContainer.innerHTML = `
        <div class="loading">
            Loading Posts...
        </div>
    `;

    const response = await fetch(`${API_URL}/posts`);

    const posts = await response.json();

    if (posts.length === 0) {

        postsContainer.innerHTML = `
            <div class="empty">
                No Posts Available
            </div>
        `;

        return;
    }

    postsContainer.innerHTML = "";

    posts.forEach(post => {

        const postDiv = document.createElement("div");

        postDiv.className = "post";

        postDiv.innerHTML = `

            <h2>${post.title}</h2>

            <p>${post.content}</p>

            <hr>

            <div class="comment-box">

                <h3>Comments</h3>

                <div class="comments">

                    ${
                        post.comments.length === 0
                        ?
                        "<p>No Comments Yet</p>"
                        :
                        post.comments.map(comment => `
                            <div class="comment">

                                <strong>${comment.author}</strong>

                                <p>${comment.content}</p>

                            </div>
                        `).join("")
                    }

                </div>

                <form class="comment-form">

                    <input
                        type="text"
                        placeholder="Your Name"
                        class="author"
                        required
                    >

                    <textarea
                        placeholder="Write a comment..."
                        class="commentContent"
                        required
                    ></textarea>

                    <button
                        type="submit"
                        class="comment-btn"
                    >
                        Add Comment
                    </button>

                </form>

            </div>

            <button
                class="delete-btn"
            >
                Delete Post
            </button>

        `;

        // ---------------------------
        // Delete Button
        // ---------------------------

        const deleteBtn = postDiv.querySelector(".delete-btn");

        deleteBtn.addEventListener("click", async () => {

            if (!confirm("Delete this post?")) return;

            const res = await fetch(`${API_URL}/posts/${post.id}`, {

                method: "DELETE"

            });

            if (res.ok) {

                loadPosts();

            } else {

                alert("Delete Failed");

            }

        });

        // ---------------------------
        // Comment Form
        // ---------------------------

        const commentForm = postDiv.querySelector(".comment-form");

        commentForm.addEventListener("submit", async (e) => {

            e.preventDefault();

            const author =
                commentForm.querySelector(".author").value.trim();

            const content =
                commentForm.querySelector(".commentContent").value.trim();

            if (!author || !content) {

                alert("Fill all fields");

                return;

            }

            const res = await fetch(

                `${API_URL}/posts/${post.id}/comments`,

                {

                    method: "POST",

                    headers: {

                        "Content-Type": "application/json"

                    },

                    body: JSON.stringify({

                        author,

                        content

                    })

                }

            );

            if (res.ok) {

                loadPosts();

            } else {

                alert("Unable to add comment.");

            }

        });

        postsContainer.appendChild(postDiv);

    });

}