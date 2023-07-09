/* scripts.js */
function showQuestionForm() {
    var fileInput = document.getElementById("fileInput");
    var questionForm = document.getElementById("questionForm");
  
    if (fileInput.value !== "") {
      questionForm.classList.remove("hidden");
    } else {
      questionForm.classList.add("hidden");
    }
  }
  
  function toggleInstructions() {
    var instructions = document.getElementById("instructions");
    instructions.classList.toggle("show");
  }
  
  function handleDrop(e) {
    e.preventDefault();
    var fileInput = document.getElementById("fileInput");
    fileInput.files = e.dataTransfer.files;
    showQuestionForm();
  }
  
  function handleDragOver(e) {
    e.preventDefault();
    var dropArea = document.getElementById("dropArea");
    dropArea.classList.add("active");
  }
  
  function handleDragLeave(e) {
    e.preventDefault();
    var dropArea = document.getElementById("dropArea");
    dropArea.classList.remove("active");
  }
  
  function handleFileChange() {
    var fileInput = document.getElementById("fileInput");
    showQuestionForm();
  }
  