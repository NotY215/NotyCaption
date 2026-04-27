// ========================================
// Audio Manager - Handles file upload, Drive upload, and audio playback
// ========================================

const AudioManager = {
    currentAudioDriveId: null,
    currentAudioFile: null,
    currentAudioBlobUrl: null,
    
    init(uploadAreaId, fileInputId, audioPlayerId, fileInfoId) {
        this.uploadArea = document.getElementById(uploadAreaId);
        this.fileInput = document.getElementById(fileInputId);
        this.audioPlayer = document.getElementById(audioPlayerId);
        this.fileInfo = document.getElementById(fileInfoId);
        
        if (!this.uploadArea || !this.fileInput) {
            console.error('Audio Manager: Required elements not found');
            return false;
        }
        
        this.setupEventListeners();
        return true;
    },
    
    setupEventListeners() {
        this.uploadArea.addEventListener('click', () => {
            this.fileInput.click();
        });
        
        this.fileInput.addEventListener('change', (e) => {
            if (e.target.files && e.target.files[0]) {
                this.handleFile(e.target.files[0]);
            }
        });
        
        this.uploadArea.addEventListener('dragover', (e) => {
            e.preventDefault();
            this.uploadArea.classList.add('drag-over');
        });
        
        this.uploadArea.addEventListener('dragleave', () => {
            this.uploadArea.classList.remove('drag-over');
        });
        
        this.uploadArea.addEventListener('drop', (e) => {
            e.preventDefault();
            this.uploadArea.classList.remove('drag-over');
            const file = e.dataTransfer.files[0];
            if (file && this.isAudioFile(file)) {
                this.handleFile(file);
            } else {
                this.showToast('Please drop an audio file', true);
            }
        });
    },
    
    isAudioFile(file) {
        const allowedTypes = ['audio/mpeg', 'audio/wav', 'audio/x-wav', 'audio/mp4', 'audio/x-m4a', 'audio/flac', 'audio/ogg', 'audio/aac'];
        const allowedExtensions = ['.mp3', '.wav', '.m4a', '.flac', '.ogg', '.aac', '.webm'];
        const ext = file.name.substring(file.name.lastIndexOf('.')).toLowerCase();
        return allowedTypes.includes(file.type) || allowedExtensions.includes(ext);
    },
    
    async handleFile(file) {
        if (!this.isAudioFile(file)) {
            this.showToast('❌ Please upload an audio file (MP3, WAV, M4A, FLAC, OGG, AAC)', true);
            return;
        }
        
        if (file.size > 50 * 1024 * 1024) {
            this.showToast('❌ File too large! Max 50MB', true);
            return;
        }
        
        this.currentAudioFile = file;
        
        if (this.currentAudioBlobUrl) {
            URL.revokeObjectURL(this.currentAudioBlobUrl);
        }
        
        this.currentAudioBlobUrl = URL.createObjectURL(file);
        this.audioPlayer.src = this.currentAudioBlobUrl;
        this.fileInfo.innerHTML = `📄 ${file.name} - Uploading to Drive...`;
        this.showToast(`📤 Uploading ${file.name}...`);
        
        await this.uploadToDrive(file);
    },
    
    async uploadToDrive(file) {
        try {
            let token = localStorage.getItem('notycaption_access_token');
            if (!token) {
                const cookies = document.cookie.split(';');
                for (let cookie of cookies) {
                    const [name, value] = cookie.trim().split('=');
                    if (name === 'notycaption_access_token') {
                        token = decodeURIComponent(value);
                        localStorage.setItem('notycaption_access_token', token);
                        break;
                    }
                }
            }
            
            if (!token) {
                throw new Error('Not authenticated');
            }
            
            // Verify token is valid
            const verifyResponse = await fetch('https://www.googleapis.com/oauth2/v2/userinfo', {
                headers: { 'Authorization': `Bearer ${token}` }
            });
            
            if (!verifyResponse.ok) {
                throw new Error('Token expired');
            }
            
            const folderId = await this.getOrCreateFolder(CONFIG.TEMP_FOLDER_NAME, token);
            
            const formData = new FormData();
            const metadata = {
                name: file.name,
                mimeType: file.type,
                parents: [folderId]
            };
            formData.append('metadata', new Blob([JSON.stringify(metadata)], { type: 'application/json' }));
            formData.append('file', file);
            
            const response = await fetch('https://www.googleapis.com/upload/drive/v3/files?uploadType=multipart', {
                method: 'POST',
                headers: { 'Authorization': `Bearer ${token}` },
                body: formData
            });
            
            if (!response.ok) {
                throw new Error(`Upload failed: ${response.status}`);
            }
            
            const data = await response.json();
            this.currentAudioDriveId = data.id;
            this.fileInfo.innerHTML = `📄 ${file.name} - ✅ Uploaded to Drive`;
            this.showToast('✅ Audio uploaded! Click "Generate Captions" to start');
            this.currentAudioName = file.name.replace(/\.(mp3|wav|m4a|flac|ogg|aac)$/i, '');
            if (this.onUploadComplete) {
                this.onUploadComplete(this.currentAudioDriveId, this.currentAudioName);
            }
            if (typeof window.enableCaptionButtons === 'function') {
                window.enableCaptionButtons(true);
            }
            
            
        } catch (err) {
            console.error('Upload error:', err);
            this.showToast('❌ Upload failed: ' + err.message, true);
            this.fileInfo.innerHTML = `📄 ${file.name} - ❌ Upload failed`;
            if (err.message === 'Token expired') {
                setTimeout(() => {
                    window.location.href = 'index.html';
                }, 2000);
            }
        }
    },
    
    async getOrCreateFolder(folderName, token) {
        const query = `name='${folderName}' and mimeType='application/vnd.google-apps.folder' and trashed=false`;
        const response = await fetch(`https://www.googleapis.com/drive/v3/files?q=${encodeURIComponent(query)}&fields=files(id,name)`, {
            headers: { 'Authorization': `Bearer ${token}` }
        });
        
        const data = await response.json();
        
        if (data.files && data.files.length > 0) {
            return data.files[0].id;
        }
        
        const metadata = {
            name: folderName,
            mimeType: 'application/vnd.google-apps.folder'
        };
        
        const createResponse = await fetch('https://www.googleapis.com/drive/v3/files', {
            method: 'POST',
            headers: {
                'Authorization': `Bearer ${token}`,
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(metadata)
        });
        
        const folderData = await createResponse.json();
        return folderData.id;
    },
    
    unloadAudio() {
        if (this.audioPlayer) {
            this.audioPlayer.pause();
            this.audioPlayer.src = '';
        }
        
        if (this.currentAudioBlobUrl) {
            URL.revokeObjectURL(this.currentAudioBlobUrl);
            this.currentAudioBlobUrl = null;
        }
        
        this.currentAudioDriveId = null;
        this.currentAudioFile = null;
        
        if (this.fileInfo) {
            this.fileInfo.innerHTML = 'No file loaded';
        }
        
        if (typeof window.enableCaptionButtons === 'function') {
            window.enableCaptionButtons(false);
        }
        
        const captionsList = document.getElementById('captionsList');
        if (captionsList) {
            captionsList.innerHTML = '<p style="color:#666;text-align:center">No captions yet</p>';
        }
        
        const exportBtn = document.getElementById('exportBtn');
        if (exportBtn) {
            exportBtn.disabled = true;
        }
        
        const enhancedSection = document.getElementById('enhancedSection');
        if (enhancedSection) {
            enhancedSection.style.display = 'none';
        }
        
        const enhancedPlayer = document.getElementById('enhancedPlayer');
        if (enhancedPlayer) {
            enhancedPlayer.src = '';
        }
        
        this.showToast('✅ Audio unloaded');
    },
    
    getAudioDriveId() {
        return {
            id: this.currentAudioDriveId,
            name: this.currentAudioName
        };
    },
    
    showToast(msg, isError = false) {
        if (typeof window.showToast === 'function') {
            window.showToast(msg, isError);
        }
    },
    setOnUploadComplete(callback) {
    this.onUploadComplete = callback;
    },
};

window.AudioManager = AudioManager;