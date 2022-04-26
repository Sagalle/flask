
function asd(a)
{
    if(a==1)
        document.getElementById("asd").style.display="none";
    else
        document.getElementById("asd").style.display="block";
}


function deletePost(noteId) {
  fetch("delete-post", {
    method: "POST",
    body: JSON.stringify({ noteId: noteId }),
  }).then((_res) => {
    window.location.href = "/";
  });
}