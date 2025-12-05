/**
 * Persons Management Module
 */

class PersonsManager {
    constructor() {
        this.persons = [];
        this.filters = {
            status: '',
            priority: '',
            search: ''
        };
    }

    init() {
        this.setupEventListeners();
        this.loadPersons();
    }

    setupEventListeners() {
        // Add person button
        const addPersonBtn = document.getElementById('addPersonBtn');
        if (addPersonBtn) {
            addPersonBtn.addEventListener('click', () => this.showAddPersonModal());
        }

        // Webcam capture buttons
        const capturePhotoBtn = document.getElementById('capturePhotoBtn');
        if (capturePhotoBtn) {
            capturePhotoBtn.addEventListener('click', () => this.showWebcamModal());
        }

        const uploadPhotoBtn = document.getElementById('uploadPhotoBtn');
        if (uploadPhotoBtn) {
            uploadPhotoBtn.addEventListener('click', () => {
                document.getElementById('personPhoto').click();
            });
        }

        const cancelWebcamBtn = document.getElementById('cancelWebcamBtn');
        if (cancelWebcamBtn) {
            cancelWebcamBtn.addEventListener('click', () => this.closeWebcamModal());
        }

        const captureBtn = document.getElementById('captureBtn');
        if (captureBtn) {
            captureBtn.addEventListener('click', () => this.capturePhoto());
        }

        // Photo file input
        const personPhoto = document.getElementById('personPhoto');
        if (personPhoto) {
            personPhoto.addEventListener('change', (e) => this.handlePhotoUpload(e));
        }

        // Filters
        const statusFilter = document.getElementById('statusFilter');
        const priorityFilter = document.getElementById('priorityFilter');
        const searchInput = document.getElementById('searchInput');

        if (statusFilter) {
            statusFilter.addEventListener('change', (e) => {
                this.filters.status = e.target.value;
                this.loadPersons();
            });
        }

        if (priorityFilter) {
            priorityFilter.addEventListener('change', (e) => {
                this.filters.priority = e.target.value;
                this.loadPersons();
            });
        }

        if (searchInput) {
            searchInput.addEventListener('input', (e) => {
                this.filters.search = e.target.value;
                clearTimeout(this.searchTimeout);
                this.searchTimeout = setTimeout(() => this.loadPersons(), 500);
            });
        }

        // Add person form
        const addPersonForm = document.getElementById('addPersonForm');
        if (addPersonForm) {
            addPersonForm.addEventListener('submit', (e) => this.handleAddPerson(e));
        }

        // Modal close buttons
        document.querySelectorAll('.close-modal').forEach(btn => {
            btn.addEventListener('click', () => this.closeModal());
        });

        // Close modal on outside click
        const modal = document.getElementById('addPersonModal');
        if (modal) {
            modal.addEventListener('click', (e) => {
                if (e.target === modal) {
                    this.closeModal();
                }
            });
        }
    }

    async loadPersons() {
        try {
            const params = {
                limit: 50
            };

            if (this.filters.status) params.status = this.filters.status;
            if (this.filters.priority) params.priority = this.filters.priority;
            if (this.filters.search) params.search = this.filters.search;

            const data = await api.getPersons(params);
            this.persons = data.persons || [];
            this.renderPersons();
        } catch (error) {
            console.error('Error loading persons:', error);
            document.getElementById('personsList').innerHTML = 
                '<p class="no-data">Error loading persons</p>';
        }
    }

    renderPersons() {
        const personsList = document.getElementById('personsList');
        
        if (!this.persons || this.persons.length === 0) {
            personsList.innerHTML = '<p class="no-data">No persons found</p>';
            return;
        }

        personsList.innerHTML = this.persons.map(person => `
            <div class="person-card">
                <div class="person-header">
                    <div>
                        <div class="person-name">${person.name}</div>
                        <div class="person-info">
                            ${person.age ? `Age: ${person.age}` : ''} 
                            ${person.gender ? `• ${person.gender}` : ''}
                        </div>
                    </div>
                    <span class="person-status status-${person.status}">
                        ${person.status}
                    </span>
                </div>
                <div class="person-info">
                    <strong>Priority:</strong> ${person.priority || 'N/A'}<br>
                    ${person.description ? `<strong>Description:</strong> ${person.description}<br>` : ''}
                    ${person.lastSeenLocation ? `<strong>Last Seen:</strong> ${person.lastSeenLocation}<br>` : ''}
                    <strong>Encodings:</strong> ${person.faceEncodings?.length || 0}
                </div>
                <div class="person-actions">
                    <button class="btn btn-primary btn-small" onclick="personsManager.viewPerson('${person._id}')">
                        <i class="fas fa-eye"></i> View
                    </button>
                    <button class="btn btn-secondary btn-small" onclick="personsManager.editPerson('${person._id}')">
                        <i class="fas fa-edit"></i> Edit
                    </button>
                </div>
            </div>
        `).join('');
    }

    showAddPersonModal() {
        const modal = document.getElementById('addPersonModal');
        if (modal) {
            modal.classList.add('active');
            document.getElementById('addPersonForm').reset();
        }
    }

