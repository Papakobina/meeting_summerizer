// DOM Elements
document.addEventListener('DOMContentLoaded', function() {
  const dropArea = document.getElementById('dropArea');
  const fileInput = document.getElementById('fileInput');
  const uploadBtn = document.getElementById('uploadBtn');
  const resultsSection = document.getElementById('resultsSection');
  const summaryEl = document.getElementById('summary');
  const actionItemsEl = document.getElementById('actionItems');
  
  // Email section elements
  const emailSection = document.getElementById('emailSection');
  const meetingNameInput = document.getElementById('meetingName');
  const recipientEmailsInput = document.getElementById('recipientEmails');
  const shareEmailBtn = document.getElementById('shareEmailBtn');
  const emailStatus = document.getElementById('emailStatus');

  // Track processing results for email sharing
  let currentResults = null;

  // Prevent default behaviors for drag events
  ['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
    dropArea.addEventListener(eventName, e => e.preventDefault(), false);
    document.body.addEventListener(eventName, e => e.preventDefault(), false);
  });

  // Highlight drop area when file is dragged over it
  ['dragenter', 'dragover'].forEach(eventName => {
    dropArea.addEventListener(eventName, () => {
      dropArea.classList.add('drag-over');
    }, false);
  });

  // Remove highlight when file is no longer dragged over
  ['dragleave', 'drop'].forEach(eventName => {
    dropArea.addEventListener(eventName, () => {
      dropArea.classList.remove('drag-over');
    }, false);
  });

  // Handle dropped files
  dropArea.addEventListener('drop', e => {
    const files = e.dataTransfer.files;
    handleFileUpload(files[0]);
  }, false);

  // Handle file selection via button
  uploadBtn.addEventListener('click', () => fileInput.click());
  fileInput.addEventListener('change', () => {
    if (fileInput.files.length > 0) {
      handleFileUpload(fileInput.files[0]);
    }
  });

  // Function to show email section after successful processing
  function showEmailSection(results) {
    currentResults = results;
    emailSection.style.display = 'block';
    
    // Default meeting name based on date
    const today = new Date();
    meetingNameInput.value = `Meeting Summary - ${today.toLocaleDateString()}`;
  }

  // Handle email sharing
  shareEmailBtn.addEventListener('click', () => {
    if (!currentResults) {
      emailStatus.textContent = 'No meeting summary to share. Please process an audio file first.';
      emailStatus.className = 'email-status error';
      return;
    }
    
    const meetingName = meetingNameInput.value || 'Meeting Summary';
    const recipientEmails = recipientEmailsInput.value.split(',').map(email => email.trim()).filter(email => email);
    
    if (recipientEmails.length === 0) {
      emailStatus.textContent = 'Please enter at least one recipient email address.';
      emailStatus.className = 'email-status error';
      return;
    }
    
    // Send the email via our API
    emailStatus.textContent = 'Sending email...';
    emailStatus.className = 'email-status';
    
    fetch('http://localhost:8000/send-email/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        meeting_name: meetingName,
        recipients: recipientEmails,
        summary: currentResults.summary,
        action_items: currentResults.action_items
      })
    })
    .then(response => response.json())
    .then(data => {
      if (data.success) {
        emailStatus.textContent = 'Email sent successfully!';
        emailStatus.className = 'email-status success';
      } else {
        emailStatus.textContent = `Failed to send email: ${data.error}`;
        emailStatus.className = 'email-status error';
      }
    })
    .catch(error => {
      emailStatus.textContent = `Error: ${error.message}`;
      emailStatus.className = 'email-status error';
    });
  });

  // File upload and processing function
  function handleFileUpload(file) {
    if (!file) return;
    
    // Show loading state
    resultsSection.style.display = 'block';
    summaryEl.textContent = "Processing file: " + file.name + "... (This may take a minute)";
    actionItemsEl.innerHTML = "<li>Analyzing audio...</li>";
    
    const formData = new FormData();
    formData.append('file', file);
    
    fetch('http://localhost:8000/process-meeting/', {
      method: 'POST',
      body: formData
    })
    .then(response => {
      if (!response.ok) {
        throw new Error('Server responded with status: ' + response.status);
      }
      return response.json();
    })
    .then(data => {
      // Update UI with real results
      summaryEl.textContent = data.summary;
      
      // Check if action_items exists and is an array
      if (data.action_items && Array.isArray(data.action_items)) {
        if (data.action_items.length > 0) {
          actionItemsEl.innerHTML = data.action_items
            .map(item => `<li>${item}</li>`)
            .join('');
        } else {
          actionItemsEl.innerHTML = "<li>No action items identified.</li>";
        }
      } else {
        actionItemsEl.innerHTML = "<li>No action items found in response.</li>";
      }
      
      // Add transcript section
      if (data.transcript) {
        // Remove any existing transcript section first
        const existingTranscript = document.querySelector('#transcriptSection');
        if (existingTranscript) {
          existingTranscript.remove();
        }
        
        const transcriptSection = document.createElement('div');
        transcriptSection.id = 'transcriptSection';
        transcriptSection.innerHTML = `
          <h2>Transcript</h2>
          <p style="white-space: pre-line">${data.transcript}</p>
        `;
        resultsSection.appendChild(transcriptSection);
      }
      
      // Show email sharing section with current results
      showEmailSection(data);
    })
    .catch(error => {
      summaryEl.textContent = "Error: " + error.message;
      actionItemsEl.innerHTML = "<li>Failed to process audio file. Please try again.</li>";
      console.error('Error:', error);
    });
  }
});