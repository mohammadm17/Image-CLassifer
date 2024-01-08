function predict() {
    var fileInput = document.getElementById('image-upload');
    var file = fileInput.files[0];

    var reader = new FileReader();
    reader.onloadend = function () {
        var base64Image = reader.result.split(',')[1];

        // Send a POST request to the /predict endpoint
        fetch('/predict', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ 'image': base64Image }),
        })
        .then(response => response.json())
        .then(data => {
            var resultElement = document.getElementById('prediction-result');
            resultElement.innerText = 'Predicted Class: ' + data.predicted_class;
        })
        .catch(error => {
            console.error('Error:', error);
        });
    };

    reader.readAsDataURL(file);
}