    closeModal() {
        const modal = document.getElementById('addPersonModal');
        if (modal) {
            modal.classList.remove('active');
        }
    }

    async handleAddPerson(e) {
        e.preventDefault();

        const personData = {
            name: document.getElementById('personName').value,
            age: parseInt(document.getElementById('personAge').value) || undefined,
            gender: document.getElementById('personGender').value,
            status: document.getElementById('personStatus').value,
            priority: document.getElementById('personPriority').value,
            description: document.getElementById('personDescription').value,
            lastSeenLocation: document.getElementById('personLocation').value
        };

        try {
            // First, upload photo if available
            let encoding = null;
            if (this.capturedPhotoBlob) {
                console.log('Uploading photo...');
                const formData = new FormData();
                formData.append('photo', this.capturedPhotoBlob, 'person_photo.jpg');
                
                const token = localStorage.getItem('auth_token');
                
                try {
                    const uploadResponse = await fetch(`${CONFIG.API_BASE_URL}/api/upload/person-photo`, {
                        method: 'POST',
                        headers: {
                            'Authorization': `Bearer ${token}`
                        },
                        body: formData
                    });
                    
                    const uploadData = await uploadResponse.json();
                    console.log('Upload response:', uploadData);
                    
                    if (uploadResponse.ok) {
                        encoding = uploadData.encoding;
                        
                        // Add face encoding to person data
                        personData.faceEncodings = [{
                            encoding: encoding,
                            imageUrl: uploadData.imageUrl
                        }];
                        console.log('Face encoding extracted successfully');
                    } else {
                        throw new Error(uploadData.error || 'Failed to upload photo');
                    }
                } catch (uploadError) {
                    console.error('Upload error:', uploadError);
                    throw new Error('Photo upload failed: ' + uploadError.message);
                }
            }

            // Create person
            console.log('Creating person with data:', personData);
            const result = await api.createPerson(personData);
            console.log('Person created:', result);
            
            this.closeModal();
            this.loadPersons();
            
            // Clear captured photo
            this.capturedPhotoBlob = null;
            
            // Show success message
            if (encoding) {
                alert('✅ Person added successfully with face encoding!');
            } else {
                alert('✅ Person added successfully! (No photo provided)');
            }
        } catch (error) {
            console.error('Error adding person:', error);
            
            // Better error message handling
            let errorMessage = 'Unknown error occurred';
            
            if (error.message) {
                errorMessage = error.message;
            } else if (typeof error === 'string') {
                errorMessage = error;
            } else if (error.error) {
                errorMessage = error.error;
            }
            
            alert('❌ Error adding person: ' + errorMessage);
        }
    }

    async viewPerson(id) {
        try {
            const data = await api.getPerson(id);
            const person = data.person;
            
            alert(`Person Details:\n\nName: ${person.name}\nStatus: ${person.status}\nPriority: ${person.priority}\nDescription: ${person.description || 'N/A'}`);
        } catch (error) {
            console.error('Error viewing person:', error);
            alert('Error loading person details');
        }
    }

    async editPerson(id) {
        alert('Edit functionality - To be implemented');
    }

    async deletePerson(id) {
        if (!confirm('Are you sure you want to delete this person?')) {
            return;
        }

        try {
            await api.deletePerson(id);
            this.loadPersons();
            alert('Person deleted successfully');
        } catch (error) {
            console.error('Error deleting person:', error);
            alert('Error deleting person: ' + error.message);
        }
    }

    async showWebcamModal() {
        const webcamModal = document.getElementById('webcamModal');
        if (webcamModal) {
            webcamModal.classList.add('active');
            
            // Start webcam
            const started = await webcamCapture.startWebcam('webcamVideo');
            if (!started) {
                this.closeWebcamModal();
            }
        }
    }

    closeWebcamModal() {
        const webcamModal = document.getElementById('webcamModal');
        if (webcamModal) {
            webcamModal.classList.remove('active');
        }
        
        // Stop webcam
        webcamCapture.stopWebcam();
    }

    async capturePhoto() {
        try {
            const blob = await webcamCapture.capturePhoto();
            const dataURL = webcamCapture.getDataURL();
            
            // Show preview
            const previewImage = document.getElementById('previewImage');
            const photoPreview = document.getElementById('photoPreview');
            
            if (previewImage && photoPreview) {
                previewImage.src = dataURL;
                photoPreview.style.display = 'block';
            }
            
            // Store the blob for upload
            this.capturedPhotoBlob = blob;
            
            // Close webcam modal
            this.closeWebcamModal();
            
        } catch (error) {
            console.error('Error capturing photo:', error);
            alert('Failed to capture photo');
        }
    }

    handlePhotoUpload(e) {
        const file = e.target.files[0];
        if (file) {
            const reader = new FileReader();
            reader.onload = (event) => {
                const previewImage = document.getElementById('previewImage');
                const photoPreview = document.getElementById('photoPreview');
                
                if (previewImage && photoPreview) {
                    previewImage.src = event.target.result;
                    photoPreview.style.display = 'block';
                }
            };
            reader.readAsDataURL(file);
            
            this.capturedPhotoBlob = file;
        }
    }
}

// Create global instance
const personsManager = new PersonsManager();
