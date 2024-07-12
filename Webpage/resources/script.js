function scrollDown(sectionId) {
    var section = document.getElementById(sectionId);
    if (section) {
        section.scrollIntoView({ behavior: 'smooth' });
    }
}

function sendFolder() {
    var input = document.createElement('input'); //Opens windows folder dialog box
    input.type = 'file';
    input.multiple = true;
    input.webkitdirectory = true;
    input.click();

    input.onchange = async function (event) {
        const files = event.target.files;

        if (files && files.length > 0) {
            document.getElementById('changeText').textContent = "Uploading your folder...";
            document.getElementById('changeIcon').src = "./resources/SpinningIcon.svg";
            var icon = document.getElementById("changeIcon");
            icon.classList.add("spin")

            const zip = new JSZip();    //Zips folder
            for (let i = 0; i < files.length; i++) {
                const file = files[i];
                const content = await file.arrayBuffer();
                zip.file(file.webkitRelativePath, content);
            }

            const zipContent = await zip.generateAsync({ type: "blob" });
            
            const formData = new FormData();
            formData.append('file', zipContent, 'folder.zip');

            fetch('http://127.0.0.1:5500/upload', {
                method: 'POST',
                body: formData
            })
            .then(response => {
                if (response.ok) {
                    icon.classList.remove("spin")
                    document.getElementById('changeText').textContent = "Yay! Your folder will download shortly..";
                    document.getElementById('changeIcon').src = "./resources/SuccessIcon.svg";

                    // Trigger file download
                    response.blob().then(blob => {
                        const url = window.URL.createObjectURL(blob);
                        const a = document.createElement('a');
                        a.href = url;
                        a.download = 'Fixed Documents.zip'; // Replace with the desired filename
                        document.body.appendChild(a);
                        a.click();
                        window.URL.revokeObjectURL(url);
                    }); 
                }    
                else {
                    icon.classList.remove("spin")
                    document.getElementById('changeText').textContent = "Failed to upload folder. Please try again.";
                    document.getElementById('changeIcon').src = "./resources/ErrorIcon.svg";
                }
            })
            .catch(error => {
                console.error('Error sending folder:', error);
                icon.classList.remove("spin")
                document.getElementById('changeText').textContent = "Failed to upload folder. Please try again.";
                document.getElementById('changeIcon').src = "./resources/ErrorIcon.svg";
            });
        }

        else {
            document.getElementById('changeText').textContent = "Hmm... Your folder looks empty. Please try again.";
            document.getElementById('changeIcon').src = "./resources/ErrorIcon.svg";
        }
    };
}