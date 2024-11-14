This is the current format for calling the Project Chameleon API using JS. THIS FORMAT IS A WORK IN PROGRESS AND WILL CHANGE.

	$.ajax({
	    url: finalEndpoint,
	    method: "POST",
	    headers: {
	        "Content-Type": "application/json",
	        "access-token": "nschakJJdEsIQUfADFerH6aGjyz706f114C3c8leXhM"
	    },
	    data: JSON.stringify(Object.assign({
	        "input_url": downloadUrl,
	        "output": outputFileName,
	        "output_type": "raw"
	    }, extraData)),
	    dataType: "json"
	}).done(function(resp) {
	    switch (endpoint) {
	        case 'option1': 
	            mimeType = 'image/png';
	            break; 
	        case 'option2': 
	            mimeType = 'text/plain';
	            break;
	        case 'option3': 
	            mimeType = 'text/plain';
	            break;
	        case 'option4': 
	            mimeType = 'text/plain';
	            break;
	        case 'option7': 
	            mimeType = 'application/zip';
	        case 'option8': 
	            mimeType = 'text/plain';
	            break;
	        default: 
	            mimeType = 'application/octet-stream';  
	    }
	    console.log("Server Response:", resp); 
	    const byteCharacters = atob(resp);
	    const byteNumbers = new Array(byteCharacters.length);
	    for (let i = 0; i < byteCharacters.length; i++) {
	        byteNumbers[i] = byteCharacters.charCodeAt(i);
	    }
	    const byteArray = new Uint8Array(byteNumbers);
	    const blob = new Blob([byteArray], {type: mimeType});
	    let mimeType;
	
	    var file = new FileModel();
	    file.uploadToItem(view.item, blob, outputFileName, mimeType);
	    $('.modal').girderModal('close');
	    //location.reload();
	}).fail(function(xhr, status, error) {
	    console.error("Error:", error);
	    // Display error message in the dialog box
	    view.$('.g-validation-failed-message').html(`<div class="alert alert-danger">Error: ${error}</div>`);
	    view.$('.g-submit-create-chameleon').girderEnable(true); // Re-enable the submit button
	});