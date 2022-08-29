const deleteModal = new bootstrap.Modal(document.getElementById("deleteModal"));
var deleteButtons = document.getElementsByClassName("btn-delete");
var editButtons = document.getElementsByClassName("btn-edit");
var deleteConfirm = document.getElementById("deleteConfirm");
var commentText = document.getElementsByTagName("textarea")[0];
var commentForm = document.getElementById("commentForm");
var submitButton = document.getElementById("submitButton");

// empty the comment text after post

commentText.value = "";

for (let button of deleteButtons) {
    button.addEventListener("click", (e) => {
        let commentId = e.target.getAttribute("comment_id");
        deleteConfirm.href = `delete_comment/${commentId}`;
        deleteModal.show();
    });
}

for (let button of editButtons) {
    button.addEventListener("click", (e) => {
        let commentId = e.target.getAttribute("comment_id");
        let commentContent = document.getElementById(`comment${commentId}`).innerText;
        commentText.value = commentContent;
        submitButton.innerText = "Update";
        commentForm.setAttribute("action", `edit_comment/${commentId}`);
    });
}