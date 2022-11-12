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
 
  // POST with Fetch API
  fetch('http://192.168.86.31:5000/upload-file', {
    method: "POST", 
    body: payload, 
    // No content-type! With FormData object, Fetch API sets this automatically.
    header: "Access-Control-Allow-Origin: *",
  })
  .then(res => {
    console.log(res.status)
    if(!res.ok){
      alert("File Upload Failed. Please Try Again - Not okay!")
    } else {
      alert("File Upload Successful!")
      return res.json()
    }
  })
  .then(data => console.log(data))
  .catch(err => {
    console.log("Coming here..")
    console.log(err)
    alert("File Upload Failed. Please Try Again")
  })
});