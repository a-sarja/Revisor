// Select your input type file and store it in a variable
const form = document.getElementById('form1');
 
form.addEventListener('submit', function(event) {
  // Prevent default HTML page refresh
  event.preventDefault();
 
  // Select file upload element
  const uploadElement = document.getElementById('file');
  const uploadEmail = document.getElementById('exampleInputEmail1');
  // Extract the file (for a single file, always 0 in the list)
  const f = uploadElement.files[0];

  // Create new formData object then append file
  const payload = new FormData();
  payload.append('user_file', f);
  payload.append('user_email', uploadEmail.value);

  // Replace below URL with backend-container URL - http://localhost:5000/upload-file
  fetch('http://3.22.233.61:5000/upload-file', {
    method: "POST",
    body: payload,
    header: {
        "Access-Control-Allow-Origin": "*"
    }
  })
  .then(function(response) {
    console.log(response.text());
    if(response.status === 200) {
        alert("File Upload Successful! Keep watching your email inbox for scan reports..")
    } else {
        alert("File Upload Failed. Please Try Again!")
    };
  })
  .catch(function(error) {
    console.log(error);
    alert("Error in uploading the file. Please Try Again!");
  })

});